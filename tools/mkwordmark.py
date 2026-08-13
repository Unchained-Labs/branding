from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

SRC="../fonts/SpaceGrotesk[wght].ttf"

def wordmark(text, weight=700, cap_h=100, tracking=0.0):
    f = instantiateVariableFont(TTFont(SRC), {"wght": weight}, inplace=False)
    upem = f["head"].unitsPerEm
    gs  = f.getGlyphSet()
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    os2 = f["OS/2"]
    capHeight = getattr(os2, "sCapHeight", None) or 700
    scale = cap_h / capHeight            # scale so cap height == cap_h units
    track = tracking * upem              # tracking in font units

    x = 0.0
    subpaths = []
    for ch in text:
        if ch == " ":
            x += hmtx[cmap[ord(" ")]][0] + track
            continue
        gname = cmap[ord(ch)]
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}")
        # flip Y (font y-up -> svg y-down), scale, translate
        t = Transform(scale, 0, 0, -scale, x * scale, cap_h)
        gs[gname].draw(TransformPen(pen, t))
        d = pen.getCommands()
        if d: subpaths.append(d)
        x += hmtx[gname][0] + track
    total_w = x * scale
    return " ".join(subpaths), total_w, cap_h

if __name__ == "__main__":
    import json, sys
    # tracking +0.04em for the uppercase label look
    d, w, h = wordmark("UNCHAINED LABS", weight=700, cap_h=100, tracking=0.02)
    print(json.dumps({"d": d, "w": round(w,2), "h": h}))
