# Roteiro do Deck — Risco Pre-Entrega Olist
**Deck:** [URL do Google Slides — preencher apos criacao]
**Duracao estimada:** ~20 minutos (18 slides principais)
**Publico:** Gestores de negocio + time tecnico

---

## Inventario de Figuras (reports/figures/)

| Arquivo | Slide | Descricao |
|---------|-------|-----------|
| `eda01_atraso_vs_nota_scatter.png` | Slide 04 | Scatter atraso vs. nota |
| `eda01_atraso_vs_nota_boxplot.png` | Slide 04 | Boxplot atraso vs. nota (com e sem atraso) |
| `eda02_frete_vs_nota.png` | Slide 05 | Frete (freight_ratio) vs. nota |
| `eda03_choropleth_bad_reviews_uf.png` | Slide 06 | Choropleth UF — proporcao de bad_review |
| `eda05_rotas_heatmap.png` | Slide 07 | Heatmap origem x destino — corredores criticos |
| `eda04_categorias_ruins.png` | Slide 08 | Top categorias com maior proporcao de bad_review |
| `pr_curve.png` | Slide 12 | Curva Precision-Recall — baseline vs XGBoost |
| `shap_beeswarm.png` | Slide 14 e A3 | SHAP beeswarm top 15 features |

---

## Slide 01 — Titulo
**Titulo:** Risco Pre-Entrega em E-commerce
**Subtitulo:** Como identificar pedidos de alto risco antes da entrega ruim acontecer
**Corpo:** Dataset Olist | 97.456 pedidos | 2016–2018
**Notas do presenter:** Contextualizar: Olist e um marketplace brasileiro; dataset publico com dados reais de logistica e avaliacoes. Periodo de 2 anos garante sazonalidade e diversidade de corredores logisticos.

## Slide 02 — Pergunta de Negocio
**Titulo:** A Pergunta que Queremos Responder
**Corpo:** "Como agir ANTES da entrega ruim acontecer?"
**Sub-bullet:** Avaliacoes ruins chegam depois da entrega — quando nao ha mais nada a fazer
**Sub-bullet:** E possivel identificar pedidos de alto risco no momento da expedicao?
**Notas do presenter:** Enfatizar "antes" — e a proposta de valor central. O sistema proposto usa apenas informacoes disponiveis no momento da aprovacao do pedido (order_approved_at) — nenhum dado pos-entrega.

## Slide 03 — Headline Ato 1
**Titulo:** ATO 1: A DOR
**Headline:** "Atraso causa insatisfacao — aqui esta a evidencia"
**Notas do presenter:** Transicao para dados. "Antes de falar em solucao, precisamos provar que o problema existe e quantificar onde ele acontece."

## Slide 04 — Atraso vs Nota
**Titulo:** Atraso Derruba a Nota
**Figura:** `reports/figures/eda01_atraso_vs_nota_boxplot.png` (boxplot principal) + `reports/figures/eda01_atraso_vs_nota_scatter.png` (scatter complementar)
**Legenda:** Pedidos com atraso vs. no prazo — nota mediana e distribuicao completa
**Corpo:**
- Nota mediana pedidos no prazo: **5,0 estrelas**
- Nota mediana pedidos com atraso: **2,0 estrelas**
- Mann-Whitney p < 0,001 — diferenca altamente significativa
- Distribuicoes completamente separadas: no prazo concentra em 5 estrelas; atrasados concentram em 1-2 estrelas
**Notas do presenter:** Explicar que Mann-Whitney foi usado porque notas sao ordinais (1-5), nao seguem distribuicao normal. O p-valor extremamente baixo confirma que a diferenca nao e por acaso.

## Slide 05 — Frete vs Nota
**Titulo:** Frete Tambem Importa
**Figura:** `reports/figures/eda02_frete_vs_nota.png`
**Corpo:**
- freight_ratio (frete / valor total do pedido) e maior em pedidos com bad_review=1 do que em bad_review=0
- Mann-Whitney p < 0,05 — diferenca estatisticamente significativa
- Um frete de R$30 em um pedido de R$50 (60% do valor) gera muito mais insatisfacao do que o mesmo frete em um pedido de R$300 (10%)
**Notas do presenter:** Mencionar tanto valor absoluto quanto percentual do pedido. A metrica freight_ratio captura o impacto relativo — o que importa para o cliente e a proporcao, nao o valor absoluto.

