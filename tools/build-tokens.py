#!/usr/bin/env python3
"""tokens.css is the source of truth. This derives tokens.json and tailwind.css
from it so the three files cannot drift apart.

Run via `make tokens`. If you edit tokens.json or tailwind.css by hand, the next
make run overwrites you — edit tokens.css instead.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS = ROOT / "tokens" / "tokens.css"

# --- contrast, so the generator can also assert the documented ratios ---------


def _srgb(c: float) -> float:
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _srgb(r) + 0.7152 * _srgb(g) + 0.0722 * _srgb(b)


def ratio(fg: str, bg: str) -> float:
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def parse_block(css: str, selector: str) -> dict[str, str]:
    """Pull `--ul-*: value;` pairs out of the first matching selector block."""
    idx = css.find(selector)
    if idx == -1:
        sys.exit(f"selector not found: {selector}")
    body = css[css.index("{", idx) + 1 : css.index("}", idx)]
    out = {}
    for name, value in re.findall(r"--ul-([a-z0-9-]+)\s*:\s*([^;]+);", body):
        out[name] = value.strip()
    return out


def main() -> None:
    css = CSS.read_text()
    dark = parse_block(css, ":root {")
    light = parse_block(css, ':root[data-theme="light"]')

    # A colour token is anything that resolves to a hex literal.
    def colours(block):
        return {k: v for k, v in block.items() if v.startswith("#")}

    dark_c, light_c = colours(dark), colours(light)

    # --- self-check: every ink token must clear its documented tier ----------
    tiers = {  # token -> (minimum ratio, why)
        "heading": (4.5, "body text"),
        "body": (4.5, "body text"),
        "muted": (4.5, "body text"),
        "faint": (3.0, "large text / UI only"),
        "accent": (4.5, "used as link text"),
        "accent-dim": (3.0, "borders and focus rings"),
        "up": (4.5, "status text"),
        "warn": (4.5, "status text"),
        "down": (4.5, "status text"),
    }
    failures = []
    for mode, block in (("dark", dark_c), ("light", light_c)):
        bg = block.get("bg") or dark_c["bg"]
        for token, (floor, why) in tiers.items():
            if token not in block:
                continue
            r = ratio(block[token], bg)
            if r < floor:
                failures.append(f"{mode}/{token}: {r:.2f}:1 < {floor} ({why})")
    if failures:
        print("token contrast check FAILED:", file=sys.stderr)
        for f in failures:
            print("  " + f, file=sys.stderr)
        sys.exit(1)

    # --- tokens.json ---------------------------------------------------------
    def measured(block):
        bg = block["bg"]
        return {
            k: {"value": v, "contrastOnBg": round(ratio(v, bg), 2)}
            for k, v in block.items()
        }

    doc = {
        "$schema": "https://design-tokens.github.io/community-group/format/",
        "name": "Unchained Labs",
        "source": "https://github.com/Unchained-Labs/branding",
        "note": "Generated from tokens/tokens.css by tools/build-tokens.py. Do not hand-edit.",
        "colour": {"dark": measured(dark_c), "light": measured(light_c)},
        "type": {
            k: dark[k] for k in dark if k.startswith(("font-", "track-", "text-"))
        },
        "space": {k: dark[k] for k in dark if k.startswith("space-")},
        "radius": {k: dark[k] for k in dark if k.startswith("radius")},
    }
    (ROOT / "tokens" / "tokens.json").write_text(json.dumps(doc, indent=2) + "\n")

    # --- tailwind.css (v4 @theme) -------------------------------------------
    lines = [
        "/* Unchained Labs — Tailwind v4 theme block.",
        " * Generated from tokens/tokens.css by tools/build-tokens.py. Do not hand-edit.",
        " * Import AFTER tokens.css so the custom properties resolve.",
        " */",
        '@import "tailwindcss";',
        "",
        "@theme {",
    ]
    for k in dark_c:
        lines.append(f"  --color-ul-{k}: var(--ul-{k});")
    lines += [
        "",
        "  --font-display: var(--ul-font-display);",
        "  --font-body: var(--ul-font-body);",
        "  --font-mono: var(--ul-font-mono);",
        "",
        "  --radius-ul-sm: var(--ul-radius-sm);",
        "  --radius-ul: var(--ul-radius);",
        "  --radius-ul-lg: var(--ul-radius-lg);",
        "}",
    ]
    (ROOT / "tokens" / "tailwind.css").write_text("\n".join(lines) + "\n")

    print(
        f"ok  {len(dark_c)} dark + {len(light_c)} light colour tokens, "
        f"all clear their contrast tier"
    )


if __name__ == "__main__":
    main()
