import streamlit as st
from utils.ui import page_header

page_header("Início", icon="📦")

st.subheader("Objetivo do Projeto")
st.markdown(
    """
Reduzir avaliações ruins (notas 1-2) com ação preventiva antes da entrega.
O foco é identificar risco logístico cedo para priorizar operação e atendimento.
"""
)

st.subheader("Fluxo das Páginas")
st.markdown(
    """
1. **Visão Exploratória**: principais descobertas e hipótese central.  
2. **EDA**: evidências visuais-chave das análises.  
3. **Mapa**: priorização geográfica de risco.  
4. **Preditor**: demonstração prática e ação recomendada.
"""
)

st.subheader("Hipótese Principal")
st.markdown(
    """
Pedidos com sinais logísticos desfavoráveis (atraso potencial, frete relativo alto,
rotas críticas e algumas categorias) têm maior chance de receber nota 1-2.
"""
)

st.subheader("Como Ler o Dashboard")
st.markdown(
    """
- Comece na Visão Exploratória para entender o problema e os drivers.  
- Use EDA e Mapa para validar onde o risco aparece com mais força.  
- Termine no Preditor para simular pedidos e decidir a ação operacional.
"""
)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Problema", "Nota 1-2")
with c2:
    st.metric("Foco", "Pré-entrega")
with c3:
    st.metric("Decisão", "Ação preventiva")
