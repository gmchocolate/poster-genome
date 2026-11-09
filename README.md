# Poster Genome 🧬 — Build your own visual taste library

**Stop relying on style adjectives alone. Learn from posters you actually love, save their images privately, and bring those real images into your next creative task.**

Poster Genome is an [Agent Skill](https://agentskills.io/specification), not a standalone image generator. It combines two things:

1. **Genomes:** reusable design principles bundled in the open-source skill.
2. **Personal Taste Library:** each user's private, on-device copies of their chosen style references, with preference annotations.

A capable image agent can look at a reference poster, explain what makes it effective, save it locally with the user's permission, then use **the real reference image** alongside the user's new photo when generating a poster.

[简体中文](README.zh-CN.md) · [Skill instructions](skills/poster-genome/SKILL.md) · [Personal library](skills/poster-genome/references/personal-taste-library.md) · [Contributing](CONTRIBUTING.md)

## Install

~~~bash
npx skills add gmchocolate/poster-genome
~~~

For a global install, add -g. Discover first without installing:

~~~bash
npx skills add gmchocolate/poster-genome --list
~~~

The installable skill lives at skills/poster-genome/. The host must support reading files and images to deliver reference-first creation. Image generation depends on the host's available tools.

## Learn and save visual references locally

Tell a vision-capable agent:

> Analyze this poster deeply. Explain the hierarchy, typography, image treatment, spacing and visual rhythm. Save the actual reference image to my **private local Poster Genome library** with a note about what I like. Do not commit the image to GitHub.

In the installed skill directory, install the optional image-library requirement:

~~~bash
python -m pip install -r requirements-library.txt
~~~

Then explicitly add a reference (the CLI only runs on your own machine or the host executing the agent):

~~~bash
python scripts/taste_library.py add \
  --image "/path/to/inspiration.jpg" \
  --title "Editorial scrapbook" \
  --genome playful-sky-editorial \
  --tag everyday --tag typography \
  --like "expressive bold headline plus handwritten accent" \
  --avoid "original artwork branding and fictitious photo metadata" \
  --rating 5
~~~

Your private library lives at ~/.poster-genome/ by default (or set POSTER_GENOME_HOME). Saved images are re-encoded to strip EXIF metadata, including embedded location data. Uploading an image for one task does **not** automatically authorize persistent saving.

## Create from actual references and your own photos

Example request:

> Use my saved playful scrapbook-style posters to create a new poster featuring **both** photos I uploaded. Keep both children recognizable and preserve their clothing. Do not invent camera data, dates or temperatures.

The agent selects 1–3 locally stored reference images, *views them*, and attaches the reference files and the user's content photos as distinct image roles when the host supports multimodal generation.

Prepare a real-image attachment manifest:

~~~bash
python scripts/taste_library.py prepare \
  --source "/path/to/first-photo.jpg" \
  --source "/path/to/second-photo.jpg" \
  --genome playful-sky-editorial \
  --tag portrait \
  --headline "A day together" \
  --top 2
~~~

This returns separate content_images and style_reference_images with absolute local file paths, taste annotations, preservation rules and explicit attachment requirements.

**A manifest is not a model invocation.** An agent must truly open or attach the image bytes using the host's supported tools. Sending file paths or a verbal style summary as text does not count as image-conditioned creation.

If the host cannot access the images or cannot pass more than one image to generation, the agent must say so and use a supported fallback (such as reference-aware artwork plus deterministic layout of the original photos) without claiming unsupported capabilities.

## Build up your taste over time

~~~bash
python scripts/taste_library.py list
python scripts/taste_library.py select --genome playful-sky-editorial --top 2
python scripts/taste_library.py feedback \
  --id ref-xxxxxxxxxxxxxxxxxxxx \
  --like "asymmetric title" --avoid "fictitious photo details" --rating 5
~~~

Reference retrieval initially uses explicit tags, genome associations and personal ratings; this is *not* image-vector search or model training. Feedback updates the private record only when the user has authorized it.

## Repo vs. personal data

| Item | Location |
| --- | --- |
| Generic design genomes and scripts | Public repo and installed skill |
| Reference image bytes | Private ~/.poster-genome/images/ |
| Taste annotations, ratings and exclusions | Private ~/.poster-genome/index.json |
| New content photos | Wherever the user provided them; never auto-saved as style references |

A cloud-hosted agent that cannot access the user's computer **cannot claim to write to their local computer**. The user must use a local agent, or explicitly choose a separate private persistent environment. This project offers no automatic cloud synchronization.

## Development and tests

Python 3.10+:

~~~bash
python -m pip install -r skills/poster-genome/requirements-dev.txt
python skills/poster-genome/scripts/validate_library.py
python -m unittest discover -s tests -v
~~~

Tests cover script behavior, image metadata stripping, local path protection, documented install packaging and JSON contracts. They do *not* verify the subjective design quality of multimodal output.

See [reference-first workflow](skills/poster-genome/references/reference-first-workflow.md), [installation notes](docs/INSTALLATION.md), [evaluation boundaries](docs/EVALUATION.md) and [contributions](CONTRIBUTING.md).

Original project code and documentation are [MIT licensed](LICENSE). Third-party reference images are not covered by this license; do not redistribute other people's artwork without permission.
