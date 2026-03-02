# Roadmap: Olist Challenge — Logistica, Satisfacao e Risco Pre-Entrega

## Overview

Este roadmap transforma 29 requisitos em 6 fases sequenciais que entregam uma apresentacao impactante para liderança sobre logistica, satisfacao e risco pre-entrega no e-commerce brasileiro. A jornada comeca com contratos explícitos que previnem os principais riscos do projeto (vazamento de dados, metrica errada, caos de notebooks), passa pela construcao da tabela gold que desbloqueia trabalho paralelo, evolui pelo Ato 1 (EDA provando a dor) e Ato 2 (modelo ML prevendo o risco), e culmina com slides de narrativa e uma demo ao vivo em Streamlit com artefatos pre-computados.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Kickoff e Contratos** - Time define contratos explícitos de features, metricas e ownership antes de qualquer codigo (completed 2026-03-01)
- [x] **Phase 2: Data Foundation** - Tabela gold validada como contrato imutavel que desbloqueia todos os tracks paralelos (completed 2026-03-01)
- [x] **Phase 3: EDA — Ato 1** - Visualizacoes e analises que provam como logistica degrada satisfacao do cliente (completed 2026-03-01)
- [x] **Phase 4: ML — Ato 2** - Pipeline de risco pre-entrega com baseline + XGBoost, SHAP e agregacao por vendedor (completed 2026-03-01)
- [x] **Phase 5: Narrativa e Slides** - Deck com dois atos, notebooks documentados e relatorio escrito (completed 2026-03-02)
- [ ] **Phase 6: Demo Streamlit e Integracao Final** - App multi-pagina carregando artefatos pre-computados, testada e pronta para apresentacao

## Phase Details

### Phase 1: Kickoff e Contratos
**Goal**: O time pode comecar a construir com seguranca porque todos os guardrails criticos estao documentados e acordados
**Depends on**: Nothing (first phase)
**Requirements**: KICK-01, KICK-02, KICK-03, KICK-04, KICK-05
**Success Criteria** (what must be TRUE):
  1. Existe um documento escrito listando explicitamente quais colunas sao permitidas e proibidas no modelo ML, com o corte temporal definido como `order_approved_at`
  2. Qualquer membro do time consultado sobre a metrica primaria responde "PR-AUC e Recall" — nao accuracy, nao ROC-AUC
  3. O repositorio tem estrutura de pastas definida e cada pessoa sabe qual notebook e seu e como nomea-lo
  4. O target do modelo esta documentado como binario: 1-2 estrelas = positivo, 3-5 estrelas = negativo
  5. O recorte temporal (datas de inclusao) e as regras de outlier estao escritos antes da primeira linha de codigo de join
**Plans**: 5 plans

Plans:
- [x] 01-01-PLAN.md — Scaffold do repositorio: pastas, .gitattributes, requirements.txt, README.md
- [ ] 01-02-PLAN.md — Contrato de features: src/features.py + docs/feature_contract.md
- [ ] 01-03-PLAN.md — Acordo de metricas: docs/metrics_agreement.md (PR-AUC, Recall, rationale)
- [ ] 01-04-PLAN.md — Kickoff document: docs/kickoff.md (target, ancora temporal, outliers)
- [ ] 01-05-PLAN.md — Ownership: notebooks placeholder por pessoa + docs/ownership.md

### Phase 2: Data Foundation
**Goal**: A tabela gold existe, esta validada e esta disponivel como contrato imutavel para todos os tracks downstream
**Depends on**: Phase 1
**Requirements**: DATA-01, DATA-02, DATA-03, DATA-04, DATA-05
**Success Criteria** (what must be TRUE):
  1. O arquivo `data/gold/olist_gold.parquet` existe, carrega sem erro e todas as colunas estao tagueadas como `[pre-entrega | pos-entrega | target]`
  2. Um checklist de qualidade de dados documentado mostra: contagem de nulos por coluna, duplicatas verificadas, CEPs invalidos tratados e datas inconsistentes resolvidas
  3. A coluna de distancia vendedor-comprador existe em km (via Haversine), e a distribuicao de valores esta entre 0 e 4000 km (nao em graus decimais)
  4. Qualquer notebook de EDA ou ML pode fazer `pd.read_parquet('data/gold/olist_gold.parquet')` e comecar analise imediatamente, sem nenhum join adicional
