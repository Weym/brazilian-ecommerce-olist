# Phase 4: ML — Ato 2 - Research

**Researched:** 2026-03-01
**Domain:** Tabular binary classification — sklearn Pipeline, XGBoost, SHAP, imbalanced-class handling, PR curve threshold selection, seller risk aggregation, joblib serialization
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Balanceamento de classes**
- `class_weight='balanced'` em ambos os modelos: LogisticRegression e XGBoost
- Sem SMOTE — sprint de 1 semana, sem tempo para debugar dados sintéticos
- SHAP funciona normalmente com `class_weight`

**Critério do limiar de decisão (ML-05)**
- Cortar a curva PR no ponto onde **Precision >= 0.40** (critério primário)
- Conferir que Recall >= 0.60 no ponto escolhido (critério secundário)
- Estimativa operacional calculada no threshold escolhido: pedidos flagrados/semana e % real de risco entre os flagrados
- Narrativa para o slide: "40% dos pedidos flagrados são de fato risco real"

**Agregação por vendedor (ML-06)**
- Score médio de risco por vendedor, ordenado maior → menor
- Mínimo de **10 pedidos** para entrar na tabela (vendedores com menos têm scores instáveis)
- Exibir **top-20 vendedores** no slide — cabe numa tabela de apresentação
- Coluna de referência: contagem de pedidos do vendedor (contexto de volume)

**Estrutura do notebook ML**
- Um único notebook: `FASE4-P4-ml-pipeline.ipynb`
- Seções marcadas internamente: (1) Load & feature matrix, (2) Baseline LogReg, (3) XGBoost, (4) SHAP, (5) Threshold + operational estimate, (6) Seller table, (7) Serialize .joblib
- Mais fácil de reproduzir de ponta a ponta e de apresentar como trilha técnica auditável

### Claude's Discretion

- Hiperparâmetros do XGBoost (n_estimators, max_depth, learning_rate) — defaults razoáveis, sem GridSearchCV extenso
- Pipeline sklearn interno: ColumnTransformer com OneHotEncoder para categóricas + StandardScaler para numéricas, depois o estimador
- Divisão treino/test: 80/20 estratificado por `bad_review`
- Formato do SHAP beeswarm: test set, top-15 features, salvo em `reports/figures/shap_beeswarm.png`
- Calibração de probabilidades: não (scores brutos são suficientes para ranking de vendedores)

### Deferred Ideas (OUT OF SCOPE)

- Nenhuma ideia de escopo adicional surgiu — discussão ficou dentro da fronteira da fase
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| ML-01 | Pipeline de features com apenas variáveis disponíveis até o momento de expedição (sem vazamento) | `PRE_DELIVERY_FEATURES` já definida em `src/features.py` (Phase 1); sklearn Pipeline encapsula transformações — fits apenas em X_train |
| ML-02 | Baseline logístico treinado e avaliado com PR-AUC e Recall (obrigatório antes de modelos complexos) | `LogisticRegression(class_weight='balanced')` dentro de `Pipeline`; `average_precision_score` do sklearn para PR-AUC; `classification_report` para Recall |
| ML-03 | Modelo XGBoost treinado com as mesmas features pré-entrega | `XGBClassifier(scale_pos_weight=ratio, eval_metric='aucpr')` dentro do mesmo Pipeline sklearn; mesmas transformações de pré-processamento |
| ML-04 | SHAP values calculados para explicar as features mais importantes do modelo XGBoost | `shap.TreeExplainer(model)` + `shap.summary_plot(shap_values, X_test_transformed, plot_type='dot')` — salvo como PNG |
| ML-05 | Limiar de decisão definido com impacto operacional estimado (pedidos flagrados/semana, % real de risco) | `precision_recall_curve` do sklearn + busca pelo índice onde Precision >= 0.40; estimativa operacional via proporção semanal do test set |
| ML-06 | Agregação de score de risco médio por vendedor (operacionalmente acionável) | `pipeline.predict_proba(X)[:, 1]` no dataset completo → `groupby('seller_id').agg(score_medio_risco=('risk_score','mean'), total_pedidos=('order_id','count'), pedidos_alto_risco=...)` com filtro `total_pedidos >= 10` |
| ML-07 | Pipeline sklearn serializado como `.joblib` para uso na demo Streamlit sem reprocessamento ao vivo | `joblib.dump(pipeline, 'models/final_pipeline.joblib')` — inclui ColumnTransformer + estimador numa única chamada |
</phase_requirements>

