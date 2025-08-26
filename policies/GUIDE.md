# Policies Folder Guide

## Add a new policy
1. Save PDF under `policies/pdf/` as `<COUNTRY>_<SECTOR>_<ID>_<ORG>_<YEAR>_<lang>.pdf`. Example: `DE_RPO_01_TUM_2014_en.pdf`.
2. Extract plain text to `policies/text/` with the same stem and `.txt` extension.
3. Create YAML metadata in `policies/metadata/` with bibliographic fields (policy_id, institution, title, year, language, source_url, date_accessed, document_type, notes, checks).
4. Record checksums of all files in `policies/checksums.sha256` using `sha256sum`.

## Updates
- Do not overwrite existing files; add new versions with updated year and amend metadata with `supersedes`/`superseded_by` where appropriate.
