# 07. Linear regression with a held-out neighbourhood test

[Course home](../README.md) | **Indicative time:** 2 hours

**Research question:** Can a simple model estimate surface temperature in neighbourhoods excluded from model fitting?

**Dataset boundary:** Every supplied observation and parameter is synthetic. The exercises teach analytical practice; their results do not establish Heat Cascade research findings.

## 1. Learning outcomes and vocabulary

- Separate predictors from a continuous target.
- Hold out whole neighbourhoods and compare a baseline.
- Interpret errors and coefficients within the validation boundary.

| Term | Meaning in this workshop |
| --- | --- |
| `predictor` | An input used by a model. |
| `target` | The quantity being estimated. |
| `training set` | Observations available for fitting the model. |
| `test set` | Observations reserved for an initial evaluation. |
| `MAE` | Mean absolute prediction error, in the target units. |

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

### 2.2. Define the analytical question and usable records

**Why this step matters:** A measured target is needed to evaluate a prediction; missing targets cannot be replaced with invented observations.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from course_utils import load_analysis_data
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

data = load_analysis_data().dropna(subset=["surface_temp_c"]).reset_index(drop=True)
features = ["regional_air_temp_c", "canopy_pct", "impervious_pct"]
X = data[features]
y = data["surface_temp_c"]
groups = data["neighbourhood_id"]
print("Usable target records:", len(data))
```

**Expected result:** 1,067 records with a measured synthetic surface-temperature target.

**Read the result:** This is a same-day estimate using observed regional air temperature. It is not a next-day forecast. The annual ecosystem snapshot is treated as available baseline metadata in the teaching scenario.

### 2.3. Hold out entire neighbourhoods

**Why this step matters:** A random row split would let repeated observations from the same area appear in both training and testing.

```python
splitter = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=42)
train_index, test_index = next(splitter.split(X, y, groups=groups))
X_train, X_test = X.iloc[train_index], X.iloc[test_index]
y_train, y_test = y.iloc[train_index], y.iloc[test_index]
train_groups = set(groups.iloc[train_index])
test_groups = set(groups.iloc[test_index])
assert train_groups.isdisjoint(test_groups)
print("Training neighbourhoods:", sorted(train_groups))
print("Test neighbourhoods:", sorted(test_groups))
```

**Expected result:** Nine training neighbourhoods and three test neighbourhoods, with no overlap.

**Read the result:** The 25% split refers to groups, so the row proportions can differ slightly. Shared weather and nearby spatial relationships remain. This split does not establish performance in another city or in future conditions.

### 2.4. Fit the model and a simple baseline

**Why this step matters:** A model is useful only when its errors are assessed against a stated alternative.

```python
model = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("regression", LinearRegression()),
])
model.fit(X_train, y_train)
predicted = model.predict(X_test)
baseline = DummyRegressor(strategy="mean").fit(X_train, y_train)
baseline_predicted = baseline.predict(X_test)
scores = pd.DataFrame([
    {"model": "Training mean baseline", "MAE_C": mean_absolute_error(y_test, baseline_predicted),
     "RMSE_C": np.sqrt(mean_squared_error(y_test, baseline_predicted)), "R2": r2_score(y_test, baseline_predicted)},
    {"model": "Linear regression", "MAE_C": mean_absolute_error(y_test, predicted),
     "RMSE_C": np.sqrt(mean_squared_error(y_test, predicted)), "R2": r2_score(y_test, predicted)},
])
print(scores.round(3).to_string(index=False))
scores.to_csv(OUTPUT / "07_regression_metrics.csv", index=False)
```

**Expected result:** MAE, RMSE and R2 for two methods. The synthetic generating equation should make the regression useful against the mean baseline.

**Read the result:** The pipeline learns any median replacement from training data only. RMSE gives larger errors more influence. R2 can be negative when a model performs poorly against a constant test-mean reference; it is not a percentage of correct predictions.

### 2.5. Inspect coefficients and residuals

**Why this step matters:** Prediction errors and fitted relationships describe different aspects of the model.

```python
coefficients = pd.DataFrame({"feature": features, "coefficient": model.named_steps["regression"].coef_})
print(coefficients.round(3).to_string(index=False))
evaluation = data.iloc[test_index][["neighbourhood_id", "date"]].copy()
evaluation["actual_surface_c"] = y_test.to_numpy()
evaluation["predicted_surface_c"] = predicted
evaluation["residual_c"] = evaluation["actual_surface_c"] - predicted
print(evaluation.groupby("neighbourhood_id")["residual_c"].agg(["mean", "std"]).round(3))
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(predicted, evaluation["residual_c"], alpha=0.5, color="#176b65")
ax.axhline(0, color="black", linewidth=1)
ax.set(xlabel="Predicted surface temperature (C)", ylabel="Actual minus predicted (C)",
       title="Synthetic held-out neighbourhood residuals")
fig.tight_layout()
fig.savefig(OUTPUT / "07_residuals.png", dpi=160)
plt.show()
evaluation.to_csv(OUTPUT / "07_test_predictions.csv", index=False)
coefficients.to_csv(OUTPUT / "07_coefficients.csv", index=False)
```

**Expected result:** A negative canopy coefficient and a residual plot centred roughly around zero, with nonzero prediction errors.

**Read the result:** The unscaled canopy coefficient refers to a one percentage-point difference, holding the other fitted predictors constant. Correlated features and a small number of areas limit this interpretation. No p-value, causal effect or deployment assurance follows from the coefficient.

## 3. Independent practice

Calculate test MAE separately for each held-out neighbourhood. Explain why a low pooled error can hide a weaker result in one area. Propose an additional validation design before applying a model to a real city.

<details>
<summary>Hint</summary>

Create an `absolute_error_c` column from the absolute residual, then group by `neighbourhood_id`. A new time window and genuinely separated spatial areas address different generalisation questions.

</details>

## 4. Interpretation and checkpoint

State the target, predictor availability, test boundary and MAE units. Explain why lower predictive error does not establish the real cooling effect of a canopy intervention. Avoid choosing features repeatedly after inspecting the same test set.

Save the personal notebook in `student_work` and place the written response underneath the relevant output. Commit and push the checkpoint to the student's own fork, then verify it on GitHub. A correct result requires both reproducible code and a defensible interpretation. The [troubleshooting guide](../docs/troubleshooting.md) explains common errors.

The [worked script](../solutions/07-linear-regression.py) repeats every guided code cell. The [practice answers](../instructor/practice-answers.md) support self-checking after an independent attempt.

[Previous workshop](06-transparent-index.md) | [Next workshop](08-classification.md)

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.
