---
phase: 01-kickoff-e-contratos
plan: "04"
subsystem: documentation
tags: [olist, kickoff, target-definition, feature-contract, outlier-policy, data-governance]

requires:
  - phase: 01-01
    provides: repository scaffold (docs/ directory, project structure)

provides:
  - "docs/kickoff.md — documento unificado de kickoff com target, ancora temporal e regras de outlier"
  - "Target bad_review definido formalmente: review_score in {1,2} = 1, caso contrario 0"
  - "Ancora temporal order_approved_at documentada e order_purchase_timestamp explicitamente proibido"
  - "Filtros de inclusao documentados: excluir canceled, unavailable, pedidos sem review"
  - "Outlier de frete: flaggar high_freight_flag (nao remover), threshold = media + 3*std"
  - "Outlier de prazo: atraso > 30 dias incluido na EDA; decisao ML deferida para Phase 4"

affects:
  - 02-data-foundation
  - 03-eda-ato-1
  - 04-ml-pipeline

tech-stack:
  added: []
  patterns:
    - "Kickoff document as contract: decisoes criticas documentadas antes de qualquer codigo de analise"
    - "Single-file decision reference: tabela de resumo legivel em 30 segundos"

key-files:
  created:
    - docs/kickoff.md
  modified: []

key-decisions:
  - "Target = bad_review: review_score in {1,2} -> 1, caso contrario 0 (int8)"
  - "Ancora temporal = order_approved_at (nao order_purchase_timestamp)"
  - "Outlier de frete: flaggar com high_freight_flag, nao remover (pode ser sinal forte)"
  - "Outlier de prazo >30 dias: incluir na EDA; Phase 4 decide tratamento para ML"
  - "Pedidos excluidos: status canceled/unavailable e pedidos sem review (inner join)"

patterns-established:
  - "Pattern 1: Kickoff doc como contrato — lido obrigatoriamente antes da Phase 2"
  - "Pattern 2: Derivacao Python documentada no artefato — df['bad_review'] = df['review_score'].isin([1, 2]).astype(int)"

requirements-completed: [KICK-04, KICK-05]

duration: 5min
completed: 2026-03-01
---

# Phase 01 Plan 04: Kickoff Document Summary

**Documento de kickoff `docs/kickoff.md` criado com 5 secoes: target binario `bad_review` (review 1-2 estrelas), ancora temporal `order_approved_at`, filtros de inclusao (excluir canceled/unavailable), regra de outlier de frete (flaggar, nao remover) e prazo (>30 dias na EDA).**

## Performance

- **Duration:** 5 min
- **Started:** 2026-03-01T21:11:01Z
- **Completed:** 2026-03-01T21:16:00Z
- **Tasks:** 1 completed
- **Files modified:** 1

## Accomplishments

- Documento `docs/kickoff.md` criado com todas as cinco secoes obrigatorias (KICK-04 e KICK-05)
- Target `bad_review` documentado: definicao, tabela de mapeamento, codigo Python de derivacao, rationale
- Ancora temporal `order_approved_at` documentada com exemplo de codigo e explicacao de por que `order_purchase_timestamp` e proibido
- Filtros de inclusao e exclusao claros: pedidos com status canceled/unavailable excluidos, inner join com reviews
- Regras de outlier escritas antes da construcao da tabela gold: frete (flaggar com `high_freight_flag`) e prazo (>30 dias na EDA)
- Tabela de resumo de decisoes com responsaveis (P1 e P4) legivel em 30 segundos

## Task Commits

1. **Task 1: Criar docs/kickoff.md** - `7129ce0` (feat)

**Plan metadata:** (a ser adicionado no commit final de docs)

## Files Created/Modified

- `docs/kickoff.md` - Documento unificado de kickoff: target do modelo, ancora temporal, janela de dados, regras de outlier e tabela de decisoes

## Decisions Made

- Target `bad_review` = 1 se `review_score` in {1,2} — definicao rigorosa que separa insatisfacao real (1-2) de neutros (3)
- Ancora temporal: `order_approved_at` (nao `order_purchase_timestamp`) — evita vazamento em pedidos com aprovacao atrasada
- Outlier de frete: policy "flaggar, nao remover" — fretes extremos podem ser sinal forte de insatisfacao
- Outlier de prazo: >30 dias incluido na EDA, Phase 4 decide tratamento para ML — responsabilidade deferida explicitamente

## Deviations from Plan

None — plan executado exatamente como especificado.

## Issues Encountered

None.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- `docs/kickoff.md` esta pronto para ser consultado antes de abrir qualquer notebook da Phase 2
- P1 (Data Lead) tem todas as regras necessarias para construir a tabela gold: filtros, ancora temporal, derivacao do target
- P4 (ML Lead) tem a definicao formal do target e a responsabilidade de tratar outliers de prazo no Phase 4
- Blocker ja registrado: proporcao real de bad_review=1 deve ser confirmada na Phase 2 (estimativa: 15-20%)

---
*Phase: 01-kickoff-e-contratos*
*Completed: 2026-03-01*
