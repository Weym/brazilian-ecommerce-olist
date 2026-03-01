---
phase: 03-eda-ato-1
plan: 02
subsystem: eda
tags: [geopandas, folium, seaborn, choropleth, heatmap, geo-aggregation, parquet]

requires:
  - phase: 02-data-foundation
    provides: "olist_gold.parquet (97456, 38) com customer_state, seller_state, bad_review, freight_value, order_delivered_customer_date, order_estimated_delivery_date"

provides:
  - "data/processed/geo_aggregated.parquet: 27 UFs com bad_review_rate normalizado (0.075-0.238)"
  - "docs/brazil_states.geojson: GeoJSON do Brasil baixado e cacheado localmente"
  - "reports/figures/eda03_choropleth_bad_reviews_uf.png: mapa coropletico por UF (YlOrRd)"
  - "reports/figures/eda03_choropleth_static.html: mapa interativo folium"
  - "reports/figures/eda05_rotas_heatmap.png: heatmap top-15 origens x 27 destinos (RdYlGn_r)"
  - "notebooks/FASE3-P2-eda-geo.ipynb: notebook geo EDA com 12 celulas documentadas"

affects:
  - 05-narrativa-e-slides
  - 06-demo-streamlit

tech-stack:
  added: [folium==0.20.0, kaleido (instalado mas Chrome headless indisponivel)]
  patterns:
    - "GeoJSON cached localmente em docs/ para evitar re-download"
    - "Deteccao automatica do campo de sigla do GeoJSON com fallback para multiplos nomes de campo"
    - "Timestamp columns removidas do GeoDataFrame antes de serializar para folium (JSON serialization fix)"
    - "Aggregation pipeline: groupby -> agg -> assign(bad_review_rate) -> reset_index"

key-files:
  created:
    - notebooks/FASE3-P2-eda-geo.ipynb
    - data/processed/geo_aggregated.parquet
    - docs/brazil_states.geojson
    - reports/figures/eda03_choropleth_bad_reviews_uf.png
    - reports/figures/eda03_choropleth_static.html
    - reports/figures/eda05_rotas_heatmap.png
  modified: []

key-decisions:
  - "GeoJSON campo de sigla = 'sigla' (nao 'abbrev_state' nem 'UF') — detectado via auto-probe das colunas"
  - "Choropleth PNG usa fallback geopandas/matplotlib (kaleido requer Chrome headless, indisponivel no ambiente Windows sem GPU/display)"
  - "dias_atraso derivado defensivamente de order_delivered_customer_date - order_estimated_delivery_date mesmo que actual_delay_days exista na gold table — garante contrato do plano"
  - "Todos os 27 estados brasileiros presentes no dataset (AC ate TO), merge 100% completo"
  - "Atraso medio negativo (-11.9 dias) significa entregas antecipadas em relacao ao prazo estimado — insight importante para narrativa"

patterns-established:
  - "Fallback geopandas para PNG quando plotly/kaleido indisponivel: fig.savefig(dpi=150, bbox_inches=tight)"
  - "Limpeza de colunas Timestamp do GeoDataFrame antes de __geo_interface__ para folium"
  - "Pivot table seller_state x customer_state com aggfunc=mean para heatmap de rotas"

requirements-completed: [EDA-03, EDA-05]

duration: 15min
completed: 2026-03-01
---

# Phase 3 Plan 2: EDA Geografica Summary

**Mapa coropletico por UF (bad_review_rate normalizado, AL=23.8% pior) e heatmap 15x27 de rotas com geopandas/folium, exportando geo_aggregated.parquet para Streamlit**

## Performance

- **Duration:** 15 min
- **Started:** 2026-03-01T22:05:00Z
- **Completed:** 2026-03-01T22:20:00Z
- **Tasks:** 2
- **Files modified:** 6

## Accomplishments

