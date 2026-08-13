# Mark study — nine candidates, and what each turned out to look like

The brief: a mark for an org whose products all argue that *linear execution is a
chain and the real work is a graph*. It had to survive 16px, read on a dark
ground, and not look like the other 400 AI-tool logos shipped in 2025–26.

Every candidate was rendered at 16, 32, 64, 128 and 512 on both grounds before
being judged. Several died at 16px and nowhere else, which is the usual outcome.

## Chosen — Fan-out

One heavy node, three edges, three light nodes.
[`../assets/logo/mark-accent.svg`](../assets/logo/mark-accent.svg).

Why it won:

- **It is the product.** `scope → fan out` is the first step of every graph in
  the reference architecture. The mark is a diagram of the thing being sold, not
  a metaphor for it.
- **It reads as `<`.** An opening bracket, a caret, the start of an argument.
  Terminal-native without being a literal prompt glyph (see rejects).
- **It survives 16px** — just. The `2.1` stroke lands near one pixel and the
  three edges stay distinct. This was the binding constraint on almost every
  candidate.
- **Direction.** The asymmetric node weight (`3.4` vs `2.6`) gives it a
  left-to-right reading, so it works as a leading element in a lockup.

Cost: a node-and-edge mark is not unheard of in dev tooling. It is distinctive
here because of the *specific* asymmetry and the exact 1→3 fan, not because
nobody has drawn a graph before.

## Option B — Broken chain link

Two interlocking rounded links with a visible gap where the third would be.
Literal reading of "unchained".

**Why it lost.** It says what we are not. The whole argument is that the
replacement for a chain is a *specific* shape, and the broken link doesn't show
it — a reader gets "something is disconnected", which in an infrastructure
context reads as *breakage*, not liberation. A mark that suggests your pipeline
is severed is an own goal.

It was also the worst 16px performer in the set: two link outlines plus a gap is
three tones inside 16 pixels, and it collapsed into a grey blob.

## Option C — Prompt bracket

`[>]` — a monospace bracket pair holding a chevron.

**Why it lost.** Genuinely good, genuinely legible, and already taken: the
sibling org [Clanker-Labs](https://github.com/Clanker-Labs/branding) uses `[●]`,
brackets holding a lamp. Two orgs with the same owner both using
bracket-enclosed glyphs is a drift. Kept as a complete file in this study only as
a record of the decision.

## Rejected — the seven that died

**Diamond graph.** The full `scope → fan → reduce → synth` diamond from the
architecture, compressed into a mark. Beautiful at 512px, unreadable at 32.
Four columns of nodes cannot live in 32 pixels. This is the classic
"my logo is an infographic" failure.

**Directed acyclic graph, organic layout.** Five nodes in an irregular
arrangement with curved edges. Looked like a molecule, then like a constellation,
then like every biotech logo. No reading order.

**Unlinked chain, vertical.** Chain links falling apart downward. Read as a
*failing* build — vertical descent plus separation is the visual language of
error states.

**Fork glyph.** The git-branch fork symbol. Legible, instantly understood, and
owned by git. Using it says "we do version control".

**Three parallel bars.** Simple, scaled beautifully, and is a hamburger menu.

**Hexagon with internal nodes.** The container/infra cliché. Hexagons in this
space read as Kubernetes or as a blockchain, and the second association is
exactly the positioning we were leaving behind.

**Speech-bubble with nodes.** An attempt to say "agents". Every LLM product
shipped this in 2024. Dead on arrival.

## The 16px test

The single most useful thing in this study was rendering everything at 16px
early, on both grounds, and looking at it in a browser tab rather than in a
design file. Four of the nine candidates were eliminated on that test alone, and
two of those four were the best-looking at large sizes.

```sh
make png     # renders every documented size
make verify  # asserts each PNG is the size and ink it claims
```

## Swapping the mark

If the mark is ever replaced, the geometry lives in one place —
[`../tools/mkmark.py`](../tools/mkmark.py) — and every SVG plus all 68 PNGs
regenerate from `make logo && make png`. The lockups pull the wordmark from
`tools/wordmark.json`, so a mark change does not touch the wordmark and vice
versa.
