# AIMRA Manuscript & Supplementary Reconciliation Report

## Reference: Authoritative Script Outputs

The verified code (`compute_aimra_g.py`) produces these authoritative values
from the raw inputs in `metric_input_data.csv`:

| System | rli_norm (recomp) | rlr_norm (recomp) | G_linear | G_geometric |
|---|---|---|---|---|
| South Africa (baseline) | **0.4877** | **0.6900** | **0.4375** | **0.4059** |
| South Africa post-AIMRA | **0.8575** | **0.9100** | **0.8095** | **0.8057** |
| Agbabu baseline | **0.3397** | **0.5300** | **0.2999** | **0.2689** |
| Agbabu post-AIMRA | **0.8164** | **0.8500** | **0.7293** | **0.7217** |
| Athabasca baseline | 0.9100 | 0.9300 | 0.8660 | 0.8643 |
| Orinoco baseline | 0.4100 | 0.3800 | 0.2720 | 0.2462 |
| Utah baseline | 0.7300 | 0.6900 | 0.5780 | 0.5620 |

> [!NOTE]
> The manuscript and supplementary materials use **rounded** input values directly (e.g., `rli_norm = 0.49` stored in CSV) rather than recomputed values (0.4877). This is an accepted approximation, but creates minor discrepancies in G scores. All discrepancies are flagged below.

---

## MANUSCRIPT (`AIMRA_26052026.docx`)

### ISSUE M-1 — South Africa: G_linear computation uses rounded RLI_norm

**Location:** Section 6.4 — paragraph reading:
> "G_base = 0.20 × (0.49 + 0.31 + 0.69 + 0.48 + 0.22) = **0.44**"

**What it says:** Uses `rli_norm = 0.49` and reports G = 0.44  
**Code output (authoritative):** recomputed `rli_norm = 0.4877`, giving `G = 0.4375`

**Status:** ⚠️ MINOR INCONSISTENCY  
The value 0.44 is correct **if** using the rounded stored value (0.49). The script produces **0.4375 ≈ 0.44** — so the rounded result reported (0.44) agrees with 2 d.p. precision. **No correction needed** at 2 d.p., but the underlying `rli_norm` should be stated as **0.49** (the stored approximation), not 0.4877, when citing the in-text formula.

---

### ISSUE M-2 — South Africa: G_proj computation and improvement percentage (body text)

**Location:** Section 6.4 — paragraph reading:
> "G_proj = 0.20 × (0.86 + 0.68 + 0.91 + 0.81 + 0.79) = **0.81**. The proportional improvement is ΔG ≈ **84%**."

**What it says:** G_proj = 0.81, improvement = 84%  
**Code output:** G_proj = **0.8095 ≈ 0.81** ✅ — correct at 2 d.p.  
**Improvement check (using rounded G values):** (0.81 − 0.44) / 0.44 × 100 = **84.1% ≈ 84%** ✅  
**Improvement check (using exact G values):** (0.8095 − 0.4375) / 0.4375 × 100 = **85.0%**

**Status:** ✅ ACCEPTABLE at 2 d.p. using rounded G values as the computational basis.

> [!NOTE]
> The exact improvement is 85.0%, but the body text computes it from the rounded G values (0.81 and 0.44), which gives 84.1% → 84%. The sensitivity table (M-3) and the supplementary (SUPP-1) should use the more precise figure of +85%. See M-3 for the required correction.

---

### ISSUE M-3 — Sensitivity Analysis Table (South Africa, Config 1)

**Location:** Sensitivity analysis table — Config 1 row:
> Equal weights: G_base = **0.44**, G_proj = **0.81**, improvement = **+84%**

**Code output:** G_base = 0.4375, G_proj = 0.8095, improvement = +85.0%

**Status:** ⚠️ ROUNDING DISCREPANCY — improvement is **+85%**, not +84%.

> **Correction to apply:**  
> Change "+84%" → **"+85%"** in the sensitivity table Config 1 row (South Africa equal weights).

Note: The supplementary (Table S6) reports the same row as "+85%" — making the **supplementary correct** and the **manuscript wrong** here. See SUPP-1 below for cross-reference.

