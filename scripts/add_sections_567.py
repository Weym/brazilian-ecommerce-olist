"""
Add sections 5, 6, 7 to FASE4-P4-ml-pipeline.ipynb
Replaces placeholder cells with full implementation.
"""
import json
import copy

NB_PATH = "notebooks/FASE4-P4-ml-pipeline.ipynb"

nb = json.load(open(NB_PATH, encoding="utf-8"))


def make_code_cell(cell_id, source_lines):
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": cell_id,
        "metadata": {},
        "outputs": [],
        "source": source_lines,
    }


def make_markdown_cell(cell_id, source_lines):
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {},
        "source": source_lines,
    }


# ─── SECTION 5 cells ───────────────────────────────────────────────────────
cell_5_1_lines = [
    "# === SECAO 5: THRESHOLD + ESTIMATIVA OPERACIONAL ===\n",
    "\n",
    "# Celula 5.1 — Curva PR e selecao de threshold\n",
    "y_proba_final = final_pipeline.predict_proba(X_test)[:, 1]\n",
    "precision, recall, thresholds = precision_recall_curve(y_test, y_proba_final)\n",
    "\n",
    "# Criterio primario: Precision >= 0.40 (LOCKED per CONTEXT.md)\n",
    "valid_idx = np.where(precision[:-1] >= 0.40)[0]\n",
    "if len(valid_idx) > 0:\n",
    "    chosen_idx = valid_idx[0]\n",
    "    chosen_threshold = thresholds[chosen_idx]\n",
    "    chosen_precision = precision[chosen_idx]\n",
    "    chosen_recall = recall[chosen_idx]\n",
    "else:\n",
    "    # Fallback: se nenhum threshold atingir Precision >= 0.40, usar o melhor Recall disponivel\n",
    "    print('AVISO: Precision >= 0.40 nao atingida. Usando fallback: max Recall com Precision >= 0.25')\n",
    "    valid_fallback = np.where(precision[:-1] >= 0.25)[0]\n",
    "    chosen_idx = valid_fallback[np.argmax(recall[valid_fallback])] if len(valid_fallback) > 0 else np.argmax(recall[:-1])\n",
    "    chosen_threshold = thresholds[chosen_idx]\n",
    "    chosen_precision = precision[chosen_idx]\n",
    "    chosen_recall = recall[chosen_idx]\n",
    "\n",
    "print(f'Threshold escolhido: {chosen_threshold:.3f}')\n",
    "print(f'Precision: {chosen_precision:.2f} | Recall: {chosen_recall:.2f}')\n",
    "\n",
    "# Criterio secundario — alerta se nao atingido, mas nao para execucao\n",
    "if chosen_recall < 0.60:\n",
    "    print(f'AVISO: Recall {chosen_recall:.2f} abaixo de 0.60 — revisar threshold manualmente se necessario')\n",
    "else:\n",
    "    print(f'OK: Recall {chosen_recall:.2f} >= 0.60 (criterio secundario atingido)')\n",
]

cell_5_2_lines = [
    "# Celula 5.2 — Estimativa operacional\n",
    "\n",
    "# Scores no dataset COMPLETO para estimativa de volume semanal\n",
    "y_proba_all = final_pipeline.predict_proba(X[PRE_DELIVERY_FEATURES])[:, 1]\n",
    "flagged_total = (y_proba_all >= chosen_threshold).sum()\n",
    "total_orders = len(y_proba_all)\n",
    "\n",
    "# Dataset Olist cobre aprox. 2 anos = 104 semanas\n",
    "weeks_in_dataset = 104\n",
    "flagged_per_week = flagged_total / weeks_in_dataset\n",
    "pct_real_risk = chosen_precision  # Precision no threshold = % real de risco entre flagrados\n",
    "\n",
    "print(f'\\n=== ESTIMATIVA OPERACIONAL ===')\n",
    "print(f'Total de pedidos no dataset: {total_orders:,}')\n",
    "print(f'Pedidos flagrados (threshold={chosen_threshold:.3f}): {flagged_total:,} ({flagged_total/total_orders:.1%})')\n",
    "print(f'Pedidos flagrados/semana: {flagged_per_week:.0f}')\n",
    "print(f'% real de risco entre flagrados: {pct_real_risk:.0%}')\n",
    "print(f\"\\nNarrativa slide: '{pct_real_risk:.0%} dos pedidos flagrados sao de fato risco real'\")\n",
]

