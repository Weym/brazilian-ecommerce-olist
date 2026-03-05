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
from utils.ui import page_header

# CRITICO: page_header deve ser a primeira chamada Streamlit
page_header("Preditor de Risco", icon="⚡")

# ---------------------------------------------------------------------------
# Carregamento de artefatos no topo do modulo
# Cache aquece na primeira visita, instantaneo nas seguintes
# ---------------------------------------------------------------------------
pipeline = load_pipeline()
threshold = load_threshold()
categories, ufs = load_categories_and_ufs()

# Thresholds visuais calibrados na distribuicao real do modelo (scores 36-48%).
# O threshold operacional (0.785) tem Recall=0.02 — quase nada cruza esse valor.
# Para a demo ser ilustrativa, as bandas visuais refletem percentis da distribuicao:
#   Verde  < 38%  — padrao, sem alerta
#   Amarelo 38-44% — monitorar
#   Vermelho > 44% — contato preventivo
# O marcador operacional (0.785) aparece no gauge como referencia de calibracao.
THRESHOLD_LOW = 0.38
THRESHOLD_HIGH = 0.44

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

# Presets confirmados por probe empírico no pipeline real
# Formato: (label, freight, price, days, category, seller, customer)
_PRESETS = {
    "-- selecione um exemplo --": None,
    "Verde (~29%) — Frete alto, categoria incomum: MG→RR, garden_tools":
        (90, 60, 35, "garden_tools", "MG", "RR"),
    "Verde (~30%) — Frete alto, categoria brinquedos: PE→AM, toys":
        (75, 55, 28, "toys", "PE", "AM"),
    "Verde (~36%) — Produto barato de bebê: BA→PA, baby":
        (65, 45, 32, "baby", "BA", "PA"),
    "Verde (~38%) — Eletrônicos, preço alto: MG→SP, electronics":
        (15, 350, 7, "electronics", "MG", "SP"),
    "Amarelo (~41%) — Móveis, rota longa: SP→AM, furniture_decor":
        (80, 50, 30, "furniture_decor", "SP", "AM"),
    "Amarelo (~41%) — Esportes, rota regional: RJ→BA, sports_leisure":
        (45, 90, 20, "sports_leisure", "RJ", "BA"),
    "Amarelo (~43%) — Informática, prazo curto: SC→PR, computers":
        (10, 250, 8, "computers_accessories", "SC", "PR"),
    "Vermelho (~45%) — Cama/mesa/banho: SP→AM, bed_bath_table":
        (55, 70, 22, "bed_bath_table", "SP", "CE"),
    "Vermelho (~48%) — Cama/mesa/banho, rota Norte: SP→PA":
        (60, 80, 25, "bed_bath_table", "SP", "PA"),
    "Vermelho (~45%) — Beleza/saúde, rota curta: SP→SP, health_beauty":
        (12, 180, 5, "health_beauty", "SP", "SP"),
    "Vermelho (~55%) — Beleza/saúde, SP→RJ, health_beauty":
        (25, 200, 10, "health_beauty", "SP", "RJ"),
    "Vermelho (~57%) — Beleza/saúde, entrega local: RJ→RJ":
        (20, 150, 8, "health_beauty", "RJ", "RJ"),
}


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
                "line": {"color": "#2c3e50", "width": 3},
                "thickness": 0.75,
                "value": threshold * 100,  # marca o threshold operacional (78.5%)
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
st.markdown(
    "Insira as características do pedido para estimar a probabilidade de "
    "avaliação ruim (1-2 estrelas) **antes da entrega**."
)
st.divider()

# ---------------------------------------------------------------------------
# Presets de demonstracao
# ---------------------------------------------------------------------------
st.subheader("Exemplos prontos por faixa de risco")
preset_key = st.selectbox(
    "Carregar exemplo:",
    options=list(_PRESETS.keys()),
    index=0,
    help="Selecione um exemplo para preencher o formulario automaticamente",
)
preset = _PRESETS[preset_key]

# Valores iniciais: preset ou defaults do formulario
if preset:
    _fv, _pr, _days, _cat, _sell, _cust = preset
else:
    _fv, _pr, _days, _cat, _sell, _cust = 17.17, 86.80, 22, "health_beauty", "SP", "RJ"

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
            value=float(_fv),
            step=0.5,
            help="Frete cobrado no pedido (mediana Olist: R$ 17,17)",
        )
        price = st.number_input(
            "Preco do Produto (R$)",
            min_value=0.01,
            max_value=10000.0,
            value=float(_pr),
            step=1.0,
            help="Valor total do produto — usado para calcular proporcao frete/preco",
        )
        estimated_delivery_days = st.number_input(
            "Prazo Estimado de Entrega (dias)",
            min_value=1,
            max_value=90,
            value=int(_days),
            step=1,
            help="Dias corridos entre aprovacao do pedido e data estimada de entrega",
        )

    with col2:
        product_category_name_english = st.selectbox(
            "Categoria do Produto",
            options=categories,
            index=categories.index(_cat) if _cat in categories else 0,
            help="Categoria do produto no catalogo Olist (71 categorias)",
        )
        seller_state = st.selectbox(
            "UF de Origem (vendedor)",
            options=ufs,
            index=ufs.index(_sell) if _sell in ufs else 0,
            help="Estado onde o vendedor esta localizado",
        )
        customer_state = st.selectbox(
            "UF de Destino (comprador)",
            options=ufs,
            index=ufs.index(_cust) if _cust in ufs else 0,
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

        st.caption(
            f"Banda vertical no gauge = threshold operacional ({threshold*100:.1f}%) — "
            "ponto de alta precisão (40% dos flagrados são risco real). "
            "Cores mostram posição relativa na distribuição do modelo."
        )

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