- `geo_aggregated.parquet` com 27 UFs e 6 colunas de schema (bad_review_rate 0.075-0.238), normalizado por taxa — AL lidera (23.8%), SP nao domina (12.1%)
- Mapa coropletico interativo (folium HTML) e estatico (PNG 113KB via geopandas) com escala YlOrRd por bad_review_rate
- Heatmap de rotas 15x27 (99KB) mostrando atraso medio por corredor vendedor x cliente — top-15 origens por volume filtradas para legibilidade
- GeoJSON do Brasil cacheado em docs/brazil_states.geojson (3.3MB), campo sigla detectado automaticamente

## Geo Aggregated Data

**27 UFs no dataset** — range bad_review_rate: 0.075 (DF) a 0.238 (AL)

**Top 5 UFs por bad_review_rate:**

| UF | bad_review_rate | total_orders |
|----|----------------|--------------|
| AL | 23.8% | 408 |
| RR | 22.2% | 45 |
| MA | 21.4% | 730 |
| SE | 20.9% | 344 |
| RJ | 19.9% | 12537 |

**Insight:** AL lidera a taxa apesar de baixo volume — normalizacao por taxa (nao contagem) e essencial para que SP nao domine o mapa artificialmente.

## GeoJSON Field Discovery

- **Campo de sigla encontrado:** `sigla` (primeira opcao da lista de candidatos)
- **GeoJSON colunas:** id, name, sigla, regiao_id, codigo_ibg, cartodb_id, created_at, updated_at, geometry
- **Merge resultado:** 27/27 UFs com dados (100% cobertura)

## Top 10 Corredores Mais Atrasados (>= 50 pedidos)

| Origem (seller) | Destino (cliente) | Atraso Medio (dias) | Volume |
|-----------------|-------------------|--------------------:|-------:|
| RJ | CE | -6.4 | 54 |
| SP | AL | -8.0 | 253 |
| PR | CE | -9.3 | 63 |
| SP | MA | -9.3 | 486 |
| SP | SE | -9.4 | 208 |
| BA | BA | -9.4 | 66 |
| SP | ES | -9.6 | 1446 |
| MA | SP | -9.9 | 122 |
| SP | SP | -10.1 | 30547 |
| SP | MS | -10.2 | 477 |

**Nota:** Todos os atrasos sao negativos (entregas antecipadas). O atraso medio geral e -11.9 dias. Os corredores "mais atrasados" sao os que ficam mais proximos do prazo estimado — RJ->CE (-6.4 dias) e o corredor com menor folga.

## Metodo Usado para PNG do Choropleth

**Metodo:** Fallback geopandas/matplotlib (`br_merged.plot(column="bad_review_rate", cmap="YlOrRd", dpi=150)`)

Razao: kaleido requer Chrome headless para renderizar imagens plotly. O Chrome instalado no ambiente Windows falhou ao iniciar em modo headless (`BrowserFailedError: The browser seemed to close immediately after starting`). O fallback geopandas produz PNG de qualidade equivalente para slides.

## Task Commits

1. **Task 1: EDA-03 — Agregacao geo + GeoJSON + Choropleth por UF** - `73e47dd` (feat)
2. **Task 2: EDA-05 — Heatmap de Rotas Origem x Destino** - `ab10216` (feat)

## Files Created/Modified

- `notebooks/FASE3-P2-eda-geo.ipynb` — notebook com 12 celulas: setup, load, agregacao, GeoJSON, merge, folium, PNG, heatmap, top-corredores
- `data/processed/geo_aggregated.parquet` — 27 UFs x 6 colunas, schema contratado para Streamlit Phase 6
- `docs/brazil_states.geojson` — GeoJSON Brasil (3.3MB), campo sigla=sigla
- `reports/figures/eda03_choropleth_bad_reviews_uf.png` — 113KB, 150 DPI, YlOrRd
- `reports/figures/eda03_choropleth_static.html` — mapa folium interativo
- `reports/figures/eda05_rotas_heatmap.png` — 99KB, 150 DPI, pivot 15x27, RdYlGn_r

## Decisions Made