cell_5_3_lines = [
    "# Celula 5.3 — Curva PR salva em PNG\n",
    "import os\n",
    "os.makedirs('../reports/figures', exist_ok=True)\n",
    "\n",
    "pr_auc_final = average_precision_score(y_test, y_proba_final)\n",
    "\n",
    "plt.figure(figsize=(8, 6))\n",
    "plt.plot(recall, precision, label=f'XGBoost (PR-AUC={pr_auc_final:.3f})', color='steelblue', linewidth=2)\n",
    "plt.scatter(\n",
    "    [chosen_recall], [chosen_precision],\n",
    "    color='red', zorder=5, s=100,\n",
    "    label=f'Threshold={chosen_threshold:.2f} | P={chosen_precision:.2f} | R={chosen_recall:.2f}',\n",
    ")\n",
    "plt.axhline(y=0.40, color='gray', linestyle='--', alpha=0.5, label='Precision = 0.40 (criterio)')\n",
    "plt.xlabel('Recall', fontsize=12)\n",
    "plt.ylabel('Precision', fontsize=12)\n",
    "plt.title('Precision-Recall Curve — Pre-Delivery Risk Model', fontsize=13)\n",
    "plt.legend(fontsize=10)\n",
    "plt.grid(alpha=0.3)\n",
    "plt.tight_layout()\n",
    "plt.savefig('../reports/figures/pr_curve.png', dpi=150, bbox_inches='tight')\n",
    "plt.close()\n",
    "print('Salvo: reports/figures/pr_curve.png')\n",
]

# ─── SECTION 6 cells ───────────────────────────────────────────────────────
cell_6_1_lines = [
    "# === SECAO 6: TABELA DE VENDEDORES ===\n",
    "\n",
    "# Celula 6.1 — Score de risco no dataset completo e agregacao por vendedor\n",
    "# seller_id NAO esta em PRE_DELIVERY_FEATURES — e join key, nao feature preditiva\n",
    "# Usar df completo com seller_id como coluna auxiliar\n",
    "df_scored = df[PRE_DELIVERY_FEATURES + ['seller_id', TARGET_COLUMN]].copy()\n",
    "df_scored['risk_score'] = final_pipeline.predict_proba(df_scored[PRE_DELIVERY_FEATURES])[:, 1]\n",
    "\n",
    "# Agregacao por vendedor\n",
    "seller_table = (\n",
    "    df_scored.groupby('seller_id')\n",
    "    .agg(\n",
    "        score_medio_risco=('risk_score', 'mean'),\n",
    "        total_pedidos=('seller_id', 'count'),\n",
    "        pedidos_alto_risco=('risk_score', lambda x: (x >= chosen_threshold).sum()),\n",
    "    )\n",
    "    .reset_index()\n",
    "    .query('total_pedidos >= 10')  # LOCKED: filtro de volume minimo (CONTEXT.md)\n",
    "    .sort_values('score_medio_risco', ascending=False)\n",
    "    .head(20)                       # LOCKED: top-20 para caber na tabela de apresentacao\n",
    "    .reset_index(drop=True)\n",
    ")\n",
    "\n",
    "eligible_sellers = df_scored.groupby('seller_id').filter(lambda x: len(x) >= 10)['seller_id'].nunique()\n",
    "print(f'Vendedores com >= 10 pedidos: {eligible_sellers}')\n",
    "print(f'\\nTop-20 Vendedores por Score Medio de Risco:')\n",
    "print(seller_table.to_string(index=False))\n",
]

# ─── SECTION 7 cells ───────────────────────────────────────────────────────
cell_7_1_lines = [
    "# === SECAO 7: VERIFICACAO FINAL E ROUND-TRIP DOS JOBLIB ===\n",
    "\n",
    "# Celula 7.1 — Verificacao de artefatos gerados\n",
    "import os\n",
    "\n",
    "artefatos = {\n",
    "    'models/baseline_logreg.joblib': 'Pipeline LogReg (Secao 2)',\n",
    "    'models/final_pipeline.joblib': 'Pipeline XGBoost (Secao 3)',\n",
    "    'reports/figures/shap_beeswarm.png': 'SHAP beeswarm top-15 (Secao 4)',\n",
    "    'reports/figures/pr_curve.png': 'Curva PR com threshold (Secao 5)',\n",
    "}\n",
    "\n",
    "print('=== ARTEFATOS GERADOS ===')\n",
    "for path, desc in artefatos.items():\n",
    "    full_path = f'../{path}'\n",
    "    if os.path.exists(full_path):\n",
    "        size_kb = os.path.getsize(full_path) / 1024\n",
    "        print(f'OK: {path} ({size_kb:.1f} KB) — {desc}')\n",
    "    else:\n",
    "        print(f'MISSING: {path} — {desc}')\n",
    "\n",
    "all_exist = all(os.path.exists(f'../{p}') for p in artefatos)\n",
    "assert all_exist, 'Um ou mais artefatos estao faltando — re-executar secoes anteriores'\n",
    "print('\\nTodos os artefatos gerados com sucesso.')\n",
]

