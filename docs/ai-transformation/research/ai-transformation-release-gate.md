# Research ledger — `ai-transformation-release-gate` (post #14/20)

**Post:** Five Evaluation Tracks, One Release Gate — Release on Evidence, Not on a Date
**Group:** Engineer · **Layer:** Spine / Learning loop · **Question:** Q6
**Book chapter:** Chapter 9 *Evaluate release observe and learn* (printed pp. 38–41 = PDF pp. 39–42) + **Artifact 7 Release gate** (printed pp. 79–80 = PDF pp. 80–81)
**Evidence snapshot of the book:** 5 September 2026 (Asia/Bangkok) — the book's own D.2 cutoff
**Access date for every source below:** **2026-09-05** (Asia/Bangkok)
**Researcher note:** Writers may not introduce a source, a number, or a Thai coinage that is not in this ledger.

---

## 0. Claim classes present in this post

| Class | Present? | Where |
|---|---|---|
| Material number (real-world, sourced) | **No** — none | The post carries no external quantitative finding. All numerals are either book-structural counts (§Number cards N1–N10) or illustrative-fictional (§Fictional values). |
| Dated legal / standard status | **Yes, one** | NIST June 2026 monitor-and-update item (§Dated statuses D1). |
| Study finding | **Yes, one** | The NIST mathematical result on guardrail robustness (via [7]). |
| Direct quotation | **Yes** | From the book only (Chapter 9 + Artifact 7). Quotable NIST lines listed in §Sources notes; use sparingly and attribute. |
| Framework attribution | **Yes, two** | NIST AI RMF 1.0 Govern/Map/Measure/Manage [3]; NIST AI 600-1 Generative AI Profile lifecycle testing & monitoring [4]. |
| Fictional-case value | **Yes, many** | CX-REFUND-01 / Luma Commerce Thailand — the whole of §Fictional values. |
| Author-supplied unpublished (r8 paper) | **Not used** | This post cites no 517-execution number. Do not introduce one. |
| Masterclass video | **Not used** | `n_IwUYevRZo` is **not** a source for this post. Spec says "No additions." Do not cite, do not paraphrase, do not timestamp. |

---

## 1. Sources

Only the three the spec names ([3], [4], [7]), plus the book itself as the primary text. **No additions.**

| # | Label | Title | URL | Publisher | Pub date | Accessed | Supports |
|---|---|---|---|---|---|---|---|
| **Book** | Synthesis | Mingkhwan, Anirach. *AI Transformation as an Organizational Core — Bilingual Companion Playbook*, Chapter 9 and Artifact 7 | — (source PDF supplied by the author; not a public URL) | Author | evidence cutoff 5 Sep 2026 | 2026-09-05 | The five evaluation tracks, the release ladder, the release dossier, the five operating principles, the readiness-room agenda, "Metrics that matter", "Failure patterns", the copy-ready gate and the CX-REFUND-01 illustrative result |
| **[3]** | Standard | *AI Risk Management Framework* (resource page) → the framework document *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*, NIST AI 100-1 | `https://www.nist.gov/itl/ai-risk-management-framework` · document: `https://doi.org/10.6028/NIST.AI.100-1` → `https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf` | National Institute of Standards and Technology (NIST), U.S. Dept. of Commerce | Framework released **26 January 2023**; document dated January 2023; page states the framework **is being revised** (see D2) | 2026-09-05 | MEASURE and MANAGE functions; "AI systems should be tested before their deployment and regularly while in operation"; the framework's voluntary, non-certifying character |
| **[4]** | Standard | *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*, NIST AI 600-1 | `https://doi.org/10.6028/NIST.AI.600-1` → `https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf` | NIST, U.S. Dept. of Commerce | **July 2024** | 2026-09-05 | Lifecycle testing and monitoring actions: adversarial testing at a regular cadence (MS-4.2-001), post-deployment monitoring plans (MANAGE 4.1 / MG-4.1-002), pre-deployment testing as one of the four GAI PWG considerations, tailoring to organizational risk tolerance |
| **[7]** | Study | *NIST Mathematical Proof Supports Transition to a Continuous-Monitor-and-Update Security Model for AI Systems* | `https://www.nist.gov/news-events/news/2026/06/nist-mathematical-proof-supports-transition-continuous-monitor-and-update` | NIST | **published 9 June 2026, updated 22 June 2026** | 2026-09-05 | "there is no finite set of guardrails that is universally robust against adversarial prompts"; the case for continuous red-teaming, continuous hardening, and operational resilience after release |

### Verification record

**[3] `https://www.nist.gov/itl/ai-risk-management-framework`** — HTTP **200** on `www.nist.gov` (GET and HEAD). Page `<title>`: `AI Risk Management Framework | NIST`. Verbatim from the page: *"The NIST AI Risk Management Framework (AI RMF) is intended for voluntary use and to improve the ability to incorporate trustworthiness considerations into the design, development, use, and evaluation of AI products, services, and systems."* and *"Released on January 26, 2023, the Framework was developed through a consensus-driven, open, transparent, and collaborative process…"*

> ⚠️ **The words GOVERN, MAP, MEASURE, MANAGE do not occur in the resource page's body text** — they appear only inside the page's Core graphic. The naming is verified instead from the framework document the page hosts, NIST AI 100-1 (downloaded 2026-09-05, 1,946,127 bytes, `nvlpubs.nist.gov`, dated January 2023):
> - *"the Core is composed of four functions: GOVERN, MAP, MEASURE, and MANAGE."* (§5)
> - MEASURE, verbatim: *"The MEASURE function employs quantitative, qualitative, or mixed-method tools, techniques, and methodologies to analyze, assess, benchmark, and monitor AI risk and related impacts. … **AI systems should be tested before their deployment and regularly while in operation.**"* ← the single strongest line for §3 `release-ladder` ("production is the final evaluation environment, not the end of evaluation").
> - MANAGE, verbatim: *"The MANAGE function entails allocating risk resources to mapped and measured risks on a regular basis and as defined by the GOVERN function. Risk treatment comprises plans to respond to, recover from, and communicate about incidents or events."* and *"It is incumbent on Framework users to continue to apply the MANAGE function to deployed AI systems as methods, contexts, risks, and needs or expectations from relevant AI actors evolve over time."*
> - Non-certifying character, verbatim: *"The Framework is intended to be voluntary, rights-preserving, non-sector-specific, and use-case agnostic…"* and *"Actions do not constitute a checklist, nor are they necessarily an ordered set of steps."*
>
> **Book's Boundary line for [3]:** *"it is a flexible framework, not certification, law, or proof that a particular system is trustworthy."*

**[4] `https://doi.org/10.6028/NIST.AI.600-1`** — DOI resolves 302 → `https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf`, **HTTP 200 on GET**, 1,174,643 bytes, retrieved and text-extracted 2026-09-05. *(Note: `nvlpubs.nist.gov` returns 404 to a bare HEAD request; a GET returns 200. Do not report this URL as dead on a HEAD-only check.)* Title page: "NIST Trustworthy and Responsible AI / NIST AI 600-1 / Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile", **July 2024**, U.S. Department of Commerce / NIST.

