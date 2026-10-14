# Course author and research lead: Sayara Beg. Preserve this author notice.
"""Worked example for Lesson 09; synthetic teaching data only."""

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

# Step 2.2: Choose one row per neighbourhood
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

# Step 2.3: Compare a few prespecified cluster counts
diagnostics = []
for k in [2, 3, 4]:
    fitted = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X_scaled)
    diagnostics.append({"k": k, "inertia": fitted.inertia_,
                        "silhouette": silhouette_score(X_scaled, fitted.labels_)})
diagnostics = pd.DataFrame(diagnostics)
print(diagnostics.round(3).to_string(index=False))
diagnostics.to_csv(OUTPUT / "09_cluster_diagnostics.csv", index=False)

# Step 2.4: Describe profiles in their original units
model = KMeans(n_clusters=3, n_init=10, random_state=42)
summary["cluster"] = model.fit_predict(X_scaled)
profiles = summary.groupby("cluster")[features].mean()
profiles["neighbourhood_count"] = summary.groupby("cluster").size()
print(profiles.round(2).to_string())
print(summary[["neighbourhood_name", "cluster"]].to_string(index=False))
summary.to_csv(OUTPUT / "09_neighbourhood_clusters.csv", index=False)
profiles.to_csv(OUTPUT / "09_cluster_profiles.csv")

# Step 2.5: Visualise the chosen partition
fig, ax = plt.subplots(figsize=(7, 4))
for cluster, group in summary.groupby("cluster"):
    ax.scatter(group["canopy_pct"], group["mean_surface_temp_c"], label=f"Cluster {cluster}", s=65)
ax.set(xlabel="Fictional canopy cover (%)", ylabel="Mean surface temperature (C)",
       title="Synthetic exploratory profiles, K=3")
ax.legend()
fig.tight_layout()
fig.savefig(OUTPUT / "09_clusters.png", dpi=160)
plt.show()
