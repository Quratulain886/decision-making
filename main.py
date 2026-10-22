"""
Main entry point for the Decision Tree project.

Usage:
    python main.py

Keep this file in the same directory as:
    - decision-tree-making.py
    - requirements.txt

Note: the original script includes Kaggle-specific dataset paths
(`/kaggle/input` and `/kaggle/working`). Those sections require Kaggle
or suitable changes to the dataset and output paths to run locally.
"""
import runpy
from pathlib import Path

SCRIPT_PATH = Path(__file__).with_name("decision-tree-making.py")

if not SCRIPT_PATH.is_file():
    raise FileNotFoundError(
        f"Required file not found: {SCRIPT_PATH.name}. "
        "Place it beside main.py."
    )

runpy.run_path(str(SCRIPT_PATH), run_name="__main__")
