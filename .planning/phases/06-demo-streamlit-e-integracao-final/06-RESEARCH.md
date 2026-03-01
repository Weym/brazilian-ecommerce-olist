# Phase 6: Demo Streamlit e Integracao Final - Research

**Researched:** 2026-03-01
**Domain:** Streamlit multipage app, Plotly gauge/choropleth, XGBoost pipeline inference, Streamlit Cloud deployment
**Confidence:** HIGH (core Streamlit/Plotly APIs) / MEDIUM (Streamlit Cloud limits, XGBoost feature handling)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- `pages/` directory nativo do Streamlit — cada página é um arquivo `.py` separado
- Sidebar automática com links para cada página
- URLs únicas por página (sem rebuild ao trocar de seção)
- Preditor: 5 inputs (frete, valor pedido, prazo em dias, categoria, UF origem/destino) → gauge Plotly (go.Indicator mode="gauge+number") verde/amarelo/vermelho
- Mapa: Plotly choropleth colorizada por % bad reviews por UF destino; filtros UF origem/destino/categoria/faixa de risco; hover com 3 métricas; fonte: `data/processed/geo_aggregated.parquet`
- EDA: imagens estáticas PNG de `reports/figures/`; navegação via st.selectbox
- `@st.cache_data` em todas as leituras de artefatos; NO joins, NO model training ao vivo
- Deploy primário: Streamlit Cloud (URL pública); Plano B: local
- Gauge thresholds: derivados do threshold operacional ML-05 da Phase 4

### Claude's Discretion
- Limiares exatos do gauge (Verde/Amarelo/Vermelho) — derivados do threshold operacional da ML-05
- Layout interno de cada página (proporção de colunas, espaçamento)
- Tratamento de encoding para categorias no pipeline (`LabelEncoder` ou `OrdinalEncoder`)
- Página Home/landing opcional com resumo do projeto

### Deferred Ideas (OUT OF SCOPE)
- Nenhuma — discussão ficou dentro do escopo da Phase 6
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| PRES-03 | Streamlit multi-página com preditor ao vivo (input de características → output de risco pré-entrega) | Seções Standard Stack, Plotly Gauge, Pipeline Inference |
| PRES-04 | Streamlit com mapa interativo (filtros por UF/rota) | Seção Choropleth Brazil, Cache Patterns |
| PRES-05 | Streamlit com painel de EDA navegável (gráficos principais do Ato 1) | Seção Architecture Patterns, Cache Patterns |
| PRES-07 | Demo carrega artefatos pré-computados — nunca processa dados pesados ao vivo | Seção Don't Hand-Roll, Cache Patterns, Demo Reliability |
</phase_requirements>

---

## Summary

Esta fase constrói um app Streamlit multi-página que serve como demo ao vivo durante apresentação. O app tem três páginas funcionais (Preditor, Mapa Geográfico, EDA) mais uma Home opcional. Todos os artefatos pesados (pipeline joblib, parquets, PNGs) são pré-computados pelas fases anteriores — o app apenas carrega e exibe, nunca processa.

A decisão de usar `pages/` directory (locked) é totalmente suportada pelo Streamlit e cria sidebar automática sem código adicional. O padrão correto para modelos ML (joblib) é `@st.cache_resource`, não `@st.cache_data` — esta distinção é crítica para evitar erros de serialização. Para o choropleth do Brasil, é necessário um GeoJSON externo (Brasil não é built-in no Plotly) com featureidkey mapeando para `properties.sigla` (códigos UF: SP, RJ, etc.).

