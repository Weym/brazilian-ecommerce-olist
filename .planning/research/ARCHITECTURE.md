# Architecture Research

**Domain:** Data Science Team Project — Relational Dataset Pipeline (Olist E-Commerce)
**Researched:** 2026-03-01
**Confidence:** HIGH (patterns verified via Cookiecutter Data Science official docs, Medallion architecture sources, sklearn official docs)

---

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DEMO LAYER                                   │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              Streamlit App  (app/)                           │   │
│  │   pages/overview.py  |  pages/mapa.py  |  pages/modelo.py   │   │
│  └──────────────────────────────────┬───────────────────────────┘   │
└─────────────────────────────────────┼───────────────────────────────┘
                                      │ loads parquet / joblib
┌─────────────────────────────────────┼───────────────────────────────┐
│                        ANALYSIS + ML LAYER                          │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────────────┐   │
│  │  notebooks/   │  │  notebooks/   │  │    notebooks/         │   │
│  │  02-eda/      │  │  03-geo/      │  │    04-ml/             │   │
│  │  (Pessoa 3)   │  │  (Pessoa 2)   │  │    (Pessoa 4)         │   │
│  └───────┬───────┘  └───────┬───────┘  └──────────┬────────────┘   │
└──────────┼──────────────────┼─────────────────────┼────────────────┘
           │ reads            │ reads               │ reads
┌──────────┼──────────────────┼─────────────────────┼────────────────┐
│          │         DATA FOUNDATION LAYER           │                │
│  ┌───────▼─────────────────────────────────────────▼────────────┐  │
│  │              data/gold/olist_gold.parquet                    │  │
│  │              (Pessoa 1 — único dono)                         │  │
│  └──────────────────────────┬───────────────────────────────────┘  │
│  ┌───────────────────────────▼───────────────────────────────────┐  │
│  │              notebooks/01-data-foundation/                    │  │
│  │              build_gold.ipynb  (Pessoa 1)                     │  │
│  └──────────────────────────┬───────────────────────────────────┘  │
└──────────────────────────────┼──────────────────────────────────────┘
                               │ reads
┌──────────────────────────────┼──────────────────────────────────────┐
│                       RAW DATA LAYER                                │
│  data/raw/                   │                                      │
│  ├── olist_orders_dataset.csv                                       │
│  ├── olist_order_items_dataset.csv                                  │
│  ├── olist_order_reviews_dataset.csv                                │
│  ├── olist_order_payments_dataset.csv                               │
│  ├── olist_customers_dataset.csv                                    │
│  ├── olist_sellers_dataset.csv                                      │
│  ├── olist_products_dataset.csv                                     │
│  ├── olist_geolocation_dataset.csv                                  │
│  └── product_category_name_translation.csv                          │
│  (IMUTÁVEL — nunca editar)                                          │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Componente | Responsabilidade | Dono | Comunica com |
|------------|-----------------|------|--------------|
| `data/raw/` | CSVs originais Kaggle, imutáveis | Pessoa 1 (setup único) | Ninguém escreve aqui após ingestão |
| `notebooks/01-data-foundation/build_gold.ipynb` | Joins entre 9 dataframes, limpeza, validação, escrita do parquet gold | Pessoa 1 | Lê `data/raw/`, escreve `data/gold/` |
| `data/gold/olist_gold.parquet` | Tabela analítica única — base de todos os outros trabalhos | Pessoa 1 (produz), todos leem | EDA, Geo, ML, Demo |
| `notebooks/02-eda/` | Gráficos de atraso × nota, frete × total, segmentações | Pessoa 3 | Lê `data/gold/` |
| `notebooks/03-geo/` | Cálculo de distância, agregações por UF/cidade, mapas | Pessoa 2 | Lê `data/gold/`, escreve `data/processed/geo_aggregated.parquet` |
| `notebooks/04-ml/` | Feature engineering pré-entrega, baseline, modelo final, métricas | Pessoa 4 | Lê `data/gold/`, escreve `models/` |
| `models/` | Artefatos serializados (joblib): pipeline de features + modelo | Pessoa 4 | Streamlit app |
| `app/` | Demo Streamlit — visualizações, inputs, predição ao vivo | Pessoa 6 (monta) + Pessoas 2/3/4 (fornecem assets) | Lê `data/gold/`, `data/processed/`, `models/` |
| `reports/` | Deck de apresentação, relatório escrito, figuras exportadas | Pessoa 6 | Consome outputs de EDA e ML |

