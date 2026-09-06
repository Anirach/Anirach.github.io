# Research ledger — post #3 `hermes-desktop-profiles`

- **Series**: Hermes Desktop Hands-On 2026 (`hermes-desktop`)
- **Post**: #3 — Profiles — หนึ่ง agent ต่อหนึ่งบทบาท / Profiles — One Agent per Role
- **Written**: 2026-09-07
- **Access date**: 2026-09-07 (every source below re-fetched in this run)
- **Sources fetched**: 11

> **Binding rule**: the post may not contain a number, date, command, path, quotation or URL
> that does not appear in this ledger.

---

## Sources

| [N] | Tag | Title | URL | Publisher | Published | Accessed | Supports |
|---|---|---|---|---|---|---|---|
| 1 | Docs | Profiles: Running Multiple Agents (`website/docs/user-guide/profiles.md`, main) | https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/profiles.md | Nous Research | main branch (undated) | 2026-09-07 | The profile definition; `~/.hermes/profiles/<name>/` and default = `~/.hermes`; the two-processes caution; profile vs workspace vs sandbox; `terminal.cwd`; the alias, `-p`, `hermes profile use`, prompt/banner; `HERMES_HOME` and 119+ files; HOME vs HERMES_HOME and `home_mode: profile`; OAuth shared from root `auth.json`; `hermes update` skill sync; `config set model.default` / `terminal.cwd`; `default` undeletable + `display_name`; per-profile gateways and token locks; `hermes setup --portal`; §2 table rows |
| 2 | Docs | Profile Commands Reference (`website/docs/reference/profile-commands.md`, main) | https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/reference/profile-commands.md | Nous Research | main branch (undated) | 2026-09-07 | The 13 subcommands; all `create` flags incl. `--no-skills` + `.no-bundled-skills`; `--clone-all` exclusions; `describe` and `profile.yaml`; `profile list` / `show` output; `export`/`import` flags, the `<name>.tar.gz` current-directory default, overwrite and `default` refusals; the documented naming rule |
| 3 | Docs | Bot Mode (`website/docs/user-guide/bot-mode.md`, main) | https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/bot-mode.md | Nous Research | main branch (undated) | 2026-09-07 | "a Bot **is** a Hermes profile"; the Bots tab and Routines tile; the whole New Agent flow; the canonical pinned Bot Chat; the teammate roster in the system prompt; Routines as `[bot:<name>]` cron jobs; the CLI parity table; Settings → Plugins → Bots |
| 4 | Docs | Profile Distributions: Share a Whole Agent (`website/docs/user-guide/profile-distributions.md`, main) | https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/profile-distributions.md | Nous Research | main branch (undated) | 2026-09-07 | Export-file contents and the "snapshot, not a curated release" caution; "Credentials are filtered by filename; content is not"; named-profile export scope; import-as-`default` refusal; three Desktop export doors + `desktop.json`; the managed `profile-exports/` location (the conflicting claim); distribution-owned vs user-owned table + `mcp.json`; the `hermes profile list` table sample |
| 5 | Docs | Hermes Desktop (`website/docs/user-guide/desktop.md`, main) | https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/desktop.md | Nous Research | main branch (undated) | 2026-09-07 | The "Applies to" chip row and the eight config-backed pages; Settings → Model as the per-profile global default; the composer picker as sticky UI state; ⌘K → Export/Import profile… and `desktop.json` |
| 6 | Docs | Personality & SOUL.md (`website/docs/user-guide/features/personality.md`, main) | https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/features/personality.md | Nous Research | main branch (undated) | 2026-09-07 | SOUL.md as primary identity in slot #1; loaded only from `HERMES_HOME`; "injected verbatim after security scanning and truncation"; the prompt-injection scan; SOUL.md vs `/personality` |
| 7 | Docs | Configuration (`website/docs/user-guide/configuration.md`, main) | https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/configuration.md | Nous Research | main branch (undated) | 2026-09-07 | `terminal.home_mode: auto \| real \| profile` and its table; the `terminal` config block used in the YAML example |
| 8 | Docs | Slash Commands (`website/docs/reference/slash-commands.md`, main) | https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/reference/slash-commands.md | Nous Research | main branch (undated) | 2026-09-07 | `/profile`; `/export` and `/import` with flags; the second statement that the export default is `<name>.tar.gz` in the current directory |
| 9 | Docs | `hermes_cli/profiles.py` (source file on main) | https://raw.githubusercontent.com/NousResearch/hermes-agent/main/hermes_cli/profiles.py | Nous Research | main branch (undated) | 2026-09-07 | `_PROFILE_ID_RE`; `_RESERVED_NAMES`; the `root / "profiles" / canon` path rule with `default` returning the root; `profile.yaml` keys |
| 10 | Release | Hermes Agent v0.21.0 (v2026.8.31) — The Pantheon Release | https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.31 | Nous Research | 2026-08-31 | 2026-09-07 | "Bot Mode is now a bundled, default-on part of the desktop app: every agent profile gets a name, a deterministic avatar face" |
| 11 | Community | Hermes Agent Desktop: Full Setup + Real Use Cases (video, 43 min) | https://www.youtube.com/watch?v=EJm8Ka-gVOc | Greg Isenberg (guest: Alex Finn) | 2026-06-06 | 2026-09-07 | Profiles organised by model (a top-tier model for strategy, another for coding, a local model for free research); the profiles-vs-subagents rule |

