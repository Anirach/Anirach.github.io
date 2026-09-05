# Research ledger — post #11 `ai-transformation-ai-core`

**Title (fixed, from the manifest):** When Is AI the Core? — Authority × Indispensability, and Context as Program
**Group:** Engineer · **Layer:** Spine · **Question:** Q4 · **Read time:** 20 min
**Book chapter:** Ch. 7 "Engineer AI-as-a-Core" (printed pp. 30–33 = PDF 31–34); Appendix B Artifact 1 (printed pp. 67–68 = PDF 68–69) and Artifact 4 (printed pp. 73–74 = PDF 74–75)
**Access date for every source below:** 2026-09-05 (Asia/Bangkok)
**Researcher note:** Writers may not introduce a source, number or claim that is not in this ledger.

---

## Sources

| # | Label | Title | URL | Publisher | Pub date | Accessed | Supports |
|---|---|---|---|---|---|---|---|
| S1 | Synthesis | Mingkhwan, Anirach. *Engineering AI-Core Systems: A Reference Architecture and Assurance Contract for Software 3.0*, revision 8 | **none — unpublished, author-supplied paper; no public URL. NEVER LINK.** | — (author-supplied) | September 2026 | 2026-09-05 | The AI-core classification (authority × indispensability, task-scoped); context-as-program; the runtime-context release manifest; proposal–effect separation; five-rail controls; reconstructable traces |
| S2 | Synthesis | Mingkhwan, Anirach. *AI Transformation as an Organizational Core — A bilingual companion playbook* | — (project source document; no public URL verified on 2026-09-05) | Anirach Mingkhwan | Evidence snapshot 5 September 2026 | 2026-09-05 | Everything quoted verbatim in this ledger: Ch. 7 argument, five operating principles, Boundary walk, Metrics that matter, Failure patterns, Artifact 1, Artifact 4, Appendix C glossary |
| S3 | Study | Saltzer, Jerome H., and Michael D. Schroeder. "The Protection of Information in Computer Systems." *Proceedings of the IEEE* 63, no. 9 (1975): 1278–1308 | `https://doi.org/10.1109/PROC.1975.9939` (DOI resolves 302 → `https://ieeexplore.ieee.org/document/1451869/`) | Institute of Electrical and Electronics Engineers (IEEE); ISSN 0018-9219 | 1975 | 2026-09-05 | Complete mediation, least privilege, fail-safe defaults, economy of mechanism — the design principles behind "code owns permissions and effect mediation" |
| S4 | Standard | NIST. *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*, NIST AI 600-1 | `https://doi.org/10.6028/NIST.AI.600-1` (resolves → `https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf`); landing page `https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence` | National Institute of Standards and Technology, U.S. Department of Commerce | 26 July 2024 (Editorial Review Board approval 2024-07-25) | 2026-09-05 | GenAI-specific risk actions: the 12 risk categories, prompt injection (direct and indirect) as an Information Security risk, version control and tamper-proof content history (MS-2.8-003), organizational governance calling for additional human review |
| S5 | Study *(essay — not a controlled study)* | Karpathy, Andrej. "Software 2.0" | `https://karpathy.medium.com/software-2-0-a64152b37c35` | Medium | 11 November 2017 (`datePublished` `2017-11-11T22:18:53Z`) | 2026-09-05 | Attribution of the Software 1.0 / Software 2.0 vocabulary |
| S6 | Study *(recorded talk — not a controlled study)* | Karpathy, Andrej. "Software Is Changing (Again)" — keynote, YC AI Startup School, San Francisco | `https://www.ycombinator.com/library/MW-andrej-karpathy-software-is-changing-again` (video `https://www.youtube.com/watch?v=LCEmiRjPEtQ`) | Y Combinator | Keynote delivered 17 June 2025; video published 18 June 2025 | 2026-09-05 | Attribution of the **Software 3.0** term, and of the LLM-as-operating-system analogy the book then breaks |

### Fetch record (what actually happened on 2026-09-05)

- **S3** — `doi.org/10.1109/PROC.1975.9939` returned **302** to `ieeexplore.ieee.org/document/1451869/`; IEEE Xplore itself returns **HTTP 202** to automated clients (Cloudflare bot challenge, not a dead link). Bibliographic record therefore confirmed against the **Crossref registry** (`api.crossref.org/works/10.1109/PROC.1975.9939` → title, *Proceedings of the IEEE*, vol. 63, iss. 9, pp. 1278–1308, 1975, publisher IEEE, authors J.H. Saltzer / M.D. Schroeder), and the principle wording read from the authors' MIT copy, `https://web.mit.edu/Saltzer/www/publications/protection/Basic.html` (**HTTP 200**). **Cite the DOI, not the MIT mirror.**
- **S4** — DOI **302** → `nvlpubs.nist.gov/.../NIST.AI.600-1.pdf` (**HTTP 200**, PDF read in full). NIST landing page (**HTTP 200**) confirms "Date Published: July 26, 2024", the DOI, and no withdrawal or supersession; page last updated 8 April 2026.
- **S5** — `karpathy.medium.com` and `medium.com/@karpathy` both return **HTTP 403** to automated fetches (Medium bot block; the page is live in a browser). Date and text confirmed from the Internet Archive capture of the same URL, `web.archive.org/web/20260726023251/…` (**HTTP 200**), whose embedded `datePublished` is `2017-11-11T22:18:53Z` and whose byline reads "Nov 11, 2017". **Cite the Medium URL** and treat the archive as the verification trail only.
- **S6** — YC library page **HTTP 200**; embedded YouTube id `LCEmiRjPEtQ` confirmed via YouTube oEmbed (title "Andrej Karpathy: Software Is Changing (Again)", channel Y Combinator). Watch page metadata: `uploadDate 2025-06-18T18:05:19-07:00`, `lengthSeconds 2371`, description opening "Andrej Karpathy's keynote on June 17, 2025 at AI Startup School in San Francisco."

### Verified but NOT a source for this post

