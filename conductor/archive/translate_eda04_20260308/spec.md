# Specification: Translate EDA-04 Product Names to Portuguese

**Overview**
Modify the visualization in table "EDA-04" within the `notebooks/FASE3-P3-eda-metricas.ipynb` notebook. The current implementation uses English product category names (`product_category_name_english`). The objective is to display these names in Portuguese.

**Functional Requirements**
1. Identify the data aggregation logic for "EDA-04" in `notebooks/FASE3-P3-eda-metricas.ipynb`.
2. Ensure the Portuguese product category names (`product_category_name`) are available in the dataframe used for plotting.
3. Update the plotting code to use `product_category_name` instead of `product_category_name_english`.
4. Update the plot labels and titles if necessary to maintain consistency (e.g., y-axis label).
5. Verify the generated PNG `reports/figures/eda04_categorias_ruins.png` reflects the change.

**Non-Functional Requirements**
- Maintain the existing visual style (colors, annotations, horizontal bars).
- Ensure the notebook remains runnable without errors.

**Acceptance Criteria**
- Table "EDA-04" in the notebook shows product categories in Portuguese.
- The exported figure `eda04_categorias_ruins.png` displays categories in Portuguese.
- No other charts in the notebook are unintentionally changed.

**Out of Scope**
- Translating other notebooks.
- Modifying the global "gold" dataset.
