#!/usr/bin/env python3
"""
AIMRA Deep Verification Script
================================
Manually recomputes every calculated value in both output files and
compares them against what the scripts produced.
Also cross-checks the two scripts for consistency.
"""

import math

# ============================================================
# INPUT DATA (from metric_input_data.csv)
# ============================================================
# Columns: system, jurisdiction, case_type, rli_days, rli_norm, cdr, rlr, rlr_norm, rcs, aai, g_linear, g_geometric, data_confidence, notes
ROWS = [
    {
        "system": "South Africa",
        "rli_days": 187, "rli_norm_orig": 0.49,
        "cdr": 0.31,
        "rlr": 0.31, "rlr_norm_orig": 0.69,
        "rcs": 0.48, "aai": 0.22,
        "g_linear_reported": 0.44, "g_geometric_reported": 0.41,
    },
    {
        "system": "South Africa post-AIMRA",
        "rli_days": 52, "rli_norm_orig": 0.86,
        "cdr": 0.68,
        "rlr": 0.09, "rlr_norm_orig": 0.91,
        "rcs": 0.81, "aai": 0.79,
        "g_linear_reported": 0.81, "g_geometric_reported": 0.80,
    },
    {
        "system": "Agbabu baseline",
        "rli_days": 241, "rli_norm_orig": 0.34,
        "cdr": 0.18,
        "rlr": 0.47, "rlr_norm_orig": 0.53,
        "rcs": 0.31, "aai": 0.14,
        "g_linear_reported": 0.30, "g_geometric_reported": 0.27,
    },
    {
        "system": "Agbabu post-AIMRA",
        "rli_days": 67, "rli_norm_orig": 0.82,
        "cdr": 0.56,
        "rlr": 0.15, "rlr_norm_orig": 0.85,
        "rcs": 0.69, "aai": 0.73,
        "g_linear_reported": 0.73, "g_geometric_reported": 0.72,
    },
    {
        "system": "Athabasca baseline",
        "rli_days": None, "rli_norm_orig": 0.91,
        "cdr": 0.82,
        "rlr": 0.07, "rlr_norm_orig": 0.93,
        "rcs": 0.88, "aai": 0.79,
        "g_linear_reported": 0.87, "g_geometric_reported": None,  # blank in input
    },
    {
        "system": "Orinoco baseline",
        "rli_days": None, "rli_norm_orig": 0.41,
        "cdr": 0.24,
        "rlr": 0.62, "rlr_norm_orig": 0.38,
        "rcs": 0.22, "aai": 0.11,
        "g_linear_reported": 0.27, "g_geometric_reported": None,  # blank in input
    },
    {
        "system": "Utah baseline",
        "rli_days": None, "rli_norm_orig": 0.73,
        "cdr": 0.48,
        "rlr": 0.31, "rlr_norm_orig": 0.69,
        "rcs": 0.61, "aai": 0.38,
        "g_linear_reported": 0.58, "g_geometric_reported": None,  # blank in input
    },
]

# ============================================================
# Expected values from aimra_g_recalculated.csv
# ============================================================
EXPECTED_RECALCULATED = [
    {"system": "South Africa",          "computed_rli_norm": 0.4877, "computed_rlr_norm": 0.6900, "computed_g_linear": 0.4375, "computed_g_geometric": 0.4059},
    {"system": "South Africa post-AIMRA","computed_rli_norm": 0.8575, "computed_rlr_norm": 0.9100, "computed_g_linear": 0.8095, "computed_g_geometric": 0.8057},
    {"system": "Agbabu baseline",        "computed_rli_norm": 0.3397, "computed_rlr_norm": 0.5300, "computed_g_linear": 0.2999, "computed_g_geometric": 0.2689},
    {"system": "Agbabu post-AIMRA",      "computed_rli_norm": 0.8164, "computed_rlr_norm": 0.8500, "computed_g_linear": 0.7293, "computed_g_geometric": 0.7217},
    {"system": "Athabasca baseline",     "computed_rli_norm": 0.9100, "computed_rlr_norm": 0.9300, "computed_g_linear": 0.8660, "computed_g_geometric": 0.8643},
    {"system": "Orinoco baseline",       "computed_rli_norm": 0.4100, "computed_rlr_norm": 0.3800, "computed_g_linear": 0.2720, "computed_g_geometric": 0.2462},
    {"system": "Utah baseline",          "computed_rli_norm": 0.7300, "computed_rlr_norm": 0.6900, "computed_g_linear": 0.5780, "computed_g_geometric": 0.5620},
]

