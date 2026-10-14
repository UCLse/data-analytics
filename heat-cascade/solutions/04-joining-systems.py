# Course author and research lead: Sayara Beg. Preserve this author notice.
"""Worked example for Lesson 04; synthetic teaching data only."""

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

# Step 2.2: Prepare the three layers
import pandas as pd
from course_utils import clean_monitoring

monitoring = clean_monitoring(pd.read_csv(DATA / "monitoring.csv"))
areas = pd.read_csv(DATA / "neighbourhoods.csv").drop(columns="data_status")
ecology = pd.read_csv(DATA / "ecosystems.csv")
current = ecology.loc[ecology["year"].eq(2025)].drop(columns=["year", "data_status"])
print("Rows:", len(monitoring), len(areas), len(current))

# Step 2.3: Join and inspect matches
analysis = monitoring.merge(areas, on="neighbourhood_id", how="left", validate="many_to_one", indicator=True)
print(analysis["_merge"].value_counts())
assert analysis["_merge"].eq("both").all(), "Some area keys did not match."
analysis = analysis.drop(columns="_merge")
analysis = analysis.merge(current, on="neighbourhood_id", how="left", validate="many_to_one", indicator=True)
assert analysis["_merge"].eq("both").all(), "Some ecosystem keys did not match."
analysis = analysis.drop(columns="_merge")
assert len(analysis) == len(monitoring)
print("Joined rows:", len(analysis))

# Step 2.4: Normalise counts and quantify transitions
analysis["service_calls_per_1000"] = analysis["service_calls"] / analysis["population"] * 1000
cover = ecology.pivot(index="neighbourhood_id", columns="year", values="canopy_pct")
transition = (cover[2025] - cover[2020]).rename("canopy_change_pp").reset_index()
analysis = analysis.merge(transition, on="neighbourhood_id", validate="many_to_one")
print(transition.to_string(index=False))
analysis.to_csv(OUTPUT / "04_analysis_table.csv", index=False)
transition.to_csv(OUTPUT / "04_canopy_transition.csv", index=False)
