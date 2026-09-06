# Research ledger — post #4 `hermes-desktop-council`

- **Series** — Hermes Desktop Hands-On 2026 (`scripts/series/hermes-desktop.json`), post #4 of 7
- **Post** — "The Council — ตรวจก่อนส่ง ทุกคำตอบ" / "The Council — Check Before Deliver"
- **Written** — 2026-09-07
- **Access date** — 2026-09-07 (every source below was re-fetched on this date; the upstream
  research slice `angles/councils.md` was dated 2026-09-06 and was NOT used as a citation)
- **Sources fetched** — 20 (14 cited, 6 verification-only)

> **Binding rule:** the post may not contain a number, date, command, path, quotation or URL that
> does not appear in this ledger.

## Sources

| [N] | Tag | Title | URL | Publisher | Published | Accessed | Supports |
|---|---|---|---|---|---|---|---|
| [1] | Docs | Mixture of Agents | https://hermes-agent.nousresearch.com/docs/user-guide/features/mixture-of-agents (raw: `.../main/website/docs/user-guide/features/mixture-of-agents.md`) | Nous Research | main branch, undated | 2026-09-07 | §2 whole mechanism, §3 preset YAML + CLI + picker, §4 blocks/failures/traces/privacy, §7 five MoA rows + cache sentences |
| [2] | Docs | Subagent Delegation | https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation (raw: `.../main/website/docs/user-guide/features/delegation.md`) | Nous Research | main branch, undated | 2026-09-07 | §5 all five `/review` facts, the 4-step routine, `auxiliary.review` YAML, steer/stop; §7 the no-per-task-model sentence |
| [3] | Docs | Slash Commands Reference | https://hermes-agent.nousresearch.com/docs/reference/slash-commands (raw: `.../main/website/docs/reference/slash-commands.md`) | Nous Research | main branch, undated | 2026-09-07 | §1 absence of `/council`; §3 `/moa` one-shot; §5 `/agents` alias `/tasks`; §6 `/subgoal` |
| [4] | Docs | Persistent Goals | https://hermes-agent.nousresearch.com/docs/user-guide/features/goals (raw: `.../main/website/docs/user-guide/features/goals.md`) | Nous Research | main branch, undated | 2026-09-07 | §6 completion contract, the inline contract block, field prefixes, `/goal show`, `/goal gate add`, judge fails open |
| [5] | Docs | Bot Mode: A Roster of Agents + Local Models | https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode (raw: `.../main/website/docs/user-guide/bot-mode.md`); https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/local-models.md | Nous Research | main branch, undated | 2026-09-07 | §8 group-chat facts; §3 the `model.provider: llamacpp` "same shape as every other provider" sentence |
| [6] | Docs | `hermes_cli/config_defaults.py` + Profiles | https://raw.githubusercontent.com/NousResearch/hermes-agent/main/hermes_cli/config_defaults.py; https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/profiles.md | NousResearch | main branch | 2026-09-07 | every default in the §7 table, the moa-traces path, `auxiliary.review` defaults, `delegation` empty defaults, the profile-home sentence in the intro and §4 |
| [7] | Docs | `skills/software-development/requesting-code-review/SKILL.md` v2.0.0 | https://raw.githubusercontent.com/NousResearch/hermes-agent/main/skills/software-development/requesting-code-review/SKILL.md | NousResearch | main branch | 2026-09-07 | §5 💡 callout quotation |
| [8] | Release | Hermes Agent v0.21.0 (v2026.8.31) | https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.31 (body via `gh api`) | NousResearch | 2026-08-31T19:29:49Z | 2026-09-07 | §1 the "Reverted in this window" line; §5 the absence of `/review` in the notes; the version string used throughout |
| [9] | Release | Hermes Agent v0.18.0 (2026.7.1) — The Judgment Release | https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.1 (body via `gh api`) | NousResearch | 2026-07-01T20:08:06Z | 2026-09-07 | §2 MoA first-class + picker sentence + "watch the committee deliberate"; §4 labelled blocks + the three named surfaces |
| [10] | Release | PR #84904 + PR #84994 | https://github.com/NousResearch/hermes-agent/pull/84904; https://github.com/NousResearch/hermes-agent/pull/84994 | NousResearch | merged 2026-08-13 | 2026-09-07 | §1 `synthesis_style`, the `/council` description quotation, both merge timestamps, the revert diffstat |
| [11] | Release | PR #93339 | https://github.com/NousResearch/hermes-agent/pull/93339 | NousResearch | merged 2026-08-24T00:38:39Z | 2026-09-07 | §5 the `/review` merge date/time |
| [12] | Issue | issue #37569, PR #848, issue #5876, PR #1972 | https://github.com/NousResearch/hermes-agent/issues/37569; /pull/848; /issues/5876; /pull/1972 (bodies + comments via `gh api`) | NousResearch | closed 2026-07-13 / 2026-03-11 / 2026-07-05 / 2026-05-11 | 2026-09-07 | §7 the delegation-model-routing quotation; §8 the four refusal facts |
| [13] | Issue | PR #86614, PR #49632 | https://github.com/NousResearch/hermes-agent/pull/86614; /pull/49632 | NousResearch | opened 2026-08-15 / 2026-06-20, both open | 2026-09-07 | §8 both are open, unmerged, no maintainer comment; the MoA-vs-council positioning line |
| [14] | Community | `Ridwannurudeen/hermes-council` README | https://raw.githubusercontent.com/Ridwannurudeen/hermes-council/master/README.md | Ridwannurudeen | undated (branch master) | 2026-09-07 | §8 MIT, five personas, three modes, the latency/token-cost warning |

