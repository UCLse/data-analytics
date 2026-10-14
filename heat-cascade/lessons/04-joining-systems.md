# 04. Joining ecosystem, heat and vulnerability data

[Course home](../README.md) | **Indicative time:** 2 hours

**Research question:** How can different data layers be connected without multiplying records or mixing incompatible dates?

**Dataset boundary:** Every supplied observation and parameter is synthetic. The exercises teach analytical practice; their results do not establish Heat Cascade research findings.

## 1. Learning outcomes and vocabulary

- Join tables using explicit keys and cardinality checks.
- Calculate a population-normalised rate.
- Measure a canopy transition in percentage points.

| Term | Meaning in this workshop |
| --- | --- |
| `join` | Combination of columns from related tables using a key. |
| `many-to-one` | Many daily records relate to one area metadata record. |
| `percentage point` | The difference between two percentages. |
| `rate` | A count divided by a stated population or exposure denominator. |

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

### 2.2. Prepare the three layers

**Why this step matters:** The join requires clean daily measurements, one area record and one ecosystem snapshot per area.

```python
import pandas as pd
from course_utils import clean_monitoring

monitoring = clean_monitoring(pd.read_csv(DATA / "monitoring.csv"))
areas = pd.read_csv(DATA / "neighbourhoods.csv").drop(columns="data_status")
ecology = pd.read_csv(DATA / "ecosystems.csv")
current = ecology.loc[ecology["year"].eq(2025)].drop(columns=["year", "data_status"])
print("Rows:", len(monitoring), len(areas), len(current))
```

**Expected result:** `Rows: 1080 12 12`.

**Read the result:** `clean_monitoring` repeats the manual Lesson 03 rules. Its source is available in [course_utils.py](../course_utils.py). The 2025 ecosystem values are fictional baseline attributes, not measured daily observations.

### 2.3. Join and inspect matches

**Why this step matters:** Cardinality and match checks prevent accidental row multiplication and silent loss of area information.

```python
analysis = monitoring.merge(areas, on="neighbourhood_id", how="left", validate="many_to_one", indicator=True)
print(analysis["_merge"].value_counts())
assert analysis["_merge"].eq("both").all(), "Some area keys did not match."
analysis = analysis.drop(columns="_merge")
analysis = analysis.merge(current, on="neighbourhood_id", how="left", validate="many_to_one", indicator=True)
assert analysis["_merge"].eq("both").all(), "Some ecosystem keys did not match."
analysis = analysis.drop(columns="_merge")
assert len(analysis) == len(monitoring)
print("Joined rows:", len(analysis))
```

**Expected result:** All 1,080 rows have a match, and the final join retains 1,080 rows.

**Read the result:** `validate="many_to_one"` checks uniqueness on the right. `indicator=True` identifies matches. `assert` stops the code when its condition fails. An error here protects the analysis from continuing with a broken join.

### 2.4. Normalise counts and quantify transitions

**Why this step matters:** Rates improve comparisons between differently sized populations; percentage-point changes describe ecosystem trajectories.

```python
analysis["service_calls_per_1000"] = analysis["service_calls"] / analysis["population"] * 1000
cover = ecology.pivot(index="neighbourhood_id", columns="year", values="canopy_pct")
transition = (cover[2025] - cover[2020]).rename("canopy_change_pp").reset_index()
analysis = analysis.merge(transition, on="neighbourhood_id", validate="many_to_one")
print(transition.to_string(index=False))
analysis.to_csv(OUTPUT / "04_analysis_table.csv", index=False)
transition.to_csv(OUTPUT / "04_canopy_transition.csv", index=False)
```

**Expected result:** A 12-row transition table. Ashfield changes by -5.5 percentage points, and Fern Park changes by +4.0.

**Read the result:** A fall from 14.5% to 9% is -5.5 percentage points. It is approximately a 37.9% relative decline. Service calls per 1,000 are daily aggregate service activity, not confirmed heat-related diagnoses.

## 3. Independent practice

Find the neighbourhood with the largest canopy loss between 2020 and 2025. State its absolute percentage-point change and explain one limitation of assigning a yearly cover value to every day.

<details>
<summary>Hint</summary>

Sort `transition` by `canopy_change_pp`. Yearly snapshots cannot show within-year losses, growth or measurement changes.

</details>

## 4. Interpretation and checkpoint

State the composite key of the joined table. Identify which attributes vary daily and which are repeated from area metadata. Explain why a finer geographical label does not automatically create finer-resolution evidence.

Save the personal notebook in `student_work` and place the written response underneath the relevant output. Commit and push the checkpoint to the student's own fork, then verify it on GitHub. A correct result requires both reproducible code and a defensible interpretation. The [troubleshooting guide](../docs/troubleshooting.md) explains common errors.

The [worked script](../solutions/04-joining-systems.py) repeats every guided code cell. The [practice answers](../instructor/practice-answers.md) support self-checking after an independent attempt.

[Previous workshop](03-data-quality.md) | [Next workshop](05-exploration-visualisation.md)

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.