**Plans**: 3 plans

Plans:
- [x] 02-01-PLAN.md — Load dos 9 CSVs, pre-agregacao de geolocation e join chain principal (1 linha por order_id)
- [ ] 02-02-PLAN.md — Feature engineering: distancia Haversine em km, features derivadas, target bad_review e tagging de colunas
- [ ] 02-03-PLAN.md — Checklist de qualidade, export para data/gold/olist_gold.parquet e docs/data_quality.md

### Phase 3: EDA — Ato 1
**Goal**: O Ato 1 da apresentacao tem evidencias visuais solidas de que logistica (atraso, frete, rota) degrada a nota do cliente
**Depends on**: Phase 2
**Requirements**: EDA-01, EDA-02, EDA-03, EDA-04, EDA-05
**Success Criteria** (what must be TRUE):
  1. Existe um grafico (scatter + boxplot) mostrando a relacao entre dias de atraso e nota de avaliacao, com significancia estatistica validada (Mann-Whitney)
  2. Existe uma analise visual de frete (valor absoluto e % do pedido) vs. nota que mostra direcao e magnitude do efeito
  3. Existe um mapa/heatmap geografico por UF mostrando onde se concentram as avaliacoes 1-2 estrelas, com `data/processed/geo_aggregated.parquet` exportado
  4. Existe uma analise de rotas/corredores (UF origem x UF destino) identificando os pares com maior concentracao de atrasos
  5. As figuras exportadas estao em `reports/figures/` em formato PNG pronto para uso nos slides
**Plans**: 2 plans

Plans:
- [ ] 03-01-PLAN.md — Pessoa 3 track: EDA-01 atraso vs nota (boxplot + scatter + Mann-Whitney), EDA-02 frete vs nota, EDA-04 categorias
- [ ] 03-02-PLAN.md — Pessoa 2 track: EDA-03 choropleth UF + geo_aggregated.parquet, EDA-05 heatmap rotas origem x destino

### Phase 4: ML — Ato 2
**Goal**: O Ato 2 da apresentacao tem um modelo de risco pre-entrega funcional, explicavel e operacionalmente acionavel
**Depends on**: Phase 2
**Requirements**: ML-01, ML-02, ML-03, ML-04, ML-05, ML-06, ML-07
**Success Criteria** (what must be TRUE):
  1. O arquivo `src/features.py` contem a lista `PRE_DELIVERY_FEATURES` como allow-list explícita, e o pipeline de treino usa exclusivamente essas features
  2. O baseline logistico existe em `models/baseline_logreg.joblib` com PR-AUC e Recall reportados no test set, sem nenhuma feature pos-entrega na matriz X
  3. O pipeline XGBoost existe em `models/final_pipeline.joblib` com PR-AUC superior ao baseline, SHAP beeswarm calculado e os top features identificados
  4. Existe uma curva PR com limiar de decisao selecionado e estimativa operacional concreta: quantos pedidos seriam flagrados por semana e qual o percentual real de risco entre os flagrados
  5. Existe uma tabela de score de risco medio por vendedor que pode ser exibida na apresentacao como recomendacao acionavel
**Plans**: 4 plans

Plans:
- [ ] 04-01-PLAN.md — Secoes 1-2: Load & feature matrix (ML-01) + Baseline LogReg com PR-AUC e Recall (ML-02)
- [ ] 04-02-PLAN.md — Secoes 3-4: XGBoost com scale_pos_weight (ML-03) + SHAP TreeExplainer beeswarm PNG (ML-04)
- [ ] 04-03-PLAN.md — Secoes 5-7: Threshold operacional (ML-05) + tabela de vendedores (ML-06) + verificacao joblib (ML-07)
- [ ] 04-04-PLAN.md — Gap closure: documentacao da limitacao operacional (Recall=0.02) + narrativa para slides (ML-05)

