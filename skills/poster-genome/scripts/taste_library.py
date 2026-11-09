#!/usr/bin/env python3
"""Private, reference-first taste library. No network, no image generation."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

try:
    from PIL import Image, ImageOps, UnidentifiedImageError
except ImportError:
    sys.exit("Pillow is required. Install: python -m pip install -r requirements-library.txt")

Image.MAX_IMAGE_PIXELS = 60_000_000
INDEX_VERSION = 1


def library_home(explicit: str | None = None) -> Path:
    value = explicit or os.environ.get("POSTER_GENOME_HOME")
    return Path(value).expanduser().resolve() if value else Path.home() / ".poster-genome"


def _time() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _mkdir_private(folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    if os.name == "posix":
        folder.chmod(0o700)


def _save_json(path: Path, document: dict) -> None:
    _mkdir_private(path.parent)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent,
        prefix=".pending-", suffix=".json", delete=False
    ) as handle:
        pending = Path(handle.name)
        json.dump(document, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    try:
        if os.name == "posix":
            pending.chmod(0o600)
        pending.replace(path)
    finally:
        pending.unlink(missing_ok=True)


def load_index(home: Path) -> dict:
    path = home / "index.json"
    if not path.exists():
        return {"schema_version": INDEX_VERSION, "references": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError(f"Cannot read taste index at {path}: {exc}") from exc
    if not isinstance(data, dict) or data.get("schema_version") != INDEX_VERSION \
            or not isinstance(data.get("references"), list):
        raise ValueError(f"Unsupported taste index format: {path}")
    return data


def _save_index(home: Path, index: dict) -> None:
    _save_json(home / "index.json", index)


def _words(values: list[str] | None, *, lower: bool = False) -> list[str]:
    result: list[str] = []
    for value in values or []:
        for item in value.split(","):
            part = item.strip()
            if lower:
                part = part.lower()
            if part and part not in result:
                result.append(part)
    return result


def _merge(left: list[str], right: list[str]) -> list[str]:
    return left + [item for item in right if item not in left]


def _reencode_without_metadata(path: Path) -> tuple[bytes, str]:
    """Strip EXIF (including GPS), orientation and other embedded metadata."""
    if not path.is_file():
        raise ValueError(f"Reference image not found: {path}")
    try:
        with Image.open(path) as source:
            if source.format not in ("JPEG", "PNG", "WEBP"):
                raise ValueError("Supported reference formats: JPEG, PNG or WebP")
            if source.width < 32 or source.height < 32:
                raise ValueError("Reference image is too small (minimum 32 x 32)")
            picture = ImageOps.exif_transpose(source)
            transparent = picture.mode in ("RGBA", "LA") or "transparency" in picture.info
            out = io.BytesIO()
            if transparent:
                picture.convert("RGBA").save(out, format="PNG")
                return out.getvalue(), ".png"
            picture.convert("RGB").save(out, format="JPEG", quality=94, subsampling=0)
            return out.getvalue(), ".jpg"
    except (OSError, UnidentifiedImageError, Image.DecompressionBombError) as exc:
        raise ValueError(f"Invalid or unsafe reference image: {exc}") from exc


def add_reference(home: Path, image: Path, *, title: str = "",
                  genomes: list[str] | None = None, tags: list[str] | None = None,
                  likes: list[str] | None = None, avoids: list[str] | None = None,
                  rating: int | None = None) -> dict:
    if rating is not None and not 1 <= rating <= 5:
        raise ValueError("rating must be from 1 to 5")
    data, extension = _reencode_without_metadata(image)
    digest = hashlib.sha256(data).hexdigest()
    ref_id = "ref-" + digest[:20]
    relpath = f"images/{digest}{extension}"
    _mkdir_private(home / "images")
    destination = home / relpath
    if not destination.exists():
        with destination.open("xb") as file:
            file.write(data)
        if os.name == "posix":
            destination.chmod(0o600)
    index = load_index(home)
    previous = next((x for x in index["references"] if x["id"] == ref_id), None)
    now = _time()
    if previous:
        for field, values in (
            ("genome_ids", _words(genomes, lower=True)),
            ("tags", _words(tags, lower=True)),
            ("liked_for", _words(likes)),
            ("avoid_copying", _words(avoids)),
        ):
            previous[field] = _merge(previous.get(field, []), values)
        if title:
            previous["title"] = title
        if rating is not None:
            previous["rating"] = rating
        previous["updated_at"] = now
        item = previous
    else:
        item = {
            "id": ref_id,
            "image_path": relpath,
            "title": title.strip() or image.stem,
            "genome_ids": _words(genomes, lower=True),
            "tags": _words(tags, lower=True),
            "liked_for": _words(likes),
            "avoid_copying": _words(avoids),
            "rating": rating if rating is not None else 3,
            "created_at": now,
            "updated_at": now,
        }
        index["references"].append(item)
    _save_index(home, index)
    return item


def _safe_image(home: Path, item: dict) -> Path:
    images = (home / "images").resolve()
    target = (home / item["image_path"]).resolve()
    if not target.is_relative_to(images) or not target.is_file():
        raise ValueError(f"Missing or unsafe local image for {item['id']}")
    return target


def choose_references(home: Path, *, genome: str | None = None,
                      tags: list[str] | None = None, top: int = 2) -> list[dict]:
    if top < 1 or top > 3:
        raise ValueError("top must be between 1 and 3")
    requested = set(_words(tags, lower=True))
    items = []
    for ref in load_index(home)["references"]:
        if genome and genome.lower() not in ref.get("genome_ids", []):
            continue
        match_tags = requested.intersection(ref.get("tags", []))
        score = 10 * len(match_tags) + 2 * ref.get("rating", 3)
        if genome:
            score += 40
        items.append({**ref, "absolute_path": str(_safe_image(home, ref)),
                      "match_tags": sorted(match_tags), "match_score": score})
    items.sort(key=lambda x: (-x["match_score"], x["id"]))
    return items[:top]


def prepare_creation(home: Path, source_paths: list[Path], *,
                     genome: str | None = None, tags: list[str] | None = None,
                     top: int = 2, headline: str = "") -> dict:
    sources = []
    for path in source_paths:
        resolved = path.expanduser().resolve()
        if not resolved.is_file():
            raise ValueError(f"Source photo not found: {path}")
        # Source images are not copied, retouched or sent anywhere by this CLI.
        sources.append({"role": "content", "path": str(resolved),
                        "preserve_identity_and_details": True})
    refs = choose_references(home, genome=genome, tags=tags, top=top)
    return {
        "schema_version": "1.0",
        "workflow": "reference-first",
        "genome_id": genome,
        "headline_exact": headline or None,
        "content_images": sources,
        "style_reference_images": [
            {"role": "style_reference", "id": r["id"],
             "path": r["absolute_path"], "title": r["title"],
             "borrow": r.get("liked_for", []),
             "do_not_copy": r.get("avoid_copying", []),
             "rating": r.get("rating", 3)}
            for r in refs
        ],
        "constraints": [
            "The content_images are the only factual source for people, pets, products and text.",
            "Style reference images influence design language, never identity or factual labels.",
            "Do not copy a reference poster's distinctive overall expression or marks.",
            "Never invent dates, temperatures, camera settings or other metadata.",
            "If exact typography matters, use a dependable text/layout tool.",
        ],
        "attachment_required": True,
        "attachment_instruction": (
            "The agent MUST open or attach each listed style reference image and each "
            "content image as actual image input to the available multimodal creation "
            "tool. File paths or text summaries alone do NOT transmit images. "
            "If the tool cannot receive them, disclose the limitation and do not "
            "claim image-conditioned generation."
        ),
        "warnings": [] if refs else [
            "No matching local visual reference; ask the user to add one or "
            "explicitly allow unreferenced original design."
        ],
    }


def _emit(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", help="Private library root; default ~/.poster-genome")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="Explicitly save a reference image locally")
    add.add_argument("--image", type=Path, required=True)
    add.add_argument("--title", default="")
    add.add_argument("--genome", action="append", default=[])
    add.add_argument("--tag", action="append", default=[])
    add.add_argument("--like", action="append", default=[])
    add.add_argument("--avoid", action="append", default=[])
    add.add_argument("--rating", type=int, choices=range(1, 6))

    sub.add_parser("list", help="List private references")
    selection = sub.add_parser("select", help="Find relevant stored style images")
    selection.add_argument("--genome")
    selection.add_argument("--tag", action="append", default=[])
    selection.add_argument("--top", type=int, default=2)
    creation = sub.add_parser("prepare", help="Create a real-image attachment manifest")
    creation.add_argument("--source", type=Path, action="append", required=True)
    creation.add_argument("--genome")
    creation.add_argument("--tag", action="append", default=[])
    creation.add_argument("--top", type=int, default=2)
    creation.add_argument("--headline", default="")
    creation.add_argument("--out", type=Path, help="Optional local JSON manifest path")
    feedback = sub.add_parser("feedback", help="Update personal taste after review")
    feedback.add_argument("--id", required=True)
    feedback.add_argument("--rating", type=int, choices=range(1, 6))
    feedback.add_argument("--like", action="append", default=[])
    feedback.add_argument("--avoid", action="append", default=[])
    removal = sub.add_parser("remove", help="Delete private reference and image")
    removal.add_argument("--id", required=True)

    args = parser.parse_args(argv)
    home = library_home(args.home)
    try:
        if args.command == "add":
            result = add_reference(home, args.image, title=args.title,
                genomes=args.genome, tags=args.tag, likes=args.like,
                avoids=args.avoid, rating=args.rating)
        elif args.command == "list":
            result = load_index(home)
        elif args.command == "select":
            result = choose_references(home, genome=args.genome,
                tags=args.tag, top=args.top)
        elif args.command == "prepare":
            result = prepare_creation(home, args.source, genome=args.genome,
                tags=args.tag, top=args.top, headline=args.headline)
            if args.out:
                _save_json(args.out.expanduser().resolve(), result)
        elif args.command == "feedback":
            index = load_index(home)
            result = next((r for r in index["references"] if r["id"] == args.id), None)
            if result is None:
                raise ValueError(f"Unknown reference: {args.id}")
            if args.rating is not None:
                result["rating"] = args.rating
            result["liked_for"] = _merge(result.get("liked_for", []), _words(args.like))
            result["avoid_copying"] = _merge(result.get("avoid_copying", []), _words(args.avoid))
            result["updated_at"] = _time()
            _save_index(home, index)
        else:  # remove
            index = load_index(home)
            result = next((r for r in index["references"] if r["id"] == args.id), None)
            if result is None:
                raise ValueError(f"Unknown reference: {args.id}")
            image = _safe_image(home, result)
            index["references"] = [r for r in index["references"] if r["id"] != args.id]
            _save_index(home, index)
            image.unlink(missing_ok=True)
            result = {"removed": args.id}
        _emit(result)
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
