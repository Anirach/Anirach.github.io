# Runbook — keeping "Latest Updates" current on anirach.com

**Audience:** an AI agent (OpenClaw) maintaining this site for Dr. Anirach Mingkhwan, unsupervised.
**Repo:** `Anirach/Anirach.github.io` · **Live:** https://anirach.com · **Branch:** `main` (pushing deploys within ~3 min)

This site has **no build system, no CMS, no database**. A news item is hand-written HTML in two
separate files, and nothing regenerates one from the other. That is why this runbook exists.

---

## The three rules that matter

**Rule 1 — an item lives in two places, and they must agree.**

1. `news/index.html` — the full timeline (every item, newest first)
2. `index.html` — the "Latest updates" strip (the **3 newest only**, same order)

This has already broken in production: the homepage showed Jul 2026 / Dec 2025 / **Nov 2024** while
the news page's third-newest was **Oct 2025**. An entire update was invisible from the front page.

**Rule 2 — nothing goes on this page without a source you actually opened.**

This is a professor's public CV. A fabricated publication, role, or award is the worst possible
outcome — worse than the page being out of date. No automated check can tell a true item from an
invented one, so the gate is procedural: **every item must carry a source comment**, and
`check-news-sync.py` fails if one is missing. Omitting a source now breaks the build; inventing one
means writing a deliberate falsehood into a file that is auditable forever.

**Rule 3 — the item counters must match reality.**

Four labels are hand-typed: `news/index.html`'s `"N updates"`, `publications/index.html`'s
`"N chapters"` (this label lived on `books/index.html` until the 2026-08-23 split of Books into
Publications + Novels), and `books/index.html`'s `"N novel"` and `"N complete"`. All four drift
silently whenever an item is added without touching the label — a split
commit nearly desynchronised them once. The gate recomputes all four from the actual item counts
(after stripping HTML comments, so a commented-out card cannot satisfy a label) and
fails if any disagrees, so adding an item means updating its label in the same commit.

---

## Step 1 — Find out whether there is anything new

| Source | What it yields | URL |
|---|---|---|
| Google Scholar, sorted by date | New papers and chapters — highest yield | `https://scholar.google.com/citations?hl=en&user=htY3F_IAAAAJ&view_op=list_works&sortby=pubdate` |
| DBLP | Cross-check venue, volume, pages | `https://dblp.org/search?q=Mingkhwan` |
| IEEE Xplore author page | IEEE-published work | `https://ieeexplore.ieee.org/author/37269079200` |
| Springer "Advances in Real-Time and Autonomous Systems" (AUTSYS) | He publishes here yearly | search on `https://link.springer.com/` |
| DEFI conference (VKU, Da Nang) | Programme-committee roles | `https://defi.vku.udn.vn/` |
| Thailand Library Consortium (TLC) | Invited talks, tied to his Springer book | `https://tlc.uni.net.th/` |
| FITM KMUTNB | Faculty events, Thai-language | `https://www.fitm.kmutnb.ac.th/` |

Two fetch quirks, so you don't misread them as dead:
- **IEEE Xplore returns HTTP 418 to plain `curl`** — it blocks non-browser agents. Use a
  browser-like fetch. 418 here means "bot-blocked", not "gone".
- **The DEFI host is intermittently unreachable.** Retry two or three times before concluding it
  is down.

Then check the item is not already present — compare against the dates and titles already in
`news/index.html`.

