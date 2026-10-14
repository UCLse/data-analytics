# Course author and research lead: Sayara Beg. Preserve this author notice.
"""Worked example for Lesson 03; synthetic teaching data only."""

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

# Step 2.2: Read a fresh copy and inspect anomalies
import pandas as pd

raw = pd.read_csv(DATA / "monitoring.csv")
print("Raw rows:", len(raw))
print("Exact duplicate rows:", raw.duplicated().sum())
numeric_surface = pd.to_numeric(raw["surface_temp_c"], errors="coerce")
new_conversion_failures = raw["surface_temp_c"].notna() & numeric_surface.isna()
print("Non-blank conversion failures:", new_conversion_failures.sum())
print(raw.loc[new_conversion_failures, ["neighbourhood_id", "date", "surface_temp_c"]])

# Step 2.3: Normalise identifiers and parse values
clean = raw.copy()
clean["neighbourhood_id"] = clean["neighbourhood_id"].str.strip().str.upper()
clean["date"] = pd.to_datetime(clean["date"], errors="coerce")
clean["surface_temp_c"] = pd.to_numeric(clean["surface_temp_c"], errors="coerce")
print("Invalid dates:", clean["date"].isna().sum())
print("Missing surface values after conversion:", clean["surface_temp_c"].isna().sum())

# Step 2.4: Apply documented teaching bounds
surface_invalid = clean["surface_temp_c"].notna() & ~clean["surface_temp_c"].between(-10, 65)
humidity_invalid = clean["relative_humidity_pct"].notna() & ~clean["relative_humidity_pct"].between(0, 100)
clean.loc[surface_invalid, "surface_temp_c"] = float("nan")
clean.loc[humidity_invalid, "relative_humidity_pct"] = float("nan")
clean = clean.drop_duplicates().sort_values(["date", "neighbourhood_id"]).reset_index(drop=True)
key_conflicts = clean.duplicated(["neighbourhood_id", "date"]).sum()
print("Clean rows:", len(clean))
print("Key conflicts:", key_conflicts)
print(clean[["surface_temp_c", "relative_humidity_pct"]].isna().sum())

# Step 2.5: Save the audit and clean table
audit = pd.DataFrame({
    "check": ["raw_rows", "exact_duplicates_removed", "nonblank_surface_conversion_failures",
              "surface_range_failures", "humidity_range_failures", "clean_rows", "surface_missing_after_cleaning"],
    "value": [len(raw), raw.duplicated().sum(), new_conversion_failures.sum(),
              surface_invalid.sum(), humidity_invalid.sum(), len(clean), clean["surface_temp_c"].isna().sum()],
})
clean.to_csv(OUTPUT / "03_monitoring_clean.csv", index=False)
audit.to_csv(OUTPUT / "03_quality_audit.csv", index=False)
print(audit.to_string(index=False))
