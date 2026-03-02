"""
utils/loaders.py — Central de carregamento de artefatos pre-computados.

REGRA: Nenhuma pagina le arquivos diretamente. Tudo passa por aqui.
- @st.cache_resource: modelos ML (joblib) — objeto global nao copiado entre sessoes
- @st.cache_data: DataFrames, JSON, listas — serializados, copiados por sessao
"""
import json
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

BASE = Path(__file__).parent.parent  # raiz do projeto


@st.cache_resource
def load_pipeline():
    """
    Carrega o pipeline XGBoost serializado da Phase 4.
    CRITICO: @st.cache_resource — modelos ML NAO sao serializaveis com cache_data.
    """
    path = BASE / "models" / "final_pipeline.joblib"
    if not path.exists():
        raise FileNotFoundError(
            f"Pipeline nao encontrado em {path}. "
            "Execute a Phase 4 antes de iniciar o app."
        )
    return joblib.load(path)


@st.cache_data
def load_geo_data() -> pd.DataFrame:
    """
    Carrega dados geograficos pre-computados da Phase 3 (EDA-03).
    OPEN QUESTION: Nomes exatos das colunas dependem do Phase 3.
    Esperado: uf_destino, uf_origem, pct_bad_review, atraso_medio_dias, volume_pedidos, categoria
    Verificar com: df.columns.tolist() antes de usar.
    """
    path = BASE / "data" / "processed" / "geo_aggregated.parquet"
    if not path.exists():
        raise FileNotFoundError(
            f"geo_aggregated.parquet nao encontrado em {path}. "
            "Execute a Phase 3 antes de iniciar o app."
        )
    df = pd.read_parquet(path)
    return df


@st.cache_data
def load_threshold() -> float:
    """
    Carrega o threshold operacional definido na Phase 4 (ML-05).
    Fallback: 0.5 se models/threshold.json nao existir.
    Para gauge tri-color: threshold_low = threshold * 0.6, threshold_high = threshold.
    """
    threshold_path = BASE / "models" / "threshold.json"
    if threshold_path.exists():
        with open(threshold_path) as f:
            data = json.load(f)
            # Aceita tanto {"threshold": 0.4} quanto valor direto
            return data.get("threshold", data) if isinstance(data, dict) else float(data)
    # Fallback: threshold da Phase 4 ML-05 a Precision=0.40 na curva PR
    return 0.785


@st.cache_data
def load_brazil_geojson() -> dict:
    """
    Carrega GeoJSON dos estados brasileiros.
    Usa arquivo local em data/geo/brazil-states.geojson (Plano B offline).
    Fallback: URL do codeforamerica se arquivo local nao existir.
    featureidkey correto: 'properties.sigla' (string como 'SP', 'RJ').
    """
    local_path = BASE / "data" / "geo" / "brazil-states.geojson"
    if local_path.exists():
        with open(local_path, encoding="utf-8") as f:
            return json.load(f)
    # Fallback online (requer internet — nao confiavel em apresentacao ao vivo)
    from urllib.request import urlopen
    url = (
        "https://raw.githubusercontent.com/codeforamerica/click_that_hood"
        "/master/public/data/brazil-states.geojson"
    )
    with urlopen(url) as resp:
        return json.load(resp)


@st.cache_data
def list_eda_figures() -> list:
    """
    Lista arquivos PNG em reports/figures/ ordenados por nome.
    Retorna lista de objetos Path.
    """
    fig_dir = BASE / "reports" / "figures"
    if not fig_dir.exists():
        return []
    return sorted(fig_dir.glob("*.png"))


@st.cache_data
def load_categories_and_ufs() -> tuple:
    """
    Extrai listas unicas de categorias e UFs da tabela gold.
    Usado pelo formulario do Preditor para popular os selectbox.
    Retorna: (lista_categorias_ordenadas, lista_ufs_ordenadas)

    Fonte primaria: data/gold/olist_gold.parquet (colunas product_category_name_english e customer_state)
    Fallback hardcoded: 71 categorias e 27 UFs do dataset Olist caso o parquet nao esteja disponivel.
    """
    _FALLBACK_CATEGORIES = [
        "agro_industry_and_commerce", "air_conditioning", "art", "arts_and_craftmanship",
        "audio", "auto", "baby", "bed_bath_table", "books_general_interest", "books_imported",
        "books_technical", "cds_dvds_musicals", "christmas_supplies", "cine_photo", "computers",
        "computers_accessories", "consoles_games", "construction_tools_construction",
        "construction_tools_lights", "construction_tools_safety", "cool_stuff",
        "costruction_tools_garden", "costruction_tools_tools", "diapers_and_hygiene", "drinks",
        "dvds_blu_ray", "electronics", "fashio_female_clothing", "fashion_bags_accessories",
        "fashion_childrens_clothes", "fashion_male_clothing", "fashion_shoes", "fashion_sport",
        "fashion_underwear_beach", "fixed_telephony", "flowers", "food", "food_drink",
        "furniture_bedroom", "furniture_decor", "furniture_living_room",
        "furniture_mattress_and_upholstery", "garden_tools", "health_beauty", "home_appliances",
        "home_appliances_2", "home_comfort_2", "home_confort", "home_construction", "housewares",
        "industry_commerce_and_business", "kitchen_dining_laundry_garden_furniture", "la_cuisine",
        "luggage_accessories", "market_place", "music", "musical_instruments", "office_furniture",
        "party_supplies", "perfumery", "pet_shop", "security_and_services",
        "signaling_and_security", "small_appliances", "small_appliances_home_oven_and_coffee",
        "sports_leisure", "stationery", "tablets_printing_image", "telephony", "toys",
        "watches_gifts",
    ]
    _FALLBACK_UFS = [
        "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT",
        "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO",
    ]

    gold_path = BASE / "data" / "gold" / "olist_gold.parquet"
    if not gold_path.exists():
        return _FALLBACK_CATEGORIES, _FALLBACK_UFS

    try:
        df = pd.read_parquet(gold_path, columns=["product_category_name_english", "customer_state"])
        categories = sorted(df["product_category_name_english"].dropna().unique().tolist())
        ufs = sorted(
            set(df["customer_state"].dropna().unique().tolist()) | set(_FALLBACK_UFS)
        )
        return categories if categories else _FALLBACK_CATEGORIES, ufs
    except Exception:
        return _FALLBACK_CATEGORIES, _FALLBACK_UFS
