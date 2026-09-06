# Research ledger — post #2 `hermes-desktop-local-models`

**Series:** Hermes Desktop Hands-On 2026 (`series-hermes-desktop`)
**Post:** #2 — Local Models — โมเดลบนเครื่องของเราเอง / Local Models — Run Hermes on Your Own Machine
**Written:** 2026-09-07 (Asia/Bangkok)
**Access date for every source below:** **2026-09-07**
**Sources fetched:** 16 cited + 10 supporting fetches recorded in §Verification but not cited

> Binding rule: the post may not contain a number, date, command, path, quotation or URL that
> does not appear in this ledger.

Product/version framing used throughout, per the brief: **Hermes Agent v0.21.0, tag v2026.8.31**.
No separate Desktop product or version number is asserted anywhere in the post.

The reference numbers in this table are the reference numbers **as they appear in the published
post** (`<li id="ref-N">`), so §Claims can be checked cell by cell against the rendered page.

---

## Sources

| N | Tag | Title | URL (as cited in the post) | Publisher | Published | Accessed | Supports |
|---|---|---|---|---|---|---|---|
| [1] | Docs | Local Models | https://hermes-agent.nousresearch.com/docs/user-guide/local-models — also fetched raw as `website/docs/user-guide/local-models.md` on `main` | Nous Research | file has a single commit, 43e67d87, 2026-09-01 | 2026-09-07 | Path A four-step flow and "That's the whole flow."; "Nothing leaves your computer…"; green/amber/red memory fit; ≥64K guarantee and the expert-weights-first overflow rule; 15-minute idle unload; byte-size download check; the `local_runtime:` block verbatim; `model.provider: llamacpp` + `model.default`; `models/` + `runtimes/llamacpp/`; build set per OS; 8 GB+/16 GB+; "a curated starting point, not a boundary", Find more models, Add model file; "is a default, not a requirement" |
| [2] | Docs | Providers & Custom Endpoints (page title on site: *LLM and Model Providers*) | https://hermes-agent.nousresearch.com/docs/integrations/providers — raw `website/docs/integrations/providers.md` | Nous Research | living page | 2026-09-07 | the 64,000-token startup rejection verbatim; "works with any OpenAI-compatible API endpoint"; tool-call flag table and the "Without `--jinja`…" sentence with the raw-JSON symptom; the `-c 64000 -np 4` trap; llama-server / vLLM / `ollama serve` / Modelfile / `ollama ps` commands; Ollama's VRAM-keyed default-context table and "the #1 source of confusion"; the "Custom endpoint (self-hosted / VLLM / etc.)" menu entry and the `hermes model` vs `/model` warning; the whole LM Studio section; the nine-step context resolution chain and the 128K default; local Ollama vs Ollama Cloud |
| [3] | Docs | Run Hermes Locally with Ollama — Zero API Cost | https://hermes-agent.nousresearch.com/docs/guides/local-ollama-setup — raw `website/docs/guides/local-ollama-setup.md` | Nous Research | living page (touched by 43e67d87) | 2026-09-07 | the `gemma4:31b` model-table row and "only `gemma4:31b` has reliable tool calling"; "By default, Ollama uses a 2048-token context"; the Modelfile with `PARAMETER num_ctx 64000`; `OLLAMA_KEEP_ALIVE=24h` and the five-minute idle unload; `HERMES_API_TIMEOUT=1800`; the test prompt "List all Python files in this directory and count the lines of code in each"; the hybrid config block and "This way, 90% of your usage is free (local)…" |
| [4] | Docs | Run Local LLMs on Mac | https://hermes-agent.nousresearch.com/docs/guides/local-llm-on-mac — raw `website/docs/guides/local-llm-on-mac.md` | Nous Research | living page (touched by 43e67d87) | 2026-09-07 | the Qwen3.5-9B-Q4_K_M row (5.3 GB / ~10 GB at 128K with a quantized KV cache); the KV-cache table f16 ~16 GB / q8_0 ~8 GB / q4_0 ~4 GB; "reduce context only while staying at or above Hermes' 64K minimum"; "That's prefill at work, not a stalled session."; `hermes prompt-size` |
| [5] | Docs | FAQ | https://hermes-agent.nousresearch.com/docs/reference/faq — raw `website/docs/reference/faq.md` | Nous Research | living page | 2026-09-07 | the `hermes model` → Custom endpoint worked example including `Context length: 64000` and its note; "Ollama's `/api/show` reports the model's *maximum* context, not the effective `num_ctx` you configured"; "read timeout raised from 120s to 1800s, stale stream detection disabled" and `HERMES_STREAM_READ_TIMEOUT=1800`; "`hermes update` pulls the latest code and reinstalls dependencies" |
| [6] | Docs | Hermes Desktop | https://hermes-agent.nousresearch.com/docs/user-guide/desktop — raw `website/docs/user-guide/desktop.md` | Nous Research | living page | 2026-09-07 | "Providers settings pane … Its **Local Models** view installs and manages an on-device llama.cpp runtime"; "**Set the default in Settings → Model.** … it's the only place that writes it"; the failed-turn error card's **Switch provider** action jumping to the provider/endpoint/auth/billing settings |
| [7] | Docs | Fallback Providers | https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers — raw `website/docs/user-guide/features/fallback-providers.md` | Nous Research | living page | 2026-09-07 | `hermes fallback` with `add`/`list`/`remove`/`clear` and the same picker as `hermes model`; the `fallback_providers:` shape; the trigger list (429, 500/502/503 after retries; 401/403/404 immediately; malformed/empty responses); the per-turn, at-most-once scope; the prompt-cache warning in both directions; the `auxiliary:` shape with the vision-on-`http://localhost:1234/v1` example and "`base_url` takes precedence over `provider`"; `provider: "auto"` = main provider + main model; "subagents inherit the parent fallback chain" |
| [8] | Docs | Environment Variables | https://hermes-agent.nousresearch.com/docs/reference/environment-variables — raw `website/docs/reference/environment-variables.md` | Nous Research | living page | 2026-09-07 | "`LM_BASE_URL` | LM Studio base URL (default: `http://localhost:1234/v1`)"; "`OLLAMA_BASE_URL` | Override Ollama Cloud base URL (default: `https://ollama.com/v1`)" |
| [9] | Docs | Subagent Delegation | https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation — raw `website/docs/user-guide/features/delegation.md` | Nous Research | living page | 2026-09-07 | the uncommented local `delegation:` block (`model: "qwen2.5-coder"`, `base_url: "http://localhost:1234/v1"`, `api_key: "local-key"`); "the children are where the tokens go — a parallel batch of subagents typically burns the large majority of a run's total tokens" |
| [10] | Docs | Hermes Desktop — download page | https://hermes-agent.nousresearch.com/desktop | Nous Research | living page | 2026-09-07 | the `Hermes-Setup.dmg` / `Hermes-Setup.exe` links carrying `?build=06402ecb7ca5`; the footer label "Hermes Agent v0.21.0"; "macOS 12 or later, Windows 10/11, and any Linux distribution. On Linux the agent installs through the terminal instead of an installer package." |
| [11] | Release | Hermes Agent v0.21.0 (v2026.8.31) — release notes | https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.31 | NousResearch/hermes-agent | published 2026-08-31T19:29:49Z | 2026-09-07 (GitHub REST via `gh api`) | the tag, name and date of the newest release; the **absence** of any local-models / llama.cpp mention in the body; the `model_overrides` line "patch context windows, pricing, or capabilities for any model without waiting on a release" citing PR #85560 |
| [12] | Release | commit 43e67d87 — "feat: local models — managed llama.cpp runtime with one-click desktop setup" (+ the `hermes_cli/local_runtime/` files it added, read on `main` the same day) | https://github.com/NousResearch/hermes-agent/commit/43e67d87 | NousResearch/hermes-agent | committed 2026-09-01T20:01:53Z | 2026-09-07 (GitHub REST via `gh api`, plus raw file fetches) | the commit date, title and 117-file count; the ancestry comparisons; `catalog.json` model ids/repos/quants/`size_bytes` behind Table 1; `supervisor.py` (`_DEFAULT_PORT = 18434`, `--host 127.0.0.1`, `--jinja`, `IDLE_UNLOAD_S = 15 * 60`); `context_policy.py` (`FLOOR = 64 * 1024`) |
| [13] | Issue | #102865 — Desktop Local Models: catalog auto-pick spawns infeasible config (35B/64K ctx on 8GB VRAM+30GB RAM) → full desktop freeze via swap thrash | https://github.com/NousResearch/hermes-agent/issues/102865 | NousResearch/hermes-agent | opened 2026-09-04, **open** on 2026-09-07; labels type/bug, comp/cli, backend/local, P2, comp/desktop | 2026-09-07 (GitHub REST via `gh api`) | RTX 4070 Laptop 8 GiB VRAM + 30 GiB RAM on Linux; auto-pick `qwen3.6-35b-a3b` (21.1 GiB); preset `ctx-size = 65536`; "Working set >> available RAM → kernel swaps… → full desktop freeze"; hard reboot |
| [14] | Issue | #103949 — local_runtime: select_backend() returns 'cuda' on Linux+NVIDIA but no Linux CUDA prebuilt exists | https://github.com/NousResearch/hermes-agent/issues/103949 | NousResearch/hermes-agent | opened 2026-09-05, **open** on 2026-09-07; labels type/bug, comp/cli, P2 | 2026-09-07 (GitHub REST via `gh api`) | `BinaryResolutionError: no prebuilt linux CUDA asset at {tag}; use vulkan/cpu or a source build`; `select_backend()` returning `cuda` for every non-macOS NVIDIA machine; the tested `backend="vulkan"` workaround |
| [15] | Issue | #43900 — Ollama local models silently capped at 4096-token context — causes finish_reason=length and garbled retry responses | https://github.com/NousResearch/hermes-agent/issues/43900 | NousResearch/hermes-agent | opened 2026-06-11, **open** on 2026-09-07; labels type/bug, comp/agent, provider/ollama, area/config, P2 | 2026-09-07 (GitHub REST via `gh api`) | GGUF metadata 131,072 for Gemma 4 vs Ollama's 4,096 default; the OpenAI-compat route ignoring `extra_body.options.num_ctx`; `finish_reason="length"` with empty/truncated content; the UI still showing `0 / 131.1K` |
| [16] | Issue | #87697 — Hermes Client cancels local LLM streams after ~1.5s during prompt evaluation / reasoning (triggering `<unused49>` token loop) | https://github.com/NousResearch/hermes-agent/issues/87697 | NousResearch/hermes-agent | opened 2026-08-16, **open** on 2026-09-07; labels type/bug, comp/agent, provider/ollama, P2, needs-repro, area/streaming | 2026-09-07 (GitHub REST via `gh api`) | cancellation "after approximately 1.4 to 1.6 seconds"; the four continuation attempts; the `<unused49>` run; the reporter's "~17k tokens from tool schemas" analysis and "1.5–2.5 seconds before the first text token"; the Ollama log line `task.n_tokens = 16862` |

