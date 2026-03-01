---
phase: 01-kickoff-e-contratos
plan: 02
subsystem: feature-contract
tags: [python, features, data-contract, leakage-prevention, olist]

# Dependency graph
requires:
  - phase: 01-kickoff-e-contratos/01-01
    provides: repository scaffold — src/ and docs/ directories with .gitkeep placeholders
provides:
  - src/__init__.py makes src/ importable as Python package
  - src/features.py exports PRE_DELIVERY_FEATURES (13 columns), FORBIDDEN_FEATURES (6 columns), TARGET_COLUMN='bad_review'
  - docs/feature_contract.md human-readable table of all columns with pre/pos-entrega/target tags
  - Zero-leakage contract: no forbidden column in PRE_DELIVERY_FEATURES
affects:
  - 02-data-foundation (gold table uses PRE_DELIVERY_FEATURES as column filter)
  - 03-eda-ato-1 (EDA respects feature contract)
  - 04-ml-pipeline (FASE4-P4-ml-pipeline.ipynb imports PRE_DELIVERY_FEATURES)
  - 06-demo-streamlit (app/pages/03_modelo.py imports PRE_DELIVERY_FEATURES)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Feature contract as Python constants: PRE_DELIVERY_FEATURES, FORBIDDEN_FEATURES, TARGET_COLUMN in src/features.py"
    - "TDD for contract validation: tests written before implementation, all 6 pass"
    - "Dual-format contract: Python (machine) + Markdown (human), kept in sync"

key-files:
  created:
    - src/__init__.py
    - src/features.py
    - docs/feature_contract.md
    - tests/test_features.py
  modified: []

key-decisions:
  - "PRE_DELIVERY_FEATURES has exactly 13 columns — freight/price, estimated days, geography, product dims, order counts/payment"
  - "Temporal anchor is order_approved_at (not order_purchase_timestamp) — blocked decision from CONTEXT.md"
  - "seller_customer_distance_km declared now as Phase 2 contract even though computed in Phase 2"
  - "FORBIDDEN_FEATURES includes 6 columns: 5 mandatory + order_delivered_carrier_date (unreliable)"
  - "TARGET_COLUMN = 'bad_review': review_score in {1,2} -> 1, else 0"

patterns-established:
  - "Import pattern: from src.features import PRE_DELIVERY_FEATURES (no sys.path hacks)"
  - "Dual-format contract: any change to src/features.py must sync to docs/feature_contract.md"

requirements-completed: [KICK-01, KICK-04]

# Metrics
duration: 3min
completed: 2026-03-01
---

# Phase 1 Plan 02: Feature Contract Summary

**Python feature contract with 13 pre-delivery columns and 6 forbidden post-delivery columns, enforced via importable constants in src/features.py and documented in docs/feature_contract.md**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-01T21:11:11Z
- **Completed:** 2026-03-01T21:14:06Z
- **Tasks:** 2 (+ TDD red commit)
- **Files modified:** 4

## Accomplishments

- src/features.py exports three constants (PRE_DELIVERY_FEATURES, FORBIDDEN_FEATURES, TARGET_COLUMN) with temporal anchor order_approved_at in module docstring
- src/__init__.py makes src/ importable — `from src.features import PRE_DELIVERY_FEATURES` works from project root
- docs/feature_contract.md provides human-readable table of all 21 columns tagged [pre-entrega], [pos-entrega], [target], [join-key], [temporal-anchor]
- All 6 TDD tests pass confirming zero leakage between forbidden and allowed columns

## Task Commits

Each task was committed atomically:

1. **TDD RED — test_features.py** - `d0ccf39` (test)
2. **Task 1: src/__init__.py + src/features.py** - `dc08d2f` (feat)
3. **Task 2: docs/feature_contract.md** - `dbe0b1e` (feat)

_Note: TDD task has two commits — test (RED) then implementation (GREEN)._

## Files Created/Modified

- `src/__init__.py` — Makes src/ a Python package; enables clean imports
- `src/features.py` — PRE_DELIVERY_FEATURES (13), FORBIDDEN_FEATURES (6), TARGET_COLUMN with full docstring
- `docs/feature_contract.md` — Human-readable column table, sync instructions, summary tag table
- `tests/test_features.py` — 6 TDD tests covering import, column counts, forbidden, target, leakage, Phase 2 contract

## Decisions Made

- Temporal anchor is `order_approved_at` throughout (blocked decision from CONTEXT.md — not `order_purchase_timestamp`)
- `seller_customer_distance_km` declared in PRE_DELIVERY_FEATURES now as a Phase 2 contract, with explicit comment noting it is computed in Phase 2
- `order_delivered_carrier_date` added to FORBIDDEN_FEATURES (partially post-approval, unreliable)
- TDD pattern applied to contract validation — tests enforced spec before implementation

## Deviations from Plan

None — plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- `from src.features import PRE_DELIVERY_FEATURES` ready for all notebooks and app pages
- docs/feature_contract.md ready to share with team
- Phase 2 (Data Foundation) can use PRE_DELIVERY_FEATURES as column filter for gold table construction

---

*Phase: 01-kickoff-e-contratos*
*Completed: 2026-03-01*

## Self-Check: PASSED

- FOUND: src/__init__.py
- FOUND: src/features.py
- FOUND: docs/feature_contract.md
- FOUND: tests/test_features.py
- FOUND commit d0ccf39 (test RED)
- FOUND commit dc08d2f (feat GREEN)
- FOUND commit dbe0b1e (feat Task 2)
- 6/6 tests pass
