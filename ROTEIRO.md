# Roteiro de Trabalho — Olist Challenge (6 Pessoas, 1 Semana)

> **Objetivo:** Sistema de alerta precoce de risco pré-entrega — narrativa em dois atos para liderança técnica e de negócio.
> **Stack:** Python · pandas · sklearn · XGBoost · SHAP · Streamlit

---

## Papéis do Time

| # | Papel | Responsabilidade central |
|---|-------|--------------------------|
| **P1** | Data Lead | Tabela gold, joins, limpeza, qualidade de dados |
| **P2** | Geo / Logística | Distância Haversine, mapas coropleth, análise de rotas |
| **P3** | EDA & Métricas | Gráficos atraso × nota × frete, segmentação por categoria |
| **P4** | ML Lead | Pipeline de features, Baseline + XGBoost, SHAP, threshold |
| **P5** | NLP / Reviews | Análise de sentimento e tópicos dos comentários *(opcional)* |
| **P6** | Storytelling | Deck de slides, roteiro narrativo, documentação dos notebooks |

---

## Visão Geral do Cronograma

```
DIA 1          DIA 2          DIA 3          DIA 4-5        DIA 6          DIA 7
│              │              │              │              │              │
├─ FASE 1 ────┤              │              │              │              │
│  Kickoff &   │              │              │              │              │
│  Contratos   │              │              │              │              │
│  (todos)     │              │              │              │              │
│              ├─ FASE 2 ────┤              │              │              │
│              │  Data        │              │              │              │
│              │  Foundation  │              │              │              │
│              │  (P1 + P2)   │              │              │              │
│              │              ├─ FASE 3 ───────────────────┤              │
│              │              │  EDA (P2+P3) │              │              │
│              │              ├─ FASE 4 ───────────────────┤              │
│              │              │  ML (P4)     │              │              │
│              │              │              │              ├─ FASE 5 ────┤
│              │              │              │              │  Narrativa   │
│              │              │              │              │  (P6+todos) │
│              │              │              │              │              ├─ FASE 6 ─
│              │              │              │              │              │  Demo
│              │              │              │              │              │  (todos)
```

---

## FASE 1 — Kickoff & Contratos *(Dia 1, todos juntos ~1–2h)*

**Objetivo:** Alinhar guardrails e criar a estrutura do repositório antes de qualquer código.

### P1 — Scaffold do repositório
**Arquivo:** *(raiz do projeto)*

- [ ] Criar estrutura de pastas: `data/raw/`, `data/gold/`, `data/processed/`, `notebooks/`, `src/`, `models/`, `reports/figures/`, `app/`, `docs/`
- [ ] Criar `.gitattributes` com filtro nbstripout (`*.ipynb filter=nbstripout`)
- [ ] Criar `requirements.txt` com dependências pinadas (pandas, sklearn, xgboost, shap, streamlit, plotly, seaborn, geopy, nbstripout)
- [ ] Criar `README.md` com estrutura de pastas, instrução de setup e convenção de notebooks (`FASE{N}-P{N}-descricao.ipynb`)
- [ ] Executar `nbstripout --install --attributes .gitattributes` — orientar o time a fazer o mesmo após clonar

> **Desbloqueador:** Nenhuma outra tarefa começa antes desta.

---

### P4 — Contrato de features *(logo após P1 criar as pastas)*
**Arquivos:** `src/__init__.py`, `src/features.py`, `docs/feature_contract.md`

- [ ] Criar `src/features.py` com as três constantes:
  - `PRE_DELIVERY_FEATURES` — 13 features pré-expedição (frete, prazo estimado, distância, produto, pedido)
  - `FORBIDDEN_FEATURES` — colunas proibidas (tudo pós-entrega: `order_delivered_customer_date`, `review_score`, `review_comment_message`, etc.)
  - `TARGET_COLUMN = "bad_review"` (1 se estrelas 1–2, 0 caso contrário)
- [ ] Criar `docs/feature_contract.md` — tabela legível com todas as colunas tagueadas como `[pré-entrega | pós-entrega | target | join-key]`
- [ ] Validar: `from src.features import PRE_DELIVERY_FEATURES` funciona da raiz

