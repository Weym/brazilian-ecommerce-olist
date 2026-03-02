# Phase 1: Kickoff e Contratos - Research

**Researched:** 2026-03-01
**Domain:** Data science sprint kickoff — feature contracts, project structure, git hygiene for notebooks
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### Contrato de Features Pre-Entrega
- Formato: arquivo Python `src/features.py` com constante `PRE_DELIVERY_FEATURES` (lista de strings com nomes de colunas permitidas) + `FORBIDDEN_FEATURES` (colunas proibidas por serem pos-entrega)
- Documento legivel complementar: `docs/feature_contract.md` com tabela explícita de cada coluna, sua origem e tag `[pre-entrega | pos-entrega | target]`
- Colunas proibidas incluem obrigatoriamente: `order_delivered_customer_date`, `review_score`, `review_comment_message`, `review_creation_date`, qualquer variavel derivada de entrega real
- O corte temporal usa `order_approved_at` como ancora (nao `order_purchase_timestamp`)

#### Metricas Primarias
- Metrica principal do modelo: **PR-AUC** (Precision-Recall AUC) e **Recall** para a classe positiva (reviews 1-2 estrelas)
- Accuracy e ROC-AUC sao explicitamente proibidos como headline metrics — documentar o motivo (dataset desbalanceado ~15-20% de positivos)
- Limiar de decisao sera escolhido na curva PR, nao a 0.5 padrao
- Baseline: Regressao Logistica com `class_weight='balanced'` como obrigatorio antes de qualquer modelo avancado

#### Target do Modelo
- Target binario: `review_score` in {1, 2} -> positivo (1), `review_score` in {3, 4, 5} -> negativo (0)
- Nome da coluna target na tabela gold: `bad_review` (booleano)
- Rationale documentado: definicao rigorosa e defensavel, separa insatisfacao real de neutros

#### Estrutura do Repositorio
- Convencao de nomes de notebooks: `FASE{N}-PESSOA{N}-descricao.ipynb`
- Estrutura de pastas padronizada:
  ```
  data/raw/          <- CSVs originais da Olist (nunca modificados)
  data/gold/         <- olist_gold.parquet (contrato imutavel)
  notebooks/         <- notebooks por fase/pessoa
  src/               <- modulos Python reutilizaveis (features.py, utils.py)
  models/            <- artefatos serializados (.joblib)
  reports/figures/   <- imagens exportadas para slides
  app/               <- codigo Streamlit
  docs/              <- documentacao (feature_contract.md, data_dictionary.md)
  ```
- Regras de git: notebooks devem ter outputs limpos antes de commit (usar `nbstripout` ou convencao manual); sem paths hardcoded (usar `pathlib.Path(__file__).parent`)

#### Recorte Temporal e Outliers
- Janela de dados: usar todos os pedidos com `order_approved_at` disponivel
- Pedidos excluidos: status `canceled`, `unavailable`
- Outlier de frete: nao remover, mas flaggar pedidos com frete > 3 desvios-padrao
- Outlier de prazo: pedidos com atraso > 30 dias incluidos na EDA, podem ser tratados separadamente no ML

#### Ownership de Notebooks
| Pessoa | Area | Notebooks |
|--------|------|-----------|
| P1 — Data Lead | Data Foundation | FASE2-P1-*.ipynb |
| P2 — Geo/Logística | Geo Analysis | FASE3-P2-*.ipynb |
| P3 — EDA & Metricas | EDA | FASE3-P3-*.ipynb |
| P4 — ML Lead | ML Pipeline | FASE4-P4-*.ipynb |
| P5 — NLP/Reviews | Reviews NLP | FASE3-P5-*.ipynb (opcional) |
| P6 — Storytelling | Apresentacao | Coordena deck e app/ |

### Claude's Discretion
- Formato exato do `requirements.txt` / `pyproject.toml` — usar o que o time ja conhece
- Ferramenta de limpeza de outputs de notebooks (nbstripout vs hook manual vs convencao)
- Template de notebook inicial (importacoes padrao, configuracoes de display)

