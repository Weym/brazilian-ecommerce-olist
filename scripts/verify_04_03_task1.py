import os, json

nb = json.load(open('notebooks/FASE4-P4-ml-pipeline.ipynb'))
src = ' '.join(''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code')

# Secao 5 — threshold
assert 'precision_recall_curve' in src, 'FAIL: precision_recall_curve ausente'
assert 'chosen_threshold' in src, 'FAIL: chosen_threshold ausente'
assert '0.40' in src, 'FAIL: criterio Precision >= 0.40 ausente'
assert 'flagged_per_week' in src, 'FAIL: estimativa operacional flagged_per_week ausente'
assert 'pr_curve.png' in src, 'FAIL: salvamento da curva PR ausente'
print('OK: Secao 5 presente no notebook')

# Secao 6 — vendedores
assert 'seller_id' in src, 'FAIL: seller_id ausente (tabela de vendedores)'
assert 'score_medio_risco' in src, 'FAIL: score_medio_risco ausente'
assert 'total_pedidos >= 10' in src, 'FAIL: filtro total_pedidos >= 10 ausente'
assert '.head(20)' in src, 'FAIL: top-20 ausente'
assert 'pedidos_alto_risco' in src, 'FAIL: coluna pedidos_alto_risco ausente'
print('OK: Secao 6 presente no notebook')

# PNG da curva PR
assert os.path.exists('reports/figures/pr_curve.png'), 'FAIL: reports/figures/pr_curve.png nao encontrado'
size_kb = os.path.getsize('reports/figures/pr_curve.png') / 1024
assert size_kb > 10, f'FAIL: pr_curve.png muito pequeno ({size_kb:.1f} KB)'
print(f'OK: reports/figures/pr_curve.png existe ({size_kb:.1f} KB)')
print('ALL CHECKS PASSED')
