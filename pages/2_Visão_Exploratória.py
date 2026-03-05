import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.loaders import load_gold_data, resolve_revenue_column
from utils.ui import page_header

page_header('Visão Exploratória', icon='🔎')
st.caption('Da descrição da base até a escolha da estratégia do projeto (predição de nota baixa pré-entrega).')


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


def has_cols(df: pd.DataFrame, cols: list[str]) -> bool:
    return all(c in df.columns for c in cols)


def build_base(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    if 'order_purchase_timestamp' in out.columns:
        out['order_purchase_timestamp'] = pd.to_datetime(out['order_purchase_timestamp'], errors='coerce')
        out['month'] = out['order_purchase_timestamp'].dt.to_period('M').dt.to_timestamp()

    if has_cols(out, ['order_delivered_customer_date', 'order_estimated_delivery_date']):
        out['order_delivered_customer_date'] = pd.to_datetime(out['order_delivered_customer_date'], errors='coerce')
        out['order_estimated_delivery_date'] = pd.to_datetime(out['order_estimated_delivery_date'], errors='coerce')
        out['delay_days'] = (
            (out['order_delivered_customer_date'] - out['order_estimated_delivery_date'])
            .dt.total_seconds() / 86400.0
        )
    elif 'actual_delay_days' in out.columns:
        out['delay_days'] = pd.to_numeric(out['actual_delay_days'], errors='coerce')
    else:
        out['delay_days'] = pd.NA

    if 'bad_review' not in out.columns and 'review_score' in out.columns:
        out['bad_review'] = out['review_score'].isin([1, 2]).astype(int)

    return out


# -----------------------------
# Load + global controls
# -----------------------------
df = build_base(load_gold_data())
revenue_col = resolve_revenue_column(df)
cat_col = 'product_category_name_english' if 'product_category_name_english' in df.columns else 'product_category_name'
if cat_col not in df.columns:
    df[cat_col] = 'unknown'

with st.sidebar:
    st.subheader('Filtros')
    min_cat_volume = st.slider('Mínimo de pedidos por categoria', min_value=20, max_value=500, value=100, step=10)
    min_route_volume = st.slider('Mínimo de pedidos por rota', min_value=20, max_value=300, value=50, step=10)

    if 'month' in df.columns and df['month'].notna().any():
        months = sorted(df['month'].dropna().unique())
        if len(months) >= 2:
            start_month, end_month = st.select_slider(
                'Janela temporal',
                options=months,
                value=(months[0], months[-1]),
                format_func=lambda x: pd.Timestamp(x).strftime('%Y-%m')
            )
            df = df[(df['month'] >= start_month) & (df['month'] <= end_month)].copy()

if df.empty:
    st.warning('Sem dados para os filtros selecionados.')
    st.stop()

# -----------------------------
# 1) Linha narrativa
# -----------------------------
st.subheader('Como esta análise se conecta com a decisão do projeto')
st.markdown(
    '1. **Descritiva:** entender tamanho e perfil da operação.\n'
    '2. **Exploratória:** descobrir o que mais se relaciona com nota baixa.\n'
    '3. **Decisão:** justificar o uso do preditor pré-entrega para intervenção.'
)

# -----------------------------
# 2) Analise descritiva
# -----------------------------
st.subheader('A) Análise Descritiva (o que aconteceu)')
orders_total = int(df['order_id'].nunique()) if 'order_id' in df.columns else len(df)
revenue_total = float(df[revenue_col].sum())
ticket_mean = revenue_total / max(orders_total, 1)
clients_col = 'customer_unique_id' if 'customer_unique_id' in df.columns else 'customer_id'
clients_total = int(df[clients_col].nunique()) if clients_col in df.columns else 0
review_mean = float(df['review_score'].mean()) if 'review_score' in df.columns else np.nan

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric('Total de pedidos', f"{orders_total:,}")
c2.metric('Receita total', f"R$ {revenue_total:,.2f}")
c3.metric('Ticket médio', f"R$ {ticket_mean:,.2f}")
c4.metric('Número de clientes', f"{clients_total:,}")
c5.metric('Avaliação média', '-' if pd.isna(review_mean) else f"{review_mean:.2f}")

stats_col1, stats_col2 = st.columns(2)
with stats_col1:
    delay_med = df['delay_days'].dropna().median() if 'delay_days' in df.columns and df['delay_days'].notna().any() else np.nan
    fr_med = df['freight_ratio'].dropna().median() if 'freight_ratio' in df.columns and df['freight_ratio'].notna().any() else np.nan
    st.metric('Mediana de atraso (dias)', '-' if pd.isna(delay_med) else f"{delay_med:.1f}")
    st.metric('Mediana freight_ratio', '-' if pd.isna(fr_med) else f"{fr_med:.3f}")
with stats_col2:
    if 'payment_type' in df.columns and df['payment_type'].notna().any():
        moda_pag = df['payment_type'].mode(dropna=True).iloc[0]
    else:
        moda_pag = '-'
    if 'review_score' in df.columns and df['review_score'].notna().any():
        moda_nota = int(df['review_score'].mode(dropna=True).iloc[0])
    else:
        moda_nota = '-'
    st.metric('Moda do tipo de pagamento', f"{moda_pag}")
    st.metric('Moda da avaliação', f"{moda_nota}")

st.caption('Uso de média, mediana e moda: média resume volume/valor; mediana reduz efeito de outliers; moda mostra o comportamento mais frequente.')

# -----------------------------
# 3) Qualidade de dados
# -----------------------------
st.subheader('B) Qualidade dos Dados (base para análise confiável)')
dq1, dq2 = st.columns(2)
with dq1:
    st.metric('Linhas da base', f"{len(df):,}")
    st.metric('Colunas da base', f"{df.shape[1]:,}")
with dq2:
    dup_orders = int(df['order_id'].duplicated().sum()) if 'order_id' in df.columns else 0
    st.metric('Pedidos duplicados (order_id)', f"{dup_orders:,}")
    st.metric('Colunas com nulos', f"{int((df.isna().mean() > 0).sum())}")
st.caption('Resumo de qualidade: volume da base, duplicidade e presença de nulos para avaliar confiabilidade.')

# -----------------------------
# 4) Analise exploratoria
# -----------------------------
st.subheader('C) Análise Exploratória (por que acontece)')

eda_tab1, eda_tab2, eda_tab3 = st.tabs(['Distribuições', 'Drivers de Nota Baixa', 'Geografia e Segmentos'])

with eda_tab1:
    c1, c2 = st.columns(2)
    with c1:
        if 'review_score' in df.columns:
            dist_review = df['review_score'].value_counts().sort_index().rename_axis('nota').reset_index(name='pedidos')
            fig = px.bar(dist_review, x='nota', y='pedidos', title='Distribuição de avaliações')
            fig.update_layout(height=340, margin={'t': 45, 'l': 10, 'r': 10, 'b': 10})
            st.plotly_chart(fig, use_container_width=True)
    with c2:
        if 'month' in df.columns and df['month'].notna().any():
            monthly = (
                df.dropna(subset=['month'])
                .groupby('month', as_index=False)
                .agg(receita=(revenue_col, 'sum'), pedidos=('order_id', 'nunique'))
                .sort_values('month')
            )
            fig = px.line(monthly, x='month', y='pedidos', markers=True, title='Pedidos por mês')
            fig.update_layout(height=340, margin={'t': 45, 'l': 10, 'r': 10, 'b': 10})
            st.plotly_chart(fig, use_container_width=True)

with eda_tab2:
    if 'bad_review' in df.columns:
        base_bad = float(df['bad_review'].mean())
    else:
        base_bad = np.nan

    r1, r2 = st.columns(2)
    with r1:
        if 'delay_days' in df.columns and df['delay_days'].notna().any() and 'bad_review' in df.columns:
            tmp = df.dropna(subset=['delay_days']).copy()
            tmp['delay_faixa'] = pd.cut(tmp['delay_days'], [-999, 0, 3, 7, 15, 999],
                                        labels=['No prazo/adiantado', '1-3', '4-7', '8-15', '16+'])
            v = tmp.groupby('delay_faixa', as_index=False, observed=False).agg(
                pedidos=('order_id', 'nunique'), bad_rate=('bad_review', 'mean')
            )
            fig = px.line(v, x='delay_faixa', y='bad_rate', markers=True, title='Atraso x taxa de nota 1-2')
            fig.update_layout(height=340, margin={'t': 45, 'l': 10, 'r': 10, 'b': 10})
            st.plotly_chart(fig, use_container_width=True)
    with r2:
        if 'freight_ratio' in df.columns and 'bad_review' in df.columns and df['freight_ratio'].notna().any():
            fr = df[['order_id', 'freight_ratio', 'bad_review']].dropna().copy()
            fr['decil'] = pd.qcut(fr['freight_ratio'], 10, duplicates='drop')
            frv = fr.groupby('decil', as_index=False, observed=False).agg(bad_rate=('bad_review', 'mean'))
            frv['decil'] = frv['decil'].astype(str)
            fig = px.line(frv, x='decil', y='bad_rate', markers=True, title='Frete relativo x taxa de nota 1-2')
            fig.update_layout(height=340, margin={'t': 45, 'l': 10, 'r': 10, 'b': 10})
            st.plotly_chart(fig, use_container_width=True)

    if 'estimated_delivery_days' in df.columns and 'review_score' in df.columns:
        corr_df = df[['estimated_delivery_days', 'review_score']].dropna().copy()
        if not corr_df.empty:
            corr_df['prazo_faixa'] = pd.qcut(corr_df['estimated_delivery_days'], 10, duplicates='drop')
            corr_view = (
                corr_df.groupby('prazo_faixa', as_index=False, observed=False)
                .agg(nota_media=('review_score', 'mean'), pedidos=('review_score', 'size'))
            )
            corr_view['prazo_faixa'] = corr_view['prazo_faixa'].astype(str)

            fig_corr = px.line(
                corr_view,
                x='prazo_faixa',
                y='nota_media',
                markers=True,
                title='Correlação: prazo estimado de entrega x nota média'
            )
            fig_corr.update_layout(height=340, margin={'t': 45, 'l': 10, 'r': 10, 'b': 10})
            fig_corr.update_xaxes(title='Faixa de prazo estimado (dias)')
            fig_corr.update_yaxes(title='Nota média')
            st.plotly_chart(fig_corr, use_container_width=True)
            st.caption('Leitura: prazos estimados mais longos tendem a se associar a notas médias menores.')

    if not pd.isna(base_bad):
        st.info(f'Taxa base de nota 1-2 no recorte: {base_bad:.2%}')

with eda_tab3:
    g1, g2 = st.columns(2)
    with g1:
        if has_cols(df, ['seller_state', 'customer_state', 'bad_review']):
            route = (
                df.groupby(['seller_state', 'customer_state'], as_index=False)
                .agg(pedidos=('order_id', 'nunique'), bad_rate=('bad_review', 'mean'))
            )
            route = route[route['pedidos'] >= min_route_volume]
            if not route.empty:
                route['rota'] = route['seller_state'].astype(str) + ' -> ' + route['customer_state'].astype(str)
                fig = px.bar(route.nlargest(12, 'bad_rate').sort_values('bad_rate'), x='bad_rate', y='rota', orientation='h',
                             title='Principais rotas críticas por taxa de nota 1-2')
                fig.update_layout(height=380, margin={'t': 45, 'l': 10, 'r': 10, 'b': 10})
                st.plotly_chart(fig, use_container_width=True)
    with g2:
        if cat_col in df.columns and 'bad_review' in df.columns:
            cat = (
                df.groupby(cat_col, as_index=False)
                .agg(pedidos=('order_id', 'nunique'), bad_rate=('bad_review', 'mean'))
            )
            cat = cat[cat['pedidos'] >= min_cat_volume]
            if not cat.empty:
                cat['categoria_pt'] = cat[cat_col].apply(category_label_pt)
                fig = px.bar(cat.nlargest(12, 'bad_rate').sort_values('bad_rate'), x='bad_rate', y='categoria_pt', orientation='h',
                             title='Principais categorias com maior taxa de nota 1-2')
                fig.update_layout(height=380, margin={'t': 45, 'l': 10, 'r': 10, 'b': 10})
                st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 5) Fechamento: por que escolhemos este projeto