### Deferred Ideas (OUT OF SCOPE)
- Nenhuma — discussao ficou dentro do escopo da Fase 1
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| KICK-01 | Time define e documenta o "contrato de features pre-entrega" — lista explícita de colunas permitidas e proibidas no modelo ML | `src/features.py` allow-list pattern + `docs/feature_contract.md` template documented in Architecture Patterns |
| KICK-02 | Time acorda as metricas primarias do modelo (PR-AUC e Recall para classe positiva) antes de qualquer codigo | Metrics rationale documented in Code Examples — why PR-AUC over ROC-AUC under class imbalance |
| KICK-03 | Time define ownership de notebooks (convencao de nomes, estrutura de pastas, regras de git) | Cookiecutter DS v2 structure + nbstripout installation pattern documented |
| KICK-04 | Time define o target do modelo: avaliacao ruim = estrelas 1–2 | Target definition documented in Code Examples with `bad_review` binary column derivation |
| KICK-05 | Time define o recorte temporal e regras de outlier antes da construcao da tabela gold | Temporal anchor (`order_approved_at`), exclusion rules, and outlier policy documented in Architecture Patterns |
</phase_requirements>

---

## Summary

Phase 1 is a documentation-and-agreement phase — no data processing or model code is written. Its sole purpose is to prevent the four most common sprint-killing mistakes before any line of analysis code is written: post-delivery data leakage, accuracy metric trap on imbalanced data, notebook chaos from undisciplined git commits, and conflicting assumptions about the target variable. All five KICK requirements are fulfilled by creating two code files (`src/features.py`, `src/__init__.py`) and four documentation files (`docs/feature_contract.md`, `docs/metrics_agreement.md`, `docs/data_dictionary.md`, the repo `README.md`), plus setting up the project folder structure and git hygiene tooling.

The `src/features.py` allow-list pattern is the critical anchor. It is the single source of truth for which columns are permitted in any model feature matrix. Both the Phase 4 ML training notebook and the Phase 5 Streamlit app import from it, guaranteeing that whatever the model was trained on is also what the demo uses at inference time. The document `docs/feature_contract.md` is the human-readable companion — a table every team member must be able to read and reason about before writing a single join.

The nbstripout git filter (not pre-commit hook mode) is the recommended approach for notebook hygiene: it modifies only what git sees, not the working copy, so analysts can keep their outputs locally while the repository stays clean. This requires each contributor to run `nbstripout --install --attributes .gitattributes` once after cloning, and the `.gitattributes` file is committed to the repo.

**Primary recommendation:** Create the folder skeleton, `src/features.py` with the two allow-list constants, and `docs/feature_contract.md` with the full column table — these three artifacts are the non-negotiable deliverables of Phase 1, and everything in Phase 2 through 5 depends on them being correct.

---

## Standard Stack

### Core (for Phase 1 artifacts only)

| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| Python | 3.11.x | Language base for `src/features.py` | Stable, max library support; avoid 3.13 |
| pathlib | stdlib | Path handling without hardcoding | Zero dependencies, OS-agnostic |
| nbstripout | 0.9.1 | Strip Jupyter output before git commit | Industry standard; git filter mode leaves working copy intact |

### Supporting (git hygiene)

