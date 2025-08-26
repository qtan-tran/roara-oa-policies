# Snippets Folder Guide

This folder contains coded excerpts from policy texts and analyst memos.

## Structure
- `by_policy/`: Contains JSON Lines (`*.jsonl`) snippet files for each policy. Each line is a JSON object with keys: `policy_id`, `page`, `quote`, `code`, and `note`. Additional `anchors.csv` files record page and character offsets to locate the quote in the original PDF.
- `memos/`: Contains analytic memos that synthesise themes across policies.

## Adding snippets
1. Determine the policy ID and create a directory inside `by_policy` if not present (use `policy_id/`).
2. Export snippets as a JSON Lines file named `snippets.jsonl`.
3. Create an `anchors.csv` with columns `page`, `start_char`, `end_char`.
4. Add a short memo in `memos/` if necessary to capture interpretative insights.

Refer to `templates/snippet_schema.json` for the canonical schema. Avoid personally identifying information in quotes. See `templates/policy_metadata_template.yml` for policy-level metadata fields.
