# Research ledger — post #5 `hermes-desktop-skills-mcp`

- **Series** — Hermes Desktop Hands-On 2026 (`scripts/series/hermes-desktop.json`), post #5 of 7
- **Post** — "Skills, MCP & Memory — ต่อความสามารถให้ agent" / "Skills, MCP & Memory — Extending
  What the Agent Knows"
- **Written** — 2026-09-07 (a Thai draft from an interrupted earlier run was fact-checked against
  re-fetched primaries, corrected, and mirrored into the English track; see **Corrections** below)
- **Access date** — 2026-09-07. Every documentation page, the release body and both video
  identities were re-fetched on this date. The upstream research slices
  (`angles/features.md`, `angles/community.md`, dated 2026-09-06) were used to decide *what* to
  check, never as a citation — with one explicit exception recorded under **Do not assert**.
- **Sources fetched** — 15 (13 cited, 2 verification-only)

> **Binding rule:** the post may not contain a number, date, command, path, quotation or URL that
> does not appear in this ledger.

## Sources

| [N] | Tag | Title | URL | Publisher | Published | Accessed | Supports |
|---|---|---|---|---|---|---|---|
| [1] | Docs | Skills System | https://hermes-agent.nousresearch.com/docs/user-guide/features/skills (raw: `.../main/website/docs/user-guide/features/skills.md`) | Nous Research | main branch, undated | 2026-09-07 | §1 the "on-demand knowledge documents" definition, agentskills.io, `~/.hermes/skills/` as "primary directory and source of truth", the Level 0 tuple and ~3k tokens; §2 every `hermes skills` line, the hub source table, the SKILL.md frontmatter and four headings, the directory tree, automatic slash commands, `opt-out`; §5 the Skill row |
| [2] | Docs | Hermes Desktop | https://hermes-agent.nousresearch.com/docs/user-guide/desktop (raw: `.../main/website/docs/user-guide/desktop.md`) | Nous Research | main branch, undated | 2026-09-07 | §1 "same config, same API keys, same sessions, same skills, same memory"; §2 the Skills tab + Install button quotation, `Ctrl+\`` terminal, management panes, `Cmd/Ctrl+K` palette; §3 "MCP servers" among settings panes; §4 Memory Graph / Star Map, All / Used / Learned, "skills are archived, memories removed", Settings → Memory & Context; §5 desktop-plugin path, Settings → Plugins, Agent plugins; §6 the whole status-bar / Context Usage paragraph |
| [3] | Docs | MCP (Model Context Protocol) | https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp (raw: `.../main/website/docs/user-guide/features/mcp.md`) | Nous Research | main branch, undated | 2026-09-07 | §3 the Nous-approved catalog section, both YAML examples, `mcp_<server_name>_<tool_name>`, `mcp-<server>` toolset, `/reload-mcp` and the frozen tool set, the Quick-start prompt, `node --version` / `npx --version`, `enabled: false`, `tools.include` / `tools.exclude` + precedence + the cloudflare figure, `hermes mcp configure`; §6 the same filter knobs |
| [4] | Docs | CLI Commands Reference | https://hermes-agent.nousresearch.com/docs/reference/cli-commands (raw: `.../main/website/docs/reference/cli-commands.md`) | Nous Research | main branch, undated | 2026-09-07 | §2 `hermes skills list` / `config` descriptions; §3 `hermes mcp test|list|add|serve|catalog|install|configure`; §4 `hermes memory setup|status|off` and `hermes plugins` → Provider Plugins → Memory Provider |
| [5] | Docs | Security | https://hermes-agent.nousresearch.com/docs/user-guide/security (raw: `.../main/website/docs/user-guide/security.md`) | Nous Research | main branch, undated | 2026-09-07 | §3 the whole "Secrets do not leak down by themselves" alert — the eight passed-through variables plus `XDG_*`, the `env:` exception, and the `[REDACTED]` pattern list |
| [6] | Docs | Persistent Memory | https://hermes-agent.nousresearch.com/docs/user-guide/features/memory (raw: `.../main/website/docs/user-guide/features/memory.md`) | Nous Research | main branch, undated | 2026-09-07 | §1 and §4 both character caps and token estimates, the frozen snapshot, the MEMORY prompt block, the `memory:` config block, `display.memory_notifications`, the both-off behaviour, `hermes journey list|edit|delete` and the id form, `write_approval` + `/memory …`, `skills.write_approval` + `/skills …`, the "One agent per Hermes home" caution, the 80 % advice, "Fixed per session (~1,300 tokens)" |
| [7] | Docs | Memory Providers | https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers (raw: `.../main/website/docs/user-guide/features/memory-providers.md`) | Nous Research | main branch, undated | 2026-09-07 | §4 "ships with 8 external memory provider plugins", the eight names, one-at-a-time with built-in always alongside, `hermes memory setup|status|off`, `memory.provider:`, and the nine-row comparison table whose extra row is Memori |
| [8] | Docs | Slash Commands Reference | https://hermes-agent.nousresearch.com/docs/reference/slash-commands (raw: `.../main/website/docs/reference/slash-commands.md`) | Nous Research | main branch, undated | 2026-09-07 | §2 `/learn`, `/reload-skills`; §4 `/journey` and its aliases; §6 `/context` + `/ctx` + the category list + `/context all`, `/usage`, `/new` alias `/reset`; §3 `/reload-mcp` |
| [9] | Docs | Bundled Skills Catalog · Optional Skills Catalog | https://hermes-agent.nousresearch.com/docs/reference/skills-catalog · https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog (raw: `.../main/website/docs/reference/skills-catalog.md`, `.../reference/optional-skills-catalog.md`) | Nous Research | main branch, undated | 2026-09-07 | §2 the 61-in-12 and 136-in-22 figures, "not active by default", and the `hermes skills install official/<category>/<skill>` form |
| [10] | Release | Hermes Agent v0.21.0 (v2026.8.31) — The Pantheon Release | https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.31 (body via `gh api repos/NousResearch/hermes-agent/releases/tags/v2026.8.31`) | NousResearch | 2026-08-31T19:29:49Z | 2026-09-07 | §1 the version/date alert; §3 the whole "MCP command center" paragraph and the Blender removal; §5 and §6 the schema-token / 30-day-usage overlay; §7 the cron-memory sentence |
| [11] | Docs | Desktop Plugin SDK | https://hermes-agent.nousresearch.com/docs/developer-guide/desktop-plugin-sdk (raw: `.../main/website/docs/developer-guide/desktop-plugin-sdk.md`) | Nous Research | main branch, undated | 2026-09-07 | §5 the plugin path, "loads it within seconds and hot-reloads every save", ⌘K → Reload desktop plugins, and the Security-model quotations ("evaluated as ESM in the renderer realm with full app authority", "error isolation only", `integrity` is not a sandbox) |
| [12] | Community | Alex Finn, *Hermes Agent just WON (Hermes desktop app)* | https://www.youtube.com/watch?v=tiFJmVhkF_s | YouTube / Alex Finn | 2026-06-03 (`uploadDate` 2026-06-03T14:47:44-07:00) | 2026-09-07 | §2 the "over 150" count and the disable-what-you-do-not-use advice; §6 one-session-per-topic, pin/folder, `/new` when the meter fills, and the every-message-resends-the-thread explanation |
| [13] | Community | Wanderloots, *Full Hermes Agent Tutorial (Desktop) 🧠 A Useful Agentic AI Workflow* | https://www.youtube.com/watch?v=GL67DEf2nyI | YouTube / Wanderloots | 2026-07-01 (`uploadDate` 2026-07-01T05:30:30-07:00) | 2026-09-07 | §2 the "71 skills built into this" count and opening `memories/` to watch a new profile line appear |