**Primary recommendation:** Separar toda lógica de carregamento em `utils/loaders.py` com funções decoradas, chamadas no topo de cada página para que o cache aqueça na primeira visita e todas as navegações subsequentes sejam instantâneas.

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| streamlit | >=1.30 | Framework do app web | Deploy nativo no Streamlit Cloud |
| plotly | >=5.18 | Gauge + choropleth interativos | Integração nativa com st.plotly_chart |
| pandas | >=2.0 | Leitura de parquet e manipulação | Padrão para DataFrames em Python |
| joblib | >=1.3 | Carregamento do pipeline serializado | Mesma lib usada no Phase 4 para salvar |
| pyarrow | >=14.0 | Backend para pd.read_parquet | Necessário para leitura de parquet |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Pillow (PIL) | >=10.0 | Carregar PNGs para página EDA | st.image() aceita PIL.Image ou path |
| xgboost | mesmo da Phase 4 | Deserialização do pipeline | Pipeline joblib requer a mesma versão do XGBoost usada no treino |
| scikit-learn | mesmo da Phase 4 | Preprocessors no pipeline | Mesma versão para evitar incompatibilidade de pickle |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| pages/ directory | st.navigation + st.Page | st.navigation é o método preferido em 2024+ mas locked pelo contexto; pages/ funciona perfeitamente |
| Plotly choropleth | Folium + streamlit-folium | Folium tem mais features de mapa mas requer dependência extra; Plotly já está no stack |
| PIL para PNGs | st.image(path) direto | st.image aceita path string diretamente — PIL não é necessário se não houver resize |

**Installation:**
```bash
pip install streamlit>=1.30 plotly>=5.18 pandas>=2.0 joblib>=1.3 pyarrow>=14.0 xgboost scikit-learn
```

> CRITICAL: As versões de xgboost e scikit-learn no requirements.txt devem ser EXATAMENTE as mesmas usadas no Phase 4 para treinar o pipeline. Um mismatch de versão corrompe a deserialização do joblib.

---

## Architecture Patterns

### Recommended Project Structure
```
app.py                          # entrypoint: st.set_page_config + logo + st.navigation (ou pages/ auto)
pages/
├── 1_Home.py                   # intro opcional — contexto do projeto
├── 2_Preditor.py               # formulário 5 inputs + gauge Plotly
├── 3_Mapa.py                   # choropleth + filtros
└── 4_EDA.py                    # selectbox + st.image para PNGs
utils/
└── loaders.py                  # todas as funções @st.cache_data e @st.cache_resource
data/
└── processed/
    └── geo_aggregated.parquet  # fonte do Mapa (Phase 3)
models/
└── final_pipeline.joblib       # pipeline XGBoost (Phase 4)
reports/
└── figures/
    └── *.png                   # figuras EDA (Phase 3)
requirements.txt                # versões pinadas
.streamlit/
└── config.toml                 # tema opcional
```

### Pattern 1: Separação de Loaders em utils/loaders.py
**What:** Todas as funções de I/O ficam em um módulo centralizado, decoradas com cache. Páginas importam funções, nunca leem arquivos diretamente.
**When to use:** Sempre — garante que o cache seja compartilhado entre páginas e que path management fique em um lugar só.
**Example:**
```python
# utils/loaders.py
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

BASE = Path(__file__).parent.parent  # raiz do projeto

@st.cache_resource
def load_pipeline():
    """Carrega o pipeline joblib. cache_resource: modelo é objeto global, não serializável."""
    return joblib.load(BASE / "models" / "final_pipeline.joblib")

@st.cache_data
def load_geo_data():
    """Carrega dados geográficos pré-computados. cache_data: DataFrame é serializável."""
    return pd.read_parquet(BASE / "data" / "processed" / "geo_aggregated.parquet")

@st.cache_data
def list_eda_figures():
    """Lista PNGs disponíveis em reports/figures/."""
    fig_dir = BASE / "reports" / "figures"
    return sorted(fig_dir.glob("*.png"))
```

