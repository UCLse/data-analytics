# Course author and research lead: Sayara Beg. Preserve this author notice.
"""Worked example for Lesson 07; synthetic teaching data only."""

# Step 2.1: Find the course files
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

# Step 2.2: Define the analytical question and usable records
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

# Step 2.3: Hold out entire neighbourhoods
splitter = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=42)
train_index, test_index = next(splitter.split(X, y, groups=groups))
X_train, X_test = X.iloc[train_index], X.iloc[test_index]
y_train, y_test = y.iloc[train_index], y.iloc[test_index]
train_groups = set(groups.iloc[train_index])
test_groups = set(groups.iloc[test_index])
assert train_groups.isdisjoint(test_groups)
print("Training neighbourhoods:", sorted(train_groups))
print("Test neighbourhoods:", sorted(test_groups))

# Step 2.4: Fit the model and a simple baseline
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

# Step 2.5: Inspect coefficients and residuals
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
