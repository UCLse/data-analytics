# Course author and research lead: Sayara Beg. Preserve this author notice.
"""Shared, transparent preparation for lessons that follow the manual cleaning workshop."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
OUTPUT = ROOT / "outputs"

def clean_monitoring(raw):
    """Repeat Lesson 03 rules; preserve missing measurements for later handling."""
    clean = raw.copy()
    clean["neighbourhood_id"] = clean["neighbourhood_id"].str.strip().str.upper()
    clean["date"] = pd.to_datetime(clean["date"], errors="coerce")
    clean["surface_temp_c"] = pd.to_numeric(clean["surface_temp_c"], errors="coerce")
    clean.loc[~clean["surface_temp_c"].between(-10, 65), "surface_temp_c"] = float("nan")
    clean.loc[~clean["relative_humidity_pct"].between(0, 100), "relative_humidity_pct"] = float("nan")
    clean = clean.drop_duplicates().sort_values(["date", "neighbourhood_id"]).reset_index(drop=True)
    if clean["date"].isna().any() or clean["neighbourhood_id"].isna().any():
        raise ValueError("A date or neighbourhood key is missing. Investigate before joining.")
    if clean.duplicated(["neighbourhood_id", "date"]).any():
        raise ValueError("Conflicting neighbourhood-date records require review.")
    return clean

def load_analysis_data():
    """Join daily monitoring to static fictional area data and the 2025 ecosystem snapshot."""
    data = clean_monitoring(pd.read_csv(RAW / "monitoring.csv"))
    areas = pd.read_csv(RAW / "neighbourhoods.csv").drop(columns="data_status")
    ecology = pd.read_csv(RAW / "ecosystems.csv")
    ecology = ecology.loc[ecology["year"].eq(2025)].drop(columns=["year", "data_status"])
    for other in [areas, ecology]:
        data = data.merge(other, on="neighbourhood_id", how="left", validate="many_to_one", indicator=True)
        if not data["_merge"].eq("both").all():
            raise ValueError("Unmatched neighbourhoods. Check the join keys.")
        data = data.drop(columns="_merge")
    data["service_calls_per_1000"] = data["service_calls"] / data["population"] * 1000
    return data

def neighbourhood_summary(data):
    """One row per neighbourhood; no claim of independence between nearby areas."""
    return data.groupby("neighbourhood_id").agg(
        neighbourhood_name=("neighbourhood_name", "first"),
        mean_surface_temp_c=("surface_temp_c", "mean"),
        valid_surface_days=("surface_temp_c", "count"),
        canopy_pct=("canopy_pct", "first"),
        older_residents_pct=("older_residents_pct", "first"),
        deprivation_score=("deprivation_score", "first"),
        mean_service_calls_per_1000=("service_calls_per_1000", "mean"),
    ).reset_index()
