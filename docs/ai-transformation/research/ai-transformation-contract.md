# Research ledger — post #12 `ai-transformation-contract`

**Post:** "Assurance Contract — เขียนสัญญาเป็นรายคุณสมบัติ" / "The Assurance Contract — Stop Saying \"Safe and Trustworthy\"; Commit Per Property"
**Group:** Engineer · **Layer:** Spine · **Question:** Q5 · **read_min:** 17 (TH track target ≈ 24,650 chars at 1,450 chars/min)
**Book chapter:** Ch. 8 "Write assurance contracts and build five rails" / "บทที่ 8 เขียนสัญญารับรองและสร้างห้า Control Rail" — printed pp. 33–37 (PDF 34–38) + Appendix B **Artifact 2** printed pp. 69–70 (PDF 70–71).
**Research date / access date for every source below:** **2026-09-05** (Asia/Bangkok).
**Book evidence cutoff (the book's own):** 5 September 2026 (Asia/Bangkok) — D.2.

> **Binding rule for writers:** no number, date, quotation, framework attribution or URL may appear in the post unless it appears in this ledger. If you need something that is not here, stop and ask for a ledger amendment.

---

## 1. Claim classes in this post

| Class | Instances in this post | How it must be handled |
|---|---|---|
| **Material number** | The r8 specimen counts only: 517 / 30-of-30 / 0-of-40 / 0-of-6 / 70-of-70 / 8-of-12 / 4-of-4 | Number card required (§3). Every one is paired with the book's boundary sentence, and the r8 paper is **never linked**. |
| **Dated legal/standard status** | ISO/IEC 42005:2025 publication status; NIST AI 600-1 publication date; (context only) Thailand's dedicated AI law | One dated sentence each (§4). |
| **Study finding** | **None.** This post cites no empirical study. NIST AI 600-1 is a Standard/guidance document, not a study. | — |
| **Direct quotation** | The book's own English/Thai sentences (Ch. 8 + Artifact 2), quoted as the book's wording; NIST AI 600-1 passages quoted verbatim | Quote exactly; attribute to the book or to NIST. **The masterclass video is never quoted** (and is not cited in this post at all). |
| **Framework attribution** | Three control classes (Hard enforcement / Soft detection / Governance) = book, author synthesis; eight contract elements = book Artifact 2; seven contract rows = book Artifact 2; five rails = book Ch. 8 (detail belongs to #13); NIST AI RMF GenAI Profile = NIST; AI system impact assessment = ISO/IEC 42005:2025 | Never describe NIST, ISO and the book's framework as equivalent (fact-check W3). The book's contract structure is **author synthesis** from the r8 paper, not a standard. |
| **Fictional-case value** | Every CX-REFUND-01 number, and the Artifact 2 "contracted example" column in full | Flag `(กรณีสมมติจากหนังสือ)` / `(a fictional case from the playbook)` on first mention; never place in a metrics table as a target (§5). |

---

## Sources

Access date for all rows: **2026-09-05**. Labels follow the plan's four-label scheme (`Law` · `Standard` · `Study` · `Synthesis`), which is the book's D.1 policy re-cut.

| [N] | Label | Title | URL | Publisher | Pub date | Accessed | Supports |
|---|---|---|---|---|---|---|---|
| **[1]** | Synthesis | Mingkhwan, Anirach. *Engineering AI-Core Systems: A Reference Architecture and Assurance Contract for Software 3.0*, revision 8 | **none — author-supplied, unpublished; NEVER link** | — (author-supplied paper attached to the playbook project) | September 2026 | 2026-09-05 | The assurance-contract structure, the three control classes, the CX-REFUND-01 worked example, and the 517-run deterministic specimen. |
| **[2]** | Synthesis | Mingkhwan, Anirach. *AI Transformation as an Organizational Core — Bilingual Companion Playbook*, Ch. 8 + Appendix B Artifact 2 | local source PDF (`UserGiven/AI_Transformation_as_an_Organizational_Core_Bilingual_Playbook.pdf`); no public URL at time of writing | — | evidence cutoff 5 September 2026 | 2026-09-05 | All chapter wording quoted in this post: the never-claim-safe sentence, the three control classes, the four gaps, the eight contract elements, the seven rows, the metrics list, the failure-pattern list, the five operating principles, and both Thai mirrors. |
| **[3]** | Standard | NIST. *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*, NIST AI 600-1 | `https://doi.org/10.6028/NIST.AI.600-1` → `https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf` | National Institute of Standards and Technology, U.S. Department of Commerce | **July 2024** (approved by the NIST Editorial Review Board 2024-07-25) | 2026-09-05 | GenAI risk identification/measurement actions behind the semantic rows: minimum performance/assurance thresholds at a go/no-go gate; measuring false positives and false negatives; documented limits of pre-deployment testing; deactivation and incident-escalation procedures behind the governance class. |
| **[4]** | Standard | ISO/IEC. *ISO/IEC 42005:2025 — Information technology — Artificial intelligence (AI) — AI system impact assessment* | `https://www.iso.org/standard/42005` (publisher canonical, human-facing) · verification corroborated on the IEC co-publisher page `https://webstore.iec.ch/en/publication/107659` | International Organization for Standardization / International Electrotechnical Commission | **28 May 2025**, edition 1, 39 pp. | 2026-09-05 | Impact assessment as a lifecycle input to residual-risk rows: identifying effects on individuals, groups and societies from an AI system *and its foreseeable applications*, when in the lifecycle to assess, and how the assessment integrates with AI risk management and an AI management system. |
| **[5]** | Law | Kingdom of Thailand. *Personal Data Protection Act B.E. 2562 (2019)* | `https://ratchakitcha.soc.go.th/documents/17082307.pdf` | Royal Gazette (ราชกิจจานุเบกษา) | B.E. 2562 (2019), Vol. 136 | 2026-09-05 | **Conditional — cite only if §6's Thai box names PDPA.** Continued applicability of lawful personal-data processing, data-subject rights, safeguards, and controller/processor duties to AI use. |

### Verification notes (read before the fact-check pass)

- **[3] NIST AI 600-1 — VERIFIED.** `https://doi.org/10.6028/NIST.AI.600-1` returns `HTTP/2 302` with `location: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf`; a GET on that target returns **HTTP 200, `content-type: application/pdf`** on the canonical NIST domain (`nvlpubs.nist.gov`). The PDF's own cover confirms the title, "NIST Trustworthy and Responsible AI / NIST AI 600-1", and **July 2024**. Note for anyone re-checking: a bare `HEAD` on the nvlpubs URL returns 404 while `GET` returns 200 — this is an nvlpubs quirk, not a dead link. Either the DOI or the nvlpubs PDF is a correct `href`; **prefer the DOI**, as the book's D.3 does.
- **[4] ISO/IEC 42005:2025 — VERIFIED, but not directly.** `https://www.iso.org/standard/42005` and `.../42005.html` return **HTTP 403** to every automated client tried (WebFetch, curl with full browser headers, Firecrawl) — iso.org bot-blocks; the page is live in a normal browser and is returned by search with the exact 2025 title. Verification was therefore completed on the **co-publisher** domain: `https://webstore.iec.ch/en/publication/107659` returns **HTTP 200** and gives designation, full title, **publication date 28 May 2025**, edition 1.0, status Published, 39 pages, and the scope paragraph. IEC is the "IEC" of ISO/IEC — a canonical publisher, not a reseller or look-alike. **Do not record this as a dead link.**
- **[5] PDPA — VERIFIED.** `https://ratchakitcha.soc.go.th/documents/17082307.pdf` returns **HTTP 200, `application/pdf`**.
- **[1] r8 — UNVERIFIABLE BY DESIGN, and that is the correct state.** Author-supplied, unpublished, no public URL. Cite as "author-supplied paper, unpublished (no public URL)"; the reference `<li>` carries **no `<a>`**. Book D.3: *"The first source is an unpublished, author-supplied paper and therefore has no public URL; it is identified transparently rather than assigned an invented link."*
- **Masterclass video** (book ref [2], id `n_IwUYevRZo`): the id resolves to a live YouTube page whose title matches the book's citation, *"AI Transformation: จากการใช้ AI สู่องค์กรที่เรียนรู้เร็วที่สุด | The Masterclass EP01"*. **It is not a source for this post** — do not cite it, do not paraphrase it, do not cite a timestamp. Recorded here only to close the protocol item.

### Verbatim support passages

**[3] NIST AI 600-1**, quotable verbatim:

- Identity: *"This document is a cross-sectoral profile of and companion resource for the AI Risk Management Framework (AI RMF 1.0) for Generative AI… The AI RMF was released in January 2023, and is intended for **voluntary** use…"* (§1 Introduction; emphasis added for the writer's benefit — do not bold it in the post).
- Behind the **semantic** rows — thresholds at a gate: **GV-1.3-002** *"Establish minimum thresholds for performance or assurance criteria and review as part of deployment approval ('go'/'no-go') policies, procedures, and processes, with reviewed processes and approval thresholds reflecting measurement of GAI capabilities and risks."*
- Behind the **semantic** rows — false accepts/rejects are a measured quantity: **MS-2.7-005** *"…Evaluate the rate of false positives and false negatives in content provenance, as well as true positives and true negatives for verification."*
- Behind "a fixed threshold does not make a fallible score true" — NIST's own measurement caveat: *"Measurement gaps can arise from mismatches between laboratory and real-world settings. Current testing approaches often remain focused on laboratory conditions or restricted to benchmark test datasets and in silico techniques that may not extrapolate well to—or directly assess GAI impacts in real-world conditions."* And: *"Challenges with risk estimation are aggravated by a lack of visibility into GAI training data, and the generally immature state of the science of AI measurement and safety today."*
- Behind the **governance** class (approval, rollback, incident response): **MG-2.4-002** *"Establish and maintain procedures for escalating GAI system incidents to the organizational risk management authority when specific criteria for deactivation or disengagement is met…"*; **MG-2.4-004** *"Establish and regularly review specific criteria that warrants the deactivation of GAI systems in accordance with set risk tolerances and appetites."*
- Tailoring caveat (the book's Boundary line, in NIST's own words): *"Organizations may choose to tailor how they measure GAI risks based on these characteristics."*

**[4] ISO/IEC 42005:2025**, scope as published by IEC: *"This document provides guidance for organizations performing artificial intelligence (AI) system impact assessments for individuals and societies that can be affected by an AI system and its foreseeable applications."* It further covers how and when to conduct assessments across the AI system life cycle, assessment documentation, and integration with the organization's AI risk management and AI management system; it applies to organizations of any size, type or nature that develop, provide or use AI systems.

**[2] The book — Ch. 8, verbatim (English), the spine of this post:**

> An assurance contract states, for each property, the assumptions, obligation, guarantee or estimate, evidence, owner, threshold, and response to change or breach. It should never claim that the whole AI system is safe. It should say narrowly what can be enforced, what can only be estimated, and what residual risk remains.

> Keep three control classes distinct. **Hard enforcement** creates structural invariants such as authorized tools, valid parameters, transaction limits, and schema-conforming payloads, provided every path is mediated and implementation is correct. **Soft detection** estimates semantic properties such as injection, faithfulness, relevance, privacy, and policy alignment. Its verdicts have false accepts and false rejects on a stated population. **Governance** supplies approval, trace retention, audit, rollback, and incident response. It creates accountability and recovery, but cannot make an individual answer correct.

> The five rails place these controls at different seams. The input rail handles the user turn. The dialog rail governs multi-turn policy and permitted state transitions. The retrieval rail enforces source membership while estimating relevance and support. The execution rail authorizes and bounds every tool effect. The output rail enforces structure and estimates semantic quality before release. Trace retention spans them all. **No rail covers everything. An input filter misses malicious retrieved content. An approved source can be poisoned. An authorized call can oppose user intent. An output filter cannot recall data exposed by an earlier tool.**

> For CX-REFUND-01, the contract can structurally guarantee that a refund routed through the execution guard will not exceed 2,000 baht or execute without an authenticated approval token. It cannot guarantee that every eligibility explanation is correct. Faithfulness must be measured on labeled policy cases, and evaluator error reported at the operating threshold. If the model proposes 2,500 baht, the guard rejects and creates an escalation trace even if the explanation sounds plausible.

**[2] The book — Ch. 8, verbatim (Thai mirror), for the TH track.** (pdftotext renders `เป็น` as `เป็ น`; the stray space is a rendering artifact — normalise it.)

> Assurance Contract เปลี่ยนความมั่นใจให้เป็นภาระที่ทดสอบและระบุผู้รับผิดชอบได้ สำหรับแต่ละคุณสมบัติ ต้องระบุสมมติฐาน ภาระ สิ่งที่รับรองหรือประเมินได้ หลักฐาน เจ้าของ Threshold และวิธีตอบสนองเมื่อเปลี่ยนแปลงหรือผิดเงื่อนไข ไม่ควรกล่าวกว้างว่าทั้งระบบ Safe แต่ต้องบอกว่าอะไรบังคับได้ อะไรเป็นเพียงค่าประเมิน และเหลือความเสี่ยงอะไร

> แยกการควบคุมสามประเภท **Hard Enforcement** สร้างกฎโครงสร้าง เช่น Tool ที่อนุญาต Parameter ที่ถูกต้อง วงเงิน และ Payload ตาม Schema โดยต้องมี Complete Mediation และ Implementation ที่ถูกต้อง **Soft Detection** ประเมิน Injection, Faithfulness, Relevance, Privacy และ Policy Alignment จึงมี False Accept และ False Reject บนประชากรที่ระบุ **Governance** ครอบคลุม Approval, Trace Retention, Audit, Rollback และ Incident Response ทำให้ตรวจสอบและกู้คืนได้ แต่ไม่ได้ทำให้คำตอบแต่ละรายการถูกต้อง

> แนวควบคุมห้าชั้นวางกลไกตาม Seam Input Rail ตรวจคำขอ Dialog Rail ตรวจ Policy และ State Transition Retrieval Rail บังคับ Source Membership พร้อมประเมิน Relevance และ Support Execution Rail ตรวจสิทธิ์และขอบเขต Tool Effect Output Rail บังคับโครงสร้างและประเมินความหมายก่อน Release ส่วน Trace พาดผ่านทั้งหมด **ไม่มี Rail ใดครอบคลุมทุกเรื่อง Input Filter มองไม่เห็นคำสั่งอันตรายจาก Retrieval แหล่งอนุมัติอาจปนเปื้อน Tool Call ที่มีสิทธิ์อาจผิดเจตนา และ Output Filter เรียกข้อมูลที่ Tool เปิดเผยไปแล้วกลับคืนไม่ได้**

> สำหรับ CX-REFUND-01 Contract สามารถรับรองเชิงโครงสร้างว่า Refund ที่ผ่าน Guard จะไม่เกิน 2,000 บาทและไม่ทำงานหากไม่มี Approval Token แต่รับรองความถูกต้องของคำอธิบายสิทธิ์ทุกครั้งไม่ได้ Faithfulness ต้องวัดจากกรณีติดป้ายและรายงาน Evaluator Error ณ Threshold จริง หากโมเดลเสนอ 2,500 บาท Guard ต้องปฏิเสธและสร้าง Escalation Trace แม้คำอธิบายฟังน่าเชื่อถือ

**[2] The book — Artifact 2 (printed p. 69–70), verbatim.**

*Purpose (EN):* "Replace 'safe and trustworthy' with property-specific commitments covering assumptions, obligation, claim, evidence, owner, threshold, change, and breach. **Use when** approving an AI-core release, provider, service boundary, or residual risk. **Accountable owner** Release owner maintains the integrated contract; each row has one answerable property owner."

*วัตถุประสงค์ (TH):* "แทนคำกว้างว่า “ปลอดภัยและน่าเชื่อถือ” ด้วยภาระรายคุณสมบัติที่ระบุสมมติฐาน กลไก ข้ออ้าง หลักฐาน เจ้าของ Threshold การเปลี่ยน และการตอบสนอง **ใช้เมื่อ** อนุมัติ AI-core Release ผู้ให้บริการ Service Boundary หรือ Residual Risk **เจ้าของหลัก** Release Owner ดูแลสัญญารวม แต่ละแถวมี Property Owner หนึ่งราย"

*The seven rows and their claim types (column headers: Property | Assumptions, mechanism, claim type | Evidence, population, threshold | Owner and breach response; TH: คุณสมบัติ | สมมติฐาน กลไก และประเภทข้ออ้าง | หลักฐาน ประชากร และ Threshold | เจ้าของและการตอบสนอง):*

| # | Property (EN) | คุณสมบัติ (TH, book's own row label) | Claim type (book's wording) |
|---|---|---|---|
| 1 | Authorized effects | Effect ได้รับอนุญาต | Structural |
| 2 | Output structure | โครงสร้าง Output | Structural |
| 3 | Task correctness by slice | Task Correctness แยกกลุ่ม | Semantic |
| 4 | Faithfulness and relevance | Faithfulness และ Relevance | Semantic |
| 5 | Injection containment | Injection | Structural effect bound plus semantic detection / Structural Effect Bound และ Semantic Detection |
| 6 | Change control | Change Control | Structural |
| 7 | Trace completeness | ความครบถ้วนของ Trace | Structural record plus governance / Structural Record และ Governance |

*The two instruction sentences under the table (EN, verbatim — §3's anchor):* "For semantic rows, state population, threshold, false accepts, false rejects and weak slices. **A fixed threshold does not make a fallible score true.** For structural rows, state mediation, validator, identity, bypass and logging assumptions."

*(TH, verbatim):* "แถว Semantic ต้องระบุ Population, Threshold, False Accept, False Reject และกลุ่มที่หลักฐานอ่อน กฎตายตัวไม่ได้ทำให้คะแนนที่ผิดกลายเป็นจริง ส่วนแถว Structural ต้องระบุสมมติฐานเรื่อง Mediation, Validator, Identity, ทางเลี่ยง และ Logging"

**[2] The book — Ch. 8 five operating principles (quote exactly ONE in the 💡 blockquote; list the rest in prose).**

| # | EN (verbatim) | TH (verbatim) |
|---|---|---|
| 1 | **State claims property by property** Separate guarantees estimates and governance duties. | **ระบุ Claim ทีละคุณสมบัติ** แยก Guarantee, Estimate และ Governance Duty |
| 2 | **Put hard controls at release and effect boundaries** Complete mediation is a prerequisite. | **วาง Hard Control ที่ Release และ Effect Boundary** Complete Mediation เป็นเงื่อนไขก่อนรับรอง |
| 3 | **Calibrate semantic gates** Report threshold population false accepts false rejects and correlated failure. | **สอบเทียบ Semantic Gate** รายงาน Threshold ประชากร False Accept, False Reject และความล้มเหลวสัมพันธ์กัน |
| 4 | **Inspect state and traces** Model narration is not evidence that an effect occurred correctly. | **ตรวจ State และ Trace** คำบรรยายของโมเดลไม่ใช่หลักฐานว่า Effect ถูกต้อง |
| 5 | **Test beyond the visible suite** Combine fixed hidden adaptive stateful failure and live evidence. | **ทดสอบไกลกว่าชุดที่มองเห็น** ใช้ Fixed, Hidden, Adaptive, Stateful, Failure และ Live Evidence |

**[2] Working session / เวิร์กช็อป — "Contract and attack tabletop" (§the working-session agenda, verbatim, five steps).**

EN: "Select a benign request, unsupported policy claim, injected passage, over-limit proposal, and trace-write failure. For each, complete a contract row and walk the five rails. Identify hard invariant, soft signal, threshold, route, evidence, owner, residual risk, and breach response. Agree which failures block release and which require human escalation."

TH: "เลือกคำขอปกติ Claim ไร้หลักฐาน Passage ที่มี Injection Proposal เกินวงเงิน และ Trace-write Failure สำหรับแต่ละกรณี กรอก Contract Row และเดินห้า Rail ระบุ Hard Invariant, Soft Signal, Threshold, Route, Evidence, Owner, Residual Risk และ Breach Response ตกลงว่า Failure ใดบล็อก Release และใด Escalate"

**[2] Metrics that matter / ตัวชี้วัดสำคัญ (verbatim — the eleven items in the book's own order).**

EN: "Track benign task success, policy escape, prohibited-effect escape, false accepts and false rejects, post-state correctness, trace completeness, escalation load, rollback time, incident recurrence, latency, tokens, and cost by consequence class. **Never collapse utility and security into one score.**"

TH: "ติดตาม Benign Task Success, Policy Escape, Prohibited-effect Escape, False Accept, False Reject, Post-state Correctness, Trace Completeness, Escalation Load, Rollback Time, Incident Recurrence, Latency, Token และ Cost แยกตาม Consequence Class **ห้ามรวม Utility กับ Security เป็นคะแนนเดียวจนซ่อน Tradeoff**"

**[2] Failure patterns / รูปแบบความล้มเหลว (verbatim — the eight patterns).**

EN: "Treating a threshold as deterministic truth, assuming stacked judges are independent, claiming zero risk after no fixed-suite failures, placing all protection at output, approving narration instead of state, writing traces after release, suppressing escalation to improve automation, and granting autonomous irreversible effects because semantic scores are high."

TH: "ถือ Threshold เป็นความจริง Deterministic สมมติ Judge หลายตัวเป็นอิสระ อ้าง Zero Risk เพราะ Fixed Suite ไม่พบ วางการป้องกันทั้งหมดที่ Output เชื่อ Narration แทน State เขียน Trace หลัง Release กด Escalation เพื่อให้ Automation ดูดี และยอม Autonomous Irreversible Effect เพราะ Semantic Score สูง"

> **Spec-vs-book note.** The spec's §7 failure list ("adjectives instead of properties, one threshold for all slices, calling an estimate a guarantee, unowned rows") is an **editorial re-cut** aimed at the contract, not the book's eight patterns. Both are legitimate; the writer must not present the re-cut as the book's list. Safest: give the book's eight verbatim, then add the spec's four as "และในทางปฏิบัติของสัญญาเอง…" / "and, in contract-writing practice…", clearly the author's own framing.
>
> **Chapter 8 has no "คำถามสำหรับผู้นำ" section.** Do not invent one.

---

## Number cards

Every card below is an **r8 specimen** number. All seven share one boundary sentence and one attribution rule.

**The single boundary sentence (the book's own, verbatim) that must accompany the 517-specimen numbers, in every place they appear:**

- **EN:** "This illustrates wiring and failure localization in author-constructed fixtures. It does not establish production quality, independent red-team robustness, legal compliance, or a population safety rate."
- **TH:** "ผลนี้แสดงการเชื่อม Control และตำแหน่ง Failure ใน Fixture ที่ผู้เขียนสร้าง ไม่ได้พิสูจน์ Production Quality, Independent Red Team, Legal Compliance หรือ Population Safety Rate"
- The book's D.3 [1] boundary, available as an alternative or an addition: "the specimen demonstrates mechanisms under declared tests; it is not a production prevalence estimate or universal benchmark."

**Attribution rule for all seven:** source is [1] (author-supplied, unpublished, **no link**), reported through [2]. Superscript `[1]` in prose; the `<li id="…-ref-1">` carries no `<a>`.

---

### Card N1 — 517 deterministic executions

- **Value / unit:** 517 · executions (runs)
- **Denominator / population:** the whole authored specimen in the r8 paper; the run count *is* the population, not a sample from a larger one.
- **Comparison:** none. There is no baseline system and no control arm. **Do not write "compared with…".**
- **Task / setting:** deterministic executions in author-constructed fixtures, refund-handling domain (CX-REFUND-01), fixed + adaptive test suites.
- **Source:** [1] via [2] Ch. 8 (printed p. 35).
- **Boundary line:** as above.
- **TH sentence as it will appear:** "งาน r8 มี specimen ที่จำกัดขอบเขตชัดเจน — การรัน deterministic 517 ครั้งที่ผู้เขียนสร้างขึ้นเอง"
- **EN sentence as it will appear:** "The r8 paper includes a deliberately bounded authored specimen of 517 deterministic executions."

### Card N2 — 30 of 30 benign cases completed (fixed suite, full envelope)

- **Value / unit:** 30/30 · cases completed (100% of that fixture)
- **Denominator / population:** the 30 benign cases in the r8 **fixed suite**, run with the **full assurance envelope** engaged.
- **Comparison:** the paper's contrast is full envelope vs. the adaptive-test condition (Cards N6–N7), not vs. an unguarded baseline. State it that way or not at all.
- **Task / setting:** benign (non-adversarial) refund requests, fixed suite.
- **Source:** [1] via [2] p. 35. **Boundary line:** as above.
- **TH:** "ใน fixed suite ระบบที่มี envelope เต็มรูปแบบทำงานปกติผ่าน 30 จาก 30 กรณี"
- **EN:** "In its fixed suite, the full envelope completed 30 of 30 benign cases."

### Card N3 — zero of 40 policy escapes

- **Value / unit:** 0/40 · policy escapes allowed
- **Denominator / population:** 40 policy-escape attempts in the r8 fixed suite.
- **Comparison:** none stated. A zero in a fixed suite is explicitly **not** evidence of zero risk — the book lists "claiming zero risk after no fixed-suite failures" as a failure pattern. Pair this number with that sentence.
- **Task / setting:** fixed suite, full envelope.
- **Source:** [1] via [2] p. 35. **Boundary line:** as above, **plus** the failure-pattern caveat.
- **TH:** "และปล่อย policy escape ศูนย์จาก 40 ครั้ง"
- **EN:** "…allowed zero of 40 policy escapes."

### Card N4 — zero of six prohibited refund effects

- **Value / unit:** 0/6 · prohibited refund effects allowed
- **Denominator / population:** six prohibited-refund-effect attempts, fixed suite.
- **Comparison:** none. Same fixed-suite caveat as N3.
- **Task / setting:** fixed suite, full envelope.
- **Source:** [1] via [2] p. 35. **Boundary line:** as above.
- **TH:** "และ prohibited refund effect ศูนย์จาก 6 ครั้ง"
- **EN:** "…and zero of six prohibited refund effects."

### Card N5 — 70 of 70 route traces recorded

- **Value / unit:** 70/70 · route traces recorded
- **Denominator / population:** 70 routes exercised in the fixed suite.
- **Comparison:** none.
- **Task / setting:** fixed suite; trace completeness is the row-7 property.
- **Source:** [1] via [2] p. 35. **Boundary line:** as above.
- **TH:** "และบันทึก route trace ครบ 70 จาก 70"
- **EN:** "…and recorded 70 of 70 route traces."

### Card N6 — eight of twelve violating candidates released (adaptive tests)

- **Value / unit:** 8/12 · violating candidates released (i.e. **soft detection failed** two-thirds of the time)
- **Denominator / population:** 12 violating candidates under **adaptive-to-implementation** tests — attacks adapted to the specific implementation, not the fixed suite.
- **Comparison:** the load-bearing comparison of the whole post — **against Card N7**, the same condition where hard mediation held. This pair is the evidence for "structural guarantee ≠ semantic estimate". Never report N6 without N7, or N7 without N6.
- **Task / setting:** adaptive-to-implementation attack tests, author-constructed fixtures.
- **Source:** [1] via [2] p. 35 (printed p. 36 top). **Boundary line:** as above.
- **TH:** "แต่ adaptive test เปิดข้อจำกัดของ soft control — violating candidate หลุดออกไป 8 จาก 12"
- **EN:** "Adaptive-to-implementation tests exposed soft-control limits: eight of twelve violating candidates were released."

### Card N7 — hard execution mediation blocked all four prohibited-effect attempts

- **Value / unit:** 4/4 · prohibited effect attempts blocked
- **Denominator / population:** four prohibited-effect attempts in the same adaptive condition as N6.
- **Comparison:** **against Card N6** (see above). Four is a very small denominator — say so.
- **Task / setting:** adaptive-to-implementation attack tests; hard execution mediation at the effect boundary.
- **Source:** [1] via [2] p. 35 (printed p. 36 top). **Boundary line:** as above; four attempts cannot support a rate claim of any kind.
- **TH:** "ขณะที่ hard execution mediation บล็อก prohibited effect ได้ทั้ง 4 ครั้ง — ฐานเพียงสี่ครั้ง จึงเป็นภาพประกอบกลไก ไม่ใช่อัตราความปลอดภัย"
- **EN:** "…while hard execution mediation blocked all four prohibited effect attempts — four attempts is an illustration of a mechanism, not a safety rate."

---

## Dated statuses

Each is one dated sentence. Use them as written, or paraphrase without changing the date or the qualifier.

1. **ISO/IEC 42005:2025 — APPLIES TO THIS POST (§6 Thai box).**
   **EN:** "ISO/IEC 42005:2025, *Information technology — Artificial intelligence (AI) — AI system impact assessment*, was published on 28 May 2025 (edition 1) and, as verified on 5 September 2026, remains the current published edition; it is voluntary guidance on assessing an AI system's effects on individuals and societies, not a certifiable requirement."
   **TH:** "ISO/IEC 42005:2025 ว่าด้วยการประเมินผลกระทบของระบบ AI เผยแพร่เมื่อ 28 พฤษภาคม 2568 (ฉบับที่ 1) และ ณ วันที่ตรวจสอบ 5 กันยายน 2569 ยังเป็นฉบับปัจจุบัน — เป็นแนวปฏิบัติโดยสมัครใจ ไม่ใช่ข้อกำหนดที่ใช้รับรอง"
   *Book's Boundary to keep:* "the public summary guides orientation; practitioners should obtain the standard and qualified advice for conformity work."

2. **NIST AI 600-1 — APPLIES TO THIS POST (§3, §7).**
   **EN:** "NIST AI 600-1, the Generative AI Profile of the AI Risk Management Framework, was published in July 2024 and, as verified on 5 September 2026, is still the current version; it is a voluntary companion profile whose suggested actions organizations must select and tailor to their own use case and risk tolerance."
   **TH:** "NIST AI 600-1 ซึ่งเป็น Generative AI Profile ของ AI Risk Management Framework เผยแพร่เมื่อกรกฎาคม 2567 และ ณ 5 กันยายน 2569 ยังเป็นฉบับปัจจุบัน — เป็นเอกสารประกอบโดยสมัครใจ องค์กรต้องเลือกและปรับ suggested action ให้เข้ากับ use case และระดับความเสี่ยงที่ยอมรับได้ของตนเอง"

3. **Thailand's dedicated AI law — CONTEXT ONLY; DO NOT ASSERT A STATUS CHANGE.**
   Checked as required by the protocol even though this post makes no Thailand-AI-law claim. ETDA's `law_ai` page (`https://www.etda.or.th/th/pr-news/law_ai.aspx`, fetched 2026-09-05, HTTP 200) is **dated 11 June 2025** and announces a public consultation on the *(ร่าง) หลักการของกฎหมายว่าด้วยปัญญาประดิษฐ์* — a draft **set of principles**, not a bill in force. A Thai-language web search on 2026-09-05 for *ร่างพระราชบัญญัติ ปัญญาประดิษฐ์* surfaced only press coverage of that same consultation round; **no source found on 2026-09-05 shows a dedicated Thai AI act enacted or in parliament.** The book's own D.2 line therefore still holds and is the safe form to reproduce:
   **EN:** "As of the playbook's 5 September 2026 cutoff — and re-checked on 5 September 2026 — Thailand's dedicated AI legislation remained under development; that does not remove duties under the Personal Data Protection Act, consumer protection, employment, intellectual-property, cybersecurity, sector rules, or contracts."
   **TH:** "ณ วันตัดข้อมูลของหนังสือ 5 กันยายน 2569 — และตรวจซ้ำเมื่อ 5 กันยายน 2569 — กฎหมายเฉพาะด้าน AI ของไทยยังอยู่ระหว่างการพัฒนา ซึ่งไม่ได้ยกเลิกหน้าที่ตาม PDPA กฎหมายผู้บริโภค แรงงาน ทรัพย์สินทางปัญญา ความมั่นคงปลอดภัยไซเบอร์ กฎเฉพาะอุตสาหกรรม และสัญญาที่เกี่ยวข้อง"

4. **PDPA — CONDITIONAL (only if §6's Thai box names it).**
   **EN:** "Thailand's Personal Data Protection Act B.E. 2562 (2019) remains in force as of 5 September 2026 and continues to govern lawful basis, data-subject rights, safeguards and controller/processor duties wherever an AI system processes personal data."
   **TH:** "พระราชบัญญัติคุ้มครองข้อมูลส่วนบุคคล พ.ศ. 2562 ยังมีผลบังคับใช้ ณ 5 กันยายน 2569 และยังคุมฐานการประมวลผล สิทธิของเจ้าของข้อมูล มาตรการคุ้มครอง และหน้าที่ของผู้ควบคุม/ผู้ประมวลผลข้อมูล ทุกครั้งที่ระบบ AI ประมวลผลข้อมูลส่วนบุคคล"
   **Mandatory pairing — the book's disclaimer, verbatim:** "this playbook offers no legal interpretation; official text and qualified Thai counsel control." / TH rendering: "หนังสือเล่มนี้ไม่ให้การตีความทางกฎหมาย ข้อความทางการและที่ปรึกษากฎหมายไทยที่มีคุณสมบัติเป็นผู้ชี้ขาด" — plus the book's Law-label rule: "Law is binding only when the organization, role, system, and jurisdiction are in scope. Confirm applicability with qualified counsel."
   **NOT verified:** individual PDPA sub-regulations / PDPC notifications. See "Do not assert".

### Dated-status checks deliberately skipped (not applicable to this post)

EU AI Act application dates and 2026 amendments · the NIST June 2026 monitor-and-update item [7] · Stanford AI Index 2026 figures · IEA 2026 energy figures · ETDA Generative AI guideline versions [17]. **None of these is a research target for post #12 and none may appear in it.** If a draft grows a sentence about any of them, that sentence must be cut, not verified late.

---

## Fictional values

All of the following are **illustrative-fictional**: they belong to invented cases inside the playbook. Flag on first mention `(กรณีสมมติจากหนังสือ)` / `(a fictional case from the playbook)`. **None of them may appear in a metrics table as a target, threshold recommendation, or benchmark.**

**Fictional entities:** Aurora Assurance · Kiri Foods · HarborLight Retail · LannaBuild Engineering · Luma Commerce Thailand · the use case id `CX-REFUND-01` · the golden-set id `CXGS-2026-09-v3`.

**Used in this post (§5 and §6):**

| Value | Where it appears | Status |
|---|---|---|
| THB **2,000** structural refund cap | Ch. 8 p. 35; Artifact 2 completed row "Effects" | illustrative-fictional |
| THB **2,500** over-limit proposal, rejected and escalated | Ch. 8 p. 35 | illustrative-fictional |
| **93%** severity-weighted success; no priority slice below **88%** | Artifact 2 "Correctness" row | illustrative-fictional |
| named **400-case** calibration set; support ≥ **96%**; estimated false accepts < **2%**; answer relevance ≥ **0.90**; context precision ≥ **0.85** | Artifact 2 "Faithfulness and relevance" row | illustrative-fictional |
| **schema v6**; "repair once, then withhold"; zero malformed releases | Artifact 2 "Structure" row | illustrative-fictional |
| **100%** terminal records; **99.5%** complete other fields | Artifact 2 "Trace" row | illustrative-fictional |
| "Zero prohibited effects required"; "Zero bypasses" | Artifact 2 "Effects"/"Injection" rows | illustrative-fictional (a *contracted commitment in a fictional contract*, never a measured result) |
| named owners: Payments Engineering · Application owner · Product owner · Policy owner · Security · Release owner · SRE | Artifact 2 completed rows | illustrative-fictional role names; fine to reuse, flagged |

**Not used in this post — do not import them from the plan's list:** THB 2,400 · THB 1,850 · 94.6% / 41.3% · 240 cases · 18 min / 46 h · 80,000 letters. (The 94.6% / 41.3% / 240-case trio belongs to Artifact 1's golden-set example on printed p. 69 — one page earlier — and the Fallback ≥ 70% gate with it. If a draft reaches for them, cut.)

---

## Glossary check

Canonical Thai renderings from the plan's Appendix C list, cross-checked against the book's own Appendix C entries (printed pp. 87–89). **Verbatim on first mention, English inline afterwards.**

| Coinage | Canonical Thai (use verbatim) | Book's Appendix C gloss (for the writer's own understanding) | Note |
|---|---|---|---|
| Assurance contract | **สัญญาการรับประกันเชิงระบบ** | "ข้อตกลงที่ทดสอบได้ เชื่อมสมมติฐาน หน้าที่ สิ่งที่รับประกัน หลักฐาน เจ้าของ เกณฑ์ กติกาเมื่อเปลี่ยนแปลง และการตอบสนองเมื่อผิดเงื่อนไข" (#28) | The plan's key-takeaway paraphrase "ข้อตกลงรายคุณสมบัติ" is fine **after** the canonical rendering has appeared once. |
| Obligation | **หน้าที่ที่ระบบต้องทำ** | "พฤติกรรมหรือขอบเขตที่ระบบต้องปฏิบัติ เขียนให้ชัดพอที่จะมอบหมายเจ้าของ เก็บหลักฐาน และตัดสินได้ว่าผ่านหรือผิดเงื่อนไข" (#29) | §4's "defined precisely enough to assign, gather, pass/fail" is exactly this gloss — quote it, don't reinvent it. |
| Structural guarantee | **การรับประกันเชิงโครงสร้าง** | "คุณสมบัติที่บังคับได้ด้วยสถาปัตยกรรมเชิงกำหนด เช่น การอนุญาต รายการที่ยอมรับ รูปแบบข้อมูล ขีดจำกัดตายตัว แซนด์บ็อกซ์ หรือกฎธุรกรรม" (#30) | **Drift risk (flagged in the plan).** Never swap with semantic estimate; never render as "การรับประกันเชิงระบบ" (that is #28). |
| Semantic estimate | **ค่าประเมินเชิงความหมาย** | "การตัดสินเชิงความน่าจะเป็น เช่น ความถูกต้อง ความเกี่ยวข้อง ความสอดคล้องนโยบาย หรือการตรวจจับการโจมตี ซึ่งต้องวัดผลและห้ามเรียกว่าเป็นการรับประกัน" (#31) | **Drift risk.** The gloss itself contains the post's thesis — "ห้ามเรียกว่าเป็นการรับประกัน". |
| Assurance envelope | **กรอบการรับประกันรอบระบบ** | #27 | **Drift risk: envelope vs contract.** Envelope = the surrounding controls; contract = the written per-property commitments. Distinguish them explicitly at least once. |
| Five rails | **รางควบคุมห้าชั้น** | Ch. 8 / Artifact 3 | This post names them only; the mechanism belongs to #13. |
| Proposal–effect separation | **การแยกข้อเสนอออกจากผลจริง** | — | The book's p. 35 line "The model proposes; an external guard authorizes; a transactional tool creates the effect." |
| Effect mediation | **การควบคุมก่อนเกิดผล** | — | Book: "Complete mediation is a prerequisite." |
| Reconstructable trace | **ร่องรอยที่สร้างเหตุการณ์ย้อนกลับได้** | — | Row 7. |
| Impact assessment | **การประเมินผลกระทบ** | "กระบวนการตลอดวงจรชีวิตเพื่อระบุผู้ได้รับผล คุณประโยชน์ ความเสียหาย สิทธิ ผลกระทบที่กระจายไม่เท่ากัน วิธีลดความเสี่ยง หลักฐาน การมีส่วนร่วม และความเสี่ยงคงเหลือ" (#39) | Plan rule: **kept English inline after the first mention.** So: "การประเมินผลกระทบ (impact assessment)" once, then "impact assessment". |
| Human oversight | **การกำกับดูแลโดยมนุษย์** | #40 | Only if §7's escalation-load metric needs it. |
| Consequence | **ระดับผลกระทบ** | — | Needed by the metrics table's "cost by consequence class". |
| Evaluation | **การประเมินระบบ** | #32 | |
| Adaptive evaluation | **การประเมินแบบปรับตัว** | #33 | Needed for Cards N6–N7's "adaptive-to-implementation tests". |
| Accountability | **ความรับผิดรับชอบ** | — | Governance class: "creates accountability and recovery". |
| AI management system | **ระบบการจัดการ AI** | #38 | Only in the §6 Thai box, alongside ISO/IEC 42005's integration sentence. |
| Fail-safe state | **ภาวะปลอดภัยเมื่อระบบล้มเหลว** | — | The Artifact 2 Trace row's "SRE fails closed on write failure". |

**Kept in English inline (as the book does), no Thai rendering:** Threshold · Trace · Guard · Manifest · Rollback · Release · Escalation · Fallback · Golden set · Prompt · Override · Workflow · Regression test · Canary · Retrieval · Schema · Population · False accept · False reject · Hard enforcement · Soft detection · Governance (as a control-class label).

**Section labels (Thai track):** `หลักปฏิบัติห้าประการ` · `เวิร์กช็อป` · `ตัวชี้วัดสำคัญ` · `รูปแบบความล้มเหลว`. **No `คำถามสำหรับผู้นำ` — Chapter 8 does not have one.**

**Ladder rule:** this post touches neither five-level ladder (the masterclass maturity wording nor Ch. 2's Explore→AI-core). If a draft reaches for a maturity level, cut it — mixing the two is a fact-check FAIL (F9).

---

## Do not assert

Things searched for and **not** established, or established as forbidden. A writer who needs any of these must drop the sentence.

1. **Do not link the r8 paper.** No URL, no DOI, no "available on request", no institutional repository link. It is author-supplied and unpublished. Searched: no public record found.
2. **Do not present any r8 specimen number as a rate, prevalence, benchmark or safety level.** 0/40 and 0/6 are fixed-suite results in author-built fixtures; the book itself lists "claiming zero risk after no fixed-suite failures" as a failure pattern. 4/4 (Card N7) has a denominator of four.
3. **Do not say NIST AI 600-1 requires, mandates or certifies anything.** It is a voluntary cross-sectoral profile; its Suggested Actions must be selected and tailored. There is no NIST conformity claim available to make.
4. **Do not say ISO/IEC 42005:2025 requires an impact assessment, nor quote its normative text.** It is guidance; the book relies only on ISO's public description and reproduces no protected ISO text — this post must do the same. Do not paraphrase clause numbers.
5. **Do not claim ISO/IEC 42005 is "the" AI impact-assessment standard, or that it is harmonised with, equivalent to, or a route to compliance with the EU AI Act.** Not checked, not supported, and outside this post's scope.
6. **Do not state a Thai AI-law status beyond "still under development".** Searched on 2026-09-05: no enacted dedicated Thai AI act found, and no bill traced into parliament. Specifically, **do not state a consultation closing date** — ETDA's own page says the hearing ran to 24 June 2025 while secondary press summaries say it closed 9 June; the discrepancy is unresolved, so name no date but the page's own publication date, 11 June 2025.
7. **Do not cite any PDPA sub-regulation, PDPC notification, or sectoral guideline.** None was fetched or verified. PDPA may be referenced only at the level of the Act itself, with the book's "no legal interpretation … qualified Thai counsel control" disclaimer attached in the same block (fact-check W2).
8. **Do not present the §6 "personal data" property row as an eighth row of the book's Artifact 2.** Artifact 2 has exactly seven rows and none of them is personal data. The personal-data row is an **editorial extension** written for this post; label it as such ("แถวที่ผมเพิ่มเอง" / "a row I add here, not in the book's seven").
9. **Do not present the spec's four contract-writing failure modes as the book's failure-pattern list.** The book's list has eight items (quoted above); the four are an editorial re-cut.
10. **Do not attribute the Scorecard column mapping to the book.** The book's metrics list carries no scorecard columns; the Value/Quality/Risk/People/Learning/Economics assignment is a series convention applied by the writer.
11. **Do not quote, paraphrase, timestamp or cite the masterclass video.** It is not a source for this post. (Id `n_IwUYevRZo` was confirmed live only to close the protocol item.)
12. **Do not describe the book's three control classes, NIST's Govern/Map/Measure/Manage functions, and ISO/IEC 42005's assessment process as the same thing, or as mapping onto each other.** No source establishes that mapping (fact-check W3).
13. **Do not report the iso.org page as returning HTTP 200 from a script.** It 403s to automated clients; verification ran on the IEC co-publisher page. If the fact-check agent re-runs the check and sees 403, that is expected — the recorded corroboration is `https://webstore.iec.ch/en/publication/107659`, HTTP 200 on 2026-09-05.
14. **Do not import numbers from neighbouring chapters** — the Artifact 1 golden-set example on the facing page (240 cases · 94.6% · 41.3% · Fallback ≥ 70% · `CXGS-2026-09-v3`) is one page away and is *not* this post's material.
15. **No study finding of any kind may appear in this post.** There is no `Study`-labelled source in this ledger; if a draft contains a productivity, accuracy or adoption finding, it came from nowhere and must be cut.

---

## Summary for the writer

- **Sources verified: 4** — [2] the book (primary text, local), [3] NIST AI 600-1 (HTTP 200 via DOI → nvlpubs), [4] ISO/IEC 42005:2025 (HTTP 200 on the IEC co-publisher page; iso.org bot-blocked), [5] PDPA Royal Gazette (HTTP 200, conditional use).
- **Unverifiable by design: 1** — [1] the r8 paper; cite as author-supplied and unpublished, never linked.
- **Reference-block labels:** [1] `Synthesis` · [2] `Synthesis` · [3] `Standard` · [4] `Standard` · [5] `Law`.
- **Every claim in the spec is supported.** Two need explicit editorial framing rather than removal: the §6 personal-data row (an addition to the book's seven, must be labelled as the author's) and the §7 four-item failure list (an editorial re-cut alongside the book's eight).
