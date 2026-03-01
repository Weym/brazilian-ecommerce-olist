import os, sys, json, joblib

sys.path.insert(0, ".")

# 1. Notebook completo com 7 secoes
nb = json.load(open("notebooks/FASE4-P4-ml-pipeline.ipynb"))
all_src = " ".join("".join(c["source"]) for c in nb["cells"])
for sec in ["(1)", "(2)", "(3)", "(4)", "(5)", "(6)", "(7)"]:
    assert sec in all_src, f"Secao {sec} ausente no notebook"
print("OK: 7 secoes presentes")

# 2. Zero leakage
from src.features import PRE_DELIVERY_FEATURES, FORBIDDEN_FEATURES
assert not [c for c in FORBIDDEN_FEATURES if c in PRE_DELIVERY_FEATURES]
print("OK: zero leakage")

# 3. Artefatos ML
for path in ["models/baseline_logreg.joblib", "models/final_pipeline.joblib"]:
    loaded = joblib.load(path)
    assert hasattr(loaded, "predict_proba")
print("OK: ambos os joblib carregaveis")

# 4. Pipeline final e completo
fp = joblib.load("models/final_pipeline.joblib")
assert "preprocessor" in fp.named_steps
assert "classifier" in fp.named_steps
print("OK: final_pipeline tem preprocessor + classifier")

# 5. Figuras para slides
for path in ["reports/figures/shap_beeswarm.png", "reports/figures/pr_curve.png"]:
    assert os.path.exists(path) and os.path.getsize(path) > 10_000
print("OK: ambas as figuras existem e nao estao vazias")

print("PASS: Fase 4 completa -- todos os entregaveis verificados")
