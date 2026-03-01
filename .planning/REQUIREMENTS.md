# Requirements: Olist Challenge — Logística, Satisfação e Risco Pré-Entrega

**Definido:** 2026-03-01
**Core Value:** Mostrar que é possível agir antes do problema acontecer — transformar dados históricos de logística em um sistema de alerta precoce que permite intervenção antes da entrega e da avaliação ruim.

## Requisitos v1

Requisitos para o desafio relâmpago de 1 semana. Cada um mapeia para fases do roadmap.

### Kickoff & Contratos (KICK)

- [ ] **KICK-01**: Time define e documenta o "contrato de features pré-entrega" — lista explícita de colunas permitidas e proibidas no modelo ML
- [ ] **KICK-02**: Time acorda as métricas primárias do modelo (PR-AUC e Recall para classe positiva) antes de qualquer código
- [ ] **KICK-03**: Time define ownership de notebooks (convenção de nomes, estrutura de pastas, regras de git)
- [ ] **KICK-04**: Time define o target do modelo: avaliação ruim = estrelas 1–2
- [ ] **KICK-05**: Time define o recorte temporal e regras de outlier antes da construção da tabela gold

### Data Foundation (DATA)

- [ ] **DATA-01**: Tabela analítica "gold" construída com joins de todos os dataframes relevantes da Olist (orders, items, reviews, customers, sellers, geolocation, products, category_translation)
- [ ] **DATA-02**: Todas as colunas da tabela gold auditadas e tagueadas como `[pré-entrega | pós-entrega | target]`
- [ ] **DATA-03**: Qualidade validada: nulos, duplicatas, CEPs inválidos e datas inconsistentes documentados e tratados
- [ ] **DATA-04**: Tabela gold exportada como `.parquet` e disponível como contrato imutável para todas as fases downstream
- [ ] **DATA-05**: Distância aproximada entre vendedor e comprador calculada via Haversine em km (não graus decimais) e integrada à tabela gold

### EDA — Ato 1: Impacto da Logística (EDA)

- [ ] **EDA-01**: Análise visual de atraso (dias de atraso) vs. nota de avaliação (scatter + boxplot)
- [ ] **EDA-02**: Análise visual de frete (valor absoluto e % do pedido) vs. nota de avaliação
- [ ] **EDA-03**: Mapa/heatmap geográfico por UF mostrando concentração de avaliações 1–2 estrelas
- [ ] **EDA-04**: Segmentação de avaliações ruins por categoria de produto (top categorias problemáticas)
- [ ] **EDA-05**: Análise de rotas/regiões com maior concentração de atrasos (origem × destino)

### ML — Ato 2: Modelo de Risco Pré-Entrega (ML)

- [ ] **ML-01**: Pipeline de features com apenas variáveis disponíveis até o momento de expedição (sem vazamento)
- [ ] **ML-02**: Baseline logístico treinado e avaliado com PR-AUC e Recall (obrigatório antes de modelos complexos)
- [ ] **ML-03**: Modelo XGBoost treinado com as mesmas features pré-entrega
- [ ] **ML-04**: SHAP values calculados para explicar as features mais importantes do modelo XGBoost
- [ ] **ML-05**: Limiar de decisão definido com impacto operacional estimado (pedidos flagrados/semana, % real de risco)
- [ ] **ML-06**: Agregação de score de risco médio por vendedor (operacionalmente acionável)
- [ ] **ML-07**: Pipeline sklearn serializado como `.joblib` para uso na demo Streamlit sem reprocessamento ao vivo

### Demo e Apresentação (PRES)

- [ ] **PRES-01**: Slide deck com narrativa em dois atos (Problema → Motor de risco → Ações/impacto esperado)
- [ ] **PRES-02**: Notebooks documentados por área (data foundation, EDA, ML) com outputs limpos no git
- [ ] **PRES-03**: Streamlit multi-página com preditor ao vivo (input de características de pedido → output de risco pré-entrega)
- [ ] **PRES-04**: Streamlit com mapa interativo (filtros por UF/rota)
- [ ] **PRES-05**: Streamlit com painel de EDA navegável (gráficos principais do Ato 1)
- [ ] **PRES-06**: Relatório escrito com achados técnicos e recomendações operacionais em linguagem de negócio
- [ ] **PRES-07**: Demo Streamlit carrega artefatos pré-computados (nunca processa dados pesados ao vivo durante apresentação)

## Requisitos v2

Deferred para após o desafio relâmpago.

### NLP / Reviews (NLP)

- **NLP-01**: Análise de tópicos/sentimento dos comentários de review (o que irrita quando a nota é 1 estrela)
- **NLP-02**: Embeddings ou labels de tópico integrados à narrativa do Ato 1

### Infraestrutura

- **INFRA-01**: Deploy em Streamlit Community Cloud (demo não apenas local)
- **INFRA-02**: Pipeline de retreinamento automatizado

## Fora de Escopo

| Feature | Motivo |
|---------|--------|
| Deep learning | Complexidade desnecessária para prazo de 1 semana; ganho marginal não justifica |
| RFM / segmentação de clientes | Olist tem taxa de recompra próxima de zero — segmentos sem significado prático |
| Chat em tempo real / streaming | Dataset é histórico/batch |
| App mobile | Showcase, não produto |
| Features pós-entrega no modelo | Vazamento de dados — invalida credibilidade do modelo |
| Accuracy como headline metric | Enganosa com ~15-20% de classe positiva (reviews 1-2 estrelas) |

## Rastreabilidade

Será preenchida durante a criação do roadmap.

| Requisito | Fase | Status |
|-----------|------|--------|
| KICK-01 a KICK-05 | Fase 1 | Pendente |
| DATA-01 a DATA-05 | Fase 2 | Pendente |
| EDA-01 a EDA-05 | Fase 3 | Pendente |
| ML-01 a ML-07 | Fase 4 | Pendente |
| PRES-01 a PRES-07 | Fase 5 | Pendente |

**Cobertura:**
- Requisitos v1: 29 total
- Mapeados para fases: 29
- Não mapeados: 0 ✓

---
*Requisitos definidos: 2026-03-01*
*Última atualização: 2026-03-01 após definição inicial*