---

### ISSUE M-4 — Agbabu: Normalised RLI_norm stated as 0.34

**Location:** Worked example section — text:
> "RLI_norm = 1 − 241/365 = **0.34**"

**Code output:** `normalise_rli(241)` = 1 − 241/365 = **0.3397**

**Status:** ⚠️ ROUNDING — 0.34 is rounded to 2 d.p. from 0.3397. Acceptable as a presented value; CSV stores `rli_norm = 0.34` consistently. Both rounded and recomputed values give G_base = 0.30. **No correction needed.**

---

### ISSUE M-5 — Agbabu: G_proj computation and improvement

**Location:** Worked example — text:
> "G_proj = 0.20 × (0.82 + 0.56 + 0.85 + 0.69 + 0.73) = **0.73**. ΔG = (0.73 − 0.30)/0.30 × 100 = **+143%**"

**Code output:** G_proj = **0.7293**, improvement = **+143.2%**

**Status:** ✅ CORRECT — G = 0.73 and +143% are both verified.

---

### ISSUE M-6 — Agbabu: Geometric mean (G′) values

**Location:** Nonlinear robustness section — text:
> "G_baseline′ = (0.34 × 0.18 × 0.53 × 0.31 × 0.14)^(1/5) ≈ **0.27**"  
> "G_proj′ = (0.82 × 0.56 × 0.85 × 0.69 × 0.73)^(1/5) ≈ **0.72**"

**Code outputs:**
- Agbabu baseline G_geometric = **0.2689 ≈ 0.27** ✅
- Agbabu post-AIMRA G_geometric = **0.7217 ≈ 0.72** ✅

**Status:** ✅ CORRECT at the precision stated.

---

### ISSUE M-7 — Agbabu improvement using nonlinear G′ stated as "+167%"

**Location:** Nonlinear robustness section — text:
> "The nonlinear proportional improvement is approximately **+167%**"

**Verification:** (0.7217 − 0.2689) / 0.2689 × 100 = **+168.4%**  
Using stored-value G′: (0.7223 − 0.2690) / 0.2690 × 100 = **+168.5%**  
Both round to **+168%**, not +167%.

**Status:** ⚠️ DISCREPANCY

> **Correction to apply:**  
> Change "approximately **+167%**" → "approximately **+168%**"

---

### ISSUE M-8 — Sensitivity Analysis Table (South Africa, Config 3)

**Location:** Sensitivity analysis table — Config 3 (Accountability-focused) row:
> weights = [0.15, 0.15, 0.15, 0.20, 0.35], G_base = **0.40**, G_proj = **0.81**, improvement = **+102%**

**Verification:**  
G_base = 0.15×0.49 + 0.15×0.31 + 0.15×0.69 + 0.20×0.48 + 0.35×0.22 = **0.3965 → 0.40** ✅  
G_proj = 0.15×0.86 + 0.15×0.68 + 0.15×0.91 + 0.20×0.81 + 0.35×0.79 = **0.8060 → 0.81** ✅  
Improvement (exact): (0.8060 − 0.3965) / 0.3965 × 100 = **103.3% → +103%**  
Improvement (rounded G): (0.81 − 0.40) / 0.40 × 100 = **102.5% → +103%**

**Status:** ⚠️ MINOR ERROR — both calculation bases give **+103%**, not +102%.

> **Correction to apply:**  
> Change "+102%" → **"+103%"** in the sensitivity table Config 3 row (Accountability-focused).

---

### ISSUE M-9 — Equation 4 formula notation: α₃ term is RLInorm instead of RLRnorm

**Location:** Equation (4) — as typeset in the manuscript (line 214):
> G = α₁·**RLInorm** + α₂·CDR + α₃·**RLInorm** + α₄·RCS + α₅·AAI

**What it says:** `RLInorm` appears in **both** positions 1 and 3.  
**What it should say:** Position 1 = **RLInorm** ✅, Position 3 = **RLRnorm** (Resource Leakage Reduction, normalised)

All computations throughout the manuscript correctly use RLRnorm in position 3; only the typeset formula is wrong. This is a notation error in the formal definition of the central equation of the paper.

