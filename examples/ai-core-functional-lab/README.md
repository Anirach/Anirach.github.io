# AI-Core Functional Workflows — tutorial companion

A twelve-part bridge for programmers who already write ordinary functions,
validation and unit tests. Build one **fictional DeskLite CSV-export reply**
workflow with explicit input checks, policy, output checks and a separate quality
gate. Functional means typed inputs/outputs and composable functions, **not a
vendor product or an invented AI-Core SDK**.

**Companion repository:** [Anirach/ai-core-functional-tutorial](https://github.com/Anirach/ai-core-functional-tutorial).
The twelve bilingual lessons are at [Anirach.com](https://anirach.com/blog/#series-ai-core-functional).
This repository and the tutorial are designed to be used together: follow a lesson,
open its matching source, run its commands and tests, then try its exercise.
All model responses and generated drafts in the default lab are authored offline
fixtures. Public availability does not grant a reuse license; see NOTICE.md.

## เริ่มต้นภาษาไทย

แล็บนี้พาจากฟังก์ชันเดิมไปสู่ workflow ที่คืน accept, reject, revise หรือ
human_review ชัดเจน ใช้ข้อมูลผลิตภัณฑ์และ ticket สมมติเท่านั้น คำตัดสินแบบ Jev
และร่างข้อความเริ่มต้นเป็น mock ที่ผู้เขียนกำหนด ไม่ใช่ผลเรียกโมเดลจริง
ไม่ต้องติดตั้ง SDK ใช้ API key หรือเสียค่า inference สำหรับคำสั่งในบทเรียน
อ่านบทเรียนบน Anirach.com คู่กับ source, tests และแบบฝึกของแต่ละตอนใน GitHub repository นี้

## Roles and architecture

- **Ordinary code** checks exact shapes, sizes, IDs, authorization, arithmetic,
  budgets and continuation. A maintained template is often sufficient.
- **Codex** is the development assistant, not a runtime provider in this lab.
- **A generative provider** would draft text. Here it is a canned mock; no live
  generator is configured.
- **Jev** supplies discriminative typed decisions about supplied state. It does
  not generate the reply. This curriculum deliberately uses text-only Choice and
  Noul requests, without claiming those exhaust current Jev capabilities.

```text
untrusted input -> code validation -> code authorization -> semantic input guard
  -> draft generator -> output schema/action check -> evidence-grounding guard
  -> independent usefulness/clarity rubric -> accepted draft artifact
       revise -> bounded new draft or deterministic template -> recheck
       reject / human_review -> stop automatic continuation
held-out evaluation of a frozen system -> separate release gate
```

This applies the author's existing AI-Core assurance ideas: specify boundaries,
constrain effects and verify outcomes. A helper that calls Jev does not by itself
establish AI-core indispensability or autonomy. No send, refund, account edit,
customer message or deployment is implemented. `accept` never authorizes one.

## Prerequisites and offline setup

Use Node **22.18+** and a terminal; verified on macOS with Node **22.23.2**.
`.nvmrc` records that tested version without installing it. The program is ESM and
uses Node's built-in tests and filesystem APIs. No runtime npm dependencies or
SDK installation are required. Windows/Linux execution has not been verified.

Get the companion with Git (network access needed only for this download):

```bash
git clone https://github.com/Anirach/ai-core-functional-tutorial.git
cd ai-core-functional-tutorial
```

Or download [the complete website ZIP](https://anirach.com/downloads/ai-core-functional-lab.zip),
extract it and enter `ai-core-functional-lab`. Both contain the same reviewed code.
Source links in the tutorials open versioned GitHub file views; use an editor for
changes. The following commands run offline after download, without installing
packages, setting a key or paying for inference.
ดาวน์โหลดจาก GitHub หรือ ZIP แล้วเปิดโฟลเดอร์ใน editor คำสั่งต่อไปนี้รันออฟไลน์ได้
โดยไม่ต้องติดตั้ง SDK ตั้งค่า key หรือเรียก API ที่มีค่าใช้จ่าย

```sh
node --version
node src/cli.mjs doctor
node src/cli.mjs compare --case V001
node src/cli.mjs run --case V001
node --test --test-reporter=spec
```

Expected: doctor reports **28 cases**, `OFFLINE FIXTURES`, `sdkRequired: false`
and `paidCalls: 0`. V001 returns `accept`, four provider attempts and
`externalEffects: 0`. Its returned artifact is a draft, not a sent reply.
The complete reference solution is present from the beginning; trace one boundary
and edit a disposable copy for each exercise.

## Four states, four continuation rules

| State | Meaning | What may happen next |
|---|---|---|
| `accept` | This stage's property passed | Continue to the next required gate; a final result is only a draft artifact |
| `reject` | Hard constraint, scope or forbidden content failed | Stop; never score away the failure |
| `revise` | A candidate needs repair | Use a bounded new candidate or deterministic fallback, then recheck |
| `human_review` | Uncertainty, unavailable evidence/provider, cancellation or exhausted budget | Stop automated continuation for a person |

Schema acceptance is not grounding. Grounding acceptance is not usefulness.
Runtime acceptance is not release approval. Semantic guards are fallible defense
in depth, and repeated judgments from related models are not independent votes.

## Twelve lessons and exact companion files

Each tutorial link points to its public bilingual article on Anirach.com.
Source/test/exercise links resolve to real files in this repository. Use the
article and its matching code together; tests explain expected refusals too.

| Part / tutorial | Source | Tests | Exercise |
|---|---|---|---|
| 1. [From Functions to Guarded Workflows / จากฟังก์ชันสู่ระบบ](https://anirach.com/blog/ai-functions-architecture.html) | [src/generation.mjs](src/generation.mjs) | [test/pipeline.test.mjs](test/pipeline.test.mjs) | [Exercise1](exercises/01-architecture.md) |
| 2. [Define Contracts Before Models / เขียนสัญญาให้ตรวจได้](https://anirach.com/blog/ai-functions-contracts.html) | [src/contracts.mjs](src/contracts.mjs) | [test/contracts.test.mjs](test/contracts.test.mjs) | [Exercise2](exercises/02-contracts.md) |
| 3. [Check Inputs with Ordinary Code / ตรวจ input ด้วยโค้ด](https://anirach.com/blog/ai-functions-input-code.html) | [src/input.mjs](src/input.mjs) | [test/contracts.test.mjs](test/contracts.test.mjs) | [Exercise3](exercises/03-input-code.md) |
| 4. [Ask Jev About Input Meaning / ตรวจความหมาย input](https://anirach.com/blog/ai-functions-input-semantic.html) | [src/semantic.mjs](src/semantic.mjs) | [test/gates.test.mjs](test/gates.test.mjs) | [Exercise4](exercises/04-input-semantic.md) |
| 5. [Put Policy Before Confidence / วางสิทธิ์ก่อนความมั่นใจ](https://anirach.com/blog/ai-functions-policy.html) | [src/policy.mjs](src/policy.mjs) | [test/gates.test.mjs](test/gates.test.mjs) | [Exercise5](exercises/05-policy.md) |
| 6. [Read Typed Decisions and Uncertainty / อ่านคำตอบและความไม่แน่ใจ](https://anirach.com/blog/ai-functions-decisions.html) | [src/questions.mjs](src/questions.mjs) | [test/contracts.test.mjs](test/contracts.test.mjs) | [Exercise6](exercises/06-decisions.md) |
| 7. [Validate Every Output Shape / ตรวจรูปแบบ output](https://anirach.com/blog/ai-functions-output-code.html) | [src/output.mjs](src/output.mjs) | [test/gates.test.mjs](test/gates.test.mjs) | [Exercise7](exercises/07-output-code.md) |
| 8. [Ground Outputs in Trusted Facts / ตรวจเนื้อหากับหลักฐาน](https://anirach.com/blog/ai-functions-output-semantic.html) | [src/semantic.mjs](src/semantic.mjs) | [test/gates.test.mjs](test/gates.test.mjs) | [Exercise8](exercises/08-output-semantic.md) |
| 9. [Build a Separate Quality Gate / แยกด่านคุณภาพให้ชัด](https://anirach.com/blog/ai-functions-quality-gate.html) | [src/quality.mjs](src/quality.mjs) | [test/gates.test.mjs](test/gates.test.mjs) | [Exercise9](exercises/09-quality-gate.md) |
| 10. [Bound Retries, Repairs, and Fallback / จำกัดการลองใหม่และทางสำรอง](https://anirach.com/blog/ai-functions-budgets.html) | [src/budget.mjs](src/budget.mjs) | [test/budget.test.mjs](test/budget.test.mjs) | [Exercise10](exercises/10-budgets.md) |
| 11. [Evaluate Adversaries and Full Cost / ทดสอบการโจมตีและต้นทุนรวม](https://anirach.com/blog/ai-functions-evaluation.html) | [src/evaluation.mjs](src/evaluation.mjs) | [test/evaluation.test.mjs](test/evaluation.test.mjs) | [Exercise11](exercises/11-evaluation.md) |
| 12. [Compose the Pipeline and Release Gate / รวม pipeline แล้วตรึงรุ่น](https://anirach.com/blog/ai-functions-release.html) | [src/pipeline.mjs](src/pipeline.mjs) | [test/pipeline.test.mjs](test/pipeline.test.mjs) | [Exercise12](exercises/12-release.md) |

The complete per-part command list and publication status are in
[docs/lessons.json](docs/lessons.json). Every exercise file includes goals,
reference commands, expected output, a failure to preserve and a checkpoint.

## Repository structure

```text
src/contracts.mjs    closed gate states; strict pinned Choice/Noul contracts
src/input.mjs        shape, field, size, normalization and small known-pattern checks
src/policy.mjs       hard draft-only authorization and policy validation
src/questions.mjs    minimal state, explicit criteria, trusted evidence, stage questions
src/semantic.mjs     fallible input and grounding decisions; uncertainty paths
src/generation.mjs   ordinary deterministic template; mock generator is separate
src/output.mjs       output fields, language, citations and action scope
src/quality.mjs      separate answersUser / stepsUsable / plainLanguage rubric
src/budget.mjs       shared call cap, transport retries, timeout and cancellation
src/fixtures.mjs     explicitly authored provider responses keyed by case ID
src/pipeline.mjs     composition and terminal-state control
src/evaluation.mjs   full accounting, case traces, hashes, slices and release gate
src/live.mjs         optional text-only REST adapter; not enabled in CLI/tests
src/cli.mjs          runnable lesson commands
config/             policy, release pins, dated price / fictional cost assumptions
data/               28 synthetic cases, authored answers and maintained product facts
test/               contract, gate, pipeline, budget, evaluation and opt-in tests
support/            test fixture loader, not production code
exercises/          twelve matching hands-on exercises
docs/lessons.json    detailed lesson-to-command map
out/                generated local reports, ignored by Git
```

## Walk the validation cases

```sh
node src/cli.mjs input --case V002
node src/cli.mjs input --case V003
node src/cli.mjs policy --case V004
node src/cli.mjs judge --stage input --case V005
node src/cli.mjs output --case V006
node src/cli.mjs run --case V006
node src/cli.mjs judge --stage output --case V007
node src/cli.mjs run --case V007
node src/cli.mjs judge --stage quality --case V008
node src/cli.mjs run --case V008
node src/cli.mjs run --case V009
node src/cli.mjs run --case V001 --max-calls 3
```

V002 is a malformed numeric request; V003 matches a known injection pattern.
Both reject before inference. V004 asks for `send_reply` and is denied with zero
provider calls. V005 has valid but uncertain typed input judgment and reviews.
V006 has a malformed output language; its first gate revises and the full run
can accept a checked template fallback. V007 fabricates an emailing feature;
its semantic gate revises before fallback. V008's quality gate revises, but the
full run reviews after two drafts. V009 counts a transient retry separately;
the first attempt's unknown usage remains unknown. Three-call V001 stops before
quality because the aggregate budget is exhausted.

## Evaluation and complete cost

```sh
node src/cli.mjs tune --split validation
node src/cli.mjs evaluate --split heldout --save
node src/cli.mjs evaluate --split attack --save
node src/cli.mjs cost --case V001
node src/cli.mjs cost --case V010
node src/cli.mjs release --split heldout
```

There are12 validation,12 held-out and4 attack cases. Early walkthroughs use
validation examples; the CLI refuses held-out tuning. Freeze policy before
opening held-out evaluation. All cases, predictions and labels are authored
teaching fixtures; public split names are **not an untouched blind study**.
Real evaluation needs fresh independently labeled evidence, sufficient samples
and uncertainty estimates in relevant language/situation slices.

The intentionally flawed H010 fixture accepts an unsupported emailing claim
because the canned judges miss it. Held-out output therefore has12 accepts but
only11 reference-correct accepts, and its release gate **rejects** for a false
accept. This is an intended demonstration of fallible semantic guards, not a
measured error rate of Jev1.14. H011 lacks usage; total held-out cost stays null.
A green unit-test suite does not erase either finding.

The `release` CLI is also a shell/CI gate: exit **0** means its computed gate
accepted, exit **2** means reject/revise/human_review, and exit **1** means an
invocation or evaluator error. The advertised `release --split heldout` command
**must exit 2** for this deliberately flawed fixture set. Our command verifier
records that expected refusal as a successful check; `npm test` still exits 0
when its assertions pass. Do not suppress an unexpected release refusal in CI.
Before deciding, the gate validates required counts, ratios, latency and cost
fields, their numeric ranges, and consistency. Missing metrics cannot approve a
release. This validation does not authenticate a report or grant deployment rights.

คำสั่ง `release` คืน exit code **0** เมื่อ gate ยอมรับ, **2** เมื่อ reject/revise/
human_review และ **1** เมื่อคำสั่งหรือ evaluator เกิดข้อผิดพลาด ตัวอย่าง heldout
ชุดนี้ต้องคืน **2** ตามที่ตั้งใจ ส่วน test suite ยังควรคืน **0** เมื่อ assertions ผ่าน
metrics ที่ขาด ผิดชนิด ไม่เป็นจำนวนจำกัด หรือขัดกันต้องไม่เปิด release gate

Accounting retains every inference attempt, failed transport retry, generator
call and candidate revision. Deterministic fallback uses no model tokens but its
infrastructure is not assumed free: modeled per-task overhead is included along
with review time and false-accept rework. `perAcceptedUSD` and
`perCorrectAcceptedUSD` have explicitly different denominators. V001's complete
fictional scenario is approximately **USD0.00037024 per correct accepted draft**;
V010's value is null because usage is unknown. Empty denominators are undefined.
These are artifact-acceptance calculations, not resolved customer-ticket costs.

Official Jev unit pricing checked **2026-10-24** is USD0.042 per million input
tokens, output free. Recheck the source before future use. Generator prices,
usage, review time/pay, infrastructure, rework and per-attempt latency are
fictional assumptions. `latency.p50/p95` is nearest-rank scenario milliseconds;
`harnessWallMs` is actual local evaluator runtime. Neither measures live Jev
latency or proves savings. Incomplete timing is not silently excluded.

Each saved report retains release/model/question/facts/dataset IDs, exact hashes
of source/config/data, a run ID/time, every case/input/result/attempt, maintained
source facts, policy/prices and Thai/English summaries. Gold labels are retained
by the evaluator, not sent to the provider. Provider responses are keyed by ID,
so editing a prompt, fact or candidate does not measure changed model behavior.

## Budgets and optional live code

The teaching policy caps8provider attempts,2drafts and1eligible transport retry
per logical call, with100ms per-call timeout for fast mocks. All attempts share
the8-call cap; a semantic repair cannot reset it. Timeout and cancellation stop
new automated work. They do not guarantee a remote service stopped or did not
bill an in-flight request. This is not a production SLA or guaranteed money cap.

**No paid calls or credential setup were performed.** CLI `--live` is refused.
`src/live.mjs` is an optional, untested REST adapter with explicit `live: true`
required before environment-key access, one HTTP attempt, pinned `jev-1.14.0`,
and an abort signal. It refuses generation because Jev supplies decisions rather
than draft text. It is not wired into the demo/evaluation or any test network call.
Do not put a real key in website HTML, source, screenshots or reports. Wiring a
live provider later requires separately authorized account/configuration work,
reviewed retry-after/backoff, complete billing traces and validation of behavior.

The official JavaScript SDK0.7.0 is documented for Node22+, but is **not installed
or required** here. Its default `maxRetries: 2` means **three transport attempts**;
SDK retries must be reconciled with application budgets rather than wrapped in
an unaware outer retry loop. The SDK documents nullable usage and rejected
promises for invalid requests. This REST example adds no hidden SDK layer.

The curriculum uses only text Choice/Noul questions, no experimental images,
box primitive or long-context flags. Current documentation includes other
capabilities; no universal text-only or three-types-only claim is intended.
Noul is probability of yes, not severity, and has no separate confidence.
Choice/Score confidence is distribution-derived, not measured accuracy. If using
an ordered Score rubric in a future design, preserve its documented semantics;
this lab deliberately uses a binary criterion checklist instead.

## Tests

```sh
npm test
npm run demo
npm run evaluate
node --test --test-reporter=spec
node --test test/contracts.test.mjs
node --test test/gates.test.mjs
node --test test/pipeline.test.mjs
node --test test/budget.test.mjs
node --test test/evaluation.test.mjs
node --test test/live.test.mjs
node --test test/cli.test.mjs
```

Tests cover exact threshold boundaries, NaN/Infinity/range failures, missing IDs,
wrong discriminants/labels/model, malformed input/output/adapter replies,
injection and self-advocating text, denied actions, zero downstream/effect calls,
uncertainty, retries, timeout/cancellation, bounded revisions, hard-constraint
priority, evidence state, gold-label isolation, unknown cost, per-case provenance
and a distinct held-out release gate. No network inference or secret setup occurs.
Use test names and refusal traces rather than only the total count.

## Troubleshooting

| Symptom | Check |
|---|---|
| Cannot find `src/cli.mjs` | Enter the extracted companion root first. |
| Runtime version refusal | Check `node --version`; our chosen minimum is22.18. |
| A tutorial URL is unavailable | Check its address in docs/lessons.json and the website deployment status; the code can still be cloned or downloaded. |
| Unexpected revise/review | Read reasons and history; do not bypass a required stage. |
| Unexpected cost null | Inspect failed attempts/usage completeness. Unknown is never zero. |
| Edited prompt has identical answers | The provider is canned by case ID; it cannot measure a prompt improvement. |
| A quality check passes a forbidden action | Preserve the hardFailure path and output action guard; rubric values cannot authorize it. |
| A test times out | Make the injected provider observe abort or allow the race to settle; the100ms setting is for mocks. |
| Release rejects despite green tests | H010 intentionally exposes a false accept. Investigate the frozen evidence, do not delete the gate. |
| Looking for the companion | Use https://github.com/Anirach/ai-core-functional-tutorial and the lesson-to-file map above. |

## Source and version notes

See [docs/sources.md](docs/sources.md) for primary sources checked2026-10-24.
No cached cookbook answer is treated as evidence for this implementation.
The older Jev1.13 jaggedness page motivates failure-mode testing but is not
presented as an accuracy measurement of the pinned1.14 model. No model quality,
calibration, universal safety or operating-cost improvement is claimed.

Copyright ©2026 Anirach Mingkhwan. All rights reserved. No additional reuse
license is granted; see [NOTICE.md](NOTICE.md). No deployment, public repository
creation or publishing command is included.
