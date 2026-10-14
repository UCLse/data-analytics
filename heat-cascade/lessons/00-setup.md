# 00. Setup with VS Code or GitHub Codespaces

[Course home](../README.md) | **Indicative time:** 1 hour

Create a GitHub account and fork the course first. Then choose local VS Code or GitHub Codespaces. Both routes use the same Python exercises and save work to the student's own fork.

## 1. Understand the working boundary

| Route | What is needed | Where Python runs |
| --- | --- | --- |
| Local VS Code | A GitHub fork, Git, VS Code and Python 3.12 | On the student's computer, using a clone of the fork |
| GitHub Codespaces | A GitHub fork, internet access and available Codespaces usage | In a remote environment created from the student's fork |

The repository and course website display instructions. VS Code edits files. A notebook kernel executes Python and stores variables. VS Code needs a separate Python environment to execute the code.

The `heat-cascade` folder contains `data/raw`, `notebooks`, `student_work` and `outputs`. Keep this structure intact. Personal notebook copies belong in `student_work`; generated figures and CSVs belong in `outputs`.

## 2. Create an account and fork the course

### 2.1. Create or sign in to a GitHub account

Create a personal account at [github.com/signup](https://github.com/signup), complete email verification and sign in. An existing personal account can be used.

**Why:** The account owns the student's fork and provides a place to retain completed work between sessions.

### 2.2. Fork the teaching repository

[Course website](https://uclse.github.io/data-analytics/) | [Fork this course](https://github.com/UCLse/data-analytics/fork) 

Open [UCLse/data-analytics](https://github.com/UCLse/data-analytics) and select **Fork**. Choose your own GitHub account as **Owner**, keep the repository name `data-analytics`, retain **Copy the main branch only**, then select **Create fork**. Use your own fork for GitHub Codespaces, or clone your own fork into local VS Code.

**Expected:** GitHub opens a repository at `https://github.com/YOUR-USERNAME/data-analytics`, with a notice that it was forked from the lecturer's teaching repository. `YOUR-USERNAME` means the student's actual GitHub username.

**Why:** A fork gives the student a repository under their own account. Commits and pushes to that fork retain the student's work while the lecturer's teaching copy remains the reference.

Use the student's fork for all remaining setup steps. Preserve Sayara Beg's author notices and citation files when adapting the materials. Public forks are visible to others, so keep personal identifiers, credentials and confidential feedback out of committed work.

## 3. Route A: local VS Code

### 3.1. Install the tools and clone the fork

Install [Git](https://git-scm.com/downloads), [VS Code](https://code.visualstudio.com/) and [Python 3.12](https://www.python.org/downloads/), using institutional support if required. In VS Code's Extensions panel, install the **Python** and **Jupyter** extensions published by Microsoft.

In the student's fork on GitHub, select **Code > Local > HTTPS** and copy its clone URL. The URL must contain the student's username. In VS Code, open the Command Palette, choose **Git: Clone**, paste that URL, select a local folder and open the cloned repository.

The Explorer should show `heat-cascade` inside the repository root. This is a Git-connected local copy of the student's fork. Sign in to GitHub when VS Code requests authentication for pushing work.

Open **Terminal > New Terminal** at the repository root and run:

```bash
cd heat-cascade
```

**Expected:** The terminal is now inside the course folder, which contains `data`, `lessons` and `notebooks`.

**Why:** Cloning retains the Git connection needed to push work back to the student's fork. Entering the course folder puts the package commands beside their requirements file.

### 3.2. Create a dedicated environment

Use the terminal already inside `heat-cascade` from Section 3.1. If a new terminal starts at the repository root, run `cd heat-cascade` first. Then run the commands for the operating system, one line at a time. These are terminal commands, not notebook cells.

**Windows PowerShell:**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-notebook.txt
```

**macOS or Linux:**

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-notebook.txt
```

**Why:** The virtual environment keeps the course packages together. Using its interpreter directly installs packages into that environment without changing terminal activation settings.

**Expected:** Installation completes without an error. If `requirements-notebook.txt` is missing, check that the terminal is inside `heat-cascade`.

### 3.3. Select the interpreter and notebook kernel

Open the Command Palette with **Ctrl+Shift+P**, or **Command+Shift+P** on macOS. Choose **Python: Select Interpreter** and select the course `.venv`. Use **Enter interpreter path** if it is not listed. The Windows path ends in `.venv\Scripts\python.exe`; the macOS or Linux path ends in `.venv/bin/python`.

Open `notebooks/01-python-fundamentals.ipynb`. Choose **Select Kernel** at the top right, then **Python Environments**, and select that same `.venv`. An existing notebook can use a different kernel from the selected script interpreter.

Save a personal copy in `heat-cascade/student_work` before editing. In a terminal already inside `heat-cascade`, that folder is simply `student_work`. Continue with Section 5.

## 4. Route B: GitHub Codespaces in the browser

### 4.1. Create the remote environment

Open the student's own fork at `https://github.com/YOUR-USERNAME/data-analytics`. Select **Code > Codespaces** and create a codespace on `main`. Advanced options allow a machine choice; the small course datasets can be used with a two-core machine.

Check who pays and review the available usage first. Codespaces consumes compute and storage allowances. Stopping a codespace ends its active compute session, while stored files continue to occupy storage until the codespace is deleted.

**Why:** Codespaces supplies Python and a browser-based VS Code editor. No local Python installation is needed. Opening `github.dev` alone does not supply this course runtime.

### 4.2. Wait for automatic setup

The repository configuration installs the Python and Jupyter extensions, creates `heat-cascade/.venv`, installs the course packages and registers **Heat Cascade (Python 3.12)** as a notebook kernel.

Wait until the setup log reports **Heat Cascade environment ready**. The editor may open before installation finishes. A setup error means the environment is not ready.

To rerun setup, open a terminal in the repository root and run:

```bash
python scripts/setup-codespaces.py
```

**Expected:** The readiness message and installed package versions appear. Expand `heat-cascade` in the Explorer to find the materials.

### 4.3. Open and save the notebook

Open `heat-cascade/notebooks/01-python-fundamentals.ipynb`. Choose **Select Kernel** and select **Heat Cascade (Python 3.12)**, possibly under **Jupyter Kernel**. The same environment can be chosen under **Python Environments** using `heat-cascade/.venv/bin/python`.

Save a personal copy in `heat-cascade/student_work`. If the registered kernel is missing, run **Developer: Reload Window** from the Command Palette, then select the kernel again.

### 4.4. Retain work in the fork and stop the codespace

Save with **Ctrl+S**, or **Command+S** on macOS. Saving writes the file inside the codespace. Section 6 explains how to commit and push that file to the student's fork on GitHub.

Complete that commit-and-push check before stopping or deleting the codespace. Work visible in the student's GitHub fork can be recovered in a new codespace; uncommitted files can be lost when the old codespace is deleted.

After pushing, use **Codespaces: Stop Current Codespace**, or stop the environment from [the Codespaces page](https://github.com/codespaces).

## 5. Common checks for both routes

Run this block in a notebook code cell:

```python
from pathlib import Path
import sys
from importlib.metadata import version
import numpy
import pandas
import matplotlib
import sklearn

candidates = [Path.cwd(), Path.cwd() / "heat-cascade", Path.cwd().parent]
ROOT = next((p for p in candidates if (p / "data/raw/neighbourhoods.csv").is_file()), None)
if ROOT is None:
    raise FileNotFoundError("Open the notebook inside heat-cascade/notebooks or heat-cascade/student_work.")
sys.path.insert(0, str(ROOT))
print("Python:", sys.version.split()[0])
print("Interpreter:", sys.executable)
print("Course folder:", ROOT.name)
for package in ["numpy", "pandas", "matplotlib", "scikit-learn"]:
    print(package, version(package))
print("Area file exists:", (ROOT / "data/raw/neighbourhoods.csv").is_file())
```

**Expected:** Python 3.12; NumPy 2.3.5; pandas 2.2.3; Matplotlib 3.10.8; scikit-learn 1.8.0. The interpreter should point into the course `.venv`. The final line must be `Area file exists: True`.

The reference analysis used Python 3.12.14. Another Python 3.12 patch version is normally suitable. Import errors or different packages require an environment check before analysis.

## 6. Save, commit and push work to the student's fork

A save writes a file in the working environment. A commit records a version in Git. A push sends that committed version to the student's fork on GitHub. All three steps are needed for a reliable session checkpoint.

1. Save the personal notebook in `heat-cascade/student_work`.
2. Open VS Code's **Source Control** panel. Review the changed files and stage the notebook using its **+** control.
3. Enter a message such as `Complete Workshop 01`, then select **Commit**.
4. Select **Push** from the Source Control menu, or use **Sync Changes**. Confirm that the target repository belongs to the student.
5. Open the student's fork on GitHub and inspect `heat-cascade/student_work`. The updated notebook and commit message must be visible there.

**Why:** GitHub now retains the work independently of the local computer or the current codespace. Closing the editor after saving alone does not provide that remote checkpoint.

Generated files in `outputs` remain ignored. Copy the small set of figures or CSVs needed as evidence into `student_work/results`, then stage, commit and push those selected files too. Retain the author credit in derivative figures and explanations.

The terminal alternative, run from the repository root, is:

```bash
git status
git add heat-cascade/student_work
git commit -m "Complete Workshop 01"
git push origin main
```

If Git reports `Author identity unknown`, configure this clone before committing:

```bash
git config --local user.name "YOUR-USERNAME"
git config --local user.email "YOUR-GITHUB-NOREPLY-EMAIL"
```

Replace both placeholders. Copy the exact GitHub-provided no-reply address from [GitHub email settings](https://github.com/settings/emails); do not guess its format.

Use the commit and push commands after configuring GitHub authentication in VS Code. `origin` should point to the student's fork; `git remote -v` displays the configured repository URL.

## 7. First checkpoint

Run `print("Heat Cascade setup complete")` in a code cell with **Shift+Enter**, or the cell's Run button. Add a Markdown cell explaining the chosen route, where Python runs and where the inputs live. Save, commit and push the notebook, then confirm it appears in the student's fork.

Run each workshop from top to bottom. Restarting its kernel clears variables, so the folder cell must run again. The [troubleshooting guide](../docs/troubleshooting.md) explains recovery.

Official guidance: [VS Code notebooks](https://code.visualstudio.com/docs/datascience/jupyter-notebooks), [kernel selection](https://code.visualstudio.com/docs/datascience/jupyter-kernel-management), [creating a codespace](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository), [stopping a codespace](https://docs.github.com/en/codespaces/developing-in-a-codespace/stopping-and-starting-a-codespace) [Codespaces usage](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces), [forking a repository](https://docs.github.com/en/pull-requests/how-tos/work-with-forks/fork-a-repo) and [source control](https://docs.github.com/en/codespaces/developing-in-a-codespace/using-source-control-in-your-codespace).

[Next workshop: Python fundamentals](01-python-fundamentals.md)

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.
