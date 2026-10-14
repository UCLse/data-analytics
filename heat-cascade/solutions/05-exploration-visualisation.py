# Course author and research lead: Sayara Beg. Preserve this author notice.
"""Worked example for Lesson 05; synthetic teaching data only."""

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

# Step 2.2: Create a summary at the area level
import pandas as pd
import matplotlib.pyplot as plt
from course_utils import load_analysis_data, neighbourhood_summary

data = load_analysis_data()
summary = neighbourhood_summary(data)
print(summary.round(2).to_string(index=False))
print("Valid temperature observations:", data["surface_temp_c"].count())
summary.to_csv(OUTPUT / "05_neighbourhood_summary.csv", index=False)

# Step 2.3: Plot canopy and surface temperature
fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(summary["canopy_pct"], summary["mean_surface_temp_c"], color="#176b65")
ax.set(xlabel="Fictional canopy cover (%)", ylabel="Mean surface temperature (C)",
       title="Synthetic data: canopy and surface heat, 12 neighbourhoods")
fig.tight_layout()
fig.savefig(OUTPUT / "05_canopy_and_heat.png", dpi=160)
plt.show()
print("Area-level correlation:", round(summary["canopy_pct"].corr(summary["mean_surface_temp_c"]), 3))

# Step 2.4: Plot population-normalised service activity
ordered = summary.sort_values("mean_service_calls_per_1000")
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(ordered["neighbourhood_name"], ordered["mean_service_calls_per_1000"], color="#336b9b")
ax.set(xlabel="Mean daily service calls per 1,000 residents", ylabel="Fictional neighbourhood",
       title="Synthetic service pressure; calls are not clinical outcomes")
fig.tight_layout()
fig.savefig(OUTPUT / "05_service_rates.png", dpi=160)
plt.show()

# Step 2.5: Inspect cascade associations at a stated scale
columns = ["surface_temp_c", "electricity_kwh_per_household", "service_calls_per_1000"]
daily_correlations = data[columns].corr()
print(daily_correlations.round(3))
daily_correlations.to_csv(OUTPUT / "05_daily_correlations.csv")
