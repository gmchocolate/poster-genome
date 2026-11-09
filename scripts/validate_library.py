#!/usr/bin/env python3
"""Validate stored genomes and example documents using Draft 2020-12 JSON Schema."""
import json
import re
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    sys.exit("Install dependency first: python -m pip install -r requirements-dev.txt")

ROOT = Path(__file__).resolve().parents[1]


def validate_document(path: Path, schema_path: Path) -> list[str]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        return [
            f"{path.relative_to(ROOT)} [{'/'.join(map(str, e.path)) or 'root'}]: {e.message}"
            for e in sorted(validator.iter_errors(document), key=lambda e: str(e.path))
        ]
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [f"{path}: {exc}"]


def main() -> int:
    issues, seen = [], set()
    genomes = sorted((ROOT / "genomes").glob("*.json"))
    if not genomes:
        issues.append("No genome JSON files found.")
    for path in genomes:
        if path.name.startswith("_"):
            continue
        issues.extend(validate_document(path, ROOT / "schemas/genome.schema.json"))
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
            if doc.get("id") != path.stem:
                issues.append(f"{path.name}: id must match filename")
            if doc.get("id") in seen:
                issues.append(f"{path.name}: duplicate genome id")
            seen.add(doc.get("id"))
            if doc.get("status") == "active" and doc.get("provenance", {}).get("rights") == "restricted":
                issues.append(f"{path.name}: restricted source cannot be active in public library")
            if doc.get("status") == "active" and "REPLACE" in json.dumps(doc):
                issues.append(f"{path.name}: draft placeholders cannot be active")
        except (OSError, json.JSONDecodeError) as exc:
            issues.append(f"{path.name}: {exc}")
    for file, schema in [
        ("examples/brief-example.json", "schemas/brief.schema.json"),
        ("examples/analysis-example.json", "schemas/analysis.schema.json")
    ]:
        issues.extend(validate_document(ROOT / file, ROOT / schema))
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not re.search(r"(?m)^---\s*\nname: poster-genome\s*\n", skill):
        issues.append("SKILL.md: missing/invalid skill name")
    if not re.search(r"(?m)^description:\s*\S", skill):
        issues.append("SKILL.md: missing description")
    if issues:
        print("\n".join("ERROR: " + v for v in issues), file=sys.stderr)
        return 1
    print(f"OK: {len(seen)} genomes, example schemas, and skill metadata validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
