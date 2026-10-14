# Course author and research lead: Sayara Beg. Preserve this author notice.
"""Worked example for Lesson 08; synthetic teaching data only."""

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

# Step 2.2: Define the target without reusing it as an input
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

# Step 2.3: Separate groups and fit three approaches
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

# Step 2.4: Read the errors in a confusion matrix
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

# Step 2.5: Inspect thresholds and a learned tree
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
