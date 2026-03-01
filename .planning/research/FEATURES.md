# Feature Research

**Domain:** E-commerce customer satisfaction & logistics analytics — data science challenge presentation
**Researched:** 2026-03-01
**Confidence:** HIGH (multiple verified sources, domain consistent with established Olist research community)

---

## Feature Landscape

This document maps features specific to a 1-week data science sprint delivering a leadership presentation. "Users" here are stakeholders (technical + business leadership). Missing table stakes = presentation loses credibility. Differentiators = team impresses. Anti-features = wasted sprint hours.

---

### Table Stakes (Stakeholders Expect These)

Absent any of these, the presentation will feel amateur or incomplete regardless of how advanced the ML is.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Data quality audit upfront | Stakeholders will ask "can we trust this data?" — no audit means no trust | LOW | Row counts, null rates, duplicate order IDs, date range validation; done once in Fase 1 |
| Distribution of review scores (1–5 stars) | Standard framing for "what is the problem" — Olist data shows J-shape distribution (most orders get 5 stars, long tail of 1-stars) | LOW | Show proportion of 1–2 star reviews as the business problem; makes target variable tangible |
| Atraso vs. nota correlation chart | The core thesis of Ato 1 — if atraso destroys satisfaction, show it visually | LOW | Scatter or boxplot: dias_de_atraso x review_score; this is the single most important Ato 1 visual |
| Frete vs. nota correlation | Stakeholders intuitively understand that high freight costs frustrate customers | LOW | Pearson correlation + scatter; frame as "freight burden at time of purchase" |
| Tabela gold com joins validados | Without a single clean analytical table, every analysis is suspect | MEDIUM | olist_orders + order_items + order_reviews + customers + sellers + geolocation; must be documented |
| Geographic map / heatmap of dissatisfaction | Leadership thinks geographically — "where is the problem worst?" | MEDIUM | Choropleth by UF or heatmap by city; concentration of 1–2 star orders by state; Plotly recommended |
| Missing values and outlier treatment documented | Any stakeholder who has worked with data will ask "how did you handle outliers?" | LOW | Document rules: cap atraso at percentile, exclude orders with no delivery date, etc. |
| Baseline ML model (logistic regression or decision tree) | Without a baseline, advanced models have no reference point — the model is uninterpretable | LOW-MEDIUM | Must exist before any gradient boosted model; guarantees deliverable even if XGBoost fails |
| Recall and PR-AUC as primary metrics (not accuracy) | Accuracy on imbalanced data is misleading; any DS-literate stakeholder knows this | LOW | State explicitly: "we use PR-AUC and recall because 1–2 star orders are the minority class" |
| Threshold decision with operational interpretation | Model scores alone mean nothing — leadership needs "at score X, we intervene on Y% of at-risk orders" | MEDIUM | Show PR curve + chosen threshold + estimated orders flagged per week/month |
| Feature list restricted to pre-expedição only | Credibility of the model hinges on this guardrail — post-delivery features = data leakage | LOW-MEDIUM | Document which features are excluded and why; include a simple diagram or bullet list in slides |
| Slides with two-act narrative | A presentation without narrative structure is a data dump, not an insight | MEDIUM | Ato 1: evidence of the problem; Ato 2: the model as the solution; this is the deliverable that leadership remembers |

---

### Differentiators (Competitive Advantage)

Features that are not expected but will make the presentation memorable and the team stand out.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| SHAP feature importance chart | Transforms "the model says so" into "delay duration is 3x more impactful than freight value" — makes ML legible to non-technical leadership | MEDIUM | Use Tree SHAP (fast for XGBoost/Random Forest); show global summary plot + 1–2 force plots for representative high-risk orders |
| Operational impact estimate ("playbook") | Converts model output into a business decision: "if we contact the top 20% of flagged orders, we potentially recover X satisfaction points" | MEDIUM | Requires recall × estimated order volume × assumed improvement rate; rough estimate is fine, caveat clearly |
| Seller-level risk aggregation | Identifies which sellers consistently produce at-risk orders — enables vendor management decisions beyond individual order intervention | MEDIUM | GROUP BY seller_id on model predictions; show top 10 riskiest sellers with order volume; high-impact for ops teams |
| Route/corridor analysis (UF origem → UF destino) | Pinpoints specific logistics corridors that are structural failure points, not just outliers | MEDIUM | Requires geolocation + orders join; heatmap of avg atraso by SP→RJ, SP→NE corridors; directly actionable for carrier negotiations |
| Live Streamlit demo | Moves presentation from "analysis we did" to "tool you can use" — creates visceral impact with leadership | HIGH | Input order attributes → see real-time risk score; high effort but highest impression; contingent on Fase 0 confirmation |
| Confidence interval on predictions | Shows the team understands uncertainty — presenting point estimates without uncertainty looks naive to DS-literate stakeholders | MEDIUM | Platt scaling on logistic regression, or bootstrap confidence intervals on XGBoost probabilities |
| Before/after narrative with counterfactual | "If we had this model in 2017, we would have flagged X orders — of which Y% received 1–2 stars" — validates the model on historical holdout with business framing | HIGH | Requires careful train/test split respecting time; powerful closing slide; only build if ML pipeline is solid |
| NLP sentiment enrichment on review text | Adds qualitative layer: "orders flagged by model AND with negative review text mention 'atrasado' 78% of the time" — corroborates quantitative findings | HIGH | Optional (Pessoa 5 scope); low priority given 1-week constraint; skip unless pipeline is done early |