| Tool | Version | Purpose | When to Use |
|------|---------|---------|-------------|
| pre-commit | 3.x | Framework to manage git hooks | Use if team wants automated enforcement beyond nbstripout |
| nb-clean | 4.0.1 | Alternative to nbstripout — also cleans execution counts and metadata | Use if nbstripout alone is insufficient or pre-commit is already adopted |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| nbstripout (git filter) | nbstripout (pre-commit hook) | Pre-commit hook mode modifies working copy — analysts lose their local outputs. Filter mode is less invasive |
| nbstripout | Manual convention ("clear all before commit") | Manual convention has zero enforcement and will fail under sprint pressure |
| requirements.txt | pyproject.toml | requirements.txt is faster for a 1-week sprint; pyproject.toml is more modern but requires tooling familiarity. Use whatever the team already knows (locked as Claude's discretion) |

**Installation (per contributor, run once after cloning):**
```bash
pip install nbstripout
nbstripout --install --attributes .gitattributes
```

**Verify installation:**
```bash
nbstripout --status
```

---

## Architecture Patterns

### Recommended Project Structure

This is the locked structure from CONTEXT.md, aligned with Cookiecutter Data Science v2 conventions:

```
olist-project/
├── data/
│   ├── raw/           # 9 Olist CSVs — immutable, never modified after ingest
│   ├── gold/          # olist_gold.parquet — interface contract for all phases
│   └── processed/     # intermediate aggregations (geo_aggregated.parquet, etc.)
├── notebooks/         # per-phase, per-person notebooks
│   # naming: FASE{N}-P{N}-descricao.ipynb
│   # e.g.: FASE2-P1-data-foundation.ipynb
├── src/               # reusable Python modules
│   ├── __init__.py
│   ├── features.py    # PRE_DELIVERY_FEATURES + FORBIDDEN_FEATURES (THE allow-list)
│   └── utils.py       # helper functions (created in later phases as needed)
├── models/            # serialized artifacts — .joblib files
├── reports/
│   └── figures/       # exported PNGs for slide deck
├── app/               # Streamlit pages (Phase 5+)
├── docs/
│   ├── feature_contract.md   # human-readable column table (Phase 1 deliverable)
│   ├── metrics_agreement.md  # PR-AUC rationale + threshold policy (Phase 1 deliverable)
│   └── data_dictionary.md    # all gold table columns defined (Phase 2 deliverable)
├── .gitattributes     # nbstripout filter registration
├── requirements.txt   # pinned dependencies
└── README.md          # project overview + how to reproduce
```

**Cookiecutter DS v2 alignment:**
- `data/raw/` = "original, immutable data dump" (official CCDS term)
- `data/gold/` maps to CCDS `data/processed/` but renamed to signal immutability
- `src/features.py` directly mirrors the CCDS `{{ module_name }}/features.py` convention
- `models/` and `reports/figures/` are CCDS-standard paths
- CCDS v2 is available at pypi as `cookiecutter-data-science` v2.3.0 — the project can optionally bootstrap from it, but manual creation is equally valid for this sprint

### Pattern 1: Feature Allow-List in `src/features.py`

**What:** A Python module with two module-level constants defining exactly which columns are permitted in the feature matrix and which are forbidden. Downstream code imports from this single source of truth.

**When to use:** Always — in both the ML training notebook and the Streamlit inference app. If a column is not in `PRE_DELIVERY_FEATURES`, it cannot appear in `X`.

**Example:**
```python
# src/features.py
# Source: project-specific, pattern verified against CCDS v2 conventions
# and sklearn leakage-prevention documentation

"""
Feature contract for the Olist pre-delivery risk model.

TEMPORAL ANCHOR: order_approved_at
All features in PRE_DELIVERY_FEATURES are available at the moment
the order is approved for shipment. No post-delivery information
is permitted in the feature matrix.

This file is imported by:
  - notebooks/FASE4-P4-ml-pipeline.ipynb (training)
  - app/pages/03_modelo.py (inference)
"""

from pathlib import Path

# Columns permitted as model inputs.
# These are knowable at the time of order approval (pre-delivery).
PRE_DELIVERY_FEATURES: list[str] = [
    # Freight and price
    "freight_value",
    "price",
    "freight_ratio",          # freight_value / price, engineered
    # Logistics time estimates
    "estimated_delivery_days",  # difference: estimated_date - approval_date
    # Seller geography
    "seller_state",
    "customer_state",
    "seller_customer_distance_km",  # Haversine, computed in Phase 2
    # Product characteristics
    "product_weight_g",
    "product_volume_cm3",       # length * width * height, engineered
    "product_category_name_english",
    # Order composition
    "order_item_count",
    "payment_type",
    "payment_installments",
]

# Columns that MUST NEVER appear in the feature matrix.
# These are only available after delivery or after the review event.
FORBIDDEN_FEATURES: list[str] = [
    "order_delivered_customer_date",   # post-delivery
    "review_score",                    # the target itself / post-delivery
    "review_comment_message",          # post-delivery review text
    "review_creation_date",            # post-delivery
    "review_answer_timestamp",         # post-delivery
    "order_delivered_carrier_date",    # partially post-approval but unreliable
]

# Target column name in the gold table.
TARGET_COLUMN: str = "bad_review"
# bad_review = 1 if review_score in {1, 2}, else 0
```

### Pattern 2: Feature Contract Document (`docs/feature_contract.md`)

**What:** A human-readable Markdown table with every gold table column, its source CSV, its derivation (if engineered), and its tag.

**When to use:** This document is the reference that every team member consults when writing a join, computing a feature, or preparing a slide. It is the enforcement mechanism for KICK-01.

**Example structure:**
```markdown
# Feature Contract — Olist Pre-Delivery Risk Model

**Temporal anchor:** `order_approved_at`
**Target:** `bad_review` = 1 if `review_score` in {1, 2}
**Model input rule:** Only columns tagged `[pre-entrega]` may appear in the feature matrix.

## Column Table

| Column | Source | Derivation | Tag | Notes |
|--------|--------|------------|-----|-------|
| order_id | orders.csv | raw | [join-key] | |
| order_approved_at | orders.csv | raw | [temporal-anchor] | Cutoff date for features |
| bad_review | order_reviews.csv | review_score in {1,2} → 1, else 0 | [target] | |
| freight_value | order_items.csv | sum per order | [pre-entrega] | |
| price | order_items.csv | sum per order | [pre-entrega] | |
| freight_ratio | engineered | freight_value / price | [pre-entrega] | |
| estimated_delivery_days | orders.csv | order_estimated_delivery_date - order_approved_at | [pre-entrega] | |
| seller_state | sellers.csv | raw | [pre-entrega] | |
| customer_state | customers.csv | raw | [pre-entrega] | |
| seller_customer_distance_km | geolocation.csv | Haversine(seller_zip, customer_zip) | [pre-entrega] | Phase 2 |
| product_weight_g | products.csv | raw | [pre-entrega] | |
| product_volume_cm3 | products.csv | length*width*height | [pre-entrega] | |
| product_category_name_english | category_translation.csv | join | [pre-entrega] | |
| order_item_count | order_items.csv | count per order_id | [pre-entrega] | |
| payment_type | order_payments.csv | mode per order | [pre-entrega] | |
| payment_installments | order_payments.csv | sum per order | [pre-entrega] | |
| order_delivered_customer_date | orders.csv | raw | [pos-entrega] | FORBIDDEN in features |
| review_score | order_reviews.csv | raw | [pos-entrega] | Used only to derive target |
| review_comment_message | order_reviews.csv | raw | [pos-entrega] | FORBIDDEN — NLP optional |
| review_creation_date | order_reviews.csv | raw | [pos-entrega] | FORBIDDEN |
```

### Pattern 3: Metrics Agreement Document (`docs/metrics_agreement.md`)

**What:** A one-page document that records the metric decisions for KICK-02 — why PR-AUC and Recall, why not accuracy or ROC-AUC, and the threshold policy.

**When to use:** Referenced by Phase 4 ML notebook when reporting results. Prevents metric drift under sprint pressure.

**Key content to include:**
- Class distribution estimate (~15-20% positive = bad_review=1)
- Why accuracy fails: a naive "always 0" classifier achieves 80-85% accuracy
- Why ROC-AUC is insufficient: insensitive to class imbalance; high AUC can coexist with poor recall
- Why PR-AUC is appropriate: directly measures precision/recall tradeoff on the minority class
- Threshold policy: chosen from PR curve to maximize operational value, NOT 0.5 default
- Baseline requirement: Logistic Regression with `class_weight='balanced'` MUST run first

### Anti-Patterns to Avoid

- **Hardcoded column lists in notebooks:** If `PRE_DELIVERY_FEATURES` is redefined in multiple notebooks, they will drift. Import from `src/features.py` only.
- **Committing `src/features.py` without documentation update:** The Python file and `docs/feature_contract.md` must be kept in sync — if a column is added to one, add it to both.
- **Using `order_purchase_timestamp` as temporal anchor:** Decision is locked to `order_approved_at`. Using purchase timestamp would include orders where approval was delayed, creating ambiguity.
- **Pre-commit hook mode for nbstripout:** Modifies the working copy, causing analysts to lose their local outputs on every commit. Use git filter mode (`nbstripout --install --attributes .gitattributes`) instead.
- **Skipping `README.md`:** The README is the first thing a new team member reads. Phase 1 must produce at least a skeleton with dataset download instructions and "how to reproduce" steps.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Notebook output stripping | Custom bash script that deletes outputs | `nbstripout` git filter | nbstripout handles edge cases (metadata, execution counts, timestamps) and integrates with git natively |
| Path management | Hardcoded absolute paths like `/home/user/olist/data/` | `pathlib.Path(__file__).parent.parent / "data"` | Relative pathlib paths work on any machine without configuration |
| Project scaffold | Manually creating all directories with `mkdir` | Either use `ccds` (Cookiecutter DS v2) or a single setup script | Missing `__init__.py` in `src/` will break `from src.features import PRE_DELIVERY_FEATURES` |
| Column documentation | Ad-hoc comments in notebooks | `docs/feature_contract.md` as the canonical table | Comments get deleted, refactored, ignored under sprint pressure |

**Key insight:** Phase 1 has very little tooling complexity. The main risk is social, not technical: team members skipping the agreements and jumping straight to code. The artifacts produced here (especially `src/features.py` and `docs/feature_contract.md`) are enforcement mechanisms, not just documentation.

---

## Common Pitfalls

### Pitfall 1: The `src/` Package Not Importable

**What goes wrong:** `from src.features import PRE_DELIVERY_FEATURES` raises `ModuleNotFoundError` in notebooks.

**Why it happens:** `src/` directory exists but `src/__init__.py` was not created. Python 3 does not treat a directory as a package without `__init__.py` (or the project root is not in `sys.path`).

**How to avoid:** Create `src/__init__.py` (can be empty) as part of Phase 1 folder setup. Add a cell at the top of every notebook:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd().parent))  # add project root to path
```
Or better: install the project in editable mode with `pip install -e .` so import works from anywhere.

**Warning signs:** First time someone writes `from src.features import ...` and gets an error.

### Pitfall 2: Feature Contract Drift Between `src/features.py` and `docs/feature_contract.md`

**What goes wrong:** A column is added to `PRE_DELIVERY_FEATURES` in the Python file but not added to the Markdown table (or vice versa). The document becomes stale and loses trust.

**Why it happens:** No enforced single source of truth. Two files, both updated manually.

**How to avoid:** In Phase 1, keep the list short and stable. Add a comment in `src/features.py` that explicitly says "if you add a column here, add a row to docs/feature_contract.md." For long-term projects, the feature list would be generated from the Markdown table — but for a 1-week sprint, a comment and discipline suffice.

**Warning signs:** PR-AUC discussion references a column name that doesn't appear in `feature_contract.md`.

### Pitfall 3: nbstripout Not Installed by All Contributors

**What goes wrong:** One team member commits a notebook with outputs (images, dataframes, tracebacks) embedded. The repo grows by megabytes per commit, and diff reviews become unreadable.

**Why it happens:** `.gitattributes` registers the filter but cannot install the tool — each contributor must run `nbstripout --install` locally. One person forgets.

**How to avoid:** Add to `README.md` under "Setup":
```
After cloning:
pip install nbstripout
nbstripout --install --attributes .gitattributes
```
Also add: "Verify with `nbstripout --status`." Consider adding a CI check (GitHub Action) that fails if any committed `.ipynb` contains outputs — this catches misses at review time.

**Warning signs:** `git diff` on a `.ipynb` file shows lines like `"output_type": "display_data"`.

### Pitfall 4: Ownership Table Not Operationalized

**What goes wrong:** The ownership table in CONTEXT.md exists as a document but doesn't prevent two people from writing to the same notebook. Merge conflicts on `.ipynb` files are notoriously difficult to resolve.

**Why it happens:** Convention without enforcement. Sprint pressure causes people to work where it's convenient.

**How to avoid:** The folder structure `notebooks/FASE{N}-P{N}-` makes ownership visible in the filename. Each person creates their own notebook file in Phase 1 as a placeholder (even just the import cell). This establishes the files early so git tracks them as separate.

**Warning signs:** Two contributors have modified the same `.ipynb` and the merge shows JSON conflicts.

### Pitfall 5: Using `order_purchase_timestamp` Instead of `order_approved_at` as Feature Anchor

**What goes wrong:** Features like `estimated_delivery_days` are calculated as `estimated_date - purchase_date` instead of `estimated_date - approval_date`. The difference is subtle but meaningful: for orders where approval was delayed, using purchase timestamp overstates the estimated window.

**Why it happens:** `order_purchase_timestamp` is the first date field encountered in the orders table and is used by default without checking the locked decision.

**How to avoid:** The `docs/feature_contract.md` must explicitly call out `order_approved_at` as the temporal anchor in a prominent header. Add a comment in `src/features.py` at the top level: `# TEMPORAL ANCHOR: order_approved_at`.