## Slide 06 — Mapa Geografico
**Titulo:** Onde Estao os Problemas? (Por UF)
**Figura:** `reports/figures/eda03_choropleth_bad_reviews_uf.png`
**Corpo:**
- Media nacional de bad_review: **13,9%**
- UFs com maior proporcao de bad_review: **MA, RN, AL** (Nordeste) — proporcoes acima da media nacional
- SP e MG, apesar do alto volume absoluto, tem proporcoes proximas ou abaixo da media
**Notas do presenter:** Destacar que ha padroes regionais claros — nao e um problema uniforme. O choropleth usa proporcao (nao contagem absoluta) para comparar estados de tamanhos diferentes de forma justa.

## Slide 07 — Rotas Criticas
**Titulo:** Os Corredores Mais Problematicos
**Figura:** `reports/figures/eda05_rotas_heatmap.png`
**Corpo:**
- Corredores mais criticos: **SP-MA, SP-CE, SP-RN** — maior concentracao de atrasos e bad_review
- Filtro de volume: apenas corredores com >= 50 pedidos exibidos (estabilidade estatistica)
- Distancia vendedor-cliente e a 3a feature mais importante no modelo (SHAP = 0,098)
**Notas do presenter:** Heatmap mostra origem x destino — concentracao em corredores especificos e acionavel: SLAs diferentes por corredor, parceiros logisticos regionais.

## Slide 08 — Categorias
**Titulo:** Categorias de Alto Risco
**Figura:** `reports/figures/eda04_categorias_ruins.png`
**Corpo:**
- Top 3 categorias com maior proporcao de bad_review: **eletronicos portateis, moveis, artigos de cama/banho/mesa**
- `computers_accessories` e `telephony` aparecem tanto no ranking de categorias quanto nas top features SHAP do modelo
- Filtro: apenas categorias com >= 100 pedidos (evitar categorias raras com proporcoes instáveis)
**Notas do presenter:** Categorias sao acionaveis — embalagem diferenciada, alinhamento de expectativas na pagina do produto, parceiros especificos com problemas recorrentes.

## Slide 09 — Conclusao Ato 1
**Titulo:** O Que Aprendemos no Ato 1
**Corpo:**
- Atraso e o principal driver — evidenciado estatisticamente (p < 0,001)
- Ha concentracao geografica — corredores SP-Nordeste sao criticos
- Ha categorias de risco elevado — eletronicos e moveis lideram
**Headline:** "Sabemos ONDE e QUANDO o problema acontece. Podemos prever ANTES?"
**Notas do presenter:** Transicao natural para Ato 2. "Temos o diagnostico. Agora vamos construir a solucao."

## Slide 10 — Transicao Ato 2
**Titulo:** ATO 2: A SOLUCAO
**Headline:** "Podemos prever o risco ANTES da entrega?"
**Corpo:** Usando apenas informacoes disponiveis no momento da expedicao (order_approved_at) — sem data leakage
**Notas do presenter:** Enfatizar "antes da entrega" — sem usar dados pos-entrega. O corte temporal e order_approved_at: tudo o que sabemos no momento em que o pedido e aprovado e o que o modelo usa.

## Slide 11 — Nossa Abordagem
**Titulo:** Como Construimos o Motor de Risco
**Bullet 1:** **Features pre-entrega apenas** — 13 variaveis auditadas (nenhuma pos-entrega)
**Bullet 2:** **Baseline logistico obrigatorio** — patamar minimo antes de qualquer complexidade
**Bullet 3:** **XGBoost** — captura interacoes nao-lineares entre features (ex.: distancia alta + prazo alto = risco amplificado)
**Bullet 4:** **Threshold definido por impacto operacional** — Precision >= 40% como criterio primario, nao acuracia
**Notas do presenter:** Mencionar que baseline primeiro e uma pratica de engenharia — garante sanidade antes de modelos complexos. Se XGBoost nao superar baseline, a complexidade nao se justifica.

## Slide 12 — Curva PR + Threshold
**Titulo:** XGBoost Supera o Baseline
**Figura:** `reports/figures/pr_curve.png`
**Legenda:** Curva Precision-Recall — baseline LogReg (laranja) vs XGBoost (azul)
**Corpo:**
- PR-AUC Baseline (LogReg): **0,2207**
- PR-AUC XGBoost: **0,2283** (+3,4% sobre baseline)
- Threshold escolhido: **0,785** — Precision = **0,40** | Recall = **0,02**
**Notas do presenter:** Explicar PR-AUC em linguagem simples: "Quanto maior, melhor o modelo em encontrar pedidos de risco sem alarmar pedidos seguros." Em datasets desbalanceados (13,9% positivos), ROC-AUC engana — PR-AUC e a metrica correta.

