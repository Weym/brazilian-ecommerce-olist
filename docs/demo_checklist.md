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

**Cenario 1 — Risco Baixo (verde esperado)**
- Frete: R$ 15, Preco: R$ 200, Prazo: 7 dias, Categoria: housewares, SP -> SP
- Score esperado: < 47% (verde)
- [ ] Verificado — score: ____%

**Cenario 2 — Risco Alto (vermelho esperado)**
- Frete: R$ 80, Preco: R$ 50, Prazo: 30 dias, Categoria: furniture_decor, SP -> AM
- Score esperado: > 78% (vermelho)
- [ ] Verificado — score: ____%

**Cenario 3 — Risco Medio (amarelo esperado)**
- Frete: R$ 35, Preco: R$ 120, Prazo: 15 dias, Categoria: sports_leisure, MG -> BA
- Score esperado: 47-78% (amarelo)
- [ ] Verificado — score: ____%

**Cenario 4 — Input do publico (improviso controlado)**
- Pedir para alguem da plateia sugerir valores
- [ ] Nenhum erro ao submeter

**Cenario 5 — Rotas Norte/Nordeste (risco esperado: alto)**
- Frete: R$ 60, Preco: R$ 80, Prazo: 25 dias, Categoria: bed_bath_table, SP -> PA
- Score esperado: alto (vermelho)
- [ ] Verificado — score: ____%

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