### Pattern 2: Gauge go.Indicator para Preditor
**What:** Plotly go.Indicator com mode="gauge+number+delta", steps coloridos e threshold.
**When to use:** Página do Preditor — transforma probabilidade float (0–1) em velocímetro visual.
**Example:**
```python
# pages/2_Preditor.py  (trecho do gauge)
import plotly.graph_objects as go

def build_gauge(prob: float, threshold_low: float = 0.35, threshold_high: float = 0.65) -> go.Figure:
    """
    prob: float 0.0–1.0 (saída de pipeline.predict_proba[:, 1])
    threshold_low / threshold_high: derivados do ML-05 da Phase 4
    Cores: verde < threshold_low <= amarelo < threshold_high <= vermelho
    """
    pct = prob * 100  # exibir como percentual 0–100

    if prob < threshold_low:
        action = "Sem acao necessaria"
        needle_color = "green"
    elif prob < threshold_high:
        action = "Monitorar — acompanhar prazo e rastrear entrega"
        needle_color = "orange"
    else:
        action = "Contato preventivo via WhatsApp antes da data estimada"
        needle_color = "red"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pct,
        number={"suffix": "%"},
        title={"text": "Risco de Avaliacao Ruim"},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1},
            "bar": {"color": needle_color, "thickness": 0.25},
            "steps": [
                {"range": [0, threshold_low * 100],    "color": "#2ecc71"},   # verde
                {"range": [threshold_low * 100, threshold_high * 100], "color": "#f39c12"},  # amarelo
                {"range": [threshold_high * 100, 100], "color": "#e74c3c"},   # vermelho
            ],
            "threshold": {
                "line": {"color": "black", "width": 4},
                "thickness": 0.75,
                "value": pct
            }
        }
    ))
    return fig, action
```

### Pattern 3: Choropleth Brasil com GeoJSON externo
**What:** Plotly Express choropleth com GeoJSON dos estados brasileiros carregado via URL ou arquivo local.
**When to use:** Página do Mapa — visualização por UF de destino.
**Example:**
```python
# pages/3_Mapa.py  (trecho do choropleth)
import streamlit as st
import plotly.express as px
import json
from urllib.request import urlopen
from utils.loaders import load_geo_data

BRAZIL_GEOJSON_URL = (
    "https://raw.githubusercontent.com/codeforamerica/click_that_hood"
    "/master/public/data/brazil-states.geojson"
)

@st.cache_data
def load_brazil_geojson():
    """Cache do GeoJSON para não baixar a cada rerun."""
    with urlopen(BRAZIL_GEOJSON_URL) as resp:
        return json.load(resp)

def build_choropleth(df_filtered):
    geojson = load_brazil_geojson()
    fig = px.choropleth(
        df_filtered,
        geojson=geojson,
        locations="uf_destino",          # coluna com sigla: "SP", "RJ", etc.
        featureidkey="properties.sigla", # campo no GeoJSON que casa com a sigla
        color="pct_bad_review",
        color_continuous_scale="Reds",
        hover_data={
            "pct_bad_review": ":.1%",
            "atraso_medio_dias": ":.1f",
            "volume_pedidos": ":,",
        },
        title="% Avaliacoes Ruins por UF de Destino",
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
    return fig
```

### Pattern 4: Formulário Preditor com Input Validation
**What:** st.form para agrupar os 5 inputs e evitar reruns parciais durante digitação.
**When to use:** Sempre que houver múltiplos inputs que dependem uns dos outros para gerar output.
**Example:**
```python
# pages/2_Preditor.py  (trecho do formulário)
import streamlit as st
import pandas as pd
from utils.loaders import load_pipeline, load_categories_and_ufs

pipeline = load_pipeline()
categories, ufs = load_categories_and_ufs()  # listas do dataset

with st.form("preditor_form"):
    col1, col2 = st.columns(2)
    with col1:
        frete = st.number_input("Valor do Frete (R$)", min_value=0.0, value=20.0, step=0.5)
        valor_pedido = st.number_input("Valor do Pedido (R$)", min_value=0.0, value=100.0, step=1.0)
        prazo_dias = st.number_input("Prazo Estimado (dias)", min_value=1, max_value=90, value=10)
    with col2:
        categoria = st.selectbox("Categoria do Produto", options=categories)
        uf_origem = st.selectbox("UF de Origem", options=ufs)
        uf_destino = st.selectbox("UF de Destino", options=ufs)
    submitted = st.form_submit_button("Calcular Risco")

if submitted:
    # DataFrame deve ter EXATAMENTE os mesmos nomes de coluna usados no treino
    input_df = pd.DataFrame([{
        "freight_value": frete,
        "payment_value": valor_pedido,
        "estimated_days": prazo_dias,
        "product_category_name_english": categoria,
        "seller_state": uf_origem,
        "customer_state": uf_destino,
    }])
    prob = pipeline.predict_proba(input_df)[0, 1]
    fig, action = build_gauge(prob)
    st.plotly_chart(fig, use_container_width=True)
    st.info(f"**Acao Recomendada:** {action}")
```

