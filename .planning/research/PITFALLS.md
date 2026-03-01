# Pitfalls Research

**Domain:** E-commerce data science — customer satisfaction prediction and logistics analysis (Olist dataset, 1-week sprint, 6-person team)
**Researched:** 2026-03-01
**Confidence:** HIGH (data leakage, class imbalance, EDA pitfalls), MEDIUM (team collaboration patterns, presentation patterns)

---

## Critical Pitfalls

### Pitfall 1: Post-Delivery Features Contaminating the Pre-Delivery Model

**What goes wrong:**
Features derived from data that only exists *after* delivery — `order_delivered_customer_date`, `order_delivered_carrier_date`, actual delivery duration, `review_score` itself, `review_comment_message` — get included in the feature matrix. The model learns from outcomes it would never observe at prediction time. Validation metrics (accuracy, AUC) appear excellent during development, but the model is completely useless operationally because it can only predict after the event it was supposed to prevent.

**Why it happens:**
The Olist schema joins `orders`, `order_reviews`, and `order_items` into one wide table. When the team builds the "gold" table first and then does feature engineering from it, all columns are visible simultaneously. Engineers grab what looks correlated without checking temporal availability. Common specific offenders in the Olist dataset:
- `order_delivered_customer_date` — the actual delivery timestamp (unavailable at shipment)
- `review_score`, `review_comment_message`, `review_comment_title` — written post-delivery, directly encodes the target
- Derived column "actual delivery delay" computed as `order_delivered_customer_date - order_estimated_delivery_date` — only calculable after delivery
- Any seller-level aggregate that uses reviews from the same order being scored

**How to avoid:**
Define an explicit temporal cutoff rule in Fase 0 (Kickoff): "Features must be derivable using only data available at `order_approved_at` or `order_delivered_carrier_date` (moment of dispatch to carrier)." Enforce it as a written checklist. For the gold table, add a column-classification pass: every column must be tagged `[pre-delivery | post-delivery | target]` before feature engineering begins. Legitimate pre-delivery features include: `order_estimated_delivery_date`, `freight_value`, `price`, `product_weight_g`, `product_description_lenght`, seller city/state, customer city/state, distance between them, seller's historical review rate (from *previous* orders only, with a date cutoff), and calendar features from order placement date.

**Warning signs:**
- Model accuracy above 85% on a balanced or moderately imbalanced dataset — investigate immediately
- A feature called `delay`, `late`, `actual_delivery`, or `days_to_deliver` in the feature list
- Any review-related column used as a feature when the target is also review-related
- Cross-validation score significantly higher than expected for this problem type (~75-80% is realistic)

**Phase to address:** Fase 0 (Kickoff) — define the pre-delivery feature contract before any code is written. Fase 1 (Data Foundation) — enforce the contract via a column audit during gold table construction.

---

### Pitfall 2: Using `review_comment_message` or `review_comment_title` as a Feature

**What goes wrong:**
This is a specific sub-case of Pitfall 1 but deserves its own entry because it is extremely common in Olist projects and highly seductive. The review text is rich, Portuguese-language, and strongly correlated with the review score. Teams working on the NLP track (Pessoa 5) often create sentiment features or topic flags and then pass them to the ML model. This is catastrophic leakage: the review text is written at the same moment as the review score and is never available before the rating exists.

**Why it happens:**
The Olist dataset serves up review text right alongside `review_score` in the same table. The NLP track produces features that look like legitimate predictors. Without clear ownership of the "no post-delivery features" guardrail, the ML lead may accept these features from the NLP contributor.

**How to avoid:**
Explicitly list `review_comment_message` and `review_comment_title` as FORBIDDEN in the ML feature pipeline during Fase 0. The NLP analysis (Pessoa 5) is valuable for EDA storytelling (Ato 1) but must be explicitly isolated and never fed into the Ato 2 model. Document this boundary in the team's shared feature registry.

**Warning signs:**
- Any sentiment score, topic flag, or review keyword count appearing in the feature matrix
- ML model accuracy above 90% — almost certainly caused by review text leaking