# Expected values from geometric_robustness_results.csv (uses ORIGINAL rli_norm / rlr_norm)
EXPECTED_ROBUSTNESS = [
    {"system": "South Africa",          "g_geometric_recomputed": 0.4063},
    {"system": "South Africa post-AIMRA","g_geometric_recomputed": 0.8062},
    {"system": "Agbabu baseline",        "g_geometric_recomputed": 0.2690},
    {"system": "Agbabu post-AIMRA",      "g_geometric_recomputed": 0.7223},
    {"system": "Athabasca baseline",     "g_geometric_recomputed": 0.8643},
    {"system": "Orinoco baseline",       "g_geometric_recomputed": 0.2462},
    {"system": "Utah baseline",          "g_geometric_recomputed": 0.5620},
]


# ============================================================
# Helper functions (mirrors the scripts exactly)
# ============================================================
def normalise_rli(rli_days):
    if rli_days is None:
        return None
    return round(1 - min(rli_days / 365, 1), 4)

def normalise_rlr(rlr):
    if rlr is None:
        return None
    return round(1 - min(rlr, 1), 4)

def linear_g(values):
    return round(sum(values) / len(values), 4)

def geometric_g(values):
    product = 1.0
    for v in values:
        product *= v
    return round(product ** (1 / len(values)), 4)

def geometric_g_math_prod(values):
    """Using math.prod, as robustness script does."""
    return round(math.prod(values) ** (1 / 5), 4)


# ============================================================
# VERIFICATION
# ============================================================
PASS = "[PASS]"
FAIL = "[FAIL]"
SEP = "=" * 72

issues = []

print(SEP)
print("AIMRA COMPREHENSIVE VERIFICATION REPORT")
print(SEP)

print("\n--- SCRIPT 1: compute_aimra_g.py (uses RECOMPUTED normalised values) ---\n")

for i, row in enumerate(ROWS):
    sys_name = row["system"]
    exp = EXPECTED_RECALCULATED[i]
    print(f"[{sys_name}]")

    # --- RLI_norm ---
    if row["rli_days"] is not None:
        my_rli = normalise_rli(row["rli_days"])
    else:
        my_rli = row["rli_norm_orig"]  # fallback to original
    match = abs(my_rli - exp["computed_rli_norm"]) < 0.00005
    status = PASS if match else FAIL
    print(f"  computed_rli_norm : {my_rli:.4f}  (expected {exp['computed_rli_norm']:.4f})  {status}")
    if not match:
        issues.append(f"{sys_name}: computed_rli_norm mismatch: got {my_rli:.4f}, expected {exp['computed_rli_norm']:.4f}")

    # --- RLR_norm ---
    if row["rlr"] is not None:
        my_rlr = normalise_rlr(row["rlr"])
    else:
        my_rlr = row["rlr_norm_orig"]
    match = abs(my_rlr - exp["computed_rlr_norm"]) < 0.00005
    status = PASS if match else FAIL
    print(f"  computed_rlr_norm : {my_rlr:.4f}  (expected {exp['computed_rlr_norm']:.4f})  {status}")
    if not match:
        issues.append(f"{sys_name}: computed_rlr_norm mismatch: got {my_rlr:.4f}, expected {exp['computed_rlr_norm']:.4f}")

    # --- Linear G (using recomputed rli/rlr) ---
    metrics = [my_rli, row["cdr"], my_rlr, row["rcs"], row["aai"]]
    my_g_lin = linear_g(metrics)
    match = abs(my_g_lin - exp["computed_g_linear"]) < 0.00005
    status = PASS if match else FAIL
    print(f"  computed_g_linear : {my_g_lin:.4f}  (expected {exp['computed_g_linear']:.4f})  {status}")
    if not match:
        issues.append(f"{sys_name}: computed_g_linear mismatch: got {my_g_lin:.4f}, expected {exp['computed_g_linear']:.4f}")

    # --- Geometric G (using recomputed rli/rlr) ---
    my_g_geo = geometric_g(metrics)
    match = abs(my_g_geo - exp["computed_g_geometric"]) < 0.00005
    status = PASS if match else FAIL
    print(f"  computed_g_geometric: {my_g_geo:.4f}  (expected {exp['computed_g_geometric']:.4f})  {status}")
    if not match:
        issues.append(f"{sys_name}: computed_g_geometric mismatch: got {my_g_geo:.4f}, expected {exp['computed_g_geometric']:.4f}")

    print()


print("\n--- SCRIPT 2: robustness_geometric_mean.py (uses ORIGINAL rli_norm / rlr_norm) ---\n")

