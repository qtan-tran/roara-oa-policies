# Naming Conventions

This repository uses consistent naming patterns to ensure clarity and traceability across files and directories.

## Policy files

- **PDFs**: Name as `<COUNTRY>_<SECTOR>_<ID>_<ORG>_<YEAR>_<lang>.pdf`. Example: `DE_RPO_01_TUM_2014_en.pdf`.
- **Extracted text**: Same stem with `.txt` extension. Example: `DE_RPO_01_TUM_2014_en.txt`.
- **Metadata**: YAML files use the same stem with `.yml` extension.
- Use uppercase for country/sector prefixes and underscores between fields. Do not include spaces or special characters.

## Data files

- Raw and processed tables in `/data` should use lowercase names with underscores, and include a date stamp if applicable, e.g., `oa_policy_attributes_raw_2025-08-26.csv`.
- Processed tables use `.tsv` or `.csv` as appropriate, with names like `oa_policy_attributes_normalized.tsv`.
- Controlled vocabularies are stored in YAML files under `data/lookups/`.

## Scripts and notebooks

- Python scripts under `analysis/scripts/` are named with verbs and nouns separated by underscores, e.g., `extract_text.py`.
- Jupyter notebooks under `analysis/notebooks/` use a prefixed number to indicate order, e.g., `01_build_normalized_table.ipynb`.

## Templates

- Templates under `/templates` are named to reflect their purpose, such as `policy_metadata_template.yml`, `snippet_schema.json`, and `data_release_checklist.md`.

Adhering to these conventions simplifies automated processing and ensures that filenames convey their contents and provenance.
