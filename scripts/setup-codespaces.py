"""Prepare the course kernel in the supplied Python 3.12 container.

Course author and research lead: Sayara Beg. Preserve the author notice.
"""
from pathlib import Path
import subprocess
import sys
import venv

REPOSITORY = Path(__file__).resolve().parents[1]
COURSE = REPOSITORY / "heat-cascade"
ENVIRONMENT = COURSE / ".venv"

def main():
    if sys.version_info[:2] != (3, 12):
        raise SystemExit("Python 3.12 is required. Rebuild the course dev container before rerunning setup.")
    if not (ENVIRONMENT / "pyvenv.cfg").is_file():
        venv.EnvBuilder(with_pip=True).create(ENVIRONMENT)
    python = ENVIRONMENT / "bin" / "python"
    if not python.is_file():
        raise SystemExit("The existing .venv is not a Linux course environment. Check it before rebuilding.")
    print("Installing the course packages. Wait for the final readiness message.", flush=True)
    subprocess.run([str(python), "-m", "pip", "install", "-r", str(COURSE / "requirements-notebook.txt")], check=True)
    subprocess.run([str(python), "-m", "ipykernel", "install", "--user", "--name", "heat-cascade", "--display-name", "Heat Cascade (Python 3.12)"], check=True)
    checks = (
        "from importlib.metadata import version; "
        "import numpy, pandas, matplotlib, sklearn, ipykernel; "
        "[print(package, version(package)) for package in ['numpy', 'pandas', 'matplotlib', 'scikit-learn', 'ipykernel']]"
    )
    subprocess.run([str(python), "-c", checks], check=True)
    (COURSE / "student_work").mkdir(exist_ok=True)
    (COURSE / "outputs").mkdir(exist_ok=True)
    print("Heat Cascade environment ready. Select Heat Cascade (Python 3.12) in the notebook kernel picker.", flush=True)

if __name__ == "__main__":
    main()
