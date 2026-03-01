---
phase: 01-kickoff-e-contratos
plan: 01
subsystem: infra
tags: [nbstripout, jupyter, pandas, xgboost, streamlit, scaffold]

requires: []
provides:
  - Estrutura de pastas do projeto (data/raw, data/gold, data/processed, notebooks, src, models, reports/figures, app, docs)
  - Filtro nbstripout registrado em .gitattributes para *.ipynb (modo git filter)
  - requirements.txt com dependencias pinadas do projeto
  - README.md com instrucoes de setup, estrutura de pastas e convencao de notebooks
affects:
  - 01-02 (src/ disponivel para features.py)
  - 01-03 (docs/ disponivel para contratos)
  - 02-data-foundation (data/raw/, data/gold/, data/processed/ prontos)
  - todos os planos subsequentes (scaffold desbloqueia trabalho paralelo)

tech-stack:
  added: [nbstripout>=0.7, pandas>=2.0, numpy>=1.26, scikit-learn>=1.4, xgboost>=2.0, shap>=0.44, pyarrow>=14.0, matplotlib>=3.8, seaborn>=0.13, plotly>=5.18, geopy>=2.4, streamlit>=1.32, joblib>=1.3, python-dotenv>=1.0, jupyter>=1.0, ipykernel>=6.0]
  patterns:
    - "nbstripout em modo git filter (nao pre-commit hook) — working copy nao modificada"
    - "Convencao de notebooks: FASE{N}-P{N}-descricao.ipynb"
    - "data/raw/ imutavel — CSVs originais nunca modificados"

key-files:
  created:
    - .gitattributes
    - requirements.txt
    - README.md
    - data/raw/.gitkeep
    - data/gold/.gitkeep
    - data/processed/.gitkeep
    - notebooks/.gitkeep
    - src/.gitkeep
    - models/.gitkeep
    - reports/figures/.gitkeep
    - app/.gitkeep
    - docs/.gitkeep
  modified: []

key-decisions:
  - "nbstripout configurado em modo git filter (nao hook) — working copy preservada, outputs filtrados apenas no staging"
  - "requirements.txt (nao pyproject.toml) — mais simples para sprint de 1 semana"
  - "src/__init__.py e src/features.py excluidos deste plano — responsabilidade do Plan 02"

patterns-established:
  - "Convencao de notebooks: FASE{N}-P{N}-descricao.ipynb"
  - "data/raw/ e imutavel — nunca modificar CSVs originais"
  - "nbstripout --install --attributes .gitattributes obrigatorio para todos os contribuidores apos clone"

requirements-completed: [KICK-03]

duration: 2min
completed: 2026-03-01
---

# Phase 01 Plan 01: Kickoff e Contratos — Scaffold do Repositorio Summary

**Scaffold completo com 9 pastas rastreadas por git, filtro nbstripout em modo git filter para notebooks, dependencias pinadas em requirements.txt e README com setup obrigatorio.**

## Performance

- **Duration:** 2 min
- **Started:** 2026-03-01T21:06:23Z
- **Completed:** 2026-03-01T21:07:59Z
- **Tasks:** 2
- **Files modified:** 12

## Accomplishments

- 9 pastas do projeto criadas com .gitkeep para rastreamento pelo git (data/raw, data/gold, data/processed, notebooks, src, models, reports/figures, app, docs)
- .gitattributes configurado com filtro nbstripout em modo git filter para *.ipynb — outputs de notebooks nunca commitados
- requirements.txt com dependencias pinadas cobrindo data science, ML, visualizacao, geoespacial, Streamlit e ferramentas de notebook
- README.md com visao geral do projeto, estrutura de pastas, instrucoes de setup passo-a-passo e convencao de notebooks

## Task Commits

Cada task foi commitada atomicamente:

1. **Task 1: Criar estrutura de pastas e .gitkeep** - `e649620` (chore)
2. **Task 2: Criar .gitattributes, requirements.txt e README.md** - `544898d` (chore)

## Files Created/Modified

- `.gitattributes` - Filtro nbstripout em modo git filter para *.ipynb e diff=ipynb
- `requirements.txt` - Dependencias pinadas: pandas, numpy, sklearn, xgboost, shap, pyarrow, matplotlib, seaborn, plotly, geopy, streamlit, nbstripout, jupyter, joblib, python-dotenv
- `README.md` - Documentacao de entrada: titulo, estrutura de pastas, setup com nbstripout obrigatorio, convencao de notebooks, secao de dados e reproducao
- `data/raw/.gitkeep` - Pasta para CSVs originais (imutavel)
- `data/gold/.gitkeep` - Pasta para olist_gold.parquet (contrato imutavel)
- `data/processed/.gitkeep` - Pasta para agregacoes intermediarias
- `notebooks/.gitkeep` - Pasta para notebooks por fase
- `src/.gitkeep` - Pasta para modulos Python (receberá features.py no Plan 02)
- `models/.gitkeep` - Pasta para artefatos serializados .joblib
- `reports/figures/.gitkeep` - Pasta para imagens exportadas para slides
- `app/.gitkeep` - Pasta para codigo Streamlit
- `docs/.gitkeep` - Pasta para documentacao

## Decisions Made

- nbstripout configurado em modo git filter (nao pre-commit hook): working copy local nao e modificada, apenas o que git ve antes do commit e filtrado. Isso evita confusao de "meu notebook mudou sem eu fazer nada".
- requirements.txt escolhido em vez de pyproject.toml: mais simples e direto para sprint de 1 semana com equipe pequena.
- src/__init__.py e src/features.py excluidos intencionalmente deste plano: responsabilidade do Plan 02 para manter separacao de responsabilidades.

## Deviations from Plan

None - plano executado exatamente como escrito.

## Issues Encountered

Nenhum. Python inline (`python -c`) apresentou erro de sintaxe no shell Windows, verificacao feita com comandos bash nativos (grep, ls) com resultado equivalente.

## User Setup Required

None - nenhuma configuracao de servico externo necessaria. Contribuidores devem rodar `nbstripout --install --attributes .gitattributes` apos clonar (documentado no README.md).

## Next Phase Readiness

- Scaffold completo desbloqueia todos os planos paralelos da Phase 1 (Plans 02-05)
- Plan 02 pode criar src/__init__.py e src/features.py imediatamente
- Plan 03 pode criar docs/feature_contract.md e docs/metrics_agreement.md imediatamente
- data/raw/ pronta para receber CSVs da Olist (Phase 2)

---
*Phase: 01-kickoff-e-contratos*
*Completed: 2026-03-01*
