import streamlit as st
from utils.ui import page_header

page_header("Home", icon="📦")

st.markdown("""
## O Problema

Avaliações ruins (1–2 estrelas) custam clientes e reputação.
A maioria é causada por problemas logísticos — atraso, frete caro, rotas críticas.

**Podemos prever o risco antes da entrega acontecer.**

---

## O que Este Dashboard Faz

| Página | O que mostra | Dados usados |
|--------|-------------|-------------|
| **Preditor de Risco** | Score 0–100% de risco para um pedido | Pipeline XGBoost (Phase 4) |
| **Mapa Geográfico** | Concentração de avaliações ruins por UF | geo_aggregated.parquet (Phase 3) |
| **Painel de EDA** | Evidências visuais do impacto logístico | Figuras PNG exportadas (Phase 3) |

---

## Como Usar

Use o menu lateral para navegar entre as páginas.

**Teste rápido:** Vá em **Preditor de Risco**, insira frete alto (R$ 80+), prazo longo (30+ dias),
UF origem SP e destino AM — o score deve mostrar risco alto (vermelho).
""")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Features pré-entrega", "5", help="Disponíveis antes da expedição")
with col2:
    st.metric("Modelo", "XGBoost", help="Treinado na Phase 4")
with col3:
    st.metric("Dados ao vivo", "Nenhum", help="Todos artefatos são pré-computados")
