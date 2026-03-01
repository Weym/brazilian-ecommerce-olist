# Project Research Summary

**Project:** Olist E-Commerce Analytics — Logistica, Satisfacao e Risco Pre-Entrega
**Domain:** Data Science Sprint — EDA + ML + Live Demo (E-commerce / Logistics Analytics)
**Researched:** 2026-03-01
**Confidence:** HIGH

## Executive Summary

This is a 1-week, 6-person data science sprint delivering a leadership presentation backed by a live Streamlit demo. The domain is well-understood: customer satisfaction prediction on the public Olist Brazilian e-commerce dataset (~100K orders, 9 relational CSVs). Research consistently converges on a two-act narrative structure — Ato 1 proves the problem (logistics delays and freight cost drive 1-2 star reviews), Ato 2 delivers the solution (a pre-delivery risk model that enables proactive intervention). Every architectural and feature decision should be evaluated against this deliverable, not against abstract engineering quality.

The recommended approach is a Medallion-style data pipeline: raw CSVs feed a single validated gold table (Parquet), which feeds parallel EDA, geo, and ML notebook tracks. The ML model is a baseline logistic regression followed by XGBoost with SHAP explainability, evaluated with PR-AUC and recall (not accuracy). The demo is a multi-page Streamlit app loading pre-computed artifacts — it never runs heavy computation live. The critical constraint driving every choice is the 1-week deadline: use stable, widely-known libraries (pandas 2.3.3, scikit-learn 1.6.x, XGBoost 3.2.0, Streamlit 1.54.0), not cutting-edge alternatives.

The principal risks are data leakage (post-delivery features or review text contaminating the pre-delivery model), class imbalance mismanagement (optimizing accuracy instead of PR-AUC/recall on a 15-20% minority class), and integration failure during the demo (Streamlit timeout if assets are not pre-computed). All three are preventable with decisions made on Day 1: define the pre-delivery feature contract explicitly, mandate PR-AUC as the headline metric from the start, and commit to pre-computing all heavy artifacts before integration day.

---

## Key Findings

### Recommended Stack

The stack is intentionally conservative. Python 3.11 is the base (stable, max ecosystem support; avoid 3.13). pandas 2.3.3 is the data layer — Copy-on-Write is on by default, and 3.0.x is still RC. XGBoost 3.2.0 is the primary model: best AUC on tabular imbalanced data with native sklearn API and `scale_pos_weight` for class imbalance. Streamlit 1.54.0 is the demo framework — 3x faster to build than Dash and zero JS required for a mixed-audience presentation. plotly 6.5.2 provides interactive charts that integrate natively with Streamlit via `st.plotly_chart()`.

Supporting libraries serve specific responsibilities: folium 0.20.0 + geopandas 1.1.2 for choropleth maps of Brazilian states, haversine 2.9.x for vectorized seller-to-customer distance (never manual formula), shap 0.50.0 for TreeExplainer beeswarm plots on XGBoost, seaborn 0.13.2 for statistical charts in notebooks and slides. NLP (HuggingFace transformers with a Portuguese model) is strictly optional for Pessoa 5 and only if the core pipeline finishes early.

**Core technologies:**
- Python 3.11.x: language base — most stable version with maximum library support
- pandas 2.3.3: data manipulation and joins — stable, Copy-on-Write, compatible with all downstream libs
- scikit-learn 1.6.x: pipeline, baseline model, metrics — broad Python compatibility, prevents leakage via Pipeline encapsulation
- XGBoost 3.2.0: main classification model — best AUC on tabular imbalanced data, native sklearn API
- Streamlit 1.54.0: live demo — fastest path to interactive presentation for mixed audience
- plotly 6.5.2: interactive visualizations — native Streamlit integration, no JS required
- SHAP 0.50.0: model explainability — TreeExplainer beeswarm plots legible to non-technical leadership
- folium 0.20.0 + geopandas 1.1.2: geographic maps — choropleth for Brazilian states with direct geopandas integration

**What to avoid:** pandas 3.0.x RC, TextBlob for Portuguese NLP, ROC-AUC as primary metric, accuracy as headline metric, deep learning, Dask/Spark, ipywidgets, matplotlib directly in Streamlit.

### Expected Features

The feature set maps directly to the two-act narrative. Ato 1 features (table stakes) prove the problem exists; Ato 2 features (differentiators) deliver the actionable solution. Anti-features are scope traps that consume sprint time without improving the presentation.

