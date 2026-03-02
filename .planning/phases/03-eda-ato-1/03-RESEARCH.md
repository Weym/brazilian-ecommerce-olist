# Phase 3: EDA — Ato 1 - Research

**Researched:** 2026-03-01
**Domain:** Exploratory Data Analysis — logistics impact on customer satisfaction (Olist dataset, Python DS stack, mixed audience)
**Confidence:** HIGH

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| EDA-01 | Analise visual de atraso (dias de atraso) vs. nota de avaliacao (scatter + boxplot) | Mann-Whitney U via `scipy.stats.mannwhitneyu`; seaborn boxplot + stripplot; plotly scatter; pattern fully documented below |
| EDA-02 | Analise visual de frete (valor absoluto e % do pedido) vs. nota de avaliacao | Same seaborn/plotly stack; frete_pct_pedido derived column; Pearson/Spearman for direction + magnitude |
| EDA-03 | Mapa/heatmap geografico por UF mostrando concentracao de avaliacoes 1–2 estrelas + export `data/processed/geo_aggregated.parquet` | geopandas 1.1.2 + folium 0.20.0 choropleth; IBGE GeoJSON source documented; aggregation pattern documented |
| EDA-04 | Segmentacao de avaliacoes ruins por categoria de produto (top categorias problematicas) | plotly bar chart on grouped gold table; `product_category_name_english` from translation table already in gold |
| EDA-05 | Analise de rotas/regioes com maior concentracao de atrasos (origem x destino UF) | 27x27 seaborn heatmap with `pivot_table`; filtering to top-N corridors for readability |
</phase_requirements>

---

## Summary

Phase 3 (EDA — Ato 1) produces the visual evidence for the first act of the narrative: logistics degrades customer satisfaction, and the pain is geographically concentrated. All five requirements (EDA-01 through EDA-05) draw from `data/gold/olist_gold.parquet` and write outputs to `reports/figures/` (PNG) and `data/processed/geo_aggregated.parquet`. The phase runs in parallel across two owners: Pessoa 3 handles quantitative EDA (EDA-01, EDA-02), Pessoa 2 handles geo and routing (EDA-03, EDA-05), and EDA-04 (category segmentation) is a lightweight addition owned by either.

The key technical decisions for this phase are: (1) use seaborn for static slide-ready charts and plotly for interactive notebook exploration — not both for the same chart; (2) use geopandas + folium for the Brazil choropleth, not plotly.express.choropleth, because folium integrates directly with geopandas and the IBGE GeoJSON; (3) for the 27x27 route heatmap, filter to the top-10 origin states by volume before pivoting, otherwise the chart is unreadable; (4) Mann-Whitney U is the correct significance test for delay vs. rating (non-parametric, non-normal distributions confirmed in Olist community analyses). All figures must be exported at 150 DPI minimum for slide legibility.

The phase has no ML component and no data modeling. Its sole risk is chart legibility for a mixed audience: avoid overplotting in scatter plots (use `alpha` and jitter), avoid raw counts in the choropleth (normalize to rate of bad reviews per UF), and always add chart titles and axis labels sufficient for a standalone slide.

