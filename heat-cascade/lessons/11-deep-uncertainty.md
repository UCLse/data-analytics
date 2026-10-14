# 11. Scenario comparison under deep uncertainty

[Course home](../README.md) | **Indicative time:** 2 hours

**Research question:** Which intervention performs acceptably across alternative assumptions when reliable scenario probabilities are unavailable?

**Dataset boundary:** Every supplied observation and parameter is synthetic. The exercises teach analytical practice; their results do not establish Heat Cascade research findings.

## 1. Learning outcomes and vocabulary

- Distinguish scenarios from predictions and probability distributions.
- Compare affordable options across explicit future assumptions.
- Calculate regret and interpret the limits of a toy systems model.

| Term | Meaning in this workshop |
| --- | --- |
| `scenario` | A conditional future built from explicit assumptions. |
| `deep uncertainty` | Uncertainty about models, parameters, futures or their probabilities sufficient to prevent a single reliable forecast. |
| `regret` | An option's loss relative to the best feasible option within a stated future. |
| `minimax regret` | Selection of the smallest worst-case regret across the specified futures. |

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

### 2.2. Inspect the assumptions and feasible options

**Why this step matters:** The scenario boundary and budget define which comparisons have meaning.

```python
import numpy as np
import pandas as pd
from course_utils import load_analysis_data, neighbourhood_summary

base = neighbourhood_summary(load_analysis_data())
futures = pd.read_csv(DATA / "scenario_assumptions.csv")
options = pd.read_csv(DATA / "interventions.csv")
budget_gbp = 120000
feasible = options.loc[options["programme_cost_gbp"] <= budget_gbp]
print(futures.to_string(index=False))
print(feasible.to_string(index=False))
```

**Expected result:** Three assumption sets, A to C, and three affordable programmes. `Combined` is excluded because its cost is GBP 200,000.

**Read the result:** All costs and cooling coefficients are invented. Costs refer to an abstract programme applied across the fictional study system. The canopy option assumes mature cover, not immediate growth. No probabilities are attached to these futures.

### 2.3. Calculate a conditional cascade outcome

**Why this step matters:** The toy calculation makes every assumed dependency visible and keeps canopy within its physical percentage bounds.

```python
results = []
for future in futures.to_dict("records"):
    for option in feasible.to_dict("records"):
        canopy_after_loss = (base["canopy_pct"] - future["canopy_loss_pp"]).clip(lower=0)
        actual_loss = base["canopy_pct"] - canopy_after_loss
        actual_gain = np.minimum(option["canopy_gain_pp"], 100 - canopy_after_loss)
        temperature = (base["mean_surface_temp_c"] + future["background_warming_c"]
                       + actual_loss * future["cooling_c_per_canopy_pp"]
                       - actual_gain * future["cooling_c_per_canopy_pp"]
                       - option["shade_units"] * future["shade_cooling_c"])
        burden = ((temperature - 28).clip(lower=0) * future["burden_per_degree"]
                  + 3 * base["deprivation_score"] / 100)
        results.append({"future": future["future"], "intervention": option["intervention"],
                        "programme_cost_gbp": option["programme_cost_gbp"],
                        "mean_teaching_burden": burden.mean(), "worst_area_teaching_burden": burden.max()})
results = pd.DataFrame(results)
print(results.round(3).to_string(index=False))
results.to_csv(OUTPUT / "11_scenario_results.csv", index=False)
```

**Expected result:** Nine results: three feasible programmes evaluated in each of three futures.

**Read the result:** The outcome is a dimensionless teaching burden, not predicted illness or economic loss. It combines an arbitrary 28 C surface rule, a heat coefficient and a vulnerability term. The toy model omits feedback, adaptation, habitat dynamics and intervention delays.

### 2.4. Compare regret without inventing likelihoods

**Why this step matters:** Regret makes dependence on the chosen futures and objective explicit.

```python
burdens = results.pivot(index="intervention", columns="future", values="mean_teaching_burden")
regret = burdens.subtract(burdens.min(axis=0), axis=1)
decision = pd.DataFrame({"maximum_regret": regret.max(axis=1)})
decision = decision.sort_values("maximum_regret")
print("Mean teaching burden:")
print(burdens.round(3))
print("Regret:")
print(regret.round(3))
print("Smallest maximum regret first:")
print(decision.round(3))
regret.to_csv(OUTPUT / "11_regret.csv")
decision.to_csv(OUTPUT / "11_minimax_regret.csv")
```

**Expected result:** Mature canopy is preferred on mean burden in A; street shade is preferred in B and C. The minimax-regret table reports a conditional choice.

**Read the result:** The ranking reversal demonstrates assumption dependence. Minimax regret expresses a decision criterion, not a universally optimal policy. Equal weighting of areas, the budget, the mature-canopy assumption and the selected futures all shape the result.

## 3. Independent practice

Compare the options using the worst-area burden instead of the mean. Then repeat with a GBP 200,000 budget. Explain why this is sensitivity analysis and why no expected-value calculation is justified.

<details>
<summary>Hint</summary>

Pivot `worst_area_teaching_burden` for the equity-oriented comparison. To change the budget, rerun the option filter and both following calculation cells. No supplied scenario has a validated probability.

</details>

## 4. Interpretation and checkpoint

Write a conditional recommendation naming the objective, budget and assumptions. State one observation that would trigger review. Explain why this exercise is a scenario calculator, and identify the empirical calibration and validation needed before operational use.

Save the personal notebook in `student_work` and place the written response underneath the relevant output. Commit and push the checkpoint to the student's own fork, then verify it on GitHub. A correct result requires both reproducible code and a defensible interpretation. The [troubleshooting guide](../docs/troubleshooting.md) explains common errors.

The [worked script](../solutions/11-deep-uncertainty.py) repeats every guided code cell. The [practice answers](../instructor/practice-answers.md) support self-checking after an independent attempt.

[Previous workshop](10-time-series.md) | [Next workshop](12-game-and-text.md)

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.
