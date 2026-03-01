---
phase: 02-data-foundation
plan: "01"
subsystem: data
tags: [pandas, joins, geolocation, gold-table, olist]
dependency_graph:
  requires: []
  provides: [gold_with_geo DataFrame, data foundation for Phase 3 EDA and Phase 4 ML]
  affects: [notebooks/FASE3-P2-geo-analysis.ipynb, notebooks/FASE4-P4-ml-pipeline.ipynb]
tech_stack:
  added: []
  patterns: [groupby-agg pre-aggregation, left-join chain, nullable Int64 for float zip codes]
key_files:
  created: []
  modified:
    - notebooks/FASE2-P1-data-foundation.ipynb
decisions:
  - "seller/customer_zip_code_prefix floats must be cast via Int64 (nullable) before str.zfill(5) — direct astype(str) produces '9350.0' instead of '09350'"
  - "geo_agg uniqueness confirmed: 1000163 rows -> 19015 unique zip_code_prefix entries via mean lat/lon"
  - "reviews deduplicated by sort_values('review_answer_timestamp').drop_duplicates(keep='last') — 99224 -> 98673"
metrics:
  duration: 7min
  completed: "2026-03-01T21:38:00Z"
  tasks_completed: 2
  files_modified: 1
---

# Phase 02 Plan 01: Data Foundation Summary

**One-liner:** 9 CSVs loaded, geolocation pre-aggregated (1M -> 19k rows), join chain built via left-merge on orders anchor producing gold_with_geo (97456, 32) with 1 row per order_id.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Criar notebook e carregar os 9 CSVs com validacao de shapes | bacc95a | notebooks/FASE2-P1-data-foundation.ipynb |
| 2 | Adicionar join de geo lat/lon para seller e customer via CEP | bacc95a | notebooks/FASE2-P1-data-foundation.ipynb |

*Note: Both tasks were committed atomically as a single unit since they modify the same notebook and Task 2 was integrated during initial construction.*

## Key Results

### Shapes Validadas

| DataFrame | Shape | Nota |
|-----------|-------|------|
| orders | (99441, 8) | Ancora do join chain |
| items | (112650, 7) | Multi-itens por pedido |
| reviews | (99224, 7) | Algumas reviews duplicadas por order_id |
| payments | (103886, 5) | Multi-metodos por pedido |
| customers | (99441, 5) | 1:1 com orders |
| sellers | (3095, 4) | |
| products | (32951, 9) | |
| geo | (1000163, 5) | 52.6 linhas por zip_code_prefix em media |
| cat_trans | (71, 2) | Traducao EN para categorias |

### Pipeline Summary

- **geo_agg:** 1000163 -> 19015 linhas (1 por zip_code_prefix, assert uniqueness passed)
- **items_agg:** 112650 -> 98666 order_ids unicos (assert passed)
- **reviews_dedup:** 99224 -> 98673 (551 pedidos com review duplicada, kept latest)
- **gold_raw:** (99441, 28) — 1 linha por order_id (assert passed)
- **gold_filtered:** 99441 -> 97456 | Removidos: 1985 (canceled, unavailable, sem review ou sem order_approved_at)
- **gold_with_geo:** (97456, 32) — 1 linha por order_id apos joins de lat/lon (assert passed)

### Geolocation Coverage

| | Sem lat/lon | Proporcao |
|-|------------|-----------|
| Sellers | 219 | 0.2% |
| Customers | 272 | 0.3% |

Cobertura excelente: >99.7% dos pedidos tem coordenadas geograficas para ambos seller e customer.

### Colunas em gold_with_geo (32)

customer_city, customer_id, customer_lat, customer_lng, customer_state, customer_unique_id, customer_zip_code_prefix, freight_value, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date, order_id, order_purchase_timestamp, order_status, payment_value, product_category_name, product_category_name_english, product_height_cm, product_id, product_length_cm, product_photos_qty, product_weight_g, product_width_cm, review_score, seller_city, seller_id, seller_lat, seller_lng, seller_state, seller_zip_code_prefix, total_payment_value

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed float64 zip code prefix producing wrong string representation**

- **Found during:** Task 2
- **Issue:** After the left-join chain, `seller_zip_code_prefix` becomes float64 (pandas promotes int to float when NaN is introduced by left merges). Direct `.astype(str).str.zfill(5)` converts `9350.0` to `'9350.0'` (6 chars, no padding) instead of `'09350'`, causing 100% NULL match rate when joining with geo_agg.
- **Fix:** Changed conversion to `.astype('Int64').astype(str).str.zfill(5)` — pandas nullable Int64 preserves integers cleanly before string conversion, producing `'09350'` as expected.
- **Files modified:** notebooks/FASE2-P1-data-foundation.ipynb (cell-dtype-fix)
- **Commit:** bacc95a
- **Impact:** seller lat/lon coverage went from 0% to 99.8% (219 missing = 0.2%)

## Decisions Made

1. **Float zip dtype via Int64:** The plan's original `.astype(str).str.zfill(5)` pattern fails on float64 columns. Using `.astype('Int64')` as intermediate step is the correct approach for any merge chain that introduces NaN into integer columns.

2. **Project root detection:** Notebook uses `Path.cwd()` with `if NOTEBOOK_DIR.name == 'notebooks': PROJECT_ROOT = NOTEBOOK_DIR.parent` to work in both execution contexts (project root via nbconvert and notebooks/ via Jupyter UI).

3. **VALID_STATUS filter:** Chose to keep 'shipped', 'invoiced', 'processing', 'approved' in addition to 'delivered' — these are valid pre-delivery states where the model should generate alerts. Pedidos com canceled/unavailable excluidos conforme spec.

## Self-Check: PASSED

- [x] notebooks/FASE2-P1-data-foundation.ipynb exists and has outputs
- [x] Commit bacc95a exists in git log
- [x] All 5 success criteria met:
  - Notebook executes without error (nbconvert exit 0)
  - geo_agg has 1 row per zip_code_prefix (assert passed)
  - gold_with_geo has 1 row per order_id (assert passed)
  - Canceled and unavailable orders excluded (1985 removed)
  - seller_lat, seller_lng, customer_lat, customer_lng present in gold_with_geo