**Primary recommendation:** Use seaborn for all publication-quality slide exports (boxplots, heatmaps, bar charts) and plotly for interactive notebook exploration. Export every figure with `fig.savefig(..., dpi=150, bbox_inches='tight')` for matplotlib/seaborn or `fig.write_image(..., scale=2)` for plotly. Choropleth goes through geopandas + folium — not plotly choropleth — because IBGE GeoJSON loads cleanly via geopandas.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| seaborn | 0.13.2 | Boxplots, violin plots, heatmaps for slides | Statistical chart types with sensible defaults; `theme()` produces publication-ready output |
| plotly | 6.5.2 | Interactive scatter, bar charts in notebooks | Native Streamlit integration; hover info for audience demos |
| geopandas | 1.1.2 | Load IBGE state polygons, spatial joins | Direct choropleth integration with folium; handles GeoJSON/shapefile natively |
| folium | 0.20.0 | Interactive choropleth map of Brazil by UF | Direct geopandas integration; exports HTML embeddable in Streamlit |
| scipy | 1.13.x | Mann-Whitney U test for EDA-01 significance | `scipy.stats.mannwhitneyu` is the standard non-parametric two-group test |
| matplotlib | 3.9.x | Backend for seaborn; `savefig` for PNG export | Required for DPI-controlled export of seaborn figures |
| pandas | 2.3.3 | Aggregation, pivot tables, derived columns | Already locked; all EDA aggregations use standard `groupby` + `pivot_table` |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| kaleido | 0.2.1 | Static PNG export from plotly figures | Required when using `fig.write_image()` — install alongside plotly |
| geopy | 2.x | GeoJSON source validation (backup) | Only if IBGE GeoJSON has CRS issues |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| folium choropleth | plotly.express.choropleth_mapbox | plotly choropleth requires manual GeoJSON featureidkey mapping; folium + geopandas is simpler for IBGE data |
| seaborn boxplot | plotly box | seaborn integrates with matplotlib `savefig` for PNG; plotly box needs kaleido; for slides use seaborn |
| 27x27 full heatmap | filtered top-N heatmap | Full 27x27 matrix is unreadable in slides — filter to top-10 or top-15 origin states by delay count |

**Installation:**
```bash
pip install seaborn==0.13.2 plotly==6.5.2 geopandas==1.1.2 folium==0.20.0 scipy kaleido
```

---

## Architecture Patterns

### Recommended Project Structure

```
notebooks/
├── FASE3-P3-eda-atraso-frete.ipynb      # EDA-01, EDA-02 (Pessoa 3)
├── FASE3-P2-geo-rotas.ipynb             # EDA-03, EDA-05 (Pessoa 2)
└── FASE3-P3-categorias.ipynb            # EDA-04 (Pessoa 3 or P2)

data/
├── gold/olist_gold.parquet              # Input — read-only
└── processed/geo_aggregated.parquet     # Output of EDA-03

reports/
└── figures/
    ├── eda01_atraso_vs_nota_boxplot.png
    ├── eda01_atraso_vs_nota_scatter.png
    ├── eda02_frete_vs_nota.png
    ├── eda03_choropleth_bad_reviews_uf.png
    ├── eda04_categorias_ruins.png
    └── eda05_rotas_heatmap.png

docs/
└── brazil_states.geojson                # IBGE GeoJSON (see source below)
```

### Pattern 1: Delay vs. Rating — Boxplot + Mann-Whitney (EDA-01)

**What:** Boxplot of `dias_atraso` by `review_score` group (bad_review=1 vs bad_review=0), then Mann-Whitney U to validate statistical significance.
**When to use:** Comparing distributions of a continuous variable across two non-normal groups.

```python
# Source: seaborn 0.13.2 docs + scipy.stats official docs
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

df = pd.read_parquet("data/gold/olist_gold.parquet")

# Derived column: dias_atraso (positive = late, negative = early)
# Assumes gold table has: order_estimated_delivery_date, order_delivered_customer_date
df["dias_atraso"] = (
    pd.to_datetime(df["order_delivered_customer_date"])
    - pd.to_datetime(df["order_estimated_delivery_date"])
).dt.days

# Group split for Mann-Whitney
bad  = df.loc[df["bad_review"] == 1, "dias_atraso"].dropna()
good = df.loc[df["bad_review"] == 0, "dias_atraso"].dropna()

stat, p = stats.mannwhitneyu(bad, good, alternative="greater")
print(f"Mann-Whitney U={stat:.0f}, p={p:.2e}")  # Expect p << 0.05

# Boxplot for slides
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(
    data=df,
    x="review_score",
    y="dias_atraso",
    palette="RdYlGn",
    order=[1, 2, 3, 4, 5],
    ax=ax,
)
ax.axhline(0, color="gray", linestyle="--", linewidth=0.8)
ax.set_title("Atraso vs. Nota de Avaliacao", fontsize=14)
ax.set_xlabel("Nota (estrelas)")
ax.set_ylabel("Dias de Atraso (positivo = atrasado)")
fig.tight_layout()
fig.savefig("reports/figures/eda01_atraso_vs_nota_boxplot.png", dpi=150, bbox_inches="tight")
```

