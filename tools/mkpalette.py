#!/usr/bin/env python3
"""Builds the palette hero image: surface ramp, ink ramp, accent, status axis.
Generated from tokens.json so the image can never disagree with tokens.css.
`make palette-image`."""
import json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
T = json.loads((ROOT/"tokens"/"tokens.json").read_text())["colour"]["dark"]
def v(k): return T[k]["value"]
def r(k): return T[k]["contrastOnBg"]

W       = 1200
PAD     = 48
SW, SH  = 128, 76
GAP     = 12
ROW_H   = 168          # swatch + name + hex + ratio + breathing room
FD = "Space Grotesk, DejaVu Sans, sans-serif"
FM = "JetBrains Mono, DejaVu Sans Mono, monospace"

o = []
def label(x, y, text, fill, size=11, font=FD, track=0.0, weight=400, anchor="start"):
    o.append(f'  <text x="{x:.0f}" y="{y:.0f}" fill="{fill}" font-family="{font}" '
             f'font-size="{size}" font-weight="{weight}" letter-spacing="{track}" '
             f'text-anchor="{anchor}">{text}</text>')

def swatches(y, title, keys, stroke=True):
    """Returns the y of the next row."""
    label(PAD, y, title, v("faint"), 10, FD, 1.6, 600)
    top = y + 16
    for i, k in enumerate(keys):
        x = PAD + i*(SW+GAP)
        st = f' stroke="{v("line")}"' if stroke else ''
        o.append(f'  <rect x="{x}" y="{top}" width="{SW}" height="{SH}" rx="6" fill="{v(k)}"{st}/>')
        label(x,    top+SH+20, k,      v("body"),  11, FM, 0, 500)
        label(x,    top+SH+36, v(k),   v("muted"), 10, FM)
        label(x+SW, top+SH+36, f'{r(k):.2f}:1', v("faint"), 10, FM, 0, 400, "end")
    return y + ROW_H

# --- header + lockup, sized so it cannot overflow ------------------------------
lock = (ROOT/"assets"/"logo"/"lockup-horizontal.svg").read_text()
lw = float(re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', lock).group(1))
inner = lock[lock.index(">")+1 : lock.rindex("</svg>")]
LS = 1.5
lx = W - PAD - lw*LS

rows = ["SURFACE", "INK", "STATUS"]
H = 96 + ROW_H*2 + 130

o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
     f'  <rect width="{W}" height="{H}" fill="{v("bg")}"/>',
     f'  <g transform="translate({lx:.0f} 40) scale({LS})">{inner}</g>']

label(PAD, 56, "UNCHAINED LABS · BRAND TOKENS", v("heading"), 15, FD, 1.8, 700)
label(PAD, 78, "Chain Teal on Midnight Navy — measured, not asserted", v("muted"), 12, FD)

y = swatches(120, "SURFACE", ["bg", "bg-raised", "bg-inset", "line", "line-strong"])

# INK row, with the accent pair appended to the right of it
label(PAD, y, "INK", v("faint"), 10, FD, 1.6, 600)
label(PAD + 4*(SW+GAP), y, "ACCENT", v("faint"), 10, FD, 1.6, 600)
top = y + 16
for i, k in enumerate(["heading", "body", "muted", "faint", "accent", "accent-dim"]):
    x = PAD + i*(SW+GAP)
    o.append(f'  <rect x="{x}" y="{top}" width="{SW}" height="{SH}" rx="6" fill="{v(k)}"/>')
    label(x,    top+SH+20, k,      v("body"),  11, FM, 0, 500)
    label(x,    top+SH+36, v(k),   v("muted"), 10, FM)
    label(x+SW, top+SH+36, f'{r(k):.2f}:1', v("faint"), 10, FM, 0, 400, "end")
y += ROW_H

# STATUS
label(PAD, y, "STATUS — A SEPARATE AXIS, NEVER COLOUR ALONE", v("faint"), 10, FD, 1.6, 600)
top = y + 16
for i, (k, glyph, word) in enumerate([("up","✓","pass"), ("warn","!","warn"), ("down","✗","fail")]):
    x = PAD + i*(SW+GAP)
    o.append(f'  <rect x="{x}" y="{top}" width="{SW}" height="46" rx="6" '
             f'fill="{v(k)}22" stroke="{v(k)}"/>')
    label(x+16, top+30, f'{glyph} {word}', v(k), 15, FM, 0, 500)
    label(x,    top+68, v(k),            v("muted"), 10, FM)
    label(x+SW, top+68, f'{r(k):.2f}:1', v("faint"), 10, FM, 0, 400, "end")

label(W-PAD, H-18, "tokens/tokens.css is the source of truth", v("faint"), 10, FD, 0, 400, "end")
o.append("</svg>")

out = ROOT/"assets"/"palette"/"tokens.svg"; out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("\n".join(o)+"\n")
print(f"   {out.relative_to(ROOT)}  {W}x{H}  (lockup at x={lx:.0f}, w={lw*LS:.0f})")
