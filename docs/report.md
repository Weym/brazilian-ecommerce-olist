# Risco Pre-Entrega em E-commerce: Uma Analise do Dataset Olist

**Data:** Março 2026
**Time:** Analise de Dados — Olist E-commerce Project
**Dataset:** Olist E-commerce Dataset (Kaggle) — pedidos 2016-2018

---

## 1. Contexto e Problema de Negocio

O e-commerce brasileiro enfrenta um desafio critico: avaliacoes ruins chegam APOS a entrega — quando nao ha mais nada a fazer. A questao que este projeto responde e: **e possivel identificar pedidos de alto risco de insatisfacao ANTES da entrega?**

Usando o dataset publico da Olist com 97.456 pedidos de 2016 a 2018, construimos um sistema de alerta precoce que usa apenas informacoes disponiveis no momento da expedicao para prever o risco de avaliacao ruim (1-2 estrelas).

**Definicao de avaliacao ruim:** Estrelas 1 ou 2 = `bad_review = 1`. Estrelas 3-5 = `bad_review = 0`. Proporcao de pedidos com bad_review: 13,9% — dataset desbalanceado, tratado com `class_weight='balanced'` nos modelos.

**Impacto do problema:** Cada avaliacao ruim representa um cliente insatisfeito que ja nao pode ser resgatado pela entrega. O sistema de alerta precoce proposto neste projeto permite que equipes de operacoes intervenham ANTES da entrega acontecer — redirecionando recursos logisticos, contatando vendedores de risco, ou comunicando proativamente o cliente sobre possíveis atrasos.

---

## 2. Dados

**Fonte:** Dataset publico Olist (Kaggle) — 9 arquivos CSV com dados de pedidos, clientes, vendedores, produtos, avaliacoes e geolocalizacao.

**Tabela gold:** Join de todas as entidades resultando em 1 linha por pedido (order_id), exportada em `data/gold/olist_gold.parquet`. Contrato imutavel: 97.456 linhas x 43 colunas, proporcao de bad_review = 13,9%.

**Ancora temporal:** Todas as features do modelo sao calculadas com dados disponiveis ate `order_approved_at`. Nenhuma variavel pos-entrega entra na matriz X — isso garante que o modelo seja operacionalmente valido (podemos agir ANTES da entrega). Ver `docs/kickoff.md` para a definicao formal do corte temporal.

**Features pre-entrega utilizadas:** 13 variaveis definidas em `src/features.py` como `PRE_DELIVERY_FEATURES`. Ver `docs/feature_contract.md` para lista completa e tagging `[pre-entrega | pos-entrega | target]`. As 13 features cobrem: valor do frete, preco, proporcao do frete no pedido, dias de prazo estimado, UF de origem e destino, distancia entre vendedor e cliente, peso e volume do produto, categoria do produto, numero de itens, tipo de pagamento e numero de parcelas.

**Tratamento de qualidade:** Nulos documentados — a feature `product_category_name_english` apresenta 1.412 nulos (1,4%), `seller_customer_distance_km` tem 490 nulos (0,5%) e demais features tem menos de 20 nulos. Tratamento via `SimpleImputer` (mediana para numericas, moda para categoricas) antes do modelo. CEPs invalidos tratados na fase de construcao da gold table. Ver `docs/data_quality.md` para checklist completo.

**Escala de classes:** Dataset desbalanceado com 13,9% de positivos (bad_review=1). `scale_pos_weight = 6,21` calculado em y_train para o XGBoost. Para Logistic Regression, `class_weight='balanced'`.

---

## 3. Metodologia

### 3.1 Ato 1 — Analise Exploratoria (EDA)

Investigamos cinco dimensoes do impacto logistico na satisfacao do cliente:

**1. Atraso vs. nota:** Scatter e boxplot de dias de atraso por nota, validado com teste Mann-Whitney (nao-parametrico — notas sao ordinais e nao seguem distribuicao normal). Hipotese nula: distribuicao de notas e identica entre pedidos com e sem atraso.

**2. Frete vs. nota:** Analise do valor absoluto e percentual do frete em relacao ao pedido (`freight_ratio = freight_value / payment_value`). Mann-Whitney para comparar proporcao de frete entre grupos bad_review=0 e bad_review=1.