---

## Verification record

**Method.** Every docs page was fetched this run with `curl` from
`https://raw.githubusercontent.com/NousResearch/hermes-agent/main/…` (HTTP 200 each) into the
session scratchpad, and read from disk. The rendered `…/docs/user-guide/local-models` page and the
`…/desktop` product page were fetched from `hermes-agent.nousresearch.com` (HTTP 200 each). The
**unauthenticated** GitHub REST API returned **HTTP 403 — "API rate limit exceeded"** for every
call from this host, so all GitHub facts (releases, commits, compare, issues, PR) were re-fetched
with the authenticated `gh api` CLI. Catalog byte totals were computed here with Python from the
fetched `catalog.json`, not copied from any prose.

**[1] `local-models.md`** — 200, 5,880 bytes. Verbatim strings confirmed present: "Nothing leaves
your computer: no account, no API key, and no network access after a model is downloaded.";
"Open **Settings → Providers → Local Models** (or choose **Run models locally** during
onboarding)"; "Click **Install runtime**. Hermes downloads the official llama.cpp build for your
hardware (a few hundred MB), verifies it, and keeps it updated."; "Pick a model from the catalog
and click **Download**."; "Click **Use**. New chats now run on the local model."; "That's the whole
flow."; "switching back to a cloud provider is one click in the model picker"; "priced against
**your machine** before you download anything"; green *Fits your GPU* / amber *Uses system RAM* /
red *Too big for this machine*; "Models that don't fit stay visible with the reason"; "**Every
recommended model gets at least a 64K context window.**"; "in the order that hurts least (expert
weights first, never the attention cache)"; "Idle models are unloaded after 15 minutes"; "a
curated starting point, not a boundary"; **Find more models**; **Add model file**; "Point a custom
endpoint at any OpenAI-compatible server for full manual control — the managed runtime is a
default, not a requirement."; the `local_runtime:` YAML block (`enabled: false`, `backend: auto`,
`tag: b10362`) copied character for character with its comments; "Models and runtime builds live
under the Hermes home directory (`models/` and `runtimes/llamacpp/`)"; "uses the standard
`model.provider: llamacpp` + `model.default` settings — the same shape as every other provider";
"**Windows and Linux:** NVIDIA GPU (CUDA) or CPU. **macOS:** Apple Silicon (Metal). Vulkan builds
serve AMD GPUs."; "A GPU with 8 GB+ of memory runs the small catalog models comfortably; 16 GB+
runs the 27–35B models at high quality."; "Model downloads are byte-size checked against the
catalog during the transfer; an incomplete download is deleted and reported, never half-used."
The rendered page at `hermes-agent.nousresearch.com/docs/user-guide/local-models` returned 200 and
contains the string "Install runtime", confirming the page is live, not just on `main`.
The docs page lists **no model names** — every name in Table 1's catalog rows comes from [12].

