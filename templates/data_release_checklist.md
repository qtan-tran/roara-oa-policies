# Data Release Checklist

Before releasing any dataset or table from this repository, ensure that the following conditions are satisfied:

- **Remove sensitive or restricted content**: Verify that no personally identifiable information (PII), confidential data, or copyrighted material is included.
- **Normalize dates**: All dates must be in ISO format (YYYY-MM-DD). If only year is known, use YYYY; if ongoing, use `Ongoing`.
- **Use controlled vocabularies**: Confirm that categorical fields use the allowed values defined in `docs/data_dictionary.md` and `data/lookups/controlled_vocab.yaml`.
- **Check null values**: Unknown information should be recorded as `Unspecified` rather than left blank.
- **Validate column headers**: Columns should match the names and order defined in the data dictionary. Avoid adding extraneous columns.
- **Ensure completeness**: Metadata fields such as `policy_id`, `institution`, `year`, and `repository` should be populated wherever possible.
- **Update citation metadata**: If releasing a new version, bump the version number in `CITATION.cff` and update the changelog.
- **Run QA scripts**: Execute `qa/lint_tables.py` with the current `validation_rules.yaml` to detect any format or value errors.
- **Document changes**: Record notable modifications or additions in `CHANGELOG.md` with date and version.
- **Tag release**: After checks pass, create a Git tag (e.g., `v1.0.0`) and attach the processed tables as release assets.

Following this checklist helps maintain data quality and reproducibility across the repository.
