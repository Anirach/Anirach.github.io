# AI-Core + Jev in Practice

A practical companion for engineers and programmers: build one support-ticket
decision pipeline and compare a generative baseline, Jev-only decisions and a
hybrid with fallback. **The code is available now; all ten website lessons are
awaiting publication.** Their links below are planned destinations, not verified
live articles. The existing *Engineering AI-Core Systems* series remains separate.

Codex helps develop the software. Jev is an optional runtime decision component;
it does not generate code or text or power the coding assistant. Default providers
return hand-authored fixtures. No result here establishes improved live accuracy,
speed or operating cost. Those are hypotheses for a controlled benchmark.

## เริ่มต้นภาษาไทย

ใช้บทเรียนควบคู่กับ source ในตารางสิบตอนด้านล่าง บทเรียนบนเว็บไซต์ยังรอเผยแพร่
แต่โค้ดใน repo นี้รันออฟไลน์ได้แล้ว ใช้ Node 22.18 ขึ้นไป ไม่ต้องติดตั้ง SDK
และไม่ต้องมี API key สำหรับการทดลองออฟไลน์ ผล fixture เป็นข้อมูลสมมติที่ผู้เขียน
กำหนด ไม่ใช่ผลวัด Jev จริง การประหยัดต้นทุนหรือทำงานเร็วขึ้นต้องพิสูจน์ด้วยข้อมูลใหม่
และเกณฑ์คุณภาพเดียวกัน ส่วน live เป็นตัวเลือกที่อาจมีค่าใช้จ่ายและยังไม่ได้ทดสอบ

## Prerequisites, version pins and getting the code

| Component | Requirement / tested status |
|---|---|
| Runtime | Node **22.18+**, ESM; tested on macOS with **22.23.2** |
| Source download | Git, or GitHub **Code → Download ZIP** |
| Optional SDK | Exact **`@typesafe-ai/sdk@0.7.0`**; not installed/live-tested by the author |
| Optional model | **`jev-1.13.0`**, not a moving alias |
| Tests | Built-in `node:test`; no framework install |
| Data | 40 synthetic tickets: 12 validation, 24 test, 4 attack |

```sh
# Obtain the repository once; downloading requires network access.
git clone https://github.com/Anirach/ai-core-jev-tutorial.git
cd ai-core-jev-tutorial
node --version
node src/cli.mjs doctor
node --test --test-reporter=spec
node src/cli.mjs demo --mode hybrid --ticket T-001
```

If you downloaded the ZIP, extract it and enter its root instead. All commands
below run from the repository root. **No `npm install` is needed for offline work.**
`.nvmrc` records the tested version without installing it. `package.json` is
private to prevent accidental npm publication; GitHub visibility is public.
The direct SDK version is pinned, but no transitive lockfile is supplied because
the live SDK was not installed. Review a generated lockfile if you opt into live
use. Linux and Windows execution have not been tested.

Expected quickstart output: `doctor` reports 40 tickets, `default: "MOCK"`,
`sdkRequiredForOffline: false` and `paidCalls: 0`; tests report **43 pass, 0 fail**
in this initial revision. T-001 yields a billing **proposal**, one Jev-shaped
fixture attempt and an explicit **OFFLINE MOCK — NOT JEV INFERENCE** evidence label.
It does not execute an approved effect. `request` prints the pinned model and
minimal state without gold labels and makes no inference call.

The complete reference implementation is supplied from the start. Each lesson
traces and tests one boundary; experiments belong in a disposable copy rather
than silently changing the reference fixtures.

## Ten lessons → source → commands

**Every website lesson link below is awaiting publication.** The source links
work in this companion now. The [machine-readable lesson map](docs/lessons.json)
contains all forty chapter command runs and the explicit publication status.