Verbatim passages that support "lifecycle testing and monitoring actions":
- Scope: *"The focus of the GAI PWG was limited to four primary considerations relevant to GAI: Governance, Content Provenance, **Pre-deployment Testing**, and Incident Disclosure…"*
- **MS-4.2-001:** *"Conduct adversarial testing at a regular cadence to map and measure GAI risks, including tests to address attempts to deceive or manipulate the application of provenance techniques or other misuses. Identify vulnerabilities and understand potential misuse scenarios and unintended outputs."*
- **MANAGE 4.1 (subcategory text):** *"Post-deployment AI system monitoring plans are implemented, including mechanisms for capturing and evaluating input from users and other relevant AI Actors, appeal and override, decommissioning, incident response, recovery, and change management."*
- **MG-4.1-002:** *"Establish, maintain, and evaluate effectiveness of organizational processes and procedures for post-deployment monitoring of GAI systems…"*
- **GV-1.2-002:** *"Establish policies to evaluate risk-relevant capabilities of GAI and robustness of safety measures, both prior to deployment and on an ongoing basis, through internal and external evaluations."*
- **MS-2.3-003** *(the single most on-point line in [4] for a release-gate post)*: *"Share results of pre-deployment testing with relevant GAI Actors, such as those with system release approval authority."* — NIST itself names a release-approval authority that receives test evidence. This is the strongest external anchor for §4 `dossier` and §5 `release-gate`.
- **MS-4.2-005:** *"Verify and document the incorporation of results of structured public feedback exercises into design, implementation, deployment approval (“go”/“no-go” decisions), monitoring, and decommission decisions."* — a "go/no-go" gate in NIST's own words.
- **MANAGE 2.4 (subcategory text):** *"Mechanisms are in place and applied, and responsibilities are assigned and understood, to supersede, disengage, or deactivate AI systems that demonstrate performance or outcomes inconsistent with intended use."* — the external anchor for the kill path in operating principle #4.
- **MG-2.4-004:** *"Establish and regularly review specific criteria that warrants the deactivation of GAI systems in accordance with set risk tolerances and appetites."* — anchors "stop thresholds" in the readiness-room agenda (§2.7 step 4).
- **MG-2.4-002:** *"Establish and maintain procedures for escalating GAI system incidents to the organizational risk management authority when specific criteria for deactivation or disengagement is met…"*
- Tailoring: *"Implementation of the suggested actions will vary depending on the type of risk, characteristics of GAI systems, stage of the GAI lifecycle, and relevant AI actors involved."* and *"Not every suggested action applies to every AI Actor…"*

> **Book's Boundary line for [4]:** *"organizations must select and tailor actions to their use case and risk tolerance."*

**[7] `https://www.nist.gov/news-events/news/2026/06/nist-mathematical-proof-supports-transition-continuous-monitor-and-update`** — HTTP **200** on `www.nist.gov`. **The live title differs from the book's citation.** Live title: **"NIST Mathematical Proof Supports Transition to a Continuous-Monitor-and-Update Security Model for AI Systems"**. Book cites it as "Mathematical Proof Supports Transition to Continuous Monitor-and-Update Approach." **Use the live title in the references block.** Published **9 June 2026**, marked updated **22 June 2026**. Author of the underlying work: **Apostol Vassilev**, senior scientist, NIST.

Verbatim from the page:
- *"there is no finite set of guardrails that is universally robust against adversarial prompts."*
- *"you likely can't patch an AI system like an LLM and then expect to be OK forever."*
- The proof extends to AI the logic of **Kurt Gödel's incompleteness theorems**; one implication is that there will always be a way to prompt an AI system to disregard its rules — it is a matter of finding it.
- The remedy described is three-part: continuous red-teaming for new adversarial prompts; continuous updates hardening guardrails against newly discovered exploits; operational resilience emphasising impact limitation and quick recovery.
- **The page specifies no update frequency or schedule.**

> **Book's Boundary line for [7]:** *"a mathematical result does not specify the correct cadence or controls for every operational context."* — This boundary must appear beside any use of [7]. It is confirmed true against the live page.

**Verified but NOT authorised for the references block:** the peer-reviewed article behind [7] — Vassilev, Apostol. *"Robust AI Security and Alignment: A Sisyphean Endeavor?"* IEEE Security & Privacy 24, no. 3, published **14 May 2026**, DOI `10.1109/MSEC.2026.3678214`; NIST CSRC record `https://csrc.nist.gov/pubs/journal/2026/05/robust-ai-security-and-alignment-a-sisyphean-endea/final` (HTTP 200 on `csrc.nist.gov`, checked 2026-09-05). Abstract verbatim: *"This article establishes information-theoretic limitations for robustness of artificial intelligence (AI) security and alignment. Knowing these limitations and preparing for their challenges is essential for responsible adoption of AI. Broader implications for cognitive reasoning limitations of AI systems are also proven."* The DOI itself resolves to `ieeexplore.ieee.org/document/11475847/` and returned **202** (bot challenge), so if this is ever added, cite the `csrc.nist.gov` record, not the DOI. **The spec says "No additions" — the writer must not add this without editor approval.**

---

## 2. Book extraction — verbatim (the writer's raw material)

Everything in this section is quoted from the book. It is not independently sourced and must never carry a `[3]`/`[4]`/`[7]` superscript.

### 2.1 Chapter argument (chapter epigraph, printed p. 38)

> "An AI release is a management decision about a complete sociotechnical system not a model demonstration or a software date."

### 2.2 Evaluation begins before development (printed p. 39)

> "The release question is whether the complete system, including model, data, retrieval, tools, permissions, interface, workflow, and human oversight, has enough evidence to operate inside an agreed boundary. Evaluation therefore begins before development. State the decision, affected people, baseline, unacceptable outcomes, and conditions that require stopping or escalation."

Thai mirror (printed p. 40):

> "คำถามก่อน Release คือระบบทั้งหมด ตั้งแต่โมเดล ข้อมูล Retrieval, Tool, Permission, Interface, Workflow และ Human Oversight มีหลักฐานพอที่จะทำงานในขอบเขตที่ตกลงหรือไม่ การประเมินจึงเริ่มก่อนพัฒนา ต้องระบุการตัดสินใจ ผู้ได้รับผล ค่าฐาน ผลลัพธ์ที่ยอมรับไม่ได้ และเงื่อนไขหยุดหรือส่งต่อ"

### 2.3 The release dossier (printed p. 39) — **10 items**

> "A release dossier should contain purpose, owners, versions, data lineage, known limitations, evaluation cases, residual risks, approvals, rollback, and monitoring. **Model benchmarks can inform this package but cannot substitute for testing in the operating context.** NIST AI RMF organizes risk work around Govern, Map, Measure, and Manage. Its Generative AI Profile emphasizes lifecycle testing and monitoring. **The book turns those principles into a release portfolio rather than claiming certification.**"

