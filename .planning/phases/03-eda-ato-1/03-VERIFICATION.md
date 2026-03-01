---
phase: 03-eda-ato-1
verified: 2026-03-01T22:30:00Z
status: passed
score: 9/9 must-haves verified
re_verification: false
---

# Phase 3: EDA — Ato 1 Verification Report

**Phase Goal:** Visualizacoes e analises que provam como logistica degrada satisfacao do cliente
**Verified:** 2026-03-01T22:30:00Z
**Status:** PASSED
**Re-verification:** No — initial verification

---

## Goal Achievement

### Observable Truths (from ROADMAP.md Success Criteria)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Existe grafico (scatter + boxplot) mostrando relacao dias de atraso vs nota, com Mann-Whitney validado | VERIFIED | `eda01_atraso_vs_nota_boxplot.png` (40,717 bytes) e `eda01_atraso_vs_nota_scatter.png` (109,314 bytes) existem. Notebook celula 3: `Mann-Whitney U=673728514, p=0.00e+00` impresso com branch condicional confirmando p < 0.05. |
| 2 | Existe analise visual de frete (valor absoluto e % do pedido) vs nota mostrando direcao e magnitude | VERIFIED | `eda02_frete_vs_nota.png` (81,371 bytes) existe. Grafico duplo: frete absoluto (R$) + frete percentual vs nota. Spearman r=-0.088 (abs) e r=-0.031 (pct) com direcao negativa confirmada e ambos p << 0.05. |
| 3 | Existe mapa/heatmap geografico por UF mostrando concentracao de avaliacoes 1-2 estrelas, com `data/processed/geo_aggregated.parquet` exportado | VERIFIED | `eda03_choropleth_bad_reviews_uf.png` (113,655 bytes) existe. `geo_aggregated.parquet` existe com 27 UFs e bad_review_rate (nao contagem bruta) — AL=23.8%, SP=12.1% (SP nao domina). |
| 4 | Existe analise de rotas/corredores (UF origem x UF destino) identificando pares com maior concentracao de atrasos | VERIFIED | `eda05_rotas_heatmap.png` (99,679 bytes) existe. Pivot table 15x27 (top-15 origens por volume) com celula 12 imprimindo top-10 corredores mais atrasados com volume >= 50 pedidos. |
| 5 | As figuras exportadas estao em `reports/figures/` em formato PNG pronto para slides | VERIFIED | Todos os 6 PNGs exportados a 150 DPI em `reports/figures/`. Menores: 40,717 bytes; maiores: 113,655 bytes. Todos > 10KB. |

**Score:** 5/5 truths from ROADMAP Success Criteria — all VERIFIED

---

### Required Artifacts

| Artifact | Provided | Status | Size | Details |
|----------|----------|--------|------|---------|
| `notebooks/FASE3-P3-eda-metricas.ipynb` | EDA metricas (EDA-01, EDA-02, EDA-04) | VERIFIED | 14,517 bytes | 12 code cells + verificacao final. Cobre atraso, frete, categorias. Sem paths hardcoded absolutos — usa PROJECT_ROOT dinamico. |
| `reports/figures/eda01_atraso_vs_nota_boxplot.png` | Boxplot atraso vs nota para slides | VERIFIED | 40,717 bytes | 150 DPI, RdYlGn palette, linha de referencia em zero, order=[1,2,3,4,5]. |
| `reports/figures/eda01_atraso_vs_nota_scatter.png` | Scatter atraso vs nota (amostrado) | VERIFIED | 109,314 bytes | 5000 amostras com jitter, alpha=0.05, 150 DPI. |
| `reports/figures/eda02_frete_vs_nota.png` | Grafico duplo frete vs nota | VERIFIED | 81,371 bytes | Dois paineis: frete absoluto (R$) e frete percentual (payment_value como denominador). |
| `reports/figures/eda04_categorias_ruins.png` | Top-15 categorias ruins | VERIFIED | 85,444 bytes | Barras horizontais via seaborn fallback (kaleido/Chrome indisponivel). |
| `notebooks/FASE3-P2-eda-geo.ipynb` | EDA geo (EDA-03, EDA-05) | VERIFIED | 13,057 bytes | 12 code cells. Cobre choropleth UF + heatmap rotas. Deteccao automatica de campo sigla. |
| `data/processed/geo_aggregated.parquet` | Agregacao geografica para Streamlit | VERIFIED | 5,385 bytes | 27 UFs x 6 colunas. Todas colunas obrigatorias presentes. bad_review_rate range: 0.075-0.238 (dentro de 0-1). |
| `reports/figures/eda03_choropleth_bad_reviews_uf.png` | Mapa estatico por UF | VERIFIED | 113,655 bytes | geopandas fallback, 150 DPI, YlOrRd, taxa normalizada. |
| `reports/figures/eda05_rotas_heatmap.png` | Heatmap corredores origem x destino | VERIFIED | 99,679 bytes | Pivot 15x27, RdYlGn_r, center=0. |
| `docs/brazil_states.geojson` | GeoJSON Brasil cacheado | VERIFIED | 3,378,231 bytes | Campo sigla detectado automaticamente. 27/27 UFs com merge completo. |
| `reports/figures/eda03_choropleth_static.html` | Mapa folium interativo | VERIFIED | 2,198,112 bytes | Exportado com sucesso. Timestamp columns removidas antes de serializacao JSON. |