---

## Recommended Project Structure

```
olist-challenge/
├── data/
│   ├── raw/                        # CSVs originais Kaggle — NUNCA editar
│   │   ├── olist_orders_dataset.csv
│   │   ├── olist_order_items_dataset.csv
│   │   ├── olist_order_reviews_dataset.csv
│   │   ├── olist_order_payments_dataset.csv
│   │   ├── olist_customers_dataset.csv
│   │   ├── olist_sellers_dataset.csv
│   │   ├── olist_products_dataset.csv
│   │   ├── olist_geolocation_dataset.csv
│   │   └── product_category_name_translation.csv
│   ├── gold/                       # Tabela analítica pronta para consumo
│   │   └── olist_gold.parquet      # Produzida por notebooks/01-data-foundation/
│   └── processed/                  # Artefatos intermediários de análise
│       └── geo_aggregated.parquet  # Agregações geográficas (Pessoa 2)
│
├── notebooks/
│   ├── 01-data-foundation/         # FASE 1 — Dono: Pessoa 1
│   │   └── 01-p1-build-gold.ipynb
│   ├── 02-eda/                     # FASE 2a — Dono: Pessoa 3
│   │   ├── 02-p3-delay-vs-score.ipynb
│   │   └── 02-p3-freight-segmentation.ipynb
│   ├── 03-geo/                     # FASE 2b — Dono: Pessoa 2
│   │   ├── 03-p2-distance-calc.ipynb
│   │   └── 03-p2-regional-maps.ipynb
│   ├── 04-ml/                      # FASE 3 — Dono: Pessoa 4
│   │   ├── 04-p4-feature-engineering.ipynb
│   │   ├── 04-p4-baseline.ipynb
│   │   └── 04-p4-model-tuning.ipynb
│   └── 05-nlp/                     # Opcional — Dono: Pessoa 5
│       └── 05-p5-review-topics.ipynb
│
├── src/                            # Código reutilizável (refatorado de notebooks)
│   ├── __init__.py
│   ├── data_loader.py              # Funções de leitura/join dos CSVs raw
│   ├── features.py                 # Features pré-entrega (compartilhadas entre ML e demo)
│   ├── metrics.py                  # Cálculo de delay, distância (compartilhado)
│   └── viz.py                      # Funções de plotagem reutilizadas no Streamlit
│
├── models/
│   ├── baseline_logreg.joblib      # Modelo baseline serializado
│   └── final_pipeline.joblib       # Pipeline sklearn completo (features + modelo)
│
├── app/                            # Demo Streamlit
│   ├── app.py                      # Entry point: st.set_page_config + navegação
│   └── pages/
│       ├── 01_overview.py          # Narrativa Ato 1 — Impacto da logística
│       ├── 02_mapa.py              # Heatmap regional de insatisfação
│       └── 03_modelo.py            # Predição ao vivo — inputs → risco
│
├── reports/
│   ├── figures/                    # Gráficos exportados pelos notebooks
│   └── deck/                       # Slides (PPTX/PDF)
│
├── .gitignore                      # Ignorar data/raw/ se arquivos grandes
├── README.md
└── requirements.txt
```

### Structure Rationale