- **The Foundation masterclass EP01**, video id `n_IwUYevRZo` — verified live on 2026-09-05 via YouTube oEmbed: title `AI Transformation: จากการใช้ AI สู่องค์กรที่เรียนรู้เร็วที่สุด | The Masterclass EP01`, channel *The Foundation (th)* (`youtube.com/@TheFoundationTH`); matches the book's D.3 entry 2 exactly. **Post #11 cites no masterclass material and no timestamp.** If a later edit adds one: paraphrase only, never quote, and re-verify the `&t=` value.

---

## Claim classes in this post

| Class | Instances in the spec | Handling |
|---|---|---|
| **Framework attribution** | AI-core 2×2 (authority × indispensability); the four cells; the four-layer reference architecture; the runtime-context manifest's six domains; the five operating principles; proposal–effect separation | S1 (author's own paper) via S2 (the book). Always attributed to Mingkhwan, never to a standards body. |
| **Framework attribution (external)** | Software 1.0 / 2.0 / 3.0 vocabulary; the LLM-as-operating-system analogy | S5 (1.0/2.0) and S6 (3.0, OS analogy). **The book itself cites neither** — grep of the full PDF returns zero occurrences of "Karpathy". This is the spec's named addition, so the writer must introduce it as the post's own attribution, never as "the book cites Karpathy". |
| **Framework attribution (external)** | Complete mediation, least privilege, fail-safe defaults | S3, with the book's own boundary line (see below). |
| **Standard reference** | GenAI-specific risk actions; prompt injection; version control of the behaviour surface | S4, with the voluntary-framework boundary. |
| **Material number** | See Number cards NC-1 … NC-8. All are either NIST's own count or structural counts of the book's own artifacts. | Card required; no card, no number. |
| **Dated legal / standard status** | Only S4's publication status. No law, no Thai regulation, no EU instrument is claimed anywhere in post #11. | See Dated statuses. |
| **Study finding** | None. This post asserts no empirical result — no effect size, no survey figure, no benchmark. | The writer must not import one. |
| **Direct quotation** | The one 💡 blockquote quoting **one** of Chapter 7's five operating principles (verbatim below); the Artifact 4 warning line "Never store credentials in the manifest"; the context-as-program sentence. | Quote from the verbatim block below, not from memory. |
| **Fictional-case value** | Luma Commerce Thailand / `CX-REFUND-01` and every id, threshold and percentage attached to it. | See Fictional values; flagged on first mention. |

---

## Verbatim source text (quote from here, do not re-translate)

### Chapter epigraph (printed p. 30)
> AI-core is a task scoped runtime class defined by decision authority and model indispensability then governed according to consequence.

### The definition (English companion, printed p. 31)
> An AI-core system is not simply software that calls a model. It is a scoped runtime class in which model output controls an important share of released content, action, or program branch, and a predeclared removal test shows that the model is indispensable to the specified task set. Classification belongs to a task, manifest, golden set, and threshold, not to a vendor, model family, or whole organization.

> This separates four ideas. AI-assisted coding changes how software is developed. A coding agent performs delegated repository work. AI-enabled software contains a model-backed feature. An AI-core system makes model-generated behavior load-bearing at runtime. One product can contain an optional summarizer, an indispensable policy advisor, and an AI-core routing function.

### Software 1.0/2.0/3.0 and context as program (printed p. 31)
> Software 1.0, 2.0, and 3.0 remain in the same call path. Explicit code owns interfaces, permissions, control flow, transactions, and effect mediation. Learned components contribute statistical capability. Runtime context supplies goals, examples, retrieved knowledge, tools, and state. Behavior therefore depends on the assembly: model version, decoding, context, retrieval, tool semantics, orchestration, memory, and environment. A behavior-relevant change to any component is a program change and should trigger a new manifest and evidence review.

### The four layers and the broken OS analogy (printed p. 31)
> The reference architecture has four layers. A governed data foundation supplies authoritative records and versioned knowledge. The AI-core layer combines the model, context assembly, retrieval, and bounded memory. Orchestration coordinates requests, specialist components, tools, and state. Applications and human operations expose outcomes and handle the residue. Assurance controls cross every layer. The operating-system analogy helps, but context has no true memory protection, retrieval has no stable read contract without versioning, and a natural-language tool request is not an authorized system call.

### The CX-REFUND-01 call path (printed pp. 31–32)
> In CX-REFUND-01, an authenticated request enters the context assembler. It retrieves only approved policy passages and reads current order state through bounded services. The model may draft an answer, select a route, or propose `issue_refund(amount, reason)`. The proposal is not the effect. An execution guard checks identity, allow-list, schema, customer binding, amount, approval token, transaction budget, and idempotency. The system reassembles context after a tool result. A structurally valid and sufficiently supported response reaches release; otherwise it is repaired once, withheld, or escalated.

### Five operating principles (English, printed p. 32) — quote exactly ONE in the 💡 blockquote, list the rest in prose; never renumber
1. **Scope AI-core behavior explicitly** Declare task authority fallback golden set and indispensability threshold.
2. **Keep control and effects in code** Models propose while services authorize validate transact and release.
3. **Version the whole behavior surface** Bind model context corpus tools policy evaluators and thresholds.
4. **Grant minimum capability per request** Bind tools to subject purpose amount duration and transaction.
5. **Design fallback as a primary path** Open-ended tasks often fall back to refusal degradation or escalation.

### หลักปฏิบัติห้าประการ (Thai mirror, printed p. 33) — the canonical Thai wording
1. **ระบุพฤติกรรม AI-core อย่างมีขอบเขต** ประกาศ Task, Authority, Fallback, Golden Set และ Threshold
2. **ให้โค้ดควบคุมสิทธิ์และผลกระทบ** โมเดลเสนอ บริการ Authorize, Validate, Transact และ Release
3. **กำหนดรุ่นของพื้นผิวพฤติกรรมทั้งหมด** ผูก Model, Context, Corpus, Tool, Policy, Evaluator และ Threshold
4. **ให้สิทธิ์ต่ำสุดต่อคำขอ** ผูก Tool กับ Subject, Purpose, Amount, Duration และ Transaction
5. **ออกแบบ Fallback เป็นเส้นทางหลัก** งานปลายเปิดมักต้อง Refuse, Degrade หรือ Escalate

