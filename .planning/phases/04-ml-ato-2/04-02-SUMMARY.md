---
phase: 04-ml-ato-2
plan: 02
subsystem: ml
tags: [xgboost, shap, sklearn-pipeline, joblib, beeswarm, scale_pos_weight, PR-AUC]

# Dependency graph
requires:
  - phase: 04-ml-ato-2/04-01
    provides: baseline_pipeline (LogReg PR-AUC=0.2207), preprocessor ColumnTransformer fitted on X_train, eval_model helper
provides:
  - XGBoost Pipeline (preprocessor + XGBClassifier) trained with scale_pos_weight from y_train
  - models/final_pipeline.joblib — complete sklearn Pipeline serialized for Streamlit
  - reports/figures/shap_beeswarm.png — beeswarm top-15 SHAP features at 150 dpi (131 KB)
  - PR-AUC improvement: 0.2207 (baseline) -> 0.2283 (XGBoost), +0.0076
affects: [04-03, app/pages/03_modelo.py, slides Ato 2]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "XGBoost scale_pos_weight always from y_train (never from full y) to avoid hyperparameter leakage"
    - "SHAP TreeExplainer on extracted named_steps['classifier'], X_test_transformed (not raw DataFrame)"
    - "SHAP beeswarm: sample to min(5000, len), show=False + plt.savefig + plt.close for headless environments"
    - "Pipeline reuses same preprocessor object from baseline — sklearn Pipeline.fit() refits it correctly"

key-files:
  created:
    - models/final_pipeline.joblib
    - reports/figures/shap_beeswarm.png
  modified:
    - notebooks/FASE4-P4-ml-pipeline.ipynb

key-decisions:
  - "XGBoost PR-AUC=0.2283 beats baseline 0.2207 — model confirmed superior before Ato 2 presentation"
  - "scale_pos_weight=6.18 computed from y_train neg/pos — matches Phase 02-02 documented estimate of 6.21"
  - "SHAP on 5000 sample of 19492 test rows — sufficient for stable beeswarm (pattern converges >2k samples)"
  - "Top SHAP feature: order_item_count (mean|SHAP|=0.188), followed by customer_state_RJ and seller_customer_distance_km"
  - "use_label_encoder comment removed from notebook code — comment text triggered static check; parameter already absent from XGBClassifier call"

patterns-established:
  - "Headless SHAP: always TreeExplainer + show=False + plt.close() to avoid display errors on Windows/server"
  - "Final pipeline = full sklearn Pipeline (preprocessor + classifier), never just the estimator alone"

requirements-completed: [ML-03, ML-04]

# Metrics
duration: 6min
completed: 2026-03-01
---

# Phase 4 Plan 02: XGBoost + SHAP Beeswarm Summary

**XGBoost Pipeline (PR-AUC 0.2283) with SHAP TreeExplainer beeswarm (top-15 features, 150 dpi) confirming order_item_count as primary pre-delivery risk factor**

## Performance

- **Duration:** ~6 min
- **Started:** 2026-03-01T23:02:37Z
- **Completed:** 2026-03-01T23:08:00Z
- **Tasks:** 2 of 2
- **Files modified:** 3

## Accomplishments

- Trained XGBoost Pipeline with scale_pos_weight=6.18 (from y_train, no leakage) — PR-AUC 0.2283 vs baseline 0.2207 (+0.0076, assert passes)
- Serialized complete sklearn Pipeline (preprocessor + XGBClassifier) to models/final_pipeline.joblib with round-trip verification
- Generated SHAP beeswarm PNG (131 KB, 150 dpi, max_display=15) via TreeExplainer on 5000-sample transformed test set
- Top SHAP features reveal: order_item_count (0.188), customer_state_RJ (0.101), seller_customer_distance_km (0.098)

## Task Commits

Each task was committed atomically:

1. **Task 1: Secao 3 — XGBoost com scale_pos_weight** - `5ff90d2` (feat)
2. **Task 2: Secao 4 — SHAP TreeExplainer e beeswarm PNG** - `b8d4e05` (feat)

## Files Created/Modified

- `notebooks/FASE4-P4-ml-pipeline.ipynb` — Sections 3 (XGBoost, 3 cells) and 4 (SHAP, 4 cells) added
- `models/final_pipeline.joblib` — Complete sklearn Pipeline (497 KB), loadable via joblib.load for Streamlit
- `reports/figures/shap_beeswarm.png` — Beeswarm chart top-15 features at 150 dpi (131 KB)

## Decisions Made

- scale_pos_weight computed from y_train only (neg=62,368 / pos=10,088 = 6.18) — consistent with Phase 02-02 estimate of 6.21
- SHAP sample capped at 5000 (from 19,492 test rows) — headless performance; beeswarm stable above 2k samples
- use_label_encoder comment removed from notebook source code — comment text triggered string-match static check; parameter was never actually passed to XGBClassifier

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Removed use_label_encoder from notebook comment text**
- **Found during:** Task 1 verification
- **Issue:** Static check `assert 'use_label_encoder' not in src` matched against comment text "NOTA: nao incluir use_label_encoder" — the parameter was never actually set but the comment triggered the assertion
- **Fix:** Removed the comment line from cell 3.1; XGBClassifier call was already correct without the parameter
- **Files modified:** notebooks/FASE4-P4-ml-pipeline.ipynb
- **Verification:** `python scripts/verify_04_02.py` passes all checks
- **Committed in:** 5ff90d2 (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (Rule 1 — comment text triggering static assertion)
**Impact on plan:** Trivial — no behavioral change; XGBClassifier never had the parameter, comment removal is cosmetic.

## Issues Encountered

- nbconvert output path: `--output notebooks/FASE4-P4-ml-pipeline.ipynb` caused double `notebooks/notebooks/` prefix — fixed by using absolute output path
- Both issues resolved without scope creep

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- models/final_pipeline.joblib ready for Plan 04-03 (threshold tuning + seller table) and app/pages/03_modelo.py (Streamlit)
- reports/figures/shap_beeswarm.png ready for Ato 2 slides
- Notebook sections 5-7 still have placeholders — Plan 04-03 responsibility
- XGBoost model beats baseline; further tuning (threshold selection for operational precision/recall) is Plan 04-03

---
*Phase: 04-ml-ato-2*
*Completed: 2026-03-01*
