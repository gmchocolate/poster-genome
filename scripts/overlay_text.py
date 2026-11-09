#!/usr/bin/env python3
"""Add exact text to existing poster artwork. Requires Pillow and a licensed CJK font.

This is a simple compositing fallback, NOT an image generation engine.
"""
from __future__ import annotations
import argparse
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError:
    raise SystemExit("Missing Pillow: python -m pip install -r requirements-render.txt")


def wrap_pixels(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines = []
    for paragraph in text.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        line = ""
        for char in paragraph:
            if font.getlength(line + char) <= max_width:
                line += char
            else:
                if line:
                    lines.append(line)
                line = char
        if line:
            lines.append(line)
    return lines


def choose_font(font_path: str, text: str, initial: int, minimum: int,
                width: int, max_lines: int) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    for size in range(initial, minimum - 1, -2):
        font = ImageFont.truetype(font_path, size)
        lines = wrap_pixels(text, font, width)
        if len(lines) <= max_lines:
            return font, lines
    raise ValueError("Text is too long for the chosen canvas. Shorten it or increase size.")


def draw_lines(draw: ImageDraw.ImageDraw, x: int, y: int, lines: list[str],
               font: ImageFont.FreeTypeFont, fill: str, line_height: int) -> int:
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height
    return y


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--image", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--font", type=Path, required=True, help="Licensed font with the needed glyphs")
    p.add_argument("--headline", required=True)
    p.add_argument("--subtitle", default="")
    p.add_argument("--footer", default="")
    p.add_argument("--width", type=int, default=1080)
    p.add_argument("--height", type=int, default=1350)
    p.add_argument("--focus-x", type=float, default=0.5)
    p.add_argument("--focus-y", type=float, default=0.5)
    p.add_argument("--text-color", default="#FFFFFF")
    p.add_argument("--accent-color", default="#F0B37E")
    a = p.parse_args()
    if not a.image.is_file() or not a.font.is_file():
        p.error("--image and --font must be existing files")
    if min(a.width, a.height) < 300:
        p.error("Dimensions must be at least 300 pixels each")
    if not (0 <= a.focus_x <= 1 and 0 <= a.focus_y <= 1):
        p.error("--focus-x and --focus-y must be between 0 and 1")
    try:
        with Image.open(a.image) as source:
            base = ImageOps.fit(source.convert("RGB"), (a.width, a.height),
                                method=Image.Resampling.LANCZOS,
                                centering=(a.focus_x, a.focus_y)).convert("RGBA")
        gradient = Image.new("RGBA", base.size, (0, 0, 0, 0))
        layer = ImageDraw.Draw(gradient)
        for y in range(int(a.height * .30), a.height):
            t = (y - a.height * .30) / (a.height * .70)
            layer.line((0, y, a.width, y), fill=(0, 0, 0, int(210 * t ** 1.3)))
        base = Image.alpha_composite(base, gradient)
        draw = ImageDraw.Draw(base)
        pad = int(a.width * .075)
        max_width = a.width - pad * 2
        head, hlines = choose_font(str(a.font), a.headline,
            max(32, int(a.height * .086)), 24, max_width, 3)
        sub, slines = (choose_font(str(a.font), a.subtitle,
            max(22, int(a.height * .035)), 18, max_width, 2)
            if a.subtitle else (None, []))
        foot, flines = (choose_font(str(a.font), a.footer,
            max(16, int(a.height * .022)), 14, max_width, 2)
            if a.footer else (None, []))
        hh = int(head.size * 1.22)
        sh = int(sub.size * 1.32) if sub else 0
        fh = int(foot.size * 1.32) if foot else 0
        gap = int(a.height * .018)
        total = len(hlines) * hh
        if sub:
            total += gap + len(slines) * sh
        if foot:
            total += gap * 2 + len(flines) * fh
        start = int(a.height * .94) - total
        if start < a.height * .43:
            raise ValueError("Copy too dense for a lower-third overlay")
        accent_y = start - gap * 2
        draw.rounded_rectangle(
            (pad, accent_y, pad + int(a.width * .075), accent_y + max(5, int(a.height * .006))),
            radius=2, fill=a.accent_color)
        y = draw_lines(draw, pad, start, hlines, head, a.text_color, hh)
        if sub:
            y = draw_lines(draw, pad, y + gap, slines, sub, a.text_color, sh)
        if foot:
            draw_lines(draw, pad, y + gap * 2, flines, foot, a.text_color, fh)
        a.output.parent.mkdir(parents=True, exist_ok=True)
        base.convert("RGB").save(a.output, quality=95)
    except (OSError, ValueError) as exc:
        p.error(str(exc))
    print(f"Wrote {a.output} ({a.width}x{a.height}); visually verify cropping and font glyphs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
