import streamlit as st

st.set_page_config(
    page_title="Home — Olist Risk",
    page_icon="📦",
    layout="wide",
)

st.title("Sistema de Alerta de Risco Pre-Entrega — Olist")

st.markdown("""
## O Problema

Avaliacoes ruins (1–2 estrelas) custam clientes e reputacao.
A maioria e causada por problemas logisticos — atraso, frete caro, rotas criticas.

**Podemos prever o risco antes da entrega acontecer.**

---

## O que Este Dashboard Faz

| Pagina | O que mostra | Dados usados |
|--------|-------------|-------------|
| **Preditor de Risco** | Score 0–100% de risco para um pedido | Pipeline XGBoost (Phase 4) |
| **Mapa Geografico** | Concentracao de avaliacoes ruins por UF | geo_aggregated.parquet (Phase 3) |
| **Painel de EDA** | Evidencias visuais do impacto logistico | Figuras PNG exportadas (Phase 3) |

---

## Como Usar

Use o menu lateral para navegar entre as paginas.

**Teste rapido:** Va em **Preditor de Risco**, insira frete alto (R$ 80+), prazo longo (30+ dias),
UF origem SP e destino AM — o score deve mostrar risco alto (vermelho).
""")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Features pre-entrega", "5", help="Disponiveis antes da expedicao")
with col2:
    st.metric("Modelo", "XGBoost", help="Treinado na Phase 4")
with col3:
    st.metric("Dados ao vivo", "Nenhum", help="Todos artefatos sao pre-computados")
