# Assessment brief: a reproducible Heat Cascade decision analysis

## 1. Assessment boundary and deliverables

The final task asks for a defensible analytical brief using the supplied synthetic system. The assessment evaluates reproducibility, interpretation and assurance. It cannot establish student competence in operating a real environmental intelligence platform.

The suggested submission identifies the student's fork URL and the commit to assess, alongside a notebook or Python script, a 750 to 1,000 word Markdown brief, three labelled figures, an evidence table and the run record. The word range and rubric are teaching proposals; the approved institutional specification governs any formal assessment.

Use the [final-brief template](../templates/final-brief.md). Identify the observation level, population boundary and data coverage before choosing an analytical method. Include one independently completed extension beyond the guided examples.

## 2. Analytical requirements

The submission must show a cleaning audit, a checked join and an exploratory comparison. Its chosen model or scenario analysis must include a meaningful comparator and explain the validation or assumption boundary. A prediction exercise needs appropriate training and test separation; a scenario exercise needs disclosed assumptions and a sensitivity comparison.

Every figure needs a title, units and a clear denominator where relevant. Each reported result needs an interpretation explaining what it supports. Copied outputs without reasoning do not meet the analytical requirement.

The independent extension may compare errors between held-out areas, examine a different index component, compare an equity-oriented scenario objective or investigate missing pre/post records. The brief must explain why the extension changes the decision discussion.

## 3. Suggested rubric

| Criterion | Weight | Evidence required for a strong submission |
| --- | --- | --- |
| Research question and system boundary | 15% | Clear decision question, observation level, system dependencies and measurable output |
| Data preparation and stewardship | 20% | Reproducible cleaning, checked keys, units, join cardinality and missingness consequences |
| Analytical method and validation | 25% | Justified method, suitable comparator, correct separation or scenario boundary, meaningful independent extension |
| Interpretation and uncertainty | 25% | Correct units and denominators; conditional conclusions; explicit limitations, assumptions and operational consequences |
| Reproducibility and communication | 15% | Clean execution, labelled artefacts, package versions, readable code and concise evidence-led prose |

Syntax success alone is insufficient. A low model error cannot compensate for target leakage, an inappropriate inference boundary or invented empirical claims. Grade descriptors and penalty rules require institutional approval before use.

## 4. Submission checks

1. Restart the kernel and run the final notebook from top to bottom.
2. Recover every required input from the original course files.
3. Confirm that no absolute path depends on the author's computer.
4. Record software versions and the number of observations used in each analysis.
5. Identify the synthetic status of the data in the brief and figure captions.
6. Explain the comparator, independent extension and remaining uncertainty.
7. Include a conclusion subsection covering contribution, limitations and further work.
8. Commit and push the notebook and selected evidence to the student's fork; identify the assessed commit in the submission.
9. Follow the institution's current academic integrity and AI-use disclosure requirements.

The exercise offers a starting assessment structure. Any use with real data requires the [real-data readiness review](../templates/real-data-readiness.md).

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.
