# Research ledger — post #1 `hermes-desktop-install`

**Series** Hermes Desktop Hands-On 2026 (`series-hermes-desktop`)
**Post** #1 — Install & First Run
**Written** 2026-09-07
**Access date** 2026-09-07 (every source below was re-fetched in this writing run, not taken from the research pack)
**Sources fetched** 15 cited + 5 fetched-but-uncited (listed under *Fetched but not cited*)

> **Binding rule:** the post may not contain a number, date, command, path, quotation or URL
> that does not appear in this ledger.

Fetch method: `curl` direct to `raw.githubusercontent.com` / the live product page (verbatim bytes,
no summariser in the loop); `gh api` for the GitHub Releases endpoint (the unauthenticated API was
rate-limited); `curl -sI` for the installer HTTP headers; `spctl` + `codesign` on the downloaded
`.dmg` (the file was deleted after inspection).

---

## Sources

| [N] | Tag | Title | URL | Publisher | Published | Accessed | Supports |
|---|---|---|---|---|---|---|---|
| 1 | Docs | Hermes Desktop (docs page, Markdown source on `main`) | `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/desktop.md` | Nous Research | branch `main` (undated) | 2026-09-07 | §1 definition + architecture; `HERMES_HOME`; §2 Electron ~114 MB + mirror self-heal; §3 `hermes desktop` description and flags, mic prompt; §4 Choose provider later, Settings → Providers, Local Models view, xAI Grok OAuth, composer picker vs Settings → Model; §5 chat-surface list, status bar, YOLO warning; §6 MCP/Agents/Command Center; §7 `desktop.log`, `hermes logs gui -f`, the two reset commands, "the same layout a CLI install uses" |
| 2 | Docs | Installation | `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/getting-started/installation.md` | Nous Research | branch `main` | 2026-09-07 | §2 prerequisites; §3 all three install commands + install-layout table + `source ~/.bashrc` + `command not found` remedy; §4 `hermes setup --portal`; §7 `hermes doctor` |
| 3 | Docs | Platform Support | `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/getting-started/platform-support.md` | Nous Research | branch `main` | 2026-09-07 | §2 the four Unsupported entries and the "PRs to fix them will *not* be accepted" line; Tier 1 membership |
| 4 | Docs | Hermes Desktop: Native AI Agent App for Mac, Windows & Linux (product page) | `https://hermes-agent.nousresearch.com/desktop` | Nous Research | live page | 2026-09-07 | §1 MIT/free FAQ line and the footer version string; §2 platform labels + "No account is needed to run the base app"; §3 button labels and download links |
| 5 | Release | Hermes Agent v0.21.0 (v2026.8.31) — latest-release record | `https://api.github.com/repos/NousResearch/hermes-agent/releases/latest` | Nous Research / GitHub | 2026-08-31T19:29:49Z | 2026-09-07 | §1 the version-naming callout: release name, tag, date, and zero assets |
| 6 | Docs | Configuration | `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/configuration.md` | Nous Research | branch `main` | 2026-09-07 | §4 `auth.json` vs `.env`; §6 on-disk column; §7 the `ls ~/.hermes` expected listing |
| 7 | Docs | CLI Commands | `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/reference/cli-commands.md` | Nous Research | branch `main` | 2026-09-07 | §6 every CLI-twin cell; §7 `hermes --version`, `hermes doctor [--fix]`, the `hermes dump` sample output, the `hermes logs` table row for `desktop` |
| 8 | Docs | Security | `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/security.md` | Nous Research | branch `main` | 2026-09-07 | §5 `approvals.mode` default `smart`, the three modes and their behaviour |
| 9 | Docs | Windows (Native) Guide | `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/windows-native.md` | Nous Research | branch `main` | 2026-09-07 | §3 Windows steps 1, 2, 3, 4, 5 — no admin rights, `%LOCALAPPDATA%\hermes`, User PATH, GUI calls `install.ps1`, shared install/data dirs |
| 10 | Release | `scripts/install.sh` (source on `main`) | `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh` | Nous Research | branch `main` | 2026-09-07 | §2 the eleven install-stage titles and the `--include-desktop` gating comment |
| 11 | Docs | `Hermes-Setup.dmg` (the served installer binary) | `https://hermes-assets.nousresearch.com/Hermes-Setup.dmg` | Nous Research | Last-Modified Sat, 06 Jun 2026 00:31:20 GMT | 2026-09-07 | §2 and §3 file sizes; §3 macOS step 2 signing/notarization status |
| 12 | Community | Hacker News — "Hermes Agent – Open-source AI agent with persistent memory" (the `hermes-agent.org` submission) | `https://news.ycombinator.com/item?id=48419000` | Hacker News | submitted 2026-06-05; cited comments 2026-06-09 | 2026-09-07 | §9 look-alike alert: the "Why is the domain not in nousresearch.com?" comment and the quoted terms-of-service line |
| 13 | Community | hermes-ai.net — "Hermes Agent Docs — Installation, Desktop & Multilingual Guide" | `https://hermes-ai.net/` | hermes-ai.net (unaffiliated) | live page | 2026-09-07 | §9 look-alike alert: the site's own "unofficial, independent community guide" / "not affiliated with Nous Research" self-description |
| 14 | Community | Hermes One — `fathah/hermes-desktop` README | `https://raw.githubusercontent.com/fathah/hermes-desktop/main/README.md` | fathah (community) | branch `main` | 2026-09-07 | §9 look-alike alert: project name and the "not affiliated to Nous Research" disclaimer |
| 15 | Release | `hermes_cli/linux_desktop_entry.py` (source on `main`) | `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/hermes_cli/linux_desktop_entry.py` | Nous Research | branch `main` | 2026-09-07 | §3 Linux step 5: `hermes.desktop` under the XDG applications directory |