**Must have (table stakes — Ato 1 + Ato 2 minimum):**
- Tabela gold validated (row counts, null audit, temporal range) — foundation of all downstream work
- Atraso vs. nota correlation chart — single most important Ato 1 visual
- Frete vs. nota correlation chart — second key Ato 1 driver
- Geographic heatmap of 1-2 star concentration by UF — answers "where is the pain worst?"
- Baseline logistic regression with PR-AUC and recall on test set — guarantees ML deliverable
- PR curve + threshold decision + estimated orders flagged per month — makes model operational
- Two-act slide deck (Ato 1: problem evidence, Ato 2: model + playbook) — the actual leadership deliverable

**Should have (competitive differentiators):**
- XGBoost replacing/augmenting baseline — trigger: baseline exists and Fase 3 has time remaining
- SHAP feature importance (beeswarm + waterfall) — transforms "model says so" into "delay is 3x more impactful than freight"
- Seller-level risk aggregation — enables vendor management decisions; trigger: model predictions on full dataset
- Route/corridor analysis (UF origin to UF destination) — pinpoints structural logistics failure points
- Operational playbook ("flag top 20% of at-risk orders, estimated X satisfaction recovery")
- Live Streamlit demo — cut if Fase 3 is not closed by Day 5

**Defer (v2+):**
- NLP deep-dive on review text — dedicated sprint needed; pitch as next step in final slide
- Real-time scoring API / production pipeline — explicitly out of scope
- A/B test for operational playbook — requires real intervention data
- Counterfactual before/after narrative — only build if XGBoost, SHAP, and playbook are all done first

**Do not build:**
- RFM customer segmentation (Olist customers have very low repeat rate — trivial segments)
- Full filterable dashboard (scope creep; focused demo impresses more)
- Real-time streaming pipeline (dataset is historical batch)
- Hyperparameter grid search (4-6 hours for <1% AUC gain)

### Architecture Approach

The architecture follows a strict Medallion pattern adapted for a 6-person sprint: Raw CSVs (immutable) feed a single gold Parquet table (Pessoa 1, Fase 1), which serves as the sole interface contract for all downstream notebooks. EDA (Pessoa 3), Geo (Pessoa 2), and ML (Pessoa 4) tracks run in parallel after gold is available. Shared feature engineering logic lives in `src/features.py` — imported by both the ML training notebook and the Streamlit app, guaranteeing training/inference consistency. The Streamlit app loads only pre-computed Parquet files and serialized joblib pipelines — no heavy computation at demo time.

**Major components:**
1. `data/raw/` — 9 immutable Olist CSVs; nobody writes here after initial ingest
2. `notebooks/01-data-foundation/build_gold.ipynb` + `data/gold/olist_gold.parquet` — all joins happen once here; Pessoa 1 owns; interface contract for the team
3. `notebooks/02-eda/` (Pessoa 3) + `notebooks/03-geo/` (Pessoa 2) — parallel analysis tracks reading gold table, writing figures and `data/processed/geo_aggregated.parquet`
4. `notebooks/04-ml/` (Pessoa 4) — pre-delivery feature engineering, baseline, XGBoost, serialization to `models/final_pipeline.joblib`
5. `src/features.py` — shared feature functions imported by both notebooks and Streamlit; Pessoa 4 owns; changes here affect training and inference simultaneously
6. `app/` (Streamlit, Pessoa 6) — multi-page app loading parquet + joblib artifacts; pages developed independently by each track owner
7. `reports/` — slide deck and exported figures; Pessoa 6 assembles from EDA/ML outputs

**Key patterns:**
- Gold table as interface contract: one join, one clean version, no ambiguity
- sklearn Pipeline encapsulating all preprocessing: scaler/encoder fitted only on X_train, serialized with model
- Pre-computed artifacts for demo: zero pandas/sklearn at presentation time
- One-person-per-notebook ownership with numbered subdirectories: zero merge conflicts

### Critical Pitfalls

1. **Post-delivery feature leakage** — `order_delivered_customer_date`, `review_score`, `review_comment_message` present in feature matrix. Prevention: define and document the pre-delivery feature contract (temporal cutoff = `order_approved_at`) on Day 1 before any code. Tag every gold table column as `[pre-delivery | post-delivery | target]`. Use `src/features.py:PRE_DELIVERY_FEATURES` as the allow-list.

