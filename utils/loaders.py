"""
utils/loaders.py — Central de carregamento de artefatos pre-computados.

REGRA: Nenhuma pagina le arquivos diretamente. Tudo passa por aqui.
- @st.cache_resource: modelos ML (joblib) — objeto global nao copiado entre sessoes
- @st.cache_data: DataFrames, JSON, listas — serializados, copiados por sessao
"""
import json
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

BASE = Path(__file__).parent.parent  # raiz do projeto


@st.cache_resource
def load_pipeline():
    """
    Carrega o pipeline XGBoost serializado da Phase 4.
    CRITICO: @st.cache_resource — modelos ML NAO sao serializaveis com cache_data.
    """
    path = BASE / "models" / "final_pipeline.joblib"
    if not path.exists():
        raise FileNotFoundError(
            f"Pipeline nao encontrado em {path}. "
            "Execute a Phase 4 antes de iniciar o app."
        )
    return joblib.load(path)


@st.cache_data
def load_geo_data() -> pd.DataFrame:
    """
    Carrega dados geograficos pre-computados da Phase 3 (EDA-03).
    OPEN QUESTION: Nomes exatos das colunas dependem do Phase 3.
    Esperado: uf_destino, uf_origem, pct_bad_review, atraso_medio_dias, volume_pedidos, categoria
    Verificar com: df.columns.tolist() antes de usar.
    """
    path = BASE / "data" / "processed" / "geo_aggregated.parquet"
    if not path.exists():
        raise FileNotFoundError(
            f"geo_aggregated.parquet nao encontrado em {path}. "
            "Execute a Phase 3 antes de iniciar o app."
        )
    df = pd.read_parquet(path)
    return df


@st.cache_data
def load_threshold() -> float:
    """
    Carrega o threshold operacional definido na Phase 4 (ML-05).
    Fallback: 0.5 se models/threshold.json nao existir.
    Para gauge tri-color: threshold_low = threshold * 0.6, threshold_high = threshold.
    """
    threshold_path = BASE / "models" / "threshold.json"
    if threshold_path.exists():
        with open(threshold_path) as f:
            data = json.load(f)
            # Aceita tanto {"threshold": 0.4} quanto valor direto
            return data.get("threshold", data) if isinstance(data, dict) else float(data)
    # Fallback se Phase 4 nao exportou threshold.json
    return 0.5


@st.cache_data
def load_brazil_geojson() -> dict:
    """
    Carrega GeoJSON dos estados brasileiros.
    Usa arquivo local em data/geo/brazil-states.geojson (Plano B offline).
    Fallback: URL do codeforamerica se arquivo local nao existir.
    featureidkey correto: 'properties.sigla' (string como 'SP', 'RJ').
    """
    local_path = BASE / "data" / "geo" / "brazil-states.geojson"
    if local_path.exists():
        with open(local_path, encoding="utf-8") as f:
            return json.load(f)
    # Fallback online (requer internet — nao confiavel em apresentacao ao vivo)
    from urllib.request import urlopen
    url = (
        "https://raw.githubusercontent.com/codeforamerica/click_that_hood"
        "/master/public/data/brazil-states.geojson"
    )
    with urlopen(url) as resp:
        return json.load(resp)


@st.cache_data
def list_eda_figures() -> list:
    """
    Lista arquivos PNG em reports/figures/ ordenados por nome.
    Retorna lista de objetos Path.
    """
    fig_dir = BASE / "reports" / "figures"
    if not fig_dir.exists():
        return []
    return sorted(fig_dir.glob("*.png"))


@st.cache_data
def load_categories_and_ufs() -> tuple:
    """
    Extrai listas unicas de categorias e UFs do geo_data.
    Usado pelo formulario do Preditor para popular os selectbox.
    Retorna: (lista_categorias_ordenadas, lista_ufs_ordenadas)
    OPEN QUESTION: nome da coluna de categoria depende do Phase 3.
    Tentativa: 'categoria', fallback: 'product_category_name_english'
    """
    df = load_geo_data()

    # Detectar coluna de categoria
    cat_col = None
    for candidate in ["categoria", "product_category_name_english", "category"]:
        if candidate in df.columns:
            cat_col = candidate
            break

    categories = sorted(df[cat_col].dropna().unique().tolist()) if cat_col else []

    # UFs — detectar coluna
    uf_col = None
    for candidate in ["uf_destino", "customer_state", "uf"]:
        if candidate in df.columns:
            uf_col = candidate
            break

    ufs = sorted(df[uf_col].dropna().unique().tolist()) if uf_col else [
        "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT",
        "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"
    ]

    return categories, ufs