### Pattern 2: Freight vs. Rating (EDA-02)

**What:** Derive `frete_pct_pedido = freight_value / (price + freight_value)`. Plot boxplot by `review_score`. Show direction (higher freight % → lower score) and magnitude (median frete_pct by score group).

```python
# Source: pandas 2.3.3 docs + seaborn 0.13.2 docs
df["frete_pct_pedido"] = df["freight_value"] / (df["price"] + df["freight_value"])

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Absolute freight value
sns.boxplot(data=df, x="review_score", y="freight_value",
            palette="RdYlGn", order=[1,2,3,4,5], ax=axes[0])
axes[0].set_title("Frete Absoluto vs. Nota")
axes[0].set_xlabel("Nota"); axes[0].set_ylabel("Valor do Frete (R$)")

# Freight as % of order value
sns.boxplot(data=df, x="review_score", y="frete_pct_pedido",
            palette="RdYlGn", order=[1,2,3,4,5], ax=axes[1])
axes[1].set_title("Frete como % do Pedido vs. Nota")
axes[1].set_xlabel("Nota"); axes[1].set_ylabel("Frete / (Preco + Frete)")

fig.tight_layout()
fig.savefig("reports/figures/eda02_frete_vs_nota.png", dpi=150, bbox_inches="tight")
```

### Pattern 3: Brazil Choropleth by UF (EDA-03)

**What:** Aggregate `bad_review` rate per `customer_state` UF, join with IBGE GeoJSON polygons, render folium choropleth, export PNG screenshot + save `geo_aggregated.parquet`.
**Brazil GeoJSON source:** IBGE official URL (verified as of 2026-03-01):
`https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson`
— or download from IBGE directly: `https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2022/Brasil/BR/BR_UF_2022.zip`

```python
# Source: geopandas 1.1.2 docs + folium 0.20.0 docs
import geopandas as gpd
import folium
import pandas as pd

df = pd.read_parquet("data/gold/olist_gold.parquet")

# Aggregate: bad_review rate per state
geo_agg = (
    df.groupby("customer_state")
    .agg(
        total_orders=("order_id", "count"),
        bad_reviews=("bad_review", "sum"),
    )
    .assign(bad_review_rate=lambda x: x["bad_reviews"] / x["total_orders"])
    .reset_index()
)
geo_agg.to_parquet("data/processed/geo_aggregated.parquet", index=False)

# Load Brazil states GeoJSON
br_states = gpd.read_file("docs/brazil_states.geojson")
br_states = br_states.merge(geo_agg, left_on="sigla", right_on="customer_state", how="left")

# Folium choropleth
m = folium.Map(location=[-15, -55], zoom_start=4, tiles="CartoDB positron")
folium.Choropleth(
    geo_data=br_states.__geo_interface__,
    data=geo_agg,
    columns=["customer_state", "bad_review_rate"],
    key_on="feature.properties.sigla",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.3,
    legend_name="Taxa de Avaliacoes 1-2 Estrelas",
).add_to(m)
m.save("reports/figures/eda03_choropleth_bad_reviews_uf.html")
# For PNG slide export: use selenium/playwright screenshot OR
# use plotly express as static fallback (see anti-patterns section)
```

**IBGE GeoJSON field mapping note:** The `sigla` field in the IBGE GeoJSON contains the 2-letter state abbreviation (SP, RJ, etc.) matching `customer_state` in the Olist gold table. Verify this field name when loading — alternate sources may use `abbrev_state` or `UF_05`.

