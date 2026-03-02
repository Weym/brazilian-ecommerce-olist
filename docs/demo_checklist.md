# Checklist de Demo — Olist Risk Dashboard

**Ultima simulacao:** 2026-03-01
**App URL (Streamlit Cloud):** [URL apos deploy — preencher apos Task 2]
**Plano B (local):** `streamlit run app.py`

---

## Pre-Apresentacao (30 min antes)

- [ ] Abrir URL do Streamlit Cloud no celular — confirmar que carrega
- [ ] Abrir `streamlit run app.py` localmente como Plano B
- [ ] Confirmar que pipeline carregou (sem spinner permanente no Preditor)
- [ ] Confirmar que mapa renderizou (estados coloridos, nao cinzas)
- [ ] Ter pelo menos 1 aba com URL do Cloud e 1 com localhost:8501 abertas

---

## Roteiro da Demo (5 minutos)

### Pagina Home (30 segundos)
- [ ] Abrir pagina Home — mostrar estrutura do dashboard e premissa

### Pagina Preditor (2 minutos — peca central)

> Bandas calibradas nos scores reais do modelo (distribuicao 36-48%):
> Verde < 38% | Amarelo 38-44% | Vermelho > 44%
> Marcador vertical no gauge = threshold operacional (78.5%)

**Cenario 1 — Risco Baixo (verde)**
- Frete: R$ 15, Preco: R$ 200, Prazo: 7 dias, Categoria: housewares, SP -> SP
- Score real medido: ~37.7% (verde)
- [ ] Verificado — score: ____%

**Cenario 2 — Risco Medio (amarelo)**
- Frete: R$ 80, Preco: R$ 50, Prazo: 30 dias, Categoria: furniture_decor, SP -> AM
- Score real medido: ~41.6% (amarelo)
- [ ] Verificado — score: ____%

**Cenario 3 — Risco Alto (vermelho)**
- Frete: R$ 60, Preco: R$ 80, Prazo: 25 dias, Categoria: bed_bath_table, SP -> PA
- Score real medido: ~48.1% (vermelho)
- [ ] Verificado — score: ____%

**Cenario 4 — Input do publico (improviso controlado)**
- Pedir para alguem da plateia sugerir valores
- Dica: frete alto + prazo longo + rota Norte (SP->PA/AM/RR) tende a score mais alto
- [ ] Nenhum erro ao submeter

### Pagina Mapa (1 minuto)
- [ ] Mapa carregou com estados coloridos (27 estados no choropleth)
- [ ] Aplicar filtro: UF Destino = AM, PA, RR — mostrar concentracao no Norte
- [ ] Hover em AM — mostrar % bad review + atraso medio + volume
- [ ] Remover filtros — mapa volta ao estado completo

### Pagina EDA (1 minuto)
- [ ] Selecionar boxplot atraso vs nota — mostrar correlacao visual
- [ ] Selecionar heatmap rotas — conectar com mapa anterior
- [ ] Navegar com botoes prev/next

---

## Plano B — Se Streamlit Cloud Falhar

```bash
# Na maquina de apresentacao
cd [caminho/do/projeto]
streamlit run app.py
# Abrir: http://localhost:8501
```

**Pre-requisitos do Plano B (verificar antes do evento):**
- [ ] Python e streamlit instalados na maquina
- [ ] `pip install -r requirements.txt` executado
- [ ] Todos os artefatos presentes localmente (models/, data/, reports/)
- [ ] `streamlit run app.py` testado — abre sem erro

---

## Problemas Conhecidos e Solucoes

| Problema | Solucao |
|---------|---------|
| Streamlit Cloud em "sleep" — spinner por 30-60s | Acessar URL 15 min antes para fazer warm-up |
| Estados cinzas no mapa | Verificar featureidkey='properties.sigla' e siglas uppercase no parquet |
| Feature names mismatch no Preditor | Verificar src/features.py PRE_DELIVERY_FEATURES vs nomes no formulario |
| Pipeline nao carrega — versao mismatch | Verificar requirements.txt vs versoes do ambiente de treino |
| reports/figures/ vazio | Executar Phase 3 antes do deploy |
| Gauge nao aparece — erro de plotly | Confirmar plotly instalado: `pip install plotly` |

---

## Resultado da Simulacao Completa

**Data da simulacao:** ___________
**Executada por:** ___________
**Resultado:**
- [ ] APROVADO — todos os cenarios verificados, app sem erros
- [ ] REPROVADO — descrever issues abaixo

**Issues encontrados:**
(preencher durante simulacao)