- **`data/raw/` imutável:** Princípio fundamental do Cookiecutter Data Science — nunca editar dados originais. Permite reprocessar a gold table do zero a qualquer momento sem perda.
- **`data/gold/` como contrato de interface:** Todos os notebooks de análise consomem apenas este arquivo. Quando a Pessoa 1 atualiza a gold table, todos automaticamente se beneficiam sem merge conflicts.
- **`notebooks/` numerados com prefixo de fase e inicial:** Convenção CCDS (`FASE-PESSOA-descricao.ipynb`) torna óbvio quem é dono e em que ordem rodar. Elimina conflitos de merge porque cada pessoa trabalha em notebooks distintos.
- **`src/` para código compartilhado:** Funções usadas em múltiplos lugares (feature engineering para ML e para demo, funções de plotagem para notebooks e Streamlit) vivem em Python puro — não em notebooks. Facilita import, teste e versionamento.
- **`models/` separado:** O Streamlit carrega apenas o artefato serializado — não precisa rodar nenhum notebook. Isso desacopla o demo da fase de treinamento.
- **`app/pages/` por página:** Multi-page Streamlit nativo (v1.28+) — cada arquivo em `pages/` vira uma página automaticamente. Pessoas 2, 3, 4 podem contribuir com sua página sem tocar no `app.py` principal.

---

## Architectural Patterns

### Pattern 1: Gold Table como Contrato de Interface

**What:** Uma única tabela analítica (`olist_gold.parquet`) produzida pela Fase 1 que serve como fonte única de verdade para todas as análises subsequentes. Todos os joins entre os 9 dataframes relacionais acontecem uma vez, neste lugar.

**When to use:** Sempre que múltiplos analistas precisam de um subconjunto consistente e limpo dos mesmos dados relacionais. Evita que cada pessoa refaça joins com lógica ligeiramente diferente.

**Trade-offs:** Requer que a Fase 1 esteja pronta antes que as outras possam começar (bloqueio de ~meia hora no Dia 1). Mas esse custo é insignificante comparado ao caos de joins inconsistentes entre membros do time.

**Example:**
```python
# notebooks/01-data-foundation/01-p1-build-gold.ipynb

import pandas as pd

orders = pd.read_csv("data/raw/olist_orders_dataset.csv", parse_dates=["order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"])
items  = pd.read_csv("data/raw/olist_order_items_dataset.csv")
reviews = pd.read_csv("data/raw/olist_order_reviews_dataset.csv")
payments = pd.read_csv("data/raw/olist_order_payments_dataset.csv")
customers = pd.read_csv("data/raw/olist_customers_dataset.csv")
sellers = pd.read_csv("data/raw/olist_sellers_dataset.csv")

# join único, lógica centralizada
gold = (
    orders
    .merge(items.groupby("order_id").agg(
        freight_value=("freight_value", "sum"),
        price_total=("price", "sum"),
        seller_id=("seller_id", "first")
    ).reset_index(), on="order_id", how="left")
    .merge(reviews[["order_id", "review_score"]].drop_duplicates("order_id"), on="order_id", how="left")
    .merge(customers[["customer_id", "customer_state", "customer_city"]], on="customer_id", how="left")
    .merge(sellers[["seller_id", "seller_state"]], on="seller_id", how="left")
)

gold.to_parquet("data/gold/olist_gold.parquet", index=False)
```

### Pattern 2: Feature Engineering dentro de Pipeline sklearn (sem vazamento)

**What:** Todas as transformações de features ficam encapsuladas em um `sklearn.Pipeline` que inclui o modelo. O pipeline é fitado apenas no train set e serializado com joblib. O Streamlit carrega o pipeline e chama `.predict_proba()` diretamente — sem nenhum preprocessing manual fora do pipeline.

**When to use:** Sempre que o modelo precisar ser servido em produção (mesmo que seja apenas uma demo ao vivo). Garante que a exata mesma transformação usada no treino seja aplicada em inferência.

**Trade-offs:** Requer disciplina no design das features — todas devem ser computáveis a partir dos inputs disponíveis no momento de expedição. Não suporta features que exigem estado global atualizado (ex: médias históricas do vendedor calculadas on-the-fly).

