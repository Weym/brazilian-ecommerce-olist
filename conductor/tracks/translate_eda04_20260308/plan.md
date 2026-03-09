# Implementation Plan: Translate EDA-04 Product Names

**Phase 1: Research and Preparation**
- [x] Task: Inspect `notebooks/FASE3-P3-eda-metricas.ipynb` to identify all cells requiring modification (aggregation and plotting).
- [x] Task: Verify that `product_category_name` is correctly loaded in the notebook's setup phase.
- [x] Task: Conductor - User Manual Verification 'Research and Preparation' (Protocol in workflow.md)

**Phase 2: Implementation**
- [ ] Task: Implement change: Grouping. Update cell 11 to group by `product_category_name`.
- [ ] Task: Implement change: Plotting. Update cell 11 (Matplotlib) and cell 12 (Plotly/Seaborn) to use `product_category_name` as labels.
- [ ] Task: Conductor - User Manual Verification 'Implementation' (Protocol in workflow.md)

**Phase 3: Validation and Completion**
- [ ] Task: Execution. Run the notebook `notebooks/FASE3-P3-eda-metricas.ipynb` to ensure it completes successfully and regenerates figures.
- [ ] Task: Visual Check. Verify `reports/figures/eda04_categorias_ruins.png` uses Portuguese names.
- [ ] Task: Conductor - User Manual Verification 'Validation and Completion' (Protocol in workflow.md)