### Working session — Boundary walk (English, printed p. 32)
> Walk a benign case, ambiguous case, injected document, over-limit refund, duplicate request, and tool failure through the architecture. At every transition ask what crosses, what is trusted, what is estimated, what hard invariant applies, what trace proves the route, and who handles failure. Produce a boundary inventory and remove any path that releases content or commits an effect without mediation.

### เวิร์กช็อป Boundary walk (Thai, printed p. 33)
> เดินกรณีปกติ กำกวม เอกสาร Injection ยอดเกิน Request ซ้ำ และ Tool Failure ผ่านสถาปัตยกรรมทุกขั้น ถามว่าอะไรข้าม Boundary สิ่งใดเชื่อถือ สิ่งใดเป็นค่าประเมิน Hard Invariant ใดใช้ Trace ใดพิสูจน์ และใครรับ Failure ผลลัพธ์คือ Boundary Inventory และการกำจัดทุกเส้นทางที่ Release หรือ Commit Effect โดยไม่ผ่านการกำกับ

### Metrics that matter (English, printed p. 32)
> Monitor mediated-path coverage, manifest resolution, provenance, schema rejection, unauthorized-effect escape, duplicate rejection, trace completeness, fallback, escalation, task success by slice, p50 and p95 latency, tokens, cost, and authoritative post-state accuracy.

### ตัวชี้วัดสำคัญ (Thai, printed p. 33)
> ติดตาม Mediated-path Coverage, Manifest Resolution, Provenance, Schema Rejection, Unauthorized-effect Escape, Duplicate Rejection, Trace Completeness, Fallback, Escalation, Task Success ตาม Slice, p50 และ p95 Latency, Token, Cost และความถูกต้องของ Authoritative Post-state

### Failure patterns (English, printed p. 32) — eight, in this order
> Bolted-on chatbots, prompts edited outside change control, direct model calls from user interfaces, tools without subject binding, unbounded cross-session memory, output filters after effects occur, agent proliferation without privilege separation, and logs without context thresholds versions or routes.

### รูปแบบความล้มเหลว (Thai, printed p. 33)
> Chatbot ที่ติดเพิ่มภายหลัง Prompt ที่แก้นอก Change Control การเรียกโมเดลตรงจาก UI, Tool ไม่ผูก Subject, Memory ข้ามเซสชันไร้ขอบเขต Output Filter หลังเกิดผล Agent จำนวนมากไร้ Privilege Separation และ Log ที่ไม่มี Context, Threshold, Version หรือ Route

### Figure 8 cell labels (printed p. 30, verbatim from the drawn figure)
- **INDISPENSABLE ADVISOR / ผู้ช่วยที่จำเป็น** — "Text release is the effect boundary" (indispensable, low authority)
- **AI-CORE / AI เป็นแกนกลาง** — "Full assurance envelope" (high on both, red)
- **AI FEATURE / คุณลักษณะ AI** — "Proportionate controls" (low on both)
- **BOUNDED AGENT / เอเจนต์ในขอบเขต** — "Hard effect mediation" (high authority, dispensable)
- Axes: `INDISPENSABILITY / ความจำเป็น` (y) × `DECISION AUTHORITY / อำนาจในการตัดสินใจ` (x)
- Panel title: "What is AI-core" / จำแนกตามอำนาจในการตัดสินใจและความจำเป็นของโมเดล
- Caption line in the book: *Figure 8 AI-core classification by authority and indispensability. Adapted as an original redraw from Mingkhwan 2026*

> ⚠️ The figure's own y-axis gloss is **ความจำเป็น**, but the Appendix C canonical rendering for *Indispensability* is **ความขาดไม่ได้** and the plan flags ความจำเป็น as the drift to avoid. In prose use **ความขาดไม่ได้**; the figure label is the drawn artwork's business, not the writer's.

### Figure 9 node labels (printed p. 31, verbatim from the drawn figure)
MODEL / โมเดล · DECODING / การสุ่ม · SYSTEM CONTEXT / บริบทระบบ · RETRIEVAL / การค้นคืน · TOOLS / เครื่องมือ · MEMORY / หน่วยความจำ · ORCHESTRATION / การประสานงาน · ENVIRONMENT / สภาพแวดล้อม → core: **BEHAVIOR / พฤติกรรม — One manifest / หนึ่งบัญชีรายการ**. Footer inside the figure: "Any behavior-relevant change is a program change and triggers evidence review." Book caption: *Figure 9 Runtime context is part of the program. Author synthesis from Mingkhwan 2026*

### Artifact 1 — preamble (printed p. 67)
> All examples use **CX-REFUND-01**, a fictional Luma Commerce Thailand assistant. It answers bilingual refund questions and may propose `issue_refund`. An external guard may execute one eligible refund no greater than THB 2,000 after confirmation; all other financial actions go to a person. **Values are illustrative, not universal thresholds.**

> **Purpose** Classify one released capability by two independent axes: model decision authority and model indispensability. Assess consequence separately. **Use when** selecting a use case and whenever task, authority, fallback, tools, thresholds, or release manifest changes. **Accountable owner** Business or product owner; release owner verifies the evidence.

**Copy-ready card — the 10 fields, in order (EN | TH, printed pp. 67–68):**