## Slide 13 — Resultado Operacional
**Titulo:** O Que Isso Significa na Pratica?
**Headline grande:** **"40% dos pedidos flagrados sao de fato risco real"**
**Corpo:**
- ~**8 pedidos flagrados por semana** (0,8% dos pedidos totais)
- **40% deles (= ~3 pedidos/semana) sao risco real** de avaliacao ruim
- Volume humanamente gerenciavel para uma equipe de operacoes
- Threshold 0,785 escolhido para Precision = 40% — cada alerta tem valor real
**Notas do presenter:** Converter abstrato em concreto. "Isso nao e 90% dos pedidos — e 8 por semana. Uma equipe de 2 pessoas consegue tratar isso sem sobrecarga." O trade-off consciente: alta precisao, baixo recall — cirurgico, nao abrangente.

## Slide 14 — SHAP: O Que o Modelo Aprendeu
**Titulo:** As Features Mais Importantes
**Figura:** `reports/figures/shap_beeswarm.png`
**Legenda:** SHAP beeswarm — top 15 features no test set (amostra de 5.000 registros)
**Corpo:**
- #1: `order_item_count` (SHAP = 0,188) — pedidos com mais itens tem maior risco
- #2: `customer_state_RJ` (SHAP = 0,101) — destino Rio de Janeiro
- #3: `seller_customer_distance_km` (SHAP = 0,098) — distancia vendedor-cliente
**Notas do presenter:** SHAP explica cada predicao individual — nao e uma "caixa preta". O beeswarm mostra tanto a importancia quanto a direcao do efeito (vermelho = valor alto, azul = valor baixo de cada feature).

## Slide 15 — Tabela de Vendedores
**Titulo:** Quais Vendedores Merecem Atencao Imediata?
**Corpo:** Top-10 vendedores com maior score medio de risco (elegibilidade: >= 10 pedidos)

| Vendedor (ID parcial) | Score Medio de Risco | Total de Pedidos | Pedidos de Alto Risco |
|----------------------|---------------------|-----------------|----------------------|
| 40db9e9a... | 0,713 | 11 | 2 |
| eed78ac1... | 0,649 | 21 | 2 |
| 1ca7077d... | 0,647 | 114 | 5 |
| 49067458... | 0,646 | 15 | 1 |
| 4324dd16... | 0,631 | 12 | 1 |
| 82e0a475... | 0,629 | 41 | 5 |
| 1fe5540d... | 0,623 | 20 | 3 |
| 712e6ed8... | 0,618 | 78 | 4 |
| 17f51e71... | 0,616 | 55 | 1 |
| ff69aa92... | 0,615 | 20 | 1 |

**Notas do presenter:** "Esta tabela e acionavel — operacoes pode contatar esses vendedores esta semana." O vendedor 1ca7077d com 114 pedidos e score 0,647 e particularmente impactante: alto volume E alto risco. Foco nos top-5 para reuniao de alinhamento.

## Slide 16 — Conclusao Ato 2
**Titulo:** O Que Temos ao Final do Ato 2
**Headline:** "Temos um motor de alerta precoce funcional"
**Corpo:**
- Modelo treinado com 77.964 pedidos historicos reais (2016-2018)
- Threshold calibrado para impacto operacional (Precision = 40%)
- Lista de vendedores prioritarios identificada (top-10 de 1.247 elegíveis)
- Pipeline serializado em `models/final_pipeline.joblib` — pronto para integracao

## Slide 17 — Recomendacoes Operacionais
**Titulo:** O Que Fazer Com Isso?
**Recomendacao 1:** **Monitoramento proativo** — alertar ~8 pedidos/semana automaticamente via score >= 0,785 no momento da aprovacao do pedido
**Recomendacao 2:** **Intervencao com top vendedores de risco** — reuniao + auditoria com os 5 de maior score medio (score > 0,64); foco especial no vendedor 1ca7077d (114 pedidos, score 0,647)
**Recomendacao 3:** **Revisao de SLAs nos corredores criticos** — SP-MA, SP-CE, SP-RN; ajustar prazos estimados exibidos ao cliente nessas rotas
**Notas do presenter:** Recomendacoes especificas e acionaveis — evitar generalidades como "melhorar a logistica". Cada recomendacao tem um responsavel natural: TI (alerta automatico), Parcerias (vendedores), Logistica (SLAs).

## Slide 18 — Proximos Passos
**Titulo:** Roadmap Tecnico
**Curto prazo (30 dias):**
- Piloto em corredor SP-MA (maior concentracao de risco): medir reducao de bad_review nos pedidos flagrados vs. grupo de controle
- Definir metrica de sucesso operacional com a equipe de operacoes
**Medio prazo (3-6 meses):**
- Retreinamento trimestral com dados mais recentes (modelo atual usa 2016-2018)
- Adicionar features de rastreamento em tempo real (primeiro scan nos Correios)
- Calibracao de probabilidades (Platt scaling) para scores mais interpretaveis
**Longo prazo:**
- Deploy via API com integracao ao sistema de atendimento ao cliente
- Expansao para outros corredores e categorias de alto risco
- GridSearchCV para hiperparametros do XGBoost (ganho potencial de 3-8% no PR-AUC)

