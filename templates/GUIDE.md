# Templates Folder Guide

This folder houses reusable templates that support consistent documentation and data formatting across the repository.

## Contents

- **policy_metadata_template.yml** – YAML template for policy metadata (institution, title, year, language, source URL, date accessed, document type, notes, checksums, and supersession info). Copy this file for each policy and fill in the fields.
- **snippet_schema.json** – JSON schema defining the structure of coded snippet files (fields like policy_id, page number, quote, code, note). Use this schema to validate your JSONL snippet files.
- **data_release_checklist.md** – A checklist to verify data quality and documentation before releasing a dataset (includes validation of ISO dates, vocabulary normalization, completeness of metadata and citations).

## Usage Instructions

1. When adding a new policy, copy `policy_metadata_template.yml` and populate it with accurate metadata. Store it in `policies/metadata/` with a descriptive filename.
2. When coding snippets, conform to the `snippet_schema.json` structure. Validate your JSONL files against this schema using appropriate tools before committing.
3. Before any public data release or version tag, follow the steps in `data_release_checklist.md` to ensure all data tables and documentation meet the quality standards defined in `qa/validation_rules.yaml`.

Keep templates up to date with evolving standards and document any changes in the changelog.
