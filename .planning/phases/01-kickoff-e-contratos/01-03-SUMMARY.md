---
phase: 01-kickoff-e-contratos
plan: 03
subsystem: documentation
tags: [pr-auc, recall, metrics, class-imbalance, logistic-regression, machine-learning]

requires:
  - phase: 01-01
    provides: scaffold do repositorio com pasta docs/ criada

provides:
  - "docs/metrics_agreement.md com rationale completo de PR-AUC vs Accuracy/ROC-AUC"
  - "Politica de limiar de decisao documentada (curva PR, nao 0.5)"
  - "Requisito de baseline obrigatorio: Regressao Logistica com class_weight='balanced'"
  - "Estimativa de distribuicao de classes (~15-20% positivos) registrada"

affects:
  - 04-ml-pipeline
  - notebooks/FASE4-P4-ml-pipeline.ipynb

tech-stack:
  added: []
  patterns:
    - "Acordo social de metricas como guardrail antes de qualquer codigo ML"
    - "PR-AUC como headline metric em datasets desbalanceados"
    - "Baseline logistico obrigatorio como pre-requisito para modelos avancados"

key-files:
  created:
    - docs/metrics_agreement.md
  modified: []

key-decisions:
  - "PR-AUC e Recall (classe positiva) sao as unicas headline metrics — documentado com rationale"
  - "Accuracy e ROC-AUC sao explicitamente proibidos como headline metrics por enganarem em datasets desbalanceados"
  - "Limiar de decisao escolhido na curva PR (nao 0.5) — criterio: maximizar F1 ou acionabilidade operacional"
  - "Regressao Logistica com class_weight='balanced' e baseline obrigatorio antes do XGBoost"

patterns-established:
  - "metrics_agreement.md como referencia normativa para Phase 4 — qualquer desvio requer justificativa explicita"

requirements-completed: [KICK-02]

duration: 3min
completed: 2026-03-01
---

# Phase 1 Plan 03: Metrics Agreement Summary

**Acordo formal de metricas para o modelo Olist registrado em docs/metrics_agreement.md — PR-AUC e Recall como primarias, Accuracy e ROC-AUC proibidos como headline, limiar via curva PR, baseline logistico obrigatorio antes do XGBoost**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-01T18:11:00Z
- **Completed:** 2026-03-01T18:14:00Z
- **Tasks:** 1 of 1
- **Files modified:** 1

## Accomplishments

- Documento docs/metrics_agreement.md criado com todas as secoes obrigatorias e rationale completo
- Explicacao clara de por que Accuracy falha (exemplo concreto: 83% acertando "sempre bom") e por que ROC-AUC e insuficiente (insensivel ao imbalance)
- Politica de limiar documentada: curva PR em Phase 4, criterio F1 ou acionabilidade operacional
- Baseline obrigatorio registrado: Regressao Logistica com class_weight='balanced' antes de qualquer modelo avancado

## Task Commits

1. **Task 1: Criar docs/metrics_agreement.md** - `460b8e4` (feat)

**Plan metadata:** [pendente — criado apos SUMMARY]

## Files Created/Modified

- `docs/metrics_agreement.md` - Acordo formal de metricas: PR-AUC/Recall primarias, Accuracy/ROC-AUC proibidas, politica de limiar, requisito de baseline logistico

## Decisions Made

- PR-AUC escolhido como headline metric por ser sensivel ao imbalance e medir diretamente a classe positiva minoritaria
- Accuracy e ROC-AUC documentados como proibidos — accuracy mascara falha total na classe positiva; ROC-AUC ignora o imbalance
- Limiar de decisao: nao 0.5, mas escolhido na curva PR da Phase 4 (maximizar F1 ou acionabilidade operacional)
- Baseline logistico com class_weight='balanced' obrigatorio — garante entregavel e valida valor do XGBoost

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- docs/metrics_agreement.md esta pronto para ser referenciado no notebook FASE4-P4-ml-pipeline.ipynb
- Phase 4 deve reportar PR-AUC e Recall conforme este acordo, com limiar escolhido na curva PR
- Proporcao real da classe positiva deve ser verificada na primeira celula do FASE2-P1 (nota inclusa no documento)

---
*Phase: 01-kickoff-e-contratos*
*Completed: 2026-03-01*
