# Palette study — five directions, and why four lost

Written August 2026, when the org repositioned from "blockchain / DeFi / Web3
solutions" to agent infrastructure. The question was whether the inherited
palette should survive that change.

## The inherited state

[unchainlabs.xyz](https://github.com/Unchained-Labs/unchainlabs.xyz) shipped with
a documented palette:

| Name | Value |
| :--- | :--- |
| Chain Teal | `#00D4AA` |
| Midnight Navy | `#0F1419` |
| Deep Space | `#1A1F2E` |
| Gray 300 | `#D1D5DB` |
| Cool Gray | `#9CA3AF` |

Kymatics, Otter, Seal and Lavoix all inherited it. So the real question was not
"what palette suits agent tooling" but "is `#00D4AA` worth keeping given five
products already use it".

## Direction A — Keep Chain Teal, formalise around it *(chosen)*

Hold `#00D4AA` and `#0F1419` exactly. Build a proper ink ramp, split status onto
its own axis, add a mono face, measure everything.

**Why it won.** The accent is genuinely good: 9.69:1 on the navy ground, high
chroma without being a neon, and it does not look like the purple-gradient
default that every AI tool shipped in 2025. Teal also reads as *instrument* — it
is the colour of an oscilloscope trace, which is the right association for a set
of measurement tools.

The cost is real and documented in [`../brand/palette.md`](../brand/palette.md):
a 168° accent sits only 26° from a conventional status-green. We took that cost
rather than orphaning five products' visual identity.

**What changed even though the accent didn't.** `Deep Space #1A1F2E` was retired.
It is noticeably blue-violet next to the ground, and against a teal accent the
whole surface picked up a purple cast. Replaced with `#171D26` — same lightness
step, hue pulled toward neutral. Almost nobody would name the difference in
isolation; side by side the teal stops looking slightly wrong.

`Gray 300` and `Cool Gray` were replaced by a four-step ink ramp
(`heading`/`body`/`muted`/`faint`), because two greys cannot express a table
header, a value, a caption, and a disabled control.

## Direction B — Teal, but shift it to escape the status collision

Move the accent to roughly 185° (`#00C2D4`, a cyan) so status-green sits a clear
43° away.

**Why it lost.** It solves the collision and creates a worse one: at 185° the
accent starts reading as an *information* colour — the blue of a `notice` callout
in every docs framework on earth. And it still would have been a rebrand of five
products, for a problem that a glyph next to every status badge solves outright.

## Direction C — Fresh brand: amber on graphite

Drop teal. `#E8912B` on `#141414`. Warm, distinctive, zero collision with any
status colour, and it separates cleanly from the teal-heavy AI-tools field.

**Why it lost.** It was the strongest of the alternatives and the closest call.
It died on two counts. First, amber *is* the warning colour in every CI surface
these tools sit next to — the collision moves from pass to warn, which is worse,
because a warning is the state you most need to read correctly. Second, this
org's sibling brand
([Clanker-Labs](https://github.com/Clanker-Labs/branding)) already runs a warm
amber accent (`#e79a4b`) on graphite. Two orgs owned by the same person, both
amber-on-dark, is a drift rather than a decision.

## Direction D — Monochrome plus one signal colour

Pure greyscale surface and ink; colour reserved *entirely* for status. No brand
accent at all.

**Why it lost.** Intellectually the cleanest answer to the collision problem —
if the brand has no colour, the brand cannot collide with status. But it is a
brand system with nothing to recognise. The mark, the docs site, and the CLI
would have no shared visual anchor, and "tasteful greyscale developer tool" is
itself a crowded look.

Kept one idea from it: **elevation is greyscale only.** No teal glows, no
accent-tinted surfaces. `--ul-bg-raised` plus a hairline.

## Direction E — Teal on true black

`#00D4AA` on `#000000`. Maximum contrast, OLED-friendly.

**Why it lost.** On `#000` the accent's contrast climbs to 11.0:1 and it starts
to vibrate — high-chroma cyan-green on pure black has a visible halo on most LCD
panels. `#0F1419` costs about two points of ratio and removes the shimmer
entirely. Pure black also leaves no room for `--ul-bg-inset`: you cannot go
darker than the floor, so wells and active rows have to be built by going
*lighter*, which inverts the depth model.

## What the choice commits us to

1. **A glyph or word beside every status colour, forever.** Not optional styling
   — it is the mitigation that made Direction A viable. See
   [`../brand/palette.md`](../brand/palette.md).
2. **The accent shifts value in light mode.** `#00D4AA` is 1.91:1 on white.
   Light mode uses `#007D66`. Any component hard-coding the dark accent breaks in
   light mode, which is why nothing hard-codes a hex.
3. **Teal is a pointer, not a surface.** Documented as the accent budget.

## Relationship to the sibling brands

Erwin Lejeune also owns [Clanker-Labs](https://github.com/Clanker-Labs/branding)
(amber `#e79a4b`, "Porchlight") and [HoopsLab](https://github.com/HoopsLab/brand).
These are **siblings, not children**: shared token vocabulary and repo layout, no
shared surface colour. Chain Teal at 168° and Porchlight amber at 30° are 138°
apart and on opposite sides of the warm/cool line. A component moves between the
two systems by swapping the token file and nothing else.
