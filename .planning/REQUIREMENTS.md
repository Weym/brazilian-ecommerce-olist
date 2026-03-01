# Requirements: Olist Challenge — Logistica, Satisfacao e Risco Pre-Entrega

**Definido:** 2026-03-01
**Core Value:** Mostrar que e possivel agir antes do problema acontecer — transformar dados historicos de logistica em um sistema de alerta precoce que permite intervencao antes da entrega e da avaliacao ruim.

## Requisitos v1

Requisitos para o desafio relâmpago de 1 semana. Cada um mapeia para fases do roadmap.

### Kickoff & Contratos (KICK)

- [x] **KICK-01**: Time define e documenta o "contrato de features pre-entrega" — lista explícita de colunas permitidas e proibidas no modelo ML
- [x] **KICK-02**: Time acorda as metricas primarias do modelo (PR-AUC e Recall para classe positiva) antes de qualquer codigo
- [x] **KICK-03**: Time define ownership de notebooks (convencao de nomes, estrutura de pastas, regras de git)
- [x] **KICK-04**: Time define o target do modelo: avaliacao ruim = estrelas 1–2
- [x] **KICK-05**: Time define o recorte temporal e regras de outlier antes da construcao da tabela gold

### Data Foundation (DATA)

- [x] **DATA-01**: Tabela analitica "gold" construida com joins de todos os dataframes relevantes da Olist (orders, items, reviews, customers, sellers, geolocation, products, category_translation)
- [ ] **DATA-02**: Todas as colunas da tabela gold auditadas e tagueadas como `[pre-entrega | pos-entrega | target]`
- [ ] **DATA-03**: Qualidade validada: nulos, duplicatas, CEPs invalidos e datas inconsistentes documentados e tratados
- [ ] **DATA-04**: Tabela gold exportada como `.parquet` e disponivel como contrato imutavel para todas as fases downstream
- [ ] **DATA-05**: Distancia aproximada entre vendedor e comprador calculada via Haversine em km (nao graus decimais) e integrada a tabela gold

### EDA — Ato 1: Impacto da Logistica (EDA)

- [ ] **EDA-01**: Analise visual de atraso (dias de atraso) vs. nota de avaliacao (scatter + boxplot)
- [ ] **EDA-02**: Analise visual de frete (valor absoluto e % do pedido) vs. nota de avaliacao
- [ ] **EDA-03**: Mapa/heatmap geografico por UF mostrando concentracao de avaliacoes 1–2 estrelas
- [ ] **EDA-04**: Segmentacao de avaliacoes ruins por categoria de produto (top categorias problematicas)
- [ ] **EDA-05**: Analise de rotas/regioes com maior concentracao de atrasos (origem x destino)

### ML — Ato 2: Modelo de Risco Pre-Entrega (ML)

- [ ] **ML-01**: Pipeline de features com apenas variaveis disponiveis ate o momento de expedicao (sem vazamento)
- [ ] **ML-02**: Baseline logistico treinado e avaliado com PR-AUC e Recall (obrigatorio antes de modelos complexos)
- [ ] **ML-03**: Modelo XGBoost treinado com as mesmas features pre-entrega
- [ ] **ML-04**: SHAP values calculados para explicar as features mais importantes do modelo XGBoost
- [ ] **ML-05**: Limiar de decisao definido com impacto operacional estimado (pedidos flagrados/semana, % real de risco)
- [ ] **ML-06**: Agregacao de score de risco medio por vendedor (operacionalmente acionavel)
- [ ] **ML-07**: Pipeline sklearn serializado como `.joblib` para uso na demo Streamlit sem reprocessamento ao vivo

### Demo e Apresentacao (PRES)

- [ ] **PRES-01**: Slide deck com narrativa em dois atos (Problema → Motor de risco → Acoes/impacto esperado)
- [ ] **PRES-02**: Notebooks documentados por area (data foundation, EDA, ML) com outputs limpos no git
- [ ] **PRES-03**: Streamlit multi-pagina com preditor ao vivo (input de caracteristicas de pedido → output de risco pre-entrega)
- [ ] **PRES-04**: Streamlit com mapa interativo (filtros por UF/rota)
- [ ] **PRES-05**: Streamlit com painel de EDA navegavel (graficos principais do Ato 1)
- [ ] **PRES-06**: Relatorio escrito com achados tecnicos e recomendacoes operacionais em linguagem de negocio
- [ ] **PRES-07**: Demo Streamlit carrega artefatos pre-computados (nunca processa dados pesados ao vivo durante apresentacao)

