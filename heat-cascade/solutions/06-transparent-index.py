# Course author and research lead: Sayara Beg. Preserve this author notice.
"""Worked example for Lesson 06; synthetic teaching data only."""

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

# Step 2.2: Define components and reference scales
import pandas as pd
from course_utils import load_analysis_data, neighbourhood_summary

summary = neighbourhood_summary(load_analysis_data())
summary["heat_component"] = ((summary["mean_surface_temp_c"] - 25) / (45 - 25)).clip(0, 1)
summary["canopy_deficit"] = 1 - summary["canopy_pct"] / 100
summary["vulnerability_component"] = summary["deprivation_score"] / 100
components = ["heat_component", "canopy_deficit", "vulnerability_component"]
print(summary[["neighbourhood_id"] + components].round(3).to_string(index=False))

# Step 2.3: Calculate and rank a weighted score
weights = {"heat_component": 0.4, "canopy_deficit": 0.3, "vulnerability_component": 0.3}
assert abs(sum(weights.values()) - 1) < 1e-9
summary["teaching_priority_score"] = 100 * sum(summary[col] * weight for col, weight in weights.items())
summary["baseline_rank"] = summary["teaching_priority_score"].rank(ascending=False, method="min").astype(int)
print(summary.sort_values("baseline_rank")[["neighbourhood_name", "teaching_priority_score", "baseline_rank"]].round(2).to_string(index=False))

# Step 2.4: Inspect an alternative decision perspective
alternative_weights = {"heat_component": 0.2, "canopy_deficit": 0.2, "vulnerability_component": 0.6}
summary["alternative_score"] = 100 * sum(summary[col] * weight for col, weight in alternative_weights.items())
summary["alternative_rank"] = summary["alternative_score"].rank(ascending=False, method="min").astype(int)
summary["rank_change"] = summary["alternative_rank"] - summary["baseline_rank"]
print(summary[["neighbourhood_name", "baseline_rank", "alternative_rank", "rank_change"]].to_string(index=False))
summary.to_csv(OUTPUT / "06_teaching_index.csv", index=False)
