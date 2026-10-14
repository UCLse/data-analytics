# Course author and research lead: Sayara Beg. Preserve this author notice.
"""Worked example for Lesson 02; synthetic teaching data only."""

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

# Step 2.2: Import pandas and read the tables
import pandas as pd

areas = pd.read_csv(DATA / "neighbourhoods.csv")
readings = pd.read_csv(DATA / "monitoring.csv")
print("Area shape:", areas.shape)
print("Monitoring shape:", readings.shape)
print(areas.head(3).to_string(index=False))

# Step 2.3: Inspect the schema
print(readings.columns.tolist())
print(readings.dtypes)
print(readings.isna().sum())
print(areas[["population", "older_residents_pct"]].describe().round(2))

# Step 2.4: Select and filter area attributes
selected = areas[["neighbourhood_id", "neighbourhood_name", "population", "older_residents_pct"]]
older_areas = selected.loc[selected["older_residents_pct"] >= 24].copy()
older_areas = older_areas.sort_values("older_residents_pct", ascending=False)
print(older_areas.to_string(index=False))

# Step 2.5: Save a useful extract
older_areas.to_csv(OUTPUT / "02_older_area_extract.csv", index=False)
print("Saved rows:", len(older_areas))
