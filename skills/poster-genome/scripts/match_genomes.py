#!/usr/bin/env python3
"""Rank poster genome compatibility from brief metadata, offline and deterministically."""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WEIGHTS = {"subject": 35, "intent": 25, "mood": 20, "ratio": 20}
KEYS = {"subject": "subjects", "intent": "intents", "mood": "moods", "ratio": "ratios"}


def normalize_ratio(value: str) -> str:
    try:
        a, b = (int(x) for x in str(value).strip().split(":"))
        if min(a, b) <= 0:
            return str(value).strip().lower()
        g = math.gcd(a, b)
        return f"{a // g}:{b // g}"
    except (ValueError, TypeError):
        return str(value).strip().lower()


def load_genomes(directory: Path | None = None) -> list[dict[str, Any]]:
    result = []
    for path in sorted((directory or ROOT / "genomes").glob("*.json")):
        if path.name.startswith("_"):
            continue
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"Cannot read genome {path}: {exc}") from exc
        if document.get("status") == "active":
            result.append(document)
    return result


def rank_genomes(brief: dict[str, Any], genomes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Metadata-based fit heuristic; a high score does not guarantee good graphic design."""
    given = {k: str(brief[k]).strip().lower() for k in WEIGHTS if brief.get(k)}
    if not given:
        raise ValueError("Provide subject, intent, mood and/or ratio.")
    denominator = sum(WEIGHTS[k] for k in given)
    conditions = {str(c).lower() for c in (brief.get("conditions") or [])}
    result = []
    for genome in genomes:
        fit = genome["compatibility"]
        points, matches, mismatches, warnings = 0, [], [], []
        for key, value in given.items():
            candidates = [str(x).strip().lower() for x in fit[KEYS[key]]]
            if key == "ratio":
                value = normalize_ratio(value)
                candidates = [normalize_ratio(x) for x in candidates]
            if value in candidates:
                points += WEIGHTS[key]
                matches.append(f"{key}: {value}")
            else:
                mismatches.append(f"{key}: {value} not listed")
        score = 100 * points / denominator
        required = {x.lower() for x in fit.get("required_conditions", [])}
        avoided = {x.lower() for x in fit.get("avoid_conditions", [])}
        if conditions:
            missing = sorted(required - conditions)
            conflicts = sorted(avoided & conditions)
            if missing:
                score -= 12 * len(missing)
                warnings.append("Required conditions not confirmed: " + ", ".join(missing))
            if conflicts:
                score -= 15 * len(conflicts)
                warnings.append("Style conflicts: " + ", ".join(conflicts))
        elif required:
            warnings.append("Verify source conditions: " + ", ".join(sorted(required)))
        result.append({
            "id": genome["id"], "title": genome["title"], "version": genome["version"],
            "score": round(max(0, score), 1), "summary": genome["summary"],
            "matches": matches, "mismatches": mismatches, "warnings": warnings
        })
    return sorted(result, key=lambda x: (-x["score"], x["id"]))


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, help="JSON creation brief")
    for key in WEIGHTS:
        p.add_argument("--" + key)
    p.add_argument("--conditions", help="Comma-separated, confirmed source-image conditions")
    p.add_argument("--top", type=int, default=3)
    p.add_argument("--library", type=Path, default=ROOT / "genomes")
    p.add_argument("--json", action="store_true", help="Print JSON output")
    args = p.parse_args()
    if args.top < 1:
        p.error("--top must be >= 1")
    try:
        brief = json.loads(args.input.read_text(encoding="utf-8")) if args.input else {}
        for key in WEIGHTS:
            if getattr(args, key) is not None:
                brief[key] = getattr(args, key)
        if args.conditions is not None:
            brief["conditions"] = [v.strip() for v in args.conditions.split(",") if v.strip()]
        ranked = rank_genomes(brief, load_genomes(args.library))[:args.top]
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        p.error(str(exc))
    if args.json:
        print(json.dumps(ranked, ensure_ascii=False, indent=2))
    else:
        if not ranked:
            print("No active genomes found.")
        for index, item in enumerate(ranked, 1):
            print(f"{index}. {item['title']} [{item['id']}@{item['version']}] — {item['score']}/100")
            print(f"   {item['summary']}")
            print(f"   Matched: {', '.join(item['matches']) or 'none'}")
            for warning in item["warnings"]:
                print(f"   Check: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