**Warning signs:** `estimated_delivery_days` feature has a different distribution than expected (some negative values, or values > 60 days frequently).

---

## Code Examples

### `src/__init__.py` (empty, but required)

```python
# src/__init__.py
# Makes src/ a Python package — required for: from src.features import PRE_DELIVERY_FEATURES
```

### `src/features.py` (complete Phase 1 version)

```python
# src/features.py
# Source: project decision (CONTEXT.md) + Cookiecutter DS v2 features.py convention
"""
Feature contract for the Olist pre-delivery risk model.

TEMPORAL ANCHOR: order_approved_at
Every feature in PRE_DELIVERY_FEATURES must be knowable at the time
the order is approved for shipment — no information from after delivery
or after the review event may appear in the feature matrix.

Imported by:
  - notebooks/FASE4-P4-ml-pipeline.ipynb  (model training)
  - app/pages/03_modelo.py                 (live inference)

If you add a column to PRE_DELIVERY_FEATURES, also add a row to:
  docs/feature_contract.md
"""

# Permitted model inputs (pre-delivery only)
PRE_DELIVERY_FEATURES: list[str] = [
    "freight_value",
    "price",
    "freight_ratio",
    "estimated_delivery_days",
    "seller_state",
    "customer_state",
    "seller_customer_distance_km",
    "product_weight_g",
    "product_volume_cm3",
    "product_category_name_english",
    "order_item_count",
    "payment_type",
    "payment_installments",
]

# Forbidden columns — must NEVER appear in X (feature matrix)
FORBIDDEN_FEATURES: list[str] = [
    "order_delivered_customer_date",
    "review_score",
    "review_comment_message",
    "review_creation_date",
    "review_answer_timestamp",
    "order_delivered_carrier_date",
]

# Target column in the gold table
TARGET_COLUMN: str = "bad_review"
# bad_review definition: (review_score == 1) | (review_score == 2) -> 1, else -> 0
```