| # | Field (EN) | ช่องข้อมูล (TH) | Complete this entry / รายการที่ต้องกรอก |
|---|---|---|---|
| 1 | ID, task set, exclusions, manifest | รหัส ชุดงาน กรณีไม่รวม และ Manifest | *(blank)* |
| 2 | Model-controlled released behavior | พฤติกรรมที่โมเดลกำหนดและถูกปล่อย | Text, tool choice, arguments, or runtime branch / ข้อความ Tool ค่า Argument หรือ Runtime Branch |
| 3 | Authority test and trace evidence | การทดสอบอำนาจและ Trace | Advisory or high authority / Advisory หรืออำนาจสูง |
| 4 | Declared non-model fallback | Fallback ที่ไม่ใช้โมเดล | *(blank)* |
| 5 | Golden set, task-success rule, predeclared indispensability threshold | Golden Set นิยาม Task Success และ Indispensability Threshold ที่ประกาศล่วงหน้า | *(blank)* |
| 6 | Removal ablation: model versus fallback on the same set | Removal Ablation บนชุดเดียวกัน | *(blank)* |
| 7 | Classification | ประเภท | High/high AI-core; high/low bounded agent; advisory/high indispensable advisor; advisory/low AI feature — สูง/สูง AI-core; สูง/ต่ำ Bounded Agent; แนะนำ/สูง Indispensable Advisor; แนะนำ/ต่ำ AI Feature |
| 8 | Separate consequence profile | ผลกระทบแยกต่างหาก | Severity, exposure, detectability, recoverability, affected rights or assets / ความรุนแรง การเปิดรับ การตรวจพบ การกู้คืน สิทธิหรือสินทรัพย์ที่ได้รับผล |
| 9 | Minimum controls, owner, decision, date | ตัวควบคุมขั้นต่ำ เจ้าของ คำตัดสิน วันที่ | *(blank)* |
| 10 | Reclassification triggers | Trigger ที่ต้องจัดประเภทใหม่ | *(blank)* |

**Completed CX-REFUND-01 — SEVEN rows, not ten (printed p. 68):** Scope · Authority · Fallback · Ablation · Class · Consequence · Decision.

- **Scope** — Delivered Thailand direct-retail orders; routine explanation and one eligible refund; excludes fraud flags, subscriptions, marketplace orders, legal complaints, non-THB payments, and amounts above THB 2,000.
- **Authority** — Model determines released explanation, cited passages, refund recommendation and proposed arguments; qualifying proposals reach the guard without line review.
- **Fallback** — Fixed policy links plus customer-care queue; no automated refund.
- **Ablation** — `CXGS-2026-09-v3`, 240 sliced cases; fallback must reach 70% to be considered sufficient; **illustrative result**: candidate 94.6%, fallback 41.3%.
- **Class** — High authority and indispensable: AI-core for this task set and manifest.
- **Consequence** — Public text may mislead; financial write is recoverable only with cost.
- **Decision** — Full envelope, mediated output and tool paths, terminal traces, human route outside the bounded cell; **VP Customer Operations owns reclassification.**

### Artifact 4 — Runtime context release manifest (printed pp. 73–74)
> **Purpose** Pin the whole behavior-determining release, not only the model. The manifest declares how context should be assembled; the trace records what one request actually received. **Use when** any model, decoding, prompt, corpus, retrieval, tool, control, threshold, evaluator, or orchestration component changes. **Accountable owner** Release owner signs the integrated manifest; component owners attest their entries.

**Six domains and their required fields (verbatim):**

| Domain (EN) | หมวด (TH) | Required fields |
|---|---|---|
| Identity and scope | Identity/Scope | Use-case and manifest IDs, status, owner, parent, ticket, tasks, exclusions, locales, channels, consequence classes |
| Core and context | Core/Context | Exact dated model ID, region, decoding, assembly commit, instruction/template hashes, examples, ordering, token budget |
| Knowledge and state | Knowledge/State | Corpus hash, source allow-list, ranker/embedding, top-k, freshness, provenance, session schema, memory and retention |
| Tools and controls | Tool/Control | Registry/schema hashes, authentication, bounds, idempotency, sandbox, five-rail versions, thresholds and routes |
| Evaluation and trace | Evaluation/Trace | Golden, hidden, adaptive and fault suites; grader versions; trace schema, storage, redaction, access and retention |
| Operations and integrity | Operations/Integrity | Rollout, exposure cap, stop conditions, rollback ID, outage route, approvals, manifest hash, dependency lock, artifact locations |

**The `.alert danger` line, verbatim (EN | TH):**
> Never store credentials in the manifest; reference a controlled secret. Deterministic decoding does not remove context, retrieval, model-version, state, or infrastructure sensitivity.
> ห้ามเก็บ Credential ใน Manifest ให้อ้างอิง Secret ที่ควบคุม และอย่าเข้าใจว่า Deterministic Decoding ลบความไวต่อ Context, Retrieval, Model Version, State หรือ Infrastructure

**Completed CX-REFUND-01 manifest — FIVE rows, not six.** The book's worked example merges *Evaluation and trace* with *Operations and integrity* into one row headed **"Evaluation and operations"**:

| Domain | Example (verbatim) |
|---|---|
| Identity and scope | `CX-REFUND-01.2026-09-rc4`, parent `2026-08-prod2`, change `CHG-4821`; Thailand web/mobile chat, Thai/English, bounded task and exclusions from Artifact 1 |
| Core and context | Fictional dated ID `luma/cx-core-2026-08-17`; temperature 0, maximum 900 tokens, schema mode; assembly commit `9f31c7a`, template `refund-chat-v12`, untrusted text never promoted to instruction |
| Knowledge and state | Corpus `TH-CX-2026-09-01`, immutable hash, allow-listed policy IDs, ranker `rr-4.2`, top-k 6; session schema v5, no cross-customer memory |
| Tools and controls | `paytools-v7`, only `issue_refund`, THB 1–2,000, confirmation and idempotency required; `cx-rails-v9`, output schema v6, contracted thresholds |
| Evaluation and operations | `CXGS-v3`, `CXRT-v5`, hidden `CXH-2026Q3`, adaptive `CXA-09`, faults `CXF-v4`; stages 5/25/50/100%; stop on prohibited effect, severe escape or missing terminal trace; seven functional sign-offs and immutable manifest hash |

**[THAI BOX] locale details** — the Thai example row wording: Corpus `TH-CX-2026-09-01` พร้อม Immutable Hash, Policy Allow-list, Ranker `rr-4.2`, Top-k 6; Session Schema v5 และไม่มี Memory ข้ามลูกค้า · Web/Mobile ไทย ภาษาไทย/อังกฤษ · `paytools-v7`, เฉพาะ `issue_refund`, 1–2,000 บาท. **The book's manifest example does not carry an explicit `+07` timestamp offset** — see Do not assert.

### External wording to quote or attribute