> ⚠️ **His Google Scholar profile contains at least one mis-attributed paper** ("The Risk and Return
> Relation in Bitcoin Spot and Futures Intraday Returns" — not his work). Scholar auto-attributes by
> name match. **Confirm authorship on the publisher's own page before adding anything.**

---

## Step 2 — Add the item to `news/index.html`

Insert immediately after the `<!-- To add news: ... -->` comment, so the newest item is first.
Copy this shape exactly — **including the source comment**:

```html
<!-- source: https://the-page-you-actually-verified | verified YYYY-MM-DD -->
<article class="card card--row">
  <div class="card__tags">
    <span class="card__tag card__tag--date">Mon YYYY</span>
  </div>
  <div class="card__body">
    <h3 class="card__excerpt">English sentence describing what happened, with <em>Titles In Italics</em> and full detail (venue, volume, pages).</h3>
    <p class="card__excerpt"><span lang="th">ประโยคภาษาไทยที่อธิบายเรื่องเดียวกัน เขียนให้เป็นธรรมชาติ ไม่ใช่แปลตรงตัวจากภาษาอังกฤษ</span></p>
    <div class="card__footer">
      <a href="https://…" target="_blank" rel="noopener" class="card__link">Short link label →</a>
    </div>
  </div>
</article>
```

- **The `<!-- source: … -->` comment is mandatory.** It records what you verified against, which is
  not always the same as a link worth showing readers — two existing items are sourced to a Wayback
  snapshot and a conference speaker page that are not reader-facing. Date format `YYYY-MM-DD`.
- **`.card__footer` is optional** — omit the whole `<div>` when there is no link a reader would
  want. It is not a substitute for the source comment.
- **Date format is `Mon YYYY`** (`Jul 2026`, `Dec 2025`). The checker matches these strings.
- **Strict newest-first.** Re-sort if needed. Watch the trap: Dec 2025 is newer than Oct 2025.
- **Both languages, always.** English in the `<h3>`, Thai in the `<p>` inside `<span lang="th">`.
  Write real Thai; do not translate word for word.
- **The `<h3>` is required**, not decorative — it is what makes the timeline navigable by heading.
  The page's ladder is `h1 → h2 → h3` and must stay that way.
- Every external link needs `target="_blank" rel="noopener"`.

---

## Step 3 — If the item is now in the top 3, update the homepage

Only if it is among the three newest. If it is older than all three, **skip this step entirely** —
`news/index.html` is the only file that changes.

In `index.html`, find `<ul class="latest__list">` and make its three `<li>` rows match the three
newest news items, in the same order. **Exactly three.** Delete the row that fell off the bottom.

```html
<li data-reveal><span class="latest__date">Mon YYYY</span><a href="news/">One-line summary — shorter than the news page wording</a></li>
```

- Keep `data-reveal`, or the row will never fade in and stays invisible.
- The link always points at `news/`, never at an external site.
- English only here; the Thai lives on the news page.

---

## Step 4 — Never do these

- ❌ **Never invent or estimate a fact.** If you cannot verify it, do not publish it — see step 6.
- ❌ **Never fabricate a source URL.** If nothing resolves, the item does not go on the site.
- ❌ **Never add a citation count, download count, or h-index without a date label**
  (`"68 citations (Springer, Aug 2026)"`). An undated number silently becomes false.
- ❌ Never add JavaScript to `news/index.html` or to `index.html`'s news sections.
- ❌ Never edit anything under `blog/` for a news item — different system.
- ❌ Never change the nav, footer year, or `:root` token block while adding news.
- ❌ Never `git push` with any step-5 check failing.

---

## Step 5 — Verify

Run all three from the repo root. All must pass.

```bash
python3 docs/openclaw/check-news-sync.py                        # sync + provenance + counters gate
python3 .claude/skills/site-check/scripts/check_site.py         # 49 cross-file integrity checks
python3 .claude/skills/blog-post/assets/verify-wiring.py        # blog wiring (should be untouched)
```

| Command | Expected |
|---|---|
| `check-news-sync.py` | `PASS`, exit 0 — runs three sections: SYNC, PROVENANCE, COUNTERS (four counters) |
| `check_site.py` | exit 0, `0 new, 55 known` — "known" is pre-existing debt; **`0 new` is what matters** |
| `verify-wiring.py` | `CLEAN` |

`check-news-sync.py` exit codes: **0** pass · **1** a real problem (it names it) · **2** the checker
itself could not run, usually because the markup was renamed. **Exit 2 is not a pass** — fix the
patterns in the script before continuing.

If `check_site.py` reports anything as **new**, you caused it. Fix before pushing.

Also confirm each link you added resolves:

```bash
curl -s -o /dev/null -w '%{http_code}\n' -L --max-time 20 "<each url>"   # expect 200
```

If you have browser tooling, render `news/index.html` and `index.html` at 1280px and 375px and
confirm the new item appears correctly with no horizontal scrollbar. If you are headless, skip it
and say so in the commit — the three checks above are the binding gate.

---

## Step 6 — Publish, or escalate

**If everything verified**, commit citing the source in the message, then push:

```bash
git add news/index.html index.html
git commit -m "news: <one line describing the item>

Source: <the URL you verified against>"
git push origin main
```

Confirm it landed after ~3 minutes:

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://anirach.com/news/     # 200
curl -s https://anirach.com/ | grep -c "Mon YYYY"                      # 1 if it is in the top 3
```

**If you could not verify something**, do not publish and do not guess. Open a GitHub issue on
`Anirach/Anirach.github.io` titled `Unverified news item: <short description>`, with what you found,
where you found it, and what you could not confirm. An issue Dr. Mingkhwan can dismiss in ten
seconds is always better than a wrong line on his CV.

```bash
gh issue create --repo Anirach/Anirach.github.io \
  --title "Unverified news item: <short description>" \
  --body "Found: <what> · Source seen: <url or 'none'> · Could not confirm: <what exactly>"
```

---

## Reference — current state

`news/index.html` holds **7 items** — Sep 2026, Aug 2026, Jul 2026, Dec 2025, Oct 2025, Nov 2024, May 2024 — each with a source comment.
Below them sits a separate **career timeline** block: that is biography, not news. Do not add news
items to it and do not give it date chips; the checker deliberately ignores rows without one.

The three homepage rows are Sep 2026 / Aug 2026 / Jul 2026.

`publications/index.html`'s Chapters section holds **8 chapters** with its own `"N chapters"`
label, and `books/index.html` (Novels) carries `"1 novel"` and `"2 complete"` — the
checker verifies all three too.

Re-derive rather than trusting this paragraph:

```bash
grep -o 'card__tag--date">[^<]*' news/index.html   # every news date, in page order
grep -o 'latest__date">[^<]*' index.html            # the homepage strip
grep -c '<!-- source:' news/index.html              # provenance comments; must equal the item count
```

---

## If the markup ever changes

`check-news-sync.py` matches on `latest__date`, `card__tag--date`, the `<!-- source: … -->`
comment, and the four `series-count` labels (`"N updates"` on news, `"N chapters"` on
publications, `"N novel"` and `"N complete"` on books). If a redesign renames any of them the script exits **2** with `found no dates — the markup
changed`, rather than silently reporting success. Update its patterns in the same commit as the
markup change.

This failure mode — a checker whose pattern stops matching and therefore passes on an empty set —
has occurred twice in this repository. Treat "0 problems found" as suspicious until you have seen
the checker report a real problem at least once.

---

## Dated content that expires

Two things on this site are written around a date that has not happened yet, and both go stale
silently the day after. Nothing computes them, and no gate can — a checker cannot know what the
copy *should* say once the event is over.

**The Last Lecture — Saturday 19 September 2026.** After that date, revise all four of these
in one commit:

| Where | What is date-bound |
|---|---|
| `books/one-day-of-light.html` | the `Event` JSON-LD block in `<head>` — past-tense it or remove it |
| `books/one-day-of-light.html` | `<meta name="description">` **and** the `og:description` in the `<!-- social -->` block — both are written around the upcoming event |
| `index.html` | the `.latest` strip line announcing the lecture |
| `news/index.html` | the corresponding news item |

The `og:description` matters more than it looks: Facebook and LINE cache the card on first
scrape, so a stale description outlives the edit until someone re-scrapes the URL through the
Facebook Sharing Debugger. Do that as the last step.

**Adding a new page?** It needs a `<!-- social -->` block in `<head>` and a `<loc>` entry in
`/sitemap.xml`. `check_site.py` INV-27 fails the build without the first; nothing but this
sentence enforces the second.

```bash
python3 .claude/skills/site-check/scripts/check_site.py --check INV-27
grep -c '<loc>' sitemap.xml    # must equal the page count (47 today, excluding 404.html)
```
