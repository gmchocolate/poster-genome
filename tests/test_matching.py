"""Offline matching and draft behavior tests; no image model is invoked."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "poster-genome"
sys.path.insert(0, str(SKILL_ROOT))

from scripts.match_genomes import load_genomes, normalize_ratio, rank_genomes
from scripts.new_genome import make_draft


class MatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.genomes = load_genomes(SKILL_ROOT / "genomes")

    def test_ratio_normalization(self):
        self.assertEqual(normalize_ratio("1080:1350"), "4:5")

    def test_example_prefers_cinematic(self):
        brief = json.loads((SKILL_ROOT / "examples/brief-example.json").read_text(encoding="utf-8"))
        ranked = rank_genomes(brief, self.genomes)
        self.assertEqual(ranked[0]["id"], "cinematic-editorial")
        self.assertEqual(ranked[0]["score"], 100)

    def test_bold_prefers_announcement(self):
        ranked = rank_genomes({
            "subject": "food", "intent": "announcement", "mood": "bold", "ratio": "1:1"
        }, self.genomes)
        self.assertEqual(ranked[0]["id"], "bold-type-minimal")

    def test_no_query_rejected(self):
        with self.assertRaises(ValueError):
            rank_genomes({}, self.genomes)

    def test_bad_source_conditions_warn(self):
        ranked = rank_genomes({
            "subject": "person", "intent": "editorial", "mood": "cinematic",
            "ratio": "4:5", "conditions": ["busy_background"]
        }, self.genomes)
        cinematic = next(x for x in ranked if x["id"] == "cinematic-editorial")
        self.assertTrue(cinematic["warnings"])
        self.assertLess(cinematic["score"], 100)

    def test_unreviewed_style_is_not_auto_selected(self):
        self.assertNotIn("playful-sky-editorial", [g["id"] for g in self.genomes])

    def test_scaffold_is_draft(self):
        self.assertEqual(make_draft("test-style", "Test", "Description")["status"], "draft")


if __name__ == "__main__":
    unittest.main()