cell_7_2_lines = [
    "# Celula 7.2 — Round-trip dos dois pipelines\n",
    "print('=== ROUND-TRIP DOS PIPELINES ===')\n",
    "\n",
    "# Baseline\n",
    "loaded_baseline = joblib.load('../models/baseline_logreg.joblib')\n",
    "baseline_scores = loaded_baseline.predict_proba(X_test.head(5))[:, 1]\n",
    "assert len(baseline_scores) == 5, 'Round-trip baseline falhou'\n",
    "print(f'OK: baseline_logreg.joblib | 5 scores: {baseline_scores.round(3)}')\n",
    "\n",
    "# Final XGBoost\n",
    "loaded_final = joblib.load('../models/final_pipeline.joblib')\n",
    "final_scores = loaded_final.predict_proba(X_test.head(5))[:, 1]\n",
    "assert len(final_scores) == 5, 'Round-trip final_pipeline falhou'\n",
    "print(f'OK: final_pipeline.joblib | 5 scores: {final_scores.round(3)}')\n",
    "\n",
    "# Verificar que o pipeline final tem preprocessor (critico para o Streamlit)\n",
    "assert 'preprocessor' in loaded_final.named_steps, 'FAIL: preprocessor ausente no pipeline final carregado'\n",
    "assert 'classifier' in loaded_final.named_steps, 'FAIL: classifier ausente no pipeline final carregado'\n",
    "print('OK: pipeline final carregado tem preprocessor + classifier')\n",
]

cell_7_3_lines = [
    "# Celula 7.3 — Resumo final do notebook\n",
    "print('=== RESUMO FASE 4 ===')\n",
    "print(f'Dataset: {len(X):,} pedidos | Classe positiva: {y.mean():.1%}')\n",
    "print(f'\\nModelos:')\n",
    "print(f'  Baseline LogReg  | PR-AUC: {baseline_pr_auc:.4f}')\n",
    "print(f'  XGBoost Final    | PR-AUC: {final_pr_auc:.4f}')\n",
    "print(f'  Melhora: +{final_pr_auc - baseline_pr_auc:.4f}')\n",
    "print(f'\\nThreshold operacional: {chosen_threshold:.3f}')\n",
    "print(f'  Precision: {chosen_precision:.2f} | Recall: {chosen_recall:.2f}')\n",
    "print(f'  Pedidos flagrados/semana: {flagged_per_week:.0f}')\n",
    "print(f'  % real de risco: {chosen_precision:.0%}')\n",
    "print(f'\\nArtefatos para Phase 6 (Streamlit):')\n",
    "print('  models/baseline_logreg.joblib')\n",
    "print('  models/final_pipeline.joblib')\n",
    "print('\\nArtefatos para Phase 5 (Slides):')\n",
    "print('  reports/figures/shap_beeswarm.png')\n",
    "print('  reports/figures/pr_curve.png')\n",
    "print('\\nFASE 4 COMPLETA.')\n",
]

# ─── BUILD NEW CELLS ────────────────────────────────────────────────────────
new_cell_5_1 = make_code_cell("cell-5-1-threshold", cell_5_1_lines)
new_cell_5_2 = make_code_cell("cell-5-2-operational", cell_5_2_lines)
new_cell_5_3 = make_code_cell("cell-5-3-pr-curve", cell_5_3_lines)
new_cell_6_1 = make_code_cell("cell-6-1-seller-table", cell_6_1_lines)
new_cell_7_1 = make_code_cell("cell-7-1-artifacts", cell_7_1_lines)
new_cell_7_2 = make_code_cell("cell-7-2-roundtrip", cell_7_2_lines)
new_cell_7_3 = make_code_cell("cell-7-3-summary", cell_7_3_lines)

# ─── REPLACE PLACEHOLDER CELLS ──────────────────────────────────────────────
new_cells = []
for cell in nb["cells"]:
    cid = cell.get("id", "")
    if cid == "cell-5-placeholder":
        new_cells.extend([new_cell_5_1, new_cell_5_2, new_cell_5_3])
    elif cid == "cell-6-placeholder":
        new_cells.append(new_cell_6_1)
    elif cid == "cell-7-placeholder":
        new_cells.extend([new_cell_7_1, new_cell_7_2, new_cell_7_3])
    else:
        new_cells.append(cell)

nb["cells"] = new_cells

with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Done. Notebook now has {len(nb['cells'])} cells.")
