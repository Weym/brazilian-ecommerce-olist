import streamlit as st


def apply_global_css():
    """Injeta CSS customizado para melhorar a estética geral."""
    custom_css = """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    [data-testid="metric-container"] {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border-left: 5px solid #e74c3c;
    }

    [data-testid="stSidebar"] {
        background-color: #f0f2f6 !important;
    }
    [data-testid="stSidebarNav"] {
        padding-top: 1rem;
    }

    hr {
        margin: 1.5rem 0 !important;
        border-top: 1px solid #e0e0e0 !important;
    }

    h1, h2, h3 {
        color: #2c3e50 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    .streamlit-expanderHeader {
        background-color: #fdfdfd;
        border-radius: 8px;
    }

    .stButton>button {
        border-radius: 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(231, 76, 60, 0.2);
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


def add_sidebar_branding():
    """Adiciona elementos de marca e navegação ao menu lateral."""
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center; padding-bottom: 1rem;">
                <h1 style="font-size: 1.5rem; margin-bottom: 0;">📦 Olist Risk</h1>
                <p style="font-size: 0.8rem; color: #666;">Monitoramento em Tempo Real</p>
                <div style="display: flex; justify-content: center; align-items: center; gap: 5px; margin-top: 5px;">
                    <span style="height: 10px; width: 10px; background-color: #2ecc71; border-radius: 50%; display: inline-block; animation: pulse 2s infinite;"></span>
                    <span style="font-size: 0.7rem; color: #2ecc71; font-weight: bold; text-transform: uppercase;">Ao vivo</span>
                </div>
            </div>
            <style>
            @keyframes pulse {
                0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(46, 204, 113, 0.7); }
                70% { transform: scale(1); box-shadow: 0 0 0 5px rgba(46, 204, 113, 0); }
                100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(46, 204, 113, 0); }
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.divider()
        st.info("Dica: use o Preditor para simular cenários de risco.")


def page_header(title, icon="📊"):
    """Cria um cabeçalho padronizado para as páginas."""
    st.set_page_config(
        page_title=f"{title} - Olist Risk",
        page_icon=icon,
        layout="wide",
    )
    apply_global_css()
    add_sidebar_branding()
    st.title(f"{icon} {title}")
