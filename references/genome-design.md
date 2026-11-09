# Genome data model, matching and governance

## What a genome is

A **genome** is an inspectable, reusable *decision system* for layout and art direction. It is not a single giant generation prompt, an unlicensed font collection or a pixel template. Each genome lives in one JSON file under `genomes/`, follows `schemas/genome.schema.json`, and records:

- `compatibility`: suitable subjects/intents/moods/ratios plus input-image requirements and warnings.
- `dna`: compositional grammar, palette roles, type hierarchy, copywriting voice and visual treatment.
- `rules`: mandatory principles, preferences, anti-patterns and adaptation strategies.
- `provenance`: original/reference-derived origin, rights status, confidence and grounded observations.
- `version`, `status` and `tags`: discoverability, controlled evolution and deprecation.

Keep foundational design knowledge in `references/` and specific choices inside individual genomes. A genome does not need to encode every conceivable dimension.

## Selection policy

Classify the source subject and brief. Query `scripts/match_genomes.py` with `--input` or `--subject`, `--intent`, `--mood`, `--ratio`, `--conditions`. Rank compatible candidates using the deterministic weighted matcher, and *then* exercise art-direction judgment. Ranking is **heuristic**, not measured design quality. Never match an inappropriate style merely because it scored highest. Explain what in the input made it fit.

If no genome is suitable, devise an original one-off direction; do not force a weak fit. A manual user choice overrides auto-selection unless it would violate hard requirements.

## Learning, saving and deduplication

1. Produce a candidate ID and summary; compare against existing genomes.
2. If same visual logic exists, propose a minor/major revision or a variant instead of duplicating nearly-identical files.
3. New source references should be described in metadata, not embedded as unlicensed public binary files.
4. **Ask the user to approve saving** before committing or updating shared library records.
5. After approval, create `genomes/<id>.json`, validate JSON/schema, update tests/examples when necessary, and summarize what changed.
6. Use semantic versioning: PATCH spelling/rule clarity without behavioral change; MINOR additive compatible guidance; MAJOR breaking layout/compatibility changes. Do not silently rewrite previous learning.
7. Mark replaced styles as `deprecated`, preserving discoverable history when possible.

## Combining genomes

Blend at most two unless explicitly requested. Select a **base** for composition and an **accent** for a limited characteristic (palette or texture or type). Preserve one dominant hierarchy. When layout systems conflict, choose one rather than mixing grids indiscriminately.

## Privacy and portability

Local learning artifacts are private until the user chooses to share. Keep personal input photos out of the repository by default. Paths in examples are placeholders. Avoid runtime state that only one AI vendor can interpret; JSON and Markdown are the portable truth.