**Phase to address:** Fase 0 (Kickoff) — explicit exclusion list. Fase 3 (ML) — ML Lead audits every feature's source table before fitting.

---

### Pitfall 3: Preprocessing Before Train/Test Split (Leakage Through Statistics)

**What goes wrong:**
The team builds the gold table, then immediately applies `StandardScaler`, `MinMaxScaler`, target encoding, or missing value imputation using `.mean()` / `.median()` on the full dataset. Statistical properties of the test set (mean delivery time, median freight, category frequency) leak into the training set. This inflates performance metrics and creates a model that generalizes less well than it appears to.

**Why it happens:**
In a 1-week sprint with separate notebook owners, the data foundation person builds a cleaned and normalized gold table that everyone uses. The normalization step "feels like data cleaning" rather than modelling. The ML Lead then splits the already-normalized data.

**How to avoid:**
The gold table must be delivered in raw, unnormalized form. All scaling, encoding, and imputation must live inside a `sklearn.Pipeline` that is fit only on `X_train`. Use `Pipeline([('scaler', StandardScaler()), ('model', LogisticRegression())])` so the fit/transform boundary is automatic. This also makes the Streamlit demo correct — predictions use the pipeline's transform step.

**Warning signs:**
- `scaler.fit_transform(df[features])` applied before `train_test_split`
- Target encoding implemented as a dictionary built from the full dataset
- Missing value fill using `df[col].mean()` on the full dataframe

**Phase to address:** Fase 1 (Data Foundation) — clarify that the gold table is raw. Fase 3 (ML) — Pipeline pattern mandated before any fitting.

---

### Pitfall 4: Optimizing Accuracy on a Class-Imbalanced Target

**What goes wrong:**
The target class (1-2 star reviews) is a minority — typically around 15-20% of the Olist dataset. A model that always predicts "no risk" achieves 80-85% accuracy without learning anything. The team celebrates high accuracy, presents it to leadership, and leadership asks "if you can identify 80% of happy customers why can't you identify unhappy ones?" — a question the team cannot answer because they never measured recall.

**Why it happens:**
Accuracy is the default metric in most notebooks and model scorecards. The team builds a baseline, sees 83% accuracy, concludes it is good. No one checks the confusion matrix.

**How to avoid:**
Establish Precision-Recall AUC (PR-AUC) and Recall for the positive class (risk = 1-2 stars) as the primary metrics in the project agreement at Fase 0. Never report accuracy as the headline metric. Always show the confusion matrix alongside PR-AUC. Set a decision threshold explicitly (e.g., "flag orders with >40% predicted risk probability") and report the operational impact: "at this threshold, we catch X% of bad reviews with Y% false alarm rate."

**Warning signs:**
- Evaluation section shows only `accuracy_score` or `roc_auc_score`
- No confusion matrix in the notebook
- Model recall for the positive class is below 40% but "accuracy looks fine"
- `class_weight='balanced'` not set and no resampling applied

**Phase to address:** Fase 0 (Kickoff) — define primary metrics as PR-AUC and Recall. Fase 3 (ML) — evaluation checklist must include confusion matrix and threshold analysis.

---

### Pitfall 5: Seller Historical Aggregates That Include the Order Being Scored

**What goes wrong:**
The team creates a valuable feature: "seller_avg_review_score" or "seller_late_delivery_rate." If computed from ALL orders in the dataset — including the order being predicted — the target information is directly embedded in the feature. This is a subtle form of target leakage that does not produce suspiciously high accuracy (the signal is diluted) but still biases the model and makes it un-deployable.

**Why it happens:**
Aggregation queries are written naively: `df.groupby('seller_id')['review_score'].mean()` and then merged back. This includes every order from that seller, including the one under analysis.

**How to avoid:**
All historical seller aggregates must use a temporal exclusion: only include orders with `order_purchase_timestamp` strictly before the timestamp of the order being scored. This is most cleanly implemented using a window function or a self-join with a date filter. Additionally, use historical data from at least 30 days prior to avoid recency contamination. Tag all seller aggregate features in the feature registry as "requires temporal exclusion."

