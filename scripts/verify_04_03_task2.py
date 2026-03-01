import os, json, joblib, sys

# Notebook com Secao 7
nb = json.load(open('notebooks/FASE4-P4-ml-pipeline.ipynb'))
src = ' '.join(''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code')
assert 'loaded_baseline' in src, 'FAIL: round-trip ausente na Secao 7'
assert 'named_steps' in src, 'FAIL: verificacao de named_steps ausente'
print('OK: Secao 7 presente no notebook')

# Ambos os joblib existem e carregam
sys.path.insert(0, '.')
for path in ['models/baseline_logreg.joblib', 'models/final_pipeline.joblib']:
    assert os.path.exists(path), f'FAIL: {path} nao encontrado'
    loaded = joblib.load(path)
    assert hasattr(loaded, 'predict_proba'), f'FAIL: {path} nao tem predict_proba'
    print(f'OK: {path} carregavel')

# final_pipeline e Pipeline completo
fp = joblib.load('models/final_pipeline.joblib')
assert 'preprocessor' in fp.named_steps, 'FAIL: preprocessor ausente'
assert 'classifier' in fp.named_steps, 'FAIL: classifier ausente'
print('OK: final_pipeline.joblib e Pipeline completo com preprocessor + classifier')

# Todos os 4 artefatos existem
for path in ['reports/figures/shap_beeswarm.png', 'reports/figures/pr_curve.png']:
    assert os.path.exists(path), f'FAIL: {path} ausente'
    print(f'OK: {path} existe')

print('ALL CHECKS PASSED -- FASE 4 COMPLETA')