### Pattern 4: Route/Corridor Heatmap (EDA-05)

**What:** Pivot table of average `dias_atraso` by `seller_state` (origin) × `customer_state` (destination). Filter to top-10 or top-15 origin states by order volume before pivoting — full 27x27 is unreadable in slides.

```python
# Source: pandas 2.3.3 + seaborn 0.13.2
import seaborn as sns
import matplotlib.pyplot as plt

# Filter to top-15 origin states by volume
top_origins = (
    df.groupby("seller_state")["order_id"].count()
    .nlargest(15).index
)

route_df = df[df["seller_state"].isin(top_origins)].copy()

pivot = route_df.pivot_table(
    values="dias_atraso",
    index="seller_state",   # origin
    columns="customer_state",  # destination
    aggfunc="mean",
)

fig, ax = plt.subplots(figsize=(16, 8))
sns.heatmap(
    pivot,
    cmap="RdYlGn_r",
    center=0,
    linewidths=0.3,
    annot=False,          # Too small for 15x27 — set True only for filtered view
    fmt=".1f",
    ax=ax,
)
ax.set_title("Atraso Medio (dias) por Corredor Origem x Destino", fontsize=13)
ax.set_xlabel("UF Destino (cliente)")
ax.set_ylabel("UF Origem (vendedor)")
fig.tight_layout()
fig.savefig("reports/figures/eda05_rotas_heatmap.png", dpi=150, bbox_inches="tight")
```

### Pattern 5: Category Segmentation (EDA-04)

```python
# Source: pandas 2.3.3 + plotly 6.5.2
import plotly.express as px

cat_agg = (
    df[df["bad_review"] == 1]
    .groupby("product_category_name_english")["order_id"]
    .count()
    .nlargest(15)
    .reset_index(name="bad_review_count")
)

fig = px.bar(
    cat_agg,
    x="bad_review_count",
    y="product_category_name_english",
    orientation="h",
    title="Top 15 Categorias com Mais Avaliacoes 1-2 Estrelas",
    labels={"bad_review_count": "Contagem", "product_category_name_english": "Categoria"},
)
fig.update_layout(yaxis={"categoryorder": "total ascending"})
# Export for slides
fig.write_image("reports/figures/eda04_categorias_ruins.png", scale=2, width=800, height=500)
```

### Anti-Patterns to Avoid

- **Plotting 100k individual points in scatter:** Use `alpha=0.05` and `s=5`, or aggregate to decile bins before scatter. Never `plt.scatter(df.dias_atraso, df.review_score)` unsampled — browser/notebook hangs.
- **Full 27x27 UF heatmap without filtering:** Every cell becomes unreadable. Filter to top-10 or top-15 origins.
- **Choropleth showing raw count instead of rate:** States with more orders (SP, MG) will dominate by count even if their rate is average. Normalize to `bad_review_rate = bad_reviews / total_orders`.
- **`plt.show()` in Streamlit:** Does not render. Use `st.plotly_chart(fig)` for plotly or `st.pyplot(fig)` for matplotlib/seaborn — explicit figure reference required.
- **Hardcoded absolute paths:** Use `pathlib.Path(__file__).parent / "../../data/gold/olist_gold.parquet"` or a shared `config.py` constant.
- **Saving to PNG without `bbox_inches='tight'`:** Axis labels and titles get clipped. Always use `fig.savefig(..., bbox_inches='tight')`.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Statistical significance for two groups | Custom t-test or manual U-statistic | `scipy.stats.mannwhitneyu` | Handles ties, non-normal data, correct one/two-tailed API |
| Brazil state polygons | Manual coordinate lists | IBGE GeoJSON via geopandas | IBGE is the authoritative source; manual coords will have CRS/projection errors |
| PNG export from plotly | `html2image`, `pyppeteer` | `kaleido` via `fig.write_image()` | kaleido is the official plotly static export engine — zero config |
| Color scales for diverging data | Custom RGB lists | `seaborn`/matplotlib named palettes (`RdYlGn`, `RdYlGn_r`, `YlOrRd`) | Perceptually uniform, accessible, recognized by mixed audience |
| 27x27 pivot table | Nested loops | `pd.pivot_table(values=..., index=..., columns=..., aggfunc='mean')` | Single line, handles missing corridors with NaN automatically |