**Fetched for verification but not cited:** `website/docs/user-guide/configuration.md`,
`website/docs/reference/cli-commands.md`, `website/docs/user-guide/desktop.md`,
`hermes_cli/moa_cmd.py`, `hermes_cli/moa_config.py`, the v0.20.6 (v2026.8.27) release body,
and `search/code?q=council+repo:NousResearch/hermes-agent`.

## Verification record

| Source | HTTP / API status | What was checked | Discrepancy |
|---|---|---|---|
| mixture-of-agents.md (raw) | 200, 12,937 bytes | Every YAML key, the six-step loop, the HermesBench table read line-by-line (`0.8202` / `0.7607` / `0.7412`), the Notes section | none |
| delegation.md (raw) | 200, 36,087 bytes | The whole `## The /review Command` section and `### Review model`; the `steer`/`stop` JSON; the "no per-task model parameter" paragraph | none |
| slash-commands.md (raw) | 200, 43,233 bytes | `grep -i council` → **0 hits**; the `/moa`, `/review`, `/agents`, `/goal`, `/subgoal` rows read verbatim | none |
| goals.md (raw) | 200, 20,857 bytes | The inline contract block copied character-for-character; the field-prefix list; `/goal gate add`; the `### Fail-open semantics` paragraph | the near-identical sentence "judge failures fail **open** (continue) so a flaky judge never wedges progress" lives in configuration.md, not goals.md — the post quotes goals.md's own wording instead |
| bot-mode.md (raw) | 200, 23,527 bytes | Lines 95–99 (2–6 Bots, three serial rounds, hard caps, `@user` badge); `grep -i vote|chair|consensus` → no mechanism documented | none |
| local-models.md (raw) | 200 | The `model.provider: llamacpp` paragraph | none |
| profiles.md (raw) | 200 | "A profile is a separate Hermes home directory"; the `HERMES_HOME` paragraph | none |
| config_defaults.py (raw) | 200, 184,347 bytes | `moa` block at lines 1285–1310; `auxiliary.review` at line 706; `delegation` at lines 1209–1217 | none |
| requesting-code-review/SKILL.md (raw) | 200, 8,423 bytes | Line 19 core-principle sentence; `version: 2.0.0` in the front matter | none |
| release v2026.8.31 | `gh api` 200 | `name`, `published_at`, the reverted-section line, `grep -c "/review"` → **0** | none |
| release v2026.7.1 | `gh api` 200 | `name`, `published_at`, the MoA highlight paragraphs | none |
| release v2026.8.27 | `gh api` 200 | `grep -c "/review"` → **0**, `grep -i review` → 0 | this is the basis for the hedge in §5 |
| PR #84904 | `gh api` 200 | `merged=true`, `merged_at=2026-08-13T02:44:10Z`, `changed_files=10`, `+407/−24`, body quotation | none |
| PR #84994 | `gh api` 200 | `merged=true`, `merged_at=2026-08-13T04:50:36Z`, body states "10 files, +24/−407" | none |
| PR #93339 | `gh api` 200 | `merged=true`, `merged_at=2026-08-24T00:38:39Z`, title | none |
| issue #37569 | `gh api` 200 + comments | `state=closed`, `closed_at=2026-07-13T22:13:31Z`, teknium1's closing comment read in full | none |
| PR #848 | `gh api` 200 + comments | `merged=false`, `created_at=2026-03-10T17:53:24Z`, `closed_at=2026-03-11T16:05:47Z`, the four numbered objections read in full | **the research slice said "closed 2026-03-10"; the API says closed 2026-03-11.** The post uses "opened 2026-03-10, closed 2026-03-11" |
| issue #5876 | `gh api` 200 + comments | `closed_at=2026-07-05T08:40:09Z`, teknium1's one-line comment verbatim | none |
| PR #1972 | `gh api` 200 + comments | `state=closed`, teknium1's two-reason comment read in full | none |
| PR #86614 / #49632 | `gh api` 200 + comments | both `state=open`, `merged=false`; comment authors are `Enough1122` + `0xNyk` (#86614) and none (#49632) — **no maintainer among them** | none |
| code search `council` | `gh api search/code` 200 | `total_count = 1`, the single hit is `tests/hermes_cli/test_backup.py` | none |
| hermes-council README | 200 | MIT badge, the five personas table, the fast/standard/deep mode table, the "adds latency and token cost" line | none |
| docs-site URLs (7) | all 200 | every `hermes-agent.nousresearch.com` URL used in the reference list was HTTP-checked | none |