---

## Summary

Phase 4 implementa o pipeline completo de risco pré-entrega em um único notebook (`FASE4-P4-ml-pipeline.ipynb`), cobrindo: construção da feature matrix com a allow-list `PRE_DELIVERY_FEATURES`, baseline logístico com PR-AUC e Recall reportados, XGBoost com mesmas features, análise SHAP para explicabilidade, seleção de threshold na curva PR (Precision >= 0.40) com estimativa operacional, tabela de vendedores de alto risco, e serialização de dois artefatos joblib consumidos pela Phase 6 (Streamlit).

O padrão central é o `sklearn.Pipeline` com `ColumnTransformer`: todas as transformações de pré-processamento (OneHotEncoder para categóricas, StandardScaler para numéricas) são encapsuladas no pipeline e fitted **exclusivamente em X_train** — prevenindo o principal pitfall da fase (leakage de estatísticas do test set). O mesmo pipeline serializado é carregado pelo Streamlit sem reconstruir transformações. A chave da fase é que `baseline_logreg.joblib` e `final_pipeline.joblib` são artefatos distintos — o baseline existe como prova de entregável mínimo; o XGBoost é o modelo final com PR-AUC superior.

A âncora temporal `order_approved_at` e a lista `PRE_DELIVERY_FEATURES` já foram definidas na Phase 1 como contratos imutáveis — esta fase apenas os consome via `from src.features import PRE_DELIVERY_FEATURES`. A métrica primária (PR-AUC, não ROC-AUC, não accuracy) também foi acordada na Phase 1. A classe positiva (~15-20% do dataset) justifica `class_weight='balanced'` e torna PR-AUC a métrica correta: um modelo que prevê "sempre negativo" atingiria 80-85% de accuracy mas PR-AUC próximo de zero.

**Primary recommendation:** Construir o notebook em seções lineares sequenciais (Load → Baseline → XGBoost → SHAP → Threshold → Seller table → Serialize), garantindo que cada seção pode ser executada de forma reprodutível do início ao fim em uma única run, sem dependências ocultas entre células.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| scikit-learn | >=1.4,<2.0 | Pipeline, ColumnTransformer, LogisticRegression, métricas PR | API estável, Pipeline previne leakage por design, `average_precision_score` é PR-AUC nativo |
| XGBoost | >=2.0,<3.0 | Classificador principal com `scale_pos_weight` | Melhor AUC em dados tabulares desbalanceados, API sklearn nativa (fit/predict_proba) |
| shap | >=0.44,<1.0 | TreeExplainer para XGBoost + summary_plot beeswarm | Único padrão aceito para explicabilidade de modelos em apresentações executivas |
| joblib | >=1.3,<2.0 | Serialização de pipelines sklearn | Padrão do projeto (já em requirements.txt), suporte nativo a objetos sklearn |
| pandas | >=2.0,<3.0 | Manipulação da feature matrix, groupby para tabela de vendedores | Base do projeto — gold table já em parquet |
| matplotlib | >=3.8,<4.0 | Curva PR, SHAP beeswarm (via plt.savefig) | Backend do shap.summary_plot; necessário para salvar PNG |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| numpy | >=1.26,<2.0 | Array de thresholds, cálculo de índice na curva PR | Indireto via sklearn/shap — já presente |
| pyarrow | >=14.0,<16.0 | `pd.read_parquet('data/gold/olist_gold.parquet')` | Leitura da gold table — já em requirements.txt |
| seaborn | >=0.13,<1.0 | Confusion matrix heatmap (opcional) | Se quiser visualizar matriz de confusão além do `classification_report` |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `class_weight='balanced'` | SMOTE (imbalanced-learn) | SMOTE gera dados sintéticos que podem criar artefatos; `class_weight` é determinístico e sem debugging; LOCKED |
| XGBoost nativo (não sklearn API) | LightGBM | LightGBM é marginalmente mais rápido mas exigiria adaptar o Pipeline; XGBoost API sklearn é documentada e familiar |
| joblib.dump | pickle | joblib é otimizado para arrays numpy grandes; pickle padrão é menos eficiente; joblib já é padrão do projeto |
| `shap.TreeExplainer` | `shap.Explainer` (auto) | TreeExplainer é específico para árvores e ~10x mais rápido; SHAP auto pode escolher errado |
| `average_precision_score` (sklearn) | `roc_auc_score` | PR-AUC é a métrica acordada (KICK-02); ROC-AUC é enganoso com classes desbalanceadas; LOCKED |

