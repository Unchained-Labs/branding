"""Prints every documented colour pair and its measured ratio. `make contrast`."""
def srgb(c):
    c = c/255
    return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
def lum(h):
    h = h.lstrip('#')
    r,g,b = (int(h[i:i+2],16) for i in (0,2,4))
    return 0.2126*srgb(r)+0.7152*srgb(g)+0.0722*srgb(b)
def ratio(a,b):
    la,lb = lum(a),lum(b)
    hi,lo = max(la,lb),min(la,lb)
    return (hi+0.05)/(lo+0.05)

BG      = '#0F1419'
RAISED  = '#171D26'
pairs = [
 ('heading #E8EDF2','#E8EDF2',BG), ('body #A8B3BF','#A8B3BF',BG),
 ('muted #7C8896','#7C8896',BG),   ('faint #5A6673','#5A6673',BG),
 ('accent #00D4AA','#00D4AA',BG),  ('accent on raised','#00D4AA',RAISED),
 ('accent-dim #00A888','#00A888',BG),
 ('line #232B35','#232B35',BG),
 ('up #4ADE80','#4ADE80',BG), ('warn #E8B339','#E8B339',BG), ('down #E5484D','#E5484D',BG),
 ('body on raised','#A8B3BF',RAISED), ('muted on raised','#7C8896',RAISED),
 ('bg on accent (btn text)','#0F1419','#00D4AA'),
]
print(f"{'pair':28} {'ratio':>6}  AA-body AA-large")
for name,fg,bg in pairs:
    r = ratio(fg,bg)
    print(f"{name:28} {r:6.2f}  {'PASS' if r>=4.5 else 'fail ':7} {'PASS' if r>=3 else 'fail'}")
print()
print("hue separation accent vs status-up:")
import colorsys
for n,h in [('accent #00D4AA','00D4AA'),('up #4ADE80','4ADE80'),('warn #E8B339','E8B339'),('down #E5484D','E5484D')]:
    r,g,b = (int(h[i:i+2],16)/255 for i in (0,2,4))
    hh,ss,vv = colorsys.rgb_to_hsv(r,g,b)
    print(f"  {n:16} hue {hh*360:5.1f}deg  sat {ss*100:4.1f}%  val {vv*100:5.1f}%")
