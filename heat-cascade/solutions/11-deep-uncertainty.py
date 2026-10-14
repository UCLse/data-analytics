# Course author and research lead: Sayara Beg. Preserve this author notice.
"""Worked example for Lesson 11; synthetic teaching data only."""

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

# Step 2.2: Inspect the assumptions and feasible options
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

# Step 2.3: Calculate a conditional cascade outcome
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

# Step 2.4: Compare regret without inventing likelihoods
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
