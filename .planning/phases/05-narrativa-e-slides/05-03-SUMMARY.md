---
phase: 05-narrativa-e-slides
plan: 03
subsystem: presentation
tags: [slides, google-slides, narrative, deck, outline, presentation]

# Dependency graph
requires:
  - phase: 05-02
    provides: docs/report.md com metricas validadas e README atualizado
  - phase: 04-ml-ato-2
    provides: reports/figures/shap_beeswarm.png e pr_curve.png, metricas do modelo
  - phase: 03-eda-ato-1
    provides: reports/figures/ com figuras EDA (choropleth, heatmap, boxplots)
provides:
  - docs/slides_outline.md — roteiro completo do deck com 18 slides principais + 5 slides de apendice
  - Inventario de figuras mapeado para slides especificos
  - Tabela top-10 vendedores de risco com dados reais
  - Deck Google Slides marcado como PENDENTE em docs/slides_outline.md — construcao manual segue o roteiro
affects:
  - 06-demo-streamlit (apresentacao final, artefatos de apresentacao)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - Roteiro de deck como documento de verdade — texto copiavel para Google Slides sem placeholders
    - Mapeamento figura-para-slide explícito como inventario no topo do documento

key-files:
  created:
    - docs/slides_outline.md
    - scripts/get_seller_risk_table.py
    - scripts/verify_task1.py
  modified: []

key-decisions:
  - "slides_outline.md usa nomes reais dos arquivos de reports/figures/ — sem nome generico como [figura_EDA]"
  - "Tabela de vendedores usa top-10 (nao top-5) para dar mais opcao ao presenter escolher escala"
  - "Score de risco exibido com 3 casas decimais para granularidade acionavel"

patterns-established:
  - "Roteiro-primeiro: documento de texto completo antes de construir o deck — garante consistencia numerica"
  - "Frase-ancora operacional em destaque visual no Slide 13: '40% dos pedidos flagrados sao risco real'"

requirements-completed: [PRES-01]

# Metrics
duration: 3min
completed: 2026-03-02
---

# Phase 5 Plan 03: Slides Outline Summary

**Roteiro completo do deck entregue em docs/slides_outline.md — 18 slides principais + 5 apendice com metricas reais de docs/report.md e inventario de 9 figuras mapeadas para slides especificos; deck Google Slides marcado como PENDENTE de construcao manual**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-02T00:18:41Z
- **Completed:** 2026-03-02T00:21:16Z
- **Tasks:** 2 de 2 concluidas (Task 1: auto; Task 2: checkpoint:human-action encerrado)
- **Files modified:** 3

## Accomplishments
- Inventario completo de 9 figuras em reports/figures/ com mapeamento explicito para slides (eda01-boxplot, eda01-scatter, eda02-frete, eda03-choropleth, eda04-categorias, eda05-heatmap, pr_curve, shap_beeswarm)
- Roteiro docs/slides_outline.md com 18 slides principais (INTRODUCAO + ATO 1 + ATO 2 + CONCLUSAO) sem nenhum placeholder — todos os valores extraidos de docs/report.md
- Tabela top-10 vendedores de risco calculada com pipeline final (threshold=0.785, elegibilidade >= 10 pedidos) e inserida no Slide 15
- 5 slides de apendice tecnico (A1-A5) com metricas completas, metodologia, SHAP ampliado, hiperparametros e limitacoes

## Task Commits

1. **Task 1: Inventariar figuras e criar slides_outline.md** - `171dc57` (feat)
2. **Task 2: Marcar deck como pendente (closure do checkpoint)** - `2773d55` (chore)

**Plan metadata:** *(este commit — docs: complete plan)*

## Files Created/Modified
- `docs/slides_outline.md` — Roteiro completo do deck com 18 slides + 5 apendice, todas as metricas reais, tabela top-10 vendedores e mapeamento de figuras
- `scripts/get_seller_risk_table.py` — Script auxiliar para calcular tabela de vendedores de risco via pipeline final
- `scripts/verify_task1.py` — Script de verificacao automatica da Task 1

## Decisions Made
- Tabela top-10 de vendedores (nao top-5) para dar mais opcao ao presenter escolher a escala da tabela no slide
- Score medio de risco exibido com 3 casas decimais para granularidade na priorização operacional
- Inventario de figuras colocado no topo do slides_outline.md como referencia rapida durante construcao do deck

## Deviations from Plan

None — Task 1 executada exatamente como especificado. Task 2 nao executavel por ser checkpoint:human-action.

## Issues Encountered

None.

## User Setup Required

**Acao pendente: construir o deck no Google Slides seguindo docs/slides_outline.md.**

O roteiro esta completo — todos os numeros, bullets e notas do presenter estao prontos para copiar.

1. Abrir Google Slides (slides.google.com) e criar nova apresentacao
2. Para cada slide em docs/slides_outline.md: inserir titulo, corpo e figuras conforme o roteiro
3. Para figuras EDA: arrastar de reports/figures/ para o slide correspondente
4. Para slides 12 (pr_curve.png) e 14 (shap_beeswarm.png): inserir diretamente de reports/figures/
5. Para slide 15 (tabela de vendedores): copiar tabela do roteiro para o Google Slides
6. Adicionar apendice tecnico (slides A1-A5) apos o slide 18
7. Compartilhar com permissao de visualizacao e obter link compartilhavel
8. Atualizar o campo "**Deck:**" em docs/slides_outline.md com o link compartilhavel

Checklist de verificacao antes de finalizar:
- [ ] 18 slides principais + pelo menos 5 slides de apendice
- [ ] Slide 13 tem "40% dos pedidos flagrados" em destaque visual
- [ ] Figuras inseridas nos slides corretos (nao em slides errados)
- [ ] Numeros batem com docs/report.md (PR-AUC 0,2283, threshold 0,785, 8 pedidos/semana)
- [ ] Link compartilhavel obtido e registrado em slides_outline.md

## Next Phase Readiness
- docs/slides_outline.md pronto como fonte de verdade para construcao do deck
- reports/figures/ com 9 figuras prontas para inserir nos slides
- Apos Task 2 (deck pronto + link registrado): plan 05-03 concluido
- Phase 6 (demo Streamlit) pode prosseguir em paralelo — nao depende do deck

---
*Phase: 05-narrativa-e-slides*
*Completed: 2026-03-02*

## Self-Check: PASSED

- [FOUND] docs/slides_outline.md - 171dc57 (Task 1) + 2773d55 (Task 2 closure)
- [FOUND] scripts/get_seller_risk_table.py - 171dc57
- [FOUND] scripts/verify_task1.py - 171dc57
- Verification script output: PASS com todos os 9 marcadores presentes
- Deck field updated to PENDENTE marker in 2773d55
