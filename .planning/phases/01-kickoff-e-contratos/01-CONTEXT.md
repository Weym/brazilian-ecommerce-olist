# Phase 1: Kickoff e Contratos - Context

**Gathered:** 2026-03-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Documentar e distribuir todos os guardrails críticos do sprint — contrato de features pré-entrega, métricas primárias, target do modelo, recorte temporal, ownership de notebooks e estrutura do repositório — antes de qualquer linha de código de análise ou join ser escrita. Não inclui construção da tabela gold nem análise de dados.

</domain>

<decisions>
## Implementation Decisions

### Contrato de Features Pré-Entrega

- Formato: arquivo Python `src/features.py` com constante `PRE_DELIVERY_FEATURES` (lista de strings com nomes de colunas permitidas) + `FORBIDDEN_FEATURES` (colunas proibidas por serem pós-entrega)
- Documento legível complementar: `docs/feature_contract.md` com tabela explícita de cada coluna, sua origem e tag `[pré-entrega | pós-entrega | target]`
- Colunas proibidas incluem obrigatoriamente: `order_delivered_customer_date`, `review_score`, `review_comment_message`, `review_creation_date`, qualquer variável derivada de entrega real
- O corte temporal usa `order_approved_at` como âncora (não `order_purchase_timestamp`)

### Métricas Primárias

- Métrica principal do modelo: **PR-AUC** (Precision-Recall AUC) e **Recall** para a classe positiva (reviews 1-2 estrelas)
- Accuracy e ROC-AUC são explicitamente proibidos como headline metrics — documentar o motivo (dataset desbalanceado ~15-20% de positivos)
- Limiar de decisão será escolhido na curva PR, não a 0.5 padrão
- Baseline: Regressão Logística com `class_weight='balanced'` como obrigatório antes de qualquer modelo avançado

### Target do Modelo

- Target binário: `review_score` ∈ {1, 2} → positivo (1), `review_score` ∈ {3, 4, 5} → negativo (0)
- Nome da coluna target na tabela gold: `bad_review` (booleano)
- Rationale documentado: definição rigorosa e defensável, separa insatisfação real de neutros

### Estrutura do Repositório

- Convenção de nomes de notebooks: `FASE{N}-PESSOA{N}-descricao.ipynb` (ex.: `FASE2-P1-data-foundation.ipynb`)
- Estrutura de pastas padronizada:
  ```
  data/raw/          ← CSVs originais da Olist (nunca modificados)
  data/gold/         ← olist_gold.parquet (contrato imutável)
  notebooks/         ← notebooks por fase/pessoa
  src/               ← módulos Python reutilizáveis (features.py, utils.py)
  models/            ← artefatos serializados (.joblib)
  reports/figures/   ← imagens exportadas para slides
  app/               ← código Streamlit
  docs/              ← documentação (feature_contract.md, data_dictionary.md)
  ```
- Regras de git: notebooks devem ter outputs limpos antes de commit (usar `nbstripout` ou convenção manual); sem paths hardcoded (usar `pathlib.Path(__file__).parent`)

### Recorte Temporal e Outliers

- Janela de dados: usar todos os pedidos com `order_approved_at` disponível (não filtrar por data de compra)
- Pedidos excluídos: status `canceled`, `unavailable` — somente pedidos com review entregue entram no modelo
- Outlier de frete: não remover, mas flaggar pedidos com frete > 3 desvios-padrão para análise exploratória
- Outlier de prazo: pedidos com atraso > 30 dias são incluídos na EDA mas podem ser tratados separadamente no ML (documentar decisão)

### Ownership de Notebooks

| Pessoa | Área | Notebooks |
|--------|------|-----------|
| P1 — Data Lead | Data Foundation | FASE2-P1-*.ipynb |
| P2 — Geo/Logística | Geo Analysis | FASE3-P2-*.ipynb |
| P3 — EDA & Métricas | EDA | FASE3-P3-*.ipynb |
| P4 — ML Lead | ML Pipeline | FASE4-P4-*.ipynb |
| P5 — NLP/Reviews | Reviews NLP | FASE3-P5-*.ipynb (opcional) |
| P6 — Storytelling | Apresentação | Coordena deck e app/ |

### Claude's Discretion

- Formato exato do `requirements.txt` / `pyproject.toml` — usar o que o time já conhece
- Ferramenta de limpeza de outputs de notebooks (nbstripout vs hook manual vs convenção)
- Template de notebook inicial (importações padrão, configurações de display)

</decisions>

<specifics>
## Specific Ideas

- O `feature_contract.md` deve ser impresso/colado no canal do time no início do sprint — visibilidade constante reduz o risco de leakage acidental
- O `src/features.py` é o único arquivo de código que deve ser criado na Fase 1 — todo o resto é documentação e estrutura
- Sugestão de documento de kickoff de 1 página: Seções = Target | Feature Contract | Métricas | Estrutura | Ownership — cada seção assinada/confirmada por todos no kickoff

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- Nenhum — projeto greenfield, primeiro sprint

### Established Patterns
- Nenhum estabelecido ainda — as decisões desta fase CRIAM os padrões para todas as fases subsequentes

### Integration Points
- `src/features.py` → importado por FASE4-P4 (ML Pipeline) e `app/` (Streamlit preditor)
- Estrutura de `data/gold/` definida aqui → contrato para todas as outras fases

</code_context>

<deferred>
## Deferred Ideas

- Nenhuma — discussão ficou dentro do escopo da Fase 1

</deferred>

---

*Phase: 01-kickoff-e-contratos*
*Context gathered: 2026-03-01*