Thai mirror (printed p. 40):

> "Release Dossier ควรมี Purpose, Owner, Version, Data Lineage, Limitation, Evaluation Case, Residual Risk, Approval, Rollback และ Monitoring · Benchmark ของโมเดลช่วยให้ข้อมูล แต่แทนการทดสอบในงานจริงไม่ได้ · NIST AI RMF จัดงานความเสี่ยงเป็น Govern, Map, Measure และ Manage ส่วน Generative AI Profile เน้นการทดสอบและติดตามตลอดวงจร คู่มือนี้แปลงหลักการเป็น Release Portfolio ไม่ได้อ้างการรับรอง"

### 2.4 The five evaluation tracks (printed p. 39)

> "Build several evaluation tracks. **Fixed cases** provide reproducible regression evidence. **Hidden cases** reduce overfitting to the visible suite. **Adaptive cases** test how controls respond when attacks change after observing them. **State and fault cases** cover duplicates, timeouts, partial commits, stale data, and tool errors. **Live monitoring** observes production drift, complaints, overrides, security signals, and outcomes. Test routine tasks, boundary cases, rare severe scenarios, **Thai and other operating languages**, affected groups, and downstream tool behavior. Report false accepts and false rejects for semantic evaluators."

Thai mirror (printed p. 40, verbatim as printed):

> "สร้างการประเมินหลายเส้นทาง Fixed Case ให้หลักฐาน Regression ที่ทำซ้ำได้ Hidden Case ลดการปรับระบบให้เข้ากับข้อสอบที่เห็น Adaptive Case ทดสอบเมื่อผู้โจมตีปรับตาม Control State and Fault Case ครอบคลุม Request ซ้ำ Timeout, Partial Commit, Stale Data และ Tool Error Live Monitoring สังเกต Drift ข้อร้องเรียน Override สัญญาณ Security และ Outcome ต้องทดสอบงานปกติ กรณีขอบ เหตุการณ์รุนแรง ภาษาไทยและภาษาจริง กลุ่มผู้ได้รับผล และ Tool ปลายทาง พร้อมรายงาน False Accept และ False Reject ของ Semantic Evaluator"

> ⚠️ The printed Thai reads **"ภาษาไทยและภาษาจริง"** where the English reads "Thai and other operating languages". The Thai is elliptical (likely for "ภาษาที่ใช้จริง"). **Do not reproduce the elliptical form.** The TH track should render the sense the English carries — recommended: **"ภาษาไทยและภาษาอื่นที่ใช้งานจริง"** — and this is a rendering choice, not a quotation, so it must not sit inside quotation marks.

Figure 12 chip labels, verbatim from the drawn figure (printed p. 38): `FIXED / ชุดตรึง` · `HIDDEN / ชุดซ่อน` · `ADAPTIVE / ปรับตามระบบ` · `STATE FAULT / ความผิดสถานะ` · `LIVE / การใช้งานจริง`. Gate bar: `RELEASE GATE — Utility Security Effects Trace Operations Economics Recovery`. Outcome chips: `PROMOTE / ปล่อย` · `CANARY / ทดลองจำกัด` · `HOLD / ระงับ` · `REJECT / ปฏิเสธ`. Figure attribution line, verbatim: *"Figure 12 Evaluation tracks and release gate · Author synthesis from Mingkhwan 2026 and NIST guidance"*.

### 2.5 The release ladder (printed p. 39) — **6 rungs**

> "Release through a ladder of sandbox, offline evaluation, shadow mode, canary traffic, limited population, and wider deployment. **Higher consequence requires stronger evidence, smaller exposure, visible human control, and faster rollback.** Human review is meaningful only if the reviewer has time, competence, evidence, and authority to disagree. **Production is the final evaluation environment, not the end of evaluation.** Supplier model changes, new user behavior, or policy updates can invalidate previous evidence."

Thai mirror (printed p. 40):

> "Release แบบขั้นบันไดจาก Sandbox, Offline, Shadow, Canary, กลุ่มจำกัด และวงกว้าง ยิ่งผลกระทบสูงยิ่งต้องมีหลักฐานมาก เปิดรับน้อย Human Control ชัด และ Rollback เร็ว Human Review มีความหมายเมื่อผู้ตรวจมีเวลา ความสามารถ หลักฐาน และอำนาจปฏิเสธ Production คือสภาพประเมินสุดท้าย ไม่ใช่จุดจบ เพราะ Supplier, User Behavior หรือ Policy เปลี่ยนแล้ว Evidence เดิมอาจใช้ไม่ได้"

### 2.6 Five operating principles (printed p. 40 EN / p. 41 TH) — **quote exactly ONE in the 💡 blockquote, list the rest in prose; never renumber**

| # | English (verbatim) | Thai (verbatim) |
|---|---|---|
| 1 | **Evidence before exposure** — "Do not increase the affected population ahead of proof." | **มีหลักฐานก่อนเพิ่ม Exposure** — "ไม่เพิ่มผู้ได้รับผลล่วงหน้ากว่าการพิสูจน์" |
| 2 | **Evaluate the system in context** — "A model score is not workflow performance." | **ประเมินระบบในบริบท** — "Model Score ไม่ใช่ Workflow Performance" |
| 3 | **Match gates to impact and reversibility** — "Stronger consequence demands stronger evidence." | **ใช้ Gate ตามผลกระทบและการย้อนกลับ** — "Consequence สูงต้อง Evidence สูง" |
| 4 | **Make every release observable and reversible** — "A live system needs a service owner and kill path." | **ทุก Release ต้องสังเกตและย้อนกลับได้** — "ระบบจริงต้องมี Service Owner และ Kill Path" |
| 5 | **Treat near misses overrides and corrections as evidence** — "Do not suppress the signals that teach the system." | **เก็บ Near Miss Override และ Correction เป็นหลักฐาน** — "อย่ากดสัญญาณที่ช่วยสอนระบบ" |

Section labels: **หลักปฏิบัติห้าประการ** (EN "Five operating principles").

### 2.7 Working session — "Release readiness room" (printed p. 40 EN / p. 41 TH) — **6 steps, in order**

English, verbatim:
1. "Restate the decision, users, affected parties, and baseline."
2. "Identify routine, boundary, adversarial, and severe cases."
3. "Review results and evidence gaps."
4. "Select the release stage, population, oversight mode, and stop thresholds."
5. **"Rehearse detection, containment, rollback, notification, and remedy for one failure."**
6. "Record the decision, owner, monitoring cadence, and next review date."

Thai, verbatim (section label **เวิร์กช็อป Release readiness room**):

