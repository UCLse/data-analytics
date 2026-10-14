# Teaching sources and verification boundary

## 1. Public teaching material

The course introduces general Python and analytics methods through newly written explanations, synthetic data and worked examples. Private research documents informed the broad teaching context. Their content, work-package plans, application identifiers and bibliography are withheld from this public release.

Previous teaching examples informed the progression from introductory syntax to preparation and modelling. Their original datasets and embedded outputs are not redistributed. No academic citation from a private document is presented as independently verified evidence here.

## 2. Checked primary software documentation

The following official documentation was checked on 13 October 2026. Some pages describe releases newer than the course's tested packages; Workshop 00 identifies the reference versions.

| Documentation | Teaching use |
| --- | --- |
| [Python 3.12 tutorial](https://docs.python.org/3.12/tutorial/) | Variables, collections, loops, functions and virtual environments |
| [pandas tutorials](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html) | Reading, selecting, joining, summarising and reshaping tables |
| [scikit-learn evaluation guide](https://scikit-learn.org/stable/modules/cross_validation.html) | Training and evaluation boundaries |
| [VS Code notebooks](https://code.visualstudio.com/docs/datascience/jupyter-notebooks) | Notebook editing, execution and saving |
| [VS Code kernel management](https://code.visualstudio.com/docs/datascience/jupyter-kernel-management) | Selecting a notebook's Python environment |
| [Forking a repository](https://docs.github.com/en/pull-requests/how-tos/work-with-forks/fork-a-repo) | Creating the student-owned course copy |
| [Codespaces source control](https://docs.github.com/en/codespaces/developing-in-a-codespace/using-source-control-in-your-codespace) | Committing and pushing work to the student's fork |
| [VS Code source control](https://code.visualstudio.com/docs/sourcecontrol/quickstart) | Cloning and retaining local work in Git |
| [Creating a codespace](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository) | Starting the remote course environment |
| [Codespaces usage](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces) | Compute and storage allowances |
| [Python development-container image](https://github.com/devcontainers/images/blob/main/src/python/README.md) | Supported Python 3.12 container variant |

These references support software use. They do not validate the invented coefficients, priority score, questionnaire measures or scenario effects.

## 3. Synthetic-data boundary

The [generator](../scripts/generate_data.py) creates fictional observations. Its equations impose relationships, so successful model fitting partly reflects that construction. A fixed seed supports reproducibility; empirical grounding requires real observations and independent assessment.

Prediction, descriptive profiling and scenario comparison answer different questions. The [readiness template](../templates/real-data-readiness.md) supports general discussion of evidence requirements before real-data use.

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.