> Discrepancy noted, **not used**: the docs example pins `tag: b10362`, while `catalog.json`'s
> `qwen3.8-flash-next` entry requires `min_engine: b10678`, and issue [13]'s environment block shows
> a user running `local_runtime.tag: b10679`. The post quotes the docs block verbatim and makes no
> claim about which tag is current.

**[2] `providers.md`** — 200, 85,919 bytes. Verbatim checks: line 760, "Hermes Agent requires at
least **64,000 tokens** of context for agent use with tools. Smaller windows are rejected at
startup because the system prompt, tool schemas, and working conversation state need enough room
for reliable multi-step workflows."; "Hermes Agent works with **any OpenAI-compatible API
endpoint**. If a server implements `/v1/chat/completions`, you can point Hermes at it."; the Ollama
default-context table "Less than 24 GB | **4,096 tokens** / 24–48 GB | 32,768 tokens / 48+ GB |
256,000 tokens"; "**You cannot set context length through the OpenAI-compatible API** … This is the
#1 source of confusion when integrating Ollama with tools like Hermes."; Option 1
`OLLAMA_CONTEXT_LENGTH=64000 ollama serve`; Option 3
`echo -e "FROM qwen2.5-coder:32b\nPARAMETER num_ctx 64000" > Modelfile` then
`ollama create qwen2.5-coder-64k -f Modelfile`; `ollama ps` / "Look at the CONTEXT column"; the
llama-server block `./build/bin/llama-server \ --jinja -fa \ -c 64000 \ -ngl 99 \ -m
models/qwen2.5-coder-32b-instruct-Q4_K_M.gguf \ --port 8080 --host 0.0.0.0`; "If using parallel
slots (`-np`), the total context is divided among slots — with `-c 64000 -np 4`, each slot only
gets 16k"; "Without `--jinja`, llama-server ignores the `tools` parameter entirely." plus the
`{"name": "web_search", ...}` symptom and "the `chat_template` field should be present" at
`http://localhost:8080/props`; the vLLM block with `--port 8000 --max-model-len 65536
--tensor-parallel-size 2 --enable-auto-tool-choice --tool-call-parser hermes`;
"`--enable-auto-tool-choice` | Required for `tool_choice: "auto"` (the default in Hermes)"; the
parser list "`hermes` (Qwen 2.5, Hermes 2/3), `llama3_json` (Llama 3.x), `mistral`, `deepseek_v3`,
`deepseek_v31`, `xlam`, `pythonic`"; SGLang "`--tool-call-parser` … `qwen` (Qwen 2.5), `llama3`,
`llama4`, `deepseekv3`, `mistral`, `glm`. Without this flag, tool calls come back as plain text.";
the fix table row "**Ollama** | Tool calling is enabled by default — make sure your model supports
it (check with `ollama show model-name`)" and "**LM Studio** | Update to 0.3.6+ and use a model
with native tool support"; the LM Studio section — `lms server start  # Starts on port 1234`,
`lms load qwen2.5-coder --context-length 64000`, "Press Enter to use http://localhost:1234/v1",
"If LM Studio server auth is enabled, enter LM_API_KEY when prompted", the gear-icon steps 1–4
including "If your machine cannot fit 64000, consider using a smaller model with larger context
lengths.", `--estimate-only`, "Hermes preserves the context of an already-loaded LM Studio
instance. For an unloaded model in the default explicit mode, Hermes omits `context_length` unless
you configured one in Hermes … Hermes then uses only the context length LM Studio reports after
loading.", `hermes config set model.lmstudio_load_mode jit|explicit`, "**Tool calling:** Supported
since LM Studio 0.3.6. Models with native tool-calling training (Qwen 2.5, Llama 3.x, Mistral,
Hermes) are auto-detected"; the wizard prompts "Select "Custom endpoint (self-hosted / VLLM /
etc.)"", "Skip API key (Ollama doesn't need one)", "Enter model name — or leave blank to
auto-detect if only one model is loaded"; the `hermes model` vs `/model` warning box; the nine
numbered steps of "Context Length Detection" ending in "**Fallback defaults** — broad model family
patterns (128K default)"; and the Ollama tip "Both speak the same OpenAI-compatible API. Cloud is a
first-class provider (`--provider ollama-cloud`, `OLLAMA_API_KEY`); local Ollama is reached via the
Custom Endpoint flow (base URL `http://localhost:11434/v1`, no key). Use cloud for large models you
can't run locally; use local for privacy or offline work." Dedicated sections exist for Ollama,
vLLM, SGLang, llama.cpp and LM Studio; LocalAI (`http://localhost:8080/v1`) and Jan
(`http://localhost:1337/v1`) appear as rows in the compatible-providers table.
> **Not found on this page, therefore not asserted:** `LM_BASE_URL` (it is on [8] only) and
> `model.ollama_num_ctx` (absent from every page fetched).