> "ทบทวน Decision, User, Affected Party และ Baseline ระบุกรณีปกติ ขอบ การโจมตี และรุนแรง ตรวจผลกับ Evidence Gap เลือก Release Stage, Population, Oversight และ Stop Threshold ซ้อม Detection, Containment, Rollback, Notification และ Remedy แล้วบันทึกมติ Owner, Monitoring Cadence และวันทบทวน"

### 2.8 "Metrics that matter" (printed p. 40 EN / p. 41 TH) — section label **ตัวชี้วัดสำคัญ**

English, verbatim, in order:

> "Track quality-adjusted task success, critical-error rate, supported claims, security escapes, subgroup disparity, override and reversal, feedback latency, drift, cost per successful outcome, time to detect contain and recover, near-miss reporting, recurrence, and releases with a tested rollback."

Thai, verbatim:

> "ติดตาม Quality-adjusted Task Success, Critical Error, Supported Claim, Security Escape, Subgroup Disparity, Override, Reversal, Feedback Latency, Drift, Cost per Successful Outcome, Time to Detect Contain and Recover, Near-miss Reporting, Recurrence และ Release ที่ทดสอบ Rollback"

> ⚠️ **The two lists do not have the same item count.** English joins "override and reversal" as one comma-group (13 groups); Thai separates "Override, Reversal" (14 items). **Never state a count of metrics in either track.** Render the list; do not number it. The metrics table must carry the Scorecard column per series convention.

### 2.9 "Failure patterns" (printed p. 40 EN / p. 41 TH) — section label **รูปแบบความล้มเหลว** — **9 items in the book**

English, verbatim, in order:

> "One average score, irrelevant benchmarks, testing only easy English cases, releasing to everyone, treating vendor testing as sufficient, no versioned evidence, ceremonial approval, suppressed near misses, and closing an incident after service restoration without verifying corrective action."

Thai, verbatim:

> "ใช้คะแนนเฉลี่ยเดียว Benchmark ไม่เหมือน Production ทดสอบเฉพาะภาษาอังกฤษง่าย เปิดใช้ทุกคน เชื่อ Vendor Test ไม่มี Evidence แบบ Versioned มี Approval เชิงพิธีกรรม กด Near Miss และปิด Incident เมื่อระบบกลับมาโดยยังไม่ตรวจ Corrective Action"

> ⚠️ **The spec lists 7 of the book's 9.** It omits "suppressed near misses" and "closing an incident after service restoration without verifying corrective action" — both are held for post #15. Using only 7 is editorially fine; **saying "the book lists seven failure patterns" is false.** Do not state a count.

### 2.10 Artifact 7 Release gate (printed p. 79 EN / p. 80 TH)

**Purpose / Use when / Accountable owner**, verbatim EN:

> "**Purpose** Make promotion a recorded decision against predeclared utility, risk, cost and operability thresholds for one manifest. **Use when** moving from experiment to production, increasing exposure or authority, or changing any manifest component. **Accountable owner** Release authority decides; property owners attest evidence; independent challenge records dissent or exceptions."

Thai, verbatim (labels **วัตถุประสงค์ / ใช้เมื่อ / เจ้าของหลัก**):

> "**วัตถุประสงค์** ทำให้ Promotion เป็นคำตัดสินที่บันทึกได้ตาม Threshold ด้าน Utility, Risk, Cost และ Operability ของ Manifest หนึ่งรุ่น **ใช้เมื่อ** ขยับจากทดลองสู่ Production เพิ่ม Exposure/Authority หรือเปลี่ยน Manifest **เจ้าของหลัก** Release Authority ตัดสิน Property Owner รับรองหลักฐาน และ Independent Challenge บันทึกข้อคัดค้าน"

**Copy-ready gate — the exact 8 rows.** Columns EN: `Gate` / `Predeclared threshold` / `Result, evidence and sign-off` / `Fail action`. Columns TH: `Gate` / `Threshold ที่ประกาศล่วงหน้า` / `ผล หลักฐาน และลายเซ็น` / `เมื่อไม่ผ่าน`.

| Row | Gate (EN, verbatim) | Gate (TH, verbatim) | Pre-filled cells in the book |
|---|---|---|---|
| 1 | Scope, classification, contract, impact | Scope, Classification, Contract, Impact | — |
| 2 | Structural path, schema, authorization, duplicate, trace | Structural Path, Schema, Authorization, Duplicate, Trace | Fail action = **Block** |
| 3 | **Golden/hidden utility by language, case and severity** | **Golden/Hidden Utility แยกภาษา กรณี ความรุนแรง** | — |
| 4 | Faithfulness, relevance, privacy and calibrated error | Faithfulness, Relevance, Privacy และ Error Calibration | — |
| 5 | Fixed and held-out adaptive attacks with benign utility | Fixed/Held-out Adaptive Attack พร้อม Benign Utility | — |
| 6 | Fault, rollback, recovery and reconstruction | Fault, Rollback, Recovery, Reconstruction | — |
| 7 | Latency, cost, reviewer capacity, accessibility and support | Latency, Cost, Capacity, Accessibility, Support | — |
| 8 | **Decision** | **คำตัดสิน** | Threshold = "Exposure cap, next review, rollback ID" / "Exposure Cap, Review, Rollback ID"; Result = "Release authority" / "Release Authority" |

The three rules below the table, verbatim EN:

> "Never average away a failed structural invariant or severe slice. A clean fixed suite does not establish adaptive robustness. Exceptions must name residual risk, approver, expiry and compensating control."

Thai, verbatim:

> "ห้ามใช้ค่าเฉลี่ยกลบ Structural Failure หรือกลุ่มรุนแรง ชุด Fixed ที่ผ่านไม่ได้พิสูจน์ Adaptive Robustness และ Exception ต้องระบุ Residual Risk ผู้อนุมัติ วันหมดอายุ และ Compensating Control"

> ⚠️ **This is the book's line, not NIST's.** The `.alert danger` must attribute it to the playbook, never to [3]/[4]/[7].

**Completed CX-REFUND-01 (illustrative) — 5 rows.** Columns EN `Gate` / `Illustrative result and decision`; TH `Gate` / `ผลและคำตัดสินสมมติ`. Full verbatim text is reproduced in §Fictional values below, because every value in it is fictional.

### 2.11 The CX-REFUND-01 framing sentence (printed p. 77) — **must be quoted or paraphrased on first mention**

> "All examples use CX-REFUND-01, a fictional Luma Commerce Thailand assistant. It answers bilingual refund questions and may propose `issue_refund`. An external guard may execute one eligible refund no greater than THB 2,000 after confirmation; all other financial actions go to a person. **Values are illustrative, not universal thresholds.**"

---

## 3. Number cards

There is **no material (real-world, sourced) number in this post.** Every numeral is either a *book-structural count* (N1–N10, verifiable in the book, carrying no external denominator) or an *illustrative-fictional value* (§4). Cards are still required — no card, no number.

> **Standing rule for N1–N10:** these are counts of items in an author's framework. They take **no** `[N]` superscript and **no** denominator/comparison clause, because they are not measurements. Attribute to the playbook. Do not write "studies show" or any comparative framing around them.

