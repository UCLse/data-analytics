# 10. Time series with chronological, one-day-ahead evaluation

[Course home](../README.md) | **Indicative time:** 2 hours

**Research question:** How well do simple methods estimate the next daily city mean using information available before that day?

**Dataset boundary:** Every supplied observation and parameter is synthetic. The exercises teach analytical practice; their results do not establish Heat Cascade research findings.

## 1. Learning outcomes and vocabulary

- Construct a dated series and check its frequency.
- Build past-only lag features and a chronological holdout.
- Compare simple baselines with a lag regression.

| Term | Meaning in this workshop |
| --- | --- |
| `lag` | A previously observed value, such as yesterday's temperature. |
| `chronological split` | Training observations precede test observations. |
| `rolling origin` | The prediction origin moves forward as new observations become available. |
| `forecast horizon` | The time between the prediction origin and its target. |

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

### 2.2. Aggregate and check the dated series

**Why this step matters:** A forecast requires a clear temporal unit and a complete, ordered history.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from course_utils import load_analysis_data
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

data = load_analysis_data()
series = data.groupby("date")["surface_temp_c"].mean().sort_index().asfreq("D")
valid_counts = data.groupby("date")["surface_temp_c"].count().asfreq("D")
print("Calendar days:", len(series))
print("Missing daily means:", series.isna().sum())
print("Minimum valid areas contributing to a day:", valid_counts.min())
assert not series.isna().any()
```

**Expected result:** 90 daily means, no missing daily mean, and at least 11 valid area readings per day.

**Read the result:** This is an unweighted city mean across fictional neighbourhoods. It is not an individual exposure estimate. Missing area readings can change the effective composition of the average.

### 2.3. Create past-only predictors and the time split

**Why this step matters:** Every predictor must be available at the time a forecast would be issued.

```python
table = pd.DataFrame({"surface_mean_c": series})
table["lag_1"] = series.shift(1)
table["lag_7"] = series.shift(7)
table["day_index"] = np.arange(len(table))
table = table.dropna()
cutoff = series.index[-28]
train = table.loc[table.index < cutoff]
test = table.loc[table.index >= cutoff]
assert train.index.max() < test.index.min()
print("Train feature rows:", len(train), "Test feature rows:", len(test))
print("First test day:", cutoff.date())
```

**Expected result:** 55 training feature rows, 28 test rows; the first test day is 2025-08-02.

**Read the result:** The first seven days provide lag history and do not form feature rows. A test-day lag can use an earlier test-day observation because evaluation moves forward one day at a time. It never uses the current target or a later observation.

### 2.4. Evaluate two baselines and a lag model

**Why this step matters:** A more complex method needs to earn its place against practical baseline forecasts.

```python
features = ["lag_1", "lag_7", "day_index"]
model = LinearRegression().fit(train[features], train["surface_mean_c"])
prediction = model.predict(test[features])
methods = {"Previous day": test["lag_1"].to_numpy(),
           "Seven days earlier": test["lag_7"].to_numpy(), "Lag regression": prediction}
scores = pd.DataFrame([{"method": name, "MAE_C": mean_absolute_error(test["surface_mean_c"], values)}
                       for name, values in methods.items()])
print(scores.round(3).to_string(index=False))
evaluation = test[["surface_mean_c"]].copy()
for name, values in methods.items():
    evaluation[name] = values
scores.to_csv(OUTPUT / "10_time_series_metrics.csv", index=False)
evaluation.to_csv(OUTPUT / "10_one_day_predictions.csv")
```

**Expected result:** Three MAE values measured in C. The ranking of methods must be read from the output.

**Read the result:** The model is fitted once on pre-cutoff records. Earlier observations become available during the test period, but the model is not refitted. This is rolling one-day-ahead evaluation, not a 28-day forecast issued at a single origin.

### 2.5. Inspect prediction behaviour and failure points

**Why this step matters:** A plot reveals whether averages hide large errors around changing conditions.

```python
fig, ax = plt.subplots(figsize=(9, 4))
series.plot(ax=ax, color="black", label="Observed synthetic mean")
evaluation["Lag regression"].plot(ax=ax, color="#176b65", label="One-day-ahead lag model")
evaluation["Previous day"].plot(ax=ax, color="#d27a32", linestyle=":", label="Previous-day baseline")
ax.axvline(cutoff, color="grey", linestyle="--", label="Test begins")
ax.set(xlabel="Date", ylabel="Mean surface temperature (C)",
       title="Synthetic short summer history; chronological evaluation")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUTPUT / "10_time_series.png", dpi=160)
plt.show()
```

**Expected result:** A 90-day history and prediction lines over the final 28 days.

**Read the result:** Ninety summer days cannot identify annual seasonality or validate future climate extrapolation. The shared warm spells are invented. Advanced ARIMA or seasonal models require their own justified history, diagnostics and validation; they are not added automatically.

## 3. Independent practice

Identify the worst-error test day for the lag regression. Explain which observed inputs would be available at the end of the previous day. Describe what must change for a seven-day forecast issued at one fixed origin.

<details>
<summary>Hint</summary>

Subtract the lag prediction from the observed mean, take absolute values and use `idxmax()`. For a fixed-origin multi-day forecast, unavailable future lag values must be predicted or replaced using a declared strategy.

</details>

## 4. Interpretation and checkpoint

State the forecast horizon, origin, training cutoff and error units. Explain why an excellent regression fit in Lesson 07 would not validate this forecast. Identify one real-world dependency, such as sensor delay, that could invalidate the assumed predictor availability.

Save the personal notebook in `student_work` and place the written response underneath the relevant output. Commit and push the checkpoint to the student's own fork, then verify it on GitHub. A correct result requires both reproducible code and a defensible interpretation. The [troubleshooting guide](../docs/troubleshooting.md) explains common errors.

The [worked script](../solutions/10-time-series.py) repeats every guided code cell. The [practice answers](../instructor/practice-answers.md) support self-checking after an independent attempt.

[Previous workshop](09-clustering.md) | [Next workshop](11-deep-uncertainty.md)

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.
