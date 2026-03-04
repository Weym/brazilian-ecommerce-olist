import streamlit as st
from utils.ui import page_header

page_header("Painel Olist Risk", icon="📦")

st.markdown("""
Bem-vindo ao dashboard de risco logístico da Olist. Use o menu lateral para navegar:

- **Preditor de Risco**: Estime o risco de avaliação ruim para um pedido antes da entrega
- **Mapa Geográfico**: Visualize concentração de avaliações ruins por estado brasileiro
- **Painel de EDA**: Explore as análises do Ato 1 — logística degrada satisfação
""")
st.info("Todos os dados são pré-computados. Nenhum processamento pesado ocorre ao vivo.")