| Part / planned website lesson | Code | First offline command |
|---|---|---|
| 1. [Build the Lab — AI-Core + Jev in Practice / Jev Lab — ตั้งแล็บก่อนวัดผล](https://anirach.com/blog/ai-core-jev-lab.html) | [src/questions.mjs](src/questions.mjs) · [src/cli.mjs](src/cli.mjs) | `node src/cli.mjs doctor` |
| 2. [Establish a Measurable Baseline — AI-Core + Jev in Practice / Baseline — วาง baseline ที่ตรวจได้](https://anirach.com/blog/ai-core-jev-baseline.html) | [src/contracts.mjs](src/contracts.mjs) · [test/contracts.test.mjs](test/contracts.test.mjs) | `node src/cli.mjs demo --mode baseline --ticket T-001` |
| 3. [Ask Typed Questions with Jev — AI-Core + Jev in Practice / Typed Questions — ถามให้เป็นชนิดข้อมูล](https://anirach.com/blog/ai-core-jev-questions.html) | [src/providers.mjs](src/providers.mjs) · [src/questions.mjs](src/questions.mjs) | `node src/cli.mjs request --ticket T-001` |
| 4. [Validate Every Response — AI-Core + Jev in Practice / Validate Responses — ตรวจคำตอบก่อนเชื่อ](https://anirach.com/blog/ai-core-jev-validation.html) | [src/contracts.mjs](src/contracts.mjs) · [test/contracts.test.mjs](test/contracts.test.mjs) | `node --test --test-reporter=spec test/contracts.test.mjs` |
| 5. [Abstain, Route, and Fall Back — AI-Core + Jev in Practice / Abstain & Route — ไม่มั่นใจให้หยุดได้](https://anirach.com/blog/ai-core-jev-routing.html) | [src/pipeline.mjs](src/pipeline.mjs) · [config/policy.json](config/policy.json) | `node src/cli.mjs demo --mode hybrid --ticket T-002` |
| 6. [Compare Without Test-Set Leakage — AI-Core + Jev in Practice / Fair Evaluation — แยกชุดวัดก่อนเทียบ](https://anirach.com/blog/ai-core-jev-evaluation.html) | [src/metrics.mjs](src/metrics.mjs) · [src/report.mjs](src/report.mjs) · [src/cli.mjs](src/cli.mjs) | `node --test --test-reporter=spec test/pipeline.test.mjs` |
| 7. [Guard Effects and Require Approval — AI-Core + Jev in Practice / Effect Guard — ตั้งด่านก่อนเกิดผลจริง](https://anirach.com/blog/ai-core-jev-guard.html) | [src/effects.mjs](src/effects.mjs) · [test/effects.test.mjs](test/effects.test.mjs) | `node src/cli.mjs actions --ticket T-001 --ledger out/chapter7-ledger.json` |
| 8. [Test Hostile Inputs and Failure Paths — AI-Core + Jev in Practice / Failure Tests — ลองทำให้พังก่อนปล่อย](https://anirach.com/blog/ai-core-jev-failures.html) | [src/pipeline.mjs](src/pipeline.mjs) · [test/pipeline.test.mjs](test/pipeline.test.mjs) · [test/network.test.mjs](test/network.test.mjs) | `node src/cli.mjs evaluate --split attack --save` |
| 9. [Measure Latency and Full Task Cost — AI-Core + Jev in Practice / Full Task Cost — วัดทั้งเวลาและต้นทุนงาน](https://anirach.com/blog/ai-core-jev-cost.html) | [src/metrics.mjs](src/metrics.mjs) · [config/prices.example.json](config/prices.example.json) | `node --test --test-reporter=spec test/metrics.test.mjs` |
| 10. [Freeze a Release and Run in Shadow Mode — AI-Core + Jev in Practice / Shadow Release — ตรึงรุ่นแล้วลองแบบเงา](https://anirach.com/blog/ai-core-jev-release.html) | [src/providers.mjs](src/providers.mjs) · [config/release.json](config/release.json) · [test/report.test.mjs](test/report.test.mjs) | `node src/cli.mjs doctor` |

## Repository structure

```text
src/
  questions.mjs   named Choice criteria, Noul, minimal request state
  contracts.mjs   ticket, answer and usage validation
  providers.mjs   canned fixtures; optional isolated live SDK adapter
  pipeline.mjs    baseline / Jev / hybrid, abstention, one fallback
  effects.mjs     deterministic guard, separate approval, serial ledger
  metrics.mjs     quality, coverage, latency scenarios, calibration, cost
  report.mjs      release/source identities, per-case traces, language slices
  cli.mjs         commands used in the lessons
config/
  policy.json    unvalidated teaching thresholds
  prices.example.json  dated Jev price and fictional cost assumptions
  release.json   model, SDK, question, policy and dataset identifiers
 data/           synthetic tickets + explicitly authored predictions
 test/           6 test files, 43 tests
 docs/lessons.json  bilingual chapter map; publication pending
 out/            generated local reports/ledger, ignored by Git
```

## Run without an SDK, credentials, network or paid calls

Use Node **22.18+** in this directory. The complete solution is supplied so each
chapter can be repeated independently. Default providers are hand-authored
fixtures; they do not call or emulate the intelligence of Jev.

```sh
node src/cli.mjs doctor
node --test --test-reporter=spec
node src/cli.mjs request --ticket T-001
node src/cli.mjs demo --mode baseline --ticket T-001
node src/cli.mjs demo --mode hybrid --ticket T-001
node src/cli.mjs evaluate --split validation --save
node src/cli.mjs sweep
node src/cli.mjs evaluate --split test --save
node src/cli.mjs evaluate --split attack --save
```

The fixture population has 40 synthetic tickets: 12 validation, 24 test, 4
attacks. These split names demonstrate plumbing and evaluation discipline. They
are **not** a statistically valid blind model study: the canned predictions were
authored alongside the tickets. Providers receive only ID, text and language;
gold labels are retained by the evaluator. The fixture provider uses ticket ID,
so changing text, question wording or option order does not change its answer.

Expected observations: T-001 proposes billing; T-002 takes a baseline fallback;
T-004 and T-006 need review; T-011 contains an intentionally confident wrong
fixture; T-040 has an invalid route and must be refused in Jev-only mode.
T-036 has unknown usage, so a complete cost cannot be reported for a run
containing that Jev attempt. See each report's evidence label.

## Simulated actions, separate approval, serial idempotency

```sh
node src/cli.mjs actions --ticket T-001 --ledger out/readme-ledger.json
node src/cli.mjs actions --ticket T-001 --approve --ledger out/readme-ledger.json
node src/cli.mjs actions --ticket T-001 --approve --ledger out/readme-ledger.json
```

With a fresh ledger these return `blocked`, `simulated`, `duplicate`. All effects
are local JSON entries. No help-desk service, customer messaging, refunds or
other external actions are implemented. `demo-reviewer` is not authentication.
The JSON ledger is serial and nontransactional; production requires authenticated
approvals, tamper-resistant audit, durable atomic writes and a database unique key.
Never infer a concurrency guarantee from this example.

## Read the reports honestly

- `rawRouteAccuracy`: correct queue labels among valid final route decisions.
- `coverage`: fraction with an automatic **proposal**, before human approval.
- `selectiveAccuracy`: correct automatic tasks that did not ignore a human request.
- `abstentionRate`, `fallbackRate`, `humanRequestMissRate`: reported separately.
- `successfulAutomatedTasks`: the narrow successful-task denominator in this lab.
  Review tasks remain unresolved. This is **not** completed customer-ticket resolution.
- `latency.p50/p95`: nearest-rank statistics of fictional per-attempt scenario
  milliseconds, summed for sequential fallback. They are not measured Jev latency.
- `harnessWallMs`: actual local evaluator runtime, not network inference time.
- ECE uses selected-option probability, **not** the Choice confidence statistic.
  Tiny synthetic bins cannot establish real-world calibration.
- Cost includes every recorded provider attempt, fallback, modeled infrastructure,
  review time and wrong-auto-task rework. Baseline prices, reviewer pay, review
  seconds, infrastructure and rework rates are **fictional assumptions**.
- Official Jev input price was USD 0.042 per million tokens, output free, when
  checked on **2026-10-23**. Recheck the official page before spending.
- Missing usage, hidden retry costs or zero successes produce an unknown total
  or undefined cost per successful task. Missing information is never a free call.
- Compare cost only after equal acceptable quality and coverage constraints pass.
  The fixtures intentionally do not prove that hybrid dominates the baseline.

Each saved evaluation retains `context` (run ID, timestamp, release/model/SDK,
question and dataset identifiers, Node version and exact source/data SHA-256
hashes), the policy and price snapshots, all per-ticket `cases` with final
outcomes and attempt traces, and `languageSlices` for Thai and English. Gold
labels in reports are evaluator annotations attached after inference; providers
never receive them. Small slices demonstrate reporting, not reliable subgroup
estimates. Early walkthroughs use only validation cases (including T-005's
wrong baseline and T-011's confident wrong Jev fixture). The public synthetic
test data is still teaching material, never claimed to be an untouched blind study.

## Optional live Jev call — not run or verified for this draft

The offline path needs **no installation**. If you choose to use your own eligible
provider account, first review the SDK and install the exact version server-side:

```sh
npm install --ignore-scripts @typesafe-ai/sdk@0.7.0
```

Review the resulting transitive lockfile. Set `TYPESAFE_API_KEY` privately in your
shell environment; do not paste it into website HTML, a screenshot or a commit.
No real keys are supplied. Then deliberately opt into **one synthetic ticket**:

```sh
node src/cli.mjs demo --ticket T-001 --live
```

This may incur charges on your account. No access/signup eligibility is claimed.
The adapter dynamically imports the SDK only in the explicit live branch and pins
`jev-1.13.0`. It uses `TypeSafeClient.systemOne`, `choice` and `noul`. Choice answers
have `choice`, `probabilities`, `confidence`; Noul has **only** `noul` plus its type,
with no separate confidence. Validate all output values before proposing anything.

The SDK can retry internally. We add no outer retry loop and do not pretend that
final-response token usage reveals every attempted request. `httpAttempts` stays
unknown and `costComplete` is false on live results. The live generative fallback
and bulk paid evaluation are deliberately not configured. API failures or invalid
responses become review results, not actions. No paid or authenticated call was
performed while authoring or testing this draft.

## Files

`src/contracts.mjs` runtime schemas; `questions.mjs` state and question definitions;
`providers.mjs` offline fixtures and isolated live adapter; `pipeline.mjs` routing;
`effects.mjs` approval and simulated ledger; `metrics.mjs` transparent accounting;
`cli.mjs` runnable commands; `report.mjs` per-case audit records and language slices. Tests cover contracts, routing, leakage, effects,
idempotency, accounting and explicit live opt-in. `config/release.json` records
release identifiers; `config/policy.json` has **unvalidated teaching thresholds**.

## Primary references (checked 2026-10-23)

- https://docs.typesafe.ai/introduction/coding-agents
- https://docs.typesafe.ai/sdk/javascript
- https://docs.typesafe.ai/sdk/javascript/changelog
- https://docs.typesafe.ai/primitives/choice
- https://docs.typesafe.ai/primitives/noul
- https://docs.typesafe.ai/confidence
- https://docs.typesafe.ai/models
- https://docs.typesafe.ai/model-jaggedness/jev-1.13

No claim of improved live accuracy, latency, calibration or operating cost is made.
The deliverable is a runnable harness and a procedure for testing those hypotheses.

## Benchmark procedure for real deployment decisions

1. Predeclare the same acceptance rule for baseline, Jev-only and hybrid. A correct
   automatic proposal must choose the right queue and preserve human requests.
   Reviews remain unresolved; do not quietly redefine success as valid JSON.
2. Freeze provider/model versions, questions, dataset, policy, prices and quality/
   coverage constraints before comparison. The route threshold 0.7 and human-no
   boundary 0.3 are **unvalidated teaching parameters**, not production advice.
3. Tune only on validation data, then freeze a candidate before test evaluation.
   Use independent, newly labeled held-out data for a real study. Public synthetic
   tickets and predictions authored together are not an untouched blind study.
4. Report raw and selective accuracy with coverage/abstention, human-request miss
   and fallback rates, plus Thai/English slices and uncertainty estimates. Better
   performance on a small retained subset does not establish equal service quality.
5. Measure end-to-end p50/p95 with fallback and retry time under comparable network,
   concurrency and warm/cold conditions. The lab's scenario latency is fictional;
   actual local `harnessWallMs` is not measured Jev inference latency.
6. Include all inference attempts/retries/fallback, infrastructure, review time and
   measured failure/rework in cost per successful task. Unknown usage/hidden SDK
   attempts or zero successes make totals unknown/undefined, never free.
7. Check calibration independently. Selected-option probabilities, not the Choice
   confidence statistic, feed ECE. Confidence 0.9 does not establish 90% accuracy;
   tiny synthetic bins do not establish production calibration.
8. Before any real effects, run a separately authorized shadow evaluation, review
   disagreements and language slices, and set rollout/rollback gates. This repo
   implements no production rollout and enables no bulk paid evaluation.

The fixture provider is indexed by ticket ID: changing text, question wording or
option order does not change its answer. Prompt, numeric, adversarial and irrelevant-
context robustness require a real model experiment; offline checks test mechanics.
Questions in one Jev request are independent; dependent decisions need separate calls.

## Environment-variable guidance for optional live use

The optional live section above may incur account charges. In bash or zsh, read
the key without echoing it or placing the value in shell history; type/paste your
key and press Enter after the first command:

```sh
# LIVE-ONLY setup, not an offline test; may incur charges.
read -rs TYPESAFE_API_KEY
export TYPESAFE_API_KEY
node src/cli.mjs demo --ticket T-001 --live
unset TYPESAFE_API_KEY
```

Never put real keys in a website, issue, screenshot or tracked file. `.env.example`
contains only a placeholder; this program does **not** automatically load dotenv
files. An environment variable alone never enables live calls: `--live` is required.
Errors or malformed results become review outcomes without effects. The SDK can
retry 429/529 internally; avoid an outer retry stack. Correct 401 authentication
and 422 schema problems before trying again. Inference retries and idempotent
execution of effects are separate concerns.

## Test commands and aliases

```sh
npm test
npm run demo
npm run bench
node --test test/contracts.test.mjs
node --test test/pipeline.test.mjs
node --test test/effects.test.mjs
node --test test/metrics.test.mjs
node --test test/report.test.mjs
node --test test/network.test.mjs
```

Aliases work without `npm install`. Tests cover invalid baseline JSON **and
out-of-set labels**, pinned Jev types/distributions/ranges, abstention and provider
failure, gold-label isolation, separate approval/serial idempotency, unknown cost
and zero successes, report provenance/per-case/language records and explicit live
opt-in before SDK import. Passing these tests is evidence about code behavior,
not model quality or complete production safety.

## Troubleshooting

| Symptom | What to inspect |
|---|---|
| Cannot find `src/cli.mjs` | Enter the repository root before running commands. |
| Old Node or runtime error | Check `node --version` and the executable your terminal selects. |
| Offline run asks for SDK | Remove accidental `--live`; SDK import belongs only in `liveJev`. |
| Unknown ticket ID | A synthetic ticket needs a matching authored prediction; the mock cannot invent one. |
| Unexpected review | Inspect reason, policy and every attempt rather than bypassing the guard. |
| Ledger says duplicate immediately | Choose a fresh ledger filename for a new experiment. |
| Cost is `null` | Retain unknown usage/attempts; do not replace them with zero. |
| Same answer after rewriting a question | Fixtures are canned. They cannot measure a changed question's effect. |
| Website lesson returns 404 | The new lessons await website publication; use the source links here now. |
| API auth/schema/rate/overload error | Check official docs and account configuration without printing keys or stacking retries. |

## Copyright and licensing

Copyright © 2026 Anirach Mingkhwan. All rights reserved. **No open-source license
or additional reuse license is granted here.** See [NOTICE.md](NOTICE.md).
The optional SDK is not vendored and retains its own license and service terms.
