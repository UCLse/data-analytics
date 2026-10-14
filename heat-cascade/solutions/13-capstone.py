# Course author and research lead: Sayara Beg. Preserve this author notice.
"""Worked example for Lesson 13; synthetic teaching data only."""

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

# Step 2.2: Create an evidence table with explicit denominators
import json
import pandas as pd
from importlib.metadata import version
from course_utils import load_analysis_data, neighbourhood_summary

data = load_analysis_data()
evidence = neighbourhood_summary(data).sort_values("mean_surface_temp_c", ascending=False)
evidence.to_csv(OUTPUT / "13_evidence_table.csv", index=False)
print(evidence.round(2).to_string(index=False))

# Step 2.3: Record the run environment and data status
manifest = json.loads((ROOT / "data/generation_manifest.json").read_text())
run_record = {
    "data_status": "synthetic", "generation_seed": manifest["seed"],
    "date_start": data["date"].min().strftime("%Y-%m-%d"),
    "date_end": data["date"].max().strftime("%Y-%m-%d"),
    "area_count": data["neighbourhood_id"].nunique(), "area_day_rows": len(data),
    "valid_surface_measurements": int(data["surface_temp_c"].count()),
    "packages": {name: version(name) for name in ["numpy", "pandas", "matplotlib", "scikit-learn"]},
}
(OUTPUT / "13_run_record.json").write_text(json.dumps(run_record, indent=2) + "\n")
print(json.dumps(run_record, indent=2))