## Requisitos v2

Deferred para apos o desafio relâmpago.

### NLP / Reviews (NLP)

- **NLP-01**: Analise de topicos/sentimento dos comentarios de review (o que irrita quando a nota e 1 estrela)
- **NLP-02**: Embeddings ou labels de topico integrados a narrativa do Ato 1

### Infraestrutura

- **INFRA-01**: Deploy em Streamlit Community Cloud (demo nao apenas local)
- **INFRA-02**: Pipeline de retreinamento automatizado

## Fora de Escopo

| Feature | Motivo |
|---------|--------|
| Deep learning | Complexidade desnecessaria para prazo de 1 semana; ganho marginal nao justifica |
| RFM / segmentacao de clientes | Olist tem taxa de recompra proxima de zero — segmentos sem significado pratico |
| Chat em tempo real / streaming | Dataset e historico/batch |
| App mobile | Showcase, nao produto |
| Features pos-entrega no modelo | Vazamento de dados — invalida credibilidade do modelo |
| Accuracy como headline metric | Enganosa com ~15-20% de classe positiva (reviews 1-2 estrelas) |

## Rastreabilidade

| Requisito | Fase | Status |
|-----------|------|--------|
| KICK-01 | Phase 1: Kickoff e Contratos | Pendente |
| KICK-02 | Phase 1: Kickoff e Contratos | Pendente |
| KICK-03 | Phase 1: Kickoff e Contratos | Pendente |
| KICK-04 | Phase 1: Kickoff e Contratos | Pendente |
| KICK-05 | Phase 1: Kickoff e Contratos | Pendente |
| DATA-01 | Phase 2: Data Foundation | Completo (02-01) |
| DATA-02 | Phase 2: Data Foundation | Pendente |
| DATA-03 | Phase 2: Data Foundation | Pendente |
| DATA-04 | Phase 2: Data Foundation | Pendente |
| DATA-05 | Phase 2: Data Foundation | Pendente |
| EDA-01 | Phase 3: EDA — Ato 1 | Pendente |
| EDA-02 | Phase 3: EDA — Ato 1 | Pendente |
| EDA-03 | Phase 3: EDA — Ato 1 | Pendente |
| EDA-04 | Phase 3: EDA — Ato 1 | Pendente |
| EDA-05 | Phase 3: EDA — Ato 1 | Pendente |
| ML-01 | Phase 4: ML — Ato 2 | Pendente |
| ML-02 | Phase 4: ML — Ato 2 | Pendente |
| ML-03 | Phase 4: ML — Ato 2 | Pendente |
| ML-04 | Phase 4: ML — Ato 2 | Pendente |
| ML-05 | Phase 4: ML — Ato 2 | Pendente |
| ML-06 | Phase 4: ML — Ato 2 | Pendente |
| ML-07 | Phase 4: ML — Ato 2 | Pendente |
| PRES-01 | Phase 5: Narrativa e Slides | Pendente |
| PRES-02 | Phase 5: Narrativa e Slides | Pendente |
| PRES-06 | Phase 5: Narrativa e Slides | Pendente |
| PRES-03 | Phase 6: Demo Streamlit e Integracao Final | Pendente |
| PRES-04 | Phase 6: Demo Streamlit e Integracao Final | Pendente |
| PRES-05 | Phase 6: Demo Streamlit e Integracao Final | Pendente |
| PRES-07 | Phase 6: Demo Streamlit e Integracao Final | Pendente |

**Cobertura:**
- Requisitos v1: 29 total
- Mapeados para fases: 29
- Nao mapeados: 0 (cobertura 100%)

---
*Requisitos definidos: 2026-03-01*
*Ultima atualizacao: 2026-03-01 — Rastreabilidade preenchida apos criacao do roadmap (6 fases)*
