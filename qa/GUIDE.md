# QA Folder Guide

The `qa` folder contains tools and documentation to ensure data quality and compliance with repository standards.

## Purpose

- **Validation rules**: YAML file defining constraints on table columns (e.g., allowed values, required fields, date format) used by the linting script.
- **Linting script**: Python script (`lint_tables.py`) that reads processed tables, applies the validation rules, and reports any errors.
- **Crosswalk tests**: Directory (`crosswalk_tests/`) for unit tests verifying conversions, mappings, and cross-table consistency.

## How to Use

1. Update the validation rules in `validation_rules.yaml` when adding new columns or categories. Keep definitions consistent with `docs/data_dictionary.md` and `data/lookups/controlled_vocab.yaml`.
2. Run `lint_tables.py` on any processed dataset before committing changes. The script will print errors and exit non-zero if validation fails.
3. Add unit tests to `crosswalk_tests/` as necessary to check relationships between tables (e.g., that policy IDs in snippets exist in metadata).
4. Log any updates to validation rules or linting logic in `CHANGELOG.md`.

Maintaining strict QA processes ensures that released data remain accurate, interoperable, and reproducible.