### Target derivation (for reference in `docs/feature_contract.md`)

```python
# This runs in Phase 2 (data foundation), documented here for clarity
# Source: CONTEXT.md locked decision KICK-04

df["bad_review"] = df["review_score"].isin([1, 2]).astype(int)
```

### Notebook standard header (template cell for all notebooks)

```python
# Standard imports — paste into first cell of every notebook
import sys
from pathlib import Path

# Add project root to path so `from src.features import ...` works
PROJECT_ROOT = Path.cwd().parent  # adjust depth if notebook is nested
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Project-specific imports
from src.features import PRE_DELIVERY_FEATURES, FORBIDDEN_FEATURES, TARGET_COLUMN

# Display settings
pd.set_option("display.max_columns", 50)
pd.set_option("display.float_format", "{:.4f}".format)
%matplotlib inline

# Data paths (pathlib — no hardcoded strings)
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_GOLD = PROJECT_ROOT / "data" / "gold"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
```

### `.gitattributes` content (after running `nbstripout --install --attributes .gitattributes`)

```
# .gitattributes
# nbstripout git filter — strips Jupyter output before git sees the file.
# Working copy is NOT modified. Each contributor must run:
#   pip install nbstripout && nbstripout --install --attributes .gitattributes
*.ipynb filter=nbstripout
*.ipynb diff=ipynb
```

