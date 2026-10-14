# 13. An evidence-led Heat Cascade analytical brief

[Course home](../README.md) | **Indicative time:** 3 hours

**Research question:** How can an analyst produce a reproducible recommendation that remains explicit about its evidence and uncertainty?

**Dataset boundary:** Every supplied observation and parameter is synthetic. The exercises teach analytical practice; their results do not establish Heat Cascade research findings.

## 1. Learning outcomes and vocabulary

- Select a bounded question and appropriate analytical methods.
- Produce reproducible evidence and a concise decision brief.
- Evaluate contribution, limitations and further work.

| Term | Meaning in this workshop |
| --- | --- |
| `provenance` | The origin, status and processing history of evidence. |
| `assurance` | Evidence that an analytical product meets its stated requirements. |
| `boundary condition` | A condition limiting where an interpretation or model applies. |
| `stewardship` | Responsibility for the quality, access and use of data and analytical outputs. |

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

### 2.2. Create an evidence table with explicit denominators

**Why this step matters:** The final brief needs inspectable values behind its charts and statements.

```python
import json
import pandas as pd
from importlib.metadata import version
from course_utils import load_analysis_data, neighbourhood_summary

data = load_analysis_data()
evidence = neighbourhood_summary(data).sort_values("mean_surface_temp_c", ascending=False)
evidence.to_csv(OUTPUT / "13_evidence_table.csv", index=False)
print(evidence.round(2).to_string(index=False))
```

**Expected result:** A 12-row evidence table with means, area attributes and valid-temperature counts.

**Read the result:** The table supports the bounded question but does not replace the quality audit, modelling checks or uncertainty analysis. Every reported comparison must name its level and period.

### 2.3. Record the run environment and data status

**Why this step matters:** A reproducible submission states the analytical stack and confirms that the inputs are synthetic.

```python
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
```

**Expected result:** A JSON run record containing 12 areas, 1,080 area-days, 1,067 valid surface readings and the installed package versions.

**Read the result:** Recording versions helps explain differences between runs. It does not validate the construct, model, data-generation process or final recommendation.

## 3. Independent practice

Complete the [capstone brief](../templates/final-brief.md). Submit one notebook or Python script, a 750 to 1,000-word Markdown brief, three labelled figures, an evidence table and the run record. Use the [assessment brief and rubric](../docs/assessment.md) to check the package.

<details>
<summary>Hint</summary>

Use one descriptive result, one defensible model evaluation and one scenario sensitivity result. A conditional recommendation can be useful even when empirical intervention evidence is absent. Keep all files in your own student-work folder.

</details>

## 4. Interpretation and checkpoint

The conclusion must evaluate contribution, limitations and further work. Explain what the analysis supports, what remains conditional and which next observation would most improve the decision. Include no claims of real-world causal effects or a validated research risk index.

Save the personal notebook in `student_work` and place the written response underneath the relevant output. Commit and push the checkpoint to the student's own fork, then verify it on GitHub. A correct result requires both reproducible code and a defensible interpretation. The [troubleshooting guide](../docs/troubleshooting.md) explains common errors.

The [worked script](../solutions/13-capstone.py) repeats every guided code cell. The [practice answers](../instructor/practice-answers.md) support self-checking after an independent attempt.

[Previous workshop](12-game-and-text.md) | [Assessment brief](../docs/assessment.md)

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.