**Installation:**
```bash
pip install scikit-learn>=1.4 xgboost>=2.0 shap>=0.44 joblib>=1.3 pandas>=2.0 matplotlib>=3.8
# Todos já em requirements.txt — sem instalações adicionais
```

---

## Architecture Patterns

### Recommended Project Structure (Phase 4 outputs)

```
notebooks/
└── FASE4-P4-ml-pipeline.ipynb   # Notebook único (7 seções internas)

src/
└── features.py                  # PRE_DELIVERY_FEATURES — importar, não editar

models/
├── baseline_logreg.joblib       # Pipeline LogReg serializado (ML-02, ML-07)
└── final_pipeline.joblib        # Pipeline XGBoost serializado (ML-03, ML-07)

reports/figures/
├── shap_beeswarm.png            # Top-15 features, test set (ML-04)
└── pr_curve.png                 # Curva PR com threshold marcado (ML-05)
```

### Pattern 1: sklearn Pipeline com ColumnTransformer (Anti-Leakage)

**What:** Todo pré-processamento (scaling, encoding) encapsulado dentro de um objeto Pipeline — fitted apenas em X_train e aplicado a X_test sem recalcular estatísticas.
**When to use:** Sempre que houver transformações que dependem de estatísticas dos dados (mean, std, categorias únicas).

```python
# Source: sklearn official docs — Pipeline.fit() e ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression

from src.features import PRE_DELIVERY_FEATURES, TARGET_COLUMN

# Identificar tipos de colunas dentro de PRE_DELIVERY_FEATURES
NUMERIC_FEATURES = [
    "freight_value", "price", "freight_ratio", "estimated_delivery_days",
    "seller_customer_distance_km", "product_weight_g", "product_volume_cm3",
    "order_item_count", "payment_installments",
]
CATEGORICAL_FEATURES = [
    "seller_state", "customer_state", "product_category_name_english", "payment_type",
]

preprocessor = ColumnTransformer(transformers=[
    ("num", StandardScaler(), NUMERIC_FEATURES),
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
])

baseline_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)),
])
```

### Pattern 2: Train/Test Split Estratificado + Fit/Eval

**What:** `train_test_split` com `stratify=y` garante que a proporção de positivos (~15-20%) é preservada em ambos os splits.

```python
# Source: sklearn official docs — train_test_split stratify parameter
from sklearn.model_selection import train_test_split

X = df[PRE_DELIVERY_FEATURES]
y = df[TARGET_COLUMN]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    stratify=y,
    random_state=42,
)

baseline_pipeline.fit(X_train, y_train)
```

### Pattern 3: PR-AUC e Recall no Test Set

**What:** Reportar `average_precision_score` (= PR-AUC) e `classification_report` com threshold padrão 0.5 como linha de base antes de otimizar o threshold.

```python
# Source: sklearn official docs — average_precision_score, classification_report
from sklearn.metrics import average_precision_score, classification_report, precision_recall_curve

y_proba = baseline_pipeline.predict_proba(X_test)[:, 1]

pr_auc = average_precision_score(y_test, y_proba)
print(f"Baseline PR-AUC: {pr_auc:.4f}")
print(classification_report(y_test, baseline_pipeline.predict(X_test)))
```

### Pattern 4: XGBoost com scale_pos_weight

**What:** Para XGBoost, `class_weight='balanced'` não é suportado diretamente — usar `scale_pos_weight = negatives / positives`.

```python
# Source: XGBoost docs — scale_pos_weight parameter
import numpy as np
from xgboost import XGBClassifier

# Calcular ratio no training set (não no full dataset)
neg = (y_train == 0).sum()
pos = (y_train == 1).sum()
scale_pos_weight = neg / pos  # tipicamente ~4-6 para 15-20% de positivos

final_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", XGBClassifier(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.05,
        scale_pos_weight=scale_pos_weight,
        eval_metric="aucpr",
        random_state=42,
        n_jobs=-1,
    )),
])

final_pipeline.fit(X_train, y_train)
```

