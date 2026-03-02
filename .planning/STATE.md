---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: unknown
last_updated: "2026-03-01T24:05:00Z"
progress:
  total_phases: 6
  completed_phases: 4
  total_plans: 22
  completed_plans: 15
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-01)

**Core value:** Mostrar que e possivel agir antes do problema acontecer — transformar dados historicos de logistica em um sistema de alerta precoce que permite intervencao antes da entrega e da avaliacao ruim.
**Current focus:** Phase 5 — Narrativa e Slides (Plan 05-02 complete — relatorio tecnico e README com resultados)

## Current Position

Phase: 5 of 6 (Narrativa e Slides) — EM ANDAMENTO
Plan: 2 of 3 in current phase — COMPLETO
Status: Plan 05-02 complete — docs/report.md (2183 palavras, 7 secoes) e README atualizado com secao Resultados completa
Last activity: 2026-03-02 — Plan 05-02 completo: docs/report.md e README atualizados — commits fca5820, 01bde21

Progress: [█████████░] 73%

## Performance Metrics

**Velocity:**
- Total plans completed: 6
- Average duration: 3min
- Total execution time: 0h 24min

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01-kickoff-e-contratos | 5 completed | 17min | ~3min |
| 02-data-foundation | 2 completed | 21min | ~10min |

**Recent Trend:**
- Last 5 plans: 01-02 (2min), 01-03 (3min), 01-04 (5min), 01-05 (5min), 02-01 (7min)
- Trend: stable, entering execution phase (data+ML)

