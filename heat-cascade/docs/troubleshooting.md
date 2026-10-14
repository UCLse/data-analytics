# Troubleshooting and recovery

## 1. Locate the problem

Read the last line of the error first. Identify the cell, the missing object or file, and the operation that failed. Correct the cause, rerun that cell and then run the cells below it in order. Restarting the runtime clears variables; it does not correct a wrong filename or a faulty join.

| Message or symptom | Likely cause | Corrective step |
| --- | --- | --- |
| `FileNotFoundError` for the course folder | Fork not cloned locally or notebook opened outside the course folder | Repeat Lesson 00's folder check; confirm `data/raw/neighbourhoods.csv` exists |
| `FileNotFoundError` for a CSV | Misspelt filename or confusion between local and remote file paths | Use the lesson's `DATA / "filename.csv"` path and exact lowercase filename |
| `ModuleNotFoundError` for pandas or sklearn | Packages installed in a different Python environment | Run the installation command using the selected notebook environment, then repeat the import check |
| `ModuleNotFoundError: course_utils` | The workshop's folder cell was skipped | Run the first cell, which adds ROOT to Python's module path |
| Binary compatibility or NumPy import error | Different versions are already loaded or installation is incomplete | Restart the runtime after installation; if necessary create a clean local environment and reinstall requirements |
| `NameError` | An earlier cell was not run, or a name was changed | Run from the first cell and check spelling and capitals |
| `KeyError` | Column name differs from the code | Print `table.columns.tolist()` and compare the exact names |
| `SyntaxError` or `IndentationError` | Missing bracket, copied backticks, curved quote or inconsistent indentation | Copy only the code inside the fence; use straight quotes and four spaces in each block |
| A temperature mean fails | A text-containing column is still an object | Complete Lesson 03's numeric conversion and range checks |
| `MergeError` during a join | The right-hand key is not unique for the declared relationship | Inspect duplicate keys and select the correct year; retain the cardinality check |
| Assertion failure for a join | Some identifiers do not match | Inspect `_merge`, normalise keys and investigate unmatched areas |
| A classifier reports only one class | A filtered training sample removed one outcome class | Inspect class counts; reconsider the sample and validation design before fitting |
| A classification metric is zero | The model identified no positives or made no true-positive prediction | Read class counts and the confusion matrix; zero can be a valid result |
| No figure appears in a script | The environment does not have an interactive display | Open the saved PNG from `outputs`; notebook users should run the plotting cell |
| Results change after editing a cell | Old variables or dependent cells were not recomputed | Restart and run the complete lesson from top to bottom |
| Codespaces setup is still running | Installation has not completed | Wait for the readiness message and inspect the setup log if it fails |
| Notebook uses the wrong kernel | Interpreter and notebook kernel differ | Choose the course `.venv` in the kernel picker and repeat Workshop 00 |
| Codespaces work is missing | A different codespace was opened or the original was deleted | Reopen the original codespace or create a new one from the student's fork containing the last pushed commit |
| `py` or `python3.12` is unavailable | Python 3.12 is not installed or not on the command path | Use institutional installation support or GitHub Codespaces |

### 1.1. Git checkpoints

| Message or symptom | Likely cause | Corrective step |
| --- | --- | --- |
| Personal notebook is absent from GitHub | The file was saved but not committed and pushed | Stage `student_work`, commit, push and check the student's fork |
| GitHub push reports permission denied | The clone points to the lecturer's repository or authentication is missing | Check `git remote -v`; clone the student's fork and sign in through VS Code |
| New files are ignored after syncing an old fork | The fork retains the earlier `student_work` ignore rule | Sync the teaching update and check the course ignore rules before committing |

## 2. Common analytical errors

Replacing missing observations with zero creates false measurements. Dropping every row containing any missing value can remove usable targets unnecessarily. A join that silently multiplies rows changes the effective weight of observations. A random split of repeated area-day records can overstate spatial generalisation.

Standardisation or imputation fitted on all observations before a predictive split leaks information into the evaluation. A threshold tuned on the test set consumes that test set as validation data. Population-normalised rates improve a stated comparison but cannot remove every reporting or service-access bias.

An attractive chart is not assurance. Check units, observation level, denominators, source status and the claim made from the chart. Every generated figure should identify that its data are synthetic.

## 3. Recover a reproducible run

Save the notebook, restart the kernel or runtime, repeat the folder check and run all cells from top to bottom. Confirm the counts against the expected results. If the problem persists, provide the final error line, the failing cell, the Python/package versions and the workshop number to the instructor. Avoid uploading personal or sensitive source records to a public repository.

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.
