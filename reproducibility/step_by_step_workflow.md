# Step-by-Step Reproducibility Workflow

1. Review `data/raw/AIMRA_corpus_access_data_workbook.xlsx` for source categories, access conditions, and annotation logic.
2. Review `data/processed/annotation_codebook.csv` for variable definitions and coding rules.
3. Review `data/processed/metric_input_data.csv` for the system-level input values used in the manuscript demonstration.
4. Run `python scripts/compute_aimra_g.py` to recalculate `RLI_norm`, `RLR_norm`, linear `G`, and geometric `G'`.
5. Run `python scripts/robustness_geometric_mean.py` to produce a compact nonlinear robustness table.
6. Compare generated outputs in `outputs/` with the values reported in the manuscript.
7. Use the data-access log to identify restricted institutional records required for Stage 2 empirical validation.
