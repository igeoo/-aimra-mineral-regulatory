#!/usr/bin/env python3
"""Run the AIMRA nonlinear robustness calculation using geometric means."""
from __future__ import annotations

import csv
import math
from pathlib import Path

# Resolve paths relative to this script's location so the script
# can be run from any working directory.
_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent

INPUT = _ROOT / "data" / "processed" / "metric_input_data.csv"
OUTPUT = _ROOT / "outputs" / "geometric_robustness_results.csv"
METRICS = ["rli_norm", "cdr", "rlr_norm", "rcs", "aai"]


def fnum(x: str):
    x = (x or "").strip()
    return None if x == "" else float(x)


def main() -> None:
    rows_out = []
    with INPUT.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            vals = [fnum(row[m]) for m in METRICS]
            if any(v is None for v in vals):
                g_geo = ""
            else:
                product = math.prod(vals)  # type: ignore[arg-type]
                g_geo = f"{product ** (1/5):.4f}"
            rows_out.append({
                "system": row["system"],
                "jurisdiction": row["jurisdiction"],
                "g_linear_reported": row.get("g_linear", ""),
                "g_geometric_recomputed": g_geo,
                "data_confidence": row.get("data_confidence", ""),
            })
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        writer.writeheader()
        writer.writerows(rows_out)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