> **Regra de ouro:** `order_approved_at` é a âncora temporal. Nenhuma variável que dependa da data real de entrega entra no modelo — jamais.

---

### P6 — Documentos de acordo *(paralelo com P4)*
**Arquivos:** `docs/metrics_agreement.md`, `docs/kickoff.md`, `docs/ownership.md`

- [ ] `docs/metrics_agreement.md`: documentar que a métrica primária é **PR-AUC + Recall** (não accuracy, não ROC-AUC) e o racional
- [ ] `docs/kickoff.md`: documentar target binário (1–2 estrelas = positivo), âncora temporal (`order_approved_at`), recorte temporal e regras de outlier acordadas em reunião
- [ ] `docs/ownership.md`: tabela de ownership de notebooks por pessoa (quem é responsável por qual arquivo)
- [ ] Criar notebooks placeholder em `notebooks/` para cada pessoa (arquivo vazio com nome correto)

---

### Todos — Reunião de kickoff *(30–60 min)*

**Decisões que devem ser tomadas e registradas antes de qualquer join:**

- [ ] Confirmar target: avaliação ruim = estrelas 1 ou 2
- [ ] Confirmar âncora temporal: `order_approved_at` (não `order_purchase_timestamp`)
- [ ] Definir recorte temporal: quais datas incluir (ex: 2017–2018)
- [ ] Definir regras de outlier: o que fazer com pedidos de frete R$0, distâncias impossíveis etc.
- [ ] Confirmar demo em Streamlit
- [ ] Todos executam `nbstripout --install --attributes .gitattributes`

**Entregáveis da Fase 1:**
```
.gitattributes
requirements.txt
README.md
src/__init__.py
src/features.py
docs/feature_contract.md
docs/metrics_agreement.md
docs/kickoff.md
docs/ownership.md
notebooks/FASE{N}-P{N}-*.ipynb  ← placeholders por pessoa
```

---

## FASE 2 — Data Foundation *(Dia 2, P1 + P2)*

**Objetivo:** Construir a tabela gold — uma linha por `order_id` — e exportá-la como contrato imutável `.parquet`.

> **Bloqueio:** Fases 3 e 4 NÃO podem começar antes de `data/gold/olist_gold.parquet` existir.

### P1 — Join chain principal
**Arquivo:** `notebooks/FASE2-P1-data-foundation.ipynb`
**Seção 1 do notebook**

- [ ] Carregar os 9 CSVs da Olist de `data/raw/` com validação de shapes
  ```
  orders (~99k), items (~113k), reviews (~99k), payments, customers, sellers, products, geo, category_translation
  ```
- [ ] Pré-agregar `geolocation` para 1 linha por CEP prefix (média de lat/lon) — **crítico: sem isso o join explode**
- [ ] Pré-agregar `items` por `order_id` (sum de freight/price, seller_id = first)
- [ ] Desduplicar `reviews` por `order_id` (manter a mais recente)
- [ ] Pré-agregar `payments` por `order_id`
- [ ] Join chain: `orders → items_agg → reviews_dedup → payments_agg → customers → sellers → products → category_translation`
- [ ] Validar: `gold_raw["order_id"].is_unique == True` (sem explosão de cardinalidade)
- [ ] Filtrar: remover pedidos `canceled`/`unavailable` e pedidos sem `review_score`

### P2 — Enriquecimento geo + feature engineering
**Arquivo:** `notebooks/FASE2-P1-data-foundation.ipynb` *(continuação) + `notebooks/FASE2-P2-features.ipynb`*

- [ ] Join de lat/lon de seller e customer via `seller_zip_code_prefix` / `customer_zip_code_prefix`
- [ ] Calcular distância **Haversine em km** (não graus decimais) entre seller e customer — coluna `seller_customer_distance_km`
- [ ] Calcular features derivadas:
  - `freight_ratio = freight_value / (price + freight_value)`
  - `estimated_delivery_days = order_estimated_delivery_date - order_approved_at` (em dias)
  - `product_volume_cm3 = length × width × height`
  - `order_item_count` (contagem de itens por pedido)
  - `bad_review = 1 se review_score in {1, 2}, else 0` (target)