2. **Optimizing accuracy on imbalanced target** — 1-2 star reviews are ~15-20% of orders; a model predicting "always good" achieves 80-85% accuracy. Prevention: establish PR-AUC + Recall as the only headline metrics at Fase 0 kickoff. Always show confusion matrix. Mandate `class_weight='balanced'` on baseline before any tuning.

3. **Preprocessing before train/test split** — `StandardScaler` applied to the full gold table before `train_test_split` leaks test-set statistics into training. Prevention: the gold table is delivered raw; all scaling/encoding live inside a `sklearn.Pipeline` fit only on X_train.

4. **Geolocation many-to-many explosion and Euclidean distance** — merging with the geolocation table without pre-aggregating creates row explosion; using degree-difference as distance gives values in 0-10 range instead of 0-4000 km. Prevention: pre-aggregate to one row per zip prefix (median lat/lon); always use Haversine formula; validate distance distribution during Fase 2.

5. **Demo instability from live computation** — Streamlit reruns the full script on every interaction; any operation >2s causes timeouts during the live presentation. Prevention: all heavy outputs (gold Parquet, geo aggregations, model pipeline) are pre-computed and frozen by Day 3; Streamlit only loads and displays.

---

## Implications for Roadmap

Based on the combined research, a 5-phase structure (Fase 0 through Fase 4) maps directly onto the dependency graph identified in ARCHITECTURE.md and the pitfall prevention requirements from PITFALLS.md.

### Phase 1 (Fase 0): Kickoff and Contracts

**Rationale:** Four of the six critical pitfalls (data leakage, metric confusion, preprocessing before split, class imbalance) are preventable only with explicit team agreements made before any code is written. This phase has no code deliverable — it produces decisions and documented contracts. Skipping it is the single highest-risk action the team can take.

**Delivers:** Pre-delivery feature contract (column allow-list with temporal cutoff documented), metric agreement (PR-AUC + Recall as headline, not accuracy), project folder structure, git branch strategy, notebook ownership assignments, Kaggle dataset download instructions.

**Addresses:** Table stakes features (by locking the feature list that enables them), anti-features (by explicitly banning RFM, deep learning, full dashboard).

**Avoids:** Post-delivery leakage (Pitfall 1, 2), accuracy metric trap (Pitfall 4), hardcoded paths, god-notebook chaos.

**Research flag:** Well-documented pattern — skip `/gsd:research-phase`.

---

### Phase 2 (Fase 1): Data Foundation

**Rationale:** `data/gold/olist_gold.parquet` is the interface contract for the entire team. Nothing else can start until this exists and is validated. A data quality error discovered after EDA begins forces rework of all charts. This phase blocks all parallel work — it must be completed in the morning of Day 1.

**Delivers:** `data/gold/olist_gold.parquet` (9-table join, validated row counts, null audit, temporal range documented, all columns tagged pre/post/target), geolocation pre-aggregated to one row per zip prefix, distance calculation function in `src/metrics.py`.

**Addresses:** Tabela gold table stakes feature, missing values and outlier treatment documented (table stakes).

**Avoids:** Many-to-many geolocation explosion (Pitfall 6), preprocessing-before-split if gold table is delivered raw, `customer_id` vs `customer_unique_id` confusion, September 2018 truncation artifact.

**Stack:** pandas 2.3.3 `merge()` chain, geopandas 1.1.2 for shapefile, haversine 2.9.x for distance.

**Research flag:** Well-documented Cookiecutter Data Science pattern — skip `/gsd:research-phase`.

---

### Phase 3 (Fase 2): EDA — Impacto da Logistica

**Rationale:** Ato 1 of the narrative requires visual proof that delays and freight costs drive bad reviews, and a geographic view of where the pain is worst. These analyses run in parallel once the gold table is available. They block the slide deck assembly (Pessoa 6 cannot finalize Ato 1 slides without these figures).

**Delivers:** Atraso vs. nota chart, frete vs. nota chart, distribution of review scores (J-shape), geographic choropleth heatmap by UF, route/corridor analysis (if bandwidth allows), exported PNG figures to `reports/figures/`, `data/processed/geo_aggregated.parquet`, Mann-Whitney significance test validating delay group differences.

**Addresses:** Atraso vs. nota (P1), frete vs. nota (P1), geographic heatmap (P1), route/corridor analysis (P2).

**Avoids:** Per-product category analysis as primary finding (anti-feature), RFM segmentation (anti-feature), plotly maps with 100k individual points (performance trap — aggregate to UF level).

**Stack:** plotly 6.5.2 (interactive EDA charts), seaborn 0.13.2 (statistical charts for slides), folium 0.20.0 + geopandas 1.1.2 (choropleth maps), scipy.stats.mannwhitneyu (significance validation).

