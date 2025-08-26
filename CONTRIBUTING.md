## Contribution Workflow
- Issues → Branch → Pull Request (PR) with checklists below.
- One policy or one logical change per PR.

## Branch Naming
`feat/policy-<ID>` | `fix/norm-dates` | `data/update-<YYYY-MM-DD>`

## PR Checklist
- [ ] Added/updated policy files under `policies/` (PDF, TXT, YAML).
- [ ] Updated `data/raw/` or `data/processed/` as appropriate.
- [ ] Ran `qa/lint_tables.py` and fixed errors.
- [ ] Updated `CHANGELOG.md`.

## Data Ethics
- Prefer official sources; record provenance in policy metadata.
- Respect copyright; store PDFs under fair-use/official OA links when possible.