- [ ] Criar `docs/data_quality.md`:
  - Contagem de nulos por coluna
  - Duplicatas verificadas
  - CEPs sem correspondência na geo (% de nulos em lat/lon)
  - Datas inconsistentes documentadas
- [ ] Taguear todas as colunas como `[pré-entrega | pós-entrega | target]` no notebook (células markdown)
- [ ] Export final: `data/gold/olist_gold.parquet`

**Entregáveis da Fase 2:**
```
notebooks/FASE2-P1-data-foundation.ipynb   ← P1: load, joins, filtros
notebooks/FASE2-P2-features.ipynb          ← P2: geo, Haversine, feature engineering
data/gold/olist_gold.parquet               ← CONTRATO IMUTÁVEL
docs/data_quality.md                       ← checklist de qualidade
```

> **Handoff:** Quando `olist_gold.parquet` existir, avisar P3, P4 e P5 — podem começar.

---

## FASE 3 — EDA (Ato 1) *(Dias 3–5, P3 + P2 em paralelo)*

**Objetivo:** Evidências visuais de que logística degrada satisfação. Gráficos prontos para slides.

> **Pré-requisito:** `data/gold/olist_gold.parquet` existindo.
> **P3 e P2 trabalham em notebooks separados — sem conflito de arquivo.**

### P3 — Atraso, frete e categorias
**Arquivo:** `notebooks/FASE3-P3-eda-metricas.ipynb`

- [ ] **EDA-01: Atraso vs Nota**
  - Derivar `dias_atraso = order_delivered_customer_date − order_estimated_delivery_date` (em dias)
  - **Boxplot** de `dias_atraso` por `review_score` (1–5) com linha em zero → export `eda01_atraso_vs_nota_boxplot.png`
  - **Scatter** amostrado (5k pontos, jitter, alpha baixo) → export `eda01_atraso_vs_nota_scatter.png`
  - **Mann-Whitney U test**: confirmar que pedidos `bad_review=1` têm maior atraso (p < 0.05)
- [ ] **EDA-02: Frete vs Nota**
  - Calcular `frete_pct_pedido = freight_value / (price + freight_value)` (protegido contra divisão por zero)
  - Gráfico duplo: frete absoluto (R$) + frete percentual, ambos por `review_score` → export `eda02_frete_vs_nota.png`
  - Spearman correlation frete × nota (confirmar direção negativa)
- [ ] **EDA-04: Categorias problemáticas**
  - Top-15 categorias por contagem de avaliações 1–2 estrelas
  - Gráfico de barras horizontais → export `eda04_categorias_ruins.png`

**Exports de P3:**
```
reports/figures/eda01_atraso_vs_nota_boxplot.png
reports/figures/eda01_atraso_vs_nota_scatter.png
reports/figures/eda02_frete_vs_nota.png
reports/figures/eda04_categorias_ruins.png
```

---

### P2 — Mapas geográficos e rotas
**Arquivo:** `notebooks/FASE3-P2-geo-mapas.ipynb`

- [ ] **EDA-03: Mapa de insatisfação por UF**
  - Agregação: % de `bad_review` por UF de destino (customer_state)
  - **Choropleth** do Brasil colorido por % de avaliações ruins → export `eda03_mapa_uf.png`
  - Exportar `data/processed/geo_aggregated.parquet` (usado pelo Streamlit na Fase 6 — não reprocessar ao vivo)
- [ ] **EDA-05: Heatmap de rotas problemáticas**
  - Agregação: % de atraso por par (seller_state × customer_state)
  - **Heatmap** de matriz origem × destino → export `eda05_heatmap_rotas.png`
  - Identificar top-5 corredores com maior concentração de atrasos

**Exports de P2:**
```
reports/figures/eda03_mapa_uf.png
reports/figures/eda05_heatmap_rotas.png
data/processed/geo_aggregated.parquet     ← artefato para Streamlit
```

---

## FASE 4 — ML (Ato 2) *(Dias 3–5, P4 — paralelo com EDA)*

**Objetivo:** Pipeline de risco pré-entrega funcional, explicável e operacionalmente acionável.

