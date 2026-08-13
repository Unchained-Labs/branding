#!/usr/bin/env python3
"""Asserts every rendered PNG is the size and ink it claims in its filename.

Catches the two failure modes that make a brand repo untrustworthy: a file called
`mark-accent-512.png` that is actually 256px, and a `mark-mono-white-*.png` that
rasterised to black because `currentColor` inherited nothing.

Run via `make verify` (in a container with Pillow).
"""
import pathlib
import re
import sys

from PIL import Image

PNG = pathlib.Path(__file__).resolve().parent.parent / "assets" / "logo" / "png"

ACCENT = (0, 212, 170)
INK = (15, 20, 25)
PAPER = (232, 237, 242)

problems: list[str] = []
checked = 0


def dominant_opaque(img: Image.Image) -> tuple[int, int, int] | None:
    """Most common fully-opaque colour, ignoring antialiased edge pixels."""
    img = img.convert("RGBA")
    colours = img.getcolors(maxcolors=img.width * img.height)
    if not colours:
        return None
    opaque = [(n, rgba) for n, rgba in colours if rgba[3] > 240]
    if not opaque:
        return None
    return max(opaque, key=lambda t: t[0])[1][:3]


def near(a: tuple[int, int, int], b: tuple[int, int, int], tol: int = 10) -> bool:
    return all(abs(x - y) <= tol for x, y in zip(a, b))


for path in sorted(PNG.glob("*.png")):
    name = path.stem
    with Image.open(path) as img:
        w, h = img.size
        ink = dominant_opaque(img)
    checked += 1

    # --- size claims -------------------------------------------------------
    m = re.match(r"^(.*)-h(\d+)$", name)
    if m:  # lockups scale by height
        want = int(m.group(2))
        if h != want:
            problems.append(f"{path.name}: claims height {want}, is {h}")
    else:
        m = re.match(r"^(.*)-(\d+)$", name)
        if not m:
            problems.append(f"{path.name}: filename encodes no size")
            continue
        want = int(m.group(2))
        if (w, h) != (want, want):
            problems.append(f"{path.name}: claims {want}x{want}, is {w}x{h}")

    # --- ink claims --------------------------------------------------------
    if ink is None:
        problems.append(f"{path.name}: fully transparent")
        continue
    if "mark-mono-white" in name:
        if not near(ink, (255, 255, 255)):
            problems.append(f"{path.name}: mono-white rendered {ink}, expected white")
    elif "mark-mono-black" in name:
        if not near(ink, (0, 0, 0)):
            problems.append(f"{path.name}: mono-black rendered {ink}, expected black")
    elif name.startswith("favicon"):
        if not near(ink, INK):
            problems.append(f"{path.name}: favicon ground is {ink}, expected {INK}")
    elif "-dark" in name:
        if not (near(ink, INK) or near(ink, ACCENT)):
            problems.append(f"{path.name}: dark variant is {ink}, expected ink or accent")
    elif "accent" in name or "lockup" in name:
        if not (near(ink, ACCENT) or near(ink, PAPER)):
            problems.append(f"{path.name}: is {ink}, expected accent or paper")
    elif "paper" in name:
        if not near(ink, PAPER):
            problems.append(f"{path.name}: is {ink}, expected paper {PAPER}")

if problems:
    print(f"png verify FAILED ({len(problems)} of {checked}):")
    for p in problems:
        print("  " + p)
    sys.exit(1)

print(f"ok  {checked} PNGs are the sizes and inks they claim")