### Pattern 5: SHAP TreeExplainer em Dados Transformados

**What:** SHAP TreeExplainer precisa do array transformado (pós-ColumnTransformer), não do DataFrame original. Extrair o classificador e os dados transformados separadamente.

```python
# Source: SHAP docs — TreeExplainer usage
import shap
import matplotlib.pyplot as plt

# Extrair classificador e transformar dados
xgb_model = final_pipeline.named_steps["classifier"]
X_test_transformed = final_pipeline.named_steps["preprocessor"].transform(X_test)

# Nomes de features após OneHotEncoder
feature_names = (
    NUMERIC_FEATURES
    + list(final_pipeline.named_steps["preprocessor"]
           .named_transformers_["cat"]
           .get_feature_names_out(CATEGORICAL_FEATURES))
)

# SHAP em amostra de 5000 se dataset for grande (performance)
sample_size = min(5000, len(X_test_transformed))
X_shap = X_test_transformed[:sample_size]

explainer = shap.TreeExplainer(xgb_model)
shap_values = explainer.shap_values(X_shap)

# Beeswarm: top-15 features
plt.figure(figsize=(10, 8))
shap.summary_plot(
    shap_values, X_shap,
    feature_names=feature_names,
    max_display=15,
    show=False,
)
plt.tight_layout()
plt.savefig("reports/figures/shap_beeswarm.png", dpi=150, bbox_inches="tight")
plt.close()
```

### Pattern 6: Seleção de Threshold na Curva PR

**What:** Encontrar o índice na curva PR onde Precision >= 0.40 (critério primário) e verificar Recall >= 0.60 (critério secundário).

```python
# Source: sklearn official docs — precision_recall_curve
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve

y_proba_final = final_pipeline.predict_proba(X_test)[:, 1]
precision, recall, thresholds = precision_recall_curve(y_test, y_proba_final)

# Encontrar primeiro threshold onde Precision >= 0.40
valid_idx = np.where(precision[:-1] >= 0.40)[0]
if len(valid_idx) > 0:
    chosen_idx = valid_idx[0]
    chosen_threshold = thresholds[chosen_idx]
    chosen_precision = precision[chosen_idx]
    chosen_recall = recall[chosen_idx]
else:
    # Fallback: melhor Recall com Precision máxima disponível
    chosen_idx = np.argmax(recall[precision >= recall.max() * 0.5])
    chosen_threshold = thresholds[chosen_idx]

print(f"Threshold: {chosen_threshold:.3f}")
print(f"Precision: {chosen_precision:.2f} | Recall: {chosen_recall:.2f}")

# Estimativa operacional
# Usar dataset completo (não apenas test set) para estimativa semanal
y_proba_all = final_pipeline.predict_proba(X[PRE_DELIVERY_FEATURES])[:, 1]
flagged_total = (y_proba_all >= chosen_threshold).sum()
total_orders = len(y_proba_all)

# Olist tem ~100k pedidos; estimar semanas no período
# dataset cobre ~2 anos = ~104 semanas
weeks_in_dataset = 104
flagged_per_week = flagged_total / weeks_in_dataset
pct_real_risk = chosen_precision  # = Precision no threshold escolhido

print(f"Pedidos flagrados/semana: {flagged_per_week:.0f}")
print(f"% real de risco entre flagrados: {pct_real_risk:.0%}")

# Salvar curva PR com threshold marcado
plt.figure(figsize=(8, 6))
plt.plot(recall, precision, label=f"XGBoost (PR-AUC={pr_auc_final:.3f})")
plt.scatter([chosen_recall], [chosen_precision], color="red", zorder=5,
            label=f"Threshold={chosen_threshold:.2f} | P={chosen_precision:.2f} | R={chosen_recall:.2f}")
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision-Recall Curve — Pre-Delivery Risk Model")
plt.legend()
plt.savefig("reports/figures/pr_curve.png", dpi=150, bbox_inches="tight")
plt.close()
```

### Pattern 7: Tabela de Risco por Vendedor