> **Pré-requisito:** `data/gold/olist_gold.parquet` + `src/features.py`
> **P4 trabalha em arquivo separado de P2 e P3 — sem conflito.**

### P4 — Pipeline ML completo
**Arquivo:** `notebooks/FASE4-P4-ml-pipeline.ipynb`

**Seção 1: Load & Feature Matrix**
- [ ] Importar `PRE_DELIVERY_FEATURES`, `FORBIDDEN_FEATURES`, `TARGET_COLUMN` de `src/features.py`
- [ ] Assert anti-leakage: nenhuma coluna de `FORBIDDEN_FEATURES` em `PRE_DELIVERY_FEATURES`
- [ ] Carregar gold table, verificar que todas as 13 features estão presentes
- [ ] Construir `X` e `y`, imprimir proporção de classe positiva
- [ ] Train/test split 80/20, **estratificado por `bad_review`**

**Seção 2: Baseline Logístico** *(entregável garantido)*
- [ ] Pipeline sklearn: `ColumnTransformer(StandardScaler + OneHotEncoder) → LogisticRegression(class_weight="balanced")`
- [ ] Fit exclusivamente em `X_train`
- [ ] Avaliar no test set: **PR-AUC** e **Recall** via `classification_report`
- [ ] Exportar `models/baseline_logreg.joblib` + round-trip check

**Seção 3: XGBoost**
- [ ] `XGBClassifier(scale_pos_weight=ratio, eval_metric="aucpr")` dentro do mesmo Pipeline
- [ ] Avaliar: PR-AUC e Recall no test set; comparar com baseline
- [ ] Exportar `models/xgb_pipeline.joblib`

**Seção 4: SHAP**
- [ ] `shap.TreeExplainer` no XGBoost
- [ ] **Beeswarm plot** dos top-15 features → export `reports/figures/ml04_shap_beeswarm.png`
- [ ] Identificar e documentar os 3 features mais importantes no notebook

**Seção 5: Threshold operacional**
- [ ] Curva Precision-Recall com marcação do limiar escolhido
- [ ] Estimar impacto: quantos pedidos flagrados/semana? qual % real de risco entre os flagrados?
- [ ] Export `reports/figures/ml05_pr_curve.png`

**Seção 6: Score por vendedor**
- [ ] Agregar score de risco médio por `seller_id`
- [ ] Exportar `data/processed/seller_risk_scores.parquet` (usado pelo Streamlit)

**Seção 7: Verificação final dos artefatos**
- [ ] Confirmar que `models/final_pipeline.joblib` (XGBoost) carrega e `predict_proba` funciona
- [ ] Confirmar que o pipeline carrega no app sem reprocessamento pesado

**Exports de P4:**
```
models/baseline_logreg.joblib
models/xgb_pipeline.joblib            ← pipeline final para Streamlit
data/processed/seller_risk_scores.parquet
reports/figures/ml04_shap_beeswarm.png
reports/figures/ml05_pr_curve.png
```

---

### P5 — NLP & Reviews *(opcional, paralelo com Fases 3–4)*
**Arquivo:** `notebooks/FASE5-P5-nlp-reviews.ipynb`
**Status: somente se sobrar tempo após Fases 1–4 garantidas**

- [ ] Análise de tópicos/sentimento dos `review_comment_message` de avaliações 1–2 estrelas
- [ ] Wordcloud ou gráfico de frequência de tópicos
- [ ] Se concluído: integrar achado em 1 slide do deck (Fase 5) e 1 card no Streamlit EDA (Fase 6)

---

## FASE 5 — Narrativa & Slides *(Dia 6, P6 + revisão do time)*

**Objetivo:** Deck de apresentação com dois atos + notebooks documentados para auditoria.

> **Pré-requisito:** Fases 3 e 4 completas (todos os PNGs e joblibs existindo).

### P6 — Deck de slides
**Arquivo:** `docs/slides_outline.md` → Google Slides (ou PowerPoint)

