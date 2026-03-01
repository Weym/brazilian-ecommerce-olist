---
phase: 04-ml-ato-2
plan: "01"
subsystem: ml
tags: [sklearn, logistic-regression, joblib, pipeline, column-transformer, imputer, anti-leakage]

requires:
  - phase: 02-data-foundation
    provides: olist_gold.parquet (97456 rows x 38 cols, bad_review=13.9%)
  - phase: 01-kickoff-e-contratos
    provides: src/features.py with PRE_DELIVERY_FEATURES (13 cols), FORBIDDEN_FEATURES, TARGET_COLUMN

provides:
  - notebooks/FASE4-P4-ml-pipeline.ipynb with sections 1-2 fully executed (sections 3-7 placeholder)
  - models/baseline_logreg.joblib — sklearn Pipeline (ColumnTransformer + LogisticRegression) serialized
  - data/gold/olist_gold.parquet enriched with 5 missing PRE_DELIVERY_FEATURES

affects:
  - 04-02-PLAN (XGBoost section uses X_train/X_test splits and NUMERIC/CATEGORICAL_FEATURES defined here)
  - 04-03-PLAN (threshold + seller table reuse baseline_pipeline)
  - 05-narrativa-e-slides (Baseline PR-AUC=0.2207 is the floor metric for slide narrative)
  - 06-demo-streamlit (loads models/baseline_logreg.joblib for predictions)

tech-stack:
  added:
    - sklearn.impute.SimpleImputer (median for numeric, most_frequent for categorical)
    - sklearn.compose.ColumnTransformer
    - sklearn.pipeline.Pipeline
    - sklearn.linear_model.LogisticRegression
    - joblib (serialize/load pipeline)
  patterns:
    - Pipeline-first imputation: SimpleImputer inside sub-Pipeline inside ColumnTransformer — no manual preprocessing outside the pipeline
    - Anti-leakage assert at notebook start — fails fast if FORBIDDEN_FEATURES bleed into PRE_DELIVERY_FEATURES
    - eval_model() helper function for consistent PR-AUC + classification_report reporting

key-files:
  created:
    - notebooks/FASE4-P4-ml-pipeline.ipynb
    - models/baseline_logreg.joblib
    - scripts/enrich_gold_features.py
    - scripts/train_baseline.py
    - scripts/verify_04_01.py
  modified:
    - data/gold/olist_gold.parquet (added 5 missing features: price, estimated_delivery_days, order_item_count, payment_type, payment_installments)

key-decisions:
  - "SimpleImputer(median) for numeric and SimpleImputer(most_frequent) for categorical — added as sub-pipelines inside ColumnTransformer to handle 3 null rows introduced by left-join enrichment"
  - "Gold table enriched in-place: price=sum(items.price), order_item_count=count(items), payment_type=mode, payment_installments=sum — Phase 2 notebook omitted these 5 features declared in Phase 1 contract"
  - "estimated_delivery_days created as copy of estimated_days (same semantics, different name) to satisfy Phase 1 contract without breaking Phase 2 outputs"
  - "class_weight=balanced locked per CONTEXT.md decision — no SMOTE"
  - "Baseline PR-AUC=0.2207, Recall(bad_review)=0.53 — floor metric; XGBoost must beat this in Plan 04-02"

patterns-established:
  - "Anti-leakage: always assert not [c for c in FORBIDDEN_FEATURES if c in PRE_DELIVERY_FEATURES] before building X"
  - "eval_model(pipeline, X_test, y_test, name) -> float: standard reporting function returning PR-AUC"
  - "Pipeline with imputer sub-pipelines: numeric_transformer = Pipeline([imputer, scaler]), categorical_transformer = Pipeline([imputer, encoder])"

requirements-completed: [ML-01, ML-02]

duration: 18min
completed: 2026-03-01
---

# Phase 4 Plan 01: Baseline LogReg Pipeline Summary

**Sklearn Pipeline (ColumnTransformer + SimpleImputer + LogisticRegression with class_weight=balanced) trained on 13 pre-delivery features, PR-AUC=0.2207, serialized to models/baseline_logreg.joblib**

## Performance

- **Duration:** 18 min
- **Started:** 2026-03-01T22:52:41Z
- **Completed:** 2026-03-01T23:10:00Z
- **Tasks:** 2
- **Files modified:** 6

## Accomplishments

- notebook FASE4-P4-ml-pipeline.ipynb created with 7 section headers; Sections 1 (load + anti-leakage + feature matrix + 80/20 stratified split) and 2 (baseline LogReg + eval + serialize) fully executed
- Gold table enriched with 5 missing PRE_DELIVERY_FEATURES (price, estimated_delivery_days, order_item_count, payment_type, payment_installments) — 97456 rows x 43 cols after enrichment
- Baseline pipeline: PR-AUC=0.2207, Recall(bad_review)=0.53 at default threshold — establishes floor for XGBoost comparison in Plan 04-02

## Task Commits

Each task was committed atomically:

