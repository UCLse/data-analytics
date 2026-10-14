# 09. Exploratory neighbourhood profiles through clustering

[Course home](../README.md) | **Indicative time:** 2 hours

**Research question:** Which synthetic neighbourhoods have similar profiles, and how dependent are the groups on analytical choices?

**Dataset boundary:** Every supplied observation and parameter is synthetic. The exercises teach analytical practice; their results do not establish Heat Cascade research findings.

## 1. Learning outcomes and vocabulary

- Build an area-level feature table and standardise units.
- Fit K-means with explicit settings.
- Compare internal diagnostics and interpret cluster profiles cautiously.

| Term | Meaning in this workshop |
| --- | --- |
| `unsupervised learning` | Pattern discovery without a supplied target label. |
| `standardisation` | Rescaling using the observed mean and standard deviation. |
| `cluster` | A group based on similarity in selected features. |
| `silhouette` | An internal separation diagnostic; it does not validate substantive categories. |

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

### 2.2. Choose one row per neighbourhood

**Why this step matters:** Repeated daily records would give some areas more influence and disguise the intended profiling unit.

```python
import pandas as pd
import matplotlib.pyplot as plt
from course_utils import load_analysis_data, neighbourhood_summary
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

summary = neighbourhood_summary(load_analysis_data())
features = ["mean_surface_temp_c", "canopy_pct", "deprivation_score"]
X = summary[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("Areas and selected features:", X.shape)
```

**Expected result:** `Areas and selected features: (12, 3)`.

**Read the result:** Scaling stops a wide numerical range from dominating distance mechanically. The selected indicators still encode an analytical perspective, and correlated features can overweight a shared dimension. This is descriptive clustering, so no held-out prediction claim is made.

### 2.3. Compare a few prespecified cluster counts

**Why this step matters:** A small comparison demonstrates the role of K without treating a diagnostic as a discovery of natural classes.

```python
diagnostics = []
for k in [2, 3, 4]:
    fitted = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X_scaled)
    diagnostics.append({"k": k, "inertia": fitted.inertia_,
                        "silhouette": silhouette_score(X_scaled, fitted.labels_)})
diagnostics = pd.DataFrame(diagnostics)
print(diagnostics.round(3).to_string(index=False))
diagnostics.to_csv(OUTPUT / "09_cluster_diagnostics.csv", index=False)
```

**Expected result:** Three rows of internal diagnostics. Inertia declines as K increases.

**Read the result:** Lower inertia is expected when more centres are supplied. A high silhouette may reflect the synthetic design. K=3 is used next as a teaching choice, even if another K gives a higher diagnostic score.

### 2.4. Describe profiles in their original units

**Why this step matters:** Cluster labels alone contain no substantive interpretation.

```python
model = KMeans(n_clusters=3, n_init=10, random_state=42)
summary["cluster"] = model.fit_predict(X_scaled)
profiles = summary.groupby("cluster")[features].mean()
profiles["neighbourhood_count"] = summary.groupby("cluster").size()
print(profiles.round(2).to_string())
print(summary[["neighbourhood_name", "cluster"]].to_string(index=False))
summary.to_csv(OUTPUT / "09_neighbourhood_clusters.csv", index=False)
profiles.to_csv(OUTPUT / "09_cluster_profiles.csv")
```

**Expected result:** Three profiles and membership assignments for 12 fictional neighbourhoods.

**Read the result:** Numbers 0, 1 and 2 are arbitrary labels. They can be permuted between runs without changing membership structure. A profile combines input features; it is not a diagnosis of residents or a validated risk category.

### 2.5. Visualise the chosen partition

**Why this step matters:** A plot allows the student to inspect the result alongside the original features.

```python
fig, ax = plt.subplots(figsize=(7, 4))
for cluster, group in summary.groupby("cluster"):
    ax.scatter(group["canopy_pct"], group["mean_surface_temp_c"], label=f"Cluster {cluster}", s=65)
ax.set(xlabel="Fictional canopy cover (%)", ylabel="Mean surface temperature (C)",
       title="Synthetic exploratory profiles, K=3")
ax.legend()
fig.tight_layout()
fig.savefig(OUTPUT / "09_clusters.png", dpi=160)
plt.show()
```

**Expected result:** A scatter plot with three coloured membership groups.

**Read the result:** The plot shows only two of the three clustering inputs. It cannot reveal every distance relation that produced the partition.

## 3. Independent practice

Repeat K=3 using only temperature and canopy. Compare pairwise co-membership, not the numeric label values. Explain whether adding deprivation changes the substantive profile story.

<details>
<summary>Hint</summary>

Two areas are co-members when their assigned labels match. The numeric label attached to that group is arbitrary. A table of area-name memberships can support a manual comparison.

</details>

## 4. Interpretation and checkpoint

Describe one cluster with original units and its number of areas. Explain why the three groups cannot be used as public risk labels. State what additional evidence would support a useful planning typology.

Save the personal notebook in `student_work` and place the written response underneath the relevant output. Commit and push the checkpoint to the student's own fork, then verify it on GitHub. A correct result requires both reproducible code and a defensible interpretation. The [troubleshooting guide](../docs/troubleshooting.md) explains common errors.

The [worked script](../solutions/09-clustering.py) repeats every guided code cell. The [practice answers](../instructor/practice-answers.md) support self-checking after an independent attempt.

[Previous workshop](08-classification.md) | [Next workshop](10-time-series.md)

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.
