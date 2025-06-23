#  Biofilm Analysis Pipeline (Python)

This is a Python reimplementation of the Julia-based multi-well biofilm analysis pipeline developed in the Bridges Lab. It supports:

-  Automatic batch analysis of `.tif` time-lapse image stacks
-  Overlay generation (normalized, masked, registered) 
-  Parameter tuning via Jupyter Notebook
-  CLI support for flexible usage
-  Biomass quantification over time


##  Installation

```bash
uv venv
source .venv/bin/activate
uv pip install -r pyproject.toml

