import streamlit as st

def apply_global_css():
    """Injeta CSS customizado para melhorar a estética geral."""
    custom_css = """
    <style>
    /* Estilo para métricas: bordas arredondadas e sombra suave */
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

    /* Estilo para o sidebar */
    [data-testid="stSidebar"] {
        background-color: #f0f2f6 !important;
    }
    [data-testid="stSidebarNav"] {
        padding-top: 1rem;
    }

    /* Estilo para dividers */
    hr {
        margin: 1.5rem 0 !important;
        border-top: 1px solid #e0e0e0 !important;
    }

    /* Melhoria tipográfica geral */
    h1, h2, h3 {
        color: #2c3e50 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    /* Estilo para expanders */
    .streamlit-expanderHeader {
        background-color: #fdfdfd;
        border-radius: 8px;
    }

    /* Ajuste para botões primários */
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
    """Adiciona elementos de marca e navegação customizada ao sidebar."""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding-bottom: 1rem;">
            <h1 style="font-size: 1.5rem; margin-bottom: 0;">📦 Olist Risk</h1>
            <p style="font-size: 0.8rem; color: #666;">Sistema de Monitoramento e Previsão</p>
        </div>
        """, unsafe_allow_html=True)
        st.divider()

        # Navigation is handled by Streamlit (Multi-page app structure)
        # We can add a footer or info box here
        st.info("**💡 Dica:** Use o Preditor de Risco para simular novos pedidos.")

        st.sidebar.markdown("---")
        st.sidebar.markdown(
            '<div style="text-align: center; font-size: 0.7rem; color: #999;">'
            'Phase 6 | Brazilian Ecommerce Olist'
            '</div>',
            unsafe_allow_html=True
        )

def page_header(title, icon="📊"):
    """Cria um cabeçalho padronizado para as páginas."""
    st.set_page_config(
        page_title=f"{title} — Olist Risk",
        page_icon=icon,
        layout="wide",
    )
    apply_global_css()
    add_sidebar_branding()
    st.title(f"{icon} {title}")
