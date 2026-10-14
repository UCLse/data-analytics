# Reading the workshop code

## 1. Basic syntax

| Code pattern | Read it as | Purpose |
| --- | --- | --- |
| `temperature = 35` | Temperature receives 35 | Assign a value |
| `temperature == 35` | Temperature equals 35 | Test equality |
| `temperature >= 30` | Temperature is at least 30 | Build a True/False condition |
| `print(value)` | Display value | Make the output visible |
| `import pandas as pd` | Load pandas under the short name pd | Access table operations |
| `DATA / "monitoring.csv"` | Construct the file path | Join a folder and filename |
| `# explanatory text` | Comment | Explain code without executing the comment |
| `for item in items:` | Repeat the indented block for each item | Avoid duplicated operations |
| `def name(input):` | Define a named operation | Create a reusable function |
| `return result` | Supply the result to the caller | Finish a function calculation |

Python treats indentation as structure. Use four spaces inside a loop, function or conditional block. Variable names are case-sensitive. Quotation marks must be straight `'` or `"`, not typographic quotation marks copied from a word processor.

## 2. Reading tables

| Code pattern | Purpose and distinction |
| --- | --- |
| `table.shape` | Read the number of rows and columns; no parentheses because this is an attribute |
| `table.head(3)` | Call a method to display the first three rows |
| `table["column"]` | Select one column as a Series |
| `table[["a", "b"]]` | Select several columns as another table |
| `table.loc[condition]` | Select rows where the condition is True |
| `table.copy()` | Create a working copy |
| `table.dropna(subset=["target"])` | Remove rows with a missing target, not every row with any missing value |
| `table.groupby("area")["value"].mean()` | Group by area, select a value and calculate its mean |
| `table.merge(other, on="key", validate="many_to_one")` | Add related columns while checking the relationship |
| `table.to_csv(path, index=False)` | Save the table without exporting row numbers |

The dot accesses an attribute or method. Chained methods execute from left to right. A variable assignment gives the resulting object a name; later statements can reuse it.

`groupby(...).agg(mean_value=("value", "mean"))` names the output column `mean_value`, takes input column `value` and applies the operation `mean`. The tuple contains two items, written inside parentheses.

`pivot(index="area", columns="year", values="canopy_pct")` reshapes a long table into one row per area with a column for each year. A unique area-year combination is required. Reshaping changes the layout, not the underlying observation level.

## 3. Functions, assertions and compact expressions

An `assert` statement checks a condition and stops when it fails. In this course, assertions protect joins and training/test separation. They are deliberate analytical checks, not a request to remove an inconvenient record.

`sum(table[column] * weight for column, weight in weights.items())` repeats a weighted column calculation for every dictionary entry, then adds the results. The expression inside `sum` is a generator expression. The first encounter can be rewritten as three explicit terms if that makes the calculation easier to explain.

A list comprehension, such as `[name for name in names]`, builds a list using a compact loop. `.to_dict("records")` converts a table into a list of row dictionaries so that a scenario loop can retrieve values by their column names.

`model.fit(X_train, y_train)` learns from training observations. `model.predict(X_test)` produces predictions for reserved inputs. A scikit-learn `Pipeline` connects preprocessing and modelling, ensuring that fitted transformations use training records only.

## 4. Figures and file outputs

`fig, ax = plt.subplots()` creates a Figure container and an Axes plotting region. Methods such as `ax.scatter` draw the data, while `ax.set` supplies units and labels. `fig.tight_layout()` adjusts spacing. `fig.savefig` writes a PNG. `plt.show()` displays the current figure in the notebook.

The workshops use `print` so that the same code remains meaningful in notebooks and scripts. Notebook display formatting can differ without changing the calculation. A script may save figures without displaying them; inspect the PNG files in `outputs`.

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.