**Example:**
```python
# src/features.py — funções de feature engineering pré-entrega

import pandas as pd
import numpy as np

PRE_DELIVERY_FEATURES = [
    "freight_value",
    "price_total",
    "days_to_estimated_delivery",   # estimated_delivery - purchase_timestamp
    "purchase_hour",
    "purchase_dayofweek",
    "seller_state",
    "customer_state",
    "same_state_flag",              # customer_state == seller_state
]

def build_pre_delivery_features(gold_df: pd.DataFrame) -> pd.DataFrame:
    """Retorna apenas features disponíveis até o momento de expedição.
    GUARDRAIL: não incluir nenhuma coluna dependente de order_delivered_customer_date.
    """
    df = gold_df.copy()
    df["days_to_estimated_delivery"] = (
        df["order_estimated_delivery_date"] - df["order_purchase_timestamp"]
    ).dt.days
    df["purchase_hour"] = df["order_purchase_timestamp"].dt.hour
    df["purchase_dayofweek"] = df["order_purchase_timestamp"].dt.dayofweek
    df["same_state_flag"] = (df["customer_state"] == df["seller_state"]).astype(int)
    return df[PRE_DELIVERY_FEATURES]
```

```python
# notebooks/04-ml/04-p4-baseline.ipynb

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
import joblib
from src.features import build_pre_delivery_features

gold = pd.read_parquet("data/gold/olist_gold.parquet")
X = build_pre_delivery_features(gold)
y = (gold["review_score"] <= 2).astype(int)  # target: avaliação ruim

# split ANTES de qualquer fit
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

num_cols = ["freight_value", "price_total", "days_to_estimated_delivery", "purchase_hour", "purchase_dayofweek", "same_state_flag"]
cat_cols = ["seller_state", "customer_state"]

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
])

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("clf", LogisticRegression(class_weight="balanced", max_iter=500))
])

pipeline.fit(X_train, y_train)
joblib.dump(pipeline, "models/baseline_logreg.joblib")
```

### Pattern 3: Streamlit Multi-Page com Assets Pré-Computados

**What:** A demo não roda nenhuma lógica pesada no momento da apresentação. Ela carrega parquets pré-computados e o modelo serializado. Cada página (`pages/`) é independente e desenvolvida pela pessoa dona daquele ato narrativo.

**When to use:** Quando o dataset tem > 100k linhas (Olist tem ~100k pedidos) e a demo precisa responder em < 1 segundo. Pré-computar agregações elimina o risco de timeout durante apresentação ao vivo.

**Trade-offs:** Requer que todos os artefatos (`data/gold/`, `data/processed/geo_aggregated.parquet`, `models/final_pipeline.joblib`) estejam prontos antes de integrar a demo. A integração acontece na Fase 4.

**Example:**
```python
# app/pages/03_modelo.py

import streamlit as st
import pandas as pd
import joblib
from src.features import build_pre_delivery_features

@st.cache_resource
def load_model():
    return joblib.load("models/final_pipeline.joblib")

pipeline = load_model()

st.title("Modelo de Risco Pré-Entrega")

freight = st.number_input("Valor do frete (R$)", min_value=0.0, value=15.0)
price_total = st.number_input("Valor total do pedido (R$)", min_value=0.0, value=80.0)
days_est = st.slider("Dias até entrega estimada", 1, 60, 14)
seller_state = st.selectbox("Estado do vendedor", ["SP", "MG", "RJ", "RS", "PR"])
customer_state = st.selectbox("Estado do cliente", ["SP", "MG", "RJ", "RS", "PR", "AM", "PA"])

if st.button("Calcular risco"):
    input_df = pd.DataFrame([{
        "freight_value": freight,
        "price_total": price_total,
        "days_to_estimated_delivery": days_est,
        "purchase_hour": 14,
        "purchase_dayofweek": 2,
        "seller_state": seller_state,
        "customer_state": customer_state,
        "same_state_flag": int(seller_state == customer_state),
    }])
    prob = pipeline.predict_proba(input_df)[0, 1]
    st.metric("Probabilidade de avaliação 1-2 estrelas", f"{prob:.1%}")
    if prob > 0.3:
        st.error("Alto risco — considerar intervenção proativa")
    else:
        st.success("Risco baixo")
```

---

## Data Flow

### Fluxo Principal (Raw → Gold → Análise → Demo)