**Status:** ⚠️ NOTATION ERROR

> **Correction to apply:**  
> In Equation (4), change the α₃ term from **RLInorm** → **RLRnorm**.

---

## CSV DATA (`metric_input_data.csv`)

### ISSUE CSV-1 — South Africa post-AIMRA: `g_geometric` stored value

**Location:** `metric_input_data.csv` row 2 (South Africa post-AIMRA)
> Stored value for `g_geometric` = **0.80**

**Code output:** Both authoritative scripts produce geometric mean = **0.8057** (Script 1) and **0.8062** (Script 2). Both round to **0.81**.

**Status:** ⚠️ MINOR ERROR — Stored value in the CSV is incorrectly truncated.

> **Correction to apply:**  
> Update `metric_input_data.csv` row 2, `g_geometric` column: **0.80** → **0.81**

---

## SUPPLEMENTARY MATERIALS (`AIMRA_Supplementary_Materials_26052026.docx`)

### ISSUE SUPP-1 — South Africa Sensitivity Table (S6): Config 1 improvement

**Location:** Table S6.x, South Africa, Config 1:
> G_base = 0.44, G_proj = 0.81, improvement = **+85%**

**Code output:** improvement = **+85.0%** ✅

**Status:** ✅ CORRECT — Supplementary correctly says +85%; manuscript (M-3) incorrectly says +84%.

> **Cross-document inconsistency:** Manuscript: +84% | Supplementary: +85%. Supplementary is correct; manuscript needs updating per M-3.

---

### ISSUE SUPP-2 — Agbabu Sensitivity Table (S6): Config 1 improvement

**Location:** Table S6.x, Agbabu, Config 1:
> G_base = 0.30, G_proj = 0.73, improvement = **+143%**

**Code output:** +143.2% ≈ **+143%** ✅

**Status:** ✅ CORRECT.

---

### ISSUE SUPP-3 — S3 Mathematical Proofs: Agbabu G and G′ values

**Location:** S3.4 / S3.5:
> "Agbabu baseline G = **0.30**, G′ = **0.27**"

**Code output:** G = 0.2999 ≈ 0.30 ✅, G′ = 0.2689 ≈ 0.27 ✅

**Status:** ✅ CORRECT.

---

### ISSUE SUPP-4 — S4 Data Triangulation: Agbabu indicator values

**Location:** Table S4:
- CDR = 0.18 [0.14–0.22] ✅ | RLR = 0.47 [0.41–0.53] ✅ | RCS = 0.31 [0.26–0.36] ✅
- AAI = 0.14 [0.10–0.18] ✅ | AAI derivation: (0.15 + 0.13 + 0.13) / 3 = 0.137 → **0.14** ✅

**Status:** ✅ ALL CORRECT.

---

### ISSUE SUPP-5 — S6 Extended Sensitivity: Config 4 (Revenue-focused) for South Africa

**Location:** Table S6, South Africa, Config 4:
> weights = [0.10, 0.20, 0.40, 0.15, 0.15], G_base = **0.43**, G_proj = **0.83**, improvement = **+93%**

**Manual verification:**  
G_base = 0.10×0.49 + 0.20×0.31 + 0.40×0.69 + 0.15×0.48 + 0.15×0.22 = **0.4920 → 0.49**, NOT 0.43  
G_proj = 0.10×0.86 + 0.20×0.68 + 0.40×0.91 + 0.15×0.81 + 0.15×0.79 = **0.8260 → 0.83** ✅  
Improvement (exact): (0.8260 − 0.4920) / 0.4920 × 100 = **+67.9% → +68%**

**Status:** ❌ SIGNIFICANT ERROR — G_base and improvement are both wrong.

> **Correction to apply:**  
> G_base: **0.43** → **0.49**; improvement: **+93%** → **+68%**  
> *(Using rounded G values gives +69%; exact basis gives +68%. The exact basis is used here for consistency with other corrections.)*

> [!WARNING]
> This is the most significant numerical error found. Both G_base and the improvement percentage are incorrect.

---

### ISSUE SUPP-6 — S6 Extended Sensitivity: Config 5 (Latency-only extreme) for Agbabu

