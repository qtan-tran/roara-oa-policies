# Policies Folder Guide

This folder contains the canonical policy documents (PDF) together with their extracted text and metadata.

## Structure

- **pdf/** – source PDFs for each policy. Filenames follow the naming convention described in `docs/naming_conventions.md`.
- **text/** – plain-text extractions of the PDFs. Filenames mirror the PDF stem with a `.txt` extension.
- **metadata/** – YAML files describing each policy (e.g., institution, year, language, notes).
- **checksums.sha256** – a manifest listing the SHA-256 checksum for each PDF. Verify integrity when downloading or updating files.

## Adding a New Policy

1. Name the PDF correctly according to the naming convention. For research performing organisations (RPO), include the institutional abbreviation. For research funding organisations (RFO), use the funder’s name. Include a letter suffix if multiple versions exist (e.g., `01A`, `01B`).
2. Place the PDF in the `pdf/` directory.
3. Add a metadata file under `metadata/` with the same stem and a `.yml` extension. Use existing examples as a template and fill out at least the `policy_id`, `institution`, `title`, `year`, `language`, `document_type`, and `notes` fields. Leave `source_url` blank if the document is local only.
4. Compute and record the checksum in `checksums.sha256`. Run `sha256sum` on the PDF and append the result followed by two spaces and the file name.
5. Generate a plain-text extraction by running the conversion script: `python analysis/scripts/pdf_to_text.py`. Ensure that the resulting `.txt` file appears in `text/`.
6. Update documentation (e.g., `CHANGELOG.md`) to record the addition, and, if applicable, extend the data dictionary or naming conventions.

By following these steps, we maintain a consistent, reproducible corpus of both RPO and RFO policies.