**What:** Calcular score médio de risco usando `predict_proba` no dataset completo, agregar por `seller_id`, filtrar vendedores com >= 10 pedidos, exibir top-20.

```python
# Adicionar scores ao DataFrame completo
df["risk_score"] = final_pipeline.predict_proba(df[PRE_DELIVERY_FEATURES])[:, 1]

# Agregar por vendedor
seller_table = (
    df.groupby("seller_id")
    .agg(
        score_medio_risco=("risk_score", "mean"),
        total_pedidos=("order_id", "count"),
        pedidos_alto_risco=("risk_score", lambda x: (x >= chosen_threshold).sum()),
    )
    .reset_index()
    .query("total_pedidos >= 10")
    .sort_values("score_medio_risco", ascending=False)
    .head(20)
    .reset_index(drop=True)
)

print(seller_table.to_string(index=False))
```

### Pattern 8: Serialização com joblib

**What:** Serializar pipeline completo (pré-processamento + modelo) como único objeto joblib. O Streamlit carregará exatamente este objeto.

```python
# Source: sklearn docs — model persistence with joblib
import joblib

# Baseline
joblib.dump(baseline_pipeline, "models/baseline_logreg.joblib")
print("Saved: models/baseline_logreg.joblib")

# Pipeline final XGBoost
joblib.dump(final_pipeline, "models/final_pipeline.joblib")
print("Saved: models/final_pipeline.joblib")

# Verificar round-trip
loaded = joblib.load("models/final_pipeline.joblib")
y_check = loaded.predict_proba(X_test.head(5))[:, 1]
print(f"Round-trip OK: {y_check}")
```

### Anti-Patterns to Avoid

- **Fit do preprocessor no full dataset antes do split:** `scaler.fit(X)` antes de `train_test_split` vaza estatísticas do test set. Usar `Pipeline` que fitará apenas em `X_train`.
- **Serializar só o estimador (não o Pipeline):** `joblib.dump(xgb_model, ...)` sem o preprocessor força o Streamlit a reconstruir as transformações manualmente — impossível sem acesso ao X_train. Sempre serializar o `Pipeline` completo.
- **Usar `review_score` ou qualquer coluna de FORBIDDEN_FEATURES como feature:** Validar `assert not any(c in PRE_DELIVERY_FEATURES for c in FORBIDDEN_FEATURES)` no início do notebook.
- **SHAP no DataFrame pandas original:** `shap.TreeExplainer(xgb_model).shap_values(X_test)` sem transformar via preprocessor produz erro ou valores errados. Sempre transformar com `preprocessor.transform(X_test)` antes do SHAP.
- **Agrupar vendedores sem filtro de volume:** Vendedores com 1-2 pedidos têm scores instáveis (alta variância). Aplicar `query("total_pedidos >= 10")` conforme decisão bloqueada.
- **Calcular `scale_pos_weight` no dataset completo:** O ratio deve ser calculado em `y_train`, não em `y` completo — para não incluir estatísticas do test set na configuração do modelo.
- **SHAP em 100k linhas sem amostra:** TreeExplainer pode levar 10+ minutos. Usar `min(5000, len(X_test_transformed))` para o notebook; a amostra é representativa para o beeswarm.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Pré-processamento sem leakage | Scaler/encoder manual com dicts salvos | `sklearn.Pipeline` + `ColumnTransformer` | Pipeline garante fit-only-on-train por design; serializa junto com o modelo |
| Curva PR e threshold selection | Loop manual sobre thresholds | `sklearn.metrics.precision_recall_curve` | Retorna arrays vetorizados de precision/recall/thresholds; eficiente e testado |
| PR-AUC | Integral manual da curva | `sklearn.metrics.average_precision_score` | Implementação numericamente estável e documentada |
| SHAP values para XGBoost | Feature importance via `xgb.feature_importances_` | `shap.TreeExplainer` | `feature_importances_` é ganho médio, não impacto marginal; SHAP é correto teoricamente e aceito por executivos |
| Serialização de modelos sklearn | pickle nativo | `joblib.dump/load` | joblib é otimizado para arrays numpy (compressão eficiente); padrão do projeto |
| Balanceamento de classes | Implementação manual de pesos | `class_weight='balanced'` (LogReg) e `scale_pos_weight` (XGBoost) | Parâmetros nativos dos estimadores — calculados automaticamente e reproducíveis |

