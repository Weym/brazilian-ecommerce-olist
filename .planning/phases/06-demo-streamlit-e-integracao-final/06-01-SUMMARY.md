---
phase: 06-demo-streamlit-e-integracao-final
plan: "01"
subsystem: ui
tags: [streamlit, plotly, xgboost, scikit-learn, geojson, joblib, pandas]

# Dependency graph
requires:
  - phase: 04-ml-ato-2
    provides: models/final_pipeline.joblib (XGBoost pipeline serializado)
  - phase: 03-eda-ato-1
    provides: data/processed/geo_aggregated.parquet e reports/figures/*.png

provides:
  - app.py: entrypoint Streamlit com set_page_config e descricao do projeto
  - utils/loaders.py: contrato de I/O centralizado com 6 funcoes cacheadas
  - pages/1_Home.py: pagina de introducao navegavel via sidebar
  - data/geo/brazil-states.geojson: GeoJSON offline 27 estados com properties.sigla
  - requirements.txt: versoes pinadas do ambiente de treino
  - .streamlit/config.toml: tema de apresentacao

affects:
  - 06-02-PLAN (Preditor de Risco usa load_pipeline e load_categories_and_ufs)
  - 06-03-PLAN (Mapa usa load_geo_data e load_brazil_geojson)
  - 06-04-PLAN (EDA usa list_eda_figures)

# Tech tracking
tech-stack:
  added: [streamlit==1.44.0]
  patterns:
    - utils/loaders.py como unico ponto de I/O — nenhuma pagina le arquivos diretamente
    - "@st.cache_resource para modelos ML (joblib), @st.cache_data para DataFrames e JSON"
    - GeoJSON local commitado para uso offline (Plano B sem internet no evento)

key-files:
  created:
    - app.py
    - utils/__init__.py
    - utils/loaders.py
    - pages/1_Home.py
    - data/geo/brazil-states.geojson
    - .streamlit/config.toml
  modified:
    - requirements.txt

key-decisions:
  - "requirements.txt pina versoes reais do ambiente de treino: xgboost==3.2.0, scikit-learn==1.8.0 (nao as versoes conservadoras do plano — ambiente ja existia)"
  - "streamlit==1.44.0 instalado (ultima versao estavel, compativel com python 3.14)"
  - "GeoJSON baixado via codeforamerica/click_that_hood com 27 features e properties.sigla confirmados"

patterns-established:
  - "Pattern I/O: toda leitura de arquivo passa por utils/loaders.py — paginas nunca usam pd.read_csv, joblib.load ou json.load diretamente"
  - "Pattern cache: @st.cache_resource para objetos ML (nao copiados entre sessoes), @st.cache_data para DataFrames/JSON (copiados por sessao)"

requirements-completed: [PRES-07]

# Metrics
duration: 12min
completed: 2026-03-01
---

# Phase 6 Plan 01: Scaffold Streamlit — App.py, Loaders e Infraestrutura Summary

**Scaffold Streamlit com entrypoint, utils/loaders.py centralizado (6 funcoes cacheadas), GeoJSON offline dos 27 estados e requirements.txt pinado ao ambiente de treino real**

## Performance

- **Duration:** 12 min
- **Started:** 2026-03-01T00:00:00Z
- **Completed:** 2026-03-01T00:12:00Z
- **Tasks:** 2
- **Files modified:** 7

## Accomplishments

- utils/loaders.py criado como unico ponto de I/O do app — contrato que todas as paginas (02-04) dependem
- data/geo/brazil-states.geojson baixado e salvo localmente com 27 estados brasileiros e campo `properties.sigla` validado
- requirements.txt atualizado com versoes pinadas reais do ambiente de treino (xgboost==3.2.0, scikit-learn==1.8.0)
- pages/1_Home.py com tabela de paginas, instrucoes de teste rapido e metricas do projeto

## Task Commits

Cada task foi commitada atomicamente:

1. **Task 1: Scaffold app.py, utils/loaders.py e .streamlit/config.toml** - `6d6033d` (feat)
2. **Task 2: requirements.txt pinado, GeoJSON local e pagina Home** - `44d53da` (feat)

**Plan metadata:** a ser gerado (docs: complete plan)

## Files Created/Modified

- `app.py` - Entrypoint Streamlit com set_page_config e descricao das 3 paginas
- `utils/__init__.py` - Modulo Python vazio para utils/
- `utils/loaders.py` - 6 funcoes de carregamento: load_pipeline (@cache_resource), load_geo_data, load_threshold, load_brazil_geojson, list_eda_figures, load_categories_and_ufs (todos @cache_data)
- `.streamlit/config.toml` - Tema com primaryColor=#e74c3c e server headless
- `requirements.txt` - Versoes pinadas: streamlit==1.44.0, xgboost==3.2.0, scikit-learn==1.8.0, plotly==6.5.2, pandas==2.3.3, pyarrow==23.0.1, joblib==1.5.3, Pillow==11.3.0
- `data/geo/brazil-states.geojson` - GeoJSON 27 estados com properties.sigla (baixado de codeforamerica)
- `pages/1_Home.py` - Pagina de introducao com tabela de paginas, metricas e instrucoes

## Decisions Made

- **Versoes pinadas reais vs plano**: O plano sugeria versoes conservadoras (xgboost==2.0.3, scikit-learn==1.4.0), mas o ambiente de treino ja tinha xgboost==3.2.0 e scikit-learn==1.8.0 — pinado com as versoes reais para garantir compatibilidade de desserializacao do joblib
- **streamlit==1.44.0**: Versao instalada (nao 1.32.0 do plano) — compativel com python 3.14
- **GeoJSON validado**: 27 features confirmadas com properties.sigla ('AC', 'SP', etc.)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Versoes pinadas atualizadas para corresponder ao ambiente real**

- **Found during:** Task 2 (requirements.txt)
- **Issue:** O plano especificava xgboost==2.0.3 e scikit-learn==1.4.0, mas o ambiente de treino tem xgboost==3.2.0 e scikit-learn==1.8.0 — pinar versoes erradas causaria erro de desserializacao do final_pipeline.joblib
- **Fix:** Pinadas as versoes reais do ambiente: xgboost==3.2.0, scikit-learn==1.8.0, streamlit==1.44.0, plotly==6.5.2, pandas==2.3.3, pyarrow==23.0.1, joblib==1.5.3, Pillow==11.3.0
- **Files modified:** requirements.txt
- **Verification:** pip show confirma versoes correspondentes; final_pipeline.joblib carregado com xgboost==3.2.0
- **Committed in:** 44d53da (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (Rule 1 - versoes pinadas ao ambiente real em vez das versoes conservadoras do plano)
**Impact on plan:** Correcao essencial — versoes erradas causariam falha de carregamento do modelo na pagina do Preditor.

## Issues Encountered

- Comandos com multiplas aspas no shell Windows causavam erros de parse — solucao: scripts Python temporarios para operacoes complexas

## Next Phase Readiness

- utils/loaders.py pronto com contrato completo — planos 06-02, 06-03, 06-04 podem importar diretamente
- GeoJSON offline disponivel para choropleth sem dependencia de internet
- requirements.txt pinado ao ambiente real — reproducibilidade garantida
- pages/ directory criado e pronto para receber 2_Preditor.py, 3_Mapa.py, 4_EDA.py

---
*Phase: 06-demo-streamlit-e-integracao-final*
*Completed: 2026-03-01*

## Self-Check: PASSED
