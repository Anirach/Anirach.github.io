# Research ledger — #9 `ai-transformation-factory`

**Post:** The AI and Data Factory (series post 9 of 20, group `redesign`)
**Book source:** *AI Transformation as an Organizational Core — Bilingual Companion Playbook*, Chapter 5 “Build the AI and data factory” / บทที่ 5 สร้างโรงงาน AI และข้อมูล — **printed pp. 23–25 (PDF pp. 24–26)**; PDF p. 27 = printed p. 26 = start of Chapter 6 (read as the boundary check only, do not draw from it).
**Book evidence snapshot:** 5 September 2026 (stated in the book's front matter).
**Access date for every source below:** **2026-09-05** (Asia/Bangkok).
**Researcher rule for writers:** you may not introduce a source, a number, a date or a quotation that is not on this page.

---

## 0. Claim classes present in this post's spec

| # | Claim class | Present? | Where it lands |
|---|---|---|---|
| C1 | Material number (study/measurement) | **No** | This post makes no empirical/statistical claim. Every number it states is a *count of book-internal structure* (six services, five principles, seven package items, two hours) or a *fictional-case value*. Cards are still written below so the fact-check agent has a target. |
| C2 | Dated legal/standard status | **Yes** — 3 | ISO/IEC 42001:2023, NIST SP 800-218A, W3C PROV-O (+ FinOps for AI page date). No law claim. |
| C3 | Study finding | **No** | Nothing in this chapter rests on a survey, RCT or index. Do not import Stanford AI Index / NBER / Science / HBS numbers — they belong to other posts. |
| C4 | Direct quotation | **Yes** — 2 | (a) the p23 context-engineering sentence; (b) one of the chapter's five operating principles, in the 💡 blockquote. Both verbatim below. |
| C5 | Framework attribution | **Yes** — 4 | PROV-O = *vocabulary*, ISO/IEC 42001 = *lifecycle/management processes*, NIST SP 800-218A = *secure development + supplier practice*, FinOps for AI = *what the FinOps band means operationally*. These four are **not** equivalent and must never be described as such (rubric W3). |
| C6 | Fictional-case value | **Yes** | Luma Commerce Thailand / `CX-REFUND-01`, the THB 2,000 guard, the six scope exclusions. |
| C7 | Masterclass paraphrase | **Yes** | App A §10, §11, §13 — paraphrase only, never quoted (§8 below). |
| C8 | r8 paper | **Not used in this post** | Chapter 5 does not draw on it. Do not cite it here; if a later edit needs it, it is Synthesis, unpublished, **never linked**, and its 517-execution numbers must carry the book's boundary sentence. |

---

## 1. Sources

| [N] | Label | Title | URL | Publisher | Pub date | Accessed | Supports |
|---|---|---|---|---|---|---|---|
| [1] | Synthesis | *AI Transformation as an Organizational Core — Bilingual Companion Playbook*, Ch. 5 “Build the AI and data factory” (pp. 23–25) | *(no public URL — author-supplied PDF, `UserGiven/`)* | Anirach Mingkhwan | Evidence snapshot 2026-09-05 | 2026-09-05 | The whole chapter argument: factory output ≠ model; demand first; the six reusable services; the five operating principles; the two-hour value-stream session; the minimum production package; the metrics list; the failure patterns; `CX-REFUND-01` as the running case. |
| [2] | Synthesis | The Foundation. “AI Transformation: จากการใช้ AI สู่องค์กรที่เรียนรู้เร็วที่สุด \| The Masterclass EP01” | `https://www.youtube.com/watch?v=n_IwUYevRZo` | The Foundation (th) — YouTube channel | uploaded **2026-08-28**; running time 52 min | 2026-09-05 | The AI-factory-versus-project framing (25:53–28:24); scale / scope / learning (28:24–31:13); the AI project → AI capability → AI operating model ladder (34:04–37:18). **Paraphrase only.** |
| [5] | Standard | NIST. *Secure Software Development Practices for Generative AI and Dual-Use Foundation Models: An SSDF Community Profile*, NIST SP 800-218A | landing `https://csrc.nist.gov/pubs/sp/800/218/a/final` · PDF `https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218A.pdf` | National Institute of Standards and Technology (US) | **2024-07-26**, status **Final** | 2026-09-05 | That secure-development and **supplier/acquirer** practice is part of the factory's shared band, not a separate late-stage review. |
| [10] | Standard | W3C. *PROV-O: The PROV Ontology* | `https://www.w3.org/TR/prov-o/` | World Wide Web Consortium | **W3C Recommendation, 30 April 2013** | 2026-09-05 | That provenance has an interoperable *vocabulary* (entities, activities, agents, derivations) the data-product and observability services can emit against. |
| [11] | Standard | ISO/IEC 42001:2023 — *Information technology — Artificial intelligence — Management system* | `https://www.iso.org/standard/42001` | ISO / IEC | **Edition 1, 2023-12**, status **Published** (stage 60.60) | 2026-09-05 | That the factory's owners, monitoring and continual improvement are *lifecycle management-system processes*, not a one-off project checklist. |
| [36] | Standard | FinOps Foundation. *FinOps for AI* (Framework technology category) + *FinOps for AI Overview* (working group) | `https://www.finops.org/framework/technology-categories/ai/` · `https://www.finops.org/wg/finops-for-ai-overview/` | FinOps Foundation (Linux Foundation) | Overview page **last updated 2026-02-17** | 2026-09-05 | What the **FinOps** band means operationally inside the factory: allocation, forecasting, optimization, unit economics (cost per call / per token / per successful outcome), and quota-and-throttle governance. |

**Reference-block numbering note for the writer:** [1] [2] [5] [10] [11] keep the book's own D.3 numbers so the series stays consistent across posts. FinOps is an *addition* named by the spec and has no D.3 number — the plan's addition slot is used here as **[36]**; if the builder assigns series-wide reference numbers, renumber consistently and keep the label `Standard`.

### Verification notes (fetch mechanics, so a later re-check does not repeat the dead ends)

- **`iso.org` returns HTTP 403 to every non-browser agent** (curl, WebFetch, firecrawl all 403). It was verified **in a real browser session on 2026-09-05**: `https://www.iso.org/standard/81230.html` → 200, redirecting to the canonical `https://www.iso.org/standard/42001`, page title “ISO/IEC 42001:2023 - AI management systems”. **The URL is live; the 403 is bot-blocking, not a dead link.** Do not "fix" it.
- **⚠️ Never append `.html` to the ISO 42001 URL.** `https://www.iso.org/standard/42001.html` is a *different standard* — it resolves to **ISO 12164-4:2008, “Hollow taper interface with flange contact surface — Part 4”** (42001 is that document's catalogue id). The extensionless form `iso.org/standard/42001` is the friendly URL for ISO/IEC 42001. Verified 2026-09-05.
- **NIST PDF:** `HEAD` on `nvlpubs.nist.gov/.../SpecialPublications/NIST.SP.800-218A.pdf` answers 404, but `GET` answers **200, `application/pdf`, 650,661 bytes**. The book's URL is correct; a HEAD-only checker will produce a false negative.
- **`w3.org/TR/prov-o/`** → 200, no redirect.
- **`finops.org`** both pages → 200.
- **Look-alike rejection:** no non-publisher mirror (iso-standards resellers, PDF aggregators, `nist.org`-style domains) was accepted for any entry.

---

## 2. Number cards

*No card, no number.* Every number the post may state is below. Nothing in this post is an empirical measurement, so the "denominator/population" line reads **not applicable — structural count** where that is the honest answer, rather than being invented.

### NC-1 — Six factory services

- **Value / unit:** 6 · reusable service categories
- **Denominator / population:** not applicable — a structural count of the chapter's own enumeration, not a sample
- **Comparison:** against the alternative the chapter rejects — per-project rebuilding, where "every use case rebuilds the same foundations" ([2] §10)
- **Task / setting:** an organization's shared AI-and-data capability, spanning use cases
- **Source:** [1] p24 — verbatim: *"Factory capability has six reusable services. Data products provide governed facts. Context services assemble instructions, retrieved evidence, and memory. Model services route tasks to the smallest adequate model and manage provider change. Evaluation services hold labeled cases, judge calibration, and test execution. Tool registry services define scopes, schemas, effect classes, and approval requirements. Observability services capture traces, outcomes, cost, drift, and incidents. Shared security, privacy, FinOps, and sustainability controls span the six."*
- **Cross-check:** the book's own six-layer table (p3–p4) gives the same layer's minimum evidence as *"Data products context services evaluation harness tool registry and observability"* — five named there, because model services sit inside the delivery spine. **Use the six-service list from p24; do not "correct" it against the p4 table.**
- **Boundary (the book's own):** author synthesis. The chapter presents the six as a design vocabulary for reuse, not as a certified reference architecture or a required org chart.
- **TH sentence:** โรงงานมีบริการที่ใช้ซ้ำได้หกด้าน — Data products, Context services, Model services, Evaluation services, Tool registry services และ Observability services โดยมี Security, Privacy, FinOps และ Sustainability พาดผ่านทั้งหกด้าน
- **EN sentence:** The factory has six reusable services — data products, context services, model services, evaluation services, tool registry services and observability services — with security, privacy, FinOps and sustainability controls spanning all six.

### NC-2 — Five operating principles

- **Value / unit:** 5 · operating principles
- **Denominator / population:** not applicable — structural count
- **Comparison:** the same five-principle form is used in every chapter of the book; principles are **never renumbered** across the series
- **Task / setting:** Chapter 5, the factory layer
- **Source:** [1] p24, verbatim and in order:
  1. *"Start with the decision — Define outcome user authority and consequence before pipelines."*
  2. *"Treat data as a product — Give every critical set an owner semantic contract lineage access policy and lifecycle."*
  3. *"Treat context as a release artifact — Version prompts templates corpus ranking memory and tools together."*
  4. *"Move evidence with the product — A candidate without test results limitations and rollback is incomplete."*
  5. *"Turn feedback into governed learning — Validate corrections add neighboring cases and rerun the gate."*
  - Thai, verbatim: 1. *เริ่มจากการตัดสินใจ ระบุ Outcome ผู้ใช้ อำนาจ และผลกระทบก่อนสร้าง Pipeline* · 2. *บริหารข้อมูลเป็นผลิตภัณฑ์ ข้อมูลสำคัญต้องมีเจ้าของ Semantic Contract, Lineage, Access และ Lifecycle* · 3. *ถือบริบทเป็นองค์ประกอบของรุ่น กำหนดรุ่นของ Prompt, Template, Corpus, Ranking, Memory และ Tool ร่วมกัน* · 4. *ส่งหลักฐานไปพร้อมผลิตภัณฑ์ รุ่นที่ไม่มีผลทดสอบ ข้อจำกัด และ Rollback ยังไม่พร้อม* · 5. *เปลี่ยน Feedback เป็นการเรียนรู้ที่กำกับได้ ตรวจคำแก้ สร้างกรณีข้างเคียง และผ่าน Gate ใหม่*
- **Boundary:** author synthesis.
- **💡 blockquote instruction:** quote **exactly one** in the `<blockquote>💡 มุมมองของผม: …</blockquote>`; the other four are listed in prose. **Recommended: principle 3, “Treat context as a release artifact.”** It is the one that carries §4 (`context-engineering`) and bridges forward to #11's runtime-context manifest. If a writer prefers principle 1, that also fits §2 (`demand-first`) — but only one may be quoted.
- **TH sentence (principle 3):** หลักปฏิบัติข้อ 3 ของบทนี้คือ “ถือบริบทเป็นองค์ประกอบของรุ่น กำหนดรุ่นของ Prompt, Template, Corpus, Ranking, Memory และ Tool ร่วมกัน”
- **EN sentence (principle 3):** The chapter's third operating principle is “Treat context as a release artifact — version prompts, templates, corpus, ranking, memory and tools together.”

### NC-3 — Seven items in the minimum production package

- **Value / unit:** 7 · required artifacts before release
- **Denominator / population:** not applicable — structural count
- **Comparison:** against a release that ships a candidate with none of them, which the chapter calls *"incomplete"* (principle 4)
- **Task / setting:** the close of the two-hour value-stream working session
- **Source:** [1] p24 — verbatim: *"Finish with a minimum production package: data contract, context manifest, golden-set plan, effect boundaries, owners, acceptance metrics, and rollback."* Thai, verbatim: *ผลลัพธ์ขั้นต่ำคือ Data Contract, Context Manifest, Golden-set Plan, Effect Boundary, Owner, Acceptance Metric และ Rollback*
- **Boundary:** author synthesis; it is a minimum, not a sufficiency test. The book's own front matter: *"This book is an organizational design and engineering resource. It is not legal, audit, certification, investment, employment, cybersecurity, or safety advice."*
- **TH sentence:** Minimum production package มีเจ็ดรายการ ได้แก่ Data contract, Context manifest, Golden-set plan, Effect boundary, Owner, Acceptance metric และ Rollback — แต่ละรายการต้องมีเจ้าของ เลขรุ่น และหลักฐานกำกับ
- **EN sentence:** The minimum production package has seven items — data contract, context manifest, golden-set plan, effect boundaries, owners, acceptance metrics and rollback — each carrying an owner, a version and its evidence.

### NC-4 — Two hours, six owners (the working session)

- **Value / unit:** 2 hours · 6 owner roles
- **Denominator / population:** not applicable — a prescribed agenda length, not a measured duration
- **Comparison:** none is offered; the chapter does not claim two hours is optimal or benchmarked
- **Task / setting:** *Factory value stream design* working session, mapping **one** request end to end
- **Source:** [1] p24 — verbatim: *"Run a two-hour session with product, domain, data, platform, operations, and risk owners. Map one request from business intent to released outcome. Identify authoritative sources, transformations, context assembly, model decisions, tool effects, human handoffs, evidence, and feedback. Mark queues, reconciliation, ambiguous definitions, and ownerless points."* Thai, verbatim: *จัดสองชั่วโมงร่วมกับเจ้าของ Product, Domain, Data, Platform, Operations และ Risk ไล่คำขอหนึ่งรายการจากเจตนาธุรกิจถึงผลลัพธ์ที่ปล่อย*
- **Boundary:** author synthesis; a facilitation default, not a measured result. **Do not write “research shows two hours is enough.”**
- **TH sentence:** เวิร์กช็อปใช้เวลาสองชั่วโมง ร่วมกับเจ้าของหกบทบาท ได้แก่ Product, Domain, Data, Platform, Operations และ Risk แล้วไล่คำขอเพียงหนึ่งรายการจากเจตนาธุรกิจถึงผลลัพธ์ที่ปล่อยจริง
- **EN sentence:** The session runs two hours with six owners — product, domain, data, platform, operations and risk — tracing a single request from business intent to released outcome.

### NC-5 — Three capability levels (project → capability → operating model)

- **Value / unit:** 3 · levels
- **Denominator / population:** not applicable — a distinction drawn in the masterclass, restated by the book
- **Comparison:** *"One hundred disconnected pilots may be further from transformation than ten uses that share a platform, feedback loop, and expansion path."* ([1] App A §13, paraphrasing [2] at 34:04–37:18)
- **Task / setting:** organizational maturity of AI delivery
- **Source:** [1] App A §13 / [2] 34:04–37:18. Book paraphrase: *"An AI project proves one problem can be addressed. An AI capability adds reusable data, model management, governance, expertise, and experimentation. An AI operating model makes those capabilities part of how decisions and workflows are designed."*
- **⚠️ Do not mix ladders.** This is a **three-level** delivery-maturity distinction. It is **not** the book's five-level maturity ladder (สำรวจ / ช่วยงาน / บริหารอย่างเป็นระบบ / บูรณาการ / ปฏิบัติการแบบ AI-core) and **not** the masterclass's own five-level wording. Series convention A.3: *"the two five-level ladders … are never mixed."* Keep this one clearly labelled as the project→capability→operating-model distinction.
- **Boundary (the book's own, for [2]):** *"practitioner synthesis, not a controlled study; this book uses corrected paraphrase of imperfect automatic captions."* The "100 pilots vs 10 uses" figures are **rhetorical illustration, not a measurement** — never put them in a metrics table.
- **TH sentence:** วิดีโอต้นทางแยกสามระดับ — AI project พิสูจน์ว่าแก้ปัญหาหนึ่งเรื่องได้, AI capability เพิ่มข้อมูล การจัดการโมเดล governance และการทดลองที่ใช้ซ้ำได้, ส่วน AI operating model ทำให้ความสามารถนั้นเป็นส่วนหนึ่งของวิธีออกแบบ decision และ workflow
- **EN sentence:** The source distinguishes three levels — an AI project proves one problem can be addressed, an AI capability adds reusable data, model management, governance and experimentation, and an AI operating model makes those capabilities part of how decisions and workflows are designed.

### NC-6 — Three powers (scale, scope, learning)

- **Value / unit:** 3 · powers of a digital operating model
- **Denominator / population:** not applicable
- **Comparison:** scale is defined *against* resource growth — *"without proportional growth in resources"*
- **Task / setting:** the economics of a shared factory, [2] 28:24–31:13
- **Source:** [1] App A §11 — *"Scale serves more customers, transactions, or decisions without proportional growth in resources. Scope reuses data and AI capabilities across products, services, and contexts. Learning turns interactions into better understanding and future performance."* And: *"The important economic loop is use → evidence → learning → better product or process → more valuable use, with quality and harm measured at each step."*
- **Boundary:** same as NC-5 — practitioner synthesis, corrected paraphrase of automatic captions. **The powers are explicitly not automatic:** *"These powers are not automatic properties of a model."*
- **TH sentence:** Digital operating model ที่แข็งแรงให้พลังสามด้าน — Scale รองรับงานมากขึ้นโดยทรัพยากรไม่เพิ่มตามสัดส่วน, Scope นำความสามารถไปใช้ซ้ำข้ามผลิตภัณฑ์และบริบท, Learning เปลี่ยน interaction ให้เป็นผลการทำงานที่ดีขึ้น และพลังทั้งสามไม่ได้เกิดจากโมเดลโดยอัตโนมัติ
- **EN sentence:** A strong digital operating model yields three powers — scale (more work without proportional resources), scope (reuse across products and contexts) and learning (interactions becoming better performance) — and none of the three is an automatic property of a model.

### NC-7 — Twelve metrics in the book's list (spec's METRICS table selects ten)

- **Value / unit:** 12 · named measures in the chapter's “Metrics that matter”
- **Denominator / population:** not applicable — structural count
- **Comparison:** the chapter's own instruction — *"Separate outcome improvement from factory health."*
- **Task / setting:** running factory
- **Source:** [1] p25, verbatim, in order: *lead time from approved use case to governed release · data freshness · contract violations · provenance coverage · evaluation coverage by consequence · reuse of approved components · defect escape · rework · escalation · p95 latency · energy and cost per successful task · time from verified incident to reusable control improvement.*
- **⚠️ Discrepancy the writer must handle:** the editorial spec's §7 lists **ten**, folding *rework* and *escalation* into neighbouring rows and shortening two labels. **If the post states a count, state twelve and cite the book; otherwise state no count at all.** Do not write "ten metrics".
- **Boundary:** author synthesis; a measurement vocabulary, not targets. No threshold value appears in the chapter and none may be invented.
- **TH sentence:** บทนี้ระบุตัวชี้วัดสิบสองตัว โดยยืนยันหลักการก่อนว่า “แยกผลลัพธ์ธุรกิจจากสุขภาพโรงงาน” และไม่ได้กำหนดค่าเป้าหมายใดไว้เลย
- **EN sentence:** The chapter names twelve measures under one instruction — separate outcome improvement from factory health — and sets no target value for any of them.

### NC-8 — Eight failure patterns (spec's §7 names three)

- **Value / unit:** 8 · failure patterns
- **Denominator / population:** not applicable — structural count
- **Source:** [1] p25, verbatim: *"Building a data lake without a decision, calling pilots a factory, shadow corpora, unversioned prompts, measuring uptime while ignoring semantic quality, treating all user feedback as truth, optimizing retrieval without post-state checks, and centralizing every delivery choice in one specialist queue."*
- **⚠️ Discrepancy:** the spec's §7 names three (*building a platform before demand · unversioned context · evaluation as a one-off*). Only the first two map cleanly to the book's list ("building a data lake without a decision"; "unversioned prompts" + "shadow corpora"). **"Evaluation as a one-off" is not in the book's failure list** — see Do-not-assert D3.
- **Boundary:** author synthesis.
- **TH sentence:** บทนี้ระบุรูปแบบความล้มเหลวแปดแบบ ตั้งแต่การสร้าง data lake โดยไม่รู้ว่าจะปรับการตัดสินใจใด ไปจนถึงการรวมทุกคำตัดสินไว้ที่คิวของทีมผู้เชี่ยวชาญส่วนกลางเพียงทีมเดียว
- **EN sentence:** The chapter names eight failure patterns, from building a data lake without knowing which decision it improves to funnelling every delivery choice into one central specialist queue.

---

## 3. Direct quotations (the only two permitted verbatim)

### Q-1 — the context-engineering sentence (printed p. 23)

- **English, verbatim:** *"For generative systems, this continues into context engineering. Retrieved passages, instructions, session state, tool semantics, and policy thresholds all influence behavior. They belong to the release process rather than invisible plumbing."*
- **Thai, verbatim (the book's own mirror, p. 23):** *สำหรับ Generative AI งานต้องขยายถึง Context Engineering เพราะข้อความที่ค้นคืน คำสั่ง สถานะเซสชัน ความหมายของเครื่องมือ และ Threshold นโยบายล้วนร่วมกำหนดพฤติกรรม จึงต้องอยู่ในกระบวนการปล่อยรุ่น*
- **Use:** §4 `context-engineering`. Quote at most the third sentence; the first two may be paraphrased. Attribute to [1] with the page.
- **⚠️ The spec renders the list as "policy thresholds"; the book's Thai mirror says "Threshold นโยบาย". Both tracks must name the same five items: retrieved passages, instructions, session state, tool semantics, policy thresholds.**

### Q-2 — one of the five operating principles

See NC-2. Verbatim, un-renumbered, in the 💡 blockquote only.

**Nothing else in this post may be presented as a quotation** — in particular, nothing from the masterclass (see §8) and nothing from ISO, NIST or W3C beyond the passages recorded in §1 and §4.

---

## 4. Dated statuses

Each is one dated sentence the writer may use as written.

- **ISO/IEC 42001:2023 — as of 5 September 2026 it is Published, Edition 1, dated 2023-12, at stage 60.60 (International Standard published), with no revision, amendment or new edition listed on its ISO catalogue page.**
  Supporting text from the page: *"ISO/IEC 42001 is an international standard that specifies requirements for establishing, implementing, maintaining, and continually improving an Artificial Intelligence Management System (AIMS) within organizations. It is designed for entities providing or utilizing AI-based products or services, ensuring responsible development and use of AI systems."*
  Book's boundary for [11], which must ride with any use: *"this book relies only on ISO's public description and does not reproduce protected requirements or confer certification."* → **never imply the post's checklist is conformity work, and never imply certification.**

- **NIST SP 800-218A — as of 5 September 2026 it remains Final, published 26 July 2024, with no superseding revision issued.**
  Abstract passage: it *"augments the secure software development practices and tasks defined in Secure Software Development Framework (SSDF) version 1.1 by adding practices, tasks, recommendations, considerations, notes, and informative references that are specific to AI model development throughout the software development life cycle,"* and serves *"producers of AI models, the producers of AI systems that use those models, and the acquirers of those AI systems."* (The acquirer clause is what carries the spec's "supplier practices" claim.)
  Book's boundary for [5]: *"a secure-development profile reduces risk; it does not guarantee secure behavior in deployment."*

- **W3C PROV-O — as of 5 September 2026 it is still a W3C Recommendation, published 30 April 2013, and has not been superseded.**
  Abstract passage: *"The PROV Ontology (PROV-O) expresses the PROV Data Model using the OWL2 Web Ontology Language (OWL2). It provides a set of classes, properties, and restrictions that can be used to represent and interchange provenance information generated in different systems and under different contexts."* The page's normative sections cover compliance, notation and ontology description — **there is no audit requirement in it.**
  Book's boundary for [10]: *"the ontology supplies a vocabulary, not a complete audit policy or storage design."* → the spec's own phrasing ("provenance vocabulary (not an audit policy)") is exactly right; keep it.

- **FinOps for AI — the FinOps Foundation's *FinOps for AI Overview* was last updated 17 February 2026, and *FinOps for AI* is a technology category of the FinOps Framework as of 5 September 2026.**
  Operational content the band may be described with: allocation (identifying the consumer of model output), forecasting (*"Predictability is generally lower… much more experience is required to make forecasts"*), optimization, unit economics (*"Additional token-based units and drivers"* — cost-per-call, cost per inference, satisfaction divided by AI cost), and governance (*"multiple limits such as quotas, use of reserved capacity, throttles"*).
  **Cost numbers belong to post #17.** Use FinOps here only to say *what the band does*, never to state a price, a TWh figure or a saving.

- **Masterclass video — the source video, id `n_IwUYevRZo`, was uploaded 28 August 2026 by the channel “The Foundation (th)”, runs 52 minutes, and carries the title the book cites verbatim.** Timestamp verification in §8.

### Re-checks that do NOT apply to this post — recorded so the fact-check agent sees they were considered

| Re-check | Applies? | Why |
|---|---|---|
| Thailand's dedicated AI law (ETDA `law_ai`; ร่างพระราชบัญญัติ…ปัญญาประดิษฐ์) | **No** | Post #9 makes no legal-status claim. The book's "still under development" line at its 5 Sept 2026 cutoff belongs to the governance posts. Do not import it. |
| EU AI Act application dates / 2026 amendment | **No** | No EU claim in this spec. |
| NIST June 2026 monitor-and-update item ([7]) | **No** | Not a research target here; it belongs to the assurance/evaluation posts. |
| Stanford AI Index 2026 ([25]) | **No** | No adoption or economy figure in this post. |
| IEA 2026 energy figures ([35]) | **No** | Spec explicitly defers costs and energy to **#17**. |
| ISO/IEC 42005:2025 ([12]) | **No** | Impact assessment is not this chapter's subject; #11–#14 carry it. |
| ETDA guideline versions ([17], [18]) | **No** | No Thai-guidance claim in this spec. |
| PDPA / PDPC sub-regulations | **No** | The privacy band is named, not described in legal terms. If the writer describes the privacy band, describe it as a control family — not as PDPA compliance. |

---

## 5. Fictional values

All of the following are **illustrative-fictional** and must be flagged on first mention: `(กรณีสมมติจากหนังสือ)` / `(a fictional case from the playbook)`. **None may appear in a metrics table as a target, a benchmark or a threshold recommendation.**

The book's own blanket statement, verbatim ([1] Appendix B preamble, p. 66): *"All examples use CX-REFUND-01, a fictional Luma Commerce Thailand assistant. It answers bilingual refund questions and may propose `issue_refund`. An external guard may execute one eligible refund no greater than THB 2,000 after confirmation; all other financial actions go to a person. **Values are illustrative, not universal thresholds.**"*

| Value | Status | Book wording |
|---|---|---|
| **Luma Commerce Thailand** | fictional company | *"a fictional Luma Commerce Thailand assistant"* |
| **`CX-REFUND-01`** | fictional case id | *"the shared fictional case CX-REFUND-01, a customer refund companion that answers policy questions, routes cases, drafts replies, proposes refunds, and creates CRM notes"* (p23) |
| **`issue_refund`** | fictional tool name | the only financial tool the guard admits |
| **THB 2,000** | fictional threshold | *"one eligible refund no greater than THB 2,000 after confirmation"*; the chapter itself says only *"prohibited refund amounts"* |
| **Six scope exclusions** | fictional scope | verbatim (p67): *"excludes fraud flags, subscriptions, marketplace orders, legal complaints, non-THB payments, and amounts above THB 2,000"* |
| Aurora Assurance · Kiri Foods · HarborLight Retail · LannaBuild Engineering | fictional, **other posts** | Do not introduce them here; #9's running case is Luma / `CX-REFUND-01` only. |
| THB 2,400 / 2,500 / 1,850 · 94.6% / 41.3% · 240 cases · 18 min / 46 h · 80,000 letters | fictional, **other posts** | **None of these belongs in #9.** If one appears in a draft, delete it. |
| “100 pilots vs 10 uses” ([2] §13) | rhetorical illustration, not a measurement | May be paraphrased as the source's framing; never as data. |

---

## 6. Glossary check

Canonical Thai renderings (plan A.3, from the book's Appendix C) for every coinage this post uses. **Verbatim on first mention, English inline afterwards.**

| Coinage | Canonical Thai (use verbatim) | Note |
|---|---|---|
| AI and data factory | **โรงงาน AI และข้อมูล** | The chapter heading is *บทที่ 5 สร้างโรงงาน AI และข้อมูล*. ⚠️ The book's Thai body prose at p24 writes *โรงงานข้อมูลและ AI* (order reversed). **Use the canonical โรงงาน AI และข้อมูล** — it matches the chapter heading, the glossary and the manifest. |
| AI transformation | การเปลี่ยนผ่านองค์กรด้วย AI | first mention only |
| Operating model | รูปแบบการดำเนินงาน | for the §2 ladder's third level |
| Learning loop | วงจรการเรียนรู้ | if §2 reaches for it |
| Provenance | ที่มาของข้อมูลและผลลัพธ์ | needed for the PROV-O paragraph and for "provenance coverage" |
| Observability | ความสามารถในการสังเกตระบบ | one of the six services |
| Evaluation | การประเมินระบบ | one of the six services |
| Release gate | ด่านอนุมัติการนำระบบออกใช้ | if §4 or §6 names the gate |
| Runtime-context manifest | บัญชีรายการบริบทขณะทำงาน | **only as the forward pointer to #11** — do not develop it here |
| Context as program | บริบทในฐานะโปรแกรม | optional; #12 owns it |
| Decision authority | อำนาจตัดสินใจ | if §2 names it |
| Consequence | ระดับผลกระทบ | used by "evaluation coverage by consequence" |
| AI management system | ระบบการจัดการ AI | for the ISO/IEC 42001 sentence |
| Sustainable AI | AI ที่ยั่งยืน | for the sustainability band |

**Kept in English inline, as the book does:** Workflow · Manifest · Release · Rollback · Regression test · Prompt · Golden set · Threshold · Guard · Retrieval · Dashboard · Trace · Escalation · Inventory · Supplier/Vendor · Pilot.

**Section labels (chapter-level, verbatim):** หลักปฏิบัติห้าประการ · เวิร์กช็อป · ตัวชี้วัดสำคัญ · รูปแบบความล้มเหลว · คำถามสำหรับผู้นำ.

### ⚠️ Two glossary deviations the writer must know

1. **“GreenOps” is NOT the book's word.** The book says **sustainability** (EN, p24: *"Shared security, privacy, FinOps, and sustainability controls span the six"*; TH, p24: *"…Security, Privacy, FinOps และ Sustainability พาดผ่านทั้งหมด"*). The string `GREENOPS` appears only in the **figure label and the plan's alt text**, which are fixed series artwork strings. **In prose, name the band's fourth control `sustainability` / `AI ที่ยั่งยืน`, and if `GreenOps` is used at all, gloss it once as the series' shorthand for the sustainability control — never attribute the word to the book.**
2. **Layer stamp wording.** The book's own layer table names the layer **“AI and data factory”** with the leadership question *"Which components should become reusable"* and minimum evidence *"Data products context services evaluation harness tool registry and observability"*. The mapped question is **Q7 — “Who owns value risk effects exceptions and learning”** (book's field promise, p2). Use those exact strings in the `🧭` stamp.

---

## 7. Do not assert

Things searched for and **not** verifiable. If a draft contains any of these, the writer must drop or rewrite the sentence.

- **D1 — “Six services” as anyone's standard.** No standards body defines a six-service AI factory. It is [1]'s author synthesis, corroborated only in spirit by [2] §10's four components (*"continuously usable data pipelines, models or algorithms, an experimentation capability, and digital infrastructure"*). **Never say "the standard six services" or attribute the six to ISO, NIST or the masterclass.**
- **D2 — Any quantified reuse benefit.** [2] §10 says only *"Reuse lowers the marginal cost of the next use case."* **There is no percentage, no multiple and no "N× cheaper" anywhere in the book or the source video.** The post's own hook ("if the second use case costs as much as the first…") is a *question*, not a measurement — keep it as a question.
- **D3 — “Evaluation as a one-off” as a book failure pattern.** The spec's §7 names it; the book's eight-item failure list does not contain it. The closest book statements are principle 5 (*"rerun the gate"*) and the metric *"evaluation coverage by consequence"*. **Rewrite as a consequence of the book's material** — e.g. "a golden set built once and never rerun stops being evidence" — attributed as the author's reading, not as a listed failure pattern. Do not cite a page for it.
- **D4 — ISO/IEC 42001 requirement text.** Only the public ISO description is available and the book forbids reproducing protected requirements. **Do not paraphrase clause numbers, Annex A controls, or "42001 requires X".** Say what the standard is *for* (lifecycle processes, ownership, monitoring, continual improvement), citing the public overview.
- **D5 — Certification language.** Neither ISO/IEC 42001, NIST SP 800-218A, PROV-O nor FinOps certifies a factory. **No sentence may imply the minimum production package makes a system compliant, certified or audited.** Carry the book's disclaimer if the paragraph gets close: *"It is not legal, audit, certification, investment, employment, cybersecurity, or safety advice."*
- **D6 — A FinOps version number for “FinOps for AI”.** The Framework's own version/edition string is not stated on the two verified pages; only the *Overview* page's last-updated date (2026-02-17) is. **Do not write "FinOps Framework v-N" or "the 2026 Framework release" without re-verifying** — the search surfaced a *FinOps Framework 2026* insights post that was **not** fetched or verified for this ledger.
- **D7 — Any masterclass quotation, slide description or presenter attribution.** See §8.
- **D8 — Anything from Chapter 6.** PDF p27 (printed p26) begins the federated operating model. Its content — the centre/domain split, the six named owners, "accountability is property specific" — belongs to **#10**. #9's §8 may point forward to it, but must not describe it.
- **D9 — The r8 paper.** Not used in this post, and never linked in any post. Its 517-execution numbers do not belong here at all.
- **D10 — Energy, cost or price figures.** Deferred to #17 by the spec. The IEA figure the book carries (485 TWh, p46) is **out of scope for #9**.

---

## 8. Masterclass verification (paraphrase-only source)

- **Video id `n_IwUYevRZo` — VERIFIED 2026-09-05.** Title returned by the platform matches the book's citation character for character: *AI Transformation: จากการใช้ AI สู่องค์กรที่เรียนรู้เร็วที่สุด | The Masterclass EP01*. Channel: **The Foundation (th)**. Upload date: **2026-08-28**. Duration: **52 minutes** (the book records 52 min 15 s).
- **Timestamps — VERIFIED against the Thai caption track:**

| Cited range | Book section | Caption at the boundary | Verdict |
|---|---|---|---|
| **25:53** | App A §10 begins | *"ทุกวันองค์กรทั่วไปมักทำ AI แบบโครงการ มีปัญหา 1 เรื่อง ตั้งทีม 1 ทีม เก็บข้อมูล สร้างโมเดล ทดลอง…"* then at 26:19 *"แนวคิด AI Factory จาก…"* | ✅ exact |
| **28:24** | §10 ends / §11 begins | *"องค์กรที่สร้าง Digital Operating Model ที่แข็งแรงจะได้พลังสำคัญ 3 อย่าง พลังแรกคือสเกล…"* | ✅ exact |
| **31:13** | §11 ends / §12 begins | *"AI operating model จึงต้องมีองค์ประกอบร่วม เช่น … Data AI platform, Governance และ Cross Functional Teams"* | ✅ exact |
| **34:04** | §13 begins | *"…workflow เจ้าของกระบวนการและคนหน้างานที่ยอมรับ ดังนั้นอย่าวัดความก้าวหน้าของ AI ด้วยจำนวน use cases เพียงอย่างเดียว องค์กรที่มี 100 Pilot แต่อยู่แยกกัน…"* | ✅ exact |

- **Handling rule (non-negotiable).** The captions above are **verification evidence for this ledger only**. They are auto-generated Thai captions with recognition errors (visible in the raw track: *"Devo"*, *"Modu"*, *"องค์พอ"*). **They must never appear in the post**, in either track, quoted or unquoted. The post paraphrases **the book's App A wording**, and attributes to the video as *"the source video's §10 (25:53–28:24)"* — never as *"the presenter said"*. The book's own boundary for [2] rides with every use: practitioner synthesis, not a controlled study; corrected paraphrase, not a transcript.
- **Linking:** link the plain watch URL `https://www.youtube.com/watch?v=n_IwUYevRZo`. A `&t=` deep link is permitted for the four verified boundaries above and for no others.

---

## 9. Section-by-section evidence map (what each spec section may rest on)

| § | Slug | Permitted evidence |
|---|---|---|
| 1 | `output-is-not-a-model` | [1] p23 opening (*"Its output is not merely a model. It includes trusted source data, retrieval corpora, context templates, tool contracts, evaluation sets, release manifests, operating procedures, and feedback converted into regression tests."*) + [2] §10 (25:53–28:24) + [2] §13 (34:04–37:18). **No number.** |
| 2 | `demand-first` | [1] p23 (*"The factory begins with demand. Identify the decision to improve, its accountable owner, the permitted role of AI, and the measurable outcome before collecting more data."*) + NC-5 + NC-6. |
| 3 | `six-services` | NC-1 (verbatim service list) + [11] for the ownership/lifecycle band + [5] for the security band + [36] for the FinOps band + [10] for provenance emitted by data-product and observability services. **D1 applies.** |
| 4 | `context-engineering` | Q-1 (p23 verbatim) + NC-2 principle 3. Forward pointer to #11's manifest only. |
| 5 | `cx-refund-01` | [1] p23 CX-REFUND-01 paragraph + Appendix B preamble (p66) + Artifact 1 scope row (p67). Everything flagged fictional (§5). |
| 6 | `value-stream` | NC-4 (session) + NC-3 (package). |
| 7 | `metrics-failures` | NC-7 + NC-8. **No target values.** Scorecard column mapping available from the book's board scorecard: Value · Quality · Risk · People · Learning · Economics. |
| 8 | `road-ahead` | Layer stamp strings in §6 deviation 2 (layer "AI and data factory", Q7). Next → `/blog/ai-transformation-operating-model`. **D8 applies.** |

---

*Ledger compiled 2026-09-05 (Asia/Bangkok). Sources verified: 6 of 6. Unverified: 0.*
