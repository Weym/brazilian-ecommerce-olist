import streamlit as st

# Navegação explícita para evitar o item "app" no menu lateral.
pg = st.navigation(
    [
        st.Page("pages/1_Home.py", title="Home"),
        st.Page("pages/2_Visão_Exploratória.py", title="Visão Exploratória"),
        st.Page("pages/3_EDA.py", title="EDA"),
        st.Page("pages/4_Mapa.py", title="Mapa"),
        st.Page("pages/5_Preditor.py", title="Preditor"),
    ]
)

pg.run()
