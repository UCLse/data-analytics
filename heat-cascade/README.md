# Heat Cascade: Python data analytics from first principles

**Course author and research lead: Sayara Beg.** Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg).

**Attribution required:** credit Sayara Beg when reusing or adapting the teaching materials. Detailed research plans are withheld.

This course introduces Python analytics through educational examples associated with Sayara Beg's Heat Cascade research. The public teaching examples introduce environmental data analysis and decision-making under uncertainty.

**Start with [Workshop 00: account, fork and setup](lessons/00-setup.md).** No prior Python experience is required. Read the Markdown instructions in GitHub, then run the supplied Python blocks in a notebook. The repository view displays code and notebooks; local VS Code or GitHub Codespaces executes the cells.

[Course website](https://uclse.github.io/data-analytics/) | [Fork this course](https://github.com/UCLse/data-analytics/fork)

## 1. Course purpose and working boundary

The course uses an invented city with 12 fictional neighbourhoods. Every supplied record, cost, coefficient and questionnaire score is synthetic. The data deliberately include missing values, invalid readings, untidy keys and duplicates. These defects create a controlled environment for learning data stewardship and analytical assurance.

Heat Cascade is currently unfunded. The generated patterns are teaching examples, not project findings. The priority score is a teaching index. The scenario calculator is a toy model. Real-world research requires compatible observations, reviewed constructs, empirical calibration and independent validation.

The intended student output is a reproducible notebook or script and an evidence-led analytical brief. Each workshop provides the research question, learning outcomes, numbered steps, their purpose, expected results, a practice task and interpretation checks.

## 2. Workshop route

Allow approximately **28 hours**, including setup and the final project. This is an indicative workload, not a credit-bearing module specification. Beginners may need additional practice. Workshops can be delivered weekly or grouped into taught blocks with independent study between them.

| Workshop | Main task | Time | Evidence produced |
| --- | --- | --- | --- |
| [00. Setup](lessons/00-setup.md) | Open a notebook and locate the course files | 1 hour | Working environment |
| [01. Python fundamentals](lessons/01-python-fundamentals.md) | Variables, collections, loops and functions | 2 hours | Explained heat calculation |
| [02. Reading data](lessons/02-reading-data.md) | Load, inspect, filter and save tables | 2 hours | Area extract |
| [03. Data quality](lessons/03-data-quality.md) | Clean measurements and record the rules | 2 hours | Cleaning audit |
| [04. Joining systems](lessons/04-joining-systems.md) | Integrate data layers and measure transitions | 2 hours | Joined table and canopy change |
| [05. Exploration](lessons/05-exploration-visualisation.md) | Compare heat, ecosystem and service patterns | 2 hours | Labelled figures and denominators |
| [06. Teaching index](lessons/06-transparent-index.md) | Combine indicators and vary weights | 2 hours | Index sensitivity table |
| [07. Linear regression](lessons/07-linear-regression.md) | Estimate temperature in held-out areas | 2 hours | Baseline comparison and residuals |
| [08. Classification](lessons/08-classification.md) | Compare a tree and logistic model | 2 hours | Confusion matrix and error trade-offs |
| [09. Clustering](lessons/09-clustering.md) | Explore neighbourhood profiles | 2 hours | Cluster profiles and limitations |
| [10. Time series](lessons/10-time-series.md) | Evaluate one-day-ahead estimates | 2 hours | Chronological prediction comparison |
| [11. Deep uncertainty](lessons/11-deep-uncertainty.md) | Compare programmes across assumptions | 2 hours | Regret and conditional recommendation |
| [12. Game and text data](lessons/12-game-and-text.md) | Link choices, paired scores and comments | 2 hours | Session-level analysis |
| [13. Capstone](lessons/13-capstone.md) | Produce an analytical decision brief | 3 hours | Reproducible final submission |

## 3. How to work through a workshop

1. Read the question and identify the observation level before opening the data.
2. Paste one code block into a new **code cell**, without its Markdown backticks.
3. Run the cell with **Shift+Enter**, then compare the expected result.
4. Add a **text or Markdown cell** explaining what the output supports.
5. Attempt the independent task before reading the hint or worked answer.
6. Save a personal notebook in `student_work`, commit it and push it to the student's own fork. Verify the checkpoint on GitHub.

Run each lesson from top to bottom. A kernel or runtime stores variables in memory; restarting it clears those values. The later workshops prepare their own inputs from the raw files, so a fresh runtime can run any completed workshop independently. Earlier workshops remain essential for understanding those preparation rules.

## 4. Files and supporting material

| Location | Purpose |
| --- | --- |
| `lessons/` | Student-facing GitHub Markdown workshops |
| `data/raw/` | Small synthetic input tables |
| [Data dictionary](docs/data-dictionary.md) | Keys, units, observation levels and limitations |
| [Research alignment](docs/research-alignment.md) | Connection to the Heat Cascade architecture |
| [Code-reading guide](docs/code-reading-guide.md) | Explanation of recurring Python syntax |
| [Troubleshooting](docs/troubleshooting.md) | Error messages and corrective steps |
| `notebooks/01-*.ipynb` to `13-*.ipynb` | Ready-to-run guided notebooks matching the Markdown workshops |
| `notebooks/student_workbook.ipynb` | A blank notebook structure for independent student work |
| `solutions/` | Executable versions of the guided code |
| `templates/` | Final brief and real-data readiness templates |
| `outputs/` | Results created by running the examples |
| `student_work/` | Personal notebooks and selected evidence, committed to the student's fork |
| [Instructor guide](instructor/teaching-guide.md) | Delivery, differentiation and verification |

The public release contains general teaching examples. Private research documents and original historical datasets are withheld. [Teaching sources](docs/sources.md) records the software documentation and verification boundary.

## 5. Outcomes and assessment

By completion, students should be able to prepare related tables, explain their analytical boundaries, compare simple models against baselines and communicate a conditional recommendation under uncertainty. Technical architecture and human behaviour are treated as parts of the same socio-technical system.

The [assessment brief](docs/assessment.md) provides a suggested rubric and submission checklist. Institutional assessment rules take precedence. The final conclusion must evaluate contribution, limitations and further work.

## 6. Running a guided notebook

After completing Workshop 00, open the numbered notebook in local VS Code or the Codespaces browser editor. Select the course kernel and save a personal copy in `student_work`. Commit and push each completed checkpoint to the student's own fork. Each notebook contains the same instructions and Python as its Markdown workshop. Record the independent task and interpretation in the cells at the end.

[Course verification](docs/verification.md) records execution checks and their limits.
