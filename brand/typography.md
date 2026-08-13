# Typography

Three faces, three jobs. The rule is that a reader should be able to tell what
kind of information they are looking at before they read a word of it.

| Role | Family | Weight | Used for |
| :--- | :--- | :--- | :--- |
| Display | Space Grotesk | 600–700 | Headings, the wordmark, stat figures |
| Label | Space Grotesk | 600, uppercase, `+0.08em` | Section eyebrows, table headers, badges |
| Body | Inter | 400–500 | Prose, docs, UI copy |
| Data | JetBrains Mono | 400–500 | Code, CLI output, token values, IDs, counts |

Space Grotesk is inherited — it was already the heading face of
[unchainlabs.xyz](https://github.com/Unchained-Labs/unchainlabs.xyz), and Inter
was already the body face. This repo kept both and added the mono, which was the
missing role: an org shipping five CLIs had no documented face for the thing
those CLIs actually emit.

## Why Space Grotesk survived the audit

The temptation when formalising a brand is to replace the inherited display face
with something more fashionable. Space Grotesk stayed for a reason that shows up
in the mark: it has a slightly mechanical, wide-aperture geometry with flat
terminals, and the mark is built from circles and straight strokes. They share a
construction logic. A humanist or high-contrast display face next to that mark
would read as two unrelated decisions.

It also holds up at the sizes this org actually uses — a 12px uppercase label in
a dense table, and a 48px figure on a landing page — which many geometric sans
faces do not.

## Why the labels are industrial and the prose is not

Uppercase Space Grotesk with `+0.08em` tracking is a deliberately technical
register: it looks like a panel legend. That is right for *structure* — the words
that tell you where you are.

Inter carries the *argument*. The docs in this org are written, not generated,
and they make claims that need to be read at length: why a barrier is
unjustified, why three identical verifiers are one verifier. A reader who has to
work through 400 words of reasoning should be doing it in a face optimised for
exactly that, which is Inter's entire design brief.

Setting prose in the display face would be the common failure here — it looks
tighter in a screenshot and gets tiring by the third paragraph.

## Data gets its own face, always

Every number that came out of a machine is set in JetBrains Mono: token counts,
dollar figures, agent counts, kappa values, file paths, commit SHAs, exit codes.

This is load-bearing rather than decorative. These products report measurements —
`N_eff = 1.2`, `$0.34`, `precision 0.71` — and the mono face is the signal that
a figure is *measured* rather than *written*. A cost estimate in Inter reads as a
claim; the same estimate in JetBrains Mono reads as output. Mixing them up
undermines the one thing these tools sell.

JetBrains Mono also has a genuinely tall x-height and disambiguated `0/O` and
`1/l/I`, which matters when the string on screen is a token you might have to
retype.

## Scale

A 1.25 ratio on a 16px base. Tokens in [`../tokens/tokens.css`](../tokens/tokens.css).

| Token | Size | Typical use |
| :--- | ---: | :--- |
| `--ul-text-xs` | 12px | Labels, badges, table headers |
| `--ul-text-sm` | 14px | Dense UI, captions, code in prose |
| `--ul-text-base` | 16px | Body |
| `--ul-text-lg` | 20px | Lead paragraph, card titles |
| `--ul-text-xl` | 24px | `h3` |
| `--ul-text-2xl` | 31px | `h2` |
| `--ul-text-3xl` | 39px | `h1` |
| `--ul-text-4xl` | 49px | Hero figure only |

Display sizes take `--ul-track-display` (`-0.02em`). Space Grotesk sets loose at
large sizes; without the negative tracking a 39px heading looks like it has been
stretched.

Body copy holds a measure of **65–75 characters**. Wider than that and the
return sweep starts costing comprehension, which is the whole reason a serif-free
body face was chosen over something more decorative.

## Fonts in this repo

[`../fonts/SpaceGrotesk[wght].ttf`](../fonts/) is vendored — the variable font,
`wght` 300–700, under the SIL Open Font License
([`OFL-SpaceGrotesk.txt`](../fonts/OFL-SpaceGrotesk.txt)). It is here so the
wordmark can be regenerated from source rather than trusted as a blob:
`tools/mkwordmark.py` instantiates it at weight 700 and converts
`UNCHAINED LABS` to outline paths.

**The lockup SVGs contain no text elements and no font references.** They carry
real vector paths, so they render identically on a machine that has never heard
of Space Grotesk. This is the difference between a wordmark and a `<text>` tag
that happens to look right on your laptop.

Inter and JetBrains Mono are *not* vendored — apps load them from their own
pipeline (npm, Fontsource, a CDN, or the OS). Both are OFL. The token stack
degrades to `system-ui` and `ui-monospace` respectively, which is a real
fallback rather than a decorative one.

## Regenerating the wordmark

```sh
make wordmark   # re-runs mkwordmark.py -> tools/wordmark.json
make logo       # rebuilds every SVG that embeds it
make png        # rasterises
```

If you change the tracking or the weight, all three must run. The wordmark JSON
is committed so a checkout without Python can still build the SVGs.