**S3 — Saltzer & Schroeder, §"3) Design Principles" (verbatim):**
- Economy of mechanism: "Keep the design as simple and small as possible."
- Fail-safe defaults: "Base access decisions on permission rather than exclusion."
- **Complete mediation: "Every access to every object must be checked for authority."**
- Least privilege: "Every program and every user of the system should operate using the least set of privileges necessary to complete the job."

**S4 — NIST AI 600-1, §2.9 Information Security (verbatim, on prompt injection):**
> GAI-based systems present two primary information security risks: GAI could potentially discover or enable new cybersecurity risks by lowering the barriers for or easing automated exercise of offensive capabilities; simultaneously, it expands the available attack surface, as GAI itself is vulnerable to attacks like prompt injection or data poisoning.

> Indirect prompt injection attacks occur when adversaries remotely (i.e., without a direct interface) exploit LLM-integrated applications by injecting prompts into data likely to be retrieved.

**S4 — action MS-2.8-003 (verbatim), the manifest's external anchor:**
> Use digital content transparency solutions to enable the documentation of each instance where content is generated, modified, or shared to provide a tamper-proof history of the content, promote transparency, and enable traceability. Robust version control systems can also be applied to track changes across the AI lifecycle over time.

**S5 — Karpathy, "Software 2.0" (verbatim):**
> The "classical stack" of Software 1.0 is what we're all familiar with — it is written in languages such as Python, C++, etc. It consists of explicit instructions to the computer written by a programmer.

> In contrast, Software 2.0 is written in much more abstract, human unfriendly language, such as the weights of a neural network.

**S6 — YC's own description of the talk (verbatim):**
> We've entered the era of "Software 3.0," where natural language becomes the new programming interface and models do the rest.

Chapter markers on the published video (for timestamp accuracy if one is cited): `01:25 — Software evolution: From 1.0 to 3.0`; `04:40 — Programming in English: Rise of Software 3.0`; `06:10 — LLMs as utilities, fabs, and operating systems`; `11:04 — The new LLM OS and historical computing analogies`.

---

## Number cards

Every number below is a **structural count of the book's own artifacts** or a **count published by NIST**. This post asserts no empirical measurement. If the writer wants a number that has no card here, the answer is: drop it.

---

### NC-1 — NIST AI 600-1 enumerates 12 GAI risk categories
- **Value / unit:** 12 · risk categories
- **Denominator / population:** the whole document; §2 "Overview of Risks Unique to or Exacerbated by GAI", numbered 2.1–2.12
- **Comparison:** none — it is an enumeration, not a rate
- **Task / setting:** a cross-sectoral profile of the AI RMF for generative AI; voluntary use
- **Source:** S4 (NIST AI 600-1, 26 July 2024). The list: CBRN Information or Capabilities · Confabulation · Dangerous, Violent, or Hateful Content · Data Privacy · Environmental Impacts · Harmful Bias and Homogenization · Human-AI Configuration · Information Integrity · Information Security · Intellectual Property · Obscene, Degrading, and/or Abusive Content · Value Chain and Component Integration
- **Boundary (NIST's own, via the book's D.3 entry 4):** "organizations must select and tailor actions to their use case and risk tolerance" — and NIST's own §2 caveat: "some GAI risks are unknown, and are therefore difficult to properly scope or evaluate"
- **TH sentence:** NIST AI 600-1 (26 กรกฎาคม 2024) แจกแจงความเสี่ยงเฉพาะของ Generative AI ไว้ 12 หมวด โดยหมวด Information Security ระบุ Prompt Injection ทั้งแบบตรงและแบบอ้อมไว้ชัดเจน — เอกสารนี้เป็นกรอบสมัครใจ องค์กรต้องเลือกและปรับ Action ให้ตรงกับ Use Case และระดับความเสี่ยงของตนเอง
- **EN sentence:** NIST AI 600-1 (26 July 2024) enumerates twelve risk categories unique to or exacerbated by generative AI, and names both direct and indirect prompt injection under Information Security — it is a voluntary profile, and organisations must select and tailor the actions to their own use case and risk tolerance.

> ⚠️ Some secondary write-ups say "13 risks and more than 400 actions". The published document's §2 is numbered 2.1–2.12 — **twelve**. Use 12, or avoid the count entirely.

---

### NC-2 — The classification card has 10 fields; the completed example fills 7 rows
- **Value / unit:** 10 · fields (blank card) — 7 · rows (worked example)
- **Denominator / population:** Artifact 1, printed pp. 67–68
- **Comparison:** the blank card's 10 field rows vs the completed CX-REFUND-01 table's 7 rows (Scope, Authority, Fallback, Ablation, Class, Consequence, Decision)
- **Task / setting:** classifying one released capability, per task and per manifest
- **Source:** S2 Artifact 1 (concept: S1)
- **Boundary:** the worked example is a fictional case; the field list is the reusable part
- **TH sentence:** การ์ดจำแนก AI-core มี 10 ช่อง และตัวอย่างที่กรอกแล้วของ CX-REFUND-01 แสดง 7 แถว
- **EN sentence:** The AI-core classification card has ten fields; the worked CX-REFUND-01 example is shown as seven filled rows.

---

### NC-3 — The runtime-context release manifest has 6 domains; the worked example shows 5 rows
- **Value / unit:** 6 · domains (copy-ready manifest) — 5 · rows (worked example)
- **Denominator / population:** Artifact 4, printed pp. 73–74
- **Comparison:** the example merges *Evaluation and trace* + *Operations and integrity* into one row, "Evaluation and operations"
- **Task / setting:** pinning one behaviour-determining release
- **Source:** S2 Artifact 4 (concept: S1)
- **Boundary:** "Never store credentials in the manifest; reference a controlled secret. Deterministic decoding does not remove context, retrieval, model-version, state, or infrastructure sensitivity."
- **TH sentence:** บัญชีรายการบริบทขณะทำงาน (runtime-context manifest) มีหกโดเมน และตัวอย่าง CX-REFUND-01 ในหนังสือรวมสองโดเมนสุดท้ายไว้ในแถวเดียว จึงแสดงห้าแถว
- **EN sentence:** The runtime-context manifest has six domains; the book's CX-REFUND-01 example collapses the last two into a single "Evaluation and operations" row, so it prints as five.