### N1 — Five evaluation tracks
- **Value / unit:** 5 · evaluation tracks
- **Denominator / population:** items enumerated in Chapter 9's "Build several evaluation tracks" paragraph and drawn as 5 chips in Figure 12
- **Comparison:** none; not a benchmark
- **Task / setting:** designing an evaluation suite for one release manifest
- **Source:** the playbook, Ch. 9 (printed p. 39) + Figure 12 (printed p. 38)
- **Boundary (book):** "Author synthesis from Mingkhwan 2026 and NIST guidance" — a design, offered as testable, not settled fact (D.1 "Author synthesis")
- **TH sentence:** "หนังสือแยกการประเมินออกเป็นห้าเส้นทาง — Fixed, Hidden, Adaptive, State and fault และ Live monitoring — ไม่ใช่คะแนนเดียวจากชุดทดสอบเดียว"
- **EN sentence:** "The playbook splits evaluation into five tracks — Fixed, Hidden, Adaptive, State and fault, and Live monitoring — rather than one score from one suite."

### N2 — Five operating principles
- **Value / unit:** 5 · principles · **numbered 1–5, never renumbered**
- **Denominator:** the chapter's own numbered list (printed p. 40 EN / p. 41 TH)
- **Comparison:** none
- **Task / setting:** Chapter 9's closing rules for release decisions
- **Source:** the playbook, Ch. 9
- **Boundary:** author synthesis; offered as a testable design
- **TH sentence:** "บทที่ 9 ปิดท้ายด้วยหลักปฏิบัติห้าประการ และผมขอหยิบข้อที่ … มาเป็นแกนของตอนนี้"
- **EN sentence:** "Chapter 9 closes with five operating principles; the one I want to build this post around is #…"

### N3 — Eight rows in the copy-ready release gate
- **Value / unit:** 8 · rows = **7 gate rows + 1 Decision row**
- **Denominator:** Artifact 7's copy-ready gate table (printed p. 79 EN / p. 80 TH)
- **Comparison:** none
- **Task / setting:** one release manifest, one recorded promotion decision
- **Source:** the playbook, Artifact 7
- **Boundary:** a worksheet, not a conformity checklist; "Exceptions must name residual risk, approver, expiry and compensating control"
- **TH sentence:** "Artifact 7 คือตารางแปดแถว — เจ็ดแถวเป็นด่านตรวจ อีกหนึ่งแถวคือ Decision ที่บันทึก exposure cap, วันทบทวนถัดไป และ rollback ID"
- **EN sentence:** "Artifact 7 is an eight-row table: seven gate rows, then a Decision row that records the exposure cap, the next review and the rollback ID."

> ⚠️ **Spec drift, resolved here.** The spec describes "eight gate rows (Utility, Security, Effects, Trace, Operations, Economics, Recovery + Thai/language slice) + Decision row" — that would be 9. It is not what the book says. The seven words *Utility Security Effects Trace Operations Economics Recovery* are the **Figure 12 gate-bar dimensions** (N4); the **Artifact 7 row labels are different wording** (see §2.10 table); and the language slice is **inside row 3** ("Golden/hidden utility **by language**, case and severity"), not a separate row. **Build the table from §2.10's verbatim rows.** If the writer wants the Figure-12 vocabulary as a mapping column, label it as such.

### N4 — Seven gate dimensions on the Figure 12 bar
- **Value / unit:** 7 · named dimensions
- **Denominator:** the dark RELEASE GATE bar in Figure 12, verbatim: "Utility Security Effects Trace Operations Economics Recovery"
- **Comparison:** none
- **Task / setting:** the figure's summary of what the gate weighs
- **Source:** the playbook, Figure 12 (printed p. 38)
- **Boundary:** figure attribution is "Author synthesis from Mingkhwan 2026 and NIST guidance"
- **TH sentence:** "แถบด่านในรูปที่ 12 อ่านออกมาเป็นเจ็ดคำ — Utility, Security, Effects, Trace, Operations, Economics, Recovery"
- **EN sentence:** "The gate bar in Figure 12 reads as seven words — Utility, Security, Effects, Trace, Operations, Economics, Recovery."

### N5 — Six rungs on the release ladder
- **Value / unit:** 6 · stages
- **Denominator:** "sandbox, offline evaluation, shadow mode, canary traffic, limited population, and wider deployment"
- **Comparison:** none
- **Task / setting:** staged exposure of one release
- **Source:** the playbook, Ch. 9 (printed p. 39)
- **Boundary:** author synthesis
- **TH sentence:** "บันไดการปล่อยมีหกขั้น — sandbox, offline, shadow mode, canary, กลุ่มจำกัด แล้วจึงวงกว้าง"
- **EN sentence:** "The release ladder has six rungs — sandbox, offline evaluation, shadow mode, canary traffic, limited population, then wider deployment."

### N6 — Ten items in the release dossier
- **Value / unit:** 10 · items
- **Denominator:** "purpose, owners, versions, data lineage, known limitations, evaluation cases, residual risks, approvals, rollback, and monitoring"
- **Comparison:** none
- **Task / setting:** the evidence package assembled before a gate meeting
- **Source:** the playbook, Ch. 9 (printed p. 39)
- **Boundary:** "Model benchmarks can inform this package but cannot substitute for testing in the operating context."
- **TH sentence:** "Release dossier ที่หนังสือกำหนดมีสิบรายการ ตั้งแต่ purpose และ owner ไปจนถึง rollback และ monitoring"
- **EN sentence:** "The dossier the playbook asks for has ten items, from purpose and owners through to rollback and monitoring."

### N7 — Six steps in the readiness-room agenda
- **Value / unit:** 6 · agenda steps, in order
- **Denominator:** the six sentences of "Working session Release readiness room" (§2.7)
- **Comparison:** none
- **Task / setting:** one working session before a release decision
- **Source:** the playbook, Ch. 9 (printed p. 40)
- **Boundary:** author synthesis; a facilitation agenda, not a control
- **TH sentence:** "ห้องซ้อมความพร้อมก่อนปล่อยมีวาระหกข้อ และข้อที่ห้าคือข้อที่คนข้ามบ่อยที่สุด — ซ้อม detection, containment, rollback, notification และ remedy กับความล้มเหลวหนึ่งกรณี"
- **EN sentence:** "The readiness room runs a six-item agenda, and the fifth is the one teams skip — rehearse detection, containment, rollback, notification and remedy for one failure."

### N8 — Four release-gate outcomes
- **Value / unit:** 4 · outcomes
- **Denominator:** the four outcome chips in Figure 12
- **Comparison:** none
- **Task / setting:** the recorded decision at the gate
- **Source:** the playbook, Figure 12 (printed p. 38)
- **Boundary:** author synthesis
- **TH sentence:** "ด่านเดียวให้ผลได้สี่แบบ — Promote (ปล่อย), Canary (ทดลองจำกัด), Hold (ระงับ) และ Reject (ปฏิเสธ)"
- **EN sentence:** "One gate, four outcomes — Promote, Canary, Hold, Reject."

