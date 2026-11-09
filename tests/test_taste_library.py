"""User-private visual references, style selection and image-preservation contracts."""
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "poster-genome"
sys.path.insert(0, str(SKILL_ROOT))

from scripts.taste_library import (
    add_reference, choose_references, library_home, load_index,
    main, prepare_creation,
)


class LocalTasteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / "private-taste"
        self.photo = self.root / "photo.jpg"
        Image.new("RGB", (120, 80), (210, 100, 40)).save(self.photo)

    def test_no_files_created_until_explicit_add(self):
        self.assertEqual(load_index(self.home)["references"], [])
        self.assertFalse(self.home.exists())

    def test_saves_a_private_usable_image_and_user_taste(self):
        item = add_reference(
            self.home, self.photo, title="Warm portrait",
            genomes=["playful-sky-editorial"], tags=["baby", "handwriting"],
            likes=["asymmetric title", "handwritten accent"],
            avoids=["fake camera metadata"], rating=5,
        )
        stored = self.home / item["image_path"]
        self.assertTrue(stored.is_file())
        self.assertNotEqual(stored.resolve(), self.photo.resolve())
        with Image.open(stored) as image:
            self.assertEqual(image.size, (120, 80))
        self.assertEqual(item["genome_ids"], ["playful-sky-editorial"])
        self.assertEqual(item["liked_for"], ["asymmetric title", "handwritten accent"])
        self.assertEqual(item["avoid_copying"], ["fake camera metadata"])
        self.assertEqual(load_index(self.home)["references"][0]["rating"], 5)

    def test_deduplicates_and_merges_taste(self):
        original = add_reference(self.home, self.photo, tags=["baby"])
        second = add_reference(self.home, self.photo, tags=["portrait"],
                               likes=["hand-drawn border"], rating=4)
        self.assertEqual(original["id"], second["id"])
        self.assertEqual(len(load_index(self.home)["references"]), 1)
        self.assertEqual(second["tags"], ["baby", "portrait"])
        self.assertEqual(second["rating"], 4)

    def test_strips_exif_including_gps(self):
        photo = self.root / "private.jpg"
        image = Image.new("RGB", (120, 100), "red")
        exif = Image.Exif()
        exif[270] = "PRIVATE-CAMERA-STRING"
        exif[306] = "1999:01:01 00:00:00"
        image.save(photo, exif=exif)
        item = add_reference(self.home, photo)
        raw = (self.home / item["image_path"]).read_bytes()
        self.assertNotIn(b"PRIVATE-CAMERA-STRING", raw)
        with Image.open(io.BytesIO(raw)) as cleaned:
            self.assertFalse(cleaned.getexif())

    def test_refuses_unknown_or_tiny_file(self):
        bad = self.root / "random.txt"
        bad.write_text("not an image")
        with self.assertRaises(ValueError):
            add_reference(self.home, bad)
        tiny = self.root / "tiny.png"
        Image.new("RGB", (3, 3), "blue").save(tiny)
        with self.assertRaises(ValueError):
            add_reference(self.home, tiny)

    def test_reference_selection_uses_matching_genome(self):
        add_reference(self.home, self.photo,
                      genomes=["playful-sky-editorial"], tags=["baby"], rating=5)
        second = self.root / "other.png"
        Image.new("RGB", (90, 90), "green").save(second)
        add_reference(self.home, second,
                      genomes=["cinematic-editorial"], tags=["baby"], rating=5)
        selected = choose_references(self.home, genome="playful-sky-editorial",
                                     tags=["baby"], top=2)
        self.assertEqual(len(selected), 1)
        self.assertIn("images", selected[0]["absolute_path"])
        self.assertEqual(selected[0]["genome_ids"], ["playful-sky-editorial"])

    def test_plan_has_two_distinct_image_roles(self):
        add_reference(self.home, self.photo, genomes=["playful-sky-editorial"],
                      likes=["free-flowing type"], avoids=["copying the logo"])
        source = self.root / "baby.jpg"
        Image.new("RGB", (64, 100), "blue").save(source)
        plan = prepare_creation(self.home, [source, source],
                 genome="playful-sky-editorial", headline="Twins")
        self.assertEqual(len(plan["content_images"]), 2)
        self.assertEqual(len(plan["style_reference_images"]), 1)
        self.assertEqual(plan["style_reference_images"][0]["role"], "style_reference")
        self.assertEqual(plan["content_images"][0]["role"], "content")
        self.assertEqual(plan["headline_exact"], "Twins")
        self.assertTrue(plan["attachment_required"])
        self.assertIn("File paths or text summaries alone", plan["attachment_instruction"])
        self.assertIn("free-flowing type", plan["style_reference_images"][0]["borrow"])
        self.assertIn("copying the logo", plan["style_reference_images"][0]["do_not_copy"])

    def test_no_reference_is_a_warning_not_a_fabricated_asset(self):
        plan = prepare_creation(self.home, [self.photo], genome="missing")
        self.assertEqual(plan["style_reference_images"], [])
        self.assertTrue(plan["warnings"])

    def test_cli_feedback_and_remove(self):
        item = add_reference(self.home, self.photo)
        self.assertEqual(main(["--home", str(self.home), "feedback", "--id", item["id"],
                               "--rating", "5", "--like", "strong hierarchy"]), 0)
        ref = load_index(self.home)["references"][0]
        self.assertEqual(ref["rating"], 5)
        self.assertIn("strong hierarchy", ref["liked_for"])
        self.assertEqual(main(["--home", str(self.home), "remove", "--id", item["id"]]), 0)
        self.assertEqual(load_index(self.home)["references"], [])
        self.assertFalse((self.home / item["image_path"]).exists())

    def test_rejects_tampered_path_outside_private_image_directory(self):
        item = add_reference(self.home, self.photo)
        record = load_index(self.home)
        record["references"][0]["image_path"] = "../elsewhere.jpg"
        (self.home / "index.json").write_text(json.dumps(record))
        with self.assertRaises(ValueError):
            choose_references(self.home)

    def test_negative_or_unrelated_references_are_not_selected(self):
        disliked = add_reference(self.home, self.photo,
                                 genomes=["playful-sky-editorial"],
                                 tags=["portrait"], rating=1)
        self.assertEqual(choose_references(
            self.home, genome="playful-sky-editorial"), [])
        second = self.root / "city.png"
        Image.new("RGB", (90, 90), "green").save(second)
        add_reference(self.home, second,
                      genomes=["playful-sky-editorial"], tags=["street"], rating=5)
        self.assertEqual(choose_references(self.home, tags=["portrait"]), [])
        self.assertEqual(len(choose_references(self.home, tags=["street"])), 1)

    def test_preparation_refuses_non_image_as_content(self):
        bad = self.root / "not-a-photo.txt"
        bad.write_text("hello", encoding="utf-8")
        with self.assertRaises(ValueError):
            prepare_creation(self.home, [bad])

    def test_top_limit(self):
        with self.assertRaises(ValueError):
            choose_references(self.home, top=999)


if __name__ == "__main__":
    unittest.main()