---

### NC-4 — The reference architecture has 4 layers, with assurance crossing all of them
- **Value / unit:** 4 · layers (+1 cross-cutting control set)
- **Denominator / population:** Chapter 7, printed p. 31
- **Comparison:** governed data foundation → AI-core layer → orchestration → applications and human operations; assurance crosses every layer
- **Task / setting:** the AI-core reference architecture for a declared task set
- **Source:** S2 Ch. 7 (concept: S1)
- **Boundary:** the OS analogy is offered and then broken — "context has no true memory protection, retrieval has no stable read contract without versioning, and a natural-language tool request is not an authorized system call"
- **TH sentence:** สถาปัตยกรรมอ้างอิงมีสี่ชั้น และ Assurance พาดผ่านทุกชั้น
- **EN sentence:** The reference architecture has four layers, and assurance controls cross every one of them.

---

### NC-5 — Five operating principles (Chapter 7)
- **Value / unit:** 5 · principles
- **Denominator / population:** Chapter 7 only. Each chapter has its own five; they are never renumbered and never mixed across chapters.
- **Comparison:** —
- **Task / setting:** engineering an AI-core runtime
- **Source:** S2 Ch. 7 (verbatim list above)
- **Boundary:** these are the author's operating principles, not a standard
- **TH sentence:** บทนี้สรุปเป็นหลักปฏิบัติห้าประการ
- **EN sentence:** The chapter closes on five operating principles.

---

### NC-6 — The boundary walk is 6 cases × 6 questions
- **Value / unit:** 6 · cases; 6 · questions (36 transitions to inspect)
- **Denominator / population:** Chapter 7 working session
- **Comparison:** cases — benign, ambiguous, injected document, over-limit refund, duplicate request, tool failure; questions — what crosses / what is trusted / what is estimated / which hard invariant applies / which trace proves the route / who handles failure
- **Task / setting:** walking one architecture end to end to produce a boundary inventory
- **Source:** S2 Ch. 7
- **Boundary:** the deliverable is an inventory with **no unmediated release or effect path** — the walk itself proves nothing without the removal
- **TH sentence:** Boundary walk เดินหกกรณีผ่านสถาปัตยกรรม โดยถามหกคำถามที่ทุกจุดเปลี่ยน
- **EN sentence:** The boundary walk runs six cases through the architecture, asking the same six questions at every transition.

---

### NC-7 — Fourteen or fifteen monitored quantities — do not assert a total
- **Value / unit:** 14 or 15 · monitored quantities, depending on whether "p50 and p95 latency" is counted as one item or two
- **Denominator / population:** Chapter 7 "Metrics that matter"
- **Comparison:** —
- **Task / setting:** operating an AI-core release
- **Source:** S2 Ch. 7 (verbatim list above)
- **Boundary:** these are things to monitor, not targets. **Fictional-case values must never appear in the metrics table as targets.**
- **TH sentence:** *(no total)* — บทนี้ระบุตัวชี้วัดที่ต้องติดตาม ตั้งแต่ Mediated-path Coverage จนถึงความถูกต้องของ Authoritative Post-state
- **EN sentence:** *(no total)* — the chapter names the quantities to monitor, from mediated-path coverage through authoritative post-state accuracy.

---

### NC-8 — Eight failure patterns
- **Value / unit:** 8 · failure patterns
- **Denominator / population:** Chapter 7 "Failure patterns"
- **Comparison:** the spec's `metrics-failures` section highlights four of them (classifying by vendor, unversioned prompts, treating retrieval as a read contract, trusting natural-language tool requests). **Only the last three map onto the book's list**; "classifying by vendor" comes from the chapter's definition paragraph ("Classification belongs to a task, manifest, golden set, and threshold, not to a vendor, model family, or whole organization"), and "treating retrieval as a read contract" comes from the broken-OS-analogy paragraph — both are legitimate, but neither is in the eight-item list.
- **Task / setting:** —
- **Source:** S2 Ch. 7
- **Boundary:** —
- **TH sentence:** หนังสือระบุรูปแบบความล้มเหลวไว้แปดข้อ
- **EN sentence:** The chapter lists eight failure patterns.

---

### NC-9 — The r8 517-execution specimen *(available, NOT required by this post's spec)*
- **Value / unit:** 517 · deterministic executions
- **Denominator / population:** one fixed suite in an author-constructed fixture. Within it: 30 of 30 benign cases completed; 0 of 40 policy escapes allowed; 0 of 6 prohibited refund effects allowed; 70 of 70 route traces recorded. Adaptive-to-implementation tests: 8 of 12 violating candidates released (soft-control limit), 4 of 4 prohibited effect attempts blocked by hard execution mediation.
- **Comparison:** full envelope vs adaptive attack, on the same fixture
- **Task / setting:** the r8 paper's bounded authored specimen — this material sits in **Chapter 8**, not Chapter 7, and belongs to post **#12**
- **Source:** S1 via S2 (Ch. 8, printed p. 35)
- **Boundary — MANDATORY, must appear in the same paragraph as any of these numbers:** "This illustrates wiring and failure localization in author-constructed fixtures. It does not establish production quality, independent red-team robustness, legal compliance, or a population safety rate." — and D.3's own line, "the specimen demonstrates mechanisms under declared tests; it is not a production prevalence estimate or universal benchmark."
- **TH sentence (if used):** งาน r8 มี Specimen ที่จำกัดขอบเขตชัด เป็นการรัน Deterministic 517 ครั้ง … ผลนี้แสดงการเชื่อม Control และตำแหน่ง Failure ใน Fixture ที่ผู้เขียนสร้าง ไม่ได้พิสูจน์ Production Quality, Independent Red Team, Legal Compliance หรือ Population Safety Rate
- **EN sentence (if used):** The r8 paper includes a deliberately bounded authored specimen of 517 deterministic executions … it illustrates wiring and failure localization in author-constructed fixtures; it does not establish production quality, independent red-team robustness, legal compliance, or a population safety rate.
- **Citation rule:** attribute to "an unpublished, author-supplied paper (no public URL)". **Never link it.**