**Warning signs:**
- Seller aggregate features computed with a simple `groupby` without a date filter
- Feature correlates very strongly (r > 0.8) with target — investigate temporal contamination

**Phase to address:** Fase 1 (Data Foundation) — data lead defines the temporal exclusion pattern. Fase 3 (ML) — ML Lead reviews all aggregated features.

---

### Pitfall 6: Geographic Distance Computed Incorrectly

**What goes wrong:**
The geolocation table in Olist has multiple lat/lon entries per zip code prefix (not per exact zip code). Teams either (a) take the first row per zip prefix, ignoring that it may be in the wrong city, or (b) compute straight-line (Euclidean) distance in lat/lon degrees rather than actual kilometers using the Haversine formula. Both produce a "distance" feature that adds noise rather than signal.

**Why it happens:**
The Olist geolocation table structure is non-obvious. There are ~19,000 distinct zip code prefixes with multiple rows each. The natural join `merge(orders, geolocation, on='customer_zip_code_prefix')` creates a many-to-many explosion unless aggregated first.

**How to avoid:**
Aggregate geolocation to one representative lat/lon per zip prefix (median is more robust than mean or first). Use the Haversine formula for distance, not Euclidean. The `geopy` library or a manual Haversine implementation handles this. Validate the resulting distances: São Paulo to Manaus should be approximately 2,700 km; if distances in the dataset are in degrees (0-10 range) rather than km (0-4000 range), the computation is wrong.

**Warning signs:**
- Distance column values below 20 (almost certainly in degrees, not km)
- DataFrame shape explodes unexpectedly after merging with geolocation (many-to-many join)
- Distance feature has near-zero correlation with delivery time (corrupted feature has no signal)

**Phase to address:** Fase 1 (Data Foundation) — geolocation aggregation pattern established. Fase 2 (EDA) — Pessoa 2 validates distance distribution before mapping.

---

## Technical Debt Patterns

Shortcuts that seem reasonable in a 1-week sprint but create compounding problems.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Single "god notebook" with all analysis | Fast start, one file to share | Merge conflicts, unclear ownership, cell state corruption | Never in a 6-person team |
| Hardcoded file paths (`pd.read_csv('/Users/maria/Desktop/orders.csv')`) | Works on one machine | Breaks on every other machine, demo fails live | Never — use relative paths or a config |
| Fitting scaler on full dataset before split | Simpler code | Data leakage from test set statistics | Never |
| Groupby aggregates without temporal exclusion | Faster to write | Target leakage in seller/customer features | Never for ML features |
| Using accuracy as primary metric | Easy to explain | Hides class imbalance failures | Never for this project |
| Skipping baseline model and going straight to XGBoost | Looks more impressive | No fallback if tuning fails; no interpretability anchor | Never in a sprint — baseline must come first |
| Committing notebooks with all outputs rendered | Preserves visual state | Massive git diffs, merge conflicts make collaboration impossible | Never — clear outputs before committing |
| Writing EDA findings in notebooks without summaries | Fast during analysis | Team members cannot reuse findings; storytelling person has no source material | Never — always add a markdown summary cell |

---

## Integration Gotchas

Common mistakes when working with the Olist multi-table schema.

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Olist geolocation join | Many-to-many explosion via `merge` on zip prefix | Pre-aggregate to one row per zip prefix (median lat/lon) before merging |
| `customer_id` vs `customer_unique_id` | Treating `customer_id` as unique customer identifier | 99,441 `customer_id` values map to 96,096 unique customers — use `customer_unique_id` for customer-level analysis |
| Temporal cutoff (September 2018) | Including the sharp revenue drop as meaningful signal | The dataset ends abruptly in Sept 2018 — exclude that month from trend analysis or explicitly note the truncation |
| `order_items` join (one order, multiple items) | Joining without aggregating produces duplicate order rows | Always `groupby('order_id').agg(...)` on items before merging with orders |
| Review join | Joining `order_reviews` 1:1 with orders when multiple reviews exist per order | Take the last review per order (or max negative score) — some orders have duplicate review entries |
| NLP features into ML pipeline | Using review text features from `order_reviews` in the ML model | Review text is post-delivery — forbidden in pre-delivery model; restrict NLP analysis to EDA/storytelling only |

