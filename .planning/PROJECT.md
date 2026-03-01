# Olist Challenge — Logística, Satisfação e Risco Pré-Entrega

## O Que É Isso

Projeto de análise de dados em formato de desafio relâmpago (1 semana) com time de 6 pessoas, usando o dataset público da Olist (e-commerce brasileiro). A entrega é uma apresentação impactante para liderança com narrativa em dois atos: primeiro provando como logística degrada a satisfação do cliente, depois propondo um modelo preditivo que antecipa pedidos em risco antes da entrega acontecer.

O público é misto (técnico + negócio), e o objetivo central é impressionar a liderança demonstrando processo rigoroso, insights acionáveis e capacidade técnica do time.

## Core Value

**Mostrar que é possível agir antes do problema acontecer** — transformar dados históricos de logística em um sistema de alerta precoce que permite intervenção antes da entrega e da avaliação ruim.

## Requisitos

### Validados

(Nenhum ainda — sprint ativo)

### Ativos

- [ ] Tabela analítica "gold" construída com joins entre os dataframes da Olist (pedidos, clientes, vendedores, geolocalização, avaliações)
- [ ] EDA visual mostrando impacto de atraso, distância e frete na nota final
- [ ] Mapa/heatmap de regiões/UFs com maior concentração de insatisfação
- [ ] Modelo ML que prevê risco de avaliação ruim (estrelas 1–2) usando apenas features disponíveis até o momento de expedição
- [ ] Pipeline de features "pré-entrega" (sem vazamento: nenhuma variável que dependa de dados pós-entrega)
- [ ] Baseline simples (regressão logística ou árvore de decisão) como fallback garantido
- [ ] Métrica orientada a ação: recall e PR-AUC, com limiar de decisão e impacto operacional estimado
- [ ] Slides com narrativa em dois atos (Problema → Motor de risco → Ações)
- [ ] Notebooks documentados por área (data foundation, EDA, ML)
- [ ] Demo ao vivo em Streamlit (decisão ainda aberta — Streamlit recomendado por impacto/velocidade)
- [ ] Relatório escrito com achados e recomendações

### Fora de Escopo

- Chat em tempo real ou dados de streaming — dataset é histórico/batch
- Features que dependem de data real de entrega (vazamento de dados) — guardrail inegociável
- Modelos deep learning — complexidade desnecessária para o prazo
- App mobile ou infraestrutura de produção — é um showcase, não deploy real
- Pessoa 5 (NLP/Reviews) como foco principal — enriquecimento opcional se sobrar tempo

## Contexto

**Dataset:** [Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/) — múltiplos dataframes relacionais conectáveis por chaves de pedido/cliente/vendedor/geo. Inclui: orders, order_items, order_reviews, order_payments, customers, sellers, products, geolocation, category_name_translation.

**Narrativa em dois atos:**
- **Ato 1 (EDA):** Evidenciar a "dor real" com dados — atrasos, distância e frete degradam a nota e concentram insatisfação em rotas/regiões específicas.
- **Ato 2 (ML):** Elevar com solução — modelo pré-entrega que prevê risco de avaliação 1–2 estrelas antes que o problema aconteça.

**Divisão do time (6 pessoas):**
| Pessoa | Função | Responsabilidade |
|--------|--------|-----------------|
| 1 | Data Lead | Tabela gold, joins, limpeza, checklist de qualidade |
| 2 | Geo/Logística | Distância/rota, agregações por UF/cidade, mapas |
| 3 | EDA & Métricas | Gráficos atraso vs nota, frete vs total, segmentações |
| 4 | ML Lead | Pipeline features, baseline + modelo, validação, explicabilidade |
| 5 | NLP/Reviews | Tópicos/sentimento dos comentários (opcional, enriquecimento) |
| 6 | Storytelling | Deck, roteiro, padronização visual, costura dos achados |

**Fases do projeto:**
- **Fase 0 – Kickoff (30–60 min):** Alinhar hipótese, dicionário de métricas, congelar recorte temporal e regras de outlier
- **Fase 1 – Data Foundation:** Tabela gold, validação de qualidade, diagrama de dados
- **Fase 2 – EDA do Impacto:** Mapas, heatmaps, gráficos de atraso × nota × frete
- **Fase 3 – ML Pré-Entrega:** Features até expedição, baseline + modelo, métricas orientadas a ação
- **Fase 4 – Story + Demo:** Playbook de intervenção, 3 slides-chave, demo ao vivo

**Guardrails definidos:**
1. Features pré-entrega apenas — qualquer variável que dependa de entrega real está proibida
2. Baseline simples antes de modelos complexos — garante entrega mesmo se faltar tempo
3. Métrica orientada a ação — recall/PR-AUC com limiar de decisão e impacto operacional

**IA como copiloto:** Acelerador de execução (código, análise, comunicação), não substituto das definições do time (target, corte temporal, o que é pré-entrega).

## Restrições

- **Prazo:** 1 semana (desafio relâmpago)
- **Time:** 6 pessoas com papéis fixos (sem redistribuição mid-sprint)
- **Stack:** Python (pandas, sklearn, plotly/seaborn esperados); demo em Streamlit (decisão pendente de confirmação na Fase 0)
- **Dados:** Dataset público Kaggle, sem acesso a dados complementares externos
- **Audiência:** Misto técnico + negócio — linguagem e visuais devem funcionar para os dois perfis
- **Integridade:** Nenhuma feature pós-entrega no modelo (guardrail de credibilidade)

## Decisões-Chave

| Decisão | Racional | Resultado |
|---------|----------|-----------|
| Target = estrelas 1–2 | Definição rigorosa e defensável; separa claramente insatisfação real | — Pendente |
| Demo em Streamlit | Maior impacto para audiência mista, entregável em horas, sem custo | — Pendente (confirmar na Fase 0) |
| Baseline obrigatório antes de modelos complexos | Garante entregável mesmo se ML avançado não fechar no prazo | — Pendente |
| Features apenas pré-expedição | Evita vazamento e mantém credibilidade do modelo | — Pendente |

---
*Última atualização: 2026-03-01 após inicialização*