**Key insight:** Every "custom" visualization solution in this phase adds hours of debugging with no audience benefit. Seaborn boxplots and folium choropleths are instantly legible to a mixed audience because they match audience expectations from news and business reports.

---

## Common Pitfalls

### Pitfall 1: dias_atraso Column Not in Gold Table

**What goes wrong:** Phase 2 (Data Foundation) delivers `olist_gold.parquet` but may not include `dias_atraso` as a pre-computed column. If the gold table only has `order_estimated_delivery_date` and `order_delivered_customer_date`, EDA-01 requires deriving it.
**Why it happens:** Phase 2 scope focused on joins and validation, not derived EDA columns.
**How to avoid:** Derive `dias_atraso` at the top of the EDA notebook: `(order_delivered_customer_date - order_estimated_delivery_date).dt.days`. Verify the range is sensible (-30 to +60 days for most orders).
**Warning signs:** Column missing from `df.columns`; values in degrees instead of days (wrong subtraction unit).

### Pitfall 2: GeoJSON Field Name Mismatch

**What goes wrong:** The folium `key_on` parameter references the wrong GeoJSON feature property. If the IBGE file uses `sigla` but you write `key_on="feature.properties.UF"`, the choropleth renders with all states grey (no matches).
**Why it happens:** Different GeoJSON sources use different field names for the state abbreviation.
**How to avoid:** After loading: `print(br_states.columns.tolist())` and `print(br_states.iloc[0])` to verify the field name before building the choropleth. Common alternatives: `sigla`, `abbrev_state`, `UF`, `CD_UF`.
**Warning signs:** All states show the same color (usually grey/null) in the choropleth output.

### Pitfall 3: Overplotting in Scatter Charts Masks the Signal

**What goes wrong:** `plt.scatter(df.dias_atraso, df.review_score)` on 100k rows produces a solid black blob. The negative correlation is invisible.
**Why it happens:** Default scatter has `alpha=1.0` and large markers.
**How to avoid:** Use `alpha=0.03`, `s=3`, and optionally jitter the y-axis (discrete 1-5 scores). Better: use seaborn `stripplot` with `jitter=True` or plotly violin instead of raw scatter.
**Warning signs:** Chart looks like a filled rectangle with no visible structure.

### Pitfall 4: Choropleth Counts vs. Rates

**What goes wrong:** Map shows Sao Paulo with the darkest red (most bad reviews by count) when its rate is similar to smaller states. Leadership asks "why is SP so dark — we sell a lot there?"
**Why it happens:** Choropleth is built on raw `bad_reviews` count instead of `bad_review_rate`.
**How to avoid:** Always normalize: `bad_review_rate = bad_reviews / total_orders`. Show rate in the choropleth; optionally add a second figure with absolute counts for context.

### Pitfall 5: PNG Export at Low DPI Looks Blurry in Slides

**What goes wrong:** Default matplotlib DPI is 72-100. On a 4K presentation screen or when printed, figures look pixelated.
**Why it happens:** `fig.savefig("fig.png")` uses default DPI.
**How to avoid:** Always `fig.savefig(..., dpi=150, bbox_inches='tight')` for seaborn/matplotlib. For plotly: `fig.write_image(..., scale=2, width=1000, height=600)` (scale=2 doubles resolution). Minimum 150 DPI for slides.

### Pitfall 6: `frete_pct_pedido` Division by Zero

