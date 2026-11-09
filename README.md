# Poster Genome 🧬

**Learn *why* a great poster works. Reuse the principles to create something original.**

Poster Genome is an open-source [Agent Skill](https://agentskills.io/specification) for analyzing reference posters, extracting reusable design rules (called **genomes**), and making new posters from user-provided images. It guides agents through source analysis, a short creative brief, genome selection, composition, real image-tool use and quality review.

It is **not** a hosted poster generator and does not include its own vision or image-generation model.

[简体中文](README.zh-CN.md) · [Skill instructions](skills/poster-genome/SKILL.md) · [Contributing](CONTRIBUTING.md)

## Install

Requires a supported agent and a suitable Node.js version (the current skills CLI documents Node.js **22.20+**).

```bash
npx skills add gmchocolate/poster-genome
```

Choose your target agent interactively. Other options:

```bash
npx skills add gmchocolate/poster-genome --list   # discover without installing
npx skills add gmchocolate/poster-genome -g       # install globally
```

The complete distributable lives at **`skills/poster-genome/`**, including references, schemas, examples, scripts and genomes. This structure lets the installer copy the skill's required files instead of picking up only a repository-root `SKILL.md`. See [installation details](docs/INSTALLATION.md) for verification and limitations.

## Try it

**Learn from a reference image:**

> Use poster-genome to analyze this reference poster. Explain its visual hierarchy, materials, typography and why the design choices may work. Propose reusable rules, but don't copy the composition or save the reference without my permission.

**Create from a photo:**

> Use poster-genome to turn this photo into a 4:5 birthday poster. The exact headline is “生日快乐”. Choose a suitable visual genome and ask only necessary questions.

**Improve a draft:**

> Keep the people, approved copy and aspect ratio; fix the cramped layout and make the headline legible.

### What the skill does

1. **Observe:** inventory visible materials and text, mark what is inferred or unknown.
2. **Explain:** connect specific visual evidence to design decisions and failure cases.
3. **Extract:** propose 3–8 reusable rules in a versioned JSON genome, with user approval before saving.
4. **Adapt:** inspect a new photo, ask at most three consequential questions, match a genome and plan a new composition.
5. **Create and review:** use real tools when available; verify exact text, source identity, cropping and output quality.

A matching score is a heuristic for selecting relevant genomes, **not a validated measure of beauty**.

## Project structure

- [Skill entrypoint](skills/poster-genome/SKILL.md): the agent's authoritative workflow.
- [References](skills/poster-genome/references/analysis-framework.md): focused design and review guidance in Chinese.
- [Genomes](skills/poster-genome/genomes/cinematic-editorial.json): original starter design-rule packs.
- [Schemas](skills/poster-genome/schemas/genome.schema.json): machine-readable contracts.
- [Examples](skills/poster-genome/examples/README.md): synthetic examples, no redistributed third-party posters.
- [Contributor guide](CONTRIBUTING.md): what to include in issues and pull requests.
- [Evaluation boundaries](docs/EVALUATION.md): what automated checks do *not* establish.

## Developer quick start

Python 3.10+:

```bash
python -m pip install -r requirements-dev.txt
python skills/poster-genome/scripts/validate_library.py
python -m unittest discover -s tests -v
python skills/poster-genome/scripts/match_genomes.py --input skills/poster-genome/examples/brief-example.json --top 2
```

For a basic deterministic copy overlay on existing art, `scripts/overlay_text.py` inside the skill accepts a user-provided licensed font and requires Pillow. **This is not an image-generation model.**

## Rights, limits and trust

Analyze visual design methods rather than reproducing distinctive third-party artwork. Do not upload private source photos, fonts or unlicensed posters into this public repository. Actual image analysis and rendering depend on host capabilities. Automated checks test structure, examples and install packaging; they do not prove visual quality or human comprehension gains.

Original code and documentation are under [MIT](LICENSE); third-party media retains its own rights.
