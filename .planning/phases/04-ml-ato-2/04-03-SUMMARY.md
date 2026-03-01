---
phase: 04-ml-ato-2
plan: 03
subsystem: ml
tags: [precision-recall, threshold-selection, operational-estimate, seller-risk-table, joblib, round-trip, pr-curve]

# Dependency graph
requires:
  - phase: 04-ml-ato-2/04-02
    provides: final_pipeline (XGBoost PR-AUC=0.2283), models/final_pipeline.joblib, models/baseline_logreg.joblib, reports/figures/shap_beeswarm.png
provides:
  - chosen_threshold=0.785 at Precision=0.40 (primary criterion met)
  - reports/figures/pr_curve.png — PR curve with threshold marked in red (53KB, 150 dpi)
  - seller_table — top-20 sellers by mean risk score (filter: total_pedidos>=10)
  - Section 7 round-trip verification — both joblib pass predict_proba check
  - notebooks/FASE4-P4-ml-pipeline.ipynb — complete 7-section notebook
affects: [app/pages/03_modelo.py, slides Ato 2, phase-05-slides, phase-06-streamlit]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Threshold selection: first index where precision[:-1] >= 0.40 (primary criterion LOCKED per CONTEXT.md)"
    - "Operational estimate: flagged_total / 104 weeks = flagged_per_week (Olist dataset ~2 years)"
    - "Seller table: groupby seller_id, agg mean risk_score + count + sum(>threshold), filter >=10 orders, top-20"
    - "seller_id excluded from PRE_DELIVERY_FEATURES — loaded as auxiliary join key via df[PRE_DELIVERY_FEATURES + ['seller_id', TARGET_COLUMN]]"

key-files:
  created:
    - reports/figures/pr_curve.png
    - scripts/verify_04_03_task1.py
    - scripts/verify_04_03_task2.py
    - scripts/verify_04_03_final.py
  modified:
    - notebooks/FASE4-P4-ml-pipeline.ipynb

key-decisions:
  - "Threshold=0.785 selected at first Precision>=0.40 point — Recall=0.02 triggers AVISO but does not halt execution (criterion secondary per CONTEXT.md)"
  - "Recall below 0.60 noted as operational limitation: 8 flagged orders/week out of 97456 total (0.8% flagged rate)"
  - "Seller table uses 1247 eligible sellers (total_pedidos>=10); top-20 shown for presentation fit"
  - "Operational narrative confirmed: 40% of flagged orders are real risk (precision at chosen threshold)"

patterns-established:
  - "Threshold fallback: if Precision>=0.40 not achievable, use max Recall with Precision>=0.25 — never silently fail"
  - "Seller scoring: predict_proba on full dataset (not just test set) for operational volume estimates"

requirements-completed: [ML-05, ML-06, ML-07]

# Metrics
duration: ~10min
completed: 2026-03-01
---

# Phase 4 Plan 03: Threshold Tuning, Seller Table, and Joblib Verification Summary

**PR threshold=0.785 at Precision=0.40 with seller risk table (top-20, >=10 orders) and round-trip verification of both sklearn Pipelines — completes FASE4-P4-ml-pipeline.ipynb with 7 sections**

## Performance

- **Duration:** ~10 min
- **Started:** 2026-03-01T23:05:00Z (estimated)
- **Completed:** 2026-03-01T23:13:21Z
- **Tasks:** 2 of 2
- **Files modified:** 2 (notebook + new pr_curve.png)

## Accomplishments

- Added Section 5: precision_recall_curve, threshold selection at Precision>=0.40 (chosen=0.785), operational estimate (8 flagged orders/week, 40% real risk), pr_curve.png saved at 150 dpi
- Added Section 6: seller risk table aggregation via groupby seller_id, filter total_pedidos>=10 (1247 eligible), top-20 by score_medio_risco descending
- Added Section 7: artifact existence check (4 files), round-trip predict_proba on both pipelines, named_steps assertion for Streamlit compatibility, full summary printout
- Integrated verification passes: zero leakage, both joblib carregaveis, both PNGs >10KB

## Task Commits

Each task was committed atomically:

1. **Task 1: Secoes 5 e 6 — Threshold operacional e tabela de vendedores** - `4d00ef3` (feat)
2. **Task 2: Secao 7 — Verificacao final e round-trip dos joblib** - `973c14f` (feat)

## Files Created/Modified

- `notebooks/FASE4-P4-ml-pipeline.ipynb` — Sections 5 (3 cells), 6 (1 cell), 7 (3 cells) added; all 7 sections executed end-to-end without error
- `reports/figures/pr_curve.png` — PR curve with XGBoost line + red dot at chosen threshold + Precision=0.40 dashed line (53KB, 150 dpi)
- `scripts/verify_04_03_task1.py` — Static notebook checks for sections 5+6
- `scripts/verify_04_03_task2.py` — Joblib round-trip + artifact existence checks
- `scripts/verify_04_03_final.py` — Integrated Fase 4 verification

## Decisions Made

- Threshold 0.785 selected at first `precision[:-1] >= 0.40` index — satisfies primary criterion from CONTEXT.md
- Recall at chosen threshold = 0.02 (below secondary criterion of 0.60) — AVISO printed, execution continues per plan spec ("alerta se nao atingido, mas nao para execucao")
- Operational estimate uses full dataset (97456 orders / 104 weeks) — gives slide-ready narrative: "40% dos pedidos flagrados sao de fato risco real"
- Seller table covers 1247 eligible sellers (out of ~3000 total); top-20 shown for presentation fit

## Deviations from Plan

None - plan executed exactly as written. The Recall below 0.60 is a model characteristic, not a code deviation — the fallback logic was pre-specified in the plan and AVISO is correctly triggered.

## Issues Encountered

- Recall at Precision=0.40 is 0.02 (model reaches high precision only at very high probability threshold). This is expected given XGBoost PR-AUC=0.2283 on a 13.9% positive class — the model is not strong enough to simultaneously achieve Precision=0.40 AND Recall=0.60. The operational estimate (8 flagged/week, 40% real risk) is honest and slide-ready.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- notebooks/FASE4-P4-ml-pipeline.ipynb complete (7 sections, all verified)
- models/final_pipeline.joblib (485KB) ready for Phase 6 Streamlit — preprocessor + classifier confirmed in named_steps
- models/baseline_logreg.joblib (8KB) ready for comparison in Streamlit
- reports/figures/pr_curve.png ready for Ato 2 slides
- reports/figures/shap_beeswarm.png ready for Ato 2 slides
- Phase 4 fully complete — all ML-05, ML-06, ML-07 requirements satisfied

---
*Phase: 04-ml-ato-2*
*Completed: 2026-03-01*

## Self-Check: PASSED

- FOUND: notebooks/FASE4-P4-ml-pipeline.ipynb (30 cells, 7 sections)
- FOUND: reports/figures/pr_curve.png (53KB)
- FOUND: models/baseline_logreg.joblib (8KB)
- FOUND: models/final_pipeline.joblib (485KB)
- FOUND: reports/figures/shap_beeswarm.png (131KB)
- FOUND: commit 4d00ef3 (Task 1)
- FOUND: commit 973c14f (Task 2)
- All integrated verification checks pass (verify_04_03_final.py)
