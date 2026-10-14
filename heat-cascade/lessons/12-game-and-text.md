# 12. Game telemetry, paired observations and text limitations

[Course home](../README.md) | **Indicative time:** 2 hours

**Research question:** What can session-level data reveal about choices and recorded scores without attributing a learning effect to the game?

**Dataset boundary:** Every supplied observation and parameter is synthetic. The exercises teach analytical practice; their results do not establish Heat Cascade research findings.

## 1. Learning outcomes and vocabulary

- Join repeated choice records to session-level attributes.
- Match pre/post observations and report incomplete pairs.
- Explain why simple text scoring and response time require contextual interpretation.

| Term | Meaning in this workshop |
| --- | --- |
| `telemetry` | Recorded interaction events, such as a choice or evidence opening. |
| `paired observation` | Two measurements linked to the same session identifier. |
| `attrition` | Loss of a measurement or participant from a repeated-measure comparison. |
| `lexicon` | A predefined collection of words used in a text-scoring rule. |

## 2. Guided analysis

Read the purpose, paste one Python block into a new code cell, then run it with **Shift+Enter**. Compare the output before moving to the next step. Code cells within this lesson share variables and must run in order.

### 2.1. Find the course files

**Why this step matters:** Python needs the course folder before it can read data or save results. Run this cell at the start of every workshop, even in an existing notebook.

```python
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
```

**Expected result:** `Course folder: heat-cascade`. If this fails, return to the folder check in Lesson 00.

**Read the result:** ROOT locates the course; DATA locates the untouched input tables; OUTPUT stores analysis products. The input tables are already present in the fork.

### 2.2. Inspect observation levels and summarise choices

**Why this step matters:** The analysis must avoid treating several choices from one session as independent participants.

```python
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
```

**Expected result:** 36 fictional sessions, 108 choice events and three recorded choices per session.

**Read the result:** The session identifies a single invented participant visit. Active decision seconds exclude pauses by definition in this generated dataset. Faster choices do not necessarily indicate better judgement, and no individual performance diagnosis is supported.

### 2.3. Link pre and post observations with an explicit completeness check

**Why this step matters:** An outer join reveals missing follow-up before a paired difference is calculated.

```python
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
```

**Expected result:** 35 complete pairs and one pre-only record, S036.

**Read the result:** The knowledge score is an invented 0 to 6 quiz count; confidence is a self-report percentage. Neither is an established judgement and decision-making instrument. An immediate pre/post comparison is within-session repeated measurement, and supplies no evidence of durable change or causal game effects.

### 2.4. Compare longitudinal linkage and cross-sectional description

**Why this step matters:** The two views answer different questions and use different denominators.

```python
print("Paired mean knowledge change:", round(complete["knowledge_change"].mean(), 3))
print("All pre-session mean knowledge:", round(pre["knowledge_score"].mean(), 3))
print("All post-session mean knowledge:", round(post["knowledge_score"].mean(), 3))
print("Paired sessions:", len(complete), "All baseline sessions:", len(pre), "All post sessions:", len(post))
print("Choice proportions:")
print(choices["choice"].value_counts(normalize=True).round(3))
```

**Expected result:** A paired mean difference for 35 sessions, separate pre/post summaries with 36 and 35 observations, and event-level choice proportions.

**Read the result:** The paired mean uses the same sessions at both stages. Separate population summaries use different denominators and cannot substitute for matched change. Cross-sectional associations describe the observed population at a defined stage. A longer longitudinal design would require further scheduled observations and retention analysis.

### 2.5. Expose the limitations of a small text rule

**Why this step matters:** A transparent word rule teaches string processing and makes semantic failures inspectable.

```python
positive_words = {"good", "helpful", "clear", "fair"}
negative_words = {"confusing", "difficult", "worry", "unfair"}

def toy_text_score(text):
    words = str(text).lower().replace(".", "").split()
    return sum(word in positive_words for word in words) - sum(word in negative_words for word in words)

sessions["toy_text_score"] = sessions["feedback_text"].map(toy_text_score)
print(sessions[["feedback_text", "toy_text_score"]].head(6).to_string(index=False))
print("Score for 'not helpful':", toy_text_score("not helpful"))
sessions.to_csv(OUTPUT / "12_toy_text_scores.csv", index=False)
```

**Expected result:** `not helpful` receives +1, demonstrating a semantic failure.

**Read the result:** The score ignores negation, context, sarcasm and many word forms. It is a teaching rule, not a validated sentiment measure or a measure of risk perception. Adapting VADER or a language model would still require domain-specific validation against independently coded text.

## 3. Independent practice

Report the incomplete-pair percentage and write a 150-word evaluation plan that could support a stronger learning claim. Include one check on instrument quality and one check on alternative explanations.

<details>
<summary>Hint</summary>

One of 36 baseline sessions lacks a post measurement. Consider item validity, a comparison condition, repeat-testing effects and a later follow-up. Evaluate any sentiment approach against independently coded examples.

</details>

## 4. Interpretation and checkpoint

Give the denominator for each reported measure. Explain why 108 choices are not 108 independent learners. Distinguish confidence from knowledge and knowledge from judgement quality. State why the paired synthetic score difference cannot demonstrate an intervention effect.

Save the personal notebook in `student_work` and place the written response underneath the relevant output. Commit and push the checkpoint to the student's own fork, then verify it on GitHub. A correct result requires both reproducible code and a defensible interpretation. The [troubleshooting guide](../docs/troubleshooting.md) explains common errors.

The [worked script](../solutions/12-game-and-text.py) repeats every guided code cell. The [practice answers](../instructor/practice-answers.md) support self-checking after an independent attempt.

[Previous workshop](11-deep-uncertainty.md) | [Next workshop](13-capstone.md)

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.
