# Voice

We ship measurement tools. The voice follows from that: **state the number, name
the tradeoff, don't sell.**

## The shape of a sentence here

Lead with the finding. Put the mechanism after it. Let the reader decide what to
do.

> 3 verifiers, `N_eff = 1.2`. You are paying for three checks and getting
> slightly more than one — they share a model, a temperature, and a prompt
> scaffold, so they fail together.

Not:

> Supercharge your agent workflows with next-generation verification analytics!

The first sentence is useful to someone at 2am. The second is a landing page for
a product nobody has run.

## Rules

**Numbers over adjectives.** Never "significantly cheaper" — say "38% fewer
tokens on the 20-case eval set". If there is no number yet, say there is no
number yet.

**Name the cost.** Every one of these tools trades something. `graphlint` will
flag barriers that are load-bearing in your specific graph. `preflight` estimates
and estimates are wrong. Say so in the README, not in a FAQ nobody opens.

**No hedging on the things we do know.** "May potentially help reduce costs in
some cases" is a sentence written to avoid being wrong. If the eval says
precision went from 0.61 to 0.78, write that.

**Second person, present tense, active voice.** "Run `graphlint check`" — not
"the check command may be invoked by the user".

**Short sentences carry the claims. Long sentences carry the reasoning.** Do not
write a 40-word sentence whose payload is a fact; do not chop an argument into
fragments to look punchy.

**No em-dash pileups, no arrow chains in prose.** `A → B → fails` belongs in a
diagram or a code block. In a sentence, use words.

## Vocabulary

| Say | Not |
| :--- | :--- |
| finding | issue, item, insight |
| verifier lens | validator, checker, guard |
| fan-out | parallelisation, scale-out |
| barrier | sync point, join, gate |
| spec | config, definition file |
| agent | worker, bot, AI |
| estimate | prediction, forecast |
| refused / not measurable | N/A, unknown, error |

That last row matters most. When a tool cannot measure something, it says so in
those words. It does not emit a zero, a null, or a confident guess. A tool that
prints a number for every field whether or not the input supports it is the
failure mode all of these products exist to argue against.

## Naming

Tools get **lowercase, single-word, verb-or-noun names**: `graphlint`,
`decorrelate`, `preflight`, `authsweep`. No camelCase, no `-js`, no `.ai`, no
prefix. The name should say what it does to something you already have.

The org is **Unchained Labs** in prose, `Unchained-Labs` on GitHub. Never
"UnchainedLabs" or "UL".

## READMEs

Every product README opens with the same four things, in order:

1. **One sentence** on what it does to what.
2. **The status line** — `alpha`, `beta`, or `stable`, and what that means for
   API churn. Honest, not aspirational.
3. **A copy-pasteable command** that produces real output.
4. **What it does not do.** The scope boundary, up front, before someone spends
   an afternoon discovering it.

Then install, usage, the reasoning, and a link to the docs site.

Do not open with a logo the width of the page, a badge wall, or a paragraph about
the future of AI engineering.

## Commits

Imperative mood, lowercase, no type prefix unless the repo already uses one:

```
add N_eff to the report output
fix barrier detection inside pipeline stages
document the 26deg accent/status collision
```

Say what the commit does. If it needs a paragraph, put a paragraph in the body —
the reasoning is worth more than the summary line.

## Issues and PR replies

Answer the question asked. If the answer is "that is a real bug", say that in the
first sentence. If the answer is "working as intended", say why the intent is
what it is, and treat a second report of the same confusion as evidence the
intent is wrong.

Never thank someone for their "interest in the project".

## On the marketing register

There is exactly one place a superlative is allowed: a claim that is
independently checkable in the same sentence. "The only linter for agent
workflow specs" is fine if it is true and someone can verify it in a search. "The
most powerful verification suite" is not fine, because nobody can check it and
everybody has read it before.
