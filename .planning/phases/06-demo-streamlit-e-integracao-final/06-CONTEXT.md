# Phase 6: Demo Streamlit e Integracao Final - Context

**Gathered:** 2026-03-01
**Status:** Ready for planning

<domain>
## Phase Boundary

App Streamlit multi-página que serve como demo ao vivo durante a apresentação: carrega artefatos pré-computados (parquet, joblib, PNG) e não executa nenhum join, treino ou processamento pesado ao vivo. O app tem 3 páginas funcionais — Preditor de Risco, Mapa Geográfico, e Painel de EDA — mais uma página Home/introdução opcional. Deploy primário no Streamlit Cloud (URL pública para acesso do celular dos jurados), com fallback local como plano B.

</domain>

<decisions>
## Implementation Decisions

### Estrutura de navegação
- `pages/` directory nativo do Streamlit — cada página é um arquivo `.py` separado
- Sidebar automática com links para cada página
- URLs únicas por página (sem rebuild ao trocar de seção)

### Página do Preditor
- **Inputs do formulário** (5 features pré-entrega, disponíveis antes da expedição):
  - Preço do frete (number_input, R$)
  - Valor do pedido (number_input, R$)
  - Prazo estimado em dias (slider ou number_input)
  - Categoria do produto (selectbox com lista das categorias do dataset)
  - UF de Origem e UF de Destino (dois selectbox com estados brasileiros)
- **Exibição do score:** gauge visual interativo do Plotly (estilo velocímetro)
  - Verde (Risco Baixo) / Amarelo (Risco Médio) / Vermelho (Risco Alto)
  - Limiares: derivados do threshold operacional da curva PR (ML-05, Phase 4) — Claude's Discretion
- **Ação Recomendada:** uma linha clara abaixo do gauge por faixa:
  - Verde: "Sem ação necessária"
  - Amarelo: "Monitorar — acompanhar prazo e rastrear entrega"
  - Vermelho: "Contato preventivo via WhatsApp antes da data estimada"

### Página do Mapa
- **Biblioteca:** Plotly choropleth — integração nativa, rápida de renderizar, responsiva no Streamlit
- **Métrica colorizada:** % de bad reviews (1-2 estrelas) por UF de destino
- **Filtros interativos:**
  - UF de Origem
  - UF de Destino
  - Categoria do produto
  - Faixa de risco
- **Hover de cada estado:** 3 métricas — % bad review + atraso médio em dias + volume de pedidos
- **Fonte de dados:** `data/processed/geo_aggregated.parquet` (pré-computado na Phase 3)

### Página de EDA
- Figuras exibidas como **imagens estáticas PNG** carregadas de `reports/figures/`
- Navegação entre gráficos via `st.selectbox` ou `st.radio` (sem rebuild, carregamento instantâneo)
- Gráficos do Ato 1: boxplot atraso vs nota, scatter frete vs nota, choropleth UF, heatmap rotas

### Performance e Cache
- `@st.cache_data` em todas as leituras de artefatos (parquet, joblib)
- Nenhum join, nenhum treino ao vivo — apenas `pd.read_parquet()` e `joblib.load()`
- Deploy primário: **Streamlit Cloud** (URL pública — jurados acessam pelo celular)
- Plano B: `streamlit run` local no notebook do apresentador (sem depender de internet do evento)

### Claude's Discretion
- Limiares exatos do gauge (Verde/Amarelo/Vermelho) derivados do threshold operacional da ML-05
- Layout interno de cada página (proporção de colunas, espaçamento)
- Tratamento de encoding para categorias no pipeline (`LabelEncoder` ou `OrdinalEncoder`)
- Página Home/landing opcional com resumo do projeto

</decisions>

<specifics>
## Specific Ideas

- Gauge tipo velocímetro com escala 0-100% e ponteiro animado — referência: `go.Indicator` do Plotly com `mode="gauge+number"`
- Os jurados devem conseguir abrir a URL no celular durante o pitch e interagir com o preditor ao vivo
- A ação recomendada em texto deve ser legível sem explicação adicional — o apresentador não precisa explicar o que fazer
- O filtro "Faixa de risco" no mapa cria a ponte visual entre o painel geográfico e o motor de ML — peça-chave da narrativa

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `models/final_pipeline.joblib`: Pipeline XGBoost completo da Phase 4 — carregado com `joblib.load()` no Preditor
- `data/processed/geo_aggregated.parquet`: Dados geográficos agregados por UF da Phase 3 — base do Mapa
- `reports/figures/*.png`: Figuras exportadas na Phase 3 — carregadas diretamente como imagens na página EDA
- `src/features.py` → `PRE_DELIVERY_FEATURES`: allow-list das features pré-entrega — define exatamente quais inputs o formulário do Preditor precisa expor

### Established Patterns
- Artefatos pré-computados como contrato: nenhuma página do app gera dados ao vivo
- `@st.cache_data` como padrão universal para todos os `pd.read_parquet()` e `joblib.load()`

### Integration Points
- Preditor conecta ao `models/final_pipeline.joblib` (Phase 4, ML-07)
- Mapa conecta ao `data/processed/geo_aggregated.parquet` (Phase 3, EDA-03)
- EDA conecta aos PNGs em `reports/figures/` (Phase 3, EDA-01 a EDA-05)
- Features do formulário devem bater exatamente com `PRE_DELIVERY_FEATURES` de `src/features.py`

</code_context>

<deferred>
## Deferred Ideas

- Nenhuma — discussão ficou dentro do escopo da Phase 6

</deferred>

---

*Phase: 06-demo-streamlit-e-integracao-final*
*Context gathered: 2026-03-01*