# -----------------------------
st.subheader('D) Síntese: como isso leva à escolha do projeto')

insights = []
if 'bad_review' in df.columns:
    insights.append(f"A taxa de nota 1-2 no recorte é {df['bad_review'].mean():.2%}.")

if has_cols(df, ['delay_days', 'bad_review']) and df['delay_days'].notna().any():
    late = df[df['delay_days'].notna()].copy()
    late['is_late'] = late['delay_days'] > 0
    if late['is_late'].any() and (~late['is_late']).any():
        r_late = late.loc[late['is_late'], 'bad_review'].mean()
        r_on = late.loc[~late['is_late'], 'bad_review'].mean()
        insights.append(f'Pedidos atrasados têm taxa de nota 1-2 maior ({r_late:.2%}) do que pedidos no prazo ({r_on:.2%}).')

if has_cols(df, ['freight_ratio', 'bad_review']) and df['freight_ratio'].notna().any():
    q90 = df['freight_ratio'].quantile(0.9)
    hi = df[df['freight_ratio'] >= q90]['bad_review'].mean()
    base = df['bad_review'].mean()
    insights.append(f'O topo de freight_ratio concentra risco maior ({hi:.2%}) vs média da base ({base:.2%}).')

for item in insights[:3]:
    st.markdown(f'- {item}')