---

### Anti-Features (Deliberately NOT Build)

These seem sophisticated but cost sprint time without convincing business stakeholders.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| ROC-AUC as primary metric | Familiar to data scientists; "standard" metric | ROC-AUC is misleading on imbalanced data (minority class = bad reviews); a model that predicts "good review" always can achieve 0.85+ ROC-AUC; stakeholders will not catch this but DS reviewers will | Use PR-AUC + recall; explicitly explain why in slides |
| Accuracy as headline metric | Intuitive, percentage feels clean to non-technical audience | With ~20% bad reviews, predicting "all good" gives 80% accuracy — this is a trap; leadership may approve a useless model | Always show confusion matrix; lead with recall and precision, not accuracy |
| Deep learning / neural network model | Sounds impressive; signals technical sophistication | Adds days of tuning for marginal gain over XGBoost on tabular data; black-box without SHAP integration; not defensible in 1 week | XGBoost with SHAP achieves comparable performance and is fully explainable; baseline logistics regression is always fallback |
| Real-time streaming pipeline | Evokes "production-ready" system | Dataset is historical and batch; building streaming infra is weeks of work with no payoff for this sprint | Frame as "batch scoring at expedição time" — operationally equivalent for the use case |
| Customer segmentation / RFM analysis | Standard DS deliverable; appears thorough | Olist customers have very low repeat purchase rate (most buy once) — RFM analysis produces trivial segments; wastes time and confuses stakeholders | Skip RFM; focus segmentation on seller-level and geo-level aggregations which have operational value |
| Full NLP pipeline on review text (main focus) | Review text seems like rich signal | Text requires preprocessing, vectorization, topic modeling or sentiment — each step takes hours; reviews with 1 star often have no text; Pessoa 5 already owns this as optional enrichment | Use text only as corroboration (e.g., keyword frequency in flagged orders), not as primary ML feature |
| Survival analysis / time-to-review modeling | More statistically rigorous framing of the problem | Complex to explain to mixed audience; adds no actionability over binary classification; PR-AUC/recall framing is already defensible | Binary classification with threshold and operational playbook is clearer and equally valid |
| Interactive dashboard with full filter set | Seems like a polished product | Building a filterable dashboard is scope creep disguised as polish; takes 2–3 days; stakeholders explore it once and forget it | Streamlit demo with a single "order risk score" input is enough; focused demos impress more than exhaustive dashboards |
| Per-product category analysis as primary finding | Seems detailed and thorough | Category-level analysis fragments attention; leadership wants regional/seller patterns they can act on operationally, not product taxonomy insights | Mention category as context, not as primary finding; defer to a post-sprint analysis if interest is shown |
| Hyperparameter tuning grid search | Signals rigor to technical audience | Grid search on XGBoost with 1-week deadline can consume 4–6 hours and yield <1% AUC improvement; delays other deliverables | Use reasonable defaults from community benchmarks on Olist dataset; document rationale; mention in Q&A if asked |

---

## Feature Dependencies

