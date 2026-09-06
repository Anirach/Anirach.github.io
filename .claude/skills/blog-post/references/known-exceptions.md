# Known exceptions and standing drift — things that look broken and are not

Read this before "fixing" anything you notice while editing a post. Every item below was
re-checked on **2026-09-06**, after the 2026-09-03 bilingual sweep and the 2026-09-05
AI Transformation launch, and each is cross-referenced to the
`check_site.py` invariant that guards it — if an item here has no live violation, it is
stale and should be deleted, not left as a standing excuse. There is no baselined debt
anywhere today: `check_site.py` reports `0 new, 0 known` and `verify-wiring.py` prints
`CLEAN — no new wiring breakage (0 warn)` with an empty `BASELINE`. Inventing links to
make things symmetrical will corrupt the one navigation chain that verifies perfectly.

> **Standing rule:** any change that invalidates a number in a skill file must update that
> number in the same commit. That includes this file's drift tables and the `BASELINE` set
> in `assets/verify-wiring.py`.

## Deliberate exceptions — leave alone

**There are no `.category` bands any more.** The Academic & Philosophy and Lifestyle
placeholders (0 cards, "First posts coming soon") added in Task 11 (2026-08-10) were
deleted on 2026-08-26, and the last band, Technology, went with them because it held 100%
of the posts. `blog/index.html` is hero (with its `.blog-jump` chip strip) → one
`.feature` → **five** `.series-section` blocks. INV-02d now fails on any empty `.category`
band a future commit adds; do not re-create placeholder bands.

**A post carrying two `<div>`s of the same article is not duplication — it is the TH ⇄ EN
switch.** All 76 posts have carried it since 2026-09-03 (Life and Hermes since
2026-09-01, the 20 AI Transformation posts from birth). `.l-th` and `.l-en` are two tracks
of one article behind a visually hidden checkbox, and `display: revert` — never `block` —
is what keeps `<span>` pairs inline. The navigation belongs to neither track: chip strips,
`.post-nav` labels, the ordinal badge and the card titles stay monolingual on purpose,
because INV-03, INV-10 and `gen_feed.py` read them with regexes that concatenate or
truncate on a nested tag. **A missing `.l-en` track is a defect, not an exception** —
`check_visibility.py` S1 keys off the substring `class="l-en"` and demands
`inLanguage: ["th","en"]` to match it.

**`git-branching.html` is the chain head and now has a real `.post-nav`.** Until
2026-08-26 every doc said it "has no nav by design" and the `cicd-pipeline.prev →
git-branching` edge was baselined as intentional. That claim was wrong: the file carried
a hand-rolled, inline-styled "Next →" to `cicd-pipeline.html` with no `.post-nav`
classes, invisible to both linters. Commit `24564b0` replaced it with the house block —
`prev "./"` ("Back to all posts", newly authored to mirror how the tail ends) and `next
cicd-pipeline.html` with the card title verbatim. The chain terminates at both ends with
`"./"` (`CHAIN_TERMINAL_PREV` / `CHAIN_TERMINAL_NEXT`); `CHAIN_HEAD` and every head
exemption are gone from both linters, so the 24-node chain verifies end to end.

**Two `#series-openclaw` cards used to wear DevOps chrome — they no longer do.**
`claude-code-architecture.html` (`Related` / `See also` block) and
`openclaw-memory-architecture.html` (`prev` grafted onto `deployment-hosting.html`) had
their `.post-nav`-shaped blocks deleted, markup and CSS, on 2026-08-26 (`f5e53fb`, owner
decision). Both are standalone no-nav posts now, listed in `NO_NAV_POSTS` in both
linters. The cost: `claude-code-architecture` lost its only links to `openclaw-101` and
`web-architecture`. Do not restore either block — INV-17 fails an OpenClaw card with
`.post-nav` chrome.

**Six posts have no nav block of any kind.**
`beyond-plugins.html`, `claude-code-architecture.html`, `idle-self-improvement.html`,
`obsidian-ai-jarvis.html`, `openclaw-memory-architecture.html`, `openclaw-migration.html`.
They are standalone pieces, not series entries — all six are `#series-openclaw` cards.
The nav partition is exactly **46 series-nav + 24 post-nav + 6 none = 76**, where the 46
is 20 AI Transformation + 10 Hermes + 9 Life + 7 numbered OpenClaw.