1. Campo `sigla` detectado automaticamente no GeoJSON — sem necessidade de ajuste manual
2. Fallback geopandas para PNG do choropleth (kaleido/Chrome indisponivel no ambiente)
3. `dias_atraso` derivado defensivamente de timestamps mesmo que `actual_delay_days` exista no gold
4. Timestamp columns removidas do GeoDataFrame antes de `__geo_interface__` para evitar erro de serializacao JSON do folium
5. `legend_kwds={"label": ...}` sem `format` — o formato `{:.0%}` causa `IndexError` no matplotlib 3.10 com `tight_layout`

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Folium choropleth falhou com TypeError: Timestamp not JSON serializable**
- **Found during:** Task 1 (celula 6 — choropleth interativo)
- **Issue:** GeoDataFrame pos-merge continha colunas `created_at` e `updated_at` do GeoJSON com dtype `datetime64[ns]`, nao serializaveis para JSON pelo Jinja2/folium
- **Fix:** Remocao das colunas Timestamp antes de chamar `__geo_interface__` para o mapa folium
- **Files modified:** run_geo_eda.py (script de execucao), refletido no notebook
- **Verification:** HTML exportado com sucesso (eda03_choropleth_static.html)
- **Committed in:** 73e47dd (Task 1 commit)

**2. [Rule 1 - Bug] matplotlib tight_layout falhou com IndexError no formato {:.0%}**
- **Found during:** Task 1 (celula 7 — choropleth estatico PNG)
- **Issue:** `legend_kwds={"format": "{:.0%}"}` causa `IndexError: tuple index out of range` no matplotlib 3.10 porque o formatador interpreta `%` como argumento posicional vazio
- **Fix:** Removido o campo `format` do legend_kwds; label mantido sem formatacao percentual
- **Files modified:** run_geo_eda.py (script de execucao), refletido no notebook
- **Verification:** PNG exportado com sucesso (113KB)
- **Committed in:** 73e47dd (Task 1 commit)

**3. [Rule 3 - Blocking] kaleido indisponivel para export de PNG plotly**
- **Found during:** Task 1 (pre-execucao, ao testar plotly write_image)
- **Issue:** kaleido requer Chrome headless; Chrome no Windows falhou com `BrowserFailedError` ao iniciar em modo automatizado
- **Fix:** Usado fallback geopandas/matplotlib conforme documentado no plano como contingencia valida
- **Files modified:** run_geo_eda.py usa diretamente o fallback; notebook celula 7 documenta a razao
- **Verification:** PNG 113KB gerado, verificacao > 10KB passou
- **Committed in:** 73e47dd (Task 1 commit)

---

**Total deviations:** 3 auto-fixed (2 bugs, 1 blocking)
**Impact on plan:** Todos os must_haves satisfeitos. PNG gerado via fallback documentado no plano. Sem impacto nos artefatos de saida.

## Issues Encountered

- `atraso_medio` negativo em todos os corredores: dataset Olist tem estimativas de prazo muito conservadoras — entregas chegam antes do prazo estimado em media 11.9 dias. Corredores "mais atrasados" sao os com menor folga. Este insight deve ser mencionado na narrativa do Ato 1.

## Next Phase Readiness

- `geo_aggregated.parquet` pronto para Phase 6 (Streamlit) — schema contratado com 6 colunas
- 2 PNGs prontos para Phase 5 (slides) — mapa UF + heatmap rotas
- GeoJSON cached em docs/ para reuso sem re-download
- Insight de atraso negativo disponivel para narrativa da Pessoa 2 no Ato 1

## Self-Check: PASSED

- data/processed/geo_aggregated.parquet: EXISTS (27 UFs, 6 cols, bad_review_rate 0.075-0.238)
- reports/figures/eda03_choropleth_bad_reviews_uf.png: EXISTS (113,655 bytes > 10KB)
- reports/figures/eda05_rotas_heatmap.png: EXISTS (99,679 bytes > 10KB)
- reports/figures/eda03_choropleth_static.html: EXISTS
- docs/brazil_states.geojson: EXISTS (3,378,231 bytes)
- notebooks/FASE3-P2-eda-geo.ipynb: EXISTS (13,057 bytes, 12 code cells)
- Commit 73e47dd: FOUND (feat(03-02): EDA-03)
- Commit ab10216: FOUND (feat(03-02): EDA-05)

---
*Phase: 03-eda-ato-1*
*Completed: 2026-03-01*