**Tag mapping used in the post:** Docs → `ref-tag--standard` · Release → `ref-tag--study` ·
Issue → `ref-tag--law` (unused in this post) · Community → `ref-tag--synthesis`.

### Fetched but not cited

Read during verification, but nothing in the post rests on them alone:
`apps/desktop/package.json`, `apps/bootstrap-installer/src-tauri/hermes-setup.manifest`,
`hermes_cli/subcommands/gui.py`, `website/docs/user-guide/profiles.md`,
`website/docs/getting-started/updating.md`, `website/docs/user-guide/features/{cron,memory,skills}.md`,
`LICENSE`, `https://hermes-agent.org/terms-of-service/`.

---

## Verification record

| [N] | HTTP | What was checked | Discrepancy / note |
|---|---|---|---|
| 1 | 200, 54,936 B | Located each quoted sentence verbatim by line: the "native app built around the **same** agent…" paragraph (L9); `HERMES_HOME` + "the same layout a CLI install uses, which is why the two are interchangeable" (L308); "Choose provider later" (L171); Local Models view (L~160); xAI Grok OAuth (L163); "the only place that writes it" (Choosing a model); status-bar YOLO line; "The build downloads the Electron runtime (~114 MB)"; `hermes logs gui -f` and the two `rm` resets (L462–474); `hermes desktop` description + flag table (L291–305) | **`~/.local/share/applications/hermes.desktop` is NOT in this file** — grepped and confirmed absent. The claim was re-sourced to [15]. |
| 2 | 200, 9,866 B | Both one-liners verbatim; "### With the Hermes Desktop installer on macOS or Windows (recommended)"; the Install Layout table; the Prerequisites paragraph naming Git, curl, xz-utils, `g++`/`build-essential`; "For more diagnostics, run `hermes doctor`" | The doc links the installer at `https://hermes-agent.nousresearch.com/` (site root), while the direct asset URLs come from [4]. Both were checked to return HTTP 200. |
| 3 | 200, 4,302 B | The Unsupported bullet list quoted verbatim; Tier 1 / Tier 2 tables read in full | — |
| 4 | 200, 79,386 B | HTML fetched and tag-stripped; verified: page `<title>`, tagline, "macOS 12+ / Mac OS / Download desktop app", "Windows 10/11 / Windows / Download desktop app", "Any distro / Linux / Install via terminal", all five FAQ answers, footer "Hermes Agent v0.21.0 … MIT License · 2026". Download hrefs extracted: `…/Hermes-Setup.dmg?build=06402ecb7ca5` and `…/Hermes-Setup.exe?build=06402ecb7ca5` | The Linux `curl` command itself is not present in the served HTML (rendered client-side); the command in the post comes from [2] instead. The "macOS 12+" string sits **above** the button in the card, not under it — post wording adjusted to "that card is labelled". |
| 5 | 403 unauthenticated (rate limit), then 200 via `gh api` | `tag_name` = `v2026.8.31`; `name` = "Hermes Agent v0.21.0 (v2026.8.31)"; `published_at` = 2026-08-31T19:29:49Z; `assets` length = **0** | The unauthenticated `api.github.com` call returned "API rate limit exceeded"; the same endpoint through the authenticated `gh` CLI returned the record. |
| 6 | 200, ~ | The `~/.hermes/` directory tree code block read verbatim, including the comment "auth.json — OAuth provider credentials (Nous Portal, etc.)" | — |
| 7 | 200, 105,184 B | `hermes doctor [--fix]` section (L820); `hermes logs` log-file table (L1042+); `hermes serve` default port 9119 (L1668+); `hermes dump` example output; `hermes --version` (L100/L1811); `hermes journey` one-liner (L82); `hermes profile`, `hermes skills`, `hermes cron`, `hermes sessions`, `hermes plugins`, `hermes model` sections | **`hermes doctor` has no documented sample output** — only the `--fix` flag and a one-line description. The post says so explicitly and points readers to `hermes dump`, which *is* documented with a full example. There is no `hermes journey` top-level section, only the summary-table row; the post cites only what that row says. |
| 8 | 200, 44,275 B | The `approvals:` YAML block; the key table row `mode | smart | …`; the three-mode behaviour table; the YOLO Mode section | — |
| 9 | 200, ~ | "No admin rights required. The installer goes to `%LOCALAPPDATA%\hermes\` and adds `hermes` to your **User PATH** — open a new terminal after it finishes." (L26); the GUI-installer paragraph (L48); the numbered install steps naming uv/Python 3.11, Node.js 26, PortableGit | This page's one-liner points at `raw.githubusercontent.com/.../scripts/install.ps1`; the post uses the short `hermes-agent.nousresearch.com/install.ps1` form from [2], which was separately confirmed to return HTTP 200 (245,718 B). |
| 10 | 200, 170,273 B | `emit_manifest()` read verbatim (L320–333): the eleven stage titles in order, the conditional `desktop_stage` line, and the explanatory comment. `--include-desktop` help text at L185 | — |
| 11 | HEAD 200 (dmg), HEAD 200 (exe); GET 200 for the dmg | `content-length: 6752854` / `last-modified: Sat, 06 Jun 2026 00:31:20 GMT` (dmg); `content-length: 7946048` / `last-modified: Mon, 10 Aug 2026 20:24:15 GMT` (exe). Downloaded dmg sha256 `b61e047efe3059faf1c55fec3252e661f2d2a993a7a3eebf5cc6a9aa5c1790f5`. `spctl -a -vvv -t open --context context:primary-signature` → `accepted / source=Notarized Developer ID`. `codesign -dvvv` → `Identifier=Hermes-Setup-0.0.1-arm64`, `Authority=Developer ID Application: … (T2F6S8MF7C)`, `Authority=Developer ID Certification Authority`, `Authority=Apple Root CA`, `Notarization Ticket=stapled`, `TeamIdentifier=T2F6S8MF7C` | This **closes an open question** the research pack left open ("no codesign/signtool verification was run… Gatekeeper/SmartScreen behaviour is undocumented"). The signing identity is an individual's Developer ID, not one issued in the name "Nous Research"; the post cites the team ID only and does not name the individual. The Windows `.exe` was **not** signature-checked (no Windows host available). |
| 12 | 200 (Algolia item JSON) | Comment by `sergiotapia` 2026-06-09T02:12:13Z: "Actually until the team comments, this page seems suspect. Why is the domain not in nousresearch.com?"; comment by `gabrielsroka` 2026-06-09T02:22:54Z quoting the ToS line | The research pack described the disclaimer as "its operator replied". That is **not** what happened: the line is the site's own Terms of Service, quoted into the thread by a third commenter. The post states it that way. I additionally opened `https://hermes-agent.org/terms-of-service/` (HTTP 200) on 2026-09-07 and confirmed the sentence is still present verbatim. |
| 13 | 200 | Front-page text: "hermes-ai.net is an unofficial, independent community guide to Hermes Agent…" and "…net is an unofficial community site and is not affiliated with Nous Research." | Cited as evidence about itself only. |
| 14 | 200, 19,098 B | L44 "Hermes One is a community maintained native desktop app…"; L346 "This repo is not affiliated to **Nous Research**. This is a community maintained project." | Cited as evidence about itself only. This project binds `127.0.0.1:8642`, a different port from the official backend's 9119 — noted here but left out of the post to avoid confusion with the Hermes API server. |
| 15 | 200, 24,879 B | `DESKTOP_ENTRY_NAME = "hermes.desktop"` (L22); `_xdg_data_home()` defaulting to `Path.home() / ".local" / "share"` (L30–32); `desktop_entry_path()` returning `_xdg_data_home() / "applications" / DESKTOP_ENTRY_NAME` (L36–37); module docstring on the absolute `Exec=` | — |