---

## Verification record

| [N] | Method | Status / size | What was checked | Discrepancy |
|---|---|---|---|---|
| 1 | `curl` raw.githubusercontent.com, full file read | HTTP 200, 16,141 B | Every quotation used in §1, §2, §4, §5, §7 read in situ, not from the research pack | none |
| 2 | `curl` raw, full file read | HTTP 200, 18,116 B | The subcommand table counted (13 rows); all `create` flags; `export`/`import` sections | **Yes** — its export default contradicts [4]; recorded below and disclosed in the post |
| 3 | `curl` raw, full file read | HTTP 200, 23,527 B | The New Agent flow enumerated field by field; the CLI parity table; "Turning it off" | none |
| 4 | `curl` raw, targeted read of the export/import and ownership sections | HTTP 200, 31,235 B | The `profile-exports/` paragraph read verbatim; the export-contents list; the ownership table | **Yes** — see [2] |
| 5 | `curl` raw, targeted grep + read | HTTP 200, 54,936 B | "Per-profile settings: the 'Applies to' scope" §; the Settings → Model bullet; the export/import bullet | none |
| 6 | `curl` raw, full file read | HTTP 200, 9,666 B | Slot #1, the load rule, verbatim injection + scanning, the SOUL vs /personality section | none |
| 7 | `curl` raw, targeted grep | HTTP 200, 197,007 B | The `terminal` block and the `home_mode` table | none |
| 8 | `curl` raw, targeted grep | HTTP 200, 43,233 B | The `/profile`, `/export`, `/import` rows | Agrees with [2], against [4] |
| 9 | `curl` raw, targeted grep | HTTP 200, 77,600 B | `_PROFILE_ID_RE`, `_RESERVED_NAMES`, the path computation, `profile.yaml` reader/writer | Source reserves `default` too; [4] lists five reserved names without it. Not asserted either way — the post quotes the source's six |
| 10 | WebFetch of the release page | 200 | The Bot Mode sentence and the version/tag/theme strings | none |
| 11 | YouTube metadata fetch (`get_video_info`) | 200 | Title, uploader, upload date 2026-06-06, and the two key-point lines quoted | none |

---

## Claims and numbers

