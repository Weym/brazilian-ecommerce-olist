# Olist — Sistema de Alerta Precoce de Risco Pre-Entrega

Transformar dados historicos de logistica em um sistema de alerta precoce que permite intervencao antes da entrega e da avaliacao ruim. O modelo classifica pedidos com risco de receber 1-2 estrelas **antes** da entrega acontecer, usando apenas variaveis disponíveis no momento da aprovacao do pedido.

---

## Estrutura de Pastas

```
.
├── data/
│   ├── raw/            # CSVs originais da Olist (nunca modificados)
│   ├── gold/           # olist_gold.parquet (contrato imutavel)
│   └── processed/      # agregacoes intermediarias
├── notebooks/          # notebooks por fase, convencao: FASE{N}-P{N}-descricao.ipynb
├── src/                # modulos Python reutilizaveis (features.py, etc.)
├── models/             # artefatos serializados (.joblib)
├── reports/
│   └── figures/        # imagens exportadas para slides
├── app/                # codigo Streamlit
├── docs/               # documentacao (contratos, acordos de metricas)
├── .gitattributes      # filtro nbstripout para notebooks
└── requirements.txt    # dependencias pinadas
```

---

## Resultados

### EDA — Ato 1: Impacto da Logistica

A analise exploratoria confirma que logistica e o principal driver de avaliacoes ruins:

- **Atraso** e o fator mais impactante: pedidos atrasados tem nota mediana 2,0 vs. 5,0 para pedidos no prazo (Mann-Whitney p < 0,001)
- **Concentracao geografica:** UFs nordestinas (MA, RN, AL) concentram desproporcionalmente as avaliacoes 1-2 estrelas — proporcao de bad_review acima da media nacional de 13,9%
- **Corredor critico:** rotas SP -> Nordeste (SP-MA, SP-CE, SP-RN) tem a maior concentracao de atrasos e avaliacoes ruins
- **Frete:** `freight_ratio` mediano e maior em pedidos com bad_review=1 — o impacto e proporcional ao valor do pedido, nao absoluto

### Modelo de Risco Pre-Entrega — Ato 2

| Metrica | Baseline (LogReg) | XGBoost |
|---------|------------------|---------|
| PR-AUC (test set) | 0,2207 | 0,2283 |
| Recall no threshold | 0,53 (threshold padrao) | 0,02 (threshold 0,785) |
| Precision no threshold | — | 0,40 |
| Pedidos flagrados/semana (estimativa) | — | 8 pedidos |

**Frase-ancora operacional:** "40% dos pedidos flagrados pelo modelo sao de fato pedidos de alto risco de avaliacao ruim — permitindo intervencao preventiva antes da entrega."

**Impacto estimado:** ~8 pedidos flagrados por semana com o threshold escolhido (threshold = 0,785, Precision = 0,40, Recall = 0,02).

**Top features (SHAP — impacto medio absoluto):**
1. `order_item_count` (0,188) — numero de itens no pedido
2. `customer_state_RJ` (0,101) — pedidos com destino ao Rio de Janeiro
3. `seller_customer_distance_km` (0,098) — distancia entre vendedor e cliente

Para detalhes completos: [`docs/report.md`](docs/report.md)

---

## Setup

Siga os passos abaixo apos clonar o repositorio:

```bash
# 1. Clonar o repositorio
git clone <url-do-repositorio>
cd <nome-do-repositorio>

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. OBRIGATORIO: configurar nbstripout (filtro de git para notebooks)
nbstripout --install --attributes .gitattributes

# 4. Verificar configuracao
nbstripout --status
```

> O passo 3 e **obrigatorio** para todos os contribuidores. O filtro nbstripout garante que outputs de notebooks (graficos, tabelas, dados) **nao sejam commitados** no repositorio. O filtro opera no modo `git filter` — a copia de trabalho local nao e modificada, apenas o que o git ve antes do commit.

---

## Convencao de Notebooks

Todos os notebooks seguem o padrao:

```
FASE{N}-P{N}-descricao.ipynb
```

Exemplos:
- `FASE2-P1-eda-distribucoes.ipynb`
- `FASE3-P1-feature-engineering.ipynb`
- `FASE4-P1-modelo-xgboost.ipynb`

---

## Dados

Os CSVs originais do dataset publico da Olist ficam em `data/raw/` e **nunca sao modificados**. O arquivo de contrato imutavel `olist_gold.parquet` fica em `data/gold/` e e gerado uma unica vez na Phase 2.

Para obter os dados brutos, baixe o [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) e coloque os CSVs em `data/raw/`.

---

## Reproducao

Execute os notebooks na seguinte ordem a partir da **raiz do projeto**:

1. `notebooks/FASE2-P1-data-foundation.ipynb` — Constroi a tabela gold (join chain, Haversine, tagging de colunas)
2. `notebooks/FASE3-P3-eda.ipynb` — Analise exploratoria — Ato 1 (atraso vs nota, frete, geo, rotas, categorias)
3. `notebooks/FASE4-P4-ml-pipeline.ipynb` — Pipeline de risco pre-entrega — Ato 2 (baseline LogReg + XGBoost + SHAP + threshold)

**Pre-requisito:** `pip install -r requirements.txt` e `nbstripout --install --attributes .gitattributes`

Os notebooks usam `Path.cwd()` para caminhos relativos — execute sempre da raiz do projeto, nao de dentro da pasta `notebooks/`.

---

## Documentacao

- `docs/feature_contract.md` — contrato de features (variaveis disponiveis antes da entrega)
- `docs/metrics_agreement.md` — acordo de metricas de avaliacao do modelo

---

## Notas de Arquitetura

- **Corte temporal de features:** apenas variaveis disponiveis em `order_approved_at` — nenhuma variavel pos-entrega no modelo
- **Target:** estrelas 1-2 (binario: `1` = insatisfacao real, `0` = satisfeito)
- **Demo Streamlit:** artefatos pre-computados — nenhum processamento pesado ao vivo
- **Baseline obrigatorio:** modelo logistico antes do XGBoost, garante entregavel mesmo se ML avancado nao fechar