**Artifact score:** 11/11 — all VERIFIED

---

### Key Link Verification

#### Plan 03-01 Key Links

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `notebooks/FASE3-P3-eda-metricas.ipynb` | `data/gold/olist_gold.parquet` | `pd.read_parquet` | WIRED | Celula 4: `df = pd.read_parquet(GOLD)` onde `GOLD = PROJECT_ROOT / "data" / "gold" / "olist_gold.parquet"`. Path relativo via PROJECT_ROOT dinamico. |
| `notebooks/FASE3-P3-eda-metricas.ipynb` | `reports/figures/*.png` | `fig.savefig(..., dpi=150)` | WIRED | Celulas 8, 10, 14, 22: `fig.savefig(FIGURES / "eda0X_*.png", dpi=150, bbox_inches="tight")` — todos os 4 PNGs exportados. |

#### Plan 03-02 Key Links

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `notebooks/FASE3-P2-eda-geo.ipynb` | `data/gold/olist_gold.parquet` | `pd.read_parquet` | WIRED | Celula 4: `df = pd.read_parquet(GOLD)` — carregamento direto da gold table. |
| `geo_aggregated.parquet` | `data/processed/` | `geo_agg.to_parquet` | WIRED | Celula 6: `geo_agg.to_parquet(PROCESSED / "geo_aggregated.parquet", index=False)` — exportacao com schema completo. |
| `folium.Choropleth` | `docs/brazil_states.geojson` | `gpd.read_file + key_on sigla` | WIRED | Celulas 8-10: download do GeoJSON, `gpd.read_file(str(GEOJSON_PATH))`, deteccao de `SIGLA_COL = "sigla"`, e `key_on=f"feature.properties.{SIGLA_COL}"` no Choropleth folium. |

**All 5 key links WIRED.**

---

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| EDA-01 | 03-01-PLAN.md | Analise visual de atraso vs nota (scatter + boxplot) | SATISFIED | Celulas 3-5 no notebook. Mann-Whitney U=673728514, p=0.00e+00. Dois PNGs exportados (40KB e 109KB). |
| EDA-02 | 03-01-PLAN.md | Analise visual de frete (absoluto e %) vs nota | SATISFIED | Celulas 6-8 no notebook. Grafico duplo com Spearman r=-0.088 (negativo confirmado). PNG 81KB. |
| EDA-03 | 03-02-PLAN.md | Mapa geografico por UF — concentracao de avaliacoes 1-2 estrelas | SATISFIED | Celulas 3-7 no notebook. geo_aggregated.parquet exportado (27 UFs, bad_review_rate normalizado). PNG 113KB. |
| EDA-04 | 03-01-PLAN.md | Segmentacao por categoria de produto (top categorias problematicas) | SATISFIED | Celulas 9-11 no notebook. Top-15 barras horizontais. bed_bath_table (1505) lidera. PNG 85KB. |
| EDA-05 | 03-02-PLAN.md | Analise de rotas/regioes — origem x destino com maior concentracao de atrasos | SATISFIED | Celulas 8-12 no notebook. Pivot 15x27 origens. Heatmap RdYlGn_r exportado (99KB). Top-10 corredores impressos. |

**Requirements coverage: 5/5 — EDA-01 through EDA-05 all SATISFIED.**

Verificado contra REQUIREMENTS.md: todos os 5 IDs da Phase 3 mapeados e marcados como `[x]` no arquivo de requisitos. Nenhum requisito orphanado detectado — todos os IDs declarados nos PLANs correspondem exatamente aos IDs definidos para Phase 3 no REQUIREMENTS.md.

---

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| — | — | — | — | No anti-patterns detected |

