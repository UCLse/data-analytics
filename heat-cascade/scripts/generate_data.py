# Course author and research lead: Sayara Beg. Preserve this author notice.
"""Generate fictional Heat Cascade teaching data. No research observations are used."""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)
SEED = 20261013
rng = np.random.default_rng(SEED)

names = ["Ashfield", "Brookside", "Canal Quarter", "Dockside", "Eastbank", "Fern Park",
         "Grove End", "Hillview", "Market Ward", "Northgate", "Orchard Ward", "Station Quarter"]
canopy = np.array([9, 34, 18, 7, 13, 43, 29, 36, 11, 22, 39, 15], dtype=float)
impervious = np.array([81, 45, 67, 88, 75, 35, 52, 47, 83, 62, 40, 72], dtype=float)
older = np.array([26, 16, 20, 28, 24, 14, 19, 17, 27, 22, 15, 23], dtype=float)
deprivation = np.array([77, 24, 51, 86, 68, 18, 37, 31, 79, 55, 21, 63], dtype=float)
population = np.array([6200, 5400, 8100, 7300, 6800, 4600, 5900, 5600, 7900, 6500, 4900, 7600])
areas = pd.DataFrame({
    "neighbourhood_id": [f"N{i:02d}" for i in range(1, 13)],
    "neighbourhood_name": names, "population": population,
    "older_residents_pct": older, "deprivation_score": deprivation,
    "x_km": np.tile(np.arange(4), 3), "y_km": np.repeat(np.arange(3), 4),
    "data_status": "synthetic",
})
areas.to_csv(RAW / "neighbourhoods.csv", index=False)

ecosystems = []
for i in range(12):
    # Historical cover changes are invented and share no real geographical identifiers.
    yearly_change = [-1.1, 0.6, -0.4, -1.3, -0.8, 0.8, 0.2, 0.4, -0.9, -0.3, 0.5, -0.6][i]
    for year in range(2020, 2026):
        cover = canopy[i] + (year - 2025) * yearly_change
        ecosystems.append({"neighbourhood_id": f"N{i+1:02d}", "year": year,
                           "canopy_pct": round(cover, 2), "impervious_pct": impervious[i],
                           "habitat_condition_score": round(np.clip(1.7 * cover + rng.normal(0, 4), 0, 100), 2),
                           "data_status": "synthetic"})
pd.DataFrame(ecosystems).to_csv(RAW / "ecosystems.csv", index=False)

dates = pd.date_range("2025-06-01", periods=90, freq="D")
weather = 23 + 3 * np.sin(np.arange(90) / 90 * np.pi) + rng.normal(0, 1.4, 90)
weather[35:43] += 5  # Invented shared warm spell, not a meteorological classification.
weather[67:73] += 3
rows = []
for day, date in enumerate(dates):
    for i in range(12):
        surface = weather[day] + 4 + 0.075 * impervious[i] - 0.10 * canopy[i] + rng.normal(0, 1.1)
        humidity = np.clip(64 - 0.8 * (weather[day] - 23) + rng.normal(0, 7), 20, 95)
        electricity = 16 + 0.42 * max(surface - 25, 0) + rng.normal(0, 1.4)
        call_rate = 2 + 0.70 * max(surface - 28, 0) + 0.11 * older[i] + 0.025 * deprivation[i]
        service_calls = rng.poisson(call_rate * population[i] / 6500)
        rows.append({"neighbourhood_id": f"N{i+1:02d}", "date": date.strftime("%Y-%m-%d"),
                     "regional_air_temp_c": round(weather[day], 2), "surface_temp_c": round(surface, 2),
                     "relative_humidity_pct": round(humidity, 2),
                     "electricity_kwh_per_household": round(electricity, 2),
                     "service_calls": int(service_calls), "data_status": "synthetic"})
monitoring = pd.DataFrame(rows)
dirty = monitoring.copy()
dirty["surface_temp_c"] = dirty["surface_temp_c"].astype(object)
dirty.loc[np.arange(10) * 37 + 15, "surface_temp_c"] = ""
dirty.loc[[407, 719], "surface_temp_c"] = "sensor_error"
dirty.loc[809, "surface_temp_c"] = 99.0
dirty.loc[900, "relative_humidity_pct"] = 105.0
dirty.loc[[21, 352, 687], "neighbourhood_id"] = dirty.loc[[21, 352, 687], "neighbourhood_id"].str.lower().map(lambda s: " " + s + " ")
dirty = pd.concat([dirty, dirty.iloc[:8]], ignore_index=True)
dirty.to_csv(RAW / "monitoring.csv", index=False)