```
data/raw/ (9 CSVs imutáveis)
    │
    ▼  [notebooks/01-data-foundation/build_gold.ipynb]
    │  joins, limpeza, derivação de delay, exclusão de linhas pós-entrega
    │
data/gold/olist_gold.parquet
    │
    ├──▶ [notebooks/02-eda/]
    │    gráficos, exporta figuras para reports/figures/
    │
    ├──▶ [notebooks/03-geo/]
    │    distâncias, mapas, agrega por UF
    │    └──▶ data/processed/geo_aggregated.parquet
    │
    └──▶ [notebooks/04-ml/]
         feature engineering pré-entrega (sem vazamento)
         treino → validação → serialização
         └──▶ models/final_pipeline.joblib
                  │
                  ▼
             app/pages/03_modelo.py
             (carrega pipeline, serve predições ao vivo)

data/gold/olist_gold.parquet ──▶ app/pages/01_overview.py (métricas gerais)
data/processed/geo_aggregated.parquet ──▶ app/pages/02_mapa.py (heatmap)
reports/figures/ ──▶ reports/deck/ (slides da apresentação)
```

### Fluxo de Dados do Modelo (Guardrail de Vazamento)

```
order_purchase_timestamp
order_estimated_delivery_date
freight_value
price_total
seller_state
customer_state
        │
        │ [src/features.py:build_pre_delivery_features()]
        │ (NUNCA usa order_delivered_customer_date)
        ▼
X_features (matriz de features pré-expedição)
        │
        │ [train_test_split — SPLIT ANTES DO FIT]
        ▼
X_train ──▶ pipeline.fit() ──▶ models/final_pipeline.joblib
X_test  ──▶ pipeline.predict_proba() ──▶ métricas (recall, PR-AUC)
```

### Key Data Flows

1. **Gold table como hub central:** Cada novo membro do time começa lendo `data/gold/olist_gold.parquet` — um único arquivo, uma única versão, sem ambiguidade sobre qual lógica de join usar.
2. **Artefatos pré-computados para demo:** A Streamlit app nunca roda pandas/sklearn durante a apresentação. Ela carrega parquet e joblib previamente prontos — resposta < 1s garantida.
3. **Funções em `src/` compartilhadas entre notebooks e app:** `src/features.py` é importado tanto no notebook de treino quanto no Streamlit — garantindo que a mesma transformação aconteça nos dois contextos (sem discrepância treino/inferência).

---

## Build Order (Ordem de Construção)

Esta é a ordem crítica de dependências. Bloqueios estão marcados.

```
DIA 1 (manhã) — BLOQUEANTE PARA TODOS
├── [Pessoa 1] Setup do repositório + ingestão dos CSVs raw
└── [Pessoa 1] build_gold.ipynb → data/gold/olist_gold.parquet
     ↓ DESBLOQUEIO: assim que gold.parquet estiver disponível, Pessoas 2, 3, 4 começam

DIA 1 (tarde) → DIA 3 — PARALELO
├── [Pessoa 2] notebooks/03-geo/ → data/processed/geo_aggregated.parquet
├── [Pessoa 3] notebooks/02-eda/ → reports/figures/*.png
├── [Pessoa 4] notebooks/04-ml/ → models/final_pipeline.joblib
└── [Pessoa 6] Estrutura do deck, placeholders visuais (não precisa de dados)

DIA 3 → DIA 4 — INTEGRAÇÃO
├── [Pessoa 4] finaliza modelo, valida métricas, serializa pipeline
├── [Pessoa 2+3] exportam figuras finais e agregações para reports/
└── [Pessoas 5] contribui NLP se estiver pronta (opcional, não bloqueia)

DIA 4 → DIA 5 — DEMO + STORY
├── [Pessoa 6] monta app/pages/ com assets das Pessoas 2, 3, 4
├── [Pessoa 6] finaliza slides com achados reais
└── [Todos] revisão de narrativa, ensaio da apresentação
```

**Dependências críticas:**
- `data/gold/olist_gold.parquet` deve existir antes de qualquer notebook de análise ou ML começar.
- `models/final_pipeline.joblib` deve existir antes que `app/pages/03_modelo.py` seja construída.
- `data/processed/geo_aggregated.parquet` deve existir antes que `app/pages/02_mapa.py` seja construída.

