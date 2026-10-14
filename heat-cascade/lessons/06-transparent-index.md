# 06. A transparent teaching index and sensitivity check

[Course home](../README.md) | **Indicative time:** 2 hours

**Research question:** How do normalisation choices and value judgements alter a composite priority ranking?

**Dataset boundary:** Every supplied observation and parameter is synthetic. The exercises teach analytical practice; their results do not establish Heat Cascade research findings.

## 1. Learning outcomes and vocabulary

- Normalise indicators with explicit directions.
- Build a weighted teaching index and inspect components.
- Compare rankings under alternative weights.

| Term | Meaning in this workshop |
| --- | --- |
| `normalisation` | Conversion of differently scaled values onto a common scale. |
| `weight` | A chosen contribution of an indicator to a composite score. |
| `sensitivity analysis` | Inspection of how outputs change when assumptions change. |
| `compensation` | A low component can offset a high component in a weighted sum. |

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

### 2.2. Define components and reference scales

**Why this step matters:** An explicit scale makes the index reproducible and reveals the assumptions behind its boundaries.

```python
import pandas as pd
from course_utils import load_analysis_data, neighbourhood_summary

summary = neighbourhood_summary(load_analysis_data())
summary["heat_component"] = ((summary["mean_surface_temp_c"] - 25) / (45 - 25)).clip(0, 1)
summary["canopy_deficit"] = 1 - summary["canopy_pct"] / 100
summary["vulnerability_component"] = summary["deprivation_score"] / 100
components = ["heat_component", "canopy_deficit", "vulnerability_component"]
print(summary[["neighbourhood_id"] + components].round(3).to_string(index=False))
```

**Expected result:** Three values between zero and one for each of 12 areas.

**Read the result:** The 25 to 45 C temperature range and the deprivation proxy are teaching assumptions. The index is an invented exercise without empirical validation. Larger components indicate greater illustrative priority.

### 2.3. Calculate and rank a weighted score

**Why this step matters:** The weight allocation encodes a decision perspective and must be disclosed.

```python
weights = {"heat_component": 0.4, "canopy_deficit": 0.3, "vulnerability_component": 0.3}
assert abs(sum(weights.values()) - 1) < 1e-9
summary["teaching_priority_score"] = 100 * sum(summary[col] * weight for col, weight in weights.items())
summary["baseline_rank"] = summary["teaching_priority_score"].rank(ascending=False, method="min").astype(int)
print(summary.sort_values("baseline_rank")[["neighbourhood_name", "teaching_priority_score", "baseline_rank"]].round(2).to_string(index=False))
```

**Expected result:** A ranking from 1 to 12, with Dockside near the highest-priority end.

**Read the result:** The score is an additive teaching index. Repeatedly measuring temperature does not validate the weights. Heat and canopy may overlap conceptually, so including both can double-count part of the same mechanism.

### 2.4. Inspect an alternative decision perspective

**Why this step matters:** Comparing components and ranks exposes what the index prioritises.

```python
alternative_weights = {"heat_component": 0.2, "canopy_deficit": 0.2, "vulnerability_component": 0.6}
summary["alternative_score"] = 100 * sum(summary[col] * weight for col, weight in alternative_weights.items())
summary["alternative_rank"] = summary["alternative_score"].rank(ascending=False, method="min").astype(int)
summary["rank_change"] = summary["alternative_rank"] - summary["baseline_rank"]
print(summary[["neighbourhood_name", "baseline_rank", "alternative_rank", "rank_change"]].to_string(index=False))
summary.to_csv(OUTPUT / "06_teaching_index.csv", index=False)
```

**Expected result:** A comparison table, with some or all ranks unchanged because these synthetic components covary strongly.

**Read the result:** A stable ranking under two choices does not prove robustness. It may reflect correlated inputs. Positive `rank_change` means a lower priority under the alternative weights, because larger rank numbers indicate lower priority.

## 3. Independent practice

Replace the vulnerability component with `older_residents_pct / 100`, recalculate both scores and compare the top three areas. Explain whether the original normalisation gives the indicators comparable influence.

<details>
<summary>Hint</summary>

Keep an unchanged copy of `summary`. The age component occupies a narrower observed range than the original deprivation component, despite both being bounded by zero and one.

</details>

## 4. Interpretation and checkpoint

Explain why this output must be called a teaching priority index. Name two validation requirements for a research index, such as construct justification, stakeholder scrutiny, independent outcome validation and examination of compensability. Identify one boundary at which a weighted sum would be unsuitable.

Save the personal notebook in `student_work` and place the written response underneath the relevant output. Commit and push the checkpoint to the student's own fork, then verify it on GitHub. A correct result requires both reproducible code and a defensible interpretation. The [troubleshooting guide](../docs/troubleshooting.md) explains common errors.

The [worked script](../solutions/06-transparent-index.py) repeats every guided code cell. The [practice answers](../instructor/practice-answers.md) support self-checking after an independent attempt.

[Previous workshop](05-exploration-visualisation.md) | [Next workshop](07-linear-regression.md)

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.