**Research flag:** Well-documented EDA pattern — skip `/gsd:research-phase`.

---

### Phase 4 (Fase 3): ML — Modelo de Risco Pre-Entrega

**Rationale:** Ato 2 of the narrative is the model. It depends on the gold table (Fase 1) and a documented pre-delivery feature set. The baseline model must exist before XGBoost — it is the fallback if tuning fails and the comparison anchor for SHAP. This phase must close by Day 4 for Pessoa 6 to integrate the demo.

**Delivers:** `src/features.py` with `PRE_DELIVERY_FEATURES` allow-list, baseline logistic regression (`models/baseline_logreg.joblib`) with PR-AUC and recall on test set, XGBoost pipeline (`models/final_pipeline.joblib`) if baseline is stable, SHAP beeswarm summary plot + waterfall examples, PR curve + selected decision threshold + operational impact estimate ("X orders flagged per week"), seller-level risk aggregation table.

**Addresses:** Baseline ML model (P1), PR curve + threshold + impact estimate (P1), XGBoost (P2), SHAP feature importance (P2), seller-level risk aggregation (P2), operational playbook (P2), confidence intervals on predictions (P2).

**Avoids:** Post-delivery features in feature matrix (Pitfall 1), review text in features (Pitfall 2), preprocessing before split (Pitfall 3), accuracy as headline metric (Pitfall 4), seller aggregates without temporal exclusion (Pitfall 5), deep learning (anti-feature), survival analysis (anti-feature), grid search (anti-feature), ROC-AUC as primary metric (anti-feature).

**Stack:** scikit-learn 1.6.x Pipeline + ColumnTransformer, XGBoost 3.2.0 with `scale_pos_weight`, shap 0.50.0 TreeExplainer, imbalanced-learn 0.14.1 (only if recall is unacceptable without SMOTE), joblib for serialization.

**Research flag:** Pattern is well-documented for tabular classification — skip `/gsd:research-phase`. However, the temporal exclusion pattern for seller-level historical aggregates (Pitfall 5) warrants a short validation step during Fase 1 when the gold table is built.

---

### Phase 5 (Fase 4): Demo + Story

**Rationale:** This phase integrates all prior outputs into the final deliverable — the slide deck and the Streamlit demo. It depends on all artifacts being frozen (gold Parquet, geo Parquet, model joblib, exported figures). The Streamlit demo is contingent on Fase 3 closing on time; if not, the slides are the non-negotiable fallback.

**Delivers:** Streamlit multi-page app (`app/pages/01_overview.py`, `02_mapa.py`, `03_modelo.py`) loading pre-computed artifacts, full presentation slide deck with two-act narrative (Ato 1: evidence, Ato 2: model + playbook), demo rehearsal on the presentation machine, static PNG fallbacks for all maps.

**Addresses:** Live Streamlit demo (P2, cut if Fase 3 is late), two-act slide deck (P1), business translation of ML metrics (table stakes), operational playbook (P2).

**Avoids:** Demo instability from live computation (use `@st.cache_data`, `@st.cache_resource`; never run joins at demo time), Plotly maps with 100k individual points, Streamlit cold-start failure (keep rendered notebook fallback).

**Stack:** Streamlit 1.54.0 multi-page, plotly 6.5.2 `st.plotly_chart()`, joblib.load for model, pandas read_parquet for data, `@st.cache_data` / `@st.cache_resource` mandatory.

**Research flag:** Streamlit multi-page pattern is well-documented (v1.28+ native pages) — skip `/gsd:research-phase`. The integration day (Day 4) is the highest-risk coordination point; a dry run with fake data before real artifacts are ready is strongly recommended.

---

### Phase Ordering Rationale

- Fase 0 before everything: four critical pitfalls are only preventable as team agreements before code is written. There is no recovery from leakage discovered the day before presentation.
- Fase 1 blocks all parallel work: the gold table is the interface contract; no analysis or ML can start without it. This is a hard dependency, not a preference.
- Fase 2 and Fase 3 run in parallel after Fase 1: EDA (Pessoa 2+3) and ML (Pessoa 4) are independent once the gold table exists. NLP (Pessoa 5) is optional and starts only after Pessoa 4 has a working baseline.
- Fase 4 is purely integrative: it has no original analysis — it assembles outputs from Fases 1-3. Starting it with fake/placeholder data (Day 1-2) reduces Day 4 integration risk.
- Cut line: if Fase 3 is not closed by Day 5, Fase 4 drops the Streamlit demo. Slides are the non-negotiable delivery.