**Fetched for verification but not cited:** `website/docs/user-guide/features/plugins.md` (to
confirm that agent-side plugins are a separate system from desktop plugins) and
`website/docs/user-guide/configuration.md` (to confirm no competing `memory:` defaults).

## Verification record

| Source | HTTP / API status | What was checked | Discrepancy |
|---|---|---|---|
| [1] skills.md | 200, 51,673 bytes | Lines 9–11 (definition, agentskills.io, source of truth); 154 (Level 0 tuple + ~3k); 52/61 (slash commands); 165–195 (frontmatter); 302–324 (directory tree); 654–692 (hub commands + source table); 39–47 (`opt-out`) | Level 0 returns `{name, description, category}` — the draft said name + description only. **Corrected.** |
| [2] desktop.md | 200, 54,936 bytes | Line 9 (same-agent quote); 52–59 (status bar, Context-usage meter, Show in status bar, `Cmd/Ctrl+Shift+S`); 105–111 (terminal, `Ctrl+\``); 122 (Memory Graph, All / Used / Learned); 159 (settings panes incl. MCP servers); 175 (Memory & Context); 186–192 (management panes, Skills tab, Star Map); 253 (palette); 405–424 (plugins) | The page never says the Skills pane is reached from the **left sidebar**; it lists Skills under "Management panes" and documents the palette as the way to open any page. **Corrected.** |
| [3] mcp.md | 200, 38,078 bytes | 25–52 (Quick start block + prompt); 54–88 (catalog: Nous-approved, disabled by default, `optional-mcps/`, no community tier); 174–182 (`hermes mcp configure`); 391–425 (minimal stdio/HTTP examples); 451–466 (naming table); 498–576 (filtering, globs, precedence); 619–657 (`/reload-mcp`, toolsets); 730–755 (troubleshooting) | None. The two YAML blocks in the post are byte-for-byte the doc's own examples. |
| [4] cli-commands.md | 200, 105,184 bytes | 1220–1235 (`hermes skills` table); 1380–1398 (`hermes memory`); 1423–1444 (`hermes mcp`); 1445–1470 (`hermes plugins`) | None. `hermes mcp catalog` / `install` / `configure` were missing from the draft's citation of this source; **added**. |
| [5] security.md | 200, 44,275 bytes | 606–639 (MCP Credential Handling; env allow-list; `[REDACTED]` patterns) | None — the draft's list matched the doc exactly. |
| [6] memory.md | 200, 21,844 bytes | 17–20 (caps table); 22–34 (one-agent caution, error-on-full); 38–57 (prompt block, frozen snapshot); 131–153 (entry counts, 80 %); 204–209 (~1,300 tokens); 213–229 (journey); 232–256 (config block, both-off); 258–297 (`write_approval`, notifications); 404–429 (`skills.write_approval`) | None. Searched for a "reset memory" command and found none — the post's hedge stands. |
| [7] memory-providers.md | 200, 31,959 bytes | 9 ("ships with 8"); 13–25 (setup/status/off, `memory.provider`, `hermes plugins` path); 673–686 (nine-row comparison table incl. Memori) | None — the 8-versus-9 observation in the draft is real and reproduced. |
| [8] slash-commands.md | 200, 43,233 bytes | 39 (`/new`), 65 (`/context`), 72 (`/journey`), 110 (`/learn`), 118 (`/reload-mcp`), 133 (`/usage`), 285 (`/reload-skills`), 291 (`/skills …`, search/install CLI-only) | `/reload-skills` exists and the draft's hand-written-skill procedure omitted it. **Added.** |
| [9] skills-catalog.md · optional-skills-catalog.md | 200, 12,909 bytes · 200, 22,599 bytes | Counted table rows and `##` category headings in each file: 61 unique bundled skills / 12 categories; 136 unique optional skills / 22 categories (the 23rd heading is "Contributing Optional Skills") | New source. The draft had no documented count at all and leaned entirely on two YouTube figures. |
| [10] release v2026.8.31 | anonymous REST → **403 rate-limited**; re-fetched with `gh api` → 200 | `tag_name` `v2026.8.31`, `name` "Hermes Agent v0.21.0 (v2026.8.31)", `published_at` 2026-08-31T19:29:49Z; body line 20 (MCP command center, verbatim), line 16 (cron memory), line 116 (Blender) | The release says the Blender MCP **catalog entry and skill** were removed; the draft said only the catalog entry. **Corrected.** |
| [11] desktop-plugin-sdk.md | 200, 43,096 bytes | 20–26 and 57–61 (paths, Settings → Plugins); 128–130 (⌘K reload); 850–867 (Security model) | The docs describe the renderer realm but never place a desktop plugin in a Context Usage category; the draft asserted "not in the model's context". **Hedged to what the docs say.** |
| [12] YouTube tiFJmVhkF_s | oEmbed 200; watch page 200, 1,362,747 bytes | Title "Hermes Agent just WON (Hermes desktop app)", author "Alex Finn", `uploadDate` 2026-06-03T14:47:44-07:00 | Transcript retrieval **failed** on the access date (YouTube blocked both the timedtext endpoint and the transcript tool). Identity/date re-verified; the spoken figure was not. Reference note now says so. |
| [13] YouTube GL67DEf2nyI | oEmbed 200; watch page 200, 1,710,441 bytes | Title "Full Hermes Agent Tutorial (Desktop) 🧠 A Useful Agentic AI Workflow", author "Wanderloots", `uploadDate` 2026-07-01T05:30:30-07:00 | Same transcript block. Also: the real title contains a 🧠 between "(Desktop)" and "A Useful"; the post renders it as an em dash to keep the one-emoji-per-section rule. |

