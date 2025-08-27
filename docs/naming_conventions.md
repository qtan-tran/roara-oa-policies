# Naming Conventions for Policy Files

This repository stores policy documents from both research performing organisations (RPOs) and research funding organisations (RFOs). File names follow a structured pattern to allow easy identification and sorting. The general format is:

`<COUNTRY>_<SECTOR>_<ID>_<INSTITUTION>_<YEAR>.pdf`

Where:

- **COUNTRY** is the ISO-3166 alpha-2 code (e.g., `DE` for Germany).
- **SECTOR** indicates whether the policy comes from a research performing organisation (`RPO`) or a research funding organisation (`RFO`).
- **ID** is a unique numeric identifier for the institution, optionally followed by a letter when multiple policies exist for the same institution (e.g., `01A`, `01B`).
- **INSTITUTION** is an abbreviated or hyphenated version of the organisation’s name, using hyphens instead of spaces. Use camel-case or hyphenated segments to preserve readability (e.g., `Max-Planck-Society`, `Fraunhofer`, `Max-Weber-Foundation`).
- **YEAR** is the year the policy was adopted. If unknown, use the document’s publication year or creation date.

The language suffix is omitted for these RFO policies because they are provided in the language distributed by the funder. When multiple language versions are available, append `_de` or `_en` as appropriate.

## Examples

- `DE_RFO_01A_BMBF_2016.pdf` – 2016 open access policy from the German Federal Ministry of Education and Research (BMBF).
- `DE_RFO_04_Max-Planck-Society_2025.pdf` – Max Planck Society open access policy (approximate year 2025).
- `DE_RPO_01_TUM_2014.pdf` – 2014 open access policy from TU München (example for an RPO).

Files should be stored under `policies/pdf/`. Corresponding plain-text extractions are saved under `policies/text/` with the same stem and `.txt` extension.