### N9 — Nine failure patterns in the book (7 used in this post)
- **Value / unit:** 9 in the book · the post renders 7 and defers 2 to #15
- **Denominator:** the "Failure patterns" paragraph (§2.9)
- **Comparison:** none
- **Task / setting:** anti-patterns at the release gate
- **Source:** the playbook, Ch. 9 (printed p. 40)
- **Boundary:** author synthesis
- **Rule:** **do not state a count in the post.** Render the list.

### N10 — "Metrics that matter" — **count deliberately unstated**
- **Value / unit:** 13 comma-groups in EN / 14 items in TH — **the two tracks disagree**
- **Denominator:** §2.8
- **Rule:** **never state a number.** Render the list as a `.table-wrapper` metrics table with the Scorecard column. Do not "fix" the mismatch by renumbering the Thai; keep the Thai items as printed and simply do not count them.

---

## 4. Fictional values — ALL flagged illustrative-fictional

The case is **CX-REFUND-01**, a **fictional Luma Commerce Thailand** refund assistant. Flag on first mention: `(กรณีสมมติจากหนังสือ)` / `(a fictional case from the playbook)`. The book's own disclaimer — "Values are illustrative, not universal thresholds" — must be reproduced beside the completed gate. **None of these numbers may appear in the metrics table as a target, a threshold, or a benchmark.**

### 4.1 Completed CX-REFUND-01 gate (Artifact 7, printed p. 79 EN / p. 80 TH) — verbatim

| Gate | Illustrative result and decision (EN, verbatim) | ผลและคำตัดสินสมมติ (TH, verbatim) |
|---|---|---|
| Structural | "All mediated path, schema, prohibited-effect, duplicate, fail-closed and terminal-trace tests pass; required zero-failure rule met" | "Path, Schema, Prohibited Effect, Duplicate, Fail-closed และ Terminal Trace ผ่านทั้งหมดตามกฎ Zero Failure" |
| Utility | "**94.6%** weighted success; all priority slices at least **89.1%**, above contracted floors; bilingual reviewer agreement reported" | "Weighted Success **94.6%** และกลุ่มสำคัญต่ำสุด **89.1%** สูงกว่าเกณฑ์ พร้อมรายงาน Reviewer Agreement สองภาษา" |
| Semantic/security | "Support **96.8%**; estimated false accepts **1.7%** on named calibration set; no prohibited effects in fixed, hidden or adaptive suites; adaptive text escapes remain visible" | "Support **96.8%**, False Accept ประเมิน **1.7%** บนชุดที่ระบุ และไม่มี Prohibited Effect ใน Fixed/Hidden/Adaptive Suite แต่ยังเปิดเผย Text Escape" |
| Operations | "**p95 3.4 seconds**, cost within case budget, rollback drill **11 minutes**, reviewer queue below capacity; privacy and accessibility checks signed" | "p95 **3.4 วินาที** ต้นทุนผ่าน Budget, Rollback Drill **11 นาที**, Queue ไม่เกิน Capacity และ Privacy/Accessibility ลงนาม" |
| Decision | "Approve manifest `rc4` for **5%** exposure, then **25%** only after **48-hour** review; stop on prohibited effect, severe policy escape, missing trace, or reviewer overload; rollback `prod2`; review owner **N. Kanya**" | "อนุมัติ `rc4` ที่ **5%** แล้วจึง **25%** หลัง Review **48 ชั่วโมง** Stop เมื่อมี Prohibited Effect, Severe Escape, Trace หาย หรือ Reviewer Overload; Rollback `prod2`; N. Kanya เป็นเจ้าของ Review" |

### 4.2 Flag list (every fictional token this post may touch)

| Token | Where in the book | Status |
|---|---|---|
| **CX-REFUND-01** | Artifacts framing, printed p. 77 | illustrative-fictional — flag on first mention |
| **Luma Commerce Thailand** | printed p. 77 | illustrative-fictional |
| **94.6%** weighted success | Artifact 7 completed, p. 79 | illustrative-fictional |
| **89.1%** lowest priority slice | Artifact 7 completed, p. 79 | illustrative-fictional |
| **96.8%** support | Artifact 7 completed, p. 79 | illustrative-fictional |
| **1.7%** estimated false accepts | Artifact 7 completed, p. 79 | illustrative-fictional |
| **p95 3.4 seconds** | Artifact 7 completed, p. 79 | illustrative-fictional |
| **11 minutes** rollback drill | Artifact 7 completed, p. 79 | illustrative-fictional |
| **5% → 25% after 48-hour review** | Artifact 7 completed, p. 79 | illustrative-fictional — **these are the only rollout percentages the series permits** (series convention: "no invented rollout percentages beyond 25% and 5%") |
| **`rc4`, `prod2`, N. Kanya** | Artifact 7 completed, p. 79 | illustrative-fictional identifiers/name |
| **THB 2,000** external guard cap | printed p. 77 | illustrative-fictional; book's own line "Values are illustrative, not universal thresholds" |
| **THB 1,850** | Artifact 6 trace tail, printed p. 79 | illustrative-fictional — belongs to post #13's trace; use only if the writer needs the manifest continuity, and flag it |
| **THB 2,400 / 60-day statement / day 45 / `CXGS-241` / `rc5` / corpus `2026-09-01`** | Artifact 8, printed p. 82 | illustrative-fictional — **these belong to post #15.** Do not spend them here beyond the next-post hook, and never as numbers. |
| **Aurora Assurance · 80,000 letters** | printed p. 22 | illustrative-fictional — **not in this post's page range; do not use.** |
| **Kiri Foods · HarborLight Retail · LannaBuild Engineering** | pp. 24, 27, 31 | illustrative-fictional — **not in this post's page range; do not use.** |
| **THB 2,500 · 41.3% · 240 cases · 18 min · 46 h** | — | **Not found anywhere in pp. 38–41 or 79–80.** Do not use in this post. |

---

## 5. Dated statuses

Each becomes exactly **one dated sentence** in the post.

### D1 — NIST June 2026 monitor-and-update item **(applies)**

**Dated sentence, TH:**
> "เมื่อ 9 มิถุนายน 2026 (ปรับปรุง 22 มิถุนายน 2026) NIST เผยแพร่บทสรุปงานวิจัยที่พิสูจน์ทางคณิตศาสตร์ว่า ไม่มีชุด guardrail จำกัดชุดใดที่ทนทานต่อ adversarial prompt ได้ในทุกกรณี จึงสนับสนุนแนวทาง monitor-and-update ต่อเนื่องแทนการตรวจครั้งเดียวจบ — แต่ผลทางคณิตศาสตร์ไม่ได้ระบุ cadence หรือ control ที่ถูกต้องสำหรับทุกบริบทการใช้งาน"