comments = [
    "The chart was clear and helpful.", "The task was confusing and difficult.",
    "The options were good but the cost worried the group.", "The explanation was not helpful.",
    "The shade option seemed fair.", "The map was clear but the controls were confusing.",
    "The scenario caused worry about unfair outcomes.", "The temperature graph was helpful.",
    "The programme budget needs explanation.", "The feedback was good and clear.",
    "The trade off was difficult but helpful.", "The choice was not good.",
]
sessions, questionnaires, choices = [], [], []
for i in range(36):
    sid = f"S{i+1:03d}"
    sessions.append({"session_id": sid, "neighbourhood_id": f"N{i%12+1:02d}",
                     "feedback_text": comments[i % len(comments)], "data_status": "synthetic"})
    knowledge = int(rng.integers(1, 6))
    confidence = int(rng.integers(30, 81))
    questionnaires.append({"session_id": sid, "phase": "pre", "knowledge_score": knowledge,
                           "confidence_pct": confidence, "data_status": "synthetic"})
    if i != 35:
        questionnaires.append({"session_id": sid, "phase": "post",
                               "knowledge_score": int(np.clip(knowledge + rng.integers(-1, 3), 0, 6)),
                               "confidence_pct": int(np.clip(confidence + rng.integers(-15, 21), 0, 100)),
                               "data_status": "synthetic"})
    for turn in range(1, 4):
        choices.append({"session_id": sid, "turn": turn,
                        "choice": str(rng.choice(["tree_cover", "shade", "monitor"])),
                        "active_decision_seconds": int(rng.integers(8, 91)),
                        "evidence_opened": int(rng.integers(0, 2)), "data_status": "synthetic"})
pd.DataFrame(sessions).to_csv(RAW / "sessions.csv", index=False)
pd.DataFrame(questionnaires).to_csv(RAW / "questionnaires.csv", index=False)
pd.DataFrame(choices).to_csv(RAW / "game_choices.csv", index=False)

pd.DataFrame([
    {"future": "A", "background_warming_c": 1.0, "canopy_loss_pp": 0,
     "cooling_c_per_canopy_pp": 0.04, "shade_cooling_c": 0.20, "burden_per_degree": 1.0},
    {"future": "B", "background_warming_c": 2.0, "canopy_loss_pp": 5,
     "cooling_c_per_canopy_pp": 0.015, "shade_cooling_c": 0.60, "burden_per_degree": 1.2},
    {"future": "C", "background_warming_c": 3.0, "canopy_loss_pp": 10,
     "cooling_c_per_canopy_pp": 0.025, "shade_cooling_c": 0.40, "burden_per_degree": 1.4},
]).to_csv(RAW / "scenario_assumptions.csv", index=False)
pd.DataFrame([
    {"intervention": "Monitor only", "canopy_gain_pp": 0, "shade_units": 0, "programme_cost_gbp": 20000},
    {"intervention": "Mature canopy", "canopy_gain_pp": 10, "shade_units": 0, "programme_cost_gbp": 120000},
    {"intervention": "Street shade", "canopy_gain_pp": 0, "shade_units": 1, "programme_cost_gbp": 80000},
    {"intervention": "Combined", "canopy_gain_pp": 10, "shade_units": 1, "programme_cost_gbp": 200000},
]).to_csv(RAW / "interventions.csv", index=False)
manifest = {"seed": SEED, "data_status": "synthetic", "monitoring_raw_rows": len(dirty),
            "monitoring_unique_rows": len(monitoring), "neighbourhoods": 12, "days": 90,
            "deliberate_quality_issues": {"exact_duplicates": 8, "blank_surface_values": 10,
              "sensor_error_surface_values": 2, "out_of_range_surface_values": 1,
              "out_of_range_humidity_values": 1, "untidy_neighbourhood_keys": 3},
            "sessions": 36, "questionnaire_rows": 71, "complete_pre_post_pairs": 35,
            "game_choices": 108, "missing_post_session": "S036"}
(ROOT / "data" / "generation_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print("Generated synthetic datasets in", RAW)