---

## Claims and numbers

| Value | Source | Where it lands in the post |
|---|---|---|
| `Hermes-Setup.dmg` = 6,752,854 bytes ≈ **6.8 MB** | [11] HTTP `content-length` | Intro hook; §2 `.alert info`; §3 macOS step 1 "what you should see"; §9 takeaway "7–8 MB" |
| `Hermes-Setup.exe` = 7,946,048 bytes ≈ **7.9 MB** | [11] HTTP `content-length` | §2 `.alert info`; §9 takeaway |
| Electron runtime ≈ **114 MB** | [1] "The build downloads the Electron runtime (~114&nbsp;MB)" | §2 `.alert info`; §3 macOS step 4 |
| **Eleven** install stages, in order, "System prerequisites" → "Finish install", with "Build desktop app" second-to-last | [10] `emit_manifest()` | §2 `.alert info`; §3 macOS steps 3–5; §7 check 3 ("Prepare config and skills") |
| **macOS 12+**, **Windows 10/11**, **any Linux distro** | [4] product page; [3] Tier 1 table | §2 opener; §3 headings |
| `approvals.mode` default = **`smart`** | [8] key table | §5 "Why an approval prompt shows up" |
| `hermes serve` default port **9119** | [7] `hermes serve` section | §6 Gateways row |
| MEMORY.md / USER.md live in `~/.hermes/memories/` | [6] directory tree | §6 Memory row; §7 check 3 |
| Latest release: name "Hermes Agent v0.21.0 (v2026.8.31)", tag `v2026.8.31`, published **2026-08-31**, **0** assets | [5] | §1 💡 callout; §9 takeaway |
| `~/.hermes/` contains `config.yaml`, `.env`, `auth.json`, `SOUL.md`, `memories/`, `skills/`, `cron/`, `sessions/`, `logs/` | [6] | §6 table; §7 check 3 |
| Per-user install layout: code `~/.hermes/hermes-agent/`, binary `~/.local/bin/hermes` (symlink), data `~/.hermes/` | [2] Install Layout table | §3 Linux step 2 |
| Node.js **v26**, **Python 3.11**, ripgrep, ffmpeg installed by the installer; only **Git** required in advance on non-Windows; `curl` + `xz-utils` on Linux; `g++` / `build-essential` for the desktop app | [2] Prerequisites | §2 second paragraph; §3 Linux step 1; §3 Windows step 3 |
| `~/.local/share/applications/hermes.desktop` | [15] | §3 Linux step 5 |
| dmg is signed (Developer ID Application, team `T2F6S8MF7C`) and **notarized**, ticket stapled; `spctl` verdict "accepted / source=Notarized Developer ID"; identifier `Hermes-Setup-0.0.1-arm64` | [11], measured 2026-09-07 | §3 macOS step 2 |
| Windows installer needs **no admin rights**, installs into `%LOCALAPPDATA%\hermes\`, adds `hermes` to **User PATH** (new terminal required) | [9] | §3 Windows steps 1, 3, 4 |

### Quotations used verbatim in the post

- "The Hermes desktop app is a native app built around the **same** agent you get from the CLI and the gateway — same config, same API keys, same sessions, same skills, same memory. It is not a separate product or a lightweight clone." — [1]
- "the same layout a CLI install uses, which is why the two are interchangeable" — [1]
- "installs workspace Node dependencies, builds the current OS's unpacked Electron app, then launches that packaged artifact" — [1]
- "YOLO bypasses the dangerous-command approval prompts, so know what you're turning off" — [1]
- "Grok is a first-class OAuth provider in the launcher; sign in through the browser flow like the other OAuth providers" — [1]
- "installs and manages an on-device llama.cpp runtime" — [1]
- "the only place that writes it" — [1]
- "gets you to your first message in seconds" — [1]
- "Electron desktop app — boot, backend spawn output, and recent Python tracebacks" — [7]
- "it will tell you exactly what's missing and how to fix it" — [2]
- "logs you in, sets Nous as your provider, and turns on the Tool Gateway in one command" — [2]
- "PRs to fix them will *not* be accepted" — [3]
- "No account is needed to run the base app." — [4]
- "Hermes Desktop is the open-source Hermes Agent under an MIT license, free to download and use." — [4]
- "the signed bootstrap installer (Hermes-Setup) passes it so a GUI install ends up with a launchable app" — [10]
- "--include-desktop  Also build the desktop app" — [10]
- "No admin rights required" · "on first launch the GUI calls `install.ps1` under the hood" · "share the same `%LOCALAPPDATA%\hermes\hermes-agent` install and `%LOCALAPPDATA%\hermes` data directory — switch between the GUI and the CLI freely" — [9]
- "Why is the domain not in nousresearch.com?" · "We are not affiliated with Nous Research or any other organization referenced on this site" — [12]
- "an unofficial, independent community guide to Hermes Agent" — [13]
- "This repo is not affiliated to **Nous Research**. This is a community maintained project." — [14]

---

## Dated statuses

True as of **2026-09-07**; re-verify before editing this post.

- Latest Hermes Agent release: **v0.21.0**, tag `v2026.8.31`, published 2026-08-31, **zero attached assets** [5].
- The product page footer reads "Hermes Agent v0.21.0" and its download links carry `?build=06402ecb7ca5` [4].
- `Hermes-Setup.dmg` Last-Modified 2026-06-06; `Hermes-Setup.exe` Last-Modified 2026-08-10 — both older than the `?build=` commit the page advertises, because the bootstrapper resolves the ref at run time [11].
- The `.dmg` is Developer-ID-signed and Apple-notarized with the ticket stapled; its identifier names **arm64** [11].
- `approvals.mode` default is `smart` [8]; the Desktop's status bar carries a per-session YOLO toggle [1].
- `hermes doctor` is documented with `--fix` only; **no sample output is published** [7].
- Unsupported install paths: AUR, macOS on x86 (Intel), `pypi`, `brew` [3].

---

## Do not assert

Things I looked for and could **not** verify, or deliberately left out:

- **The first-run wizard's screens.** The docs never enumerate them. Only "Choose provider later"
  and "gets you to your first message in seconds" are documented [1]. The post says this in the
  open rather than inventing a screen order. The phrasing "OAuth-first setup and API-key fallback"
  that circulates in secondary write-ups comes from the original desktop PR description, **not**
  from the current docs — it is not quoted.
- **A "Run models locally" button in onboarding.** Not documented. What *is* documented is the
  Settings → Providers pane's **Local Models** view [1], which is what the post points at, with the
  detail deferred to post #2.
- **What the status bar shows after "Choose provider later".** Community walkthroughs report the
  bottom-left indicating the gateway still needs a provider, but no source I fetched in this run
  says so, so the post does not claim it — it says only that the app drops you into the chat with
  no model configured and shows where to set one.
- **Installer button labels ("Install Hermes", "Launch Hermes").** These come from community video
  transcripts in the research pack, which I did not re-fetch. Replaced throughout by the install
  script's own **stage titles** [10], which are primary and verbatim.
- **`Hermes-Setup.exe` signature / SmartScreen behaviour.** Not checked — no Windows host. Only the
  `.dmg` was inspected. The post makes no claim about SmartScreen.
- **Whether the `.dmg` is arm64-only or universal.** The code-signing identifier is
  `Hermes-Setup-0.0.1-arm64`, which is suggestive but is a signing identifier, not a proof of the
  Mach-O slice set. The post says only that the identifier names arm64, in the reference note.
- **`apps/desktop/package.json` still declares `"version": "0.17.0"`** while the agent is at 0.21.0.
  Verified in this run, but omitted from the post: it needs a 16th source and changes nothing the
  reader does. The version-naming callout rests on [4] and [5] instead.
- **"Public preview" status.** The 2026-06-02 announcement used the phrase; nothing on the current
  product page or docs does. The post never calls Hermes Desktop a preview.
- **`hermes doctor` output.** Not published anywhere I could fetch, so the post does not describe
  what it prints and offers `hermes dump` as the documented alternative [7].
- **`connections.json` / Electron `userData` paths** for the registered-gateway registry. Named in
  the research pack, but absent from `desktop.md` as fetched today, so the §6 Gateways row cites
  `~/.hermes/.env` on the backend host instead.
- **`~/.hermes/profiles/<name>/` as the profile path.** It is in `profiles.md`, which I read but did
  not cite; the §6 Profiles row therefore says "a separate home directory per profile", matching the
  wording in [7].
- **CVE-2026-10223.** Out of scope for an install post, and no Nous source maps it to Desktop.
- **Nous Portal prices / tier contents.** Not asserted; the post says only that no account is
  required [4].
