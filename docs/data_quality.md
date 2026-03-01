# Checklist de Qualidade — Tabela Gold

**Arquivo:** `data/gold/olist_gold.parquet`
**Gerado em:** 2026-03-01
**Notebook:** `notebooks/FASE2-P1-data-foundation.ipynb`

## Dimensoes

| Metrica | Valor |
|---------|-------|
| Total de pedidos (linhas) | 97456 |
| Total de colunas | 38 |
| Pedidos excluidos (canceled/unavailable/sem review) | 1985 |

## [1] Nulos por Coluna

| Coluna | Nulos | % | Impacto |
|--------|-------|---|---------|
| order_delivered_customer_date | 1646 | 1.69% | Feature pos-entrega — NaN = pedido ainda nao entregue |
| actual_delay_days | 1646 | 1.69% | Feature pos-entrega derivada — NaN quando sem data entrega |
| product_category_name_english | 1412 | 1.45% | Categoria sem traducao disponivel |
| product_category_name | 1393 | 1.43% | Produto sem categoria cadastrada |
| product_photos_qty | 1393 | 1.43% | Feature de produto indisponivel |
| order_delivered_carrier_date | 608 | 0.62% | Feature pos-entrega — NaN = nao coletado ainda |
| seller_customer_distance_km | 490 | 0.50% | Feature de distancia indisponivel (CEP sem match geo) |
| customer_lat / customer_lng | 272 | 0.28% | CEP de cliente nao encontrado na tabela geo |
| seller_lat / seller_lng | 219 | 0.22% | CEP de seller nao encontrado na tabela geo |
| product_length_cm / height / width | 19 | 0.02% | Dimensoes de produto indisponiveis |
| product_weight_g | 19 | 0.02% | Feature de peso indisponivel |
| product_volume_cm3 | 19 | 0.02% | Feature de volume indisponivel (derivada de dimensoes) |
| freight_ratio | 4 | 0.00% | Divisao por zero evitada (total_payment_value=0) |
| seller_id / seller_state / seller_city | 3 | 0.00% | Pedidos sem seller identificado |
| total_payment_value | 1 | 0.00% | Pagamento sem valor registrado |

**Colunas criticas (order_id, bad_review, customer_id, customer_state, order_approved_at, review_score): SEM NULOS.**

Nota: seller_id e seller_state tem 3 nulos (0.003% do dataset) — nao impacta qualidade do modelo.

## [2] Duplicatas

- order_id duplicados: 0 (OK)
- Tabela gold tem exatamente 1 linha por pedido

## [3] CEPs e Cobertura Geografica

| Metrica | Valor |
|---------|-------|
| Sellers sem lat/lon (CEP ausente no geo) | 219 (0.2%) |
| Customers sem lat/lon (CEP ausente no geo) | 272 (0.3%) |
| Pedidos sem distancia calculada | 490 (0.5%) |
| seller_zip validos (formato 5 digitos) | 97453/97456 (100.0%) |
| customer_zip validos (formato 5 digitos) | 97456/97456 (100.0%) |

**Tratamento:** CEPs nao encontrados na tabela de geolocation resultam em seller_customer_distance_km = NaN. Pipeline de ML deve tratar NaN com imputer.

## [4] Datas

| Verificacao | Resultado |
|-------------|-----------|
| order_approved_at nulos | 0 (OK — filtrado antes do export) |
| estimated_delivery < approved_at | 7 pedidos (AVISO — manter, investigar na EDA) |
| estimated_days negativos | 7 (AVISO — mesmos 7 pedidos) |
| Range temporal | 2016-09-15 a 2018-09-03 |

**AVISO:** Dataset Olist encerra abruptamente em setembro de 2018. Analises de tendencia temporal devem excluir ou anotar esse mes.

## [5] Target

| Classe | Pedidos | Proporcao |
|--------|---------|-----------|
| bad_review = 1 (1-2 estrelas) | 13521 | 13.9% |
| bad_review = 0 (3-5 estrelas) | 83935 | 86.1% |

**scale_pos_weight sugerido para XGBoost:** 6.2

## [6] Outliers

- Pedidos com frete > media+3*desvio: 1561 (1.6%)
- Decisao (Phase 1): manter no gold, nao remover — flagar para EDA

## Colunas por Tag

### Pre-entrega (permitidas no modelo ML)
order_id, order_approved_at, order_estimated_delivery_date, estimated_days,
payment_value, freight_value, freight_ratio, total_payment_value,
product_weight_g, product_volume_cm3, product_photos_qty,
seller_customer_distance_km, seller_id, seller_state, seller_city,
customer_id, customer_unique_id, customer_state, customer_city,
product_category_name_english, order_status, order_purchase_timestamp,
seller_lat, seller_lng, customer_lat, customer_lng

### Pos-entrega (PROIBIDO no modelo ML — vazamento de dados)
order_delivered_customer_date, order_delivered_carrier_date, actual_delay_days, review_score

### Target
bad_review (1 = insatisfacao 1-2 estrelas, 0 = ok 3-5 estrelas)

---
*Qualidade validada: 2026-03-01*
*Proxima verificacao recomendada: antes de iniciar Phase 4 (ML)*
