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

Execute as fases em ordem:

| Fase | Descricao | Notebook principal |
|------|-----------|--------------------|
| 1 | Kickoff e Contratos | (este setup) |
| 2 | Data Foundation | `FASE2-P1-consolidacao.ipynb` |
| 3 | EDA | `FASE3-P1-eda-distribucoes.ipynb` |
| 4 | Modelagem | `FASE4-P1-modelo-xgboost.ipynb` |
| 5 | Narrativa e Slides | `FASE5-P1-narrativa.ipynb` |
| 6 | Demo Streamlit | `app/app.py` |

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