**Location:** Table S6, Agbabu, Config 5:
> weights = [0.60, 0.10, 0.10, 0.10, 0.10], G_base = **0.30**, G_proj = **0.74**, improvement = **+147%**

**Manual verification:**  
G_base = 0.60×0.34 + 0.10×0.18 + 0.10×0.53 + 0.10×0.31 + 0.10×0.14 = **0.320 → 0.32**, NOT 0.30  
G_proj = 0.60×0.82 + 0.10×0.56 + 0.10×0.85 + 0.10×0.69 + 0.10×0.73 = **0.775 → 0.78**, NOT 0.74  
Improvement: (0.775 − 0.320) / 0.320 × 100 = **+142%**, NOT +147%

**Status:** ❌ ERROR — All three values are incorrect.

> **Correction to apply:**  
> G_base: **0.30** → **0.32**; G_proj: **0.74** → **0.78**; improvement: **+147%** → **+142%**

---

### ISSUE SUPP-7 — S6 Extended Sensitivity: Config 6 (Accountability-only) for Agbabu

**Location:** Table S6, Agbabu, Config 6:
> weights = [0.10, 0.10, 0.10, 0.10, 0.60], G_base = **0.24**, G_proj = **0.73**, improvement = **+204%**

**Manual verification:**  
G_base = 0.10×0.34 + 0.10×0.18 + 0.10×0.53 + 0.10×0.31 + 0.60×0.14 = **0.220 → 0.22**, NOT 0.24  
G_proj = 0.10×0.82 + 0.10×0.56 + 0.10×0.85 + 0.10×0.69 + 0.60×0.73 = **0.730 → 0.73** ✅  
Improvement: (0.730 − 0.220) / 0.220 × 100 = **+232%**, NOT +204%

**Status:** ❌ ERROR — G_base and improvement are both incorrect.

> **Correction to apply:**  
> G_base: **0.24** → **0.22**; improvement: **+204%** → **+232%**

---

## REVISED REFERENCE MANUSCRIPT (`AIMRA_revised_reference_manuscript.docx`)

> [!NOTE]
> This document was not covered in earlier versions of this reconciliation report. It contains its own set of errors, some of which mirror issues in the original manuscript and some of which are distinct.

---

### ISSUE R-1 — Equation 4 formula notation: both α₁ and α₃ terms use undefined "RLMnorm"

**Location:** Equation (4) — inside the `<m:oMath>` block
> G = α₁·**RLMnorm** + α₂·CDR + α₃·**RLMnorm** + α₄·RCS + α₅·AAI

**What it says:** Uses the term `RLMnorm` in both positions 1 and 3. "RLM" is not defined anywhere in the paper.  
**What it should say:** Position 1 = **RLInorm** (Regulatory Latency Index, normalised); Position 3 = **RLRnorm** (Resource Leakage Reduction Index, normalised)

This is a more severe version of the corresponding error in the original manuscript (M-9): in the original, position 1 is correctly `RLInorm` but position 3 wrongly repeats it; here, both positions use the entirely undefined `RLMnorm`. All numerical computations are correct throughout the document; only the typeset formula is wrong.

**Status:** ⚠️ NOTATION ERROR (both positions)

> **Correction to apply:**  
> In Equation (4): α₁ term **RLMnorm** → **RLInorm**; α₃ term **RLMnorm** → **RLRnorm**

---

### ISSUE R-2 — Section 6.5 body text: SA equal-weight improvement stated as +84%

**Location:** Section 6.5, comparison sentence:
> "...compared to **+84%** for South Africa under equal-weight configuration from a higher starting point."

**Verified value:** SA equal-weight improvement = **85.0%** (exact) → **+85%**  
The revised manuscript's own Table 5 (Config 1) correctly states **+85%**, making this an internal inconsistency within the same document.

**Status:** ⚠️ MINOR ERROR — body text is inconsistent with its own table.

> **Correction to apply:**  
> Change "compared to **+84%**" → "compared to **+85%**"

---

### ISSUE R-3 — Table 5 (Sensitivity Analysis): Config 3 improvement stated as +102%