**The AI Transformation strip nests, and that is not drift.** Its 20 chips sit in four
labelled `.series-links__group` blocks inside `.series-links--grouped`, unlike the flat
`.series-links` the other three strips use. INV-03d exists because the old `RE_SNAV`
parser stopped at the first `</div></div>`; `Site._parse_navs` walks div depth via
`series_nav_body()` now. Do not "normalise" the grouped strip flat, and do not simplify
the walker back into a regex.

**No cover is shared.** `github-actions-cover.jpg` and `monitoring-cover.jpg` were each
borrowed by a second post until 2026-08-26, when `vibe-coding-devops-process` and
`openclaw-memory-architecture` got dedicated art drawn by `scripts/make_cover.py`. INV-07a
has no baseline entry; a re-used cover fails the build. All 76 post covers are drawn today,
one `covers.tsv` row each, and `make_cover.py --check` rejects a repeated motif outright.

**12 of the 76 posts deliberately do not use `<slug>-cover.jpg`.** `iac-cover.jpg`,
`auth-cover.jpg`, `sre-cover.jpg`, `cicd-cover.jpg`, `linux-cli-cover.jpg`,
`api-lifecycle-cover.jpg`, `security-cover.jpg`, `gitops-cover.jpg`,
`kubernetes-cover.jpg`, `monitoring-cover.jpg`, `networking-cover.jpg`,
`testing-cover.jpg`. INV-07d only fires when a correctly-named file *exists* and the post
ignores it, so these are legal; renaming them to match the slug breaks two references for
zero gain.

**`deployment-hosting.html` has one `<h1>`** — the duplicate inside the article body was
deleted by the 2026-08-26 metadata sweep. INV-11 fails any post with `h1 != 1`.

**`images/` has 0 orphans** — the 9 template leftovers were deleted on 2026-08-26 (INV-06a
now also walks the repo root). 195 files today. Not every `*-cover.jpg` belongs to a post:
`libraries-in-transformation-cover.jpg` is referenced from `publications/index.html`, and
the eight `-cover-en` / `-cover-th` / `-cover-front` / `-cover-back` faces belong to the
four `books/` titles. INV-06a walks every page, so none of them is an orphan.

## Standing drift — real inconsistencies, not blockers

There is none. Every row that used to sit here is one form on disk, guarded at fail or
warn level with no baseline entry, so a new post that deviates is reported as new:

| Thing | On disk (76 posts) | Use in new posts | Guard |
|---|---|---|---|
| Header | `<nav class="blog-nav">` with `href="./"` ×76 | that block | INV-29 |
| Footer container | `<footer class="blog-footer">` ×76 | `<footer class="blog-footer">` | INV-16 |
| Copyright | `© 2026` (literal `©`, never `&copy;`) ×76 | `© 2026` | INV-15 |
| `<meta name="description">` | present in all 76 (all 86 pages) | always write one | INV-14 / INV-27 |
| `<html lang>` | `th` ×76; the 10 English pages are the 6 index pages + 4 `books/` detail pages | `th`, and never flip it — the EN track is `lang="en"` wrappers | INV-13 |
| Bilingual switch | `class="l-en"` ×76, `lang-switch-box` ×76, `og:locale:alternate` ×76 | all three, in one commit | `check_visibility.py` S1 |
| `.series-nav` `<h3>` | 4 strips, one heading each: `📚 OpenClaw for Organizations 2026` ×7, `⚡ Hermes Agent in Practice 2026` ×10, `🌅 Life Thought &amp; Philosophy 2026` ×9, `🧭 AI Transformation for Organizations 2026` ×20 | the emoji form of the series you are joining | INV-03b (the 7) / INV-03c (the other three) |
| `.post-nav` container | `<div>` ×24, `<nav>` ×0 | `<div class="post-nav">` | INV-04c |
| `.post-nav__dir` wording | `← Previous`/`Next →` everywhere | the arrows | INV-04d |
| OpenClaw badge | `.post-hero__tag` "OpenClaw for Organizations 2026 • Post #N" ×7 | that form | INV-20a/20b/20c |
| `post-hero__series` text | `DevOps & Vibe Coding 2026` ×21 + `DevOps &amp; Vibe Coding 2026` ×2; `Life Thought &amp; Philosophy 2026` ×9; `AI Transformation for Organizations 2026 • Post #N` ×20; `Hermes Agent in Practice 2026 • Post #N` ×10; `AI Developer Tools 2026` ×1 (`claude-code-architecture`) | literal `&`; add `• Post #N` only in a numbered series | — |
| `.post-series-footer` | a `.l-th`/`.l-en` span pair inside one `<div>`, ×61 | copy the pair from the nearest sibling in the same series | — |

