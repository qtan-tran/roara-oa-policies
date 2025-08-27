# QA Roadmap

This roadmap describes how quality assurance (QA) will be developed and extended in the repository. It is structured into short-, medium-, and long-term actions. Each stage builds on the previous one to ensure data integrity, reproducibility, and scalability.

## Stage 1 – Short Term (0–3 months)

**Goal:** Establish baseline QA for the core policy corpus.

- **File integrity**
  - Ensure all policy PDFs in `/policies/` have SHA256 checksums listed in `checksums.sha256`.
  - Validate that filenames follow the naming convention (`DE_RPO_XX_[Institution]_[Year].pdf`).
- **Metadata validation**
  - Automatic discovery of tables: The linter inspects each table’s header and only validates files containing the expected columns. Unrelated TSV files (e.g., analysis outputs) are skipped to prevent false positives.
  - Define required fields in `/data/lookups/controlled_vocab.yaml`.
  - Extend `qa/lint_tables.py` to check:
    - Harmonized vocabularies (mandate strength, OA type, etc.).
    - Valid date formats (ISO 8601).
    - No empty required fields.
- **Documentation**
  - Expand `GUIDE.md` files in `/policies/` and `/data/` with clear “how to add a new policy” instructions.
  - Add examples of compliant vs. non-compliant entries.

## Stage 2 – Medium Term (3–9 months)

**Goal:** Automate QA and make results reproducible.

- **Automation**
  - Add a GitHub Actions workflow (`.github/workflows/qa.yml`) to run validation scripts automatically on each commit/PR.
  - Integrate continuous markdown linting (e.g., `markdownlint`) to catch formatting issues in docs.
- **Testing**
  - Introduce pytest tests in `/qa/tests/`:
    - `test_schema.py` – metadata fields completeness.
    - `test_crosswalk.py` – coding tables and PDFs alignment.
    - `test_links.py` – repository and URL checks.
- **Change tracking**
  - Require all dataset changes to update `/docs/CHANGELOG.md`.
  - Enforce branch workflows (feature branches for new categories, validation before merge).

## Stage 3 – Long Term (9–18 months)

**Goal:** Extend QA to collaborative and comparative projects.

- **Scaling**
  - Add country-specific subfolders in `/data/` (e.g., `DE/`, `ID/`) with the same schema.
  - Harmonize controlled vocabularies across national corpora.
- **Advanced QA**
  - Create cross-language validation rules for translations in `/snippets/translation/`.
  - Implement metadata completeness scoring (e.g., % of policies with repository names, embargo times, incentives).
- **Transparency**
  - Publish QA reports (auto-generated markdown summaries) in `/reports/qa_status/`.
  - Provide machine-readable exports of validation results (JSON/CSV).

## Milestones

- **M1**: Checksums + validation rules (month 3).
- **M2**: CI workflow and pytest suite (month 6).
- **M3**: First cross-country QA comparison (month 12).
- **M4**: Public QA reports auto-generated (month 18).

This roadmap should be reviewed quarterly and updated as new needs or collaborations arise.
