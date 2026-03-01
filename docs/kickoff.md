# Kickoff Document — Olist Pre-Delivery Risk Model

> **Status:** Finalizado na Phase 1 (Kickoff e Contratos)
> Deve ser lido antes de abrir qualquer notebook da Phase 2.

---

## 1. Target do Modelo

**Definicao:** Avaliacao ruim = `review_score` in {1, 2}
**Nome da coluna na tabela gold:** `bad_review`
**Tipo:** Binario (int8)

| review_score | bad_review | Interpretacao          |
|:------------:|:----------:|------------------------|
| 1            | 1          | Insatisfacao severa     |
| 2            | 1          | Insatisfacao moderada   |
| 3            | 0          | Neutro                  |
| 4            | 0          | Satisfacao moderada     |
| 5            | 0          | Satisfacao plena        |

**Derivacao (Python):**

```python
df["bad_review"] = df["review_score"].isin([1, 2]).astype(int)
```

**Rationale:**

- Estrelas 1-2 representam insatisfacao real e defensavel — nao e ambiguo como estrela 3 (neutro)
- A separacao {1,2} vs {3,4,5} produz um sinal binario limpo para o modelo de classificacao
- Estrela 3 e deliberadamente excluida do positivo para evitar ruido de clientes "mornos"
- Distribuicao esperada: ~15-20% de positivos (bad_review=1) — confirmar na Phase 2 com `df["bad_review"].value_counts(normalize=True)`

**Referencia de codigo:** `src/features.py` — constante `TARGET_COLUMN = "bad_review"`

---

## 2. Ancora Temporal

**Variavel ancora:** `order_approved_at`
**Variavel PROIBIDA como ancora:** `order_purchase_timestamp`

**Rationale:**

Usar `order_purchase_timestamp` causaria vazamento de pedidos com aprovacao atrasada, distorcendo `estimated_delivery_days` e outras features pre-entrega. A ancora correta e o momento em que o pedido foi aprovado para envio — a partir dai, todas as features devem ser calculadas.

**Regra de derivacao de features temporais:**

```python
# CORRETO: ancora em order_approved_at
df["estimated_delivery_days"] = (
    df["order_estimated_delivery_date"] - df["order_approved_at"]
).dt.days

# PROIBIDO: ancora em order_purchase_timestamp
# df["estimated_delivery_days"] = (
#     df["order_estimated_delivery_date"] - df["order_purchase_timestamp"]
# ).dt.days  # <- ERRADO
```

**Principio geral:** Toda feature no modelo deve ser calculada como `valor - order_approved_at` ou `valor no momento da aprovacao`. Qualquer feature que requer informacao posterior a `order_approved_at` e pos-entrega e proibida.

---

## 3. Janela de Dados e Filtros de Inclusao

**Dataset Olist:** abrange set/2016 a ago/2018.
**Politica de janela:** usar todo o historico disponivel — nao filtrar por data de compra.

### Pedidos INCLUIDOS na tabela gold

- Todos os pedidos com `order_approved_at` nao-nulo (aprovacao confirmada)
- Todos os pedidos com review disponivel (inner join com `order_reviews`)

### Pedidos EXCLUIDOS da tabela gold

| Criterio de Exclusao | Campo | Valores | Motivo |
|----------------------|-------|---------|--------|
| Status invalido | `order_status` | `canceled` | Pedido cancelado — sem entrega, sem review valida |
| Status invalido | `order_status` | `unavailable` | Pedido indisponivel — sem entrega, sem review valida |
| Sem aprovacao | `order_approved_at` | `NULL` | Pedido nao foi aprovado para envio |
| Sem review | `order_id` | Ausente em `order_reviews` | Sem target disponivel |

**Resultado esperado:** Somente pedidos entregues com review disponivel entram no modelo.

**Codigo de referencia (Phase 2 — P1 Data Lead):**

```python
import pandas as pd

# Filtro de status
STATUS_EXCLUIDOS = {"canceled", "unavailable"}

df_gold = (
    orders[~orders["order_status"].isin(STATUS_EXCLUIDOS)]
    .dropna(subset=["order_approved_at"])
    .merge(order_reviews[["order_id", "review_score"]], on="order_id", how="inner")
)

# Derivar target
df_gold["bad_review"] = df_gold["review_score"].isin([1, 2]).astype(int)
```

---

## 4. Regras de Outlier

### 4.1 Outlier de Frete

| Parametro | Decisao |
|-----------|---------|
| **Politica** | NAO remover outliers de frete |
| **Acao** | Flaggar com coluna booleana `high_freight_flag` |
| **Threshold** | `freight_value > media + 3 * std` |

**Motivo:** Fretes extremos podem ser o sinal mais forte de insatisfacao do cliente — remover esses registros perderia informacao critica para o modelo.

**Codigo de derivacao:**

```python
freight_mean = df["freight_value"].mean()
freight_std = df["freight_value"].std()
df["high_freight_flag"] = (df["freight_value"] > freight_mean + 3 * freight_std).astype(bool)
```

### 4.2 Outlier de Prazo (Atraso)

**Definicao de atraso:**

```python
df["delay_days"] = (
    df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]
).dt.days
# Valores negativos = entrega antecipada
# Valores positivos = entrega com atraso
```

| Fase | Politica |
|------|---------|
| **EDA (Phase 2/3)** | Pedidos com atraso > 30 dias INCLUIDOS — a EDA precisa desses dados para evidenciar o problema |
| **ML (Phase 4)** | P4 (ML Lead) decide se capeia esses valores ou trata separadamente — decisao documentada no notebook `FASE4-P4-ml-pipeline.ipynb` |

**Nota importante:** `delay_days` e uma feature POS-ENTREGA e PROIBIDA no modelo ML. Ela serve apenas para analise exploratoria (EDA).

---

## 5. Resumo das Decisoes (Referencia Rapida)

| Decisao | Valor | Responsavel |
|---------|-------|-------------|
| Target | `bad_review` = 1 se `review_score` in {1, 2} | P4 — ML Lead |
| Nome coluna target | `bad_review` (int8) | P4 — ML Lead |
| Ancora temporal | `order_approved_at` | P1 — Data Lead |
| Ancora PROIBIDA | `order_purchase_timestamp` | — |
| Janela de dados | Todo o historico Olist (set/2016–ago/2018) | P1 — Data Lead |
| Pedidos excluidos — status | `canceled`, `unavailable` | P1 — Data Lead |
| Pedidos excluidos — sem aprovacao | `order_approved_at` IS NULL | P1 — Data Lead |
| Pedidos excluidos — sem review | Ausente em `order_reviews` | P1 — Data Lead |
| Outlier frete | Flaggar `high_freight_flag` (nao remover), threshold = media + 3 std | P1 — Data Lead |
| Outlier prazo | Atraso > 30 dias incluido na EDA; ML decide separadamente em Phase 4 | P4 — ML Lead |
| Distribuicao esperada | ~15-20% positivos (bad_review=1) | Confirmar na Phase 2 |

---

*Documento criado na Phase 1 (Kickoff). Deve ser lido antes de abrir qualquer notebook da Phase 2.*
*Referencia de codigo: `src/features.py` | Metricas: `docs/metrics_agreement.md` | Features: `docs/feature_contract.md`*