**Key insight:** O sklearn Pipeline é o padrão que resolve simultaneamente leakage (fit apenas em train), serialização (objeto único coerente), e reprodutibilidade (mesmo objeto em treino e inferência). Qualquer desvio deste padrão cria problemas na integração com o Streamlit da Phase 6.

---

## Common Pitfalls

### Pitfall 1: Leakage por Preprocessing Antes do Split
**What goes wrong:** `StandardScaler().fit_transform(X)` no DataFrame completo antes de `train_test_split` injeta mean e std do test set no treinamento. O modelo aprende distribuição "ideal" e reporta métricas infladas.
**Why it happens:** Parece mais simples normalizar tudo de uma vez. Comum em tutoriais que omitem o Pipeline.
**How to avoid:** Encapsular todas as transformações dentro de `sklearn.Pipeline`. Jamais chamar `fit` ou `fit_transform` em X antes do split.
**Warning signs:** PR-AUC muito acima do esperado (>0.70 em dados tabulares simples sem features poderosas).

### Pitfall 2: Serializar Só o Estimador (Não o Pipeline)
**What goes wrong:** `joblib.dump(xgb_model, 'models/final_pipeline.joblib')` salva apenas o XGBClassifier. O Streamlit carrega o modelo mas não tem o ColumnTransformer fitted — qualquer chamada a `predict_proba` falha ou produz resultados incorretos porque os dados não estão transformados.
**Why it happens:** Confusão entre "modelo" (estimador) e "pipeline" (pré-processamento + estimador).
**How to avoid:** Sempre `joblib.dump(pipeline, ...)` onde `pipeline` é o objeto `sklearn.Pipeline` completo. Verificar round-trip no notebook.
**Warning signs:** `ValueError: Input contains NaN` ou shape mismatch ao carregar no Streamlit.

### Pitfall 3: SHAP no DataFrame Pandas (Não no Array Transformado)
**What goes wrong:** `explainer.shap_values(X_test)` onde `X_test` ainda contém colunas categóricas. XGBoost espera array numérico; shap lança erro de tipo ou produz valores com dimensões incorretas.
**Why it happens:** A extração do modelo e a transformação dos dados são feitas em passos separados e o passo de transformação é esquecido.
**How to avoid:** `X_test_transformed = pipeline.named_steps["preprocessor"].transform(X_test)` antes de qualquer chamada ao SHAP.
**Warning signs:** `TypeError: Input data must be numeric` ou shape de `shap_values` diferente de `(n_samples, n_features_transformed)`.

### Pitfall 4: scale_pos_weight Calculado no Dataset Completo
**What goes wrong:** `scale_pos_weight = (y == 0).sum() / (y == 1).sum()` inclui estatísticas do test set. Tecnicamente é leakage de hiperparâmetro (minor), mas é incorreto metodologicamente.
**Why it happens:** Calculado antes do split por conveniência.
**How to avoid:** Calcular após o split: `neg/pos = y_train.value_counts()[0] / y_train.value_counts()[1]`.
**Warning signs:** Não há warning — deve ser prevenido como boa prática.

### Pitfall 5: Tabela de Vendedores Sem Filtro de Volume Mínimo
**What goes wrong:** Vendedor com 2 pedidos — ambos com review ruim — aparece com `score_medio_risco = 1.0` no topo da tabela. Na apresentação, parece um problema grave quando é ruído estatístico.
**Why it happens:** `groupby().agg()` sem `.query("total_pedidos >= 10")`.
**How to avoid:** Filtro `total_pedidos >= 10` conforme decisão bloqueada no CONTEXT.md.
**Warning signs:** Top vendedores com `total_pedidos` < 5 na tabela de resultado.

### Pitfall 6: Threshold 0.5 Padrão com Classe Desbalanceada
**What goes wrong:** `predict()` usa threshold 0.5 por padrão. Com ~15-20% de positivos e `class_weight='balanced'`, o modelo calibra probabilidades em torno de valores mais baixos — threshold 0.5 descarta muitos positivos reais, causando Recall baixo.
**Why it happens:** Usar `predict()` diretamente sem otimizar o threshold via curva PR.
**How to avoid:** Sempre usar `predict_proba()[:, 1]` para gerar scores, então selecionar threshold via `precision_recall_curve` com o critério Precision >= 0.40.
**Warning signs:** Recall < 0.30 com `classification_report(y_test, pipeline.predict(X_test))`.