---

## Anti-Patterns

### Anti-Pattern 1: Joins Duplicados em Múltiplos Notebooks

**What people do:** Cada analista faz seu próprio `pd.merge()` no início do notebook, às vezes com lógica de limpeza ligeiramente diferente (diferentes critérios de filtro de datas, tratamento de NaN distinto).

**Why it's wrong:** Resulta em números inconsistentes entre atos da apresentação. A Pessoa 3 mostra "X% de pedidos atrasados" com base em um join; a Pessoa 4 usa outra versão. A audiência percebe.

**Do this instead:** Gold table única produzida pela Pessoa 1. Todos os notebooks fazem `pd.read_parquet("data/gold/olist_gold.parquet")` — nenhum join fora do notebook de foundation.

### Anti-Pattern 2: Features Pós-Entrega no Modelo

**What people do:** Incluem `order_delivered_customer_date` como feature (para calcular delay real), ou usam `review_score` de pedidos anteriores do mesmo cliente como predictor.

**Why it's wrong:** O modelo parece excelente no treino mas é inútil em produção — essas informações não existem no momento em que a intervenção precisa acontecer (antes da entrega). A credibilidade da demo desaparece se a audiência técnica detectar o vazamento.

**Do this instead:** Definir e documentar explicitamente no início do projeto quais colunas são "disponíveis até o momento de expedição". Usar `src/features.py:PRE_DELIVERY_FEATURES` como lista de allow-list. Nunca passar `gold_df` diretamente para o modelo — sempre passar pelo filtro de features.

### Anti-Pattern 3: Notebooks Pesados na Demo ao Vivo

**What people do:** A demo Streamlit importa e roda o notebook de análise (ou código equivalente) toda vez que o usuário interage, fazendo joins em 100k linhas na hora.

**Why it's wrong:** Timeout durante apresentação ao vivo. Streamlit reroda o script a cada interação — qualquer operação > 2s torna a demo instável.

**Do this instead:** Todos os outputs pesados pré-computados como parquet ou joblib. O Streamlit apenas carrega e exibe. Usar `@st.cache_resource` para o modelo e `@st.cache_data` para dataframes grandes.

### Anti-Pattern 4: Todos os Notebooks em um Único Diretório

**What people do:** Colocam todos os notebooks na raiz de `notebooks/` com nomes genéricos como `analysis.ipynb`, `model.ipynb`, `final_model_v3.ipynb`.

**Why it's wrong:** Merge conflicts quando duas pessoas salvam arquivos no mesmo diretório. Impossível saber a ordem de execução. Impossiíbel saber quem é dono.

**Do this instead:** Subdiretórios numerados por fase + prefixo de inicial do dono (`01-p1-build-gold.ipynb`). Cada pessoa trabalha em seu subdiretório — zero conflitos de merge em notebooks.

---

## Team Collaboration Considerations

### Estratégia de Branches para Reduzir Conflitos de Merge

```
main (branch estável)
├── feature/01-gold-table       (Pessoa 1) — merge quando gold.parquet estiver pronta
├── feature/02-eda              (Pessoa 3) — merge ao final da Fase 2
├── feature/03-geo              (Pessoa 2) — merge ao final da Fase 2
├── feature/04-ml               (Pessoa 4) — merge quando pipeline estiver serializado
├── feature/05-nlp              (Pessoa 5) — merge opcional, não bloqueia
└── feature/06-demo             (Pessoa 6) — merge no Dia 4/5
```

**Regras para conflito zero:**
- `data/raw/` e `data/gold/`: apenas Pessoa 1 escreve. Todos os outros: read-only.
- `src/features.py`: Pessoa 4 é dona. Outros podem propor via PR, mas não commitam diretamente.
- `app/pages/`: cada página tem dono único. `app.py` (entry point) é responsabilidade da Pessoa 6.
- Notebooks: cada notebook pertence a exatamente uma pessoa. Nunca dois commitam no mesmo arquivo.

### Artefatos Grandes e .gitignore