> NOTE: Os nomes das colunas no DataFrame de input (`freight_value`, `payment_value`, etc.) devem bater EXATAMENTE com os nomes usados no treino da Phase 4. Verificar `src/features.py` → `PRE_DELIVERY_FEATURES` para obter a lista canônica.

### Pattern 5: Página EDA com Selectbox de PNGs
**What:** Listar PNGs do diretório, exibir via st.image com largura máxima.
**When to use:** Página EDA — navegação entre figuras estáticas sem rebuild.
**Example:**
```python
# pages/4_EDA.py
import streamlit as st
from utils.loaders import list_eda_figures

figures = list_eda_figures()
fig_names = [f.stem for f in figures]  # nomes sem extensão para exibição

selected = st.selectbox("Selecione o Grafico", options=fig_names)
idx = fig_names.index(selected)

st.image(str(figures[idx]), use_container_width=True)
```

### Anti-Patterns to Avoid
- **Chamar joblib.load() fora de função cacheada:** Modelo recarregado do disco a cada rerun — viola PRES-07 e torna o app lento.
- **Usar @st.cache_data para joblib:** Modelos ML não são serializáveis como dados; causa erros silenciosos ou crashes. Use `@st.cache_resource`.
- **Colocar pd.read_parquet() diretamente no corpo da página:** Executado em todo rerun. Sempre encapsular em função com decorator.
- **Import pesado no nível de módulo:** `import xgboost` no topo de todas as páginas aumenta cold start. Centralizar em `loaders.py` que é importado sob demanda.
- **st.set_page_config() fora do topo:** Deve ser a primeira chamada Streamlit em cada arquivo de página, antes de qualquer outro st.* call.
- **Hardcodar paths absolutos:** Usar `Path(__file__).parent.parent` para portabilidade entre local e Streamlit Cloud.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Gauge visual com faixas de cor | Matplotlib semicírculo custom | `go.Indicator` do Plotly | API nativa, interativo, responsivo, integra direto no st.plotly_chart |
| Mapa de estados brasileiros | Desenhar polígonos manualmente | GeoJSON de estados BR + px.choropleth | GeoJSON oficial com geometrias validadas do IBGE/codeforamerica |
| Sidebar de navegação entre páginas | st.sidebar.radio + importação manual | pages/ directory nativo | Streamlit gera sidebar e URLs automaticamente |
| Cache de artefatos entre reruns | session_state manual com flags | @st.cache_data / @st.cache_resource | Invalidação automática por hash de parâmetros + gerenciamento de memória |
| Pipeline inference | Re-implementar preprocessors manualmente | pipeline.predict_proba(input_df) | Pipeline encapsula todo o preprocessing — uma chamada faz tudo |

**Key insight:** O app é um loader/viewer, não um processador. Todo o valor computacional está nos artefatos da Phase 4. O código do app deve ser thin: carregar → exibir → interagir.

---

## Common Pitfalls