### Pitfall 7: SHAP em 100k Linhas Sem Amostragem
**What goes wrong:** `explainer.shap_values(X_test_transformed)` onde `X_test_transformed` tem 20k+ linhas. TreeExplainer pode levar 10-30 minutos, travando o notebook.
**Why it happens:** Assumir que SHAP é tão rápido quanto `predict`.
**How to avoid:** Usar `X_shap = X_test_transformed[:5000]` — 5k linhas são representativas para o beeswarm; o padrão de importância de features é estável acima de 1-2k amostras.
**Warning signs:** Célula do SHAP rodando por > 2 minutos sem output.

---

## Code Examples

### Verificação Anti-Leakage no Início do Notebook

```python
# Executar no topo do notebook — falha rápido se o contrato foi violado
from src.features import PRE_DELIVERY_FEATURES, FORBIDDEN_FEATURES, TARGET_COLUMN

leakage = [c for c in FORBIDDEN_FEATURES if c in PRE_DELIVERY_FEATURES]
assert not leakage, f"LEAKAGE DETECTADO: {leakage}"

# Verificar que todas as features existem na gold table
df = pd.read_parquet("data/gold/olist_gold.parquet")
missing = [c for c in PRE_DELIVERY_FEATURES if c not in df.columns]
assert not missing, f"Features ausentes na gold table: {missing}"

X = df[PRE_DELIVERY_FEATURES]
y = df[TARGET_COLUMN]

print(f"Dataset: {len(df)} pedidos | Positivos: {y.mean():.1%} | Features: {len(PRE_DELIVERY_FEATURES)}")
```

### Métricas Comparativas Baseline vs. XGBoost

```python
from sklearn.metrics import average_precision_score, classification_report

def eval_model(pipeline, X_test, y_test, name):
    y_proba = pipeline.predict_proba(X_test)[:, 1]
    y_pred = pipeline.predict(X_test)
    pr_auc = average_precision_score(y_test, y_proba)
    print(f"\n{'='*40}")
    print(f"{name} | PR-AUC: {pr_auc:.4f}")
    print(classification_report(y_test, y_pred, target_names=["good", "bad_review"]))
    return pr_auc

baseline_pr_auc = eval_model(baseline_pipeline, X_test, y_test, "Baseline LogReg")
final_pr_auc = eval_model(final_pipeline, X_test, y_test, "XGBoost")

assert final_pr_auc > baseline_pr_auc, \
    f"XGBoost ({final_pr_auc:.4f}) deve superar baseline ({baseline_pr_auc:.4f})"
print(f"\nMelhora: +{final_pr_auc - baseline_pr_auc:.4f} PR-AUC")
```

### Verificação de Round-Trip dos Artefatos Joblib