---

## Performance Traps

Patterns that cause problems during the sprint timeline (not production scale, but relevant for demo stability).

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Loading all 9 Olist CSVs unfiltered at once | Notebook takes 2+ min to restart kernel; demo freezes | Pre-merge into gold table once; load only the gold parquet for ML and EDA notebooks | On laptops with <8GB RAM during live demo |
| SHAP on large datasets without sampling | SHAP TreeExplainer runs for 10+ minutes on 100k rows | Sample 5,000 rows for SHAP visualization; use `shap.sample` | During live demo with full dataset |
| Plotly maps with all 100k customer points | Browser crashes or hangs rendering the map | Aggregate to zip prefix or UF level before plotting — never plot individual points | Any audience laptop with <16GB RAM |
| Uncleared notebook outputs in git | Merge conflicts on every pull; notebook JSON diffs are unreadable | Add `nbstripout` as a pre-commit hook or manually clear outputs before push | After the first team member pushes a rendered notebook |
| Re-running full data pipeline on demo day | Risk of environment mismatch, random seed differences, new errors | Freeze the gold table as a parquet on Day 3 and never re-generate it | If a dependency updates or a random seed changes between runs |

---

## "Looks Done But Isn't" Checklist

Things that appear complete to the team but fail in review or during the presentation.

- [ ] **Pre-delivery feature contract:** Every feature has been verified against the temporal cutoff — check that no column derived from `order_delivered_customer_date`, `review_score`, or `review_comment_*` appears in `X_train`
- [ ] **Model metrics:** Confusion matrix, PR-AUC, and Recall for positive class are all present — not just accuracy or ROC-AUC
- [ ] **Decision threshold:** A specific threshold is chosen and justified ("at 0.42 we catch 68% of bad reviews with 22% false alarm rate") — a model without an operational threshold is not actionable
- [ ] **Geolocation distances:** Distance column values are in kilometers (expected range 0–4000), not decimal degrees (0–10)
- [ ] **Gold table reproducibility:** The gold table can be rebuilt by anyone on the team by running one notebook from top-to-bottom with restarted kernel — no hidden state
- [ ] **EDA charts have axis labels and titles visible without the presenter speaking:** Each chart must stand alone for the slide deck
- [ ] **Business translation for ML:** Model results expressed in operational terms ("X orders per week would be flagged, costing Y intervention actions, preventing Z bad reviews") — not just metric scores
- [ ] **Seller aggregate features use temporal exclusion:** At least spot-check one seller aggregate feature to confirm it was not computed on the full dataset
- [ ] **Streamlit demo tested on the presentation machine:** Not just on the developer's laptop
- [ ] **Class distribution reported:** The audience must know that 1-2 star reviews are ~15-20% of orders for the metrics to be interpretable

---

## Recovery Strategies

When pitfalls occur despite prevention, how to recover quickly within the sprint.

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Post-delivery features discovered mid-sprint | MEDIUM — 2-4 hours | Drop the leaking columns, re-run feature engineering, re-train; expect metrics to drop — this is honest |
| Model accuracy collapses after leakage fix | LOW | Show the baseline (logistic regression) which should still perform reasonably; contextualize the drop as "removing artificial inflation" — leadership respects honesty |
| Geolocation many-to-many explosion discovered | LOW | Pre-aggregate geolocation table once, re-run merge; the fix is a 3-line pandas operation |
| Notebook merge conflict on team pull | MEDIUM | Assign one person as notebook integration owner per area; resolve manually using `nbdime` or accept one version and re-run |
| Demo machine cannot render Plotly maps | LOW | Have static `.png` exports of all maps as a fallback in the slides |
| Class imbalance: model predicts all negatives | LOW | Add `class_weight='balanced'` to logistic regression or XGBoost; re-run; if still failing, apply SMOTE on training split only |
| Streamlit demo fails to start on presentation day | LOW | Have a pre-rendered Jupyter notebook with all outputs visible as fallback; never demo from a cold start without a backup |