### Research Flags

Phases likely needing deeper research during planning:
- None identified — all phases follow well-established, documented patterns for the Olist dataset and Python DS stack.

Phases with standard patterns (skip research-phase):
- **Phase 1 (Fase 0):** Project kickoff agreements — standard DS sprint practice
- **Phase 2 (Fase 1):** Medallion data pipeline on relational CSVs — Cookiecutter Data Science documented pattern
- **Phase 3 (Fase 2):** EDA for e-commerce satisfaction — abundant practitioner and academic examples on exactly this dataset
- **Phase 4 (Fase 3):** Tabular classification with sklearn Pipeline + XGBoost — exhaustively documented
- **Phase 5 (Fase 4):** Streamlit multi-page demo with pre-computed assets — official documentation covers this exactly

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Versions verified via PyPI release data and official docs on 2026-03-01; compatibility matrix validated across all core libraries |
| Features | HIGH | Peer-reviewed source (SpringerLink ICCCE 2024) plus practitioner sources; feature prioritization consistent across multiple independent Olist analyses |
| Architecture | HIGH | sklearn Pipeline leakage prevention is officially documented; Cookiecutter Data Science v2 is the established community standard; Streamlit multi-page is in official docs |
| Pitfalls | HIGH (leakage, imbalance), MEDIUM (collaboration patterns) | Data leakage and PR-AUC superiority over ROC-AUC are academically established; Olist-specific gotchas (geolocation, customer_id vs customer_unique_id, September 2018 truncation) are practitioner-verified but should be confirmed against actual dataset on Day 1 |

**Overall confidence:** HIGH

### Gaps to Address

- **Geolocation aggregation behavior on actual data:** PITFALLS.md flags the many-to-many explosion and distance range validation. Confirm during Fase 1 that pre-aggregation to median lat/lon per zip prefix produces a distance distribution in the 0-4000 km range (not 0-10 degrees) before Pessoa 2 builds the choropleth.
- **Class distribution of actual target:** Research estimates 15-20% of orders have 1-2 star reviews, which informs `scale_pos_weight` for XGBoost. Verify the actual proportion during Fase 0 / early Fase 1 to confirm imbalance ratio before setting model hyperparameters.
- **Seller-level historical aggregate feasibility:** Pitfall 5 warns that `groupby('seller_id')` without temporal exclusion leaks target. Whether pre-computing temporally-correct seller history is feasible within the sprint timeline should be confirmed during Fase 1; if too complex, defer seller aggregates to the demo's post-model section rather than the feature matrix.
- **SHAP runtime on full dataset:** PITFALLS.md warns SHAP TreeExplainer can take 10+ minutes on 100k rows. Verify during Fase 3 by running SHAP on a 5,000-row sample first; if performance is acceptable, expand to full set. Pre-sample before presenting to avoid blocking the demo.

---

## Sources

### Primary (HIGH confidence)
- PyPI release history for all core libraries — versions verified 2026-03-01
- scikit-learn official documentation — Pipeline data leakage prevention pattern
- Streamlit official documentation — multi-page apps (v1.28+), caching patterns
- SpringerLink ICCCE 2024 — "Customer Satisfaction Prediction via Interpretable Models and Sentiment Analysis" — peer-reviewed validation of SHAP + PR-AUC approach
- Multiple ML academic sources — PR-AUC vs ROC-AUC superiority under class imbalance

### Secondary (MEDIUM confidence)
- Cookiecutter Data Science v2 official documentation — project structure and gold table pattern
- Databricks Medallion Architecture documentation — Raw/Bronze/Silver/Gold layer concepts
- Kaggle Olist community — dataset structure, common pitfalls (customer_id confusion, September 2018 truncation, review join duplicates)
- Towards Data Science (Jan 2025) — Olist customer satisfaction case study — practitioner validation of approach
- SHAP documentation + practitioner sources — beeswarm/waterfall plots for executive presentations

### Tertiary (LOW confidence, validate during Fase 1)
- Estimated 15-20% class imbalance ratio for 1-2 star reviews — verify on actual dataset
- Haversine distance range validation on actual Olist geolocation data — verify during Fase 1
- Seller historical aggregate feasibility with temporal exclusion — assess complexity on actual data

---
*Research completed: 2026-03-01*
*Ready for roadmap: yes*