**What goes wrong:** If `price == 0` for any order (free products, gifts), `price + freight_value` can be zero, producing `inf` or `NaN` in the derived column.
**Why it happens:** Gold table includes orders with zero-priced items.
**How to avoid:** `df["frete_pct_pedido"] = df["freight_value"] / (df["price"] + df["freight_value"]).replace(0, float("nan"))` — or filter out zero-price orders before this computation and document the exclusion.

---

## Code Examples

### Mann-Whitney U — Correct Usage

```python
# Source: scipy.stats official docs (https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html)
from scipy import stats

# alternative='greater': test that bad_review group has GREATER delay than good_review group
stat, p = stats.mannwhitneyu(
    df.loc[df["bad_review"] == 1, "dias_atraso"].dropna(),
    df.loc[df["bad_review"] == 0, "dias_atraso"].dropna(),
    alternative="greater",
)
# Report: U={stat:.0f}, p={p:.2e}
# Reject H0 (equal distributions) if p < 0.05
```

### Seaborn Figure with Slide-Ready Export

```python
# Source: matplotlib 3.9.x docs (https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html)
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", context="talk")  # 'talk' context = larger fonts for slides

fig, ax = plt.subplots(figsize=(10, 6))
# ... chart code ...
ax.set_title("Chart Title", fontsize=16, fontweight="bold")
ax.set_xlabel("X Label", fontsize=13)
ax.set_ylabel("Y Label", fontsize=13)
fig.tight_layout()
fig.savefig("reports/figures/chart_name.png", dpi=150, bbox_inches="tight")
plt.close(fig)  # Free memory — important in notebooks processing many charts
```

### Plotly Static Export (kaleido required)

```python
# Source: plotly 6.x docs (https://plotly.com/python/static-image-export/)
# pip install kaleido
import plotly.express as px

fig = px.box(df, x="review_score", y="dias_atraso", ...)
fig.write_image(
    "reports/figures/chart_name.png",
    format="png",
    scale=2,        # 2x resolution for slides
    width=900,
    height=550,
)
```

### geo_aggregated.parquet Schema