for i, row in enumerate(ROWS):
    sys_name = row["system"]
    exp = EXPECTED_ROBUSTNESS[i]
    print(f"[{sys_name}]")

    # This script reads rli_norm and rlr_norm directly from CSV (original values)
    orig_metrics = [row["rli_norm_orig"], row["cdr"], row["rlr_norm_orig"], row["rcs"], row["aai"]]
    my_g_geo2 = geometric_g_math_prod(orig_metrics)
    match = abs(my_g_geo2 - exp["g_geometric_recomputed"]) < 0.00005
    status = PASS if match else FAIL
    print(f"  g_geometric_recomputed: {my_g_geo2:.4f}  (expected {exp['g_geometric_recomputed']:.4f})  {status}")
    if not match:
        issues.append(f"{sys_name} [robustness]: g_geometric_recomputed mismatch: got {my_g_geo2:.4f}, expected {exp['g_geometric_recomputed']:.4f}")
    print()


# ============================================================
# CROSS-CHECK: Do the two scripts agree on geometry?
# ============================================================
print("\n--- CROSS-CHECK: Script 1 vs Script 2 geometric values ---\n")
print("(Script 1 uses recomputed normalised values; Script 2 uses original normalised values)")
print(f"{'System':<30} {'S1 geo (recomputed)':<22} {'S2 geo (original)':<22} {'Match?'}")
print("-" * 85)
for i, row in enumerate(ROWS):
    sys_name = row["system"]
    if row["rli_days"] is not None:
        my_rli = normalise_rli(row["rli_days"])
        my_rlr = normalise_rlr(row["rlr"])
    else:
        my_rli = row["rli_norm_orig"]
        my_rlr = row["rlr_norm_orig"]
    s1 = geometric_g([my_rli, row["cdr"], my_rlr, row["rcs"], row["aai"]])
    s2 = geometric_g_math_prod([row["rli_norm_orig"], row["cdr"], row["rlr_norm_orig"], row["rcs"], row["aai"]])
    match = abs(s1 - s2) < 0.01
    note = "~agree" if match else "DIFFER"
    print(f"{sys_name:<30} {s1:<22.4f} {s2:<22.4f} {note}")


# ============================================================
# EDGE-CASE CHECKS
# ============================================================
print(f"\n\n--- EDGE-CASE AND ROBUSTNESS CHECKS ---\n")

# 1. normalise_rli bounds
assert normalise_rli(0) == 1.0,       "RLI of 0 days should give 1.0"
assert normalise_rli(365) == 0.0,     "RLI of exactly 365 days should give 0.0"
assert normalise_rli(730) == 0.0,     "RLI > 365 should be clamped to 0.0"
print(f"  RLI normalisation boundary clamp:  {PASS}")

# 2. normalise_rlr bounds
assert normalise_rlr(0.0) == 1.0,    "RLR of 0 should give 1.0"
assert normalise_rlr(1.0) == 0.0,    "RLR of 1 should give 0.0"
assert normalise_rlr(1.5) == 0.0,    "RLR > 1 should be clamped to 0.0"
print(f"  RLR normalisation boundary clamp:  {PASS}")

# 3. geometric mean with zero value
zero_vals = [0.5, 0.5, 0.0, 0.5, 0.5]
g_zero = geometric_g(zero_vals)
assert g_zero == 0.0, f"Geometric mean with a zero should be 0.0, got {g_zero}"
print(f"  Geometric mean with zero element:  {PASS} (result = {g_zero:.4f})")

# 4. Confirm the two scripts use different normalization inputs for rows with rli_days
print(f"\n  Key observation:")
for row in ROWS:
    if row["rli_days"] is not None:
        recomp = normalise_rli(row["rli_days"])
        orig   = row["rli_norm_orig"]
        diff   = abs(recomp - orig)
        note   = "DIFFERS" if diff > 0.0001 else "same"
        print(f"    {row['system']}: rli_norm original={orig}, recomputed={recomp} -> {note}")

print(f"\n  NOTE: robustness_geometric_mean.py uses original rli_norm/rlr_norm from CSV,")
print(f"      while compute_aimra_g.py recomputes them from rli_days and rlr.")
print(f"      This is by design but means the two scripts report slightly different geometric means.")


# ============================================================
# FINAL SUMMARY
# ============================================================
print(f"\n{SEP}")
print("FINAL SUMMARY")
print(SEP)
if issues:
    print(f"\n[ISSUES FOUND] {len(issues)} issue(s):\n")
    for issue in issues:
        print(f"  - {issue}")
else:
    print(f"\n[ALL PASS] All {len(ROWS) * 4 + len(ROWS)} computed values verified successfully.")
    print(f"  Both scripts produce mathematically correct results.")
    print(f"  Edge-case boundary conditions are properly handled.")
print()