**Dated sentence, EN:**
> "On 9 June 2026 (updated 22 June 2026) NIST published a research summary of a mathematical proof that no finite set of guardrails is universally robust against adversarial prompts, supporting a continuous monitor-and-update posture rather than a one-time check — while the result itself specifies no cadence or set of controls for any particular operating context."

**Verification, 2026-09-05:** page live, HTTP 200 on `www.nist.gov`; dates as shown on the page; author Apostol Vassilev. The live title is **"NIST Mathematical Proof Supports Transition to a Continuous-Monitor-and-Update Security Model for AI Systems"** — use that, not the book's shortened form. The boundary clause is confirmed: the page names no frequency or schedule.

### D2 — NIST AI RMF 1.0 is itself under revision **(applies — one dated sentence, or a footnote on [3])**

Found on the live resource page on the access date; **not in the book**, whose D.2 snapshot predates nothing here but simply does not mention it. It matters because the post leans on [3] as a stable organizing frame.

Verbatim from `https://www.nist.gov/itl/ai-risk-management-framework`, read 2026-09-05:
> "The AI RMF 1.0 is being revised as part of the White House AI Action Plan."

and, on the same page:
> "On April 7, 2026, NIST released a concept note for an AI RMF Profile on Trustworthy AI in Critical Infrastructure. The profile will guide critical infrastructure operators towards specific risk management practices to consider when engaging AI-enabled capabilities."

**Dated sentence, TH:**
> "ณ วันที่ 5 กันยายน 2026 หน้าเว็บทางการของ NIST ระบุว่า AI RMF 1.0 (เผยแพร่ 26 มกราคม 2023) กำลังอยู่ระหว่างการปรับปรุงภายใต้ White House AI Action Plan ดังนั้นสิ่งที่ยืมมาใช้ในตอนนี้คือโครงคิด Govern, Map, Measure, Manage ไม่ใช่ข้อความฉบับใดฉบับหนึ่งที่ตรึงถาวร"

**Dated sentence, EN:**
> "As of 5 September 2026 NIST's own page states that AI RMF 1.0 — released 26 January 2023 — is being revised under the White House AI Action Plan, so what this post borrows is the Govern/Map/Measure/Manage shape of the work, not a frozen text."

**Rule:** if the writer cites [3] as a framework, this caveat is optional but recommended. If the writer cites [3] as a *current requirement* or quotes a clause as settled, the caveat is **mandatory**. Never write "the latest AI RMF".

### D3–D9 — **not applicable to this post**

| Re-check | Applies? | Why |
|---|---|---|
| Thailand's dedicated AI law (ETDA `law_ai` + ร่างพระราชบัญญัติ … ปัญญาประดิษฐ์) | **No** | Post #14 makes no Thai legal claim. The spec's research targets are `[3] [4] [7]` and "No additions." **If a writer wants a Thai-law sentence, it must be researched afresh — this ledger does not carry one.** |
| EU AI Act application dates / 2026 amendment | **No** | No EU claim in the spec. |
| Stanford AI Index 2026 figures | **No** | No adoption/economy number in the spec. |
| IEA 2026 figures | **No** | No energy number in the spec. |
| ISO/IEC 42005:2025 status | **No** | Impact assessment is post #12/#16 material, not here. |
| ETDA guideline versions | **No** | Not cited in the spec. |
| PDPA sub-regulations | **No** | Not cited in the spec. |

### The r8 paper and the masterclass — **neither is used here**