### Pitfall 1: Mismatch de versão joblib/XGBoost/scikit-learn
**What goes wrong:** O pipeline carrega com `ValueError: Incompatible sklearn version` ou `XGBoostError` ao deserializar.
**Why it happens:** joblib/pickle serializa metadados da versão. Streamlit Cloud instala a versão mais recente se não pinada.
**How to avoid:** requirements.txt deve pinar EXATAMENTE as mesmas versões usadas na Phase 4. Verificar com `pip freeze` no ambiente de treino.
**Warning signs:** Erro imediatamente ao `joblib.load()` no startup.

### Pitfall 2: Feature names mismatch no pipeline.predict_proba()
**What goes wrong:** `XGBoost: feature_names mismatch` ou `ValueError: X has N features but model expects M`.
**Why it happens:** O pipeline foi treinado com DataFrame de nomes específicos. O formulário passa nomes diferentes.
**How to avoid:** Importar `PRE_DELIVERY_FEATURES` de `src/features.py` e usar os mesmos nomes de coluna exatamente. Construir o DataFrame de input com dict usando as chaves corretas.
**Warning signs:** Erro ao clicar "Calcular Risco" pela primeira vez.

### Pitfall 3: GeoJSON sigla vs. id mismatch no choropleth
**What goes wrong:** Estados aparecem em branco ou com cor errada no mapa.
**Why it happens:** `featureidkey` aponta para campo errado no GeoJSON. O GeoJSON codeforamerica usa `properties.sigla` (string como "SP"), não o campo `id`.
**How to avoid:** Usar `featureidkey="properties.sigla"` e garantir que a coluna `uf_destino` no parquet contém siglas em uppercase ("SP", "RJ") e não códigos IBGE numéricos.
**Warning signs:** Mapa renderiza mas todos os estados ficam cinza.

### Pitfall 4: st.set_page_config não é primeira chamada
**What goes wrong:** `StreamlitAPIException: set_page_config() can only be called once per app, and must be called as the first Streamlit command in your script`.
**Why it happens:** Qualquer import que execute código Streamlit antes do set_page_config, ou chamada em posição errada no arquivo.
**How to avoid:** Sempre colocar `st.set_page_config()` como primeira linha após imports no arquivo da página.
**Warning signs:** Crash imediato ao navegar para a página.

### Pitfall 5: GeoJSON carregado via URL lento ou indisponível ao vivo
**What goes wrong:** Mapa demora 3–5s para carregar ou falha se não há internet no evento.
**Why it happens:** `urlopen()` faz request HTTP a cada cold start; sem cache.
**How to avoid:** Decorar `load_brazil_geojson()` com `@st.cache_data`. Alternativamente, baixar o GeoJSON e colocar no repositório em `data/geo/brazil-states.geojson` como fallback offline — crítico para o Plano B local.
**Warning signs:** Mapa demora mesmo após primeira carga.

### Pitfall 6: @st.cache_data em modelo joblib
**What goes wrong:** Erro de serialização ou comportamento imprevisível ao retornar modelo.
**Why it happens:** `@st.cache_data` serializa/deserializa o retorno via pickle para copiar entre sessões. Modelos ML frequentemente têm state interno não serializável desta forma.
**How to avoid:** Modelos ML SEMPRE com `@st.cache_resource`. DataFrames e valores simples com `@st.cache_data`.
**Warning signs:** Warning "Object of type X is not JSON serializable" ou erros intermitentes de predição entre usuários.

### Pitfall 7: Cold start lento no Streamlit Cloud (primeira visita)
**What goes wrong:** Primeira visita ao app demora 30–60s (ambiente sendo inicializado).
**Why it happens:** Streamlit Cloud faz "sleep" em apps inactivos. Cold start baixa dependências e inicializa ambiente.
**How to avoid:** Pré-aquecer enviando request antes da apresentação. Não há solução de código — é limitação do tier Community. Manter Plano B (local) como contingência real.
**Warning signs:** App mostra spinner por mais de 15s na primeira visita.

---

## Code Examples

Verified patterns from official sources:

### Cache Resource vs Cache Data — Regra de Ouro
```python
# Source: Streamlit docs — https://docs.streamlit.io/develop/concepts/architecture/caching
import streamlit as st
import pandas as pd
import joblib

# MODELOS: cache_resource (objeto global, não copiado entre sessões)
@st.cache_resource
def load_pipeline():
    return joblib.load("models/final_pipeline.joblib")

# DATAFRAMES: cache_data (serializado, copiado por sessão)
@st.cache_data
def load_geo_data():
    return pd.read_parquet("data/processed/geo_aggregated.parquet")

# IMAGENS: não precisa cache — st.image lê do disco uma vez
```

### Gauge com Thresholds Dinâmicos da Phase 4
```python
# Os thresholds devem ser lidos de um artefato da Phase 4
# Ex: models/threshold.json ou direto de um parquet de métricas
import json
from pathlib import Path

@st.cache_data
def load_threshold():
    """Threshold operacional definido na Phase 4 ML-05."""
    threshold_path = Path("models") / "threshold.json"
    if threshold_path.exists():
        with open(threshold_path) as f:
            return json.load(f)["threshold"]
    return 0.5  # fallback se arquivo não existir

THRESHOLD = load_threshold()
# Para gauge tri-color: baixo = THRESHOLD * 0.6, alto = THRESHOLD
THRESHOLD_LOW = THRESHOLD * 0.6
THRESHOLD_HIGH = THRESHOLD
```

### Filtros do Mapa com st.multiselect
```python
# pages/3_Mapa.py — filtros interativos
df = load_geo_data()

col1, col2, col3, col4 = st.columns(4)
with col1:
    uf_orig_filter = st.multiselect("UF Origem", options=sorted(df["uf_origem"].unique()), default=[])
with col2:
    uf_dest_filter = st.multiselect("UF Destino", options=sorted(df["uf_destino"].unique()), default=[])
with col3:
    cat_filter = st.multiselect("Categoria", options=sorted(df["categoria"].unique()), default=[])
with col4:
    risco_filter = st.multiselect("Faixa de Risco", options=["Baixo", "Medio", "Alto"], default=[])

# Aplicar filtros (sem alterar df original — evitar mutação de cache)
df_filtered = df.copy()
if uf_orig_filter:
    df_filtered = df_filtered[df_filtered["uf_origem"].isin(uf_orig_filter)]
if uf_dest_filter:
    df_filtered = df_filtered[df_filtered["uf_destino"].isin(uf_dest_filter)]
# ... etc
```

### app.py Entrypoint com pages/ directory
```python
# app.py — entrypoint (streamlit run app.py)
import streamlit as st

st.set_page_config(
    page_title="Olist Risk Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Olist — Sistema de Alerta de Risco Pre-Entrega")
st.markdown("""
Bem-vindo ao dashboard de risco logístico. Use o menu lateral para navegar:

- **Preditor**: Estime o risco de avaliação ruim para um pedido
- **Mapa Geografico**: Visualize concentração de riscos por estado
- **EDA**: Explore as análises do Ato 1
""")
```