**Location:** Table 5, Config 3 (Accountability-focused) row:
> weights = [0.15, 0.15, 0.15, 0.20, 0.35], G_base = **0.40**, G_proj = **0.81**, improvement = **+102%**

**Verification:**  
Improvement (exact): (0.8060 − 0.3965) / 0.3965 × 100 = **103.3% → +103%**  
Improvement (rounded G): (0.81 − 0.40) / 0.40 × 100 = **102.5% → +103%**

Both methods give **+103%**. This is the same error as M-8 in the original manuscript.

**Status:** ⚠️ MINOR ERROR

> **Correction to apply:**  
> Change "+102%" → **"+103%"** in Table 5, Config 3.

---

### ISSUE R-4 — Section 6.4 introductory range statement: "+85% to +102%"

**Location:** Section 6.4, sentence preceding Table 5:
> "Improvements range from **+85% to +102%** across all three configurations..."

Since Config 3 is +103% (not +102%), this range is understated at the top end.

**Status:** ⚠️ MINOR ERROR — follows directly from R-3.

> **Correction to apply:**  
> Change "**+85% to +102%**" → "**+85% to +103%**"

---

### ISSUE R-5 — Section 6.6 (Nonlinear Robustness): SA post-AIMRA G′ stated as 0.80

**Location:** Section 6.6, nonlinear robustness paragraph:
> "South Africa: Baseline G′ = ... = **0.41**; Post-AIMRA G′ = ... = **0.80**; improvement: **+98%**."

**Verification:**  
SA G_geo_baseline = (0.49 × 0.31 × 0.69 × 0.48 × 0.22)^(1/5) = **0.4063 → 0.41** ✅  
SA G_geo_proj = (0.86 × 0.68 × 0.91 × 0.81 × 0.79)^(1/5) = **0.8062 → 0.81**, NOT 0.80  
Improvement = (0.8062 − 0.4063) / 0.4063 × 100 = **98.4% → +98%** ✅

The G_geo_proj value is incorrectly rounded (0.8062 truncated to 0.80 instead of rounded to 0.81). The improvement figure of +98% is correct regardless of this error. This is the same underlying value as CSV-1 but manifests here as an error in document text.

**Status:** ⚠️ MINOR ERROR — Post-AIMRA G′ should be 0.81; improvement +98% remains correct.

> **Correction to apply:**  
> Change Post-AIMRA G′ from **0.80** → **0.81** in the Section 6.6 nonlinear robustness text.

---

### ISSUE R-6 — Conclusion: SA sensitivity range stated as "+85% to +102%"

**Location:** Conclusion paragraph:
> "...projected G improvements of **+85% to +102%** for South Africa across three weight configurations..."

Since Config 3 is +103% (not +102%), this range is wrong at the top end. Follows directly from R-3 and R-4.

**Status:** ⚠️ MINOR ERROR

> **Correction to apply:**  
> Change "**+85% to +102%**" → "**+85% to +103%**"

---

## SUMMARY OF ALL CORRECTIONS REQUIRED