**[3] `local-ollama-setup.md`** — 200, 12,784 bytes. Verbatim: the model table row
"`gemma4:31b` | ~20 GB | 24+ GB | Yes | Best quality — strong tool use and reasoning"; "of the
models listed above, only `gemma4:31b` has reliable tool calling"; "By default, Ollama uses a
2048-token context. Hermes requires at least 64,000 tokens for agentic work with tools:"; the
Modelfile heredoc `FROM gemma4:31b` / `PARAMETER num_ctx 64000` and `ollama create gemma4-64k -f
/tmp/Modelfile`; "By default, Ollama unloads models after 5 minutes of inactivity" and
`Environment="OLLAMA_KEEP_ALIVE=24h"`; `HERMES_API_TIMEOUT=1800   # 30 minutes — generous for slow
local models`; "**Widen the API timeout** — set `HERMES_API_TIMEOUT=1800` in `~/.hermes/.env`"; the
worked test prompts including "List all Python files in this directory and count the lines of code
in each"; the hybrid config `model: default: "gemma4:31b" / provider: "custom" / base_url:
"http://localhost:11434/v1"` with `fallback_providers: - provider: openrouter / model:
anthropic/claude-sonnet-4` and "This way, 90% of your usage is free (local), and only the hard
tasks hit the paid API."

**[4] `local-llm-on-mac.md`** — 200, 10,161 bytes. Verbatim: "we recommend **Qwen3.5-9B**"; the row
"Qwen3.5-9B-Q4_K_M (GGUF) | 5.3 GB | ~10 GB with quantized KV cache | llama.cpp"; the KV table
"f16 (default) | ~16 GB / q8_0 | ~8 GB / **q4_0** | **~4 GB**"; "`--cache-type-k q4_0` | Quantize
the key cache to 4-bit. **This is the big memory saver.**"; "If you're still running out of memory,
reduce context only while staying at or above Hermes' 64K minimum"; "Hermes sends its system prompt
and tool schemas on every call, so on slower hardware the first turn can involve minutes of silence
while the model processes that prompt before generating anything. That's prefill at work, not a
stalled session." and the pointer to trimming it "with `hermes prompt-size`". The guide's own
`llama-server` invocation carries **no** `--jinja`; the post's llama-server block is the
providers-page one, which does — noted so the two are not confused.

**[5] `faq.md`** — 200, 35,609 bytes. Verbatim: the block `hermes model` / `# Select: Custom
endpoint (enter URL manually)` / `# API base URL: http://localhost:11434/v1` / `# API key: ollama`
/ `# Model name: qwen3.5:27b` / `# Context length: 64000   ← Hermes minimum; set this to match your
server's actual context window`; "If you set a custom `num_ctx` in Ollama … Ollama's `/api/show`
reports the model's *maximum* context, not the effective `num_ctx` you configured."; "Hermes
auto-detects local endpoints and relaxes streaming timeouts (read timeout raised from 120s to
1800s, stale stream detection disabled). If you still hit timeouts on very large contexts, set
`HERMES_STREAM_READ_TIMEOUT=1800` in your `.env`."; "`hermes update` pulls the latest code and
reinstalls dependencies **once** (not per-profile)."

**[6] `desktop.md`** — 200, 54,936 bytes. Verbatim: "**Providers settings pane** — a dedicated
place to manage inference providers … Its **Local Models** view installs and manages an on-device
llama.cpp runtime — see [Local Models](/user-guide/local-models)."; "**Set the default in Settings
→ Model.** That "main" model is your **per-profile global default** — it's what new chats, crons,
subagents, and auxiliary tasks start from, and it's the only place that writes it."; "**Switch
provider** — jumps to Settings → Models for provider, endpoint, auth, and billing failures."

**[7] `fallback-providers.md`** — 200, 21,576 bytes. Verbatim: "`hermes fallback` reuses the
provider picker from `hermes model` … Use the subcommands `add`, `list` (alias `ls`), `remove`
(alias `rm`), and `clear`"; the `fallback_providers:` example with `provider: openrouter` /
`model: anthropic/claude-sonnet-4`; the trigger list "**Rate limits** (HTTP 429) — after exhausting
retry attempts / **Server errors** (HTTP 500, 502, 503) — after exhausting retry attempts / **Auth
failures** (HTTP 401, 403) — immediately / **Not found** (HTTP 404) — immediately / **Invalid
responses**"; "Fallback is **turn-scoped**: each new user message starts with the primary model
restored … Within a single turn, fallback activates at most once"; the prompt-cache warning
"Prompt caches are keyed to the model (and on most providers, the account) … the same applies when
the turn ends and the primary is restored — that first request back on the primary is a full
re-read too"; the `auxiliary:` block with `base_url: ""  # direct endpoint (takes precedence over
provider)` and the local vision example `base_url: "http://localhost:1234/v1"` / `api_key:
"local-key"` / `model: "qwen2.5-vl"` plus "`base_url` takes precedence over `provider`."; "When a
task's provider is set to `"auto"` (the default), Hermes first tries the main provider + main model
for that auxiliary task."; "Subagent delegation | ✔ (subagents inherit the parent fallback chain)".

**[8] `environment-variables.md`** — 200, 99,755 bytes. Verbatim rows: "`LM_API_KEY` | API key for
LM Studio (`lmstudio` provider). Often a placeholder for local servers"; "`LM_BASE_URL` | LM Studio
base URL (default: `http://localhost:1234/v1`)"; "`OLLAMA_BASE_URL` | Override Ollama Cloud base
URL (default: `https://ollama.com/v1`)"; "`HERMES_STREAM_READ_TIMEOUT` | Streaming socket read
timeout in seconds (default: `120`). Auto-increased to `HERMES_API_TIMEOUT` for local providers."

