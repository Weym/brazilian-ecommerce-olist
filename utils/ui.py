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


CATEGORY_PT_MAP = {
    'agro_industry_and_commerce': 'Agro, Indústria e Comércio',
    'air_conditioning': 'Ar-condicionado',
    'art': 'Arte',
    'arts_and_craftmanship': 'Artes e Artesanato',
    'audio': 'Áudio',
    'auto': 'Automotivo',
    'baby': 'Bebê',
    'bed_bath_table': 'Cama, Mesa e Banho',
    'books_general_interest': 'Livros de Interesse Geral',
    'books_imported': 'Livros Importados',
    'books_technical': 'Livros Técnicos',
    'cds_dvds_musicals': 'CDs, DVDs e Musicais',
    'christmas_supplies': 'Artigos de Natal',
    'cine_photo': 'Cine e Foto',
    'computers': 'Computadores',
    'computers_accessories': 'Informática e Acessórios',
    'consoles_games': 'Consoles e Games',
    'construction_tools_construction': 'Ferramentas para Construção',
    'construction_tools_lights': 'Ferramentas e Iluminação',
    'construction_tools_safety': 'Ferramentas e Segurança',
    'cool_stuff': 'Produtos Criativos',
    'costruction_tools_garden': 'Ferramentas para Jardim',
    'costruction_tools_tools': 'Ferramentas em Geral',
    'diapers_and_hygiene': 'Fraldas e Higiene',
    'drinks': 'Bebidas',
    'dvds_blu_ray': 'DVDs e Blu-ray',
    'electronics': 'Eletrônicos',
    'fashio_female_clothing': 'Moda Feminina',
    'fashion_bags_accessories': 'Bolsas e Acessórios',
    'fashion_childrens_clothes': 'Moda Infantil',
    'fashion_male_clothing': 'Moda Masculina',
    'fashion_shoes': 'Calçados',
    'fashion_sport': 'Moda Esportiva',
    'fashion_underwear_beach': 'Moda Praia e Íntima',
    'fixed_telephony': 'Telefonia Fixa',
    'flowers': 'Flores',
    'food': 'Alimentos',
    'food_drink': 'Alimentos e Bebidas',
    'furniture_bedroom': 'Móveis para Quarto',
    'furniture_decor': 'Móveis e Decoração',
    'furniture_living_room': 'Móveis para Sala',
    'furniture_mattress_and_upholstery': 'Colchões e Estofados',
    'garden_tools': 'Ferramentas para Jardim',
    'health_beauty': 'Saúde e Beleza',
    'home_appliances': 'Eletrodomésticos',
    'home_appliances_2': 'Eletrodomésticos 2',
    'home_comfort_2': 'Conforto para Casa 2',
    'home_confort': 'Conforto para Casa',
    'home_construction': 'Construção para Casa',
    'housewares': 'Utilidades Domésticas',
    'industry_commerce_and_business': 'Indústria, Comércio e Negócios',
    'kitchen_dining_laundry_garden_furniture': 'Cozinha, Jantar, Lavanderia e Jardim',
    'la_cuisine': 'Cozinha Gourmet',
    'luggage_accessories': 'Malas e Acessórios',
    'market_place': 'Marketplace',
    'music': 'Música',
    'musical_instruments': 'Instrumentos Musicais',
    'office_furniture': 'Móveis de Escritório',
    'party_supplies': 'Artigos para Festa',
    'perfumery': 'Perfumaria',
    'pet_shop': 'Pet Shop',
    'security_and_services': 'Segurança e Serviços',
    'signaling_and_security': 'Sinalização e Segurança',
    'small_appliances': 'Eletroportáteis',
    'small_appliances_home_oven_and_coffee': 'Eletroportáteis para Forno e Café',
    'sports_leisure': 'Esporte e Lazer',
    'stationery': 'Papelaria',
    'tablets_printing_image': 'Tablets, Impressão e Imagem',
    'telephony': 'Telefonia',
    'toys': 'Brinquedos',
    'watches_gifts': 'Relógios e Presentes',
    'unknown': 'Desconhecida',
}

def category_label_pt(value: str) -> str:
    key = str(value).strip().lower()
    return CATEGORY_PT_MAP.get(key, str(value).replace('_', ' ').title())
