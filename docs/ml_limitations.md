# ML Model Limitations — Olist Pre-Delivery Risk

**Phase 4 documented limitation — referencia para Phase 5 (slides) e Phase 6 (Streamlit)**

---

## Limitacao Principal: Alta Precisao, Baixo Recall

| Metrica | Valor | Criterio | Status |
|---------|-------|----------|--------|
| PR-AUC (XGBoost) | 0.2283 | > baseline (0.2207) | SATISFEITO |
| PR-AUC (Baseline LogReg) | 0.2207 | — | referencia |
| Precision no threshold | 0.40 | >= 0.40 (primario) | SATISFEITO |
| Recall no threshold | 0.02 | >= 0.60 (secundario) | NAO ATINGIDO |
| Threshold selecionado | 0.785 | primeiro ponto Precision >= 0.40 | — |

**Estimativa operacional (volume Olist ~2 anos, 97.456 pedidos):**
- Pedidos flagrados por semana: **8**
- Percentual de risco real entre os flagrados: **40%** (Precision = 0.40)
- Percentual de pedidos em risco capturados: **2%** (Recall = 0.02)

---

## Por que o Modelo Nao Atinge Recall >= 0.60

O modelo XGBoost treinado nas 13 features pre-entrega tem PR-AUC = 0.2283 em um dataset com 13.9% de positivos. Esta performance reflete que **as features disponiveis antes da entrega tem poder preditivo limitado** — a satisfacao do cliente e determinada por muitos fatores pos-entrega que o modelo nao pode observar por definicao (resultado da entrega, estado do produto, atendimento).

Para atingir Recall = 0.60 com as features atuais seria necessario usar threshold ~0.14:
- Precision cairia para ~0.18 (82% de falsos alarmes)
- Pedidos flagrados por semana: ~540 (vs. 8 atual)
- Operacionalmente inviavel para qualquer time de atendimento

**A escolha de Precision >= 0.40 e uma decisao operacional, nao uma falha do modelo.**

---

## Framing para Slides (Ato 2)

### Narrativa recomendada

> "O modelo de alerta precoce opera em modo cirurgico: **40% dos pedidos que ele alerta sao de fato riscos reais**. Com 8 alertas por semana, o time de operacoes tem uma carga de trabalho humanamente gerenciavel para intervir antes que o problema chegue ao cliente."

### O que NAO dizer

- NAO: "O modelo detecta 60% dos pedidos em risco" — isso e falso (Recall = 0.02)
- NAO: "O modelo e impreciso" — Precision = 0.40 e bem superior ao baseline aleatorio (~0.14)
- NAO omitir o recall baixo — audiencia tecnica perceberá; honestidade constrói credibilidade

### Slide de limitacoes (recomendado no Apendice Tecnico)

Incluir um slide honesto com o tradeoff Precision/Recall visualizado na curva PR:
- Mostrar onde o threshold 0.785 esta na curva (extremo direito, alta precisao)
- Mostrar o tradeoff: mover o threshold para a esquerda aumenta recall mas explode os falsos alarmes
- Mensagem: "Escolhemos cirurgia, nao rastreio em massa"

---

## Impacto na Phase 6 (Streamlit Demo)

O predictor no Streamlit deve exibir:
- Score de risco (probabilidade bruta do modelo) — sempre util
- Indicacao de "ALTO RISCO" apenas quando score > threshold (0.785)
- Aviso contextual: "Este modelo alerta com 40% de precisao — 8 casos/semana em media"

Evitar exibir Recall na UI — e tecnicamente correto mas confuso para audiencia nao-tecnica.

---

## Referencias Tecnicas

- Notebook: `notebooks/FASE4-P4-ml-pipeline.ipynb` — Secao 5 (Threshold + Operational Estimate)
- Curva PR: `reports/figures/pr_curve.png` — ponto vermelho em Precision=0.40, Recall=0.02
- SHAP beeswarm: `reports/figures/shap_beeswarm.png` — top features explicam o modelo
- Joblib: `models/final_pipeline.joblib` — pipeline completo para Streamlit

---

*Gerado em Phase 4 gap closure — 2026-03-01*
*Referencia para: Phase 5 (docs/slides_outline.md) e Phase 6 (app/pages/2_Preditor.py)*
