# Methodology Note

This package supports a Stage 1 Design Science Research demonstration of the African AI-Integrated Mineral Regulatory Architecture (AIMRA).

## Purpose

The repository documents how the manuscript operationalises AIMRA's governance-performance function, including the source categories, annotation variables, structured estimates, uncertainty ranges, and reproducible calculations used for South Africa, Agbabu tar sands in Nigeria, and global tar sand analogues.

## Calculation logic

1. Collect raw or estimated values for RLI, CDR, RLR, RCS, and AAI.
2. Normalise latency and resource-loss indicators to a [0,1] scale.
3. Preserve CDR, RCS, and AAI as bounded [0,1] indicators.
4. Compute equal-weight composite performance score `G`.
5. Compute geometric mean `G'` as a nonlinear robustness check.

## Interpretation

The repository does not claim that all values are measured field observations. It separates public data, structured estimates, restricted data pathways, and Stage 2 calibration requirements.