| ID | Document | Location | Current value | Correct value | Severity |
|---|---|---|---|---|---|
| M-3 | Manuscript | Sensitivity table, SA Config 1 improvement | +84% | **+85%** | Minor |
| M-7 | Manuscript | Agbabu G′ improvement statement | ≈+167% | **≈+168%** | Minor |
| M-8 | Manuscript | Sensitivity table, SA Config 3 improvement | +102% | **+103%** | Minor |
| M-9 | Manuscript | Equation (4), α₃ term | RLInorm | **RLRnorm** | Notation error |
| CSV-1 | CSV Data | `metric_input_data.csv` SA post-AIMRA `g_geometric` | 0.80 | **0.81** | Minor |
| SUPP-1 | (Cross-doc) | SA Config 1 improvement: manuscript vs supplementary | Manuscript: +84% | **+85%** (supplementary correct) | Minor |
| SUPP-5 | Supplementary | Table S6, SA Config 4 (Revenue-focused) G_base | 0.43 | **0.49** | **Major** |
| SUPP-5 | Supplementary | Table S6, SA Config 4 (Revenue-focused) improvement | +93% | **+68%** | **Major** |
| SUPP-6 | Supplementary | Table S6, Agbabu Config 5 (Latency-only) G_base | 0.30 | **0.32** | **Major** |
| SUPP-6 | Supplementary | Table S6, Agbabu Config 5 (Latency-only) G_proj | 0.74 | **0.78** | **Major** |
| SUPP-6 | Supplementary | Table S6, Agbabu Config 5 (Latency-only) improvement | +147% | **+142%** | **Major** |
| SUPP-7 | Supplementary | Table S6, Agbabu Config 6 (Accountability-only) G_base | 0.24 | **0.22** | **Major** |
| SUPP-7 | Supplementary | Table S6, Agbabu Config 6 (Accountability-only) improvement | +204% | **+232%** | **Major** |
| R-1 | Revised ref. MS | Equation (4), α₁ and α₃ terms | RLMnorm (both) | **RLInorm** (α₁) / **RLRnorm** (α₃) | Notation error |
| R-2 | Revised ref. MS | Section 6.5 body text — SA improvement | +84% | **+85%** | Minor |
| R-3 | Revised ref. MS | Table 5 Config 3 improvement | +102% | **+103%** | Minor |
| R-4 | Revised ref. MS | Section 6.4 sensitivity range statement | +85% to +102% | **+85% to +103%** | Minor |
| R-5 | Revised ref. MS | Section 6.6 SA post-AIMRA G′ | 0.80 | **0.81** | Minor |
| R-6 | Revised ref. MS | Conclusion — SA sensitivity range | +85% to +102% | **+85% to +103%** | Minor |

---

## Items Verified as Correct

The following were fully verified across all three documents and require no changes:

- All core indicator values (RLI, CDR, RLR, RCS, AAI) in both manuscripts ✅
- South Africa G_base = 0.44, G_proj = 0.81 ✅
- South Africa G_geo_base = 0.41 ✅
- South Africa post-AIMRA G_geo improvement = +98% ✅ (correct despite the G′ rounding error in R-5)
- Agbabu G_base = 0.30, G_proj = 0.73, improvement = +143% ✅
- Agbabu G′_base ≈ 0.27, G′_proj ≈ 0.72 ✅
- Agbabu G_geo improvement ≈ +168% (manuscript M-7 needs correction from +167%); revised MS +169% is CORRECT ✅
  - Exact value = 168.54%; rounds to +169% by standard (round-half-up) rounding, as used in revised MS
  - Original manuscript uses +167%, which is wrong by one integer — see M-7
- Sensitivity table Config 2 (Regulatory-focused): G_base = 0.43, G_proj = 0.80, improvement = +86% ✅
  - (Using rounded G values: (0.80 − 0.43)/0.43 = 86.0%; exact = 85.4%; both manuscripts use rounded-G basis here)
- All uncertainty ranges for Agbabu indicators (Table S4) ✅
- All equal-weight (Config 1) rows in supplementary Table S6 ✅
- All benchmarking G values for Athabasca (0.87), Orinoco (0.27), Utah (0.58) ✅
- Supplementary S3 mathematical proofs ✅
- Supplementary S1 PRISMA search numbers — not in scope

> [!IMPORTANT]
> Before correcting SUPP-5, SUPP-6, and SUPP-7, confirm which input values (stored CSV rounded values vs. recomputed normalised values) were **intended** as the basis for the sensitivity analysis. The above corrections use the **stored rounded values** (rli_norm = 0.34 for Agbabu, rli_norm = 0.49 for South Africa), which is consistent with how both manuscripts present the G formula. If recomputed values (0.3397, 0.4877) were intended, corrections still apply but exact figures change slightly.

> [!NOTE]
> **On the Config 2 improvement (+86%) convention:** The revised manuscript's Section 6.4 range statement says "+85% to +102%" treating Config 1 as +85% and Config 3 as +102%. Since Config 2 computes to either +85.4% (exact) or +86.0% (rounded-G basis), the "+86%" figure in the table is internally consistent with the rounded-G computation basis used for that row. Config 2 requires no correction; only Config 3 (+103% not +102%) and Config 1 (+85% not +84%) are affected.
