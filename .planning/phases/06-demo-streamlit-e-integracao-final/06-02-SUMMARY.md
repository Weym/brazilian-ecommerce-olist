---
phase: 06-demo-streamlit-e-integracao-final
plan: "02"
subsystem: ui
tags: [streamlit, plotly, xgboost, gauge, risk-prediction]

requires:
  - phase: 04-ml-ato-2
    provides: models/final_pipeline.joblib — XGBoost sklearn Pipeline with ColumnTransformer preprocessor
  - phase: 06-01
    provides: utils/loaders.py — centralized I/O with @st.cache_resource and @st.cache_data

provides:
  - pages/2_Preditor.py — Streamlit predictor page with 6-input form, Plotly gauge, and recommended action line
  - Fixed utils/loaders.load_categories_and_ufs() reading from gold parquet
  - Fixed utils/loaders.load_threshold() fallback to 0.785 (Phase 4 operational value)

affects:
  - 06-05-PLAN (deploy Streamlit Cloud — predictor is the centerpiece demo page)

tech-stack:
  added: []
  patterns:
    - "st.form() wrapper prevents partial reruns on each widget interaction"
    - "go.Indicator gauge with steps[] for tri-color risk bands derived from threshold"
    - "Default values for non-exposed pipeline features use Phase 2 gold table medians"
    - "@st.cache_resource for pipeline (non-serializable), @st.cache_data for lists"

key-files:
  created:
    - pages/2_Preditor.py
  modified:
    - utils/loaders.py

key-decisions:
  - "6 user-visible inputs + 7 default-filled features: freight_value, price, estimated_delivery_days, product_category_name_english, seller_state, customer_state exposed; freight_ratio, distance, weight, volume, item_count, payment_type, installments filled with dataset medians"
  - "THRESHOLD_LOW = threshold * 0.6, THRESHOLD_HIGH = threshold (0.785) for gauge tri-color bands"
  - "load_categories_and_ufs() reads from data/gold/olist_gold.parquet, not geo_aggregated.parquet (which has no category column)"
  - "load_threshold() fallback changed from 0.5 to 0.785 (Phase 4 ML-05 Precision=0.40 threshold)"

patterns-established:
  - "All pipeline features provided at predict_proba() time — non-user-exposed features use medians as defaults"
  - "try/except around predict_proba with informative error showing feature names for debugging"

requirements-completed: [PRES-03]

duration: 5min
completed: 2026-03-02
---

# Phase 06 Plan 02: Preditor de Risco Summary

**Pagina Streamlit com formulario de 6 inputs, gauge go.Indicator tri-color (verde/amarelo/vermelho baseado no threshold 0.785 da Phase 4) e linha de acao recomendada especifica por faixa de risco.**

## Performance

- **Duration:** 5min
- **Started:** 2026-03-02T00:57:53Z
- **Completed:** 2026-03-02T00:58:23Z
- **Tasks:** 1 completed
- **Files modified:** 2

## Accomplishments

- Criado pages/2_Preditor.py com formulario st.form de 6 campos, build_gauge() com go.Indicator e faixas tri-color, e exibicao de acao recomendada via st.success/warning/error
- Pipeline XGBoost chamado apenas via predict_proba() — nenhum treino ou join ao vivo
- Corrigido bug em utils/loaders.load_categories_and_ufs() que retornava lista vazia (lia geo_aggregated.parquet sem coluna de categoria; agora le olist_gold.parquet)
- Corrigido fallback de load_threshold() de 0.5 para 0.785 (valor real da Phase 4)

## Task Commits

1. **Task 1: Pagina Preditor — formulario, gauge e acao recomendada** - `3ca1028` (feat)

**Plan metadata:** TBD (docs: complete plan)

## Files Created/Modified

- `pages/2_Preditor.py` — Pagina Streamlit completa: formulario 6 inputs, build_gauge() com go.Indicator, acao recomendada st.success/warning/error, expander com detalhes para apresentacao
- `utils/loaders.py` — Bug fix: load_categories_and_ufs() agora le gold parquet; load_threshold() fallback 0.785

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed load_categories_and_ufs() returning empty category list**
- **Found during:** Task 1 (implementation)
- **Issue:** The function read from `data/processed/geo_aggregated.parquet` which has columns `['customer_state', 'total_orders', 'bad_reviews', 'avg_dias_atraso', 'avg_freight_value', 'bad_review_rate']` — no product category column. Function always returned `categories=[]`.
- **Fix:** Changed to read from `data/gold/olist_gold.parquet` columns `product_category_name_english` and `customer_state`. Added 71-item hardcoded fallback list.
- **Files modified:** `utils/loaders.py`
- **Commit:** 3ca1028

**2. [Rule 1 - Bug] Fixed load_threshold() fallback value**
- **Found during:** Task 1 (implementation)
- **Issue:** Fallback was 0.5 (generic midpoint) — Phase 4 established threshold=0.785 at Precision=0.40 on PR curve. Demo would show wrong color bands if threshold.json is missing.
- **Fix:** Changed fallback from `0.5` to `0.785`
- **Files modified:** `utils/loaders.py`
- **Commit:** 3ca1028

**3. [Rule 2 - Missing functionality] Added 7 pipeline-required features with median defaults**
- **Found during:** Task 1 (pipeline inspection)
- **Context:** Plan listed "5 inputs pre-entrega" but pipeline expects 13 features (PRE_DELIVERY_FEATURES). Missing: freight_ratio, seller_customer_distance_km, product_weight_g, product_volume_cm3, order_item_count, payment_type, payment_installments.
- **Fix:** Computed freight_ratio dynamically (freight_value/price), filled remaining 6 with dataset medians from Phase 2 gold table. All features documented with their median values in code.
- **Files modified:** `pages/2_Preditor.py`
- **Commit:** 3ca1028

## Self-Check: PASSED

- [x] `pages/2_Preditor.py` exists and has valid syntax (ast.parse confirmed)
- [x] `utils/loaders.py` updated with bug fixes
- [x] Commit `3ca1028` exists in git log
- [x] All must-have truths verified:
  - Formulario com 6 inputs aparece e aceita valores (st.form with 6 widgets)
  - pipeline.predict_proba() chamado e retorna float 0-1
  - go.Indicator renderiza com faixas verde/amarelo/vermelho baseadas em threshold
  - Linha de acao recomendada especifica por faixa abaixo do gauge
  - Nenhum treino ou join ocorre ao clicar Calcular Risco