---

## Dated statuses

Each of these is one dated sentence. Only DS-1 is load-bearing for this post; DS-2 to DS-5 are verification records.

- **DS-1 (NIST AI 600-1).** As of **5 September 2026**, NIST AI 600-1 remains the current published Generative AI Profile: dated **26 July 2024**, DOI `10.6028/NIST.AI.600-1` resolving to the live PDF, no revision, errata, withdrawal or supersession noted on the NIST publication page (page last updated 8 April 2026).
- **DS-2 (Saltzer & Schroeder DOI).** As of **5 September 2026**, DOI `10.1109/PROC.1975.9939` resolves to the IEEE Xplore record for document 1451869; IEEE Xplore answers automated clients with HTTP 202 (bot challenge), so the bibliographic record was confirmed against the Crossref registry and the principle wording against the authors' MIT copy (HTTP 200).
- **DS-3 (Karpathy talk).** As of **5 September 2026**, "Software Is Changing (Again)" is live on the YC Startup Library and on YouTube as `LCEmiRjPEtQ`, published by Y Combinator on **18 June 2025** from a keynote delivered **17 June 2025** at AI Startup School, San Francisco; runtime 2,371 s (39 min 31 s).
- **DS-4 (Karpathy essay).** As of **5 September 2026**, "Software 2.0" is dated **11 November 2017** on Medium; `karpathy.medium.com` returns HTTP 403 to automated fetches (bot block, not removal), and the date and text were confirmed from an Internet Archive capture of the same URL.
- **DS-5 (masterclass id).** As of **5 September 2026**, YouTube id `n_IwUYevRZo` resolves to "AI Transformation: จากการใช้ AI สู่องค์กรที่เรียนรู้เร็วที่สุด | The Masterclass EP01" on the channel *The Foundation (th)* — verified, but **not cited by this post**.

**Re-checks that do NOT apply to post #11** (none of these is asserted anywhere in the spec, so none was fetched; if a later edit introduces one, it must be re-verified first): Thailand's dedicated AI law / ร่างพระราชบัญญัติปัญญาประดิษฐ์ (ETDA `law_ai`); EU AI Act application dates and any 2026 amendment; the NIST June 2026 monitor-and-update research item (book source [7]); Stanford AI Index 2026 economy figures; IEA 2026 energy figures; ISO/IEC 42001:2023 and ISO/IEC 42005:2025 status; ETDA guideline versions; PDPA / PDPC sub-regulations.

---

## Fictional values

Every value in this list is **illustrative and fictional**. The book states it outright: *"Values are illustrative, not universal thresholds."* Flag on first mention per track — `(กรณีสมมติจากหนังสือ)` / `(a fictional case from the playbook)` — and **never** let one appear in a metrics table as a target.

**Named fictional organisations (series-wide; keep the names exactly):** Aurora Assurance · Kiri Foods · HarborLight Retail · LannaBuild Engineering · **Luma Commerce Thailand** (the only one used in this post).

**`CX-REFUND-01` — the fictional Luma Commerce Thailand assistant. Every value below is fictional:**

| Value | Where it appears | Note |
|---|---|---|
| `CX-REFUND-01` | throughout Ch. 7 and Appendix B | the fictional use case id |
| `issue_refund(amount, reason)` | Ch. 7, Artifacts 1/4 | the fictional tool signature |
| **THB 2,000** | Artifact 1 preamble, Scope, Artifact 5 | the fictional guard ceiling ("one eligible refund no greater than THB 2,000") |
| **THB 1–2,000** | Artifact 4 Tools and controls | the fictional bound in the manifest |
| **240** sliced cases | Artifact 1 Ablation | the fictional golden-set size |
| **70%** | Artifact 1 Ablation | the fictional fallback-sufficiency threshold |
| **94.6%** (candidate) / **41.3%** (fallback) | Artifact 1 Ablation | the fictional removal-ablation result. The book itself labels these "illustrative result" |
| `CXGS-2026-09-v3` | Artifact 1 Ablation | the fictional golden-set id. **NB: Artifact 4 writes the same suite as `CXGS-v3`** — two different id forms in the book; do not silently normalise |
| `CX-REFUND-01.2026-09-rc4` / parent `2026-08-prod2` / change `CHG-4821` | Artifact 4 | fictional release ids |
| `luma/cx-core-2026-08-17` | Artifact 4 | the book calls it a "Fictional dated ID" in the cell itself |
| temperature 0 · max 900 tokens · commit `9f31c7a` · template `refund-chat-v12` | Artifact 4 | fictional |
| Corpus `TH-CX-2026-09-01` · ranker `rr-4.2` · top-k 6 · session schema v5 | Artifact 4 | fictional |
| `paytools-v7` · `cx-rails-v9` · output schema v6 | Artifact 4 | fictional |
| `CXRT-v5` · hidden `CXH-2026Q3` · adaptive `CXA-09` · faults `CXF-v4` | Artifact 4 | fictional |
| stages **5/25/50/100%** · **seven** functional sign-offs | Artifact 4 | fictional rollout figures |
| **VP Customer Operations** | Artifact 1 Decision | the fictional reclassification owner |

**Fictional values from OTHER chapters — do NOT import into this post:** THB 2,400 · THB 2,500 (the Ch. 8 over-limit proposal) · THB 1,850 · 18 min / 46 h · 80,000 letters. Post #11's only monetary figure is THB 2,000 (and the THB 1–2,000 manifest bound).

---

## Glossary check

Canonical Thai rendering used **verbatim on first mention**, English inline afterwards. Source: the plan's Appendix C list, cross-checked against the book's own Appendix C (entry numbers given).