---

## APENDICE TECNICO

*(Nao apresentado — backup para perguntas)*

## Slide A1 — PR-AUC Detalhado
**Titulo:** Metricas Completas do Modelo
**Conteudo:** Tabela completa de metricas no test set (19.492 pedidos, 80/20 estratificado):

| Metrica | Baseline (LogReg) | XGBoost |
|---------|------------------|---------|
| PR-AUC (test set) | 0,2207 | 0,2283 |
| Recall no threshold | 0,53 (threshold padrao 0,5) | 0,02 (threshold 0,785) |
| Precision no threshold | — | 0,40 |
| Pedidos flagrados/semana | — | ~8 pedidos |
| Proporcao flagrada | — | 0,8% dos pedidos |

**Nota:** Recall = 0,02 e uma limitacao conhecida e documentada — modelo opera em modo de alta precisao cirurgica. Para capturar mais pedidos de risco (Recall >= 0,60), Precision cairia para ~18%.

## Slide A2 — Metodologia
**Titulo:** Como o Modelo Foi Treinado
**Conteudo:**
- **Divisao treino/test:** 80/20 estratificada por bad_review — Treino: 77.964 pedidos | Teste: 19.492 pedidos
- **Balanceamento:** class_weight='balanced' (LogReg) e scale_pos_weight=6,21 (XGBoost) — sem SMOTE
- **Features:** 13 features pre-entrega da allow-list PRE_DELIVERY_FEATURES (sem nenhuma variavel pos-entrega)
- **Preprocessamento:** SimpleImputer (mediana/moda) + StandardScaler (numericas) + OneHotEncoder (categoricas, handle_unknown='ignore')
- **Anti-leakage:** Assert explicito verifica que nenhuma FORBIDDEN_FEATURE esta no modelo antes do treino
- **Sem GridSearchCV:** Hiperparametros escolhidos como defaults razoaveis — ganho marginal nao justifica risco de prazo

## Slide A3 — SHAP Ampliado
**Titulo:** SHAP Beeswarm — Top 15 Features (Detalhado)
**Figura:** `reports/figures/shap_beeswarm.png` (versao ampliada / zoom nas features principais)
**Conteudo:**
- TreeExplainer aplicado em amostra de 5.000 registros do test set (dos 19.492 disponiveis)
- Top 5 features por impacto medio absoluto:
  1. order_item_count (0,188)
  2. customer_state_RJ (0,101)
  3. seller_customer_distance_km (0,098)
  4. price (0,069)
  5. seller_state_SP (0,049)
- Cores: vermelho = valor alto da feature; azul = valor baixo

## Slide A4 — Parametros XGBoost
**Titulo:** Hiperparametros do Modelo
**Conteudo:**

| Parametro | Valor | Justificativa |
|-----------|-------|---------------|
| n_estimators | 300 | Default razoavel; ganho marginal apos 300 arvores e baixo |
| max_depth | 4 | Profundidade moderada — evita overfitting em 77k amostras |
| learning_rate | 0,05 | Conservador para estabilidade; combina bem com 300 estimators |
| scale_pos_weight | 6,21 | Calculado de y_train: (1-0,139)/0,139 — corrige desbalanceamento |
| objective | binary:logistic | Classificacao binaria (bad_review = 0 ou 1) |
| eval_metric | aucpr | Otimiza PR-AUC durante treino (alinhado com metrica de avaliacao) |

## Slide A5 — Limitacoes e Riscos
**Titulo:** O Que o Modelo Nao Faz (Ainda)
**Conteudo:**
- **Dataset historico 2016-2018:** comportamento logistico pode ter mudado; retreinamento periodico necessario antes de producao
- **Recall muito baixo (0,02):** Modelo cirurgico — captura apenas 2% dos pedidos de risco real. Para capturar mais, precision cai para ~18% (mapeado na curva PR)
- **Sem calibracao de probabilidades:** Scores sao ordinais (maior = mais risco), mas nao sao probabilidades absolutas. Score 0,785 nao = 78,5% de probabilidade. Para dashboards com custo absoluto, usar Platt scaling
- **Features limitadas ao momento de expedicao:** Sem rastreamento em tempo real — primeiro scan nos Correios aumentaria a precisao significativamente
- **Hiperparametros nao otimizados:** Sem GridSearchCV — ganho potencial de 3-8% no PR-AUC com tuning sistematico
- **Seller_id como feature ausente:** Identidade do vendedor nao e usada como feature direta (usa-se state e distancia) — para producao, considerar entity embedding por vendedor