- [ ] Criar `docs/slides_outline.md` com roteiro completo da apresentação
- [ ] **Estrutura obrigatória do deck:**
  - Slide 1: Capa — "Risco Pré-Entrega: Como Agir Antes do Problema"
  - Slide 2: O problema em números (taxa de bad_review, impacto de 1–2 estrelas)
  - **Ato 1** (slides 3–7): A dor logística
    - `eda01_atraso_vs_nota_boxplot.png` + Mann-Whitney p-value
    - `eda02_frete_vs_nota.png`
    - `eda03_mapa_uf.png`
    - `eda04_categorias_ruins.png`
    - `eda05_heatmap_rotas.png`
  - Slide de transição: "E se pudéssemos prever antes?"
  - **Ato 2** (slides 9–13): O motor de risco
    - Features usadas (sem pós-entrega!) — de `docs/feature_contract.md`
    - Baseline vs XGBoost (PR-AUC e Recall comparados)
    - `ml04_shap_beeswarm.png` — o que o modelo aprendeu
    - `ml05_pr_curve.png` + estimativa operacional (pedidos flagrados/semana)
    - Tabela de top vendedores de risco
  - Slide 14: Recomendações operacionais (3 ações concretas)
  - Slide 15: Demo ao vivo → Streamlit
  - Apêndice: metodologia, métricas detalhadas, reprodutibilidade

---

### P6 — Relatório técnico
**Arquivo:** `docs/report.md` (5–8 páginas)

- [ ] Traduzir achados técnicos em linguagem de negócio
- [ ] Seções: Contexto → Dados → EDA → Modelo → Resultados → Recomendações Operacionais
- [ ] Adicionar seção "Resultados" ao `README.md` com PR-AUC, Recall e top features

---

### Todos — Documentar notebooks *(cada pessoa documenta o próprio)*
**Responsabilidade distribuída — sem conflito de arquivo**

| Notebook | Responsável |
|----------|-------------|
| `FASE2-P1-data-foundation.ipynb` | P1 |
| `FASE2-P2-features.ipynb` | P2 |
| `FASE3-P3-eda-metricas.ipynb` | P3 |
| `FASE3-P2-geo-mapas.ipynb` | P2 |
| `FASE4-P4-ml-pipeline.ipynb` | P4 |
| `FASE5-P5-nlp-reviews.ipynb` | P5 *(se existir)* |

**Checklist de documentação (cada pessoa aplica no próprio notebook):**
- [ ] Células markdown de decisão metodológica antes de seções críticas
- [ ] Nenhum path absoluto (`C:\Users\...`) — usar `pathlib.Path` relativo
- [ ] Outputs limpos no git (nbstripout ativo)
- [ ] Reprodução: rodar do topo ao fim deve funcionar sem intervenção manual

**Entregáveis da Fase 5:**
```
docs/slides_outline.md
docs/report.md → deck Google Slides
README.md (seção Resultados atualizada)
Notebooks de todas as fases documentados
```

---

## FASE 6 — Demo Streamlit & Integração Final *(Dia 7, todos)*

**Objetivo:** App multi-página carregando artefatos pré-computados — roda em < 3 segundos, não falha na apresentação.

> **Regra crítica:** Nenhum join, nenhum treino, nenhuma leitura de CSV durante a demo. Tudo pré-computado.

### P1 — Estrutura base do app
**Arquivos:** `app/app.py`, `app/utils/loaders.py`, `app/pages/1_Home.py`

- [ ] `app/app.py`: configurar multi-page Streamlit, título, tema, navegação
- [ ] `app/utils/loaders.py`: funções com `@st.cache_data` para carregar `olist_gold.parquet`, `geo_aggregated.parquet`, `seller_risk_scores.parquet` e `xgb_pipeline.joblib`
- [ ] `app/pages/1_Home.py`: página inicial com resumo do projeto, 4 KPIs em `st.metric` (total de pedidos, % bad_review, PR-AUC, Recall)

### P4 — Página do preditor
**Arquivo:** `app/pages/2_Preditor.py`

- [ ] Formulário com 5 inputs principais (frete, prazo estimado, distância, categoria, estado vendedor)
- [ ] Chamar `loaded_pipeline.predict_proba()` no input — sem reprocessamento pesado
- [ ] Exibir score de risco com gauge (Plotly) + ação recomendada baseada no threshold definido na Fase 4
- [ ] Carregar `models/xgb_pipeline.joblib` via `loaders.py` (cacheado)

