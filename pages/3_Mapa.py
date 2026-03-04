import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.loaders import load_geo_data, load_brazil_geojson
from utils.ui import page_header

page_header("Mapa Geográfico", icon="🗺️")


def detect_column(df: pd.DataFrame, candidates: list, default: str) -> str:
    """Detecta nome de coluna tentando candidatos em ordem. Retorna default se nenhum encontrado."""
    for c in candidates:
        if c in df.columns:
            return c
    return default


st.markdown("Concentração de avaliações ruins (1-2 estrelas) por UF de destino.")

# Carregamento via loaders (cache_data — instantaneo apos primeira visita)
df_raw = load_geo_data()
geojson = load_brazil_geojson()

# Detectar colunas (OPEN QUESTION — dependem de Phase 3)
COL_UF_DEST   = detect_column(df_raw, ["uf_destino", "customer_state", "estado_destino"], "uf_destino")
COL_UF_ORIG   = detect_column(df_raw, ["uf_origem", "seller_state", "estado_origem"], "uf_origem")
COL_PCT_BAD   = detect_column(df_raw, ["pct_bad_review", "bad_review_rate", "taxa_bad_review", "pct_ruim"], "pct_bad_review")
COL_ATRASO    = detect_column(df_raw, ["avg_dias_atraso", "atraso_medio_dias", "delay_avg_days", "dias_atraso_medio"], "atraso_medio_dias")
COL_VOLUME    = detect_column(df_raw, ["volume_pedidos", "total_orders", "n_pedidos"], "volume_pedidos")
COL_CATEGORIA = detect_column(df_raw, ["categoria", "product_category_name_english", "category"], "categoria")
COL_FAIXA     = detect_column(df_raw, ["faixa_risco", "risk_level", "nivel_risco"], "faixa_risco")

# Normalizar pct_bad_review para escala 0-100 se necessario
df = df_raw.copy()
if COL_PCT_BAD in df.columns and df[COL_PCT_BAD].max() <= 1.01:
    df["pct_bad_review_pct"] = df[COL_PCT_BAD] * 100
    col_color = "pct_bad_review_pct"
    color_label = "% Aval. Ruins"
else:
    col_color = COL_PCT_BAD
    color_label = "% Aval. Ruins"

# Calcular faixa de risco se coluna nao existir no parquet
if COL_FAIXA not in df.columns:
    threshold_bad = df[col_color].quantile(0.67)
    threshold_low = df[col_color].quantile(0.33)
    df["faixa_risco"] = pd.cut(
        df[col_color],
        bins=[-1, threshold_low, threshold_bad, float("inf")],
        labels=["Baixo", "Medio", "Alto"],
    )
    COL_FAIXA = "faixa_risco"

# --- Filtros ---
# geo_aggregated.parquet e agregado por UF de destino (27 linhas).
# Nao ha colunas de UF origem ou categoria neste nivel de agregacao.
st.subheader("Filtros")
col1, col2 = st.columns(2)

with col1:
    opts_dest = sorted(df[COL_UF_DEST].dropna().unique().tolist()) if COL_UF_DEST in df.columns else []
    uf_dest_filter = st.multiselect("UF Destino", options=opts_dest, default=[],
                                    help="Filtrar por estado do comprador")
with col2:
    faixa_filter = st.multiselect("Faixa de Risco", options=["Baixo", "Medio", "Alto"], default=[],
                                   help="Faixa de risco calculada por % de avaliacoes ruins")

# Aplicar filtros sem mutar df cacheado
df_filtered = df.copy()
if uf_dest_filter and COL_UF_DEST in df_filtered.columns:
    df_filtered = df_filtered[df_filtered[COL_UF_DEST].isin(uf_dest_filter)]
if faixa_filter and COL_FAIXA in df_filtered.columns:
    df_filtered = df_filtered[df_filtered[COL_FAIXA].isin(faixa_filter)]

# --- Agregacao por UF destino para o choropleth ---
# O choropleth precisa de uma linha por UF de destino
agg_dict = {col_color: "mean"}
if COL_ATRASO in df_filtered.columns:
    agg_dict[COL_ATRASO] = "mean"
if COL_VOLUME in df_filtered.columns:
    agg_dict[COL_VOLUME] = "sum"

if COL_UF_DEST not in df_filtered.columns or df_filtered.empty:
    st.warning("Sem dados para os filtros selecionados.")
    st.stop()

df_map = df_filtered.groupby(COL_UF_DEST, as_index=False).agg(agg_dict)

# --- Hover customizado ---
hover_data = {col_color: ":.1f"}
if COL_ATRASO in df_map.columns:
    hover_data[COL_ATRASO] = ":.1f"
if COL_VOLUME in df_map.columns:
    hover_data[COL_VOLUME] = ":,"

# --- Choropleth ---
fig = px.choropleth(
    df_map,
    geojson=geojson,
    locations=COL_UF_DEST,
    featureidkey="properties.sigla",   # CRITICO: campo correto no GeoJSON codeforamerica
    color=col_color,
    color_continuous_scale="Reds",
    hover_name=COL_UF_DEST,
    hover_data=hover_data,
    labels={
        col_color: color_label,
        COL_ATRASO: "Atraso Medio (dias)",
        COL_VOLUME: "Volume de Pedidos",
    },
    title="% Avaliacoes Ruins por UF de Destino",
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    height=500,
    coloraxis_colorbar=dict(title=color_label),
)

st.plotly_chart(fig, use_container_width=True)

# Metricas resumo
if not df_map.empty:
    m1, m2, m3 = st.columns(3)
    with m1:
        if col_color in df_map.columns:
            worst_uf = df_map.loc[df_map[col_color].idxmax(), COL_UF_DEST]
            st.metric("UF com Mais Risco", worst_uf)
    with m2:
        if COL_ATRASO in df_map.columns:
            st.metric("Atraso Medio Geral", f"{df_map[COL_ATRASO].mean():.1f} dias")
    with m3:
        if COL_VOLUME in df_map.columns:
            st.metric("Pedidos no Filtro", f"{int(df_map[COL_VOLUME].sum()):,}")

# Debug expandivel — facilita ajuste de nomes de colunas apos Phase 3 ser executada
with st.expander("Debug: colunas do geo_aggregated.parquet"):
    st.write("Colunas detectadas:", df_raw.columns.tolist())
    st.write("Mapeamento usado:", {
        "UF destino": COL_UF_DEST, "UF origem": COL_UF_ORIG,
        "% bad review": COL_PCT_BAD, "Atraso": COL_ATRASO,
        "Volume": COL_VOLUME, "Categoria": COL_CATEGORIA,
    })
    st.dataframe(df_raw.head(5))
