#!/usr/bin/env python3
"""Scaffold a draft genome. Only run after the user approves a library write."""
import argparse
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def make_draft(gid: str, title: str, summary: str) -> dict:
    return {
        "schema_version": "1.0", "id": gid, "version": "0.1.0", "title": title,
        "summary": summary, "status": "draft", "tags": ["draft"],
        "compatibility": {
            "subjects": ["person"], "intents": ["editorial"], "moods": ["elegant"],
            "ratios": ["4:5"], "required_conditions": [], "avoid_conditions": []
        },
        "dna": {
            "principle": "REPLACE: causal, transferable design principle",
            "composition": {
                "layout": "REPLACE", "focal_strategy": "REPLACE",
                "text_zones": ["REPLACE"], "negative_space": "REPLACE", "depth": "REPLACE"
            },
            "visual": {
                "palette": ["#151515", "#FFFFFF"], "contrast": "REPLACE",
                "lighting": "REPLACE", "texture": "REPLACE",
                "image_treatment": "REPLACE", "elements": []
            },
            "typography": {
                "headline_style": "REPLACE", "body_style": "REPLACE",
                "hierarchy": "REPLACE", "max_text_density": "low"
            },
            "copywriting": {
                "voice": "REPLACE", "headline_guideline": "REPLACE", "cta_guideline": "REPLACE"
            }
        },
        "rules": {
            "must": ["REPLACE: first rule", "REPLACE: second rule", "REPLACE: third rule"],
            "prefer": [], "avoid": ["REPLACE: anti-pattern"],
            "adaptation": ["REPLACE: how to adapt to source and ratio"]
        },
        "provenance": {
            "kind": "original", "rights": "unknown", "source_url": None,
            "confidence": 0.0, "observations": [], "inferences": [],
            "notes": "DRAFT: verify rights and replace all placeholders before activation."
        },
        "created_at": date.today().isoformat()
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--id", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--summary", required=True)
    p.add_argument("--output", type=Path)
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", a.id):
        p.error("--id must be lowercase and hyphen-separated")
    content = json.dumps(make_draft(a.id, a.title, a.summary), ensure_ascii=False, indent=2) + "\n"
    if a.dry_run:
        print(content)
        return 0
    path = a.output or ROOT / "genomes" / f"{a.id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8") as stream:
            stream.write(content)
    except FileExistsError:
        p.error(f"Refusing to overwrite {path}")
    print(f"Created draft {path}; review and replace all placeholders before activation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
