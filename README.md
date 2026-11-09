# Poster Genome 🧬

[![Validate Poster Genome](https://github.com/gmchocolate/poster-genome/actions/workflows/validate.yml/badge.svg)](https://github.com/gmchocolate/poster-genome/actions/workflows/validate.yml)

**Learn the design DNA of great posters. Create original posters from your own images.**

[简体中文](README.zh-CN.md) · [Agent Skills specification](https://agentskills.io/specification)

Poster Genome is an open-source **Agent Skill**, not a hosted image-generation service. Give a vision-capable AI a poster reference and it will analyze its visual language, explain the design decisions, and propose a reusable, structured **genome**. Give it an image to create with and it will ask only the essential questions, match a genome, plan an original composition, generate using available image tools, and review the result.

> **Design principles, not pixel cloning.** Respect authors' rights, brand assets, people and exact user-provided text.

## Workflows

| Mode | Input | Output |
| --- | --- | --- |
| **Learn** | Reference poster image | Deep visual analysis, evidence/uncertainty, proposed reusable genome |
| **Create** | Source photo/image and optional brief | Focused questions, ranked genomes, composition plan and poster when an image tool is available |
| **Refine** | Draft poster and feedback | Quality review, focused iteration, deliverables |
| **Library** | JSON genomes | Validated, searchable, versioned style knowledge |

## Quick start

Install as an [Agent Skill](https://agentskills.io/specification) in a compatible AI agent. For a portable local installation:

```bash
git clone https://github.com/gmchocolate/poster-genome.git
mkdir -p ~/.agents/skills
ln -s "$(pwd)/poster-genome" ~/.agents/skills/poster-genome
```

On platforms that use a different skills directory, copy or link the whole `poster-genome` directory there. Restart or rescan the agent if required.

**Prompts:**
- "Use poster-genome to learn the design DNA of this poster. Show the analysis before saving a reusable genome."
- "Use poster-genome to create a 4:5 poster with this photo. Ask only what you need to know."
- "Use poster-genome to review this poster, explain its weaknesses and improve it without changing my exact headline."

**Library tools (Python 3.10+):**
```bash
python scripts/match_genomes.py --subject person --intent editorial --mood cinematic --ratio 4:5
python -m pip install -r requirements-dev.txt
python scripts/validate_library.py
python -m unittest discover -s tests -v
```

The match CLI is deterministic and works offline. For a simple exact-text composition over existing artwork, use `scripts/overlay_text.py` with Pillow and a licensed font (see [examples](examples/README.md)). Vision analysis and image generation rely on capabilities of the host agent. The included starter genomes are **illustrative original examples**, not extracted from copyrighted work. See [Chinese guide](README.zh-CN.md) for the complete design philosophy and workflows.

## Project map

- [SKILL.md](SKILL.md): concise skill instructions and routing
- [references/](references/): learn, selection, conversation, creation, QA and provenance rules
- [genomes/](genomes/): independent, versionable visual genomes
- [schemas/](schemas/): machine-readable JSON contracts
- [scripts/](scripts/): genome matching and validation
- [examples/](examples/): example input and outputs
- [CONTRIBUTING.md](CONTRIBUTING.md): contribution rules

## Capabilities & limits

Poster Genome is **model/tool agnostic**. It does not ship a vision model, image renderer, font files or secret API keys. The agent must actually have image inspection/generation tools to complete visual steps; otherwise it returns a specific composition specification instead of claiming an image was generated. Exact text and logos should be overlaid in a deterministic editing step when supported. User approval is required before adding a learned genome to the shared library.

## License

MIT for repository code and documentation, except any separately licensed contributed references; contributors must have rights to the material they submit. See [LICENSE](LICENSE).