**3. Geografico:** Choropleth e barplot horizontal por UF de concentracao de avaliacoes 1-2 estrelas (proporcao, nao contagem absoluta). Arquivo `data/processed/geo_aggregated.parquet` exportado para uso na demo interativa da Phase 6.

**4. Rotas criticas:** Heatmap de pares UF-origem x UF-destino com maior concentracao de bad_review. Filtro de volume: apenas corredores com >= 50 pedidos sao exibidos para estabilidade estatistica.

**5. Categorias:** Top 15 categorias de produto com maior proporcao de bad_review (filtro: >= 100 pedidos por categoria).

Justificativa de metricas: ver `docs/metrics_agreement.md` para justificativa de PR-AUC e Recall como metricas primarias (em vez de accuracy — enganosa em datasets desbalanceados).

### 3.2 Ato 2 — Modelo de Risco Pre-Entrega

**Pipeline de features:** `from src.features import PRE_DELIVERY_FEATURES` — allow-list explícita auditavel de 13 colunas. `ColumnTransformer` com `OneHotEncoder` para categoricas (`handle_unknown='ignore'`) e `StandardScaler` para numericas. `SimpleImputer` adicionado como primeira etapa em cada sub-pipeline para tratar nulos antes da transformacao.

**Verificacao anti-leakage:** Antes do treino, verificamos que nenhuma das 6 `FORBIDDEN_FEATURES` (variaveis pos-entrega) esta presente em `PRE_DELIVERY_FEATURES`. O assert falha rapidamente se o contrato for violado.

**Estrategia de balanceamento:** `class_weight='balanced'` em ambos os modelos. Sem SMOTE (dados sinteticos adicionam risco sem ganho garantido no prazo disponivel).

**Divisao treino/test:** 80/20 estratificado por `bad_review` para preservar proporcao de classes em ambos os conjuntos. Treino: 77.964 pedidos | Teste: 19.492 pedidos.

**Baseline obrigatorio:** `LogisticRegression` treinado e avaliado ANTES do XGBoost — garante patamar minimo e detecta problemas de dados antes de modelos complexos. Se XGBoost nao superar o baseline, a complexidade adicional nao se justifica.

**Modelo final:** `XGBClassifier` com `n_estimators=300`, `max_depth=4`, `learning_rate=0.05`, `scale_pos_weight=6,21`. Hiperparametros escolhidos como defaults razoaveis sem GridSearchCV extenso — o ganho marginal de tuning nao justifica o risco de prazo.

**Threshold de decisao:** Corte na curva Precision-Recall onde Precision >= 0,40 (criterio primario). Com o modelo atual (PR-AUC = 0,2283), o criterio de Recall >= 0,60 nao pode ser atingido simultaneamente — documentado como limitacao em `docs/ml_limitations.md`. Ver justificativa em `notebooks/FASE4-P4-ml-pipeline.ipynb`, secao 5.

**Explicabilidade:** SHAP `TreeExplainer` aplicado em amostra de 5.000 registros do test set. Beeswarm exportado em `reports/figures/shap_beeswarm.png`.

---

## 4. Resultados

### 4.1 Achados do Ato 1 (EDA)

**Atraso e o principal driver de insatisfacao:**
- Pedidos com atraso tem nota mediana de 2,0 vs. 5,0 para pedidos no prazo (Mann-Whitney p < 0,001 — diferenca altamente significativa)
- O boxplot de "com atraso vs. no prazo" mostra distribuicoes completamente separadas: pedidos no prazo se concentram em 5 estrelas; pedidos atrasados se concentram em 1-2 estrelas

**Frete tem impacto relevante mas secundario:**
- `freight_ratio` mediano e maior em pedidos com bad_review=1 do que em bad_review=0 (Mann-Whitney p < 0,05)
- O impacto do frete e relativo ao valor total do pedido: um frete de R$30 em um pedido de R$50 (60% do valor) gera muito mais insatisfacao do que o mesmo frete em um pedido de R$300 (10%)

**Concentracao geografica de problemas:**
- UFs com maior proporcao de bad_review: estados do Nordeste (MA, RN, AL) concentram proporcoes de bad_review acima da media nacional de 13,9%
- Corredores mais criticos: rotas SP -> Nordeste (SP-MA, SP-CE, SP-RN) tem a maior concentracao de atrasos e bad_review
- UFs como SP e MG, apesar de alto volume absoluto, tem proporcoes de bad_review proximas ou abaixo da media nacional

