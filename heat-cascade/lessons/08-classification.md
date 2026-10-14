# 08. Decision trees, logistic regression and error trade-offs

[Course home](../README.md) | **Indicative time:** 2 hours

**Research question:** Can same-day environmental and area attributes distinguish higher synthetic service demand?

**Dataset boundary:** Every supplied observation and parameter is synthetic. The exercises teach analytical practice; their results do not establish Heat Cascade research findings.

## 1. Learning outcomes and vocabulary

- Define an explicit binary target and avoid target leakage.
- Compare a baseline, a logistic model and a shallow tree.
- Read a confusion matrix and discuss probability thresholds.

| Term | Meaning in this workshop |
| --- | --- |
| `classification` | Prediction of a category, here a teaching binary demand flag. |
| `recall` | The proportion of actual positive cases identified. |
| `precision` | The proportion of positive predictions that are actually positive. |
| `leakage` | Use of information unavailable or prohibited at the stated prediction time. |
| `Brier score` | Mean squared probability error for a binary target; lower is better. |

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

### 2.2. Define the target without reusing it as an input

**Why this step matters:** The teaching label must have a declared meaning and remain separate from its generating count.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from course_utils import load_analysis_data
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (confusion_matrix, accuracy_score, precision_score,
                            recall_score, roc_auc_score, brier_score_loss)

data = load_analysis_data()
data["high_service_demand"] = (data["service_calls"] >= 12).astype(int)
features = ["surface_temp_c", "canopy_pct", "older_residents_pct", "deprivation_score"]
X, y = data[features], data["high_service_demand"]
print("Class counts:")
print(y.value_counts().sort_index())
```

**Expected result:** Both classes are present. Class 1 means at least 12 synthetic calls in one neighbourhood-day.

**Read the result:** Twelve calls is an invented service-planning threshold. It is not a heat-health alert. Calls, calls per 1,000 and the target flag cannot enter X because they reveal the target. This exercise uses contemporaneous measurements, so it is a same-day classification exercise.

### 2.3. Separate groups and fit three approaches

**Why this step matters:** Group separation and training-only preprocessing reduce two common sources of optimistic evaluation.

```python
groups = data["neighbourhood_id"]
splitter = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=42)
train_index, test_index = next(splitter.split(X, y, groups))
X_train, X_test = X.iloc[train_index], X.iloc[test_index]
y_train, y_test = y.iloc[train_index], y.iloc[test_index]
assert set(groups.iloc[train_index]).isdisjoint(set(groups.iloc[test_index]))
models = {
    "Majority baseline": Pipeline([("imputer", SimpleImputer(strategy="median")),
                                   ("classifier", DummyClassifier(strategy="most_frequent"))]),
    "Logistic regression": Pipeline([("imputer", SimpleImputer(strategy="median")),
                                     ("scale", StandardScaler()),
                                     ("classifier", LogisticRegression(max_iter=2000, random_state=42))]),
    "Shallow tree": Pipeline([("imputer", SimpleImputer(strategy="median")),
                              ("classifier", DecisionTreeClassifier(max_depth=3, min_samples_leaf=30, random_state=42))]),
}
rows = []
for name, classifier in models.items():
    classifier.fit(X_train, y_train)
    predictions = classifier.predict(X_test)
    probability = classifier.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, probability) if y_test.nunique() == 2 else np.nan
    rows.append({"model": name, "accuracy": accuracy_score(y_test, predictions),
                 "precision": precision_score(y_test, predictions, zero_division=0),
                 "recall": recall_score(y_test, predictions, zero_division=0),
                 "ROC_AUC": auc, "Brier": brier_score_loss(y_test, probability)})
metrics = pd.DataFrame(rows)
print(metrics.round(3).to_string(index=False))
metrics.to_csv(OUTPUT / "08_classification_metrics.csv", index=False)
```

**Expected result:** Three metric rows. A majority-only rule can have reasonable accuracy while missing all positives.

**Read the result:** `scale` learns the mean and spread only from training records. AUC measures ranking, not probability calibration. The Brier score evaluates probability error but cannot establish calibration by itself. With three held-out areas, subgroup and spatial performance remain uncertain.

### 2.4. Read the errors in a confusion matrix

**Why this step matters:** False positives and false negatives imply different operational costs.

```python
logistic = models["Logistic regression"]
predictions = logistic.predict(X_test)
matrix = confusion_matrix(y_test, predictions, labels=[0, 1])
print("Rows = actual [0,1]; columns = predicted [0,1]")
print(matrix)
fig, ax = plt.subplots(figsize=(5, 4))
ax.imshow(matrix, cmap="Blues")
for row in range(2):
    for column in range(2):
        ax.text(column, row, str(matrix[row, column]), ha="center", va="center", color="black",
                bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "none"})
ax.set(xticks=[0, 1], yticks=[0, 1], xlabel="Predicted class", ylabel="Actual class",
       title="Synthetic same-day demand classification")
fig.tight_layout()
fig.savefig(OUTPUT / "08_confusion_matrix.png", dpi=160)
plt.show()
```

**Expected result:** A 2 by 2 matrix whose four counts sum to the 270 test neighbourhood-days.

**Read the result:** Top left is a true negative; top right is a false positive; bottom left is a false negative; bottom right is a true positive. The class label refers to aggregate demand, never to a person.

### 2.5. Inspect thresholds and a learned tree

**Why this step matters:** Predefined threshold comparisons show the trade-off; the tree exposes learned partitions.

```python
probability = logistic.predict_proba(X_test)[:, 1]
for threshold in [0.3, 0.5, 0.7]:
    flagged = (probability >= threshold).astype(int)
    print(threshold, "precision", round(precision_score(y_test, flagged, zero_division=0), 3),
          "recall", round(recall_score(y_test, flagged, zero_division=0), 3))
tree = models["Shallow tree"].named_steps["classifier"]
fig, ax = plt.subplots(figsize=(12, 6))
plot_tree(tree, feature_names=features, class_names=["Lower calls", "Higher calls"],
          filled=True, rounded=True, ax=ax, fontsize=8)
ax.set_title("Synthetic shallow tree; learned splits are not policy thresholds")
fig.tight_layout()
fig.savefig(OUTPUT / "08_tree.png", dpi=160)
plt.show()
```

**Expected result:** Three threshold comparisons and a shallow decision-tree diagram.

**Read the result:** Lowering the flag threshold usually increases recall and can reduce precision. These are demonstration contrasts. Any operational threshold needs a separate validation set and an explicit cost or utility model, followed by untouched test evaluation.

## 3. Independent practice

Calculate how many false negatives occur at each of the three thresholds. Recommend a threshold-selection process for a service planner with limited capacity, without declaring an operational winner from this test set.

<details>
<summary>Hint</summary>

For each threshold use `confusion_matrix(y_test, flagged, labels=[0, 1])[1, 0]`. Selection needs demand costs, capacity constraints and separate validation data.

</details>

## 4. Interpretation and checkpoint

Explain why a model with higher accuracy can have lower operational value. Identify one predictor that would leak the target. Describe the difference between a learned decision-tree split and an empirically established intervention threshold.

Save the personal notebook in `student_work` and place the written response underneath the relevant output. Commit and push the checkpoint to the student's own fork, then verify it on GitHub. A correct result requires both reproducible code and a defensible interpretation. The [troubleshooting guide](../docs/troubleshooting.md) explains common errors.

The [worked script](../solutions/08-classification.py) repeats every guided code cell. The [practice answers](../instructor/practice-answers.md) support self-checking after an independent attempt.

[Previous workshop](07-linear-regression.md) | [Next workshop](09-clustering.md)

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.
