"""Generates the Unchained Labs mark + lockups. Geometry is computed, not eyeballed:
edge endpoints are placed on each node's circumference so no stroke pokes through."""
import json, math, pathlib

OUT = pathlib.Path("../assets/logo"); OUT.mkdir(parents=True, exist_ok=True)
ACCENT, INK, PAPER = "#00D4AA", "#0F1419", "#E8EDF2"

L   = (7.0, 16.0); LR = 3.4          # scope node
RS  = [(25.0, 6.5), (25.0, 16.0), (25.0, 25.5)]; RR = 2.6   # fan-out nodes
SW  = 2.1

def edge(a, ar, b, br):
    dx, dy = b[0]-a[0], b[1]-a[1]
    d = math.hypot(dx, dy); ux, uy = dx/d, dy/d
    return (a[0]+ar*ux, a[1]+ar*uy), (b[0]-br*ux, b[1]-br*uy)

def mark_body(node_fill, edge_stroke):
    p = []
    for r in RS:
        (x1,y1),(x2,y2) = edge(L, LR, r, RR)
        p.append(f'    <line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}"/>')
    edges = (f'  <g stroke="{edge_stroke}" stroke-width="{SW}" stroke-linecap="round" fill="none">\n'
             + "\n".join(p) + "\n  </g>")
    nodes = [f'    <circle cx="{L[0]:.2f}" cy="{L[1]:.2f}" r="{LR}"/>']
    nodes += [f'    <circle cx="{r[0]:.2f}" cy="{r[1]:.2f}" r="{RR}"/>' for r in RS]
    return edges + f'\n  <g fill="{node_fill}">\n' + "\n".join(nodes) + "\n  </g>"

def write(name, svg):
    (OUT/name).write_text(svg.rstrip()+"\n"); print("  ", name)

HDR = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32" role="img" aria-label="Unchained Labs">'
for name, nf, es in [("mark-accent.svg", ACCENT, ACCENT),
                     ("mark-dark.svg",   INK,    INK),
                     ("mark-paper.svg",  PAPER,  PAPER),
                     ("mark-mono.svg",   "currentColor", "currentColor")]:
    write(name, f"{HDR}\n{mark_body(nf, es)}\n</svg>")

# favicon: same mark on the brand ground, so a browser tab reads as a tile
write("favicon.svg",
      f'{HDR}\n  <rect width="32" height="32" rx="7" fill="{INK}"/>\n'
      f'{mark_body(ACCENT, ACCENT)}\n</svg>')

# ---- lockups: mark + real Space Grotesk outlines (no font dependency at render time)
w = json.load(open("wordmark.json"))
CAP, WW = 100.0, w["w"]

def lockup_h(name, mark_fill, text_fill):
    """Horizontal: 32-unit mark, gap, wordmark scaled to 13 units cap height."""
    s = 13.0 / CAP; tw = WW * s; gap = 9.0
    total_w = 32 + gap + tw
    ty = (32 - 13.0) / 2
    write(name,
      f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w:.2f} 32" '
      f'width="{total_w:.2f}" height="32" role="img" aria-label="Unchained Labs">\n'
      f'{mark_body(mark_fill, mark_fill)}\n'
      f'  <g transform="translate({32+gap:.2f} {ty:.2f}) scale({s:.5f})" fill="{text_fill}">\n'
      f'    <path d="{w["d"]}"/>\n  </g>\n</svg>')

def lockup_v(name, mark_fill, text_fill):
    s = 9.0 / CAP; tw = WW * s
    total_w = max(32.0, tw); mx = (total_w - 32)/2; tx = (total_w - tw)/2
    write(name,
      f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w:.2f} 49" '
      f'width="{total_w:.2f}" height="49" role="img" aria-label="Unchained Labs">\n'
      f'  <g transform="translate({mx:.2f} 0)">\n{mark_body(mark_fill, mark_fill)}\n  </g>\n'
      f'  <g transform="translate({tx:.2f} 38) scale({s:.5f})" fill="{text_fill}">\n'
      f'    <path d="{w["d"]}"/>\n  </g>\n</svg>')

lockup_h("lockup-horizontal.svg",       ACCENT, PAPER)
lockup_h("lockup-horizontal-dark.svg",  ACCENT, INK)
lockup_h("lockup-horizontal-mono.svg",  "currentColor", "currentColor")
lockup_v("lockup-stacked.svg",          ACCENT, PAPER)
lockup_v("lockup-stacked-dark.svg",     ACCENT, INK)
print("wordmark units:", round(WW,2), "x", CAP)