1. **Task 1: Secao 1 — Load, anti-leakage e feature matrix** - `8132a98` (feat)
2. **Task 2: Secao 2 — Baseline LogReg + serializacao + enrichment gold** - `4c29835` (feat)

**Plan metadata:** (docs commit — created below)

## Files Created/Modified

- `notebooks/FASE4-P4-ml-pipeline.ipynb` — Full notebook with 7 section structure; Sections 1-2 implemented
- `models/baseline_logreg.joblib` — sklearn Pipeline (8.1 KB): ColumnTransformer (imputer+scaler/encoder) + LogisticRegression(class_weight=balanced)
- `data/gold/olist_gold.parquet` — Enriched with 5 missing PRE_DELIVERY_FEATURES from raw CSVs
- `scripts/enrich_gold_features.py` — Joins price, order_item_count, payment_type, payment_installments from raw CSVs; derives estimated_delivery_days from estimated_days
- `scripts/train_baseline.py` — CLI replica of notebook Sections 1-2 for verification

## Decisions Made

- `SimpleImputer` added to pipeline for both numeric (median) and categorical (most_frequent) features — 3 nulls in price/order_item_count and 1 null in payment_type/installments from left-join enrichment
- Gold table enriched in-place rather than rebuilding from scratch — Phase 2 parquet is the frozen contract; new columns added via join, original columns unchanged
- `estimated_delivery_days` created as alias of existing `estimated_days` column — same computation, satisfies Phase 1 contract name

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Gold table missing 5 of 13 declared PRE_DELIVERY_FEATURES**
- **Found during:** Task 2 (Secao 2 — Baseline LogReg)
- **Issue:** Phase 2 notebook built gold table without price, estimated_delivery_days (only estimated_days), order_item_count, payment_type, payment_installments — all 5 declared in src/features.py PRE_DELIVERY_FEATURES contract
- **Fix:** Created scripts/enrich_gold_features.py that joins items_agg (price=sum(price), order_item_count=count) and payments_agg (payment_type=mode, payment_installments=sum) from raw CSVs, and creates estimated_delivery_days from existing estimated_days; overwrites gold parquet
- **Files modified:** data/gold/olist_gold.parquet, scripts/enrich_gold_features.py
- **Verification:** All 13 PRE_DELIVERY_FEATURES present; 97456 rows unchanged; 3 nulls in price/order_item_count, 1 null in payment_type/installments (0.003%) — handled by imputers
- **Committed in:** 4c29835 (Task 2 commit)

**2. [Rule 2 - Missing Critical] Added SimpleImputer to ColumnTransformer sub-pipelines**
- **Found during:** Task 2 (Secao 2 — Baseline LogReg)
- **Issue:** LogisticRegression raised ValueError: "Input X contains NaN" — 3-4 rows with nulls from left-join enrichment; StandardScaler/OneHotEncoder do not handle NaN natively
- **Fix:** Wrapped StandardScaler in Pipeline([SimpleImputer(median), StandardScaler()]) for numeric; wrapped OneHotEncoder in Pipeline([SimpleImputer(most_frequent), OneHotEncoder()]) for categorical
- **Files modified:** notebooks/FASE4-P4-ml-pipeline.ipynb, scripts/train_baseline.py
- **Verification:** Model trains and predicts without NaN errors; round-trip OK
- **Committed in:** 4c29835 (Task 2 commit)

---

**Total deviations:** 2 auto-fixed (1 Rule 1 bug, 1 Rule 2 missing critical)
**Impact on plan:** Both fixes essential for correctness. Gold enrichment adds necessary features declared in Phase 1 contract. Imputer is standard ML pipeline practice for robustness. No scope creep.

## Issues Encountered

- Gold table was built in Phase 2 without `payment_type`, `payment_installments`, `order_item_count`, `price`, and `estimated_delivery_days` (only `estimated_days` was stored) — Phase 1 contract declared these features but Phase 2 implementation was incomplete. Fixed by enrichment script.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 04-02 (XGBoost + SHAP) can begin: X_train/X_test defined, NUMERIC_FEATURES/CATEGORICAL_FEATURES established, eval_model() helper ready
- Gold table now has all 13 PRE_DELIVERY_FEATURES — both LogReg baseline and XGBoost use same feature matrix
- Baseline PR-AUC=0.2207 is the floor — XGBoost must beat this; if not, baseline is the production model

---
*Phase: 04-ml-ato-2*
*Completed: 2026-03-01*

## Self-Check: PASSED

All files verified present:
- notebooks/FASE4-P4-ml-pipeline.ipynb: FOUND
- models/baseline_logreg.joblib: FOUND
- data/gold/olist_gold.parquet: FOUND
- scripts/enrich_gold_features.py: FOUND
- scripts/train_baseline.py: FOUND
- .planning/phases/04-ml-ato-2/04-01-SUMMARY.md: FOUND

Commits verified:
- 8132a98: feat(04-01) Task 1 — Secao 1
- 4c29835: feat(04-01) Task 2 — Secao 2 + enrichment
