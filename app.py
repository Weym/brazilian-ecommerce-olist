import streamlit as st

st.set_page_config(
    page_title="Olist Risk Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Olist — Sistema de Alerta de Risco Pre-Entrega")
st.markdown("""
Bem-vindo ao dashboard de risco logistico da Olist. Use o menu lateral para navegar:

- **Preditor de Risco**: Estime o risco de avaliacao ruim para um pedido antes da entrega
- **Mapa Geografico**: Visualize concentracao de avaliacoes ruins por estado brasileiro
- **Painel de EDA**: Explore as analises do Ato 1 — logistica degrada satisfacao
""")
st.info("Todos os dados sao pre-computados. Nenhum processamento pesado ocorre ao vivo.")