## Claims and numbers

| Value | Source | Where it lands |
|---|---|---|
| Skills live in `~/.hermes/skills/`, "the primary directory and source of truth" | [1] | §1 bullet, §5 table |
| Level 0 index = `{name, description, category}` per skill, ~3k tokens | [1] | §1 bullet, §2 blockquote, §5 table |
| Hub sources: `official`, `skills-sh`, `well-known`, `url`, `github`, `clawhub`, `lobehub`, `browse-sh` | [1] | §2 step 3 |
| 61 bundled skills in 12 categories (seeded on install) | [9] | §2 catalog paragraph, §2 blockquote |
| 136 official optional skills in 22 categories, not active by default | [9] | §2 catalog paragraph, §2 blockquote |
| "over 150" (Finn) / "71 skills built into this" (Wanderloots) | [12], [13] | §2 blockquote — flagged as user reports, reconciled against [9] |
| MCP tool names `mcp_<server_name>_<tool_name>`; toolset `mcp-<server>` | [3] | §1 bullet, §3 opener |
| Catalog entries are Nous-reviewed, kept in `optional-mcps/`, disabled by default | [3] | §3 step 1 |
| cloudflare ≈ 3,300 OpenAPI endpoint tools | [3] | §3 filtering paragraph |
| `include` wins when both `include` and `exclude` are present | [3] | §3 filtering paragraph |
| stdio MCP env allow-list: `PATH, HOME, USER, LANG, LC_ALL, TERM, SHELL, TMPDIR` + `XDG_*` | [5] | §3 alert, §7 key takeaway |
| Redacted patterns: `ghp_…`, `sk-…`, Bearer tokens, `token=`, `key=`, `API_KEY=`, `password=`, `secret=` | [5] | §3 alert |
| MEMORY.md 2,200 chars ≈ 800 tokens; USER.md 1,375 chars ≈ 500 tokens | [6] | §1 bullet, §4 opener, §4 config block, §5 table |
| Prompt block example `[67% — 1,474/2,200 chars]`, `§` separators | [6] | §4 code block |
| Consolidate above 80 % of capacity | [6] | §4 blockquote |
| Persistent memory "Fixed per session (~1,300 tokens)" | [6] | §6 blockquote |
| 8 external memory providers on the page; 9 rows in the comparison table (Memori) | [7] | §4 provider paragraph |
| Context Usage categories: system prompt, tool definitions, skills, memory, rules, MCP, subagent definitions, conversation | [2] | §6 opener |
| `/context` CLI category list: system prompt, tool definitions, rules, skills index, MCP, subagents, memory, conversation | [8] | §6 code block |
| v0.21.0, tag `v2026.8.31`, released 2026-08-31 | [10] | §1 alert, §3, §7 |
| "schema token estimates and 30-day usage per server" | [10] | §3, §5 table, §6 step 3 |
| Desktop plugin at `$HERMES_HOME/desktop-plugins/<id>/plugin.js` | [11] | §5 table and paragraph |
| "evaluated as ESM in the renderer realm with full app authority" / "error isolation only" | [11] | §5 danger alert |