```gitignore
# .gitignore
data/raw/           # baixar do Kaggle localmente (ou usar script de download)
data/gold/          # regenerado pelo notebook 01
data/processed/     # regenerado pelos notebooks 02/03
models/*.joblib     # regenerado pelo notebook 04

# manter no git:
# src/, app/, notebooks/ (código), reports/deck/, requirements.txt
```

Isso evita que arquivos binários grandes (CSVs, parquets, modelos) entrem no repositório e causem conflitos de merge irresolvíveis.

---

## Integration Points

### Internal Boundaries

| Fronteira | Comunicação | Notas |
|-----------|-------------|-------|
| `notebooks/01` → Resto do time | `data/gold/olist_gold.parquet` (arquivo) | Interface estável — mudanças na gold table exigem aviso ao time |
| `src/features.py` → `notebooks/04-ml/` | Import Python direto | Pessoa 4 é dona; mudanças na feature list afetam demo e treino |
| `src/features.py` → `app/pages/03_modelo.py` | Import Python direto | Mesma função em treino e inferência — crítico para consistência |
| `models/` → `app/` | Joblib (arquivo binário) | Pessoa 4 serializa, Pessoa 6 carrega. Formato contratado: sklearn Pipeline |
| `data/processed/geo_aggregated.parquet` → `app/pages/02_mapa.py` | Arquivo parquet | Pessoa 2 produz, Pessoa 6 consome |
| `reports/figures/` → `reports/deck/` | Arquivos PNG/SVG | Pessoas 2/3 exportam figuras; Pessoa 6 insere nos slides |

### External Services

| Serviço | Padrão de Integração | Notas |
|---------|---------------------|-------|
| Kaggle Dataset | Download manual ou `kaggle datasets download` | Baixar uma vez, colocar em `data/raw/`, commitar path no README |
| Streamlit Community Cloud | Push para GitHub + connect repo | Deploy de 1 clique; requer `requirements.txt` e `app/app.py` na raiz ou path configurado |

---

## Scaling Considerations

| Escala | Ajustes Arquiteturais |
|--------|----------------------|
| 1 analista, exploração inicial | Notebooks diretos nos CSVs, sem estrutura formal |
| 6 pessoas, 1 semana (este projeto) | Gold table + subdiretórios por dono + src/ para código compartilhado + artefatos pré-computados |
| Time de 20+ pessoas, multi-sprint | Substituir gold parquet por DuckDB ou Delta Lake; CI/CD para reproductibilidade; data catalog |
| Produção real | Substituir Streamlit por API FastAPI + frontend separado; treino agendado via Airflow/Prefect |

### Scaling Priorities (para este projeto)

1. **Primeiro gargalo:** A Fase 1 (gold table) bloqueia todo o time por ~30–60 minutos no Dia 1. Mitigar colocando a Pessoa 1 nisso desde o primeiro momento.
2. **Segundo gargalo:** Integração do Streamlit no Dia 4 depende de todos os artefatos prontos. Mitigar tendo a Pessoa 6 construir a estrutura do app com dados fake primeiro, substituindo por reais quando chegarem.

---

## Sources

- Cookiecutter Data Science v2 official documentation — https://cookiecutter-data-science.drivendata.org/ (MEDIUM confidence — fetched 2026-03-01)
- Medallion Architecture (Bronze/Silver/Gold) — Databricks documentation and community articles (MEDIUM confidence — WebSearch verified, padrão estabelecido pela indústria)
- scikit-learn Pipeline documentation — data leakage prevention via Pipeline encapsulation (HIGH confidence — padrão documentado oficialmente)
- Streamlit multi-page apps documentation — https://docs.streamlit.io/library/get-started/multipage-apps (MEDIUM confidence — WebSearch verified)
- Git workflows for data science teams — feature branches por analista para evitar merge conflicts em notebooks (MEDIUM confidence — múltiplas fontes concordam)

---

*Architecture research for: Olist Challenge — Data Science Pipeline (Raw → Gold → EDA/ML → Streamlit Demo)*
*Researched: 2026-03-01*
