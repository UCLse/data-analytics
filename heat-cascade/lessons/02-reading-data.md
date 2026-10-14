# 02. Reading and exploring tables with pandas

[Course home](../README.md) | **Indicative time:** 2 hours

**Research question:** Which observations and geographical units are available for a Heat Cascade analysis?

**Dataset boundary:** Every supplied observation and parameter is synthetic. The exercises teach analytical practice; their results do not establish Heat Cascade research findings.

## 1. Learning outcomes and vocabulary

- Read CSV files into a pandas DataFrame.
- Inspect shape, columns, types and missingness.
- Select columns, filter rows and save an extract.

| Term | Meaning in this workshop |
| --- | --- |
| `DataFrame` | A table with named columns and indexed rows. |
| `CSV` | A plain-text table whose values are separated by commas. |
| `method` | An operation attached to an object, called with parentheses. |
| `Boolean filter` | A series of True/False values selecting rows. |

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

### 2.2. Import pandas and read the tables

**Why this step matters:** The analysis begins by inspecting what each file contains.

```python
import pandas as pd

areas = pd.read_csv(DATA / "neighbourhoods.csv")
readings = pd.read_csv(DATA / "monitoring.csv")
print("Area shape:", areas.shape)
print("Monitoring shape:", readings.shape)
print(areas.head(3).to_string(index=False))
```

**Expected result:** 12 rows and 8 columns in the area table; 1,088 rows and 8 columns in monitoring.

**Read the result:** `pd` is a short name for pandas. `DATA / "filename.csv"` constructs a path. `head(3)` shows three rows; it does not change the table.

### 2.3. Inspect the schema

**Why this step matters:** Column types affect which calculations Python can perform safely.

```python
print(readings.columns.tolist())
print(readings.dtypes)
print(readings.isna().sum())
print(areas[["population", "older_residents_pct"]].describe().round(2))
```

**Expected result:** `surface_temp_c` and `date` initially appear as `object`. Ten surface-temperature blanks are counted as missing.

**Read the result:** The surface column contains text errors as well as numeric-looking strings. Its type must be corrected before calculating averages. `count` in `describe` counts non-missing observations.

### 2.4. Select and filter area attributes

**Why this step matters:** A focused extract answers a bounded question without removing the original data.

```python
selected = areas[["neighbourhood_id", "neighbourhood_name", "population", "older_residents_pct"]]
older_areas = selected.loc[selected["older_residents_pct"] >= 24].copy()
older_areas = older_areas.sort_values("older_residents_pct", ascending=False)
print(older_areas.to_string(index=False))
```

**Expected result:** Four fictional neighbourhoods meet the rule: Dockside, Market Ward, Ashfield and Eastbank.

**Read the result:** `>= 24` defines a teaching selection rule. It does not designate an area or its residents as unsafe. `.copy()` creates a separate working table.

### 2.5. Save a useful extract

**Why this step matters:** Saving with explicit column choices and without the pandas index supports reuse.

```python
older_areas.to_csv(OUTPUT / "02_older_area_extract.csv", index=False)
print("Saved rows:", len(older_areas))
```

**Expected result:** `Saved rows: 4`; the CSV appears in `outputs`.

**Read the result:** `index=False` prevents an unnamed row-number column from entering the CSV. Raw input tables remain available for another analysis.

## 3. Independent practice

Create a second extract for neighbourhoods with a population of at least 7,000. Save it as `02_population_extract.csv` and state the number of rows.

<details>
<summary>Hint</summary>

Start from `areas`, use `areas["population"] >= 7000`, and call `to_csv` with `index=False`.

</details>

## 4. Interpretation and checkpoint

State the unit of observation in each table. Explain why the monitoring row count cannot yet be treated as the number of unique observations. Describe the next cleaning step that the `object` surface column requires.

Save the personal notebook in `student_work` and place the written response underneath the relevant output. Commit and push the checkpoint to the student's own fork, then verify it on GitHub. A correct result requires both reproducible code and a defensible interpretation. The [troubleshooting guide](../docs/troubleshooting.md) explains common errors.

The [worked script](../solutions/02-reading-data.py) repeats every guided code cell. The [practice answers](../instructor/practice-answers.md) support self-checking after an independent attempt.

[Previous workshop](01-python-fundamentals.md) | [Next workshop](03-data-quality.md)

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.