## Dated statuses

True as of **2026-09-07**:

- Latest Hermes Agent release is **v0.21.0**, tag `v2026.8.31`, published 2026-08-31T19:29:49Z.
  There is no separate "Hermes Desktop" version number — the post says so in its version alert.
- The **MCP page** described in §3 is documented only in the v0.21.0 release notes; the MCP
  documentation page still describes config-file and CLI workflows and does not yet picture the
  merged Desktop page. The post states this limitation in its version alert.
- The **Memory Providers** page still opens with "ships with 8" while its comparison table lists
  nine providers (Memori is the ninth). Both readings are reproduced in §4 rather than resolved.
- The docs offer **no `reset memory` command**; §4 says so and gives the two manual routes instead.
- YouTube served video metadata but refused transcript retrieval from this network on this date.

## Corrections made to the interrupted run's Thai draft

1. Level 0 index tuple includes `category` — [1] line 154.
2. "Open the left sidebar → Skills" replaced with the documented management-pane / command-palette
   route — [2] lines 37, 186–188, 253.
3. `/reload-skills` added to the write-your-own procedure — [8] line 285.
4. Blender removal covers the catalog entry **and** the skill — [10] line 116.
5. Desktop-plugin context-cost cell hedged to what [11] actually says.
6. Documented catalog counts (61 / 136) added and the community counts subordinated to them — [9].
7. Nous-approved catalog facts re-cited from [3] (which carries them) rather than from the release
   notes alone, and "disabled by default" added.
