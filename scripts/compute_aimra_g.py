#!/usr/bin/env python3
"""Compute AIMRA composite governance-performance scores.

This script recalculates normalised AIMRA indicators, the equal-weight linear
composite G, and the geometric-mean robustness score G'.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Dict, List

# Resolve the project root relative to this script so default paths work
# regardless of the working directory from which the script is invoked.
_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent

METRIC_COLUMNS = ["rli_norm", "cdr", "rlr_norm", "rcs", "aai"]


def to_float(value: str) -> float | None:
    value = (value or "").strip()
    if value == "":
        return None
    return float(value)


def normalise_rli(rli_days: float | None, current: float | None) -> float | None:
    if rli_days is None:
        return current
    return round(1 - min(rli_days / 365, 1), 4)


def normalise_rlr(rlr: float | None, current: float | None) -> float | None:
    if rlr is None:
        return current
    return round(1 - min(rlr, 1), 4)


def linear_g(values: List[float]) -> float:
    return round(sum(values) / len(values), 4)


def geometric_g(values: List[float]) -> float:
    product = 1.0
    for value in values:
        product *= value
    return round(product ** (1 / len(values)), 4)


def recalculate(input_csv: Path, output_csv: Path) -> None:
    with input_csv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows: List[Dict[str, str]] = list(reader)
        fieldnames = list(reader.fieldnames or [])

    for column in ["computed_rli_norm", "computed_rlr_norm", "computed_g_linear", "computed_g_geometric"]:
        if column not in fieldnames:
            fieldnames.append(column)

    for row in rows:
        rli_days = to_float(row.get("rli_days", ""))
        rlr = to_float(row.get("rlr", ""))
        rli_norm = normalise_rli(rli_days, to_float(row.get("rli_norm", "")))
        rlr_norm = normalise_rlr(rlr, to_float(row.get("rlr_norm", "")))
        row["computed_rli_norm"] = "" if rli_norm is None else f"{rli_norm:.4f}"
        row["computed_rlr_norm"] = "" if rlr_norm is None else f"{rlr_norm:.4f}"

        metric_values = []
        for col in METRIC_COLUMNS:
            if col == "rli_norm":
                value = rli_norm
            elif col == "rlr_norm":
                value = rlr_norm
            else:
                value = to_float(row.get(col, ""))
            if value is not None:
                metric_values.append(value)

        if len(metric_values) == len(METRIC_COLUMNS):
            row["computed_g_linear"] = f"{linear_g(metric_values):.4f}"
            row["computed_g_geometric"] = f"{geometric_g(metric_values):.4f}"
        else:
            row["computed_g_linear"] = ""
            row["computed_g_geometric"] = ""

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recalculate AIMRA governance-performance scores.")
    parser.add_argument(
        "--input",
        default=str(_ROOT / "data" / "processed" / "metric_input_data.csv"),
        help="Input CSV path",
    )
    parser.add_argument(
        "--output",
        default=str(_ROOT / "outputs" / "aimra_g_recalculated.csv"),
        help="Output CSV path",
    )
    args = parser.parse_args()
    recalculate(Path(args.input), Path(args.output))
    print(f"Wrote recalculated scores to {args.output}")
