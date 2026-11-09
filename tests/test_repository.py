"""Static contracts: this does not evaluate a vision model or human design preference."""
import json
import re
import unittest
from pathlib import Path
from urllib.parse import unquote

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "poster-genome"


class RepositoryTests(unittest.TestCase):
    def test_one_canonical_installable_skill(self):
        self.assertFalse((REPO_ROOT / "SKILL.md").exists(),
                         "A root SKILL.md can shadow the complete nested skill during installation")
        found = list(REPO_ROOT.rglob("SKILL.md"))
        self.assertEqual(found, [SKILL_ROOT / "SKILL.md"])
        for folder in ("references", "genomes", "schemas", "scripts", "examples"):
            self.assertTrue((SKILL_ROOT / folder).is_dir(), folder)

    def test_frontmatter_and_modes(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\n"))
        header = skill.split("---\n", 2)[1]
        self.assertRegex(header, r"(?m)^name: poster-genome$")
        desc = re.search(r"(?m)^description:\s*(.+)$", header)
        self.assertIsNotNone(desc)
        self.assertLessEqual(len(desc.group(1)), 1024)
        self.assertRegex(header, r'(?m)^  version: "0\.2\.0"$')
        for mode in ("LEARN", "CREATE", "REFINE", "LIBRARY"):
            with self.subTest(mode=mode):
                self.assertIn(mode, skill)
        self.assertLessEqual(len(skill.splitlines()), 500)

    def test_all_local_markdown_links_resolve(self):
        # Checks file targets, not remote HTTP links or heading fragments.
        sources = list(REPO_ROOT.rglob("*.md"))
        for source in sources:
            text = source.read_text(encoding="utf-8")
            for match in re.finditer(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text):
                target = match.group(1).split("#", 1)[0].strip()
                if not target or "://" in target or target.startswith(("mailto:", "#")):
                    continue
                candidate = (source.parent / unquote(target)).resolve()
                with self.subTest(file=str(source.relative_to(REPO_ROOT)), target=target):
                    self.assertTrue(candidate.is_relative_to(REPO_ROOT))
                    self.assertTrue(candidate.exists(), f"Broken link: {source}: {target}")

    def test_install_and_capability_boundaries_documented(self):
        readme = (REPO_ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        install = (REPO_ROOT / "docs/INSTALLATION.md").read_text(encoding="utf-8")
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        for text in (readme, install):
            self.assertIn("npx skills add gmchocolate/poster-genome", text)
            self.assertIn("skills/poster-genome", text)
        for term in ("不能", "观察", "推断", "未经", "文字", "工具"):
            with self.subTest(term=term):
                self.assertIn(term, skill)
        evaluation = (REPO_ROOT / "docs/EVALUATION.md").read_text(encoding="utf-8")
        self.assertIn("不会调用任何图像模型", evaluation)
        self.assertIn("尚无可宣称的系统实验结果", evaluation)

    def test_example_and_genome_ids_stay_aligned(self):
        genomes = [json.loads(p.read_text(encoding="utf-8"))
                   for p in sorted((SKILL_ROOT / "genomes").glob("*.json"))]
        ids = [item["id"] for item in genomes]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("cinematic-editorial", ids)
        self.assertIn("bold-type-minimal", ids)
        for item in genomes:
            with self.subTest(id=item["id"]):
                self.assertEqual(item["status"], "active")
                self.assertGreaterEqual(len(item["rules"]["must"]), 3)
                self.assertTrue(item["rules"]["avoid"])

    def test_sample_brief_does_not_fake_generation(self):
        example = json.loads((SKILL_ROOT / "examples/analysis-example.json").read_text(encoding="utf-8"))
        self.assertIn("HYPOTHETICAL", example["reference"]["description"])
        self.assertEqual(example["candidate"]["save_status"], "not-requested")


if __name__ == "__main__":
    unittest.main()
