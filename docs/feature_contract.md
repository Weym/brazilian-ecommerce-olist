# Feature Contract — Olist Pre-Delivery Risk Model

**Temporal anchor:** `order_approved_at`
**Target:** `bad_review` = 1 se `review_score` in {1, 2}, 0 caso contrario
**Regra de ouro:** Apenas colunas marcadas `[pre-entrega]` podem entrar na matriz de features do modelo.
**Arquivo de referencia:** `src/features.py` — unica fonte de verdade para codigo

---

## Tabela de Colunas

| Coluna | Origem CSV | Derivacao | Tag | Notas |
|--------|-----------|-----------|-----|-------|
| order_id | orders.csv | raw | [join-key] | Chave primaria do pedido |
| order_approved_at | orders.csv | raw | [temporal-anchor] | Ancora de corte — features calculadas relativas a esta data |
| review_score | order_reviews.csv | raw | [pos-entrega] | Usado APENAS para derivar bad_review — **nunca como feature** |
| bad_review | derivada | review_score in {1,2} -> 1, else 0 | [target] | Classe positiva = insatisfacao real |
| freight_value | order_items.csv | soma por pedido | [pre-entrega] | Valor total de frete do pedido |
| price | order_items.csv | soma por pedido | [pre-entrega] | Valor total dos itens do pedido |
| freight_ratio | engineered | freight_value / price | [pre-entrega] | Proporcao do frete sobre o valor do pedido |
| estimated_delivery_days | orders.csv | order_estimated_delivery_date - order_approved_at | [pre-entrega] | Usa order_approved_at como ancora (nao order_purchase_timestamp) |
| seller_state | sellers.csv | raw | [pre-entrega] | Estado do vendedor |
| customer_state | customers.csv | raw | [pre-entrega] | Estado do comprador |
| seller_customer_distance_km | geolocation.csv | Haversine(seller_zip, customer_zip) em km | [pre-entrega] | Computada na Phase 2 — esperado 0-4000 km |
| product_weight_g | products.csv | raw | [pre-entrega] | Peso do produto em gramas |
| product_volume_cm3 | products.csv | length * width * height | [pre-entrega] | Volume do produto em cm3 |
| product_category_name_english | category_translation.csv | join via product_category_name | [pre-entrega] | Categoria do produto em ingles |
| order_item_count | order_items.csv | contagem por order_id | [pre-entrega] | Numero de itens no pedido |
| payment_type | order_payments.csv | moda por pedido | [pre-entrega] | Tipo de pagamento predominante |
| payment_installments | order_payments.csv | soma por pedido | [pre-entrega] | Total de parcelas do pedido |
| order_delivered_customer_date | orders.csv | raw | [pos-entrega] | **PROIBIDA** — so disponivel apos entrega fisica |
| review_comment_message | order_reviews.csv | raw | [pos-entrega] | **PROIBIDA** — texto pos-entrega (NLP opcional e fora do escopo v1) |
| review_creation_date | order_reviews.csv | raw | [pos-entrega] | **PROIBIDA** — data em que o cliente criou a review |
| review_answer_timestamp | order_reviews.csv | raw | [pos-entrega] | **PROIBIDA** — timestamp da resposta do vendedor |
| order_delivered_carrier_date | orders.csv | raw | [pos-entrega] | **PROIBIDA** — parcialmente pos-aprovacao, pouco confiavel |

---

## Resumo de Tags

| Tag | Significado | Pode entrar em X? |
|-----|-------------|-------------------|
| [pre-entrega] | Disponivel em order_approved_at | **SIM** |
| [pos-entrega] | So disponivel apos entrega fisica | **NAO (PROIBIDA)** |
| [target] | Variavel alvo do modelo | **NAO (e Y, nao X)** |
| [join-key] | Chave de juncao entre tabelas | **NAO (identificador)** |
| [temporal-anchor] | Ancora de corte temporal | **NAO (auxiliar)** |

---

## Como manter este documento sincronizado

Se uma coluna e adicionada a `PRE_DELIVERY_FEATURES` em `src/features.py`, uma linha correspondente DEVE ser adicionada a esta tabela. As duas fontes devem estar sempre em sincronia.

Fluxo de atualizacao:
1. Edite `src/features.py` — adicione a coluna a `PRE_DELIVERY_FEATURES` com comentario explicativo
2. Edite `docs/feature_contract.md` — adicione a linha correspondente na tabela com tag `[pre-entrega]`
3. Commit ambos os arquivos no mesmo commit

`src/features.py` e a fonte de verdade para codigo. `docs/feature_contract.md` e a fonte de verdade para comunicacao com o time.

---

*Gerado em: 2026-03-01*
*Fase: Phase 1 — Kickoff e Contratos*