8. Per-tool MCP filtering (`tools.include` / `tools.exclude`, glob, precedence, `hermes mcp
   configure`, the cloudflare figure) added to §3 and §6 — [3], [4].
9. Cross-link labels for the analytical series normalised to "Hermes #N …", matching
   `hermes-desktop-council`, so they cannot be read as this series' own #3/#5/#6.
10. Community reference notes rewritten to say exactly what was re-verified today (identity, channel,
    publication date) and what was not (the spoken counts).

## Do not assert

Looked for and could **not** verify on 2026-09-07 — deliberately absent from the post:

- **How many skills a given install actually shows.** The bundled catalog (61) and the optional
  catalog (136) are documented; what any one machine displays after updates and hub installs is not.
  The post never states a per-machine total in its own voice.
- **The exact wording spoken in either YouTube walkthrough.** Transcripts were unreachable; the two
  counts are attributed as user reports, in quotation marks, with the block explaining why the
  numbers differ.
- **The labels and layout of the Desktop MCP page.** Only the release-notes paragraph describes it;
  no documentation page or screenshot was available, so §3 quotes the release notes and says so.
- **Any per-control walkthrough of Settings → Memory & Context.** [2] names the page; it does not
  enumerate its controls, and §4 says the docs do not.
- **Whether a Desktop plugin costs any context at all.** [11] describes the renderer realm; nothing
  states a token cost either way, so the table cell reports the absence rather than a number.
- **The community "compression threshold 0.5" tip** from the research slice: no documentation page
  confirms that control or its default, so it was left out entirely.