| Coinage (EN) | Canonical TH | Book Appendix C | Drift to avoid |
|---|---|---|---|
| AI-core | **AI ที่เป็นแกนหลัก** | C.2 #12 | ❌ not "AI แกนกลาง". Note the book's *figure* uses "AI เป็นแกนกลาง" as artwork — prose must use ที่เป็นแกนหลัก |
| Task scope | **ขอบเขตชุดงาน** | C.2 #13 | — |
| Decision authority | **อำนาจตัดสินใจ** | C.2 #14 | — |
| Indispensability | **ความขาดไม่ได้** | C.2 #15 | ❌ not "ความจำเป็น" (which is what the Fig 8 axis gloss shows) |
| Consequence | **ระดับผลกระทบ** | C.2 #16 | — |
| Software 1.0, 2.0, 3.0 | **ซอฟต์แวร์ 1.0, 2.0 และ 3.0** | C.2 #17 | — |
| Runtime context | **บริบทขณะทำงาน** | C.2 #18 | — |
| Context as program | **บริบทในฐานะโปรแกรม** | C.2 #19 | — |
| Runtime-context manifest | **บัญชีรายการบริบทขณะทำงาน** | C.2 #20 | — |
| Proposal–effect separation | **การแยกข้อเสนอออกจากผลจริง** | C.2 #21 | — |
| Effect mediation | **การควบคุมก่อนเกิดผล** | C.2 #22 | — |
| Least agency | **อำนาจกระทำเท่าที่จำเป็น** | C.2 #23 | — |
| Five rails | **รางควบคุมห้าชั้น** | C.2 #24 | mentioned only as the manifest's "five-rail versions" field in this post |
| Provenance | **ที่มาของข้อมูลและผลลัพธ์** | C.2 #25 | — |
| Reconstructable trace | **ร่องรอยที่สร้างเหตุการณ์ย้อนกลับได้** | C.2 #26 | — |
| Assurance envelope | **กรอบการรับประกันรอบระบบ** | C.3 #27 | ❌ do not confuse with *assurance contract* = สัญญาการรับประกันเชิงระบบ (#28), which is post #12's term |
| Structural guarantee | **การรับประกันเชิงโครงสร้าง** | C.3 #30 | ❌ do not confuse with *semantic estimate* = ค่าประเมินเชิงความหมาย |
| Semantic estimate | **ค่าประเมินเชิงความหมาย** | C.3 | — |

**Kept in English inline, as the book does:** Workflow · Trace · Fallback · Threshold · Manifest · Escalation · Release · Rollback · Regression test · Prompt · Golden set · Canary · Retrieval · Override · Guard · Inventory. Chapter section labels in Thai: **หลักปฏิบัติห้าประการ · เวิร์กช็อป · ตัวชี้วัดสำคัญ · รูปแบบความล้มเหลว · คำถามสำหรับผู้นำ** and, inside artifacts, **วัตถุประสงค์ / ใช้เมื่อ / เจ้าของหลัก**.

**Deviations found:** one. The drawn Figure 8 glosses `INDISPENSABILITY` as **ความจำเป็น**, which is the exact drift the plan warns against; the prose must use **ความขาดไม่ได้**. The figure alt text in the manifest already uses ความขาดไม่ได้ — leave it alone.

---

## Do not assert

Things searched for and not verified, or verified to be false. If a draft contains one of these, the writer must drop it.

1. **Do not say Karpathy coined or used "Software 3.0" in the 2017 essay.** The essay text was read end to end from an archived capture: it contains **zero** occurrences of "Software 3.0". The term belongs to the 17 June 2025 talk (S6).
2. **Do not say the book cites Karpathy.** A grep of the whole 97-page PDF returns **no** occurrence of "Karpathy", and D.3 does not list him. The 1.0/2.0/3.0 attribution is this post's own addition, offered by the writer, not sourced from the playbook.
3. **Do not attribute the LLM-as-operating-system analogy to the book as an endorsement.** The book *offers it and breaks it* in the same sentence. If the talk is credited with the analogy, the break must follow immediately.
4. **Do not say the completed CX-REFUND-01 classification card has ten filled rows.** The blank card has 10 fields; the worked example is printed as 7 rows (NC-2).
5. **Do not say the worked manifest shows six rows.** It shows five; the book merges *Evaluation and trace* with *Operations and integrity* (NC-3).
6. **Do not give a total count for "Metrics that matter."** It is 14 or 15 depending on how "p50 and p95 latency" is counted (NC-7). Name the quantities; skip the total.
7. **Do not claim the manifest example carries `+07` timestamps.** The spec's Thai-box note mentions `+07`, but the book's Artifact 4 example contains **no** timezone offset — its locale markers are the corpus id `TH-CX-2026-09-01`, "Thailand web/mobile chat", "Thai/English" and the THB bound. Write the Thai box from those; if `+07` is wanted, present it as the writer's own recommendation, not as the book's.
8. **Do not treat `CXGS-2026-09-v3` and `CXGS-v3` as an error to be tidied.** They are the book's two renderings of the same fictional suite in two artifacts. Quote whichever artifact you are quoting.
9. **Do not present the AI-core 2×2, the four-layer architecture or the manifest as a standard, a certification scheme, or industry consensus.** They are one author's synthesis (S1), redrawn for this series.
10. **Do not present NIST AI 600-1 as a requirement.** It is a voluntary cross-sectoral profile; its own boundary is that organisations must select and tailor the actions.
11. **Do not cite "13 risks and 400+ actions" for NIST AI 600-1.** That phrasing appears in secondary coverage; the published §2 is numbered 2.1–2.12 (NC-1).
12. **Do not link the r8 paper, and do not paraphrase away its boundary.** No URL, no DOI, no repository. If any 517-specimen number appears, the boundary sentence appears in the same paragraph (NC-9).
13. **Do not claim IEEE Xplore serves the Saltzer & Schroeder paper openly.** The DOI resolves; the Xplore page answers automated clients with 202 and the full text is paywalled. Cite the DOI, not a mirror.
14. **Do not assert any legal or regulatory status in this post** — Thai, EU or otherwise. Nothing of the kind was verified for post #11 (see "Re-checks that do NOT apply").
15. **Do not quote the masterclass or cite a timestamp.** The video id is verified live, but this post has no masterclass claim; paraphrase-only remains the standing rule if that ever changes.
16. **Do not give the playbook a public URL.** None was verified on 2026-09-05.
17. **Do not move any fictional value into the metrics table as a target** — 94.6%, 41.3%, 70%, 240 and THB 2,000 are illustrative only, by the book's own words.