```python
# Output contract for EDA-03 — consumed by Phase 5 Streamlit map
geo_agg = df.groupby("customer_state").agg(
    total_orders=("order_id", "count"),
    bad_reviews=("bad_review", "sum"),
    avg_dias_atraso=("dias_atraso", "mean"),
    avg_freight_value=("freight_value", "mean"),
).assign(
    bad_review_rate=lambda x: x["bad_reviews"] / x["total_orders"]
).reset_index()

# customer_state: 2-letter UF code (SP, RJ, MG, ...)
# total_orders: int
# bad_reviews: int
# avg_dias_atraso: float (days, positive=late)
# avg_freight_value: float (BRL)
# bad_review_rate: float (0.0 to 1.0)

geo_agg.to_parquet("data/processed/geo_aggregated.parquet", index=False)
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| matplotlib choropleth (basemap) | geopandas + folium choropleth | ~2020 (basemap deprecated) | folium is maintained, interactive, embeds in HTML/Streamlit |
| seaborn 0.12 FacetGrid for comparisons | seaborn 0.13 `sns.set_theme()` + `Axes`-level API | v0.13 (2023) | Simpler API, `context='talk'` for slide-sized fonts |
| plotly static export via orca | kaleido | plotly 4.9+ | kaleido is the official replacement; orca is deprecated |
| Manual Haversine formula | `haversine` library | Ongoing | Library is vectorized and tested; manual formula has sin/cos bugs |

**Deprecated/outdated:**
- `basemap` (matplotlib): deprecated, replaced by geopandas + folium/cartopy
- `orca` (plotly static export): deprecated, replaced by kaleido
- `plt.show()` in Streamlit: does not render — use `st.pyplot(fig)` with explicit figure

---

## Open Questions

1. **`dias_atraso` column availability in gold table**
   - What we know: Phase 2 (Data Foundation) computes join columns; whether `dias_atraso` is pre-derived or requires derivation in EDA is unspecified.
   - What's unclear: Does `olist_gold.parquet` already include `dias_atraso` or only the raw date columns?
   - Recommendation: Derive it in the EDA notebook defensively (`df["dias_atraso"] = ...`) even if it already exists — idempotent and safe.

2. **IBGE GeoJSON field name at runtime**
   - What we know: The standard GitHub-hosted GeoJSON for Brazil states uses `sigla`; IBGE's own downloads use different schemas.
   - What's unclear: Which source the team downloads; field name only confirmed at load time.
   - Recommendation: Print `br_states.columns` and `br_states.head(1)` immediately after loading; adjust `key_on` in folium based on actual field name.

3. **Folium choropleth → PNG export method**
   - What we know: Folium saves `.html` natively; `write_image` is not available on folium maps.
   - What's unclear: Whether the team will use selenium/playwright for screenshot or fall back to a static plotly choropleth for the PNG slide export.
   - Recommendation: Use plotly express as a static PNG fallback (`px.choropleth` with the GeoJSON) and keep folium for the interactive Streamlit map. Both serve their purpose.

4. **`product_category_name_english` availability in gold table**
   - What we know: The Olist dataset includes a `product_category_name_translation.csv` that maps Portuguese to English category names. Phase 2 should have joined this.
   - What's unclear: Whether the join was included in Phase 2's gold table contract.
   - Recommendation: Check `df.columns` for `product_category_name_english`. If missing, the EDA notebook can do a quick merge from `data/raw/product_category_name_translation.csv` at the top of the EDA-04 analysis.

---

## Sources

### Primary (HIGH confidence)
- scipy.stats official docs — `mannwhitneyu` API and `alternative` parameter: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html
- seaborn 0.13.2 official docs — `boxplot`, `set_theme`, `context='talk'`: https://seaborn.pydata.org/
- matplotlib 3.9.x official docs — `savefig`, DPI, `bbox_inches`: https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html
- plotly official docs — static image export with kaleido: https://plotly.com/python/static-image-export/
- geopandas 1.1.2 official docs — GeoJSON loading, spatial operations: https://geopandas.org/en/stable/
- folium 0.20.0 official docs — Choropleth, key_on parameter: https://python-visualization.github.io/folium/
- pandas 2.3.3 official docs — `pivot_table`, `groupby`: https://pandas.pydata.org/docs/

### Secondary (MEDIUM confidence)
- IBGE GeoJSON for Brazil states — GitHub community mirror (brazil-states.geojson): `codeforamerica/click_that_hood` — multiple Olist practitioners use this source
- Olist Kaggle community analyses — confirmed `customer_state` field uses 2-letter UF codes matching IBGE `sigla` field
- Towards Data Science Olist case study (Jan 2025) — confirmed scatter overplotting pitfall and choropleth rate vs count distinction

### Tertiary (LOW confidence — validate at runtime)
- IBGE GeoJSON `sigla` field name — confirmed in community sources but must be verified when loading the specific file version
- `dias_atraso` pre-computed vs derived status in gold table — depends on Phase 2 implementation

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all library versions verified via project STACK.md (cross-referenced PyPI 2026-03-01); official docs confirm APIs
- Architecture: HIGH — notebook naming convention, folder structure, and output contracts defined in Phase 1 CONTEXT.md
- Pitfalls: HIGH (overplotting, DPI export, rate vs count choropleth) — verified across multiple Olist practitioner sources; MEDIUM (GeoJSON field name) — depends on source chosen at runtime
- Code examples: MEDIUM — patterns correct per official docs but `dias_atraso` derivation and GeoJSON field name require runtime validation

**Research date:** 2026-03-01
**Valid until:** 2026-04-01 (stable libraries; seaborn/folium APIs do not change frequently)