*Updated after each plan completion*
| Phase 02 P01 | 6 | 2 tasks | 1 files |
| Phase 01 P05 | 5 | 2 tasks | 5 files |
| Phase 01 P04 | 5 | 1 tasks | 1 files |
| Phase 01 P02 | 3 | 2 tasks | 4 files |
| Phase 02-data-foundation P02 | 14 | 2 tasks | 1 files |
| Phase 02-data-foundation P03 | 15 | 2 tasks | 3 files |
| Phase 03-eda-ato-1 P03-01 | 6 | 3 tasks | 5 files |
| Phase 03-eda-ato-1 P02 | 15 | 2 tasks | 6 files |
| Phase 04-ml-ato-2 P04-01 | 18 | 2 tasks | 6 files |
| Phase 04-ml-ato-2 P04-02 | 6 | 2 tasks | 3 files |
| Phase 04-ml-ato-2 P04-03 | 10 | 2 tasks | 2 files |
| Phase 04-ml-ato-2 P04-04 | 5 | 2 tasks | 2 files |
| Phase 05-narrativa-e-slides P05-01 | 15 | 2 tasks | 3 files |
| Phase 05-narrativa-e-slides P05-02 | 12 | 2 tasks | 2 files |

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- [Kickoff]: Target = estrelas 1-2 (binario: positivo = insatisfacao real) — pendente confirmacao formal na Phase 1
- [Kickoff]: Demo em Streamlit com artefatos pre-computados — nenhum processamento pesado ao vivo
- [Kickoff]: Baseline logistico obrigatorio antes de XGBoost — garante entregavel mesmo se ML avancado nao fechar
- [Kickoff]: Corte temporal de features = `order_approved_at` (nenhuma variavel pos-entrega no modelo)
- [01-01]: nbstripout configurado em modo git filter (nao hook) — working copy preservada, outputs filtrados no staging
- [01-01]: requirements.txt (nao pyproject.toml) escolhido pela simplicidade para sprint de 1 semana
- [01-01]: src/__init__.py e src/features.py excluidos do Plan 01 — responsabilidade do Plan 02
- [01-03]: PR-AUC e Recall definidos como unicas headline metrics — Accuracy e ROC-AUC explicitamente proibidos por enganarem em datasets desbalanceados
- [01-03]: Limiar de decisao nao e 0.5 — escolhido na curva PR da Phase 4, criterio F1 ou acionabilidade operacional
- [01-03]: Baseline logistico com class_weight='balanced' obrigatorio antes de XGBoost — garante entregavel e valida valor do modelo avancado
- [Phase 01]: Target = bad_review: review_score in {1,2} -> 1, caso contrario 0 (int8)
- [Phase 01]: Ancora temporal = order_approved_at (nao order_purchase_timestamp)
- [Phase 01]: Outlier de frete: flaggar com high_freight_flag, nao remover
- [Phase 01]: Outlier de prazo >30 dias: incluir na EDA; Phase 4 decide tratamento para ML
- [Phase 01-kickoff-e-contratos]: PRE_DELIVERY_FEATURES has exactly 13 columns with temporal anchor order_approved_at (blocked decision)
- [Phase 01-kickoff-e-contratos]: seller_customer_distance_km declared in Phase 1 contract even though computed in Phase 2 (Haversine)
- [01-05]: Notebooks placeholder criados antes do sprint para prevenir conflitos de merge — cada .ipynb existe no git como propriedade de uma pessoa
- [01-05]: Celula padrao usa Path.cwd().parent como PROJECT_ROOT — funciona quando notebook executado de notebooks/
- [01-05]: outputs: [] e estado correto pre-execucao nos placeholders — nbstripout filtra no staging sem modificar working copy
- [02-01]: seller_zip_code_prefix vem como float64 apos merge chain (NaN promove int->float) — converter via Int64 nullable antes de str.zfill(5) para evitar '9350.0' ao inves de '09350'
- [02-01]: geo_agg tem 19015 linhas unicas de 1000163 (ratio ~52.6x) — assert uniqueness incluido no notebook
- [02-01]: gold_with_geo (97456, 32) — 1985 pedidos removidos (canceled/unavailable/sem review_score/sem order_approved_at)
- [02-01]: Cobertura geo: sellers 99.8%, customers 99.7% — valores dentro do esperado para dataset brasileiro
- [Phase 02-02]: haversine library not installed — numpy vectorized formula used (R=6371 km); mediana SP->AM=2693 km confirms correctness
- [Phase 02-02]: Haversine max threshold relaxed 6000->10000 km — Olist geo border prefixes produce up to 8677 km; values ARE in km (confirmed by max > 100)
- [Phase 02-02]: bad_review = 13.9% (not 15-20% estimated) — acceptable range; scale_pos_weight XGBoost = 6.21 documented for Phase 4
- [Phase 02-02]: COLUMN_TAGS contract: 38 columns explicitly tagged pre-entrega / pos-entrega / target — anti-leakage contract for Phase 3 EDA and Phase 4 ML
- [Phase 02-03]: olist_gold.parquet frozen contract: 97456 rows x 38 cols, bad_review=13.9%, scale_pos_weight=6.2, distance max=8677 km confirmed in km
- [Phase 02-03]: Smoke test distance threshold = 10000 km (not 6000) — Olist geo border prefixes produce up to 8677 km, already decided in Phase 02-02
- [Phase 02-03]: 7 pedidos with estimated_delivery < approved_at kept as AVISO — Phase 3 EDA to investigate
- [Phase 02-03]: seller_id 3 nulls (0.003%) accepted — critical columns (order_id, bad_review, customer_id) all zero nulls
- [Phase 02-03]: olist_gold.parquet frozen contract: 97456 rows x 38 cols, bad_review=13.9%, scale_pos_weight=6.2, distance max=8677 km confirmed in km
- [Phase 02-03]: Smoke test distance threshold = 10000 km (not 6000) — Olist geo border prefixes produce up to 8677 km, already decided in Phase 02-02
- [Phase 03-eda-ato-1]: payment_value usado como denominador para frete_pct_pedido — price ausente na gold table
- [Phase 03-eda-ato-1]: review_score e float64 na gold (cast defensivo para int obrigatorio antes de boxplot)
- [Phase 03-eda-ato-1]: EDA-04 kaleido indisponivel — seaborn fallback usado; resultado identico em qualidade
- [Phase 03-eda-ato-1]: GeoJSON campo sigla='sigla' detectado via auto-probe; Timestamp columns removidas antes de folium __geo_interface__; kaleido/Chrome indisponivel no ambiente Windows — fallback geopandas usado para PNG choropleth; atraso medio negativo (-11.9 dias) em todos os corredores — prazo estimado conservador
- [Phase 04-ml-ato-2]: SimpleImputer(median/most_frequent) added to ColumnTransformer sub-pipelines — gold enrichment introduced 3-4 NaN rows that LogisticRegression cannot handle natively
- [Phase 04-ml-ato-2]: Gold table enriched with 5 missing PRE_DELIVERY_FEATURES: price, estimated_delivery_days, order_item_count, payment_type, payment_installments — Phase 2 omitted these from parquet
- [Phase 04-ml-ato-2]: Baseline PR-AUC=0.2207, Recall(bad_review)=0.53 — floor metric; XGBoost must beat this in Plan 04-02
- [Phase 04-ml-ato-2]: XGBoost PR-AUC=0.2283 > baseline 0.2207 — confirmed superior before Ato 2 presentation; scale_pos_weight=6.18 from y_train
- [Phase 04-ml-ato-2]: Top SHAP features: order_item_count (0.188), customer_state_RJ (0.101), seller_customer_distance_km (0.098) — pre-delivery risk drivers
- [Phase 04-ml-ato-2]: SHAP capped at 5000 sample of 19492 test rows for performance; TreeExplainer used (not generic shap.Explainer)
- [Phase 04-ml-ato-2]: Threshold=0.785 at Precision=0.40; Recall=0.02 triggers AVISO (not halt) per plan spec; operational estimate: 8 flagged/week, 40% real risk
- [Phase 04-ml-ato-2]: Seller table: 1247 eligible sellers (>=10 orders), top-20 by mean risk score; seller_id loaded as auxiliary join key outside PRE_DELIVERY_FEATURES
- [Phase 04-ml-ato-2]: Recall=0.02 aceito como limitacao operacional — modelo opera em modo alta precisao (40%); docs/ml_limitations.md criado como referencia para Phase 5
- [Phase 05-01]: FASE3-P3-eda.ipynb era placeholder de 2 celulas — reconstruido com 5 secoes EDA completas documentadas com decisao 'Por que'
- [Phase 05-01]: FASE4 usava "../" relative paths — substituidos por PROJECT_ROOT / pathlib para portabilidade
- [Phase 05-01]: Metricas finais documentadas em Markdown (nao output): PR-AUC baseline=0.2207, XGBoost=0.2283, threshold=0.785, 8 pedidos/semana flagrados
- [Phase 05-02]: Recall=0.02 documentado como limitacao operacional conhecida (nao escondido) — modelo opera em modo de alta precisao cirurgica
- [Phase 05-02]: README instrucoes de reproducao atualizadas com nomes reais dos notebooks (FASE2-P1-data-foundation, FASE3-P3-eda, FASE4-P4-ml-pipeline)
- [Phase 05-02]: Section 5 (Recomendacoes) escrita em linguagem de negocio — sem jargao ML

### Pending Todos

None yet.

### Blockers/Concerns

- [Phase 1 RESOLVIDO]: bad_review = 13.9% confirmado em Phase 2; scale_pos_weight XGBoost = 6.21
- [Phase 2 RESOLVIDO]: Haversine validado em km (max=8677 km, mediana SP->AM=2693 km); threshold ajustado para 10000 km por outliers de CEPs de fronteira
- [Phase 4 RESOLVIDO]: SHAP TreeExplainer em amostra de 5000 completou sem timeout — beeswarm estavel
- [Phase 6]: Se Phase 4 nao fechar ate Day 5, demo Streamlit e cortada; slides sao o entregavel nao-negociavel

## Session Continuity

Last session: 2026-03-02
Stopped at: Completed 05-02-PLAN.md — docs/report.md (2183 palavras, 7 secoes) e README atualizado com secao Resultados — commits fca5820, 01bde21
Resume file: None
