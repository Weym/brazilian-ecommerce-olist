"""
Train baseline LogisticRegression and save models/baseline_logreg.joblib.
Replicates notebook Sections 1 and 2 for CLI execution.
"""
import sys
import os

# Project root is one level up from scripts/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import average_precision_score, classification_report

from src.features import PRE_DELIVERY_FEATURES, FORBIDDEN_FEATURES, TARGET_COLUMN

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- Section 1: Load & Feature Matrix ---

# Anti-leakage check
leakage = [c for c in FORBIDDEN_FEATURES if c in PRE_DELIVERY_FEATURES]
assert not leakage, f"LEAKAGE DETECTADO: {leakage}"
print("OK: nenhum leakage em PRE_DELIVERY_FEATURES")

# Load gold table
gold_path = os.path.join(PROJECT_ROOT, "data", "gold", "olist_gold.parquet")
df = pd.read_parquet(gold_path)
print(f"Gold table: {len(df):,} linhas x {df.shape[1]} colunas")

missing = [c for c in PRE_DELIVERY_FEATURES if c not in df.columns]
assert not missing, f"Features ausentes na gold table: {missing}"
print(f"OK: todas as {len(PRE_DELIVERY_FEATURES)} features pre-entrega presentes")

# Feature matrix
X = df[PRE_DELIVERY_FEATURES].copy()
y = df[TARGET_COLUMN].copy()
print(f"Dataset: {len(X):,} pedidos")
print(f"Classe positiva (bad_review=1): {y.mean():.1%}")
print(f"Features: {X.shape[1]} colunas")

assert X.shape[1] == len(PRE_DELIVERY_FEATURES) == 13
assert set(y.unique()).issubset({0, 1})
assert 0.10 <= y.mean() <= 0.30, f"y.mean() fora do range esperado: {y.mean()}"

# Numeric/categorical split
NUMERIC_FEATURES = [
    "freight_value", "price", "freight_ratio", "estimated_delivery_days",
    "seller_customer_distance_km", "product_weight_g", "product_volume_cm3",
    "order_item_count", "payment_installments",
]
CATEGORICAL_FEATURES = [
    "seller_state", "customer_state",
    "product_category_name_english", "payment_type",
]

assert set(NUMERIC_FEATURES + CATEGORICAL_FEATURES) == set(PRE_DELIVERY_FEATURES), \
    "NUMERIC + CATEGORICAL nao cobrem exatamente PRE_DELIVERY_FEATURES"

# Train/test split — 80/20 estratificado por bad_review
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    stratify=y,
    random_state=42,
)
print(f"Treino: {len(X_train):,} | Teste: {len(X_test):,}")
print(f"Positivos treino: {y_train.mean():.1%} | Positivos teste: {y_test.mean():.1%}")

# --- Section 2: Baseline LogisticRegression ---

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
])

preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_transformer, NUMERIC_FEATURES),
    ("cat", categorical_transformer, CATEGORICAL_FEATURES),
])

baseline_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(
        class_weight="balanced",  # LOCKED: sem SMOTE (decisao CONTEXT.md)
        max_iter=1000,
        random_state=42,
    )),
])

baseline_pipeline.fit(X_train, y_train)
print("Baseline pipeline treinado.")

# Evaluate
y_proba = baseline_pipeline.predict_proba(X_test)[:, 1]
y_pred = baseline_pipeline.predict(X_test)
pr_auc = average_precision_score(y_test, y_proba)
print(f"\n{'='*40}")
print(f"Baseline LogReg | PR-AUC: {pr_auc:.4f}")
print(classification_report(y_test, y_pred, target_names=["good_review", "bad_review"]))

# Serialize
models_dir = os.path.join(PROJECT_ROOT, "models")
os.makedirs(models_dir, exist_ok=True)
joblib_path = os.path.join(models_dir, "baseline_logreg.joblib")
joblib.dump(baseline_pipeline, joblib_path)
print(f"Salvo: models/baseline_logreg.joblib")

# Round-trip verification
loaded_baseline = joblib.load(joblib_path)
sample_scores = loaded_baseline.predict_proba(X_test.head(3))[:, 1]
print(f"Round-trip OK: {sample_scores.round(3)}")

print("\nALL SECTION 2 CHECKS PASSED")
