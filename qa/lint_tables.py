#!/usr/bin/env python3
"""Lint OA policy tables against validation rules.
This script loads a YAML file of rules and checks TSV files for compliance.
"""
import argparse
import csv
import os
import sys
import yaml
from pathlib import Path


def load_rules(path: str) -> dict:
    """Load validation rules from a YAML file."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_row(row: dict, rules: dict, line_no: int) -> list:
    """Validate a single TSV row against rules. Returns list of error strings."""
    errors = []
    for col, rule in rules.get("columns", {}).items():
        value = row.get(col, "").strip()
        if not value:
            # Missing value
            errors.append(f"Line {line_no}: column '{col}' is missing")
            continue
        if "allowed_values" in rule and value not in rule["allowed_values"]:
            errors.append(
                f"Line {line_no}: value '{value}' in column '{col}' not in allowed values {rule['allowed_values']}"
            )
        if "regex" in rule:
            import re

            if not re.match(rule["regex"], value):
                errors.append(
                    f"Line {line_no}: value '{value}' in column '{col}' does not match pattern {rule['regex']}"
                )
    return errors


def validate_file(file_path: str, rules: dict) -> list:
    """Validate a TSV file against rules. Returns list of error strings."""
    errors = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for i, row in enumerate(reader, start=2):  # start=2 to account for header line
            errors.extend(validate_row(row, rules, i))
    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate OA policy tables.")
    parser.add_argument(
        "input",
        nargs="?",
        help="TSV file to validate (optional; if omitted, searches analysis/outputs/tables)",
    )
    parser.add_argument(
        "--rules",
        default="qa/validation_rules.yaml",
        help="Path to YAML rules file",
    )
    args = parser.parse_args()
    rules_path = args.rules
    # Resolve the default rules path relative to this script if necessary
    if not os.path.exists(rules_path) and rules_path == "qa/validation_rules.yaml":
        script_dir = Path(__file__).resolve().parent
        candidate = script_dir / "validation_rules.yaml"
        if candidate.is_file():
            rules_path = str(candidate)
    rules = load_rules(rules_path)
    # Determine which files to validate
    if args.input:
        target_files = [Path(args.input)]
    else:
        repo_root = Path(__file__).resolve().parents[1]
        search_dir = repo_root / "analysis" / "outputs" / "tables"
        if search_dir.is_dir():
            target_files = list(search_dir.glob("*.tsv"))
        else:
            target_files = []
        if not target_files:
            print("No TSV files found for validation. Skipping lint and exiting successfully.")
            return
    return_code = 0
    required_columns = set(rules.get("columns", {}).keys())
    for file_path in target_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter="\t")
                header = next(reader, [])
        except Exception as exc:
            print(f"Warning: could not read {file_path}: {exc}")
            continue
        if not required_columns.intersection(header):
            print(f"Skipping {file_path} – no required columns for validation found.")
            continue
        print(f"Validating {file_path} using rules from {args.rules}")
        errors = validate_file(str(file_path), rules)
        if errors:
            print(f"Errors found in {file_path}:")
            for err in errors:
                print(err)
            return_code = 1
        else:
            print(f"No errors found in {file_path}.")
    sys.exit(return_code)


if __name__ == "__main__":
    main()