| Value / string | Source | Where it lands |
|---|---|---|
| "A profile is a separate Hermes home directory" | [1] | Intro, §1 opener, §8 takeaway 1 |
| `~/.hermes/profiles/<name>/`; default = `~/.hermes`; internal ID always `default` | [1], [9] | §1, §2 table paths, §8 takeaway 1 |
| "No migration needed — existing installs work identically" | [1] | §1 |
| 119+ files resolve paths via `get_hermes_home()` | [1] | §1 |
| "Profiles do **not** sandbox the agent" | [1] | §1 list item 3, §8 takeaway 2 |
| `cwd: "."` = "the directory Hermes was launched from" | [1] | §5 |
| "Asking the model 'what directory are you in?' is not a reliable isolation test" | [1] | §5 |
| Name regex `^[a-z0-9][a-z0-9_-]{0,63}$`; 6 reserved names (`hermes`, `default`, `test`, `tmp`, `root`, `sudo`) | [9] | §1 callout |
| "Must be a valid directory name (alphanumeric, hyphens, underscores)" | [2] | §1 callout (contrasted with [9]) |
| 13 `hermes profile` subcommands, listed by name | [2] | §4 opener |
| `--clone` / `--clone-all` / `--clone-from` / `--no-skills` semantics; `--no-skills` refuses to combine with clone flags; `.no-bundled-skills` marker | [2] | §4 `<pre>`, §4 prose, §7 bullet 2 |
| `--clone-all` excludes sessions, `state.db`, backups, state-snapshots, checkpoints | [2] | §2 table (sessions, state.db rows), §4 `<pre>` |
| Description persisted in `<profile_dir>/profile.yaml`; keys `description`, `description_auto`, `display_name` | [2], [9] | §2 table, §4 step 1 |
| Kanban orchestrator routes "based on role instead of profile name alone" | [2] | §3 step 3 |
| `hermes profile list` marks the active profile with `*`; the fuller table has Model / Gateway / Alias / Distribution columns | [2], [4] | §4 step 2 |
| `hermes profile show` fields (Path, Model, Gateway, Skills, .env, SOUL.md, Alias) | [2] | §4 step 6 |
| Alias at `~/.local/bin/<name>`; "it's just `hermes -p <name>` under the hood" | [1] | §4 step 3 |
| `hermes chat -p research -q "hello"` works in any position | [1] | §4 step 3 |
| "Like `kubectl config use-context`" | [1] | §4 step 4 |
| Prompt `research ❯`; banner `Profile: research`; bare `hermes profile` prints name/path/model/gateway | [1] | §4 step 5 |
| `/profile` shows active profile name and home directory | [8] | §4 step 5 |
| "Quickest setup: run `hermes setup --portal` inside the new profile to wire up models + tools at once" | [1] | §4 step 7 |
| "There is no new primitive to learn: a Bot **is** a Hermes profile" / "Bot Mode is a UI over that primitive" | [3] | §3 opener, §8 takeaway 3 |
| Bots tab next to Sessions; Routines tile docked while the tab is active | [3] | §3 step 1 |
| New Agent quick path = Name / Title / Description; the Bot introduces itself as the first message | [3] | §3 step 2 |
| "names **and roles** from each profile's title/description" in every Bot Chat's system prompt | [3] | §3 step 3, §8 takeaway 4 |
| Advanced: Clone from an existing profile / Fresh profile / Create empty | [3] | §3 step 4 |
| "Leave it unset to inherit from the launch profile" | [3] | §3 step 5 |
| Per-skill / per-toolset / per-MCP-server enablement; Shared keys shares one OAuth/token pool with the main profile | [3] | §3 step 7 |
| The canonical Bot Chat is created and pinned the moment the Bot is born | [3] | §3 step 8 |
| CLI parity: `hermes -p <bot> chat`, `~/.hermes/profiles/<bot>/`, `hermes cron list`, `hermes profile create` / `list` | [3] | §3 step 9 |
| "Bot Mode is now a bundled, default-on part of the desktop app: every agent profile gets a name, a deterministic avatar face" — v0.21.0, tag v2026.8.31, "The Pantheon Release", 2026-08-31 | [10] | §3 closing paragraph |
| Disable at Settings → Plugins → Bots; "Your profiles, sessions, and cron jobs are untouched either way; Bot Mode never owns your data, it only renders it" | [3] | §3 closing paragraph |
| SOUL.md "occupies slot #1 in the system prompt, replacing the hardcoded default identity" | [6] | §5, §8 takeaway 5 |
| "injected verbatim after security scanning and truncation"; "is scanned like other context-bearing files for prompt injection patterns before inclusion" | [6] | §5 |
| SOUL.md changes "take effect cleanly on a new session" | [1] | §5 |
| "`SOUL.md` = baseline voice" / "`/personality` = temporary mode switch" | [6] | §5 callout |
| `coder config set model.default anthropic/claude-sonnet-4`; `coder config set terminal.cwd /absolute/path/to/project`; `echo "You are a focused coding assistant." > ~/.hermes/profiles/coder/SOUL.md` | [1] | §5 `<pre>` (verbatim from the docs' examples) |
| `terminal.home_mode: auto \| real \| profile`; `{HERMES_HOME}/home`; `HERMES_REAL_HOME` | [1], [7] | §2 table + prose, §5 YAML `<pre>` |
| "host profiles share normal user-level CLI state by default" | [1] | §2 prose |
| Settings → Model is the "per-profile global default" and "the only place that writes it"; "Each profile keeps its own default" | [5] | §5 |
| "The composer picker is sticky UI state and never touches your default" | [5] | §5 |
| "Applies to" chip row on Model, Workspace, Safety, Memory & Context, Voice, Chat, Advanced, Tools & Keys; follows the active profile; hidden below two profiles | [5] | §5, §8 takeaway 5 |
| Export strips `auth.json` and `.env` always; import installs as a NEW profile, refuses to overwrite, cannot import as `default` | [2], [4] | §6 opener, §6 `<pre>`, §7 bullet 4, §8 takeaway 6 |
| "a snapshot of your profile, not a curated release"; "Credentials are filtered by filename; content is not"; "A named profile copies the whole directory minus `auth.json` / `.env`" | [4] | §6 prose, §8 takeaway 6 |
| ⌘K → Export profile… / right-click a profile square in the rail / the import button beside the rail's `+`; `desktop.json` carries skin, light/dark mode, custom themes, rail color, window layout | [4], [5] | §6 prose |
| Export default location conflict: `<name>.tar.gz` in the current directory ([2], [8]) vs the managed `profile-exports/` under the default Hermes home ([4]) | [2], [4], [8] | §6 `.alert` (disclosed with both sources) |
| Distributions: git repo + `distribution.yaml`, `hermes profile install` / `update`, user data never touched | [4] | §6 closing paragraph (cross-link to #10 rather than re-teaching) |
| OAuth: "single-use refresh tokens"; `--clone-all` drops OAuth rows; root `auth.json`; `hermes -p <name> auth add <provider>` | [1] | §7 bullet 1, §8 takeaway 7 |
| "Skills synced: default (up to date), coder (+2 new), assistant (+2 new)"; "User-modified skills are never overwritten" | [1] | §7 bullet 2 |
| `hermes skills opt-out` / `hermes skills opt-in` | [2] | §7 bullet 2 |
| Routines are "plain Hermes cron jobs namespaced `[bot:<name>] <routine>`"; visible in `hermes cron list` | [3] | §2 table, §7 bullet 3 |
| "You cannot delete the default profile (`~/.hermes`). To remove everything, use `hermes uninstall`" | [1] | §7 bullet 4 |
| "You cannot import as `default` — that name is the built-in root profile" | [4] | §7 bullet 4 |
| `hermes profile rename default <Name>` sets `display_name` in `~/.hermes/profile.yaml`; canonical ID stays `default` | [1] | §7 bullet 4 |
| `coder gateway start`; `coder gateway install` → `hermes-gateway-coder` systemd/launchd service | [1] | §7 bullet 5 |
| "the second gateway will be blocked with a clear error naming the conflicting profile"; Telegram, Discord, Slack, WhatsApp, Signal | [1] | §7 bullet 5 |
| "hermes update pulls code once (shared)" | [1] | §2 table (code row) |
| Community: profiles organised by model — a top-tier model for strategy, another for coding, a local model for free research | [11] | §8 |
| Community: "Sub-agents handle one skill across many parallel tasks; profiles handle work where each step needs a distinct skill set" | [11] | §8, and the §8 lead-in |

---

## Dated statuses (true as of 2026-09-07)

- Hermes Agent's current release is **v0.21.0, tag `v2026.8.31`**, "The Pantheon Release", published 2026-08-31 [10]. The post never treats Hermes Desktop as a separate product with its own version number.
- **Bot Mode is bundled and on by default** in the desktop app as of that release [3], [10]; it is switched off under Settings → Plugins → Bots [3].
- The **`hermes profile` subcommand set is 13 commands** as documented on `main` today [2]. If a 14th appears, §4's opening paragraph is the sentence to re-check.
- The **export default-location contradiction between [2]/[8] and [4] is still live** on `main` today. Three pages were read in this run; two say the current directory, one says a managed `profile-exports/` directory. The post states both and recommends always passing `-o`.
- The **six reserved profile names in the source** include `default`, while the distributions guide names only five (`hermes`, `test`, `tmp`, `root`, `sudo`). The post cites the source's six and does not claim the docs agree.

---

## Do not assert

Looked for and deliberately left out of the post:

- **The Windows profile path.** `%LOCALAPPDATA%\hermes\profiles\<name>` is a derivation from the Windows-native page plus the source's path rule, not a sentence in any doc. Not published; the post uses POSIX paths throughout and does not claim Windows equivalence.
- **Where the Windows `.bat` alias is written.** The source read shows `Path.home()/.local/bin` with no Windows override; the Windows guide talks about a different PATH entry. Unverified, so no Windows alias claim is made.
- **Which release first shipped `hermes profile`.** v0.13.0 (2026-05-07) already mentions a dashboard Profiles page, so profiles predate it, and no CHANGELOG settles it. The post states no "profiles arrived in vX" date.
- **`hermes profile create --portal`.** The flag appears in an earlier post of mine as an alternative but is **not** in the current `create` flag table [2]. The post uses the documented `hermes setup --portal` inside a new profile instead, which is what [1] actually says.
- **The Profile Builder's on-screen field labels** (dashboard `/profiles/new`). No screenshot was fetched and the labels could not be verified, so the dashboard route is not taught in this post at all; the post covers only the Desktop and CLI routes.
- **`ui_meta` as a `profile.yaml` key.** Bot Mode says section/hidden/avatar state lives in "profile metadata (`ui_meta`)", while the source's `profile.yaml` reader exposes only `description`, `description_auto` and `display_name`. The post lists only the three verified keys and never names `ui_meta`.
- **A per-profile spend cap, token budget or rate-limit key.** None found in the docs; only generic `config.yaml` keys that happen to be per profile by construction. No such feature is claimed.
- **`hermes profile list` exact rendering.** [2] shows a plain list with `*`; [4] shows a column table. Both are cited side by side in §4 step 2 rather than one being presented as the format.
- **Bot Mode's exact first bundling version.** Community reporting places it around v0.20.3 in mid-August; the post cites only v0.21.0, which is the release whose own notes state "bundled, default-on".
- **Any Hermes Cloud price, "public preview" label, or claim that Hermes Desktop is a separate product or repository.**
