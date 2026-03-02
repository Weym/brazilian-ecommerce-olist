"""
Pagina 2: Preditor de Risco Pre-Entrega

Demo ao vivo: o apresentador digita caracteristicas de um pedido hipotetico
e a plateia ve o score de risco em tempo real via gauge Plotly.

Arquitetura:
- Formulario com 6 inputs visiveis ao usuario (features pre-entrega)
- Features adicionais preenchidas com medianas do dataset (transparentes ao usuario)
- Pipeline XGBoost carregado via @st.cache_resource (instantaneo apos warm-up)
- Gauge go.Indicator com faixas verde/amarelo/vermelho
- Acao recomendada especifica por faixa de risco
"""
import sys
from pathlib import Path

# Adicionar raiz ao path para importar utils e src
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.loaders import load_pipeline, load_threshold, load_categories_and_ufs

# CRITICO: st.set_page_config deve ser a primeira chamada Streamlit
st.set_page_config(
    page_title="Preditor de Risco — Olist",
    page_icon="⚡",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Carregamento de artefatos no topo do modulo
# Cache aquece na primeira visita, instantaneo nas seguintes
# ---------------------------------------------------------------------------
pipeline = load_pipeline()
threshold = load_threshold()
categories, ufs = load_categories_and_ufs()

# Thresholds tri-color derivados do threshold operacional da Phase 4 (ML-05)
# threshold = 0.785 (Precision=0.40 na curva PR)
# THRESHOLD_LOW = abaixo deste valor: risco baixo (verde)
# THRESHOLD_HIGH = acima deste valor: risco alto (vermelho)
THRESHOLD_LOW = threshold * 0.6    # ~0.471
THRESHOLD_HIGH = threshold         # ~0.785

# Valores default (medianas do dataset Olist — Phase 2 gold table)
# Usados para features que o formulario nao expoe ao usuario
_DEFAULTS = {
    "freight_ratio": None,              # calculado dinamicamente: freight_value / price
    "seller_customer_distance_km": 434.33,
    "product_weight_g": 700.0,
    "product_volume_cm3": 6400.0,
    "order_item_count": 1,
    "payment_type": "credit_card",
    "payment_installments": 2,
}

# Garantir que listas nao estejam vazias (fallback hardcoded)
_FALLBACK_CATEGORIES = [
    "health_beauty", "sports_leisure", "furniture_decor", "bed_bath_table",
    "housewares", "computers_accessories", "toys", "watches_gifts",
    "telephony", "garden_tools", "baby", "electronics", "cool_stuff",
    "perfumery", "auto",
]
_FALLBACK_UFS = [
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA",
    "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN",
    "RO", "RR", "RS", "SC", "SE", "SP", "TO",
]

if not categories:
    categories = _FALLBACK_CATEGORIES
if not ufs:
    ufs = _FALLBACK_UFS


# ---------------------------------------------------------------------------
# Gauge builder
# ---------------------------------------------------------------------------

def build_gauge(prob: float) -> tuple:
    """
    Transforma probabilidade float 0-1 em gauge visual go.Indicator e acao recomendada.

    Parameters
    ----------
    prob : float
        Probabilidade de avaliacao ruim (0.0 a 1.0) retornada pelo pipeline.

    Returns
    -------
    tuple[go.Figure, str]
        (fig, action_text)
    """
    pct = prob * 100  # exibir como 0-100%

    if prob < THRESHOLD_LOW:
        action = "Sem acao necessaria — pedido dentro do padrao"
        bar_color = "#2ecc71"   # verde
        risk_label = "Risco Baixo"
    elif prob < THRESHOLD_HIGH:
        action = "Monitorar — acompanhar prazo e rastrear entrega"
        bar_color = "#f39c12"   # amarelo
        risk_label = "Risco Medio"
    else:
        action = "Contato preventivo via WhatsApp antes da data estimada de entrega"
        bar_color = "#e74c3c"   # vermelho
        risk_label = "Risco Alto"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pct,
        number={"suffix": "%", "font": {"size": 48}},
        title={
            "text": (
                f"Score de Risco Pre-Entrega"
                f"<br><span style='font-size:0.75em;color:{bar_color}'>"
                f"<b>{risk_label}</b></span>"
            )
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": "darkgray",
                "tickfont": {"size": 12},
            },
            "bar": {"color": bar_color, "thickness": 0.3},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "lightgray",
            "steps": [
                {"range": [0, THRESHOLD_LOW * 100], "color": "#d5f5e3"},          # verde claro
                {"range": [THRESHOLD_LOW * 100, THRESHOLD_HIGH * 100], "color": "#fdebd0"},   # amarelo claro
                {"range": [THRESHOLD_HIGH * 100, 100], "color": "#fadbd8"},        # vermelho claro
            ],
            "threshold": {
                "line": {"color": "black", "width": 4},
                "thickness": 0.75,
                "value": pct,
            },
        },
    ))
    fig.update_layout(
        height=350,
        margin={"t": 80, "b": 10, "l": 40, "r": 40},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig, action


# ---------------------------------------------------------------------------
# UI — Cabecalho
# ---------------------------------------------------------------------------
st.title("Preditor de Risco Pre-Entrega")
st.markdown(
    "Insira as caracteristicas do pedido para estimar a probabilidade de "
    "avaliacao ruim (1-2 estrelas) **antes da entrega**."
)
st.divider()

# ---------------------------------------------------------------------------
# Formulario de entrada
# ---------------------------------------------------------------------------
with st.form("preditor_form"):
    st.subheader("Caracteristicas do Pedido")

    col1, col2 = st.columns(2)

    with col1:
        freight_value = st.number_input(
            "Valor do Frete (R$)",
            min_value=0.0,
            max_value=500.0,
            value=17.17,
            step=0.5,
            help="Frete cobrado no pedido (mediana Olist: R$ 17,17)",
        )
        price = st.number_input(
            "Preco do Produto (R$)",
            min_value=0.01,
            max_value=10000.0,
            value=86.80,
            step=1.0,
            help="Valor total do produto — usado para calcular proporcao frete/preco",
        )
        estimated_delivery_days = st.number_input(
            "Prazo Estimado de Entrega (dias)",
            min_value=1,
            max_value=90,
            value=22,
            step=1,
            help="Dias corridos entre aprovacao do pedido e data estimada de entrega",
        )

    with col2:
        product_category_name_english = st.selectbox(
            "Categoria do Produto",
            options=categories,
            index=categories.index("health_beauty") if "health_beauty" in categories else 0,
            help="Categoria do produto no catalogo Olist (71 categorias)",
        )
        seller_state = st.selectbox(
            "UF de Origem (vendedor)",
            options=ufs,
            index=ufs.index("SP") if "SP" in ufs else 0,
            help="Estado onde o vendedor esta localizado",
        )
        customer_state = st.selectbox(
            "UF de Destino (comprador)",
            options=ufs,
            index=ufs.index("RJ") if "RJ" in ufs else 0,
            help="Estado do comprador",
        )

    submitted = st.form_submit_button(
        "Calcular Risco",
        type="primary",
        use_container_width=True,
    )

# ---------------------------------------------------------------------------
# Inferencia e exibicao dos resultados
# ---------------------------------------------------------------------------
if submitted:
    # Calcular freight_ratio dinamicamente
    freight_ratio = freight_value / price if price > 0 else 0.18

    # Construir DataFrame com TODOS os campos que o pipeline espera
    # Ordem dos campos deve bater com PRE_DELIVERY_FEATURES de src/features.py
    input_data = {
        "freight_value": freight_value,
        "price": price,
        "freight_ratio": freight_ratio,
        "estimated_delivery_days": estimated_delivery_days,
        "seller_state": seller_state,
        "customer_state": customer_state,
        "seller_customer_distance_km": _DEFAULTS["seller_customer_distance_km"],
        "product_weight_g": _DEFAULTS["product_weight_g"],
        "product_volume_cm3": _DEFAULTS["product_volume_cm3"],
        "product_category_name_english": product_category_name_english,
        "order_item_count": _DEFAULTS["order_item_count"],
        "payment_type": _DEFAULTS["payment_type"],
        "payment_installments": _DEFAULTS["payment_installments"],
    }
    input_df = pd.DataFrame([input_data])

    try:
        # CRITICO: apenas predict_proba() — nenhum treino ou join ocorre aqui
        prob = pipeline.predict_proba(input_df)[0, 1]
        fig, action = build_gauge(prob)

        # Exibir gauge
        st.plotly_chart(fig, use_container_width=True)

        # Acao recomendada em destaque visual
        if prob < THRESHOLD_LOW:
            st.success(f"**Acao Recomendada:** {action}")
        elif prob < THRESHOLD_HIGH:
            st.warning(f"**Acao Recomendada:** {action}")
        else:
            st.error(f"**Acao Recomendada:** {action}")

        # Detalhes para apresentacao (expander nao atrapalha o fluxo principal)
        with st.expander("Detalhes do calculo (para apresentacao)"):
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.metric("Probabilidade bruta", f"{prob:.4f}")
                st.metric("Threshold operacional (Phase 4)", f"{threshold:.4f}")
            with col_d2:
                st.metric("Threshold baixo (x0.6)", f"{THRESHOLD_LOW:.4f}")
                st.metric("Freight ratio calculado", f"{freight_ratio:.4f}")
            st.caption(
                "Features nao expostas no formulario usam medianas do dataset Olist: "
                "distancia=434 km, peso=700g, volume=6400cm3, 1 item, credito, 2 parcelas."
            )
            st.dataframe(input_df, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao calcular risco: {e}")
        st.info(
            "Verifique se os nomes das colunas batem com PRE_DELIVERY_FEATURES de "
            "src/features.py. "
            f"Colunas enviadas: {list(input_data.keys())}"
        )
        with st.expander("Traceback completo"):
            import traceback
            st.code(traceback.format_exc())
