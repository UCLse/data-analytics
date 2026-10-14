# 05. Exploration, visualisation and the cascade boundary

[Course home](../README.md) | **Indicative time:** 2 hours

**Research question:** Which patterns connect ecosystem condition, surface heat and service pressure in this synthetic system?

**Dataset boundary:** Every supplied observation and parameter is synthetic. The exercises teach analytical practice; their results do not establish Heat Cascade research findings.

## 1. Learning outcomes and vocabulary

- Produce an area summary with valid-measurement counts.
- Draw labelled charts and inspect missingness.
- Separate association, scale and causal interpretation.

| Term | Meaning in this workshop |
| --- | --- |
| `aggregation` | Combining observations at a stated level, such as neighbourhood. |
| `correlation` | A numerical description of linear association. |
| `ecological fallacy` | Inferring individual characteristics from area-level patterns. |
| `surface temperature` | Temperature of a surface, distinct from near-surface air temperature. |

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

### 2.2. Create a summary at the area level

**Why this step matters:** One row per area makes the level of comparison explicit and exposes unequal valid-reading counts.

```python
import pandas as pd
import matplotlib.pyplot as plt
from course_utils import load_analysis_data, neighbourhood_summary

data = load_analysis_data()
summary = neighbourhood_summary(data)
print(summary.round(2).to_string(index=False))
print("Valid temperature observations:", data["surface_temp_c"].count())
summary.to_csv(OUTPUT / "05_neighbourhood_summary.csv", index=False)
```

**Expected result:** 12 neighbourhood rows and 1,067 valid surface-temperature observations.

**Read the result:** The helper repeats Lessons 03 and 04 with the current ecosystem snapshot. It does not rely on saved outputs from earlier lessons. Area-level comparisons have 12 units, not 1,080 independent areas.

### 2.3. Plot canopy and surface temperature

**Why this step matters:** A scatter plot displays the relationship, units and number of area-level points directly.

```python
fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(summary["canopy_pct"], summary["mean_surface_temp_c"], color="#176b65")
ax.set(xlabel="Fictional canopy cover (%)", ylabel="Mean surface temperature (C)",
       title="Synthetic data: canopy and surface heat, 12 neighbourhoods")
fig.tight_layout()
fig.savefig(OUTPUT / "05_canopy_and_heat.png", dpi=160)
plt.show()
print("Area-level correlation:", round(summary["canopy_pct"].corr(summary["mean_surface_temp_c"]), 3))
```

**Expected result:** A downward pattern across 12 points, with a strongly negative correlation.

**Read the result:** The generator builds part of this pattern deliberately. Impervious cover and other area attributes also covary with canopy. The chart cannot establish the effect of planting trees in a real neighbourhood.

### 2.4. Plot population-normalised service activity

**Why this step matters:** A labelled rate avoids interpreting larger raw counts as greater individual risk.

```python
ordered = summary.sort_values("mean_service_calls_per_1000")
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(ordered["neighbourhood_name"], ordered["mean_service_calls_per_1000"], color="#336b9b")
ax.set(xlabel="Mean daily service calls per 1,000 residents", ylabel="Fictional neighbourhood",
       title="Synthetic service pressure; calls are not clinical outcomes")
fig.tight_layout()
fig.savefig(OUTPUT / "05_service_rates.png", dpi=160)
plt.show()
```

**Expected result:** A horizontal chart showing all 12 fictional neighbourhoods.

**Read the result:** The population denominator makes the bars more comparable. The rates remain area-level service activity and may reflect reporting, access or service availability in real data.

### 2.5. Inspect cascade associations at a stated scale

**Why this step matters:** A short association table guides questions for later research without claiming to confirm a cascade.

```python
columns = ["surface_temp_c", "electricity_kwh_per_household", "service_calls_per_1000"]
daily_correlations = data[columns].corr()
print(daily_correlations.round(3))
daily_correlations.to_csv(OUTPUT / "05_daily_correlations.csv")
```

**Expected result:** A 3 by 3 correlation table with 1.0 on the diagonal.

**Read the result:** These correlations pool repeated area-day records and shared weather. Their magnitude does not measure a causal pathway, and the table supplies no valid causal significance test. Correlation near zero also does not rule out a nonlinear relationship.

## 3. Independent practice

Create a third labelled chart showing the number of valid surface readings per neighbourhood. Identify which averages use fewer than 90 readings and write a 120-word explanation of the analytical boundary.

<details>
<summary>Hint</summary>

Use the `valid_surface_days` column in `summary`. Include synthetic status, observation level, period and missingness in the explanation.

</details>

## 4. Interpretation and checkpoint

Write one observation, one possible explanation and one further data requirement. Keep those statements distinct. Identify a missing layer, such as infrastructure capacity, and explain why a temperature-service correlation alone cannot demonstrate risk propagation.

Save the personal notebook in `student_work` and place the written response underneath the relevant output. Commit and push the checkpoint to the student's own fork, then verify it on GitHub. A correct result requires both reproducible code and a defensible interpretation. The [troubleshooting guide](../docs/troubleshooting.md) explains common errors.

The [worked script](../solutions/05-exploration-visualisation.py) repeats every guided code cell. The [practice answers](../instructor/practice-answers.md) support self-checking after an independent attempt.

[Previous workshop](04-joining-systems.md) | [Next workshop](06-transparent-index.md)

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.
