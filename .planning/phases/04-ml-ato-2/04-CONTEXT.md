# Phase 4: ML — Ato 2 - Context

**Gathered:** 2026-03-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Pipeline completo de risco pré-entrega: features validadas → baseline logístico → XGBoost com SHAP → limiar de decisão com estimativa operacional → tabela de vendedores → pipeline serializado como .joblib. Tudo consumido por Phase 5 (slides) e Phase 6 (Streamlit). A fronteira é a âncora temporal `order_approved_at` — nenhuma feature pós-entrega entra na matriz X.

</domain>

<decisions>
## Implementation Decisions

### Balanceamento de classes
- `class_weight='balanced'` em ambos os modelos: LogisticRegression e XGBoost
- Sem SMOTE — sprint de 1 semana, sem tempo para debugar dados sintéticos
- SHAP funciona normalmente com `class_weight`

### Critério do limiar de decisão (ML-05)
- Cortar a curva PR no ponto onde **Precision ≥ 0.40** (critério primário)
- Conferir que Recall ≥ 0.60 no ponto escolhido (critério secundário)
- Estimativa operacional calculada no threshold escolhido: pedidos flagrados/semana e % real de risco entre os flagrados
- Narrativa para o slide: "40% dos pedidos flagrados são de fato risco real"

### Agregação por vendedor (ML-06)
- Score médio de risco por vendedor, ordenado maior → menor
- Mínimo de **10 pedidos** para entrar na tabela (vendedores com menos têm scores instáveis)
- Exibir **top-20 vendedores** no slide — cabe numa tabela de apresentação
- Coluna de referência: contagem de pedidos do vendedor (contexto de volume)

### Estrutura do notebook ML
- Um único notebook: `FASE4-P4-ml-pipeline.ipynb`
- Seções marcadas internamente: (1) Load & feature matrix, (2) Baseline LogReg, (3) XGBoost, (4) SHAP, (5) Threshold + operational estimate, (6) Seller table, (7) Serialize .joblib
- Mais fácil de reproduzir de ponta a ponta e de apresentar como trilha técnica auditável

### Claude's Discretion
- Hiperparâmetros do XGBoost (n_estimators, max_depth, learning_rate) — defaults razoáveis, sem GridSearchCV extenso
- Pipeline sklearn interno: ColumnTransformer com OneHotEncoder para categóricas + StandardScaler para numéricas, depois o estimador
- Divisão treino/test: 80/20 estratificado por `bad_review`
- Formato do SHAP beeswarm: test set, top-15 features, salvo em `reports/figures/shap_beeswarm.png`
- Calibração de probabilidades: não (scores brutos são suficientes para ranking de vendedores)

</decisions>

<specifics>
## Specific Ideas

- "40% dos pedidos flagrados são de fato risco real" — frase para o slide do Ato 2
- Tabela de vendedores deve ter no mínimo: seller_id, score_medio_risco, total_pedidos, pedidos_alto_risco
- O .joblib serializado deve incluir todo o pipeline (pré-processamento + modelo), não só o estimador — para que o Streamlit carregue e prediga sem reconstruir transformações

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/features.py`: `PRE_DELIVERY_FEATURES` (13 colunas), `FORBIDDEN_FEATURES`, `TARGET_COLUMN = "bad_review"` — importar diretamente no notebook
- `data/gold/olist_gold.parquet`: tabela gold da Phase 2 — `pd.read_parquet(...)` direto, sem joins adicionais
- `models/`: pasta existe (criada na Phase 1) — destino de `baseline_logreg.joblib` e `final_pipeline.joblib`
- `reports/figures/`: pasta existe — destino de `shap_beeswarm.png` e `pr_curve.png`

### Established Patterns
- Âncora temporal: `order_approved_at` — nenhum cálculo usa datas posteriores como input
- Métrica primária: PR-AUC e Recall — não accuracy, não ROC-AUC (decisão do KICK-02)
- Serialização: `.joblib` (já no requirements.txt) — padrão do projeto para artefatos ML

### Integration Points
- `from src.features import PRE_DELIVERY_FEATURES` — o notebook filtra a matriz X usando essa lista
- `models/final_pipeline.joblib` → consumido por `app/pages/03_modelo.py` na Phase 6
- `reports/figures/shap_beeswarm.png` + `reports/figures/pr_curve.png` → consumidos pelos slides da Phase 5

</code_context>

<deferred>
## Deferred Ideas

- Nenhuma ideia de escopo adicional surgiu — discussão ficou dentro da fronteira da fase

</deferred>

---

*Phase: 04-ml-ato-2*
*Context gathered: 2026-03-01*