**Categorias de alto risco:**
- Top 3 categorias com maior proporcao de bad_review: eletronicos portateis, moveis e artigos de cama/banho/mesa concentram proporcoes acima da media
- Categoria `computers_accessories` e `telephony` aparecem tanto no top de categorias quanto nas top features SHAP do modelo

### 4.2 Desempenho do Modelo (Ato 2)

| Metrica | Baseline (LogReg) | XGBoost |
|---------|------------------|---------|
| PR-AUC (test set) | 0,2207 | 0,2283 |
| Recall no threshold | 0,53 (threshold padrao) | 0,02 (threshold 0,785) |
| Precision no threshold | — | 0,40 |
| Pedidos flagrados/semana (estimativa) | — | 8 pedidos |

**Threshold escolhido:** 0,785 — Precision = 0,40 | Recall = 0,02.

**Frase-ancora operacional:** "40% dos pedidos flagrados pelo modelo sao de fato pedidos de alto risco de avaliacao ruim — permitindo intervencao preventiva antes da entrega."

**Melhora sobre baseline:** +0,0076 de PR-AUC. O XGBoost captura interacoes nao-lineares entre features (ex.: distancia alta + prazo estimado alto juntos predizem mais risco do que cada um separado), o que a regressao logistica nao consegue modelar.

**Features mais importantes (SHAP — top 5 por impacto medio absoluto):**
1. `order_item_count` (0,188) — numero de itens no pedido: pedidos com mais itens tem maior risco
2. `customer_state_RJ` (0,101) — pedidos com destino ao Rio de Janeiro
3. `seller_customer_distance_km` (0,098) — distancia entre vendedor e cliente
4. `price` (0,069) — valor unitario do produto
5. `seller_state_SP` (0,049) — vendedores localizados em Sao Paulo

**Estimativa de volume operacional:** Das 793 predicoes acima do threshold em todo o dataset (0,8% dos pedidos), 40% sao verdadeiros positivos. Em producao, isso equivale a aproximadamente 8 alertas por semana — volume humanamente gerenciavel para uma equipe de atendimento.

---

## 5. Recomendacoes Operacionais

Com base nos achados, recomendamos tres acoes imediatas para equipes de operacoes:

**1. Monitoramento proativo de pedidos flagrados**

Implementar alerta automatico para pedidos com pontuacao de risco acima do patamar de 0,785. A cada semana, aproximadamente 8 pedidos receberiam esse alerta — volume gerenciavel para uma equipe de operacoes. Entre esses pedidos, 40% sao de fato alto risco de avaliacao ruim.

Acao concreta: No momento da aprovacao do pedido, calcular a pontuacao de risco usando o modelo serializado em `models/final_pipeline.joblib`. Pedidos com pontuacao >= 0,785 entram na fila de monitoramento proativo, onde um operador pode antecipar comunicacao com o cliente, verificar o estado do envio ou acionar o parceiro logistico.

**2. Intervencao prioritaria com os principais vendedores de risco**

A pontuacao media de risco por vendedor (calculada em `notebooks/FASE4-P4-ml-pipeline.ipynb`, secao 6) identifica os parceiros que mais contribuem para avaliacoes ruins. Com 1.247 vendedores elegíveis (>= 10 pedidos), os 20 de maior risco medio concentram desproporcionalmente os alertas.

Acoes concretas:
- Reuniao de alinhamento com os 5 vendedores de maior pontuacao media de risco (score medio > 0,64)
- Auditoria das praticas de embalagem e prazos prometidos desses vendedores
- Programa de suporte logistico para vendedores com alto volume de pedidos E alta pontuacao de risco (ex.: vendedor com 969 pedidos e pontuacao media 0,598 — impacto operacional mais alto)

**3. Revisao de rotas e corredores criticos**

Os corredores SP -> estados do Nordeste concentram desproporcionalmente os atrasos e as avaliacoes ruins. Pedidos com alta distancia vendedor-cliente (`seller_customer_distance_km`) figuram entre as top features do modelo — distancia longa e um sinal de risco.

Acoes concretas:
- Revisao dos parceiros logisticos e SLAs para rotas SP-MA, SP-CE e SP-RN
- Ajuste dos prazos estimados exibidos ao cliente nas rotas de longa distancia (sub-estimar prazos gera expectativas irreais e avaliacoes ruins mesmo com entrega dentro do prazo do transportador)
- Consideracao de hubs regionais de distribuicao no Nordeste para reduzir a distancia de entrega final

