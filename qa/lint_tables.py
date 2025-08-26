#!/usr/bin/env python3
"""Lint OA policy tables against validation rules.
This script loads a YAML file of rules and checks TSV files for compliance.
"""
import argparse
import csv
import sys
import yaml


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
    parser.add_argument("input", help="TSV file to validate")
    parser.add_argument(
        "--rules",
        default="qa/validation_rules.yaml",
        help="Path to YAML rules file",
    )
    args = parser.parse_args()
    rules = load_rules(args.rules)
    print(f"Validating {args.input} using rules from {args.rules}")
    errors = validate_file(args.input, rules)
    if errors:
        print("Errors found:")
        for err in errors:
            print(err)
        sys.exit(1)
    print("No errors found.")


if __name__ == "__main__":
    main()