### Metrics agreement summary (content for `docs/metrics_agreement.md`)

```markdown
# Metrics Agreement — Olist Pre-Delivery Risk Model

## Decision

Primary metrics: **PR-AUC** and **Recall (class=1)**
Forbidden headline metrics: Accuracy, ROC-AUC

## Rationale

| Metric | Why Forbidden |
|--------|--------------|
| Accuracy | Dataset is ~80-85% negative (bad_review=0). A classifier predicting "always good" achieves 80-85% accuracy with zero predictive value. |
| ROC-AUC | Insensitive to class imbalance. A model with high ROC-AUC can still have very poor recall on the minority class. |

## Class Distribution (estimated)
- Negative (good review, 3-5 stars): ~80-85% of orders
- Positive (bad review, 1-2 stars): ~15-20% of orders
- Verify actual proportion during Phase 2 gold table build.

## Threshold Policy
- Default threshold (0.5) is NOT used.
- Threshold selected from the PR curve during Phase 4, maximizing F1 or
  chosen based on operational impact (orders flagged per week vs. precision).

## Baseline Requirement
- Logistic Regression with `class_weight='balanced'` MUST run and be evaluated
  before any advanced model (XGBoost, etc.) is trained.
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|-----------------|--------------|--------|
| Manual "clear outputs" before commit | `nbstripout` git filter | ~2015, mainstream by 2020 | Automated, working copy intact, enforced by `.gitattributes` |
| `requirements.txt` only | `requirements.txt` + `pyproject.toml` | PEP 621, ~2021 | For a 1-week sprint, `requirements.txt` remains practical; `pyproject.toml` is the long-term standard |
| Ad-hoc notebook naming | Cookiecutter DS v2 convention (number + author + description) | CCDS v2, 2023 | Encodes phase, person, and topic in filename — zero-ambiguity ownership |
| Inline feature lists in notebooks | `src/features.py` module-level constants | Established MLOps practice | Single source of truth prevents training/inference skew |
| CCDS `cookiecutter` CLI | `ccds` CLI (new package: `cookiecutter-data-science` v2.3.0) | CCDS v2 release | Provides branching logic and better UX; plain `cookiecutter` still works for v1 |

**Deprecated/outdated:**
- `nbstripout` pre-commit hook mode: still valid but modifies working copy — prefer git filter mode for data science teams that want local outputs preserved
- `cookiecutter` (original package) for CCDS v2: replaced by `ccds` command from `cookiecutter-data-science` package — use `pip install cookiecutter-data-science` or `pipx install cookiecutter-data-science`

---

## Open Questions

1. **Exact class distribution of `bad_review=1` in the Olist dataset**
   - What we know: estimated 15-20% positive rate from project research
   - What's unclear: actual proportion — affects `scale_pos_weight` for XGBoost in Phase 4
   - Recommendation: first cell in Phase 2 gold build notebook should print `df["bad_review"].value_counts(normalize=True)` and record the result

2. **Engineered feature list completeness**
   - What we know: `PRE_DELIVERY_FEATURES` list above covers the main drivers identified in project research
   - What's unclear: whether `seller_customer_distance_km` will be ready in Phase 1 or only after Phase 2 Haversine computation
   - Recommendation: include `seller_customer_distance_km` in `PRE_DELIVERY_FEATURES` now with a comment noting it is "computed in Phase 2 — not available until gold table is built"; Phase 4 will raise a clear error if it tries to use the column before Phase 2 completes

3. **Whether the team already has `pre-commit` installed**
   - What we know: Claude's discretion on tooling choice
   - What's unclear: team familiarity with pre-commit framework
   - Recommendation: start with the simpler git filter approach (`nbstripout --install --attributes .gitattributes`) — no additional dependencies beyond nbstripout itself; upgrade to pre-commit if the team wants broader hook management in later phases

---

## Sources

### Primary (HIGH confidence)
- Cookiecutter Data Science v2 official documentation — https://cookiecutter-data-science.drivendata.org/ — folder structure, `features.py` convention, notebook naming
- nbstripout official README — https://github.com/kynan/nbstripout — git filter vs pre-commit hook mode, `.gitattributes` per-repo setup, `--status` command
- `.planning/research/SUMMARY.md` (project research, 2026-03-01) — stack decisions, critical pitfalls, architecture patterns
- `.planning/phases/01-kickoff-e-contratos/01-CONTEXT.md` — all locked decisions

### Secondary (MEDIUM confidence)
- WebSearch: nbstripout 0.9.1 pre-commit hook configuration — `.pre-commit-config.yaml` snippet verified against official nbstripout GitHub
- WebSearch: Cookiecutter DS v2 PyPI release v2.3.0 — verified via pypi.org reference in search results
- WebSearch: pyproject.toml vs requirements.txt 2025 — multiple consistent sources; recommendation for 1-week sprint is `requirements.txt` (pragmatic), consistent with CONTEXT.md "Claude's discretion"

### Tertiary (LOW confidence, validate during execution)
- nb-clean 4.0.1 as nbstripout alternative — mentioned in search results, not verified via official docs; only use if nbstripout causes issues
- LeakageDetector VS Code extension (2025) — WebSearch only; not relevant for Phase 1 (documentation phase), flagged as FYI

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — nbstripout is well-documented with official GitHub; CCDS v2 has official docs verified via WebFetch; all locked decisions come from CONTEXT.md
- Architecture patterns: HIGH — `src/features.py` allow-list pattern is standard MLOps practice, verified against CCDS v2 convention; folder structure is locked in CONTEXT.md
- Pitfalls: HIGH (importability, nbstripout installation, temporal anchor) / MEDIUM (drift between Python file and Markdown table — social/process risk, hard to verify technically)

**Research date:** 2026-03-01
**Valid until:** 2026-04-01 (nbstripout and CCDS are stable; 30-day validity applies)