### P2 — Página do mapa
**Arquivo:** `app/pages/3_Mapa.py`

- [ ] Carregar `data/processed/geo_aggregated.parquet` (pré-computado na Fase 3)
- [ ] Choropleth interativo por UF com filtros: estado de origem, estado de destino, faixa de risco
- [ ] Hover com 3 métricas: % bad_review, volume de pedidos, atraso médio
- [ ] Usar GeoJSON de UFs brasileiras (arquivo local em `app/assets/`)

### P3 — Página de EDA
**Arquivo:** `app/pages/4_EDA.py`

- [ ] Carregar PNGs pré-computados de `reports/figures/` com `st.image`
- [ ] `st.selectbox` para navegar entre os gráficos do Ato 1
- [ ] Texto explicativo (legenda) para cada gráfico — contexto para audiência de negócio

### P6 — Deploy & checklist final
**Arquivo:** `docs/demo_checklist.md`

- [ ] Smoke test local completo: abrir cada página, testar todos os filtros, verificar que nenhuma página demora > 3s
- [ ] Deploy no Streamlit Community Cloud (PRES-07 — sem processar dados pesados ao vivo)
- [ ] Criar `docs/demo_checklist.md` com script da demo (o que clicar e em que ordem durante a apresentação)
- [ ] Simular apresentação completa na máquina de apresentação

**Entregáveis da Fase 6:**
```
app/app.py
app/utils/loaders.py
app/pages/1_Home.py       ← P1
app/pages/2_Preditor.py   ← P4
app/pages/3_Mapa.py       ← P2
app/pages/4_EDA.py        ← P3
docs/demo_checklist.md    ← P6
```

---

## Mapa de Dependências e Conflitos

### Sequência obrigatória (bloqueadores)

```
Fase 1 (scaffold)
    └── Fase 2 (gold table)
            ├── Fase 3 (EDA)  ──┐
            └── Fase 4 (ML)  ──┤── Fase 5 (narrativa) ── Fase 6 (Streamlit)
```

### Quem pode trabalhar em paralelo

| Quando | P1 | P2 | P3 | P4 | P5 | P6 |
|--------|----|----|----|----|----|----|
| Fase 1 | Scaffold | Aguarda P1 | Aguarda P1 | Contrato features | NLP prep (leitura) | Docs de acordo |
| Fase 2 | Join chain | Geo + Haversine | **Bloqueado** | **Bloqueado** | **Bloqueado** | Roteiro slides (rascunho) |
| Fase 3+4 | Disponível para ajudar | Mapas EDA | Métricas EDA | Pipeline ML | NLP Reviews | Outline do deck |
| Fase 5 | Documenta notebook | Documenta notebooks | Documenta notebook | Documenta notebook | Documenta notebook | **Deck + Report** |
| Fase 6 | App base | Página mapa | Página EDA | Página preditor | Integra NLP se pronto | Deploy + checklist |

### Arquivos exclusivos por pessoa (nunca editar o arquivo do outro)

| Arquivo | Dono | Outras pessoas |
|---------|------|----------------|
| `notebooks/FASE2-P1-data-foundation.ipynb` | P1 | Só leitura |
| `notebooks/FASE2-P2-features.ipynb` | P2 | Só leitura |
| `notebooks/FASE3-P3-eda-metricas.ipynb` | P3 | Só leitura |
| `notebooks/FASE3-P2-geo-mapas.ipynb` | P2 | Só leitura |
| `notebooks/FASE4-P4-ml-pipeline.ipynb` | P4 | Só leitura |
| `src/features.py` | P4 (acordo de todos) | **Não modificar sem PR** |
| `app/pages/2_Preditor.py` | P4 | Só leitura |
| `app/pages/3_Mapa.py` | P2 | Só leitura |
| `app/pages/4_EDA.py` | P3 | Só leitura |
| `app/pages/1_Home.py` + `app/utils/loaders.py` | P1 | Só leitura |
| `docs/report.md` + `docs/slides_outline.md` | P6 | Só revisão |

### Arquivos compartilhados (comunicar antes de editar)

