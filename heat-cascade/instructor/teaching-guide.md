# Instructor guide

## 1. Delivery boundary

The course introduces Python through a single synthetic socio-technical system. Its 14 workshops develop data stewardship before modelling and interpretation before recommendations. The suggested workload is 28 hours; additional beginner practice may be needed.

The workload and assessment guidance are teaching suggestions. [Research context](../docs/research-alignment.md) identifies Sayara Beg's authorship and the public-release boundary.

## 2. Recommended delivery pattern

| Teaching block | Workshops | Classroom emphasis | Checkpoint evidence |
| --- | --- | --- | --- |
| Environment and foundations | 00 to 02 | Distinguish storage from execution; explain each line before running it | Working notebook, types and filtered extract |
| Preparation and integration | 03 to 04 | Inspect defects before fixing them; check the unit and join cardinality | Cleaning audit and checked integrated table |
| Exploration and indicator design | 05 to 06 | Label plots; distinguish percentages from percentage points; disclose weights | Exploratory figures and sensitivity comparison |
| Predictive and descriptive models | 07 to 10 | Declare predictor availability; retain baselines; recognise spatial and temporal dependence | Errors, confusion matrix, profile interpretation and forecast comparison |
| Assumptions and behaviour | 11 to 12 | Explain conditional futures and nested observations | Regret table and session-level paired analysis |
| Analytical communication | 13 | Link evidence to a conditional decision | Reproducible brief and independent extension |

Begin each practical with a short demonstration, then allow students to run one cell and explain its output to a partner. Pause when students encounter an error; the final line of the traceback often identifies the immediate problem.

The [code-reading guide](../docs/code-reading-guide.md) supports novices. The generated notebooks contain the same guided code as the Markdown lessons. Independent tasks should be attempted before opening [practice answers](practice-answers.md).

## 3. Differentiation and misconceptions

Students needing more support can explain a working cell before changing one value. More experienced students can investigate a second observation boundary or validation design. Extensions should strengthen interpretation rather than reward additional model complexity.

The major misconceptions concern treating surface temperature as personal exposure, daily rows as independent neighbourhoods, fitted coefficients as causal effects and scenario rankings as unconditional policies. Workshop 12 also distinguishes a score change from evidence that a game caused learning.

The text exercise deliberately shows that a small word list can misread negation. It should not be presented as a validated sentiment instrument. The questionnaire score and confidence measure cannot support psychometric or item-level calibration claims.

## 4. Preparation and reference checks

Complete Workshop 00 in the teaching environment before class. Use local VS Code or GitHub Codespaces and confirm that the notebook kernel uses the declared packages. Provide the approved teaching repository link directly to students. Confirm that students fork that repository and push completed notebooks to their own forks. Read [verification](../docs/verification.md) for reference outputs and verification limits.

From the `heat-cascade` folder, a local interpreter can run a worked script, for example `python solutions/03-data-quality.py`. On Windows, use `.venv\Scripts\python.exe`; on macOS or Linux, use `.venv/bin/python`. Generated CSVs and figures appear in `outputs`.

A fresh Codespaces container and the VS Code notebook interface were not exercised end to end. Institutions should complete Workshop 00 in their chosen delivery environment. The small synthetic analytical examples run without external data services after setup.

## 5. Assessment stewardship

The [assessment brief](../docs/assessment.md) proposes a rubric. The institution must approve its final weighting and requirements before formal use. Students should explain the method and decision boundary even when the code produces the expected numerical answer.

Course release decisions should preserve the source boundary. Private research plans and original historical datasets are withheld from this public teaching release.

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.

## 6. Student repository workflow

Workshop 00 requires a personal GitHub account and fork before either environment is opened. Student notebooks in `student_work` are tracked by Git. Generated outputs remain ignored until selected evidence is copied into `student_work/results`. Students should submit the fork URL and an assessed commit identifier through the approved submission channel.

Public forks retain repository history. Complete the planned public-release history review before inviting students to fork. Confidential feedback and personal assessment identifiers should be handled through the institutional submission system.