Scan executado nos dois notebooks para: TODO/FIXME/PLACEHOLDER, `return null`, `return {}`, handlers so com `preventDefault`. Nenhum encontrado.

Desvios documentados no SUMMARY (uso de `payment_value` em vez de `price`, `review_score` cast para int, seaborn fallback para EDA-04, geopandas fallback para EDA-03) sao adapatacoes tecnicas validas previstas nos planos como contingencia, nao stubs.

---

### Commit Verification

| Commit | Task | Verificado |
|--------|------|-----------|
| `03782d4` | EDA-01 — Atraso vs Nota | FOUND — `feat(03-01): EDA-01 atraso vs nota — boxplot + scatter + Mann-Whitney` |
| `3687a54` | EDA-02 — Frete vs Nota | FOUND — `feat(03-01): EDA-02 frete vs nota — grafico duplo + Spearman` |
| `e9d622d` | EDA-04 — Segmentacao Categorias | FOUND — `feat(03-01): EDA-04 segmentacao por categoria — top-15 barras horizontais` |
| `73e47dd` | EDA-03 — Choropleth + geo_aggregated | FOUND — `feat(03-02): EDA-03 — agregacao geo + GeoJSON + choropleth por UF` |
| `ab10216` | EDA-05 — Heatmap Rotas | FOUND — `feat(03-02): EDA-05 — heatmap de rotas origem x destino (top-15 origens)` |

Todos os 5 commits documentados existem no repositorio e incluem os arquivos correspondentes.

---

### Human Verification Required

#### 1. Qualidade Visual dos Graficos para Slides

**Test:** Abrir os 6 PNGs em `reports/figures/` e avaliar legibilidade para projecao de slides.
**Expected:** Titulos legıveis, eixos com labels claros, escala de cores adequada (RdYlGn para boxplots, YlOrRd para mapa, RdYlGn_r para heatmap), sem sobreposicao de texto.
**Why human:** Qualidade visual e adequacao para apresentacao nao podem ser verificadas programaticamente.

#### 2. Mapa Coropletico — Cobertura Geografica Visual

**Test:** Abrir `reports/figures/eda03_choropleth_bad_reviews_uf.png` e verificar se todos os estados do Brasil aparecem coloridos no mapa (fallback geopandas foi usado em vez de plotly).
**Expected:** Mapa do Brasil com todos 27 estados visiveis, escala YlOrRd de bad_review_rate, sem estados em branco (exceto possivelmente os sem dados).
**Why human:** A qualidade da renderizacao geografica e a correta atribuicao de cores por UF requerem inspecao visual.

#### 3. Interpretacao Economica dos Valores de Atraso

**Test:** Revisar o SUMMARY e os graficos — todos os valores de `dias_atraso` sao negativos (media geral -11.9 dias), indicando entregas antecipadas.
**Expected:** A narrativa do Ato 1 deve reconhecer que "corredores mais atrasados" significa "menor folga em relacao ao prazo estimado", nao entregas pos-prazo. Este insight deve constar nos slides.
**Why human:** A interpretacao do sinal negativo e sua implicacao para a narrativa de negocio requer julgamento humano sobre o framing adequado.

---

### Gaps Summary

Nenhuma gap identificada. Todos os must-haves verificados em 3 niveis (existencia, substancia, ligacao).

---

## Summary

A Phase 3 atingiu plenamente seu objetivo. As 5 analises visuais que provam como a logistica degrada a satisfacao do cliente estao completas e em formato pronto para slides:

- **EDA-01:** Mann-Whitney U=673,728,514, p=0.00e+00 — evidencia estatistica solida de que pedidos com avaliacao ruim tem maior atraso (diferenca de mediana: 5 dias).
- **EDA-02:** Spearman r=-0.088, p=1.04e-164 — frete maior correlaciona com nota menor.
- **EDA-03:** Mapa coropletico por taxa (nao volume): AL=23.8% lidera, SP=12.1% nao domina artificialmente.
- **EDA-04:** bed_bath_table (1505), health_beauty (1070), computers_accessories (1033) — top-3 categorias problematicas identificadas.
- **EDA-05:** Heatmap 15x27 corredores com RJ->CE como corredor de menor folga (-6.4 dias vs media -11.9 dias).

Todos os artefatos de downstream (geo_aggregated.parquet para Streamlit Phase 6, 6 PNGs para slides Phase 5) estao prontos e contratados.

---

_Verified: 2026-03-01T22:30:00Z_
_Verifier: Claude (gsd-verifier)_
