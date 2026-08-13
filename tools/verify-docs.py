#!/usr/bin/env python3
"""Checks every contrast ratio *written in the docs* against the measured value.

This exists because the numbers in brand/palette.md were wrong twice while this
repo was being written — estimated by eye, then asserted in a table as if
measured. A brand doc that states a wrong ratio is worse than one that states
none, because the wrong one gets trusted. So the docs are now tested.

Scans tokens/tokens.css and brand/*.md for `#RRGGBB ... N.NN:1` claims and any
markdown table cell of the form `| N.NN:1 |` adjacent to a `--ul-token`, then
recomputes each against the right ground.

Run via `make verify-docs`. Runs in CI.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOKENS = json.loads((ROOT / "tokens" / "tokens.json").read_text())["colour"]

TOL = 0.015  # measured values are printed to 2dp


def _srgb(c: float) -> float:
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def ratio(fg: str, bg: str) -> float:
    def lum(h):
        h = h.lstrip("#")
        r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
        return 0.2126 * _srgb(r) + 0.7152 * _srgb(g) + 0.0722 * _srgb(b)

    a, b = lum(fg), lum(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


DARK_BG = TOKENS["dark"]["bg"]["value"]
LIGHT_BG = TOKENS["light"]["bg"]["value"]

problems: list[str] = []
checked = 0


def check(where: str, fg: str, bg: str, claimed: float, label: str) -> None:
    global checked
    checked += 1
    actual = ratio(fg, bg)
    if abs(actual - claimed) > TOL:
        problems.append(
            f"{where}: {label} claimed {claimed:.2f}:1, measured {actual:.2f}:1"
        )


# --- tokens.css inline comments: `--ul-x: #HEX;  /* N.NN:1 */` -----------------
css = (ROOT / "tokens" / "tokens.css").read_text()
light_start = css.find(':root[data-theme="light"]')
for m in re.finditer(
    r"--ul-([a-z0-9-]+)\s*:\s*(#[0-9A-Fa-f]{6})\s*;[^\n]*?([0-9]+\.[0-9]{2}):1", css
):
    token, hexv, claimed = m.group(1), m.group(2), float(m.group(3))
    # `on-accent` is measured against the accent fill, not the page ground.
    in_light = m.start() > light_start >= 0
    block = TOKENS["light"] if in_light else TOKENS["dark"]
    bg = block["accent"]["value"] if token == "on-accent" else block["bg"]["value"]
    check("tokens.css", hexv, bg, claimed, f"--ul-{token}")

# --- brand/*.md tables: rows containing a --ul-token, a hex, and ratios --------
for md in sorted((ROOT / "brand").glob("*.md")):
    for line in md.read_text().splitlines():
        if "`--ul-" not in line or ":1" not in line:
            continue
        hexes = re.findall(r"`(#[0-9A-Fa-f]{6})`", line)
        ratios = [float(x) for x in re.findall(r"([0-9]+\.[0-9]{2}):1", line)]
        token_m = re.search(r"`--ul-([a-z0-9-]+)`", line)
        if not hexes or not ratios or not token_m:
            continue
        token = token_m.group(1)
        # Status table carries dark hex + dark ratio + light hex + light ratio.
        if len(hexes) == 2 and len(ratios) == 2:
            check(md.name, hexes[0], DARK_BG, ratios[0], f"--ul-{token} (dark)")
            check(md.name, hexes[1], LIGHT_BG, ratios[1], f"--ul-{token} (light)")
        elif len(hexes) == 1 and len(ratios) == 1:
            # Which ground? Light tables are the ones stating `#FFFFFF`.
            bg = LIGHT_BG if "#FFFFFF" in md.read_text().split(line)[0][-400:] else DARK_BG
            check(md.name, hexes[0], bg, ratios[0], f"--ul-{token}")

if problems:
    print(f"doc contrast check FAILED ({len(problems)} of {checked} claims wrong):")
    for p in problems:
        print("  " + p)
    sys.exit(1)

print(f"ok  {checked} contrast claims in tokens.css + brand/*.md all match measurement")
