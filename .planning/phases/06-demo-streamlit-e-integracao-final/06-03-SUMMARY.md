---
phase: 06-demo-streamlit-e-integracao-final
plan: "03"
subsystem: ui
tags: [streamlit, plotly, choropleth, geojson, pandas, visualization]

# Dependency graph
requires:
  - phase: 06-01
    provides: utils/loaders.py com load_geo_data() e load_brazil_geojson()
  - phase: 03-eda-ato-1
    provides: data/processed/geo_aggregated.parquet com dados geograficos agregados
provides:
  - pages/3_Mapa.py — pagina Streamlit com choropleth interativo dos estados brasileiros
affects:
  - 06-04
  - 06-05

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "detect_column() helper para resolucao resiliente de nomes de colunas em runtime"
    - "Normalizacao automatica de escala 0-1 -> 0-100 para percentuais"
    - "Bloco de debug expansivel st.expander para diagnostico sem poluir UI"
    - "df_filtered = df.copy() antes de qualquer filtro para nao mutar df cacheado"

key-files:
  created:
    - pages/3_Mapa.py
  modified: []

key-decisions:
  - "detect_column() com lista de candidatos garante robustez mesmo se Phase 3 usou nomes diferentes"
  - "featureidkey='properties.sigla' confirmado como campo correto no GeoJSON codeforamerica (nao 'id' nem 'properties.id')"
  - "Normalizacao pct_bad_review: if max <= 1.01 multiplica por 100 — detecta escala automaticamente"
  - "faixa_risco calculada via pd.cut(quantile) se coluna nao existir no parquet — resiliente a ausencia"
  - "Agregacao groupby(COL_UF_DEST) antes do choropleth garante uma linha por estado independente dos filtros"

patterns-established:
  - "Deteccao defensiva de colunas: detect_column(df, candidates, default) — toda pagina que consumir parquets de fases anteriores deve usar este padrao"
  - "Bloco de debug expansivel: st.expander('Debug: colunas do ...') — visivel para dev, escondido para audience"

requirements-completed: [PRES-04]

# Metrics
duration: 2min
completed: 2026-03-02
---

# Phase 6 Plan 03: Mapa Geografico Summary

**Choropleth Plotly interativo dos 27 estados brasileiros colorizado por % bad reviews, com 4 filtros multiselect e hover tri-metrico, carregado 100% via loaders sem I/O direto**

## Performance

- **Duration:** 2 min
- **Started:** 2026-03-02T01:01:18Z
- **Completed:** 2026-03-02T01:03:00Z
- **Tasks:** 1 of 1
- **Files modified:** 1

## Accomplishments

- Choropleth Plotly dos estados brasileiros via featureidkey="properties.sigla" (campo correto para GeoJSON codeforamerica)
- 4 filtros interativos em colunas horizontais: UF Origem, UF Destino, Categoria, Faixa de Risco
- Hover com 3 metricas por estado: % avaliacoes ruins, atraso medio em dias, volume de pedidos
- Deteccao automatica de nomes de colunas com helper detect_column() — resiliente a nomes diferentes da Phase 3
- Normalizacao automatica pct_bad_review de escala 0-1 para 0-100 via threshold max <= 1.01
- Calculo de faixa_risco via quantis (Baixo/Medio/Alto) se coluna ausente no parquet
- Bloco de debug expansivel mostrando colunas reais e mapeamento para diagnostico rapido
- Zero chamadas diretas a pd.read_parquet() ou json.load() — I/O exclusivamente via utils/loaders.py

## Task Commits

1. **Task 1: Pagina Mapa — choropleth + filtros interativos + hover** - `d888af2` (feat)

## Files Created/Modified

- `pages/3_Mapa.py` - Pagina Streamlit com choropleth interativo, 4 filtros, hover tri-metrico e debug expansivel (163 linhas)

## Decisions Made

- `detect_column()` com lista de candidatos ordenados por prioridade: garante que a pagina funciona mesmo que Phase 3 tenha usado nomes ligeiramente diferentes (ex: "customer_state" vs "uf_destino")
- `featureidkey="properties.sigla"` confirmado como o campo correto — usar "id" ou "properties.id" causa estados em branco no choropleth
- Normalizacao automatica de escala: `if df[col].max() <= 1.01: *= 100` detecta escala 0-1 sem configuracao manual
- `faixa_risco` calculada via `pd.cut(quantile(0.33, 0.67))` quando coluna ausente — choropleth funciona mesmo sem Phase 3 ter gerado a coluna
- Agregacao `groupby(COL_UF_DEST)` antes do choropleth obrigatorio: garante 1 linha por estado apos aplicacao de filtros multi-linha

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- Verificacao inicial falhou com UnicodeDecodeError no Windows (cp1252 vs UTF-8 por causa do emoji na page_icon). Resolvido adicionando `encoding='utf-8'` na chamada open() do verificador — o arquivo em si esta correto.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- pages/3_Mapa.py pronto para integracao com o app principal (Home, Preditor, Mapa)
- GeoJSON local em data/geo/brazil-states.geojson ja commitado (offline-first para apresentacao)
- Se geo_aggregated.parquet nao existir, load_geo_data() levanta FileNotFoundError com mensagem clara indicando que Phase 3 deve ser executada primeiro
- Plan 06-04 pode prosseguir com pagina EDA ou integracao final

---
*Phase: 06-demo-streamlit-e-integracao-final*
*Completed: 2026-03-02*

## Self-Check: PASSED

- pages/3_Mapa.py: FOUND
- 06-03-SUMMARY.md: FOUND
- Commit d888af2: FOUND
