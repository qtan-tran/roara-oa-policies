# Data Folder Guide

## Files
- `raw/`: Direct exports (no manual edits).
- `processed/`: Harmonized tables for analysis.
- `lookups/`: Controlled vocabularies and code lists.

## Update workflow
1. Add raw exports (date-stamped) into `data/raw/`.
2. Use scripts in `analysis/scripts/` to produce normalized tables in `data/processed/`.
3. Validate tables with `qa/lint_tables.py` against `qa/validation_rules.yaml`.
4. Commit both raw and processed files.

For column definitions and allowed values, see `docs/data_dictionary.md`.
