# Analysis Folder Guide

This folder contains notebooks, scripts, and outputs used to generate and analyse the OA policy dataset.

## Structure
- `notebooks/`: Jupyter or R Markdown notebooks demonstrating exploratory analyses and reproducible workflows.
- `scripts/`: Command-line scripts (Python or R) for tasks such as text extraction, table building, and validation.
- `outputs/figs/` and `outputs/tables/`: Generated figures and processed tables saved during analysis.

## Usage
To reproduce the results, set up the required environment (see requirements.txt or renv.lock). Use `python analysis/scripts/build_tables.py` to generate normalized tables. Execute notebooks in sequence with parameter cells at the top. Save outputs in the designated outputs subfolders.
