# The post template lives in the page-design skill

`.claude/skills/page-design/assets/post-template.html` — **still true, verified
2026-09-06**: the file is there, it is the only `post-template.html` in the repo, and its
`:root` matches `style.css`'s canonical block token for token (29 today).

```bash
cp .claude/skills/page-design/assets/post-template.html blog/<slug>.html
```

**Two things it is not.**

1. **It is not the source for the AI Transformation series.** Those 20 posts are emitted by
   `scripts/build_series.py`, which lifts its skeleton from `blog/hermes-101.html` **at run
   time** rather than from any checked-in template — same anti-rot argument, a different
   mechanism. `--check` diffs what it lifted. A 21st post in that series never touches this
   file.
2. **It does not ship the TH ⇄ EN switch.** The template's only mentions of bilingual are
   two head comments (`og:locale:alternate`, `dateModified`); the checkbox, the ~26 lines of
   switch CSS, the two `.l-th`/`.l-en` tracks, the duplicated TOC and the `th-`/`en-` id
   split are all inserted afterwards by `python3 scripts/bilingualize.py --post <slug>`,
   which reads its CSS out of a live post (`blog/hermes-101.html` or
   `blog/morning-waking.html`) for the same reason. **That is deliberate — do not "complete"
   the template by pasting the switch into it**, or there will be two copies of the pattern
   with nothing keeping them in sync, which is the exact failure this file documents.

There used to be a second template here, `blog-post/assets/post-template.html`.
It was deleted on 2026-08-10 because it had silently rotted three sitewide
sweeps behind the corpus while still being the file this skill told authors to
copy — so every new post written from it would have been born off the house
system and would have quietly undone the sweeps one post at a time:

| Sweep | What the corpus got | What the stale template still had |
|---|---|---|
| 6670480 tokens | 24-token canonical `:root` in all 42 files | 11 tokens, no `--radius`/`--measure`/`--wide`/`--transition` |
| ec2827b covers | JPG covers, all ≤200 KB | no guidance, no `width`/`height` |
| e8da9da a11y | `:focus-visible`, `prefers-reduced-motion`, `color-scheme`, `text-wrap`, `aspect-ratio`, `loading`/`decoding`/`width`/`height` on 120/120 images | **0** of them |
| 635eb94 ladder | card titles are `h4` | `h2` |
| layout constants | `var(--measure)` / `var(--wide)` / `var(--radius-lg)` | hardcoded `720px` / `860px` / `16px` |

Those are the corpus values **at each named commit**, not today's. Two of them have moved
since: the canonical `:root` is **29** tokens after the 2026-08-26 re-key to the book
covers, and card titles are **`<h3>`** since deleting the `.category` bands cut the heading
ladder one level shallower (`h1` hero → `h2` series → `h3` card). Copy the level from
`blog/index.html`, never from this table.

**Deliberate design choice: one file, not two kept in sync.** Two copies of a
template in a repo with no build step is the same failure mode as two copies of
a counter — nothing enforces the sync, so it silently stops holding. Everything
the deleted file said that page-design's did not is now inline in the surviving
template as comments (single-`h1` rule, prev/next-is-derived rule, the Thai-prose /
English-headings body convention, Thai code comments, diagrams-are-PNGs, `🐕` closing
bullet). The TH ⇄ EN *switch* is the one thing that stayed out — see above.

Do not recreate a template here. If a future template needs blog-post-specific
guidance, add it as a comment to the page-design file.