**[9] `delegation.md`** — 200, 36,087 bytes. Verbatim: the block `delegation:` / `model:
"qwen2.5-coder"` / `base_url: "http://localhost:1234/v1"` / `api_key: "local-key"` (lines 534–537);
"the children are where the tokens go — a parallel batch of subagents typically burns the large
majority of a run's total tokens, so the worker model is where the cost actually lives."

**[10] Desktop download page** — 200, 79,386 bytes. Found: four occurrences of the substring
`build=06402ecb7ca5`, on the hrefs
`https://hermes-assets.nousresearch.com/Hermes-Setup.dmg?build=06402ecb7ca5` and
`https://hermes-assets.nousresearch.com/Hermes-Setup.exe?build=06402ecb7ca5`; the only version
string on the page is `v0.21.0`, rendered in the footer as "Hermes Agent v0.21.0"; the platform
copy "macOS 12 or later, Windows 10/11, and any Linux distribution. On Linux the agent installs
through the terminal instead of an installer package." No "beta" or "public preview" label appears.

**[11] Release v2026.8.31** — `gh api repos/NousResearch/hermes-agent/releases?per_page=6` returns,
newest first: `v2026.8.31` "Hermes Agent v0.21.0 (v2026.8.31)" published `2026-08-31T19:29:49Z`
(draft=false, prerelease=false), then v2026.8.27, v2026.8.19, v2026.8.18, v2026.8.16.2, v2026.8.16.
**There is no tag newer than v2026.8.31 on 2026-09-07.** Grepping the release body for
`local model|llamacpp|llama.cpp|local_runtime` matches only the two `model_overrides` lines —
nothing about a managed local-model runtime. The `model_overrides` bullet reads: "**Per-model
metadata overrides** via `model_overrides` config — patch context windows, pricing, or capabilities
for any model without waiting on a release ([#85560])". PR #85560 was fetched separately
(`gh api …/pulls/85560`): state closed, `merged: true`, `merged_at 2026-08-13T20:33:54Z`, title
"feat(models): per-model metadata overrides via model_overrides config"; its body carries the
`model_overrides:` YAML reproduced in the post (`custom:my-local-vllm` / `my-llava-model`
`context_window: 8192` + `supports_vision: true`; `_default` `context_window: 32768` with the
comment "fill-gap only: models not in the catalog") and the field list `context_window`,
`max_output_tokens`, `supports_tools` / `supports_vision` / `supports_reasoning`, `model_family`.

**[12] commit 43e67d87 and the `local_runtime` sources** —
`gh api repos/NousResearch/hermes-agent/commits/43e67d87`: sha
`43e67d872f769de6c40f3549277d88dfb2d47382`, committer date `2026-09-01T20:01:53Z`, first line of
the message "feat: local models — managed llama.cpp runtime with one-click desktop setup",
`files` length **117**.
Ancestry, both via `gh api …/compare/…`:
`v2026.8.31...43e67d87…` → status "ahead", ahead_by **242**, behind_by 0 (so the commit is after the
tag); `43e67d87…...06402ecb7ca5` → status "ahead", ahead_by **5139**, behind_by 0 (so the download
page's build commit **contains** the feature commit).
`gh api …/commits/06402ecb7ca5` → sha `06402ecb7ca5c583f035941a88acc803ddaf9118`, author date
`2026-09-06T10:04:59Z`, committer date `2026-09-06T10:10:05Z`, message "test(desktop): tighten the
real-sh mutex quoting test".
`hermes_cli/local_runtime/catalog.json` — 200, 4,898 bytes, `schema_version: 1`, exactly four
entries. Byte sums computed here with Python:
- `qwen3.8-27b` "Qwen3.8 27B", repo `unsloth/Qwen3.8-27B-GGUF`, quant `UD-Q4_K_M`, 1 file
  **16,464,440,224 B = 16.46 GB = 15.33 GiB**; `mmproj` 931,146,432 B (**0.87 GiB**);
  `n_ctx_train` 262,144; `quality` 90; description "Best all-round agent model; sees images; long
  context stays fast".
- `qwen3.6-35b-a3b` "Qwen3.6 35B-A3B", repo `unsloth/Qwen3.6-35B-A3B-MTP-GGUF`, `UD-Q4_K_M`,
  1 file **22,663,387,424 B = 22.66 GB = 21.11 GiB**; `mmproj` 902,822,528 B (**0.84 GiB**);
  the **only** variant in the file with `"validated": true`; `quality` 80.
- `qwen3.8-flash-next` "Qwen3.8 Flash Next", repo `unsloth/Qwen3.8-Flash-Next-GGUF`,
  `UD-Q4_K_XL`, **4 files summing 111,334,654,784 B = 111.33 GB = 103.69 GiB**; `min_engine`
  `b10678`; `quality` 95; description "Frontier-scale model; needs a very large GPU to run well".
- `deepseek-v4-flash` "DeepSeek V4 Flash", repo `unsloth/DeepSeek-V4-Flash-0731-GGUF`,
  `UD-Q4_K_XL`, **5 files summing 155,095,241,120 B = 155.10 GB = 144.44 GiB**; `draft`
  `dspark-DeepSeek-V4-Flash-0731-Q8_0.gguf` 10,896,057,440 B (**10.15 GiB**); `n_ctx_train`
  1,048,576; description "Frontier-class model for machines with 128GB+ memory".
  *The post prints the GiB figures and says so; the GB figures are recorded here for completeness.*
`hermes_cli/local_runtime/supervisor.py` — 200, 17,407 bytes: `_DEFAULT_PORT = 18434`;
`s.bind(("127.0.0.1", _DEFAULT_PORT))` with a `s.bind(("127.0.0.1", 0))` fallback and the log line
"port — existing sessions may need a model re-pick"; `IDLE_UNLOAD_S = 15 * 60`;
`f"http://127.0.0.1:{self.port}/v1"`; the `_spawn` argument list containing `"--host",
"127.0.0.1"`, `"--port"`, `"--api-key"`, `"--models-dir"`, `"--models-max"`,
`"--models-autoload"`, `"--metrics"`, `"--slots"`, `"--no-webui"`, **`"--jinja"`**, `"-dio"`.
`hermes_cli/local_runtime/context_policy.py` — 200, 8,926 bytes: `FLOOR = 64 * 1024` with the
comment "= target; one internal constant", i.e. **65,536**.
(`endpoint.py`, 200, 6,087 bytes, and `bootstrap.py`, 200, 13,097 bytes, were fetched and read but
no fact from them appears in the post.)

**[13] #102865** — `gh api …/issues/102865`: state **open**, created 2026-09-04, labels
type/bug, comp/cli, backend/local, P2, comp/desktop. Body verbatim: "laptop, NVIDIA RTX 4070 Laptop
(8 GiB VRAM) + AMD iGPU …, 30 GiB RAM, Linux (CachyOS)"; "Catalog auto-pick: `recommended_id(budget)`
returns **`qwen3.6-35b-a3b`** … a 21.1 GiB weights model (UD-Q4_K_M, unquantized mmproj 0.9 GiB)";
"`generate_presets()` writes a preset with **`ctx-size = 65536`**"; "Working set >> available RAM →
kernel swaps (zram zstd + 32 G swapfile) → **full desktop freeze** → user must hard-reboot."

**[14] #103949** — `gh api …/issues/103949`: state **open**, created 2026-09-05, labels type/bug,
comp/cli, P2. Body verbatim: "Reproduced on: Ubuntu 26.04, RTX 5070 Ti, driver 610.43.02, tag
b10679, hermes 0.21.0"; "`select_backend()` returns `"cuda"` for any NVIDIA vendor on non-macOS,
including Linux"; "`asset_plan()` then raises `BinaryResolutionError: no prebuilt linux CUDA asset
at {tag}; use vulkan/cpu or a source build`"; "**Verified workaround (tested end-to-end):**
explicitly pass `backend="vulkan"` … installs, boots, and serves catalog models correctly".

**[15] #43900** — `gh api …/issues/43900`: state **open**, created 2026-06-11, labels type/bug,
comp/agent, provider/ollama, area/config, P2. Body verbatim: "the model runs with Ollama's
**default `num_ctx` (4096 tokens)** even though the GGUF metadata reports a much larger context
(e.g. 131,072 for Gemma 4). Hermes reads the GGUF value and stores it in `_ollama_num_ctx`, but
never actually sends it to Ollama's `/v1/chat/completions` endpoint — because the OpenAI-compat
route **ignores** the `extra_body.options.num_ctx` field"; "every response returns
`finish_reason="length"` with empty or truncated content — even when the Hermes UI shows
`0 / 131.1K` context usage. The truncation-retry loop then concatenates three broken partial
responses into garbled output."

**[16] #87697** — `gh api …/issues/87697`: state **open**, created 2026-08-16, labels type/bug,
comp/agent, provider/ollama, P2, needs-repro, area/streaming. Body verbatim: "Hermes issues a
client-side cancellation (`cancel task`) after approximately 1.4 to 1.6 seconds while the local
model is still evaluating the system prompt / generating initial reasoning chunks. This triggers a
broken retry loop (4 continuation attempts) and outputs raw `<unused49>` token artifacts.";
environment "Hermes Agent (CLI `hermes chat` and Desktop Wrapper) both V 0.20.1", backend
"Ollama (`http://127.0.0.1:11434/v1`)", model "Gemma 4 (26B) with custom parameters (`num_ctx
131072`…)"; the pasted Ollama log line "slot operator(): id 1 | task 64 | new prompt, n_ctx_slot =
131072, **task.n_tokens = 16862**" and "`[GIN] | 200 | 1.621478725s`". The "~17k tokens from tool
schemas" root-cause sentence is the reporter's own analysis and is attributed as such in the post.

**Supporting fetches this run, not cited in the post:**
`website/docs/user-guide/configuration.md` (200, 197,007 B — contains "Hermes raises this to 30
minutes when it detects a local endpoint"; the post uses the FAQ's "120s to 1800s" wording
instead); `website/docs/user-guide/configuring-models.md` (200, 22,936 B — the 11 auxiliary slots
and the `auxiliary` YAML; dropped because [7] carries the same shapes);
`website/docs/getting-started/quickstart.md` (200, 20,110 B);
`website/docs/reference/cli-commands.md` (200 — `hermes update` "Pull latest code and reinstall
dependencies", `hermes desktop` (alias `gui`) "Build and launch the native Electron desktop app",
`hermes fallback` subcommands, `hermes prompt-size`; dropped because [5], [7] and [4] carry the
three facts the post actually uses);
`website/docs/reference/model-catalog.md` (200 — no `model_overrides` section);
`hermes_cli/local_runtime/endpoint.py` and `bootstrap.py` (200 each);
`gh api repos/NousResearch/hermes-agent/contents/website/docs/reference` (directory listing, used
to establish that there is no `reference/cli.md`);
`https://www.youtube.com/oembed?url=…GL67DEf2nyI` (200 — title "Full Hermes Agent Tutorial
(Desktop) 🧠 A Useful Agentic AI Workflow", author Wanderloots). **The video is not cited**: the
post's Desktop click-path is sourced entirely from [6] and [1], so no Community reference was
needed and none appears in the published list.

---

## Claims and numbers

| Value | Source | Where it lands in the post |
|---|---|---|
| Three roads: managed `llamacpp`, `lmstudio`, `custom` + `base_url` | [1], [2] | §1 `<ul>`, Table 2 |
| "works with any OpenAI-compatible API endpoint … `/v1/chat/completions`" | [2] | §1 |
| "Nothing leaves your computer: no account, no API key, and no network access after a model is downloaded." | [1] | §1 |
| The docs name Ollama, vLLM, llama.cpp server, SGLang, LocalAI, Jan | [2] | §1 |
| 64,000-token floor, "rejected at startup", quoted verbatim | [2] | §2 heading + `.alert danger` + takeaway |
| `-c 64000 -np 4` → 16k per slot | [2] | §2 `.alert danger` |
| "Every recommended model gets at least a 64K context window"; expert-weights-first overflow | [1] | §2 |
| `FLOOR = 64 * 1024` = 65,536 | [12] | §2, takeaway |
| Tool-call flags: `--jinja`; `--enable-auto-tool-choice --tool-call-parser hermes`; `--tool-call-parser qwen`; Ollama default-on + `ollama show`; LM Studio 0.3.6+ | [2] | §2 `<ul>`, Table 2, takeaway |
| `{"name": "web_search", ...}` printed as a message; `chat_template` at `/props` | [2] | §2 |
| Catalog: `qwen3.8-27b` ≈15.3 GiB + mmproj ≈0.87 GiB; `qwen3.6-35b-a3b` ≈21.1 GiB + mmproj ≈0.84 GiB (only `validated` entry); `qwen3.8-flash-next` ≈103.7 GiB across 4 files; `deepseek-v4-flash` ≈144.4 GiB across 5 files + draft ≈10.1 GiB; repos and quant names | [12] | Table 1 |
| Catalog descriptions "needs a very large GPU to run well" / "for machines with 128GB+ memory" | [12] | Table 1 |
| "8 GB+" small models, "16 GB+" for 27–35B | [1] | Table 1, §3, takeaway |
| Green / amber / red memory fit, and unfit models staying visible with a reason | [1] | §3, §4 step 3 |
| `gemma4:31b` ~20 GB / 24+ GB RAM / only reliable tool caller in its table | [3] | Table 1 |
| Qwen3.5-9B `Q4_K_M` 5.3 GB / ~10 GB at 128K with quantized KV; guide silent on tool calling | [4] | Table 1 |
| KV cache at 128K on a 9B: f16 ~16 GB, q8_0 ~8 GB, q4_0 ~4 GB | [4] | §3 |
| "a curated starting point, not a boundary"; Find more models; Add model file | [1] | §3 |
| No Hermes-family model is recommended for local tool use on any docs page read | [1], [2], [3], [4], [12] | §3 💡 blockquote |
| Path A four-step flow + "That's the whole flow." + "New chats now run on the local model." | [1] | §4 intro + `<ol>` |
| Install runtime = a few hundred MB, verified, kept updated; CUDA/CPU on Win+Linux, Metal on Apple Silicon, Vulkan for AMD | [1] | §4 step 2 |
| Byte-size checked downloads, "never half-used" | [1] | §4 step 4 |
| Test prompt "List all Python files in this directory and count the lines of code in each" | [3] | §4 step 6, §5 step 6 (paraphrased) |
| `grep -A3 local_runtime ~/.hermes/config.yaml` — **author-composed shell command**; the path and the key are documented in [1] | [1] | §4 step 7 |
| The `local_runtime:` block verbatim (`enabled`, `backend`, `tag: b10362`) | [1] | §4 `<pre>` |
| `model.provider: llamacpp` + `model.default`, "the same shape as every other provider"; `models/` and `runtimes/llamacpp/` | [1] | §4, Table 2 |
| `127.0.0.1`, default port 18434, free-port fallback, `--jinja` always passed, 15-minute idle unload | [12] (unload also [1]) | §4, Table 1 "Tool calling", Table 2 |
| commit 43e67d87 dated 2026-09-01, 117 files; 242 commits after tag v2026.8.31; build `06402ecb7ca5` dated 2026-09-06, 5,139 ahead / 0 behind | [12] | §4 `.alert info`, takeaway |
| Newest tag v2026.8.31 = v0.21.0, 2026-08-31, notes silent on local models | [11] | §4 `.alert info`, takeaway |
| Download page serves `?build=06402ecb7ca5`; footer says "Hermes Agent v0.21.0" | [10] | §4 `.alert info` |
| "`hermes update` pulls the latest code and reinstalls dependencies" | [5] | §4 `.alert info` |
| Providers pane holds the Local Models view | [6] | §4 step 1 |
| #102865: RTX 4070 Laptop 8 GiB + 30 GiB RAM, auto-pick `qwen3.6-35b-a3b`, `ctx-size = 65536`, swap thrash, hard reboot | [13] | §4 `<ul>` |
| #103949: `BinaryResolutionError: no prebuilt linux CUDA asset`, `select_backend()` returning cuda, tested `vulkan` workaround | [14] | §4 `<ul>` |
| LM Studio: `lmstudio` provider, `lms server start` on 1234, `lms load … --context-length 64000`, `--estimate-only`, gear-icon steps, reload to apply, 0.3.6+, auto-detected families, explicit-vs-jit behaviour | [2] | §5 `<ol>` + `<pre>` + closing paragraph |
| `LM_BASE_URL` default `http://localhost:1234/v1` | [8] | §5 closing paragraph, Table 2 |
| `LM_API_KEY` only when server auth is on | [2] | §5 closing paragraph |
| `Settings → Model` is the only place that writes the profile default | [6] | §5 step 5, §6 |
| `hermes model` → "Custom endpoint (self-hosted / VLLM / etc.)"; skip key; blank model name auto-detects; `/model` cannot add providers | [2] | §6 `<ol>` |
| Context length `64000` with "Hermes minimum; set this to match your server's actual context window" | [5] | §6 step 5 |
| **Switch provider** on the failed-turn card | [6] | §6 |
| Managed runtime "is a default, not a requirement"; point a custom endpoint at any OpenAI-compatible server | [1] | §6 |
| `OLLAMA_CONTEXT_LENGTH=64000 ollama serve`; the `echo -e … > Modelfile` + `ollama create qwen2.5-coder-64k`; `ollama ps` | [2] | §6 `<pre>` 1 |
| llama-server block verbatim; `curl …/props | jq '.default_generation_settings.n_ctx'` | [2] | §6 `<pre>` 2 |
| `vllm serve … --max-model-len 65536 --tensor-parallel-size 2 --enable-auto-tool-choice --tool-call-parser hermes` verbatim | [2] | §6 `<pre>` 3 |
| Ports 11434 / 8080 / 8000 / 1234 / 18434 | [2], [8], [12] | Table 2 |
| Local Ollama is a Custom endpoint; Ollama Cloud is `--provider ollama-cloud` with `OLLAMA_API_KEY`; "Use cloud for large models you can't run locally; use local for privacy or offline work." | [2] (Cloud base URL also [8]) | §6 💡 blockquote |
| Ollama default context 4,096 / 32,768 / 256,000 by VRAM band; "the #1 source of confusion" | [2] | §7 `<ul>` |
| Ollama guide's competing "2048-token context" figure, presented as a disagreement | [3] | §7 |
| #43900: 131,072 GGUF vs 4,096 in use; `finish_reason="length"`; `0 / 131.1K` | [15] | §7 |
| `/api/show` reports the maximum, not the configured `num_ctx` | [5] | §7 |
| Nine-step context resolution chain; 128K default for unknown models | [2] | §7 |
| Prefill: "That's prefill at work, not a stalled session."; `hermes prompt-size` | [4] | §7 |
| 120s → 1800s read timeout on local endpoints, stale detection disabled; `HERMES_STREAM_READ_TIMEOUT=1800` | [5] | §7, takeaway |
| `HERMES_API_TIMEOUT=1800`; `OLLAMA_KEEP_ALIVE=24h`; Ollama's five-minute idle unload | [3] | §7 |
| #87697: ~1.5 s cancel, four continuation attempts, `<unused49>` run, ~17k-token system prompt, `task.n_tokens = 16862` | [16] | §7 |
| `model_overrides` release-notes wording, PR #85560 merged 2026-08-13, field list, and the YAML block | [11] | §7 `<ol>` + `<pre>` |
| `model.ollama_num_ctx` is **not** a documented key | [2], [5], [8] (searched, absent) | §7 closing paragraph |
| Local-primary + `fallback_providers` block and "This way, 90% of your usage is free (local)…" | [3] | §8 `<pre>` + prose |
| `hermes fallback add` / `list` / `remove` / `clear`, same picker as `hermes model` | [7] | §8 |
| Trigger conditions; turn scope and at-most-once; prompt-cache loss both ways | [7] | §8 `<ul>`, takeaway |
| `auxiliary.vision` on `http://localhost:1234/v1`; `base_url` takes precedence over `provider`; `provider: auto` = main model | [7] | §8 `<pre>` + prose |
| `delegation:` local block verbatim; subagents are where most tokens go | [9] (inheritance of the chain: [7]) | §8 `<pre>` + prose |

---

## Dated statuses (true as of 2026-09-07)

- Newest tag/release: **v2026.8.31 = Hermes Agent v0.21.0**, published 2026-08-31T19:29:49Z. No
  newer tag exists.
- The managed llama.cpp runtime (commit 43e67d87, 2026-09-01) is on `main` and **in no tagged
  release**; the v0.21.0 notes do not mention it. The Desktop download page still labels itself
  v0.21.0 but serves installers built from commit 06402ecb7ca5 (2026-09-06), which **contains**
  43e67d87 (5,139 ahead / 0 behind). The post states exactly this chain and claims nothing beyond
  it — in particular it never says the feature "shipped in version X".
- The `…/docs/user-guide/local-models` page is live on the public docs site (HTTP 200, contains
  "Install runtime"), not merely present in the repo.
- Open issues cited, all confirmed **open** on 2026-09-07: #102865, #103949, #43900, #87697.
- PR #85560 merged 2026-08-13; `model_overrides` is described in the v0.21.0 release notes but does
  **not** appear on any docs page fetched (`providers.md`, `configuring-models.md`,
  `configuration.md`, `model-catalog.md` all searched) — the post therefore cites the release notes.
- The managed catalog holds exactly four entries today; the docs call it curated, so it may change.
  All four size figures in Table 1 were computed here from `size_bytes` and are labelled GiB.
- `LM_BASE_URL` is documented only in `environment-variables.md`, not on the providers page — the
  post cites [8] for it and [2] for `LM_API_KEY`.

---

## Do not assert (looked for, could not verify, or excluded by the brief)

- **No verbatim X-post text.** The Nous post announcing one-click local models
  (status 2095602995874410664) was not fetched in this run; nothing is quoted or paraphrased from it.
- **No "shipped in Desktop vX.Y" claim.** Only the tag / commit / build-parameter chain above.
- **No CLI command that installs the managed runtime.** None appears in [1] or in the
  `local_runtime` sources read; the post describes the Desktop UI only.
- **`model.ollama_num_ctx` is explicitly declined.** It appears only in issue reporters' text; a
  search of `providers.md`, `faq.md` and `environment-variables.md` found it nowhere. The post says
  so in §7 and points the reader at `OLLAMA_CONTEXT_LENGTH` / a Modelfile instead.
- **No Nous Hermes weights recommended for local tool use.** The post states only what the four
  fetched docs pages and the catalog show. The Hugging Face `Hermes-4.3-36B-GGUF` card was not
  fetched or cited.
- **No claim about which `local_runtime.tag` is current.** The docs example says `b10362`; the
  catalog's `min_engine` for one model is `b10678`; a reporter runs `b10679`. The post quotes the
  docs block and stops there.
- **No throughput numbers** (tokens/sec on named GPUs, CPU-only speeds, cost-per-session figures).
  They exist in [3] and in community blogs but are not needed by this post's argument and are not used.
- **No `--include-desktop` flag, `ollama launch hermes`, or `unsloth start hermes`.** Vendor or
  community-only; not fetched this run; not used.
- **No Community source at all.** The Wanderloots walkthrough was verified to exist (oEmbed 200)
  but the Desktop click-path is fully covered by [6] and [1], so the post ships with 16 primary
  references and no Community tag.
- **No LM Studio multi-model-residency claim** (PR #46106) — not fetched this run, not used.
- **Nothing about `/council`, Hermes Cloud prices, a "public preview" label, or CVE-2026-10223** —
  out of scope for this post and unverified here.
- **The research slice's catalog sizes ≈122 GB and ≈205 GB** for the two frontier models are
  **contradicted** by today's `catalog.json` (111.33 GB / 103.69 GiB and 155.10 GB / 144.44 GiB,
  summed here). The post uses the values computed from the fetched file.