```python
import joblib

# Verificar ambos os artefatos após serialização
for path in ["models/baseline_logreg.joblib", "models/final_pipeline.joblib"]:
    loaded = joblib.load(path)
    sample_proba = loaded.predict_proba(X_test.head(3))[:, 1]
    print(f"OK: {path} | sample scores: {sample_proba.round(3)}")
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `pickle` para serializar modelos sklearn | `joblib.dump/load` | scikit-learn 0.23+ | Joblib é ~3-5x mais rápido para arrays grandes; pickle ainda funciona mas não é recomendado |
| `feature_importances_` do XGBoost | SHAP TreeExplainer | 2017+ (mainstream 2020+) | `feature_importances_` é ganho médio global; SHAP dá contribuição por predição — base para waterfall e beeswarm executivos |
| ROC-AUC como métrica principal | PR-AUC (average_precision_score) | Bem documentado para datasets desbalanceados | ROC-AUC pode ser > 0.8 mesmo com modelo ruim para classe minoritária; PR-AUC é honesto sobre desempenho real |
| `GridSearchCV` para hiperparâmetros | Defaults razoáveis + otimização manual de threshold | Contexto do sprint | Grid search leva 4-6h para <1% de ganho de AUC; threshold na curva PR tem impacto operacional direto e imediato |
| `sparse_output=True` (padrão antigo do OHE) | `sparse_output=False` no OneHotEncoder | sklearn 1.2+ | `sparse_output=False` retorna array denso, compatível com SHAP sem conversão adicional |

**Deprecated/outdated:**
- `make_pipeline(...)` sem nome explícito dos steps: ainda funciona, mas `Pipeline(steps=[("name", obj)])` é preferível para acessar steps por nome em `pipeline.named_steps["preprocessor"]` — necessário para SHAP.
- `XGBClassifier(use_label_encoder=False)`: parâmetro removido no XGBoost 1.6+. Não incluir — causará `TypeError`.

---

## Open Questions

1. **Proporção real da classe positiva (bad_review) na gold table**
   - What we know: Estimativa do projeto é 15-20% de reviews 1-2 estrelas
   - What's unclear: Proporção exata determina `scale_pos_weight` do XGBoost
   - Recommendation: Calcular `y_train.value_counts(normalize=True)` na Section 1 do notebook e usar o ratio calculado dinamicamente — não hardcodar um valor fixo

2. **Performance do SHAP no test set completo**
   - What we know: STATE.md documenta que SHAP pode levar 10+ min em 100k linhas
   - What's unclear: Tamanho do test set (20% de ~100k = ~20k linhas) vs. amostra de 5k
   - Recommendation: Usar amostra de 5000 por padrão (já especificado no Claude's Discretion); o padrão do beeswarm é estável acima de 2k amostras

3. **Disponibilidade de `seller_id` na gold table para a tabela de vendedores**
   - What we know: `seller_id` deve estar na gold table (Phase 2 fez join com sellers.csv)
   - What's unclear: Se `seller_id` está em `PRE_DELIVERY_FEATURES` ou apenas como coluna auxiliar
   - Recommendation: `seller_id` NÃO deve estar em `PRE_DELIVERY_FEATURES` (é join key, não feature preditiva). Carregar `df[PRE_DELIVERY_FEATURES + ["seller_id", TARGET_COLUMN]]` para o groupby da tabela de vendedores; usar o DataFrame completo com `seller_id` separadamente do array X

---

## Sources

### Primary (HIGH confidence)
- scikit-learn official docs — Pipeline, ColumnTransformer, average_precision_score, precision_recall_curve, train_test_split stratify
- XGBoost official docs — XGBClassifier, scale_pos_weight, eval_metric='aucpr'
- SHAP official docs — TreeExplainer, summary_plot, beeswarm
- joblib official docs — dump/load para objetos sklearn
- `.planning/research/SUMMARY.md` — pesquisa de projeto com stack, pitfalls e arquitetura verificados em 2026-03-01
- `.planning/phases/04-ml-ato-2/04-CONTEXT.md` — decisões bloqueadas do usuário
- `.planning/phases/01-kickoff-e-contratos/01-02-PLAN.md` — spec definitiva de PRE_DELIVERY_FEATURES (13 colunas)

### Secondary (MEDIUM confidence)
- `.planning/STATE.md` — nota de blocker: "SHAP TreeExplainer pode levar 10+ min em 100k linhas — testar em amostra de 5000 primeiro" — verificado pela equipe do projeto
- SpringerLink ICCCE 2024 — "Customer Satisfaction Prediction via Interpretable Models and Sentiment Analysis" — valida SHAP + PR-AUC para o problema de satisfação em e-commerce

### Tertiary (LOW confidence)
- Proporção exata da classe positiva (~15-20%): estimativa — verificar em `y.value_counts()` na Section 1 do notebook

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — versões confirmadas no requirements.txt do projeto (Phase 1); APIs verificadas via docs oficiais
- Architecture: HIGH — padrão sklearn Pipeline para leakage prevention é documentado; serialização joblib é padrão do projeto desde Phase 1
- Pitfalls: HIGH — pitfalls 1-3 são documentados nas fontes oficiais sklearn/SHAP; pitfalls 4-7 são verificados no STATE.md e SUMMARY.md do projeto

**Research date:** 2026-03-01
**Valid until:** 2026-04-01 (stack estável; XGBoost e scikit-learn têm ciclos de release de 3-6 meses)