**Note on the copyright row:** `check_site.py`'s `RE_COPYRIGHT` matches only a literal `©`,
so an `&copy;` entity reads to INV-15 as "no copyright at all". That is why the sweep
settled on the literal character; write it that way.

**The `:root` row is gone: it is no longer drift.** `6670480` landed the canonical block
in every post (24 tokens then; **29 today**, after the 2026-08-26 re-key to the book
covers), and INV-22 PASSes. Always keep it, byte-identical. Per-post topic accents are
added *after* it and are the one allowed exception — `--docker-blue`, `--sky`, `--orange`,
`--teal`, `--purple-light`, and `--coral` on all 20 AI Transformation posts.

**`.post-nav__title` labels: 0 stale.** Eight used to disagree with their target's
`card__title` (worst case: `devops-security.html` calling `linux-command-line.html`
"Linux & Shell Essentials", a title that post never had). Three went with the grafted
posts' navs and five were rewritten to the card title verbatim on 2026-08-26 (`73032cb`).
Both linters agree at 0 (`verify-wiring.py` warns; `check_site.py` INV-10 warns), and
`verify-wiring.py`'s `norm()` now strips tags like `check_site.norm_title`, so they
compare the same string.

`verify-wiring.py` was **blind to this entire class of drift** until 2026-08-10: it
matched `<h2 class="card__title">` against cards that Task 11 had made `<h4>`, so it read
0 titles and printed CLEAN. It now matches any `h1`–`h6` and hard-fails a card whose title
heading it cannot find at all. If the two tools ever disagree on this list, one of them has
gone blind again — do not assume the quieter one is right.

Copy the two labels adjacent to any post you insert from the cards verbatim.

## Fixed since this file was written — do not re-report

**`blog/index.html`'s dead mobile menu is gone.** It used to render a
`<button class="nav__hamburger">` with no handler in a file with zero `<script>`. Task 9
(`ad3c42d`, `c25c682`) replaced it with the pure-CSS `.nav__toggle` checkbox +
`.nav__burger` label pattern now shared by **all 10 island-chrome pages** — `blog/index.html`,
the four other section indexes, the four `books/` detail pages and `404.html`.
`check_site.py` INV-12 verifies every toggle is wired and has **no baseline entry**, so a
regression will fail the build. `grep -rn 'nav__hamburger' --include='*.html' --exclude-dir=.claude .` returns
`index.html` only, and since `script.js` was deleted (2026-08-26) that one is an `href="#menu"` anchor, not a JS button.

(One mobile-nav defect does survive, in a file this skill rarely touches:
`blog/obsidian-ai-jarvis.html` hides `.nav__links` at ≤768px with no toggle at all. See
a11y-perf R2.)

**`openclaw-production.html`'s legacy `<section class="series-nav">`** — listing five
posts that never existed, invisible to `RE_SNAV` — was deleted on 2026-08-26 (`01332eb`).

## Still genuinely broken and worth telling the user about

Nothing from the old list survives: the two-`<h1>` post (INV-11) and the double-booked
covers (INV-07a) were both fixed on 2026-08-26 — see above.

**`data-reveal` does nothing inside `blog/`.** `CLAUDE.md` says to add `data-reveal` for
scroll-triggered fade-in, but the handler lived in `script.js`, which only `index.html`
loaded — and `script.js` itself was deleted on 2026-08-26 (`bb9c7dc`; the site is
zero-JavaScript, INV-38). `grep -o 'data-reveal' blog/index.html | wc -l` returns 0. Do not
add `data-reveal` attributes to blog pages expecting animation.