## Claims and numbers

| Value | Source | Where it lands |
|---|---|---|
| Hermes Agent **v0.21.0**, tag **v2026.8.31**, published 2026-08-31 | [8] | §1 opening sentence, key takeaways |
| PR #84904 merged **2026-08-13 02:44 UTC** | [10] | §1 |
| PR #84994 merged **2026-08-13 04:50 UTC**, **10 files, +24/−407** | [10] | §1 |
| "about two hours" (the gap between the two merges) | derived from [10] — 02:44:10 → 04:50:36 = 2 h 6 min | §1 |
| Code search for `council` → **1 hit**, an unrelated test file | code search (verification-only) | §1 |
| `synthesis_style`: `guidance` default, `council` alternative | [10] | §1 |
| MoA first-class in **v0.18.0**, tag **v2026.7.1**, published **2026-07-01**, "The Judgment Release" | [9] | §2 |
| HermesBench **0.8202** (MoA) vs **0.7607** (`anthropic/claude-opus-4.8`) vs **0.7412** (`openai/gpt-5.5`) | [1] | §2 💡 callout — quoted exactly, with the caveat that it is Nous' own internal benchmark and the page publishes no method |
| Shipped `default` preset: refs `openai-codex:gpt-5.5` + `openrouter:deepseek/deepseek-v4-pro`, aggregator `openrouter:anthropic/claude-opus-4.8`, `max_tokens: 4096`, `enabled: true` | [1] + [6] | §3 `<pre>` (renamed to `council`; every key/value otherwise unchanged) |
| `moa.default_preset` default `"default"`; `moa.active_preset` default `""`; `moa.save_traces` default `false` | [6] | §3 `<pre>`, §7 table |
| `fanout` default `user_turn`; alternatives `per_iteration`, `every_n:3` | [1] | §3 `<pre>`, §7 table |
| `reference_max_tokens` unset = uncapped; suggested `600` | [1] | §7 table |
| Trace path `<hermes_home>/moa-traces/<session_id>.jsonl`, override `moa.trace_dir` | [6] | §4, §7 table |
| `moa.privacy_filter` — `""` off (default), `display`, `full` | [1] + [6] | §4 alert |
| `/review` snapshots the **last 10** user/assistant messages, tool output excluded | [2] | §5 |
| `auxiliary.review` default `{"provider": "auto", "model": "", "base_url": "", "api_key": "", "api_mode": ""}`; `api_mode` ∈ `chat_completions` / `anthropic_messages` / `codex_responses` | [6] | §5, §7 table |
| Docs example `provider: openrouter` / `model: anthropic/claude-opus-4.6` | [2] | §5 `<pre>` (copied verbatim, comments included) |
| `/review` merged **2026-08-24 00:38 UTC** (PR #93339); first tagged release by date is **v0.20.6 (v2026.8.27)** but neither v0.20.6's nor v0.21.0's notes mention `/review` | [11] + [8] | §5 closing paragraph — stated as an explicit hedge |
| `/goal` inline contract block (5 lines) and the prefix list `verify:` `verified by:` `constraints:` `preserve:` `boundaries:` `scope:` `stop when:` `blocked:` | [4] | §6 `<pre>` and the paragraph after it |
| Judge fail-open: "If the judge errors (network blip, malformed response, unavailable aux client), Hermes treats the verdict as `continue` — a broken judge never wedges progress." (goals.md `### Fail-open semantics`) | [4] | §6 |
| `delegation.model` and `delegation.provider` both default `""` (inherit parent) | [6] | §7 table |
| "subagent models are not selectable per call; the supported configuration is a single global `delegation.provider` / `delegation.model` override" | [12] | §7 closing paragraph |
| Bot Mode groups **2–6 Bots**, **up to three serial rounds**, hard caps **10 messages per send, 3 rounds** | [5] | §8 |
| PR #848 opened **2026-03-10**, closed **2026-03-11**; "5 hidden LLM calls per invocation" | [12] | §8 alert |
| issue #5876 closed **2026-07-05**, "Implemented with our MoA update 2 weeks ago" | [12] | §8 alert |
| PR #1972 closed **2026-05-11** | [12] | §8 alert |
| PRs #86614 (opened 2026-08-15) and #49632 (opened 2026-06-20) both still **open** | [13] | §8 alert |
| hermes-council: MIT, five personas, three modes, "The council adds latency and token cost" | [14] | §8 alert |

## Dated statuses

True as of **2026-09-07**:

- Hermes Agent's newest tagged release is **v0.21.0 (v2026.8.31)**, published 2026-08-31.
- **There is no `/council` command** in Hermes Agent or Hermes Desktop. Hermes Desktop is not a
  separate product with its own version — it is the same agent with a GUI, so this post writes
  "Hermes Agent v0.21.0, tag v2026.8.31" and never a "Desktop version".
- `/review` is in `main` and in the current documentation; **no release note names the tagged
  release that first carried it**.
- PR #86614 and PR #49632 are **open**, unmerged, with no maintainer comment.
- `github.com/Ridwannurudeen/hermes-council` exists on branch `master` and is third-party.
- The delegation defaults raised in v0.21.0 (250 iterations, 10 concurrent children) resolve the
  slice's open question about `delegation.max_iterations`; **no number from that dispute is used in
  this post**, so it needed no adjudication here.

## Do not assert

Things I looked for and could not verify, and therefore left out or hedged:

- **Why `/council` was reverted.** PR #84994's body gives only "Teknium narrowed the original
  full-wave revert … to just this port" and says it may "re-land later via revert-of-revert or fresh
  cherry-pick". The post states the fact of the revert and never speculates on the reason.
- **Which tagged release first shipped `/review`.** Hedged explicitly in §5; the release notes are
  silent, so the post says only "in main since 2026-08-24".
- **Whether MoA's labelled reference blocks render on gateway messaging platforms.** The v0.18.0
  notes name only CLI, TUI and desktop. §4 says so and declines to claim Telegram/Discord.
- **A worked local-model MoA preset.** The docs' MoA examples are all cloud providers. §3 says the
  structure supports it (provider/model pairs; `llamacpp` is a normal provider slug; the only stated
  slot restriction is that an aggregator may not be another MoA preset) and explicitly says the
  documentation gives no local example.
- **The Nous Research X post** (2026-06-26, "8% higher than Opus 4.8 …"). Not fetchable (HTTP 402
  in the upstream sweep) and never verified here — **no verbatim X-post text appears in the post**.
- **Any Karpathy LLM Council port for Hermes.** Not found in the official docs, the repo, or the
  community awesome lists. §8 states this as a negative finding of my own search, not as a fact
  about the world.
- **`/review` on the Desktop docs page.** The Desktop page does not list `/review`; the claim that
  it works in the Desktop app rests on delegation.md's own sentence ("CLI, TUI, the Desktop app, and
  every gateway messaging platform"), which is what the post cites.
- **hermes-council installation commands.** The post names the project and its status but gives no
  `pip install` line, because it is third-party and unendorsed; §8 points at the series' own MCP
  post for the mechanism instead.
- **Hermes Cloud prices, CVE claims, per-call `delegate_task` models, `model.ollama_num_ctx`, and
  the look-alike domains** (hermes-agent.org, hermes-ai.net, hermesatlas.com) — none appear.
