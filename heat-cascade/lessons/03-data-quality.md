# 03. Cleaning measurements with a recorded audit

[Course home](../README.md) | **Indicative time:** 2 hours

**Research question:** Which records are usable, and how do cleaning decisions change the evidence base?

**Dataset boundary:** Every supplied observation and parameter is synthetic. The exercises teach analytical practice; their results do not establish Heat Cascade research findings.

## 1. Learning outcomes and vocabulary

- Normalise join keys and parse dates and numeric values.
- Distinguish duplicate records from repeated observations.
- Record missingness and preserve an audit trail.

| Term | Meaning in this workshop |
| --- | --- |
| `missing value` | A value that is absent or cannot be used; often shown as NaN. |
| `coercion` | Conversion of invalid text to a missing value. |
| `composite key` | Several columns that together identify one observation. |
| `audit trail` | A record of the rules applied and their consequences. |

## 2. Guided analysis

Read the purpose, paste one Python block into a new code cell, then run it with **Shift+Enter**. Compare the output before moving to the next step. Code cells within this lesson share variables and must run in order.

### 2.1. Find the course files

**Why this step matters:** Python needs the course folder before it can read data or save results. Run this cell at the start of every workshop, even in an existing notebook.

```python
from pathlib import Path
import sys

candidates = [Path.cwd(), Path.cwd() / "heat-cascade", Path.cwd().parent]
ROOT = next((p for p in candidates if (p / "data/raw/neighbourhoods.csv").is_file()), None)
if ROOT is None:
    raise FileNotFoundError("Open the notebook inside the fork's heat-cascade/notebooks or heat-cascade/student_work folder.")
sys.path.insert(0, str(ROOT))
DATA = ROOT / "data" / "raw"
OUTPUT = ROOT / "outputs"
OUTPUT.mkdir(exist_ok=True)
print("Course folder:", ROOT.name)
```

**Expected result:** `Course folder: heat-cascade`. If this fails, return to the folder check in Lesson 00.

**Read the result:** ROOT locates the course; DATA locates the untouched input tables; OUTPUT stores analysis products. The input tables are already present in the fork.

### 2.2. Read a fresh copy and inspect anomalies

**Why this step matters:** A fresh copy allows the cleaning decisions to be reproduced independently.

```python
import pandas as pd

raw = pd.read_csv(DATA / "monitoring.csv")
print("Raw rows:", len(raw))
print("Exact duplicate rows:", raw.duplicated().sum())
numeric_surface = pd.to_numeric(raw["surface_temp_c"], errors="coerce")
new_conversion_failures = raw["surface_temp_c"].notna() & numeric_surface.isna()
print("Non-blank conversion failures:", new_conversion_failures.sum())
print(raw.loc[new_conversion_failures, ["neighbourhood_id", "date", "surface_temp_c"]])
```

**Expected result:** 1,088 raw rows, eight exact duplicates and two non-blank conversion failures.

**Read the result:** An exact duplicate repeats a whole record. A different day in the same area is a legitimate repeated observation. Conversion failures must remain distinguishable from initially blank readings.

### 2.3. Normalise identifiers and parse values

**Why this step matters:** Consistent keys prevent missed joins, while explicit parsing supports numerical analysis.

```python
clean = raw.copy()
clean["neighbourhood_id"] = clean["neighbourhood_id"].str.strip().str.upper()
clean["date"] = pd.to_datetime(clean["date"], errors="coerce")
clean["surface_temp_c"] = pd.to_numeric(clean["surface_temp_c"], errors="coerce")
print("Invalid dates:", clean["date"].isna().sum())
print("Missing surface values after conversion:", clean["surface_temp_c"].isna().sum())
```

**Expected result:** Zero invalid dates; 12 missing surface readings after conversion.

**Read the result:** The conversion identifies unreadable values. It does not decide whether a readable value is plausible. Normalisation fixes three untidy identifiers; it does not merge different areas.

### 2.4. Apply documented teaching bounds

**Why this step matters:** Range rules identify deliberate errors, but the rules require justification when working with research observations.

```python
surface_invalid = clean["surface_temp_c"].notna() & ~clean["surface_temp_c"].between(-10, 65)
humidity_invalid = clean["relative_humidity_pct"].notna() & ~clean["relative_humidity_pct"].between(0, 100)
clean.loc[surface_invalid, "surface_temp_c"] = float("nan")
clean.loc[humidity_invalid, "relative_humidity_pct"] = float("nan")
clean = clean.drop_duplicates().sort_values(["date", "neighbourhood_id"]).reset_index(drop=True)
key_conflicts = clean.duplicated(["neighbourhood_id", "date"]).sum()
print("Clean rows:", len(clean))
print("Key conflicts:", key_conflicts)
print(clean[["surface_temp_c", "relative_humidity_pct"]].isna().sum())
```

**Expected result:** 1,080 clean rows; zero key conflicts; 13 missing surface readings and one missing humidity reading.

**Read the result:** The -10 to 65 C surface bounds are course rules, not universal sensor specifications. Conflicting records with the same area-date key need investigation; keeping an arbitrary row would hide the conflict.

### 2.5. Save the audit and clean table

**Why this step matters:** A defensible output states exactly which rules were used and how many measurements remain missing.

```python
audit = pd.DataFrame({
    "check": ["raw_rows", "exact_duplicates_removed", "nonblank_surface_conversion_failures",
              "surface_range_failures", "humidity_range_failures", "clean_rows", "surface_missing_after_cleaning"],
    "value": [len(raw), raw.duplicated().sum(), new_conversion_failures.sum(),
              surface_invalid.sum(), humidity_invalid.sum(), len(clean), clean["surface_temp_c"].isna().sum()],
})
clean.to_csv(OUTPUT / "03_monitoring_clean.csv", index=False)
audit.to_csv(OUTPUT / "03_quality_audit.csv", index=False)
print(audit.to_string(index=False))
```

**Expected result:** Two CSV files are saved. The audit records every expected count from the previous steps.

**Read the result:** Missing values remain missing. Replacing them with zero would imply a measured value. Model-specific imputation belongs inside a training pipeline, not in this descriptive cleaning stage.

## 3. Independent practice

Calculate the percentage of cleaned surface readings that are missing. Then explain why replacing every missing surface value with zero would distort a neighbourhood average.

<details>
<summary>Hint</summary>

Use `clean["surface_temp_c"].isna().mean() * 100`. A zero is a recorded numerical value, while NaN marks missingness.

</details>

## 4. Interpretation and checkpoint

Identify the raw, parsed and cleaned row counts. Explain why the 90 readings in one area are not 90 independent replications of that area. List one possible reason for missingness that would threaten a real heat analysis.

Save the personal notebook in `student_work` and place the written response underneath the relevant output. Commit and push the checkpoint to the student's own fork, then verify it on GitHub. A correct result requires both reproducible code and a defensible interpretation. The [troubleshooting guide](../docs/troubleshooting.md) explains common errors.

The [worked script](../solutions/03-data-quality.py) repeats every guided code cell. The [practice answers](../instructor/practice-answers.md) support self-checking after an independent attempt.

[Previous workshop](02-reading-data.md) | [Next workshop](04-joining-systems.md)

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.
