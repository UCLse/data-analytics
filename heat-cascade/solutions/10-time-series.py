# Course author and research lead: Sayara Beg. Preserve this author notice.
"""Worked example for Lesson 10; synthetic teaching data only."""

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

# Step 2.2: Aggregate and check the dated series
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

# Step 2.3: Create past-only predictors and the time split
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

# Step 2.4: Evaluate two baselines and a lag model
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

# Step 2.5: Inspect prediction behaviour and failure points
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