---

## 6. Limitacoes e Proximos Passos

**Limitacoes do modelo atual:**

- **Dataset historico (2016-2018):** comportamento logistico e de consumo pode ter mudado significativamente. Retreinamento periodico com dados mais recentes e necessario antes de producao.
- **PR-AUC baixo (0,2283):** O modelo opera em modo de alta precisao cirurgica — 40% de precisao com apenas 2% de recall. Para capturar mais pedidos de risco, seria necessario aceitar muito mais falsos alarmes (a Precision cairia para ~18% ao atingir Recall >= 0,60).
- **Calibracao de probabilidades nao realizada:** Os scores sao ordinais (maior = mais risco), mas nao sao probabilidades absolutas. Um score de 0,785 nao significa 78,5% de probabilidade de bad_review. Para uso em decisoes com custo absoluto, seria necessario Platt scaling ou isotonic regression.
- **Features limitadas ao momento de expedicao:** Informacoes de rastreamento em tempo real (primeiro scan no correio, demora no processamento do centro de distribuicao) aumentariam significativamente a precisao.
- **Hiperparametros nao otimizados:** Sem GridSearchCV — os parametros n_estimators=300, max_depth=4, learning_rate=0,05 sao defaults razoaveis. Ganho potencial de 3-8% no PR-AUC com tuning sistematico.

**Proximos passos tecnicos:**

- Retreinamento trimestral com dados mais recentes
- Adicionar features de rastreamento (quando disponivel via API logistica do parceiro)
- Avaliar calibracao de probabilidades (Platt scaling) para scores mais interpretaveis em dashboards de risco
- Expandir features com analise de texto dos titulos de produtos (correlacao com expectativa do cliente)
- GridSearchCV para hiperparametros do XGBoost com validacao cruzada estratificada

**Proximos passos operacionais:**

- Piloto de 30 dias com um corredor de alto risco (ex.: SP -> MA) para medir impacto real da intervencao
- Definir metricas de sucesso operacional: reducao de bad_review nos pedidos flagrados vs. grupo de controle
- Avaliar integracao com sistema de atendimento ao cliente para acionamento automatico de notificacoes proativas

---

## Referencias e Artefatos

| Artefato | Caminho | Descricao |
|----------|---------|-----------|
| Tabela gold | `data/gold/olist_gold.parquet` | Contrato imutavel de dados — 97.456 pedidos x 43 colunas |
| Feature contract | `docs/feature_contract.md` | Allow-list de 13 features pre-entrega com tagging |
| Metrics agreement | `docs/metrics_agreement.md` | Justificativa de PR-AUC e Recall como metricas primarias |
| Kickoff | `docs/kickoff.md` | Ancora temporal, definicao de target e contratos iniciais |
| Limitacoes ML | `docs/ml_limitations.md` | Documentacao do trade-off Precision/Recall e limitacoes conhecidas |
| Notebook Data Foundation | `notebooks/FASE2-P1-data-foundation.ipynb` | Join chain, Haversine, tagging de colunas |
| Notebook EDA | `notebooks/FASE3-P3-eda.ipynb` | Analise exploratoria — Ato 1 |
| Notebook ML | `notebooks/FASE4-P4-ml-pipeline.ipynb` | Pipeline de risco — Ato 2 (fonte de verdade das metricas) |
| SHAP beeswarm | `reports/figures/shap_beeswarm.png` | Top 15 features do modelo por impacto medio SHAP |
| Curva PR | `reports/figures/pr_curve.png` | Curva Precision-Recall com threshold marcado |
| Geo agregado | `data/processed/geo_aggregated.parquet` | Dados por UF para mapa interativo no Streamlit |
| Pipeline serializado | `models/final_pipeline.joblib` | Modelo XGBoost completo (preprocessor + estimador) para producao |
| Pipeline baseline | `models/baseline_logreg.joblib` | Pipeline LogReg para comparacao e auditoria |

**Para reproduzir os resultados:** Execute os notebooks na ordem `FASE2-P1-data-foundation.ipynb` -> `FASE3-P3-eda.ipynb` -> `FASE4-P4-ml-pipeline.ipynb` a partir da raiz do projeto.
