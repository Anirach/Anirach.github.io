# The post template lives in the page-design skill

`.claude/skills/page-design/assets/post-template.html`

```bash
cp .claude/skills/page-design/assets/post-template.html blog/<slug>.html
```

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

**Deliberate design choice: one file, not two kept in sync.** Two copies of a
template in a repo with no build step is the same failure mode as two copies of
a counter — nothing enforces the sync, so it silently stops holding. Everything
the deleted file said that page-design's did not is now inline in the surviving
template as comments (single-`h1` rule, prev/next-is-derived rule, bilingual
body scaffold, Thai code comments, diagrams-are-PNGs, `🐕` closing bullet).

Do not recreate a template here. If a future template needs blog-post-specific
guidance, add it as a comment to the page-design file.
