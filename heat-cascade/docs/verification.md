# Course verification record

## 1. Reference execution and checks

The 13 worked Python scripts were executed against the supplied synthetic data in the reference environment. Their retained execution logs contain outputs without Python tracebacks. The analytical stack used Python 3.12.14, NumPy 2.3.5, pandas 2.2.3, Matplotlib 3.10.8 and scikit-learn 1.8.0.

The 13 generated guided notebooks contain exactly the same Python operations as their corresponding worked scripts. A syntax-tree comparison checks that parity without relying on formatting or comments. The blank student workbook supplies an independent working structure.

## 2. Expected structural checkpoints

| Checkpoint | Reference result |
| --- | --- |
| Raw monitoring observations | 1,088 rows, including eight exact duplicates |
| Clean monitoring observations | 1,080 neighbourhood-days |
| Valid surface-temperature targets | 1,067 |
| Area and annual ecosystem records | 12 areas and 72 area-year records |
| Regression evaluation groups | Nine training areas and three held-out areas |
| Classification test records | 270 neighbourhood-days |
| Game data | 36 sessions, 108 turns and 35 complete pre/post pairs |
| Baseline scenario comparisons | Nine combinations within the GBP 150,000 budget |

Numerical outputs can differ slightly with different software or platform settings. Cluster numbers are arbitrary labels. Structural discrepancies require investigation before interpretation.

## 3. Verification limits

The reference checks do not include a fresh Codespaces container, a VS Code notebook interface test, a Windows or macOS installation test, or empirical validation of measures and coefficients. The declaration of tested versions records a reference environment; it does not claim compatibility with every future package release.

Local teaching environments should complete Workshop 00 before delivery. Research use requires measurement and validation evidence beyond this course. The machine-readable [verification record](verification.json) records script hashes and notebook parity checks.

Course author and research lead: **Sayara Beg**. Preserve this author credit when reusing or adapting the material.