```
[Tabela Gold (joins validados)]
    └──requires──> [EDA Analyses] (all EDA depends on clean gold table)
    └──requires──> [ML Pipeline] (model requires clean feature set from gold table)

[EDA - Atraso vs. Nota]
    └──requires──> [Tabela Gold]
    └──enhances──> [Geographic Heatmap] (both tell Ato 1 story together)

[Geographic Heatmap]
    └──requires──> [Tabela Gold + geolocation join]
    └──enhances──> [Route/Corridor Analysis] (corridor is deeper geographic cut)

[Baseline ML Model (Logistic Regression)]
    └──requires──> [Tabela Gold + pre-expedição feature set]
    └──enables──> [Advanced ML Model (XGBoost)] (baseline must exist before upgrade)

[Advanced ML Model (XGBoost)]
    └──requires──> [Baseline ML Model] (for comparison)
    └──enables──> [SHAP Feature Importance] (Tree SHAP requires tree-based model)
    └──enables──> [Seller-Level Risk Aggregation] (requires model predictions)

[PR Curve + Threshold Decision]
    └──requires──> [Any ML Model with probability output]
    └──enables──> [Operational Impact Estimate / Playbook]

[SHAP Feature Importance]
    └──requires──> [Tree-based model (XGBoost or Random Forest)]
    └──enhances──> [Slides Ato 2] (makes model legible to leadership)

[Streamlit Demo]
    └──requires──> [Trained ML Model + serialized artifact]
    └──conflicts──> [time budget if model pipeline is late] (build only if Fase 3 closes on time)

[NLP Sentiment Enrichment]
    └──requires──> [Baseline EDA complete] (optional layer)
    └──conflicts──> [ML pipeline timeline] (if Pessoa 4 is still tuning, Pessoa 5 blocks)

[Slides Two-Act Narrative]
    └──requires──> [EDA visuals finalized] (Ato 1)
    └──requires──> [Model metrics + SHAP] (Ato 2)
    └──enhances──> [Operational Playbook] (gives Ato 2 a concrete recommendation)
```

### Dependency Notes

- **Tabela Gold requires validation before any downstream analysis:** A data quality error discovered after EDA starts forces rework of all charts. Fase 1 must close before Fase 2 begins — no exceptions.
- **Baseline ML requires pre-expedição feature audit:** The guardrail (no post-delivery features) must be verified at feature engineering time, not after model training. Produce a documented feature list with inclusion/exclusion rationale before fitting any model.
- **SHAP requires tree-based model:** If Pessoa 4 sticks with logistic regression as the final model, SHAP TreeExplainer is unavailable; use LIME or coefficient visualization instead (lower differentiator value).
- **Streamlit demo conflicts with last-day time budget:** If Fase 3 is not closed by day 5, cut the demo. The slides are the non-negotiable deliverable.
- **NLP enrichment conflicts with ML pipeline if both are running simultaneously:** Pessoa 5 should only start NLP after Pessoa 4 has a working baseline and the gold table is locked.

---

## MVP Definition

### Launch With — Presentation Day Minimum (v1)

The absolute minimum to deliver a credible, impactful presentation to leadership.

- [ ] Tabela gold validated (row counts confirmed, null audit passed, temporal range documented) — foundation of everything
- [ ] Atraso vs. nota chart — single most important Ato 1 visual; proves the thesis
- [ ] Frete vs. nota chart — second key Ato 1 driver
- [ ] Geographic heatmap of 1–2 star concentration by UF — gives leadership the "where is the pain" answer
- [ ] Baseline logistic regression model with PR-AUC and recall on test set — guarantees ML deliverable regardless of XGBoost timeline
- [ ] PR curve + threshold decision + "orders we would flag per month" estimate — makes model operational
- [ ] Two-act slide deck (Ato 1: problem evidence, Ato 2: model + playbook) — the actual deliverable leadership receives

### Add After MVP Is Locked (v1.x)

Add these only if the MVP features above are complete and validated.

- [ ] XGBoost model replacing or augmenting baseline — trigger: logistic regression baseline exists and Fase 3 has time remaining
- [ ] SHAP summary plot — trigger: tree-based model is final model
- [ ] Seller-level risk aggregation — trigger: model predictions are generated on full dataset
- [ ] Route/corridor analysis — trigger: geo join is clean and Pessoa 2 has bandwidth

### Future Consideration — Post-Sprint (v2+)

Features to pitch as "next steps" in the final slide, not to build during the sprint.

- [ ] NLP deep-dive on review text — interesting signal, needs dedicated sprint; pitch as next step
- [ ] Real-time scoring API / production pipeline — explicitly out of scope; frame as "productionization roadmap"
- [ ] A/B test for operational playbook — "does intervening on flagged orders actually improve scores?" — requires real intervention data
- [ ] Counterfactual holdout validation (before/after framing) — powerful if model is strong; build only if XGBoost, SHAP, and playbook are all done first

---

## Feature Prioritization Matrix