st.subheader('Insights-chave para apresentação')
card1, card2, card3 = st.columns(3)
if has_cols(df, ['delay_days', 'bad_review']) and df['delay_days'].notna().any():
    tmp = df[df['delay_days'].notna()].copy()
    tmp['is_late'] = tmp['delay_days'] > 0
    late_rate = tmp.loc[tmp['is_late'], 'bad_review'].mean() if tmp['is_late'].any() else np.nan
    ontime_rate = tmp.loc[~tmp['is_late'], 'bad_review'].mean() if (~tmp['is_late']).any() else np.nan
else:
    late_rate, ontime_rate = np.nan, np.nan

if has_cols(df, ['freight_ratio', 'bad_review']) and df['freight_ratio'].notna().any():
    q90 = df['freight_ratio'].quantile(0.9)
    fr_top = df[df['freight_ratio'] >= q90]['bad_review'].mean()
else:
    fr_top = np.nan

if has_cols(df, ['seller_state', 'customer_state', 'bad_review']):
    route_card = (
        df.groupby(['seller_state', 'customer_state'], as_index=False)
        .agg(pedidos=('order_id', 'nunique'), bad_rate=('bad_review', 'mean'))
    )
    route_card = route_card[route_card['pedidos'] >= min_route_volume]
    if not route_card.empty:
        top_route_row = route_card.sort_values('bad_rate', ascending=False).iloc[0]
        top_route_label = f"{top_route_row['seller_state']} -> {top_route_row['customer_state']}"
        top_route_rate = top_route_row['bad_rate']
    else:
        top_route_label, top_route_rate = '-', np.nan
else:
    top_route_label, top_route_rate = '-', np.nan

with card1:
    st.metric('Risco em atraso vs prazo', '-' if pd.isna(late_rate) else f'{late_rate:.1%}',
              delta='vs. no prazo: -' if pd.isna(ontime_rate) else f"no prazo {ontime_rate:.1%}")
with card2:
    st.metric('Faixa de 10% maior freight_ratio', '-' if pd.isna(fr_top) else f'{fr_top:.1%}',
              delta='taxa de nota 1-2')
with card3:
    st.metric('Rota mais crítica', top_route_label,
              delta='-' if pd.isna(top_route_rate) else f"{top_route_rate:.1%} nota 1-2")

st.success(
    'Conclusão: os padrões exploratórios sustentam a escolha do projeto atual: '
    'prever risco de nota baixa antes da entrega para permitir intervenção preventiva.'
)

#st.caption('Próximo passo no fluxo: página 3 (EDA com figuras exportadas), 4 (mapa) e 5 (preditor de ação).')