- **Mingkhwan, Anirach. *Engineering AI-Core Systems: A Reference Architecture and Assurance Contract for Software 3.0*, revision 8 (September 2026)** — author-supplied, unpublished, **no public URL; never link it.** This post cites **no** 517-execution number, so its boundary sentence ("the specimen demonstrates mechanisms under declared tests; it is not a production prevalence estimate or universal benchmark") is not needed. If any writer reintroduces a 517 figure, that boundary sentence must accompany it verbatim.
- **The Foundation masterclass, video id `n_IwUYevRZo`** — **not a source for this post.** The id was nonetheless checked on 2026-09-05: `https://www.youtube.com/watch?v=n_IwUYevRZo` resolves and carries the title the book cites, "AI Transformation: จากการใช้ AI สู่องค์กรที่เรียนรู้เร็วที่สุด | The Masterclass EP01" (book's own method note: The Foundation, 28 August 2026, running time 52 minutes 15 seconds). The spec authorises **no additions**, so: do not quote, paraphrase, timestamp or link it here. No timestamp is cited by this post, so none was verified.

---

## 6. Glossary check

Canonical Appendix C Thai renderings, verbatim on first mention, English inline afterwards.

| Coinage (EN) | Canonical Thai (use verbatim on first mention) | Notes for this post |
|---|---|---|
| Release gate | **ด่านอนุมัติการนำระบบออกใช้** | The post's spine term. After first mention, "release gate" inline is fine. Never shorten to "ด่านปล่อย". |
| Evaluation | **การประเมินระบบ** | Not plain "การประเมิน" on first mention — the "ระบบ" is the argument. |
| Adaptive evaluation | **การประเมินแบบปรับตัว** | Track 3. |
| Consequence | **ระดับผลกระทบ** | Used by principle #3 ("Match gates to impact and reversibility"). |
| Observability | **ความสามารถในการสังเกตระบบ** | Principle #4. |
| Fail-safe state | **ภาวะปลอดภัยเมื่อระบบล้มเหลว** | If the writer reaches for the kill-path idea. |
| Structural guarantee | **การรับประกันเชิงโครงสร้าง** | Needed for the `.alert danger` — a *structural invariant* that fails must not be averaged away. |
| Semantic estimate | **ค่าประเมินเชิงความหมาย** | Pairs with the above; the Semantic/security gate row. **Do not conflate the two** (flagged in A.3 as a drift risk). |
| Reconstructable trace | **ร่องรอยที่สร้างเหตุการณ์ย้อนกลับได้** | Gate rows 2 and 6. |
| Provenance | **ที่มาของข้อมูลและผลลัพธ์** | Only if the writer reaches back to #13. |
| Human oversight | **การกำกับดูแลโดยมนุษย์** | §2.2 lists it as part of "the complete system". |
| Model versus system | **โมเดลกับระบบ** | Principle #2. |
| Learning loop | **วงจรการเรียนรู้** | Layer stamp. |
| Incident-learning loop | **วงจรเรียนรู้จากเหตุการณ์ผิดปกติ** | Next-post hook only. |
| Assurance envelope / Assurance contract | **กรอบการรับประกันรอบระบบ / สัญญาการรับประกันเชิงระบบ** | Only if called back from #11/#12. **envelope ≠ contract** — flagged drift risk. |
| AI-core | **AI ที่เป็นแกนหลัก** | **Not** "AI แกนกลาง" — flagged drift risk. |

**Kept in English inline (as the book does):** Workflow · Trace · Fallback · Threshold · Manifest · Escalation · Release · Rollback · Regression test · Prompt · Golden set · Canary · Shadow mode · Pilot · Dashboard · Retrieval · Override · Guard · Supplier/Vendor · Sandbox · Drift · Exposure.

**Thai section labels (verbatim from the book):** หลักปฏิบัติห้าประการ · เวิร์กช็อป · ตัวชี้วัดสำคัญ · รูปแบบความล้มเหลว · วัตถุประสงค์ / ใช้เมื่อ / เจ้าของหลัก.

**Deviations from the canonical list, declared:** none. One *rendering* decision that is not a glossary entry — the Thai track should read **"ภาษาไทยและภาษาอื่นที่ใช้งานจริง"** rather than the book's elliptical printed "ภาษาไทยและภาษาจริง"; render it outside quotation marks (see §2.4).

---

## 7. Do not assert

Searched for, and could not verify. A writer who needs any of these must drop the claim or reframe it as flagged in the right-hand column.

| Claim | Status | What to do instead |
|---|---|---|
| **A Thai golden set must contain tone, transliterated product names, mixed-script queries, and Buddhist-era dates** (spec §5 THAI BOX) | **NOT IN THE BOOK.** Full-text search of all 97 pages for `Buddhist`, `B.E.`, `พ.ศ.`, `พุทธศักราช`, `transliterat`, `mixed-script`, `mixed script` → **zero hits** in any evaluation context (the only `B.E.` hit is reference [22], the PDPA's title). No external source supports it either. | The book supports only: "Thai and other operating languages" is one of the things to test (§2.4), and gate row 3 is "Golden/hidden utility **by language**, case and severity" (§2.10). The four specifics may be written as **the author's own practitioner guidance in the first person** ("สิ่งที่ผมยืนยันว่าชุด golden ภาษาไทยต้องมี…" / "In my own practice a Thai golden set has to carry…") — **never with a `[N]` superscript, never as "the book says".** |
| **"The book lists seven failure patterns"** | FALSE — it lists nine (§2.9). | State no count; render the list. |
| **Any count of "Metrics that matter"** | The EN and TH lists disagree (13 vs 14, §2.8). | State no count; render the table. |
| **"Eight gate rows: Utility, Security, Effects, Trace, Operations, Economics, Recovery + Thai/language slice"** (spec §5 wording) | Does not match the book. Artifact 7 has 7 gate rows + a Decision row; the seven-word list is Figure 12's gate bar; "by language" is inside row 3. | Build the table from §2.10's verbatim rows (N3). |
| **NIST requires / mandates a release gate, canary rollout, or exposure cap** | NOT SUPPORTED. AI RMF 1.0: *"intended to be voluntary… Actions do not constitute a checklist, nor are they necessarily an ordered set of steps."* AI 600-1 issues *suggested actions* whose implementation "will vary". | Say the playbook **turns** NIST's principles **into** a release portfolio — the book's own framing: "The book turns those principles into a release portfolio rather than claiming certification." |
| **NIST's June 2026 proof tells you how often to re-test / gives a cadence** | NOT SUPPORTED — the page names no frequency or schedule; the book's own boundary says so. | Pair every use of [7] with the boundary clause (§D1). Note that AI 600-1's MS-4.2-001 *does* say "at a regular cadence" — that is [4], and it names no interval either. |
| **NIST's June 2026 proof is about evaluation tracks, release gates, or Thai-language testing** | NOT SUPPORTED — it is an information-theoretic result about guardrail robustness against adversarial prompts. | Use it only to justify **track 3 (Adaptive)** and **track 5 (Live monitoring)**: a fixed defence set cannot be finished. The link from that result to a five-track suite is the **book's** synthesis. |
| **"Never average away a failed structural invariant or severe slice" is a NIST rule** | It is the **playbook's** line (Artifact 7, §2.10). | Attribute to the playbook in the `.alert danger`. |
| **AI RMF 1.0 is NIST's current and settled framework text** | NOT SAFE as written. The resource page, read 2026-09-05, says: *"The AI RMF 1.0 is being revised as part of the White House AI Action Plan."* | Cite the Govern/Map/Measure/Manage **shape**, dated to 26 January 2023, and add the D2 caveat. Never write "the latest AI RMF" or quote a clause as a live requirement. |
| **NIST's AI RMF resource page names Govern/Map/Measure/Manage in its text** | It does not — the four names live in the page's graphic. | Cite the framework document NIST AI 100-1, which the page hosts, for the naming and the MEASURE/MANAGE definitions. |
| **Any 517-execution figure from the r8 paper** | Not used in this post; the paper is unpublished and unlinkable. | Omit. If ever reintroduced, pair with its boundary sentence verbatim and never link. |
| **Anything from the masterclass video `n_IwUYevRZo`** | Not a source for this post ("No additions"); not verified here. | Omit entirely. |
| **41.3% · 240 cases · 18 min · 46 h · THB 2,500 · 80,000 letters** | Not present in pp. 38–41 or 79–80. | Omit from this post. |
| **Any Thai legal, EU AI Act, AI Index, IEA, ISO 42005, ETDA or PDPA status sentence** | No such claim is in the spec, and this ledger verified none. | Omit; a writer who wants one must commission a fresh check. |
| **The IEEE article behind [7]** (Vassilev, *IEEE S&P* 24(3), 14 May 2026, DOI 10.1109/MSEC.2026.3678214) | **Verified** (csrc.nist.gov record, HTTP 200) but **not authorised** — the spec says "No additions." | Do not add without editor approval. If approved, cite the `csrc.nist.gov` record, not the DOI (`doi.org` → ieeexplore returns 202 behind a bot challenge). |

---

*Independently re-verified 2026-09-05: every quotation in §1 was re-fetched and matched byte-for-byte — `nist.gov/itl/ai-risk-management-framework` (HTTP 200), `nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf` (HTTP 200, 1,946,127 bytes; the "four functions" and "tested before their deployment" lines confirmed in situ), `nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf` (HTTP 200, 1,174,643 bytes, July 2024), the June 2026 news item (HTTP 200, `datePublished 2026-06-09`, `dateModified 2026-06-22` from the page's own JSON-LD), `csrc.nist.gov` record (HTTP 200), `doi.org/10.1109/MSEC.2026.3678214` (→ `ieeexplore.ieee.org/document/11475847/`, **202** bot challenge — cite the CSRC record instead). The full-text search for `Buddhist` / `พ.ศ.` / `พุทธศักราช` / `transliterat` / `mixed-script` across all 97 book pages was re-run: still zero hits.*

*Ledger compiled 2026-09-05 (Asia/Bangkok). Book pages read in full before writing: PDF 39–42 (printed 38–41) and PDF 80–83 (printed 79–82), plus PDF 93–96 (printed 92–95, Appendix D) for the boundary lines and PDF 78 (printed 77) for the CX-REFUND-01 framing.*