| Arquivo | Quem pode editar | Quando |
|---------|-----------------|--------|
| `data/gold/olist_gold.parquet` | P1 e P2 (Fase 2 apenas) | Depois da Fase 2 = **read-only para todos** |
| `reports/figures/` | Cada pessoa só cria seus PNGs | Nunca sobrescrever PNG de outro |
| `README.md` | P6 na Fase 5 | Comunicar antes |
| `requirements.txt` | P1 (Fase 1) + qualquer pessoa que precisar de nova lib | Comunicar antes — re-pin a versão |

---

## Guardrails Críticos (não negociáveis)

1. **Zero leakage:** Nenhuma feature que dependa de `order_delivered_customer_date`, `review_score` ou qualquer dado pós-entrega entra na matriz `X`. Usar `PRE_DELIVERY_FEATURES` de `src/features.py` como única fonte de verdade.

2. **Baseline antes de tudo:** `models/baseline_logreg.joblib` deve existir antes de qualquer XGBoost. Se o XGBoost não fechar no prazo, o baseline garante entrega.

3. **Métrica primária:** PR-AUC + Recall. Não reportar accuracy como headline — é enganosa com ~15–20% de classe positiva.

4. **Gold table é imutável:** Após `data/gold/olist_gold.parquet` exportado, não modificar. Se precisar recalcular algo, abrir issue com o time.

5. **Demo não processa dados ao vivo:** Todo arquivo carregado pelo Streamlit deve ser pré-computado. Nenhum join, nenhum treino durante a apresentação.

6. **Git limpo:** `nbstripout` ativo em todos os computadores. Antes de qualquer `git push`, verificar com `nbstripout --status`.

---

## Checklist de Entrega Final

### Artefatos de dados
- [ ] `data/gold/olist_gold.parquet` — tabela gold com 1 linha por `order_id`
- [ ] `data/processed/geo_aggregated.parquet` — agregações por UF para Streamlit
- [ ] `data/processed/seller_risk_scores.parquet` — score de risco por vendedor

### Modelos
- [ ] `models/baseline_logreg.joblib` — pipeline baseline (entregável mínimo garantido)
- [ ] `models/xgb_pipeline.joblib` — pipeline XGBoost (entregável principal)

### Notebooks (documentados, outputs limpos)
- [ ] `notebooks/FASE2-P1-data-foundation.ipynb`
- [ ] `notebooks/FASE2-P2-features.ipynb`
- [ ] `notebooks/FASE3-P3-eda-metricas.ipynb`
- [ ] `notebooks/FASE3-P2-geo-mapas.ipynb`
- [ ] `notebooks/FASE4-P4-ml-pipeline.ipynb`

### Figuras (PNG 150 DPI para slides)
- [ ] `reports/figures/eda01_atraso_vs_nota_boxplot.png`
- [ ] `reports/figures/eda01_atraso_vs_nota_scatter.png`
- [ ] `reports/figures/eda02_frete_vs_nota.png`
- [ ] `reports/figures/eda03_mapa_uf.png`
- [ ] `reports/figures/eda04_categorias_ruins.png`
- [ ] `reports/figures/eda05_heatmap_rotas.png`
- [ ] `reports/figures/ml04_shap_beeswarm.png`
- [ ] `reports/figures/ml05_pr_curve.png`

### Documentação
- [ ] `docs/feature_contract.md`
- [ ] `docs/metrics_agreement.md`
- [ ] `docs/kickoff.md`
- [ ] `docs/ownership.md`
- [ ] `docs/data_quality.md`
- [ ] `docs/report.md`
- [ ] `docs/slides_outline.md`
- [ ] `docs/demo_checklist.md`

### App
- [ ] `app/app.py` + `app/utils/loaders.py`
- [ ] `app/pages/1_Home.py` · `2_Preditor.py` · `3_Mapa.py` · `4_EDA.py`
- [ ] App abre em < 3s, todas as páginas funcionando, sem erro

### Apresentação
- [ ] Deck com Ato 1 (EDA) + Ato 2 (ML) + recomendações operacionais
- [ ] Demo ao vivo testada na máquina de apresentação

---

*Roteiro gerado com base no planejamento técnico do projeto — 2026-03-01*