---

## Pitfall-to-Phase Mapping

How each roadmap phase should address these pitfalls.

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Post-delivery features in ML model | Fase 0 (Kickoff) — define temporal cutoff contract | Fase 3: ML Lead runs column audit showing every feature source before fitting |
| Review text/score leakage | Fase 0 (Kickoff) — explicit forbidden column list | Fase 3: Check `X_train.columns` for any review-table column |
| Preprocessing before split | Fase 1 (Data Foundation) — deliver raw gold table; Fase 3 — Pipeline pattern | Confirm scaler is inside Pipeline, not applied to `df` before split |
| Accuracy metric on imbalanced data | Fase 0 (Kickoff) — define PR-AUC + Recall as primary metrics | Fase 3: Evaluation section must show confusion matrix |
| Seller aggregates without temporal exclusion | Fase 1 (Data Foundation) — data lead documents temporal exclusion pattern | Fase 3: Spot-check one seller feature computation |
| Geolocation distance errors | Fase 1 (Data Foundation) — Pessoa 2 validates Haversine computation | Fase 2 (EDA): Distance distribution check before mapping |
| God-notebook chaos | Fase 0 (Kickoff) — define notebook ownership (one per area) | Fase 1: Each person has their own named notebook, gold table is a shared artifact |
| Hardcoded file paths | Fase 0 (Kickoff) — define project folder structure and relative path convention | Fase 1: Verify everyone loads from the same relative path |
| EDA findings not documented for storytelling | Fase 2 (EDA) — each chart notebook ends with a markdown findings cell | Fase 4 (Storytelling): Pessoa 6 can pull findings without re-running notebooks |
| Demo instability | Fase 3 (ML) — freeze gold table as parquet; Fase 4 — test demo on presentation machine | Fase 4: Full end-to-end demo rehearsal 24 hours before presentation |
| Business translation missing | Fase 4 (Story) — translate every metric to an operational number | Presentation: Leadership can answer "what do we do Monday morning?" |
| Class imbalance ignored | Fase 0 (Kickoff) — class distribution check is first step of EDA | Fase 3: Baseline must use `class_weight='balanced'` |

---

## Sources

- WebSearch: Data leakage in feature engineering — multiple sources agree on temporal leakage definition and prevention via time-based CV (MEDIUM confidence, patterns well-established)
- WebSearch: Olist dataset common mistakes — Kaggle community analysis identified `review_comment_message` leakage, `customer_id` vs `customer_unique_id` confusion, September 2018 truncation (MEDIUM confidence, practitioner-sourced)
- WebSearch: Class imbalance and precision-recall pitfalls — multiple ML resources confirm accuracy is misleading on imbalanced targets; PR-AUC preferred over ROC-AUC under severe imbalance (HIGH confidence, academically established)
- WebSearch: EDA and stakeholder presentation mistakes — multiple practitioner sources agree on jargon problem, correlation-causation confusion, one-time vs iterative EDA framing (MEDIUM confidence)
- WebSearch: Jupyter notebook team collaboration pitfalls — hidden state, environment drift, lack of real-time collaboration are well-documented (MEDIUM confidence)
- WebSearch: Logistics ML model pitfalls — recall for delayed deliveries more important than accuracy; practical applicability gap between research and operations (MEDIUM confidence)
- Training data / domain knowledge: Haversine vs Euclidean distance, many-to-many geolocation joins in Olist, sklearn Pipeline leakage patterns — LOW to MEDIUM confidence, should be verified during Fase 1 with actual dataset inspection

---
*Pitfalls research for: Olist E-Commerce — Customer Satisfaction & Logistics Risk Prediction*
*Researched: 2026-03-01*
