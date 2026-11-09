# Examples

`brief-example.json` is a fictional creation brief. Try:

```bash
python scripts/match_genomes.py --input examples/brief-example.json --top 2
```

`analysis-example.json` is a **hypothetical teaching example**: no real poster was inspected, and it does not constitute evidence for a genuine poster.

The optional photo/text compositing fallback adds accurate words to existing art. Supply your own picture and a **licensed** TrueType/OpenType font with Chinese glyphs:

```bash
python -m pip install -r requirements-render.txt
python scripts/overlay_text.py --image ./photo.jpg --font /path/to/CJK-font.ttf --headline "秋日物语" --subtitle "留住此刻" --output ./output/poster.png
```

This simple layout is **not** the same as AI-based art direction and cannot preserve a full graphical style by itself. Verify crops, text accuracy and glyphs visually.
