# Course author and research lead: Sayara Beg. Preserve this author notice.
"""Worked example for Lesson 12; synthetic teaching data only."""

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

# Step 2.2: Inspect observation levels and summarise choices
import pandas as pd

sessions = pd.read_csv(DATA / "sessions.csv")
choices = pd.read_csv(DATA / "game_choices.csv")
questionnaires = pd.read_csv(DATA / "questionnaires.csv")
linked = choices.merge(sessions[["session_id", "neighbourhood_id"]], on="session_id", validate="many_to_one")
telemetry = linked.groupby("session_id").agg(
    recorded_choices=("turn", "count"),
    mean_active_seconds=("active_decision_seconds", "mean"),
    evidence_open_fraction=("evidence_opened", "mean"),
)
print("Sessions:", len(sessions), "Choice rows:", len(choices))
print(telemetry.head().round(2))
print(choices["choice"].value_counts())

# Step 2.3: Link pre and post observations with an explicit completeness check
pre = questionnaires.loc[questionnaires["phase"].eq("pre"), ["session_id", "knowledge_score", "confidence_pct"]]
post = questionnaires.loc[questionnaires["phase"].eq("post"), ["session_id", "knowledge_score", "confidence_pct"]]
pairs = pre.merge(post, on="session_id", how="outer", validate="one_to_one",
                  suffixes=("_pre", "_post"), indicator=True)
print(pairs["_merge"].value_counts())
complete = pairs.loc[pairs["_merge"].eq("both")].copy()
complete["knowledge_change"] = complete["knowledge_score_post"] - complete["knowledge_score_pre"]
complete["confidence_change_pp"] = complete["confidence_pct_post"] - complete["confidence_pct_pre"]
complete = complete.merge(telemetry, on="session_id", validate="one_to_one")
print("Complete pairs:", len(complete))
print(complete[["knowledge_change", "confidence_change_pp", "mean_active_seconds"]].describe().round(2))
complete.to_csv(OUTPUT / "12_paired_session_summary.csv", index=False)
pairs.to_csv(OUTPUT / "12_pair_completeness.csv", index=False)

# Step 2.4: Compare longitudinal linkage and cross-sectional description
print("Paired mean knowledge change:", round(complete["knowledge_change"].mean(), 3))
print("All pre-session mean knowledge:", round(pre["knowledge_score"].mean(), 3))
print("All post-session mean knowledge:", round(post["knowledge_score"].mean(), 3))
print("Paired sessions:", len(complete), "All baseline sessions:", len(pre), "All post sessions:", len(post))
print("Choice proportions:")
print(choices["choice"].value_counts(normalize=True).round(3))

# Step 2.5: Expose the limitations of a small text rule
positive_words = {"good", "helpful", "clear", "fair"}
negative_words = {"confusing", "difficult", "worry", "unfair"}

def toy_text_score(text):
    words = str(text).lower().replace(".", "").split()
    return sum(word in positive_words for word in words) - sum(word in negative_words for word in words)

sessions["toy_text_score"] = sessions["feedback_text"].map(toy_text_score)
print(sessions[["feedback_text", "toy_text_score"]].head(6).to_string(index=False))
print("Score for 'not helpful':", toy_text_score("not helpful"))
sessions.to_csv(OUTPUT / "12_toy_text_scores.csv", index=False)