| Feature | Stakeholder Value | Implementation Cost | Priority |
|---------|-------------------|---------------------|----------|
| Tabela gold validada | HIGH | MEDIUM | P1 |
| Atraso vs. nota chart | HIGH | LOW | P1 |
| Frete vs. nota chart | HIGH | LOW | P1 |
| Geographic heatmap (UF) | HIGH | MEDIUM | P1 |
| Baseline ML model | HIGH | LOW-MEDIUM | P1 |
| PR curve + threshold + impact estimate | HIGH | MEDIUM | P1 |
| Two-act slide deck | HIGH | MEDIUM | P1 |
| XGBoost model | MEDIUM | MEDIUM | P2 |
| SHAP feature importance | HIGH | MEDIUM | P2 |
| Seller-level risk aggregation | HIGH | LOW (post-model) | P2 |
| Route/corridor analysis | MEDIUM | MEDIUM | P2 |
| Operational playbook quantified | HIGH | MEDIUM | P2 |
| Streamlit live demo | HIGH | HIGH | P2 (cut if time at risk) |
| NLP sentiment enrichment | MEDIUM | HIGH | P3 |
| Counterfactual before/after narrative | MEDIUM | HIGH | P3 |
| RFM customer segmentation | LOW | LOW | Do not build |
| Real-time pipeline | LOW | VERY HIGH | Do not build |
| Full filterable dashboard | LOW | HIGH | Do not build |

**Priority key:**
- P1: Must have for presentation day — non-negotiable
- P2: Should have — builds impressiveness; cut last if time runs short
- P3: Nice to have — only if MVP + P2 are locked by day 5

---

## Competitor Feature Analysis

Context: "Competitors" here are other Olist Kaggle analyses and DS challenge presentations the leadership may have seen. The differentiation axis is "ação" (actionability) vs. "exploração" (exploration).

| Feature | Typical Kaggle Olist Analysis | Typical DS Academic Report | Our Approach |
|---------|-------------------------------|---------------------------|--------------|
| Target definition | Varies (1-star only, or 1–3 as "bad") | Often multiclass | Binary 1–2 stars — defensible and operationally clean |
| Evaluation metric | Accuracy or ROC-AUC | F1 or accuracy | PR-AUC + recall + threshold — business-aligned |
| Feature leakage | Often present (actual delivery date used) | Mixed | Zero tolerance — features locked to pre-expedição |
| Explainability | Rarely present | Coefficients only | SHAP TreeExplainer on XGBoost — visual and business-legible |
| Geographic analysis | Occasional map | Rare | Full choropleth + corridor analysis — operationally actionable |
| Business output | "Model achieves 0.82 AUC" | Statistical significance tables | Playbook: "flag these order types, contact proactively, estimated recovery X" |
| Narrative | Technical report | Academic abstract | Two-act storytelling: problem → solution → call to action |

---

## Alignment with Two-Act Narrative

This feature set is explicitly designed around the PROJECT.md narrative structure:

**Ato 1 — "A dor é real e está nos dados"**
- Table stakes features deliver the evidence: atraso, frete, distribuição geográfica
- These are not optional — they ARE the first act
- Missing any of these makes the thesis unsubstantiated

**Ato 2 — "Podemos agir antes que o problema aconteça"**
- Differentiators elevate the solution: SHAP makes the model trustworthy, seller aggregation makes it operational, the playbook makes it a decision (not just a prediction)
- The Streamlit demo, if delivered, makes Ato 2 visceral rather than theoretical

**Anti-features protect the sprint by eliminating the three most common time drains:**
1. Metric confusion (accuracy/ROC-AUC) that destroys credibility with DS-literate reviewers
2. Scope creep (RFM, NLP deep-dive, real-time pipeline) that delays P1 features
3. Complexity theater (deep learning, survival analysis) that impresses no one and delays everything

---

## Sources

- [Brazilian E-Commerce Public Dataset by Olist — Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/) — MEDIUM confidence (community verified, dataset structure confirmed)
- [Case Study: Customer Satisfaction Prediction on Olist Dataset — Towards Data Science, Jan 2025](https://towardsdatascience.com/case-study-1-customer-satisfaction-prediction-on-olist-brazillian-dataset-4289bdd20076/) — MEDIUM confidence (practitioner case study, verified approach)
- [Customer Satisfaction Prediction via Interpretable Models and Sentiment Analysis — SpringerLink ICCCE 2024](https://link.springer.com/chapter/10.1007/978-981-95-0269-1_114) — HIGH confidence (peer reviewed)
- [PR-AUC vs ROC-AUC for imbalanced classification — multiple ML sources, 2025] — HIGH confidence (established statistical practice, consensus across sources)
- [SHAP for executive presentations — SHAP documentation + practitioner sources, 2025] — HIGH confidence (SHAP is industry standard for tree-based model explainability)
- [Data science stakeholder presentation anti-patterns — multiple practitioner sources, 2025] — MEDIUM confidence (practitioner consensus, not empirically measured)
- [Heatmap analytics for geographic logistics distribution — multiple sources, 2025] — MEDIUM confidence (established practice in logistics analytics)
- [EDA best practices for e-commerce customer satisfaction — multiple sources, 2025] — MEDIUM confidence (multiple independent sources agree on core practices)

---

*Feature research for: Olist Challenge — Logística, Satisfação e Risco Pré-Entrega*
*Researched: 2026-03-01*
