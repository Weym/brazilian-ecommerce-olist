# Metrics Agreement — Olist Pre-Delivery Risk Model

## Decisao

Metricas primarias: **PR-AUC** (Precision-Recall AUC) e **Recall (classe positiva)**
Metricas proibidas como headline: Accuracy, ROC-AUC

---

## Por que Accuracy Falha

O dataset Olist apresenta um desbalanceamento de classes significativo:

- **~80-85% dos pedidos** resultam em avaliacao boa (bad_review = 0)
- **~15-20% dos pedidos** resultam em avaliacao ruim (bad_review = 1)

Esse desbalanceamento (imbalance) faz com que a accuracy seja uma metrica enganosa:

- Um classificador "sempre bom" — que prediz 0 para todos os pedidos — atinge 80-85% de accuracy **sem nenhum valor preditivo real**
- A accuracy mascara completamente a performance na classe que importa (avaliacoes ruins)

**Exemplo concreto:** Se o modelo chuta "bom" para todos os 100 pedidos, acerta 83 — parece otimo, mas nao detectou nenhuma avaliacao ruim.

Portanto, **accuracy nao pode ser usada como headline metric** neste projeto.

---

## Por que ROC-AUC Insuficiente

ROC-AUC (Area Under the Receiver Operating Characteristic Curve) mede a capacidade de separacao entre classes em geral, mas possui uma limitacao critica em datasets desbalanceados:

- ROC-AUC e **insensivel ao imbalance** de classes — ela avalia a separacao entre positivos e negativos de forma simetrica
- Um modelo com ROC-AUC = 0.80 pode ter **Recall = 0.10** na classe positiva — ou seja, detecta apenas 10% dos pedidos em risco
- Para este projeto, o objetivo e **maximizar a deteccao antecipada** de pedidos que gerarao avaliacao ruim. Recall alto na classe positiva e essencial para que o sistema de alerta precoce tenha valor operacional.

ROC-AUC pode ser reportada como informacao adicional, mas **nao pode ser usada como headline metric**.

---

## Por que PR-AUC e a Metrica Certa

PR-AUC (Area Under the Precision-Recall Curve) e a metrica adequada para este cenario porque:

- Mede o **tradeoff Precision/Recall diretamente na classe positiva** (a minoritaria — avaliacoes ruins)
- E **sensivel ao imbalance** e penaliza fortemente modelos que ignoram a classe positiva
- Permite visualizar qual e o melhor **limiar de decisao** (threshold) a partir da curva PR
- Um modelo sem valor preditivo tem PR-AUC proxima da proporcao de positivos (~0.15-0.20), tornando o baseline trivial facil de identificar

**PR-AUC e a metrica primaria do projeto. Toda comparacao entre modelos deve usar PR-AUC.**

---

## Distribuicao de Classes (Estimativa)

| Classe | Descricao | Estimativa |
|--------|-----------|------------|
| 0 (negativo) | Avaliacao boa (3-5 estrelas) | ~80-85% dos pedidos |
| 1 (positivo) | Avaliacao ruim (1-2 estrelas) | ~15-20% dos pedidos |

> **Nota:** Verificar proporcao real na primeira celula do notebook FASE2-P1 — o valor exato afeta `scale_pos_weight` do XGBoost.
>
> ```python
> df["bad_review"].value_counts(normalize=True)
> ```

---

## Politica de Limiar de Decisao

O **limiar padrao 0.5 NAO e usado** — ele e arbitrario e otimiza a metrica errada para datasets desbalanceados.

O limiar de decisao (threshold) deve ser selecionado a partir da **curva PR na Phase 4**, em funcao do impacto operacional:

- **Criterio principal:** maximizar F1-score na classe positiva (balanco entre Precision e Recall)
- **Criterio alternativo:** escolher o limiar que produz uma estimativa de pedidos flagrados por semana que seja operacionalmente acionavel — nem poucos demais (subnotificacao), nem muitos (fadiga de alerta)

**Documentar na Phase 4:**

> "Com limiar X, Y% dos pedidos seriam flagrados por semana, dos quais Z% sao positivos verdadeiros (Precision = Z%)."

Essa declaracao e obrigatoria no relatorio final e na apresentacao de slides.

---

## Requisito de Baseline

**ANTES de qualquer modelo avancado (XGBoost, Random Forest, etc.), o seguinte baseline DEVE ser treinado e avaliado:**

| Parametro | Valor |
|-----------|-------|
| Modelo | Regressao Logistica (`LogisticRegression`) |
| Parametro critico | `class_weight='balanced'` |
| Features | Apenas colunas em `PRE_DELIVERY_FEATURES` (src/features.py) |
| Split | Mesmo train/test set que o XGBoost usa |

**Por que o baseline logistico e obrigatorio:**

1. **Garante que o XGBoost realmente adiciona valor** acima de um modelo simples e interpretavel
2. **Garante um entregavel** mesmo se o modelo avancado nao fechar dentro do sprint

**Por que `class_weight='balanced'`:**

- Corrige o imbalance de classes automaticamente, ajustando os pesos de cada classe inversamente proporcional a sua frequencia
- Sem esse parametro, a Regressao Logistica tende a ignorar a classe positiva e se aproximar do classificador "sempre bom"
- Nao requer oversampling (SMOTE, etc.) — e a forma mais simples e robusta de lidar com desbalanceamento em um modelo linear

**O que reportar para o baseline:**

- PR-AUC no test set
- Recall na classe positiva no test set (com o limiar escolhido na curva PR)
- Nenhuma feature pos-entrega pode estar presente

---

## Tabela-Resumo de Metricas

| Metrica | Status | Motivo |
|---------|--------|--------|
| PR-AUC | **PRIMARIA** | Sensivel ao imbalance, mede classe positiva diretamente |
| Recall (classe positiva) | **PRIMARIA** | Maximizar deteccao antecipada e o objetivo central |
| ROC-AUC | Informativa apenas | Insensivel ao imbalance — nao pode ser headline |
| Accuracy | **PROIBIDA** como headline | Mascara falha total na classe positiva |
| F1-score (classe positiva) | Auxiliar | Util para selecao de limiar na curva PR |

---

*Acordo definido na Phase 1 (Kickoff). Valido para todas as fases de ML.*
*Referencia: docs/feature_contract.md (definicao de features) | src/features.py (codigo)*