### requirements.txt Seguro para Streamlit Cloud
```txt
# requirements.txt — versões PINADAS para evitar breaking changes
streamlit==1.32.0
plotly==5.18.0
pandas==2.1.4
pyarrow==14.0.2
joblib==1.3.2
xgboost==2.0.3        # MESMA versão do Phase 4
scikit-learn==1.4.0   # MESMA versão do Phase 4
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| pages/ directory | st.navigation + st.Page (preferido) | Streamlit 1.29 (2023) | pages/ ainda funciona — locked pelo contexto, mas st.navigation oferece mais controle |
| @st.cache (deprecated) | @st.cache_data / @st.cache_resource | Streamlit 1.18 (2022) | @st.cache causa DeprecationWarning; usar os novos sempre |
| st.experimental_memo | @st.cache_data | Streamlit 1.18 (2022) | st.experimental_memo é alias deprecated |
| use_column_width=True (st.image) | use_container_width=True | Streamlit 1.20 (2022) | Parâmetro renomeado; use_column_width gera warning |

**Deprecated/outdated:**
- `@st.cache`: Substituído por `@st.cache_data` e `@st.cache_resource`. Não usar.
- `use_column_width=True` em `st.image` e `st.plotly_chart`: Renomeado para `use_container_width=True`.
- `st.beta_columns`: Renomeado para `st.columns`.

---

## Open Questions

1. **Nomes exatos das colunas no PRE_DELIVERY_FEATURES**
   - What we know: `src/features.py` define a lista — será criada na Phase 1
   - What's unclear: Nomes serão em inglês ou português? (e.g., `freight_value` ou `valor_frete`)
   - Recommendation: Página do Preditor deve importar `PRE_DELIVERY_FEATURES` diretamente de `src/features.py` em vez de hardcodar — isso cria contrato automático entre Phase 1/4 e Phase 6

2. **Formato do geo_aggregated.parquet (colunas exatas)**
   - What we know: Exportado na Phase 3 (EDA-03) com dados por UF
   - What's unclear: Nomes das colunas (pct_bad_review? bad_review_rate? uf_destino? estado_destino?)
   - Recommendation: Phase 6 deve ter uma célula de verificação que faz `df.columns.tolist()` antes de construir o choropleth

3. **Threshold da Phase 4 — formato de persistência**
   - What we know: ML-05 define threshold operacional; pipeline está em `models/final_pipeline.joblib`
   - What's unclear: Threshold foi salvo separadamente (JSON/parquet) ou precisa ser lido de algum artefato?
   - Recommendation: Phase 6 planner deve verificar se Phase 4 exporta `models/threshold.json`; se não, definir um fallback fixo com comentário explicando o valor

4. **GeoJSON offline para Plano B**
   - What we know: Plano B é local sem internet do evento
   - What's unclear: Se o evento não tem internet, `urlopen(GEOJSON_URL)` falha
   - Recommendation: Baixar GeoJSON para `data/geo/brazil-states.geojson` e usar path local; URL como fallback

---

## Validation Architecture

> Skipped — `workflow.nyquist_validation` not present in config.json (defaults to disabled).

---

## Sources

### Primary (HIGH confidence)
- Streamlit official docs — multipage apps, pages/ directory, st.navigation: https://docs.streamlit.io/develop/concepts/multipage-apps
- Streamlit official docs — caching st.cache_data vs st.cache_resource: https://docs.streamlit.io/develop/concepts/architecture/caching
- Plotly official docs — Gauge Charts (go.Indicator): https://plotly.com/python/gauge-charts/
- Plotly official docs — Choropleth Maps in Python: https://plotly.com/python/choropleth-maps/

### Secondary (MEDIUM confidence)
- Streamlit Community Forum — Plotly Indicator Gauge Demo: https://discuss.streamlit.io/t/plotly-indicator-gauge-demo/54544
- GitHub codeforamerica — Brazil states GeoJSON (featureidkey properties.sigla): https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson
- Streamlit official docs — Streamlit Cloud deployment: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app

### Tertiary (LOW confidence — verificar antes de implementar)
- Streamlit Community Forum — Plotly gauge overwriting itself (bug de sobreposição): https://discuss.streamlit.io/t/plotly-gauge-overwriting-itself/46651 — Verificar se ainda ocorre na versão pinada
- Streamlit Community Cloud resource limits — limites de CPU/memória não documentados publicamente com valores exatos; validar empiricamente

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — Streamlit/Plotly APIs verificadas em docs oficiais
- Architecture: HIGH — Padrões pages/ directory e loaders.py verificados em docs oficiais
- Pitfalls: HIGH (versão mismatch, feature names, cache) / MEDIUM (cold start timing no Cloud)
- GeoJSON Brasil: MEDIUM — URL verificada em múltiplas fontes mas geometrias dependem do repositório externo permanecer ativo

**Research date:** 2026-03-01
**Valid until:** 2026-06-01 (Streamlit API é estável; risco de mudança em 90 dias é baixo)
