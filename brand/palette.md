# Palette

**Chain Teal on Midnight Navy.** Both colours predate this repo — they are the
palette of [unchainlabs.xyz](https://github.com/Unchained-Labs/unchainlabs.xyz)
and of Kymatics, Otter, Seal and Lavoix. This repo did not invent a palette; it
took an existing one, measured it, gave it a ramp, and split status out into its
own axis.

Machine-readable copies live in [`../tokens/`](../tokens/). `tokens.css` is the
source of truth; `tokens.json` and `tailwind.css` are generated from it by
`tools/build-tokens.py`, which fails the build if any ink token drops below its
documented contrast tier.

## Dark — the native ground

Every product in this org is a developer tool that lives next to a terminal.
Dark is not a theme here, it is the default state.

| Role | Token | Value | On `--ul-bg` |
| :--- | :--- | :--- | ---: |
| Ground | `--ul-bg` | `#0F1419` | — |
| Raised surface | `--ul-bg-raised` | `#171D26` | 1.09:1 |
| Inset well | `--ul-bg-inset` | `#0B0F13` | 1.04:1 |
| Hairline | `--ul-line` | `#232B35` | 1.29:1 |
| Strong border | `--ul-line-strong` | `#313B47` | 1.63:1 |
| Heading | `--ul-heading` | `#E8EDF2` | **15.71:1** |
| Body | `--ul-body` | `#A8B3BF` | **8.70:1** |
| Muted | `--ul-muted` | `#7C8896` | **5.13:1** |
| Faint | `--ul-faint` | `#5A6673` | 3.16:1 |
| Accent | `--ul-accent` | `#00D4AA` | **9.69:1** |
| Accent dim | `--ul-accent-dim` | `#00A888` | **6.13:1** |

Two rows are deliberately below the AA body-text floor of 4.5:1, and neither is
allowed to carry prose:

- **`--ul-line` (1.29:1)** is a hairline. It separates regions; it never spells
  anything. A 1px rule at 1.29:1 is visible without becoming a stripe, which is
  the whole job.
- **`--ul-faint` (3.16:1)** clears AA for large text (3:1) and fails it for body
  text. It is for 20px-and-up labels, disabled controls, and decorative
  metadata. If you find it on a sentence, that is a bug — use `--ul-muted`.

## Light — supported, not default

Docs get read in bright rooms. Light mode is a real mode with its own measured
ramp, not the dark ramp inverted by eye.

| Role | Token | Value | On `#FFFFFF` |
| :--- | :--- | :--- | ---: |
| Heading | `--ul-heading` | `#0F1419` | **18.51:1** |
| Body | `--ul-body` | `#3E4A57` | **9.04:1** |
| Muted | `--ul-muted` | `#5D6B7A` | **5.46:1** |
| Faint | `--ul-faint` | `#7B8896` | 3.62:1 |
| Accent | `--ul-accent` | `#007D66` | **5.09:1** |
| Accent dim | `--ul-accent-dim` | `#00604E` | **7.55:1** |

**The accent changes value between modes, and only the accent.** Chain Teal on
white measures **1.91:1** — it is invisible as text. Keeping `#00D4AA` in light
mode for the sake of brand consistency would mean shipping unreadable links.
Light mode therefore holds the hue and drops the luminance to `#007D66`. This is
the single place in the system where a token's identity shifts between modes, and
the justification is arithmetic rather than preference.

## Status is a separate axis

The dashboards and CLIs in this org exist to answer *did it pass?* That answer
must never share a colour with the brand, or a green build and a branded button
become the same visual event.

| Role | Token | Dark | On bg | Light | On white |
| :--- | :--- | :--- | ---: | :--- | ---: |
| Pass | `--ul-up` | `#4ADE80` | 10.62:1 | `#12783F` | 5.55:1 |
| Warn | `--ul-warn` | `#E8B339` | 9.64:1 | `#8A5B00` | 5.87:1 |
| Fail | `--ul-down` | `#E5484D` | 4.73:1 | `#C0272C` | 5.89:1 |

### The tension we did not design away

Chain Teal sits at hue **168°**. Status-pass sits at **142°**. That is 26° of
separation between the brand accent and the colour that means "green build" —
uncomfortably close, and the direct cost of inheriting a blue-green brand accent
rather than picking a fresh one.

The alternatives were worse. Moving status-pass yellower collides with
status-warn. Making it blue breaks the near-universal convention that pass is
green. Changing the brand accent throws away the visual identity of five
shipped products. So the constraint stays, and it is handled rather than hidden:

**Status is never encoded in colour alone.** Every pass/warn/fail signal in an
Unchained Labs surface carries a glyph or a word next to the colour — `✓ pass`,
`! warn`, `✗ fail`. This is required for the 8% of men with red-green colour
vision deficiency regardless of our hue spacing, so the honest reading is that
the 26° problem forced us into an accessibility practice we owed users anyway.

The saturation gap does most of the remaining work: the accent is 100%
saturated, status-pass is 67%. Side by side the accent reads as the more
electric of the two.

## Accent budget

The accent is a pointer, not a paint. On a given view it should appear:

- once on the primary action,
- on interactive text (links, focused inputs),
- on the mark.

If a screenshot shows teal in more than roughly a tenth of its pixels, the
accent has stopped meaning "look here". Large teal fills are a specific mistake:
`#00D4AA` at 100% saturation across a panel vibrates against the near-black
ground. Use `--ul-accent-wash` (12%) for selected rows and subtle fills.

## Elevation

Shadows are close to useless on a `#0F1419` ground — there is nothing darker to
cast onto. Elevation is expressed with `--ul-bg-raised` plus a
`--ul-line` hairline. Do not add glows to simulate depth; a teal glow reads as a
status indicator, which collides with the status axis above.

## Checking your work

```sh
make contrast   # prints every documented pair and its measured ratio
make tokens     # regenerates tokens.json + tailwind.css, fails on a tier breach
```

Both run in CI. A palette change that breaks a contrast tier does not merge.
