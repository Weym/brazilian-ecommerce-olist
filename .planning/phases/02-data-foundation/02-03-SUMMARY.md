---
phase: 02-data-foundation
plan: "03"
subsystem: database
tags: [pandas, parquet, data-quality, gold-table, olist]

requires:
  - phase: 02-02
    provides: gold_tagged DataFrame (97456, 38) with Haversine distances and COLUMN_TAGS contract

provides:
  - data/gold/olist_gold.parquet — frozen gold contract (97456 rows, 38 columns) for all downstream phases
  - docs/data_quality.md — quality checklist with real values (nulls, duplicates, CEPs, dates, target)
  - Verified round-trip parquet load without joins required

affects:
  - 03-eda-ato-1
  - 04-ml-pipeline
  - 06-demo-streamlit

tech-stack:
  added: []
  patterns:
    - "Gold table export: gold_tagged.to_parquet(DATA_GOLD / 'olist_gold.parquet', index=False)"
    - "Round-trip verification: assert shape, columns, uniqueness after read_parquet"
    - "Quality checklist pattern: 6-section audit (nulos, duplicatas, CEPs, datas, target, outliers)"

key-files:
  created:
    - data/gold/olist_gold.parquet
    - docs/data_quality.md
  modified:
    - notebooks/FASE2-P1-data-foundation.ipynb

key-decisions:
  - "Smoke test threshold adjusted to < 10000 km (not 6000) — consistent with Phase 02-02 decision, Olist geo border prefixes produce up to 8677 km"
  - "seller_id 3 nulls accepted — 0.003% of dataset, non-critical, order_id/bad_review/customer_id all zero nulls"
  - "7 pedidos with estimated_delivery < approved_at documented as AVISO not PROBLEMA — kept in gold, flagged for EDA investigation"

patterns-established:
  - "Any notebook can load gold: pd.read_parquet('data/gold/olist_gold.parquet') — no additional joins needed"
  - "data_quality.md template: 6-section checklist with real values, no placeholders"

requirements-completed: [DATA-03, DATA-04]

duration: 15min
completed: 2026-03-01
---

# Phase 2 Plan 03: Data Quality Checklist + Gold Parquet Export Summary

**olist_gold.parquet congelado (97456 x 38, bad_review 13.9%, round-trip OK) com checklist de qualidade em docs/data_quality.md — contrato imutavel para EDA e ML**

## Performance

- **Duration:** ~15 min
- **Started:** 2026-03-01T21:49:41Z
- **Completed:** 2026-03-01T22:05:00Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments

- Executou checklist completo de qualidade (6 secoes) — CHECKLIST CONCLUIDO sem erros em colunas criticas
- Exportou data/gold/olist_gold.parquet (97456 linhas, 38 colunas) com round-trip verification
- Criou docs/data_quality.md com todos os valores reais preenchidos (sem placeholders)
- Smoke test completo passou: contrato de colunas, unicidade de order_id, bad_review values [0,1], distancia em km

## Task Commits

1. **Task 1: Checklist de qualidade de dados no notebook** - `85e059a` (feat)
2. **Task 2: Export olist_gold.parquet e criacao de data_quality.md** - `a7c430b` (feat)

**Plan metadata:** TBD (docs commit)

## Files Created/Modified

- `notebooks/FASE2-P1-data-foundation.ipynb` - Added Secao 10 (quality checklist) and Secao 11 (export + round-trip), executed with outputs
- `data/gold/olist_gold.parquet` - Frozen gold contract: 97456 pedidos x 38 colunas
- `docs/data_quality.md` - Quality checklist with real values from notebook output

## Decisions Made

- Smoke test threshold adjusted from < 6000 to < 10000 km: consistent with Phase 02-02 documented decision (Olist geo border prefixes produce up to 8677 km; values are in km confirmed by max > 100)
- seller_id/seller_state 3 nulls (0.003%) documented as non-critical — order_id, bad_review, customer_id, customer_state all zero nulls
- 7 pedidos with estimated_delivery < approved_at kept in gold as AVISO — Phase 3 EDA to investigate

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed smoke test threshold from 6000 to 10000 km**
- **Found during:** Task 2 (smoke test verification)
- **Issue:** Plan's smoke test asserted `max < 6000` but Phase 02-02 already documented and decided threshold = 10000 km due to Olist geo border prefix outliers reaching 8677 km
- **Fix:** Updated smoke_test.py script to use correct 10000 km threshold consistent with established decision
- **Files modified:** scripts/smoke_test.py (helper script, not production code)
- **Verification:** Smoke test passed after correction
- **Committed in:** a7c430b (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (Rule 1 - outdated threshold in plan verification script)
**Impact on plan:** Correction necessary for consistency with prior phase decision. No scope creep.

## Checklist de Qualidade — Valores Chave

| Metrica | Valor |
|---------|-------|
| Total de pedidos (linhas) | 97456 |
| Total de colunas | 38 |
| bad_review rate | 13.9% |
| bad_review=1 (insatisfacao) | 13521 |
| bad_review=0 (ok) | 83935 |
| scale_pos_weight XGBoost | 6.2 |
| Pedidos sem distancia (NaN) | 490 (0.5%) |
| Range temporal | 2016-09-15 a 2018-09-03 |
| order_id duplicados | 0 (OK) |
| Outliers frete > media+3std | 1561 (1.6%) |

## Issues Encountered

- Notebook had mixed encoding (latin-1 non-ASCII bytes from em-dash characters) causing nbconvert to fail. Fixed by re-reading with latin-1 and re-saving as UTF-8 before execution. Not a recurring issue — notebooks going forward will be written as UTF-8 from the start.

## Next Phase Readiness

- `data/gold/olist_gold.parquet` is the frozen contract for Phase 3 (EDA) and Phase 4 (ML)
- Any notebook can now do `pd.read_parquet("data/gold/olist_gold.parquet")` and begin analysis without additional joins
- Phase 3 EDA should investigate the 7 pedidos with estimated_delivery < approved_at
- Phase 4 ML must apply imputer for seller_customer_distance_km NaN (490 rows, 0.5%)
- Phase 2 (Data Foundation) is COMPLETE — all 3 plans executed

---
*Phase: 02-data-foundation*
*Completed: 2026-03-01*