### Phase 5: Narrativa e Slides
**Goal**: O deck de apresentacao conta a historia completa em dois atos e todos os notebooks estao documentados e prontos para auditoria
**Depends on**: Phase 3, Phase 4
**Requirements**: PRES-01, PRES-02, PRES-06
**Success Criteria** (what must be TRUE):
  1. O slide deck tem estrutura clara de dois atos: Ato 1 mostra a dor (logistica → insatisfacao) com os graficos da Phase 3; Ato 2 apresenta a solucao (modelo de risco) com metricas e SHAP da Phase 4
  2. Qualquer pessoa tecnica pode abrir os notebooks de data foundation, EDA e ML e reproduzir os resultados — outputs estao limpos, celulas documentadas, sem paths hardcoded
  3. O relatorio escrito traduz os achados tecnicos em linguagem de negocio com recomendacoes operacionais especificas
**Plans**: 3 plans

Plans:
- [x] 05-01-PLAN.md — Documentacao dos notebooks FASE2, FASE3, FASE4: celulas Markdown de decisao metodologica + paths relativos (PRES-02)
- [x] 05-02-PLAN.md — Relatorio tecnico docs/report.md (5-8 paginas) + secao Resultados no README (PRES-06)
- [ ] 05-03-PLAN.md — Roteiro slides_outline.md + construcao do deck Google Slides com dois atos e apendice tecnico (PRES-01)

### Phase 6: Demo Streamlit e Integracao Final
**Goal**: A demo ao vivo em Streamlit carrega instantaneamente com artefatos pre-computados e nao falha durante a apresentacao
**Depends on**: Phase 4, Phase 5
**Requirements**: PRES-03, PRES-04, PRES-05, PRES-07
**Success Criteria** (what must be TRUE):
  1. O app Streamlit multi-pagina inicia sem erro e carrega em menos de 3 segundos — nenhum join, nenhum treino de modelo acontece ao vivo
  2. A pagina de preditor aceita caracteristicas de um pedido como input e retorna um score de risco pre-entrega sem reprocessamento pesado
  3. A pagina de mapa tem filtros por UF/rota funcionando interativamente usando o arquivo `data/processed/geo_aggregated.parquet` pre-computado
  4. A pagina de EDA exibe os graficos principais do Ato 1 de forma navegavel, carregados de artefatos estaticos
  5. Uma simulacao completa da demo foi feita na maquina de apresentacao sem timeout, erro ou carregamento lento
**Plans**: 5 plans

Plans:
- [ ] 06-01-PLAN.md — Wave 1: app.py + utils/loaders.py + pages/1_Home.py + requirements.txt + GeoJSON local
- [ ] 06-02-PLAN.md — Wave 1 (paralelo): pages/2_Preditor.py — formulario 5 inputs + gauge Plotly + acao recomendada
- [ ] 06-03-PLAN.md — Wave 2: pages/3_Mapa.py — choropleth + 4 filtros interativos + hover 3 metricas
- [ ] 06-04-PLAN.md — Wave 2 (paralelo): pages/4_EDA.py — PNGs estaticos + st.selectbox navigation
- [ ] 06-05-PLAN.md — Wave 3: Smoke test local + deploy Streamlit Cloud + docs/demo_checklist.md

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 (parallel with 4) → 5 → 6

Note: Phases 3 and 4 can run in parallel after Phase 2 is complete. Phase 5 requires both Phase 3 and Phase 4 to be complete.

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Kickoff e Contratos | 5/5 | Complete   | 2026-03-01 |
| 2. Data Foundation | 3/3 | Complete   | 2026-03-01 |
| 3. EDA — Ato 1 | 2/2 | Complete   | 2026-03-01 |
| 4. ML — Ato 2 | 4/4 | Complete   | 2026-03-01 |
| 5. Narrativa e Slides | 3/3 | Complete   | 2026-03-02 |
| 6. Demo Streamlit e Integracao Final | 0/5 | Not started | - |
