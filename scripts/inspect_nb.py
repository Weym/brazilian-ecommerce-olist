import json
import os

nb = json.load(open('notebooks/FASE4-P4-ml-pipeline.ipynb'))
cells = nb['cells']
print(f'Total cells: {len(cells)}')
for i, c in enumerate(cells):
    src = ''.join(c['source'])
    if src.strip():
        first = src.split('\n')[0][:80]
        print(f'Cell {i} ({c["cell_type"]}): {first}')

print()
full_src = ' '.join(''.join(c['source']) for c in cells if c['cell_type'] == 'code')
for check in ['precision_recall_curve', 'chosen_threshold', 'flagged_per_week', 'pr_curve.png',
              'seller_id', 'score_medio_risco', 'loaded_baseline', 'named_steps',
              '# (1)', '# (2)', '# (3)', '# (4)', '# (5)', '# (6)', '# (7)']:
    present = 'YES' if check in full_src else 'NO'
    print(f'{present}: {check}')

print()
for path in ['models/baseline_logreg.joblib', 'models/final_pipeline.joblib',
             'reports/figures/shap_beeswarm.png', 'reports/figures/pr_curve.png']:
    exists = 'YES' if os.path.exists(path) else 'NO'
    size = os.path.getsize(path) if os.path.exists(path) else 0
    print(f'{exists} ({size} bytes): {path}')
