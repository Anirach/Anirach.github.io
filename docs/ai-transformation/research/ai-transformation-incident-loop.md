# Research ledger — #15 `ai-transformation-incident-loop`

**Post:** Evidence Before Change — จากเหตุการณ์ผิดพลาดสู่ระบบที่ดีขึ้น / *Evidence Before Change — From Incident to Improvement*
**Group:** Engineer · **Layer:** Learning loop · **Question:** Q6 · **Figure:** 13 · **Artifacts:** 6 and 8
**Book pages read:** PDF 39–43 (printed 38–42 — Chapter 9 opener and Figure 12 for context, the incident half of the English and Thai companions, Figure 13, and the Part four opener) · PDF 78–80 and 82–85 (printed 77–79 and 81–84 — Artifact 6 in both languages, the tail of Artifact 7 for the pre-incident baseline, Artifact 8 in both languages) · PDF 88–91 (printed 87–90 — Appendix C entries 20–45) · PDF 93–96 (printed 92–95 — the D.3 source list and its Boundary lines). The whole PDF was additionally extracted with `pdftotext -layout` and searched, which is how the fabricated `INC-CX-014` was caught and how the r8 passage and the Thai verbatim strings were confirmed character-for-character.
**Access date for every web source below: 2026-09-05 (Asia/Bangkok).**
**Verified: 4 of 4 sources (all HTTP 200 on the canonical publisher domain). Unverified: 0. Claims in the spec that could not be supported: 0 — but three need re-wording before they are true (Cards 1, 2 and 3, and the two synthesis metrics in §7).**

Writers may not introduce a source or a number that is not in this ledger.

---

## Sources

| # | Book ref | Label | Title | URL | Publisher | Pub date | Accessed | Supports |
|---|---|---|---|---|---|---|---|---|
| [1] | book [4] | **Standard** | *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*, NIST AI 600-1 | `https://doi.org/10.6028/NIST.AI.600-1` → `https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf` | National Institute of Standards and Technology (NIST), U.S. Department of Commerce | July 2024 | 2026-09-05 | §2 the loop; §5 the worksheet; §7 metrics — incident response and recovery plans, near-miss recording, after-action verification, incident reporting, content-provenance tracking |
| [2] | book [10] | **Standard** | *PROV-O: The PROV Ontology* | `https://www.w3.org/TR/prov-o/` | World Wide Web Consortium (W3C) | W3C Recommendation, 30 April 2013 | 2026-09-05 | §3 the trace schema — entity / activity / agent as the vocabulary a reconstructable trace is expressed in |
| [3] | book [22] | **Law** | พระราชบัญญัติคุ้มครองข้อมูลส่วนบุคคล พ.ศ. ๒๕๖๒ / Personal Data Protection Act B.E. 2562 (2019) | `https://ratchakitcha.soc.go.th/documents/17082307.pdf` | ราชกิจจานุเบกษา (Royal Gazette), เล่ม ๑๓๖ ตอนที่ ๖๙ ก, หน้า ๕๒ | 27 May 2019 (๒๗ พฤษภาคม ๒๕๖๒) | 2026-09-05 | §3 the Thai box — data minimisation, retention/erasure and security as *design inputs*; the 72-hour breach-notification duty as an external clock on the incident loop |
| [4] | book [14] | **Study** (monitor) | *AIM: AI Incidents and Hazards Monitor* — with its *Overview and methodology* page | `https://oecd.ai/en/incidents/` · `https://oecd.ai/en/incidents-methodology` | OECD.AI (OECD) | Definitions published 17 May 2024; incident/hazard classification methodology in force since November 2024 | 2026-09-05 | §1 incident vs hazard definitions; §6 external recurrence scanning — and the caveat that entries are media-derived and not adjudications |

### Source-verification notes

- **[1] NIST AI 600-1.** `https://doi.org/10.6028/NIST.AI.600-1` resolves 302 → `https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf` on the canonical NIST domain, and the PDF was downloaded and text-extracted in full (cover page: "NIST Trustworthy and Responsible AI / NIST AI 600-1 … July 2024"). **A `HEAD` request to that PDF returns 404 while a plain `GET` returns 200** (both re-measured 2026-09-05) — a method artefact of NIST's CDN, not a dead link, and a link-checker that probes with `HEAD` will report a false failure. Do not "fix" the link. The landing page `https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence` also returns 200 if a non-PDF href is ever wanted. No errata or revision notice appears in the document.
- **[2] PROV-O.** 200 on `w3.org`. Still a live W3C Recommendation of 30 April 2013; **no obsoletion or superseding note present** on the access date.
- **[3] PDPA.** 200 on `ratchakitcha.soc.go.th`; the PDF is the authentic Royal Gazette text (เล่ม ๑๓๖ ตอนที่ ๖๙ ก, ๒๗ พฤษภาคม ๒๕๖๒). Sections quoted below were read from the extracted text, not from a summary.
- **[4] OECD.AI AIM.** 200 on `oecd.ai`; the listing URL normalises to a query-string form with an all-time date filter (`from_date=1900-09-05&to_date=2026-09-05`). The methodology page carries the definitions and the disclaimers. Both pages are on the canonical `oecd.ai` domain — no look-alike used. **Verification trail, not a citable reference:** the 17 May 2024 date for the definitions was confirmed on `https://oecd.ai/en/wonk/defining-ai-incidents-and-hazards` (200 on the same canonical domain, same publisher). Cite the date to **[4]**; do not add the wonk page to the post's reference list — that would be a fifth entry.
- **No additions.** The spec says "No additions", and none were made. Nothing in this post may cite a fifth source. The four `.references` entries are exactly [1]–[4] above.

### The book's own Boundary line for each of the four sources (D.3, printed pp 92–95) — verbatim

Every number card below repeats the relevant one. These are the master copies; a card's Boundary line must match a line here.

- **[1] NIST AI 600-1** (D.3 #4) — "**Supports:** GenAI-specific risk identification, measurement, management, incident learning, content provenance, and governance actions. **Boundary:** organizations must select and tailor actions to their use case and risk tolerance."
- **[2] W3C PROV-O** (D.3 #10) — "**Supports:** interoperable representation of entities, activities, agents, derivations, and provenance relationships for reconstructable evidence. **Boundary:** the ontology supplies a vocabulary, not a complete audit policy or storage design."
- **[3] PDPA B.E. 2562** (D.3 #22) — "**Supports:** the continued relevance of lawful personal-data processing, data-subject rights, safeguards, and controller or processor obligations to AI use. **Boundary:** this playbook offers no legal interpretation; official text and qualified Thai counsel control."
- **[4] OECD.AI AI Incidents and Hazards Monitor** (D.3 #14) — "**Supports:** external scanning for recurring incident and hazard patterns and the value of shared learning. **Boundary:** entries may draw on incomplete public reports; inclusion is not an official adjudication of facts or liability."

### Verbatim passages that carry the post's claims

**[1] NIST AI 600-1**

> **MG-2.3-001** — "Develop and update GAI system incident response and recovery plans and procedures to address the following: Review and maintenance of policies and procedures to account for newly encountered uses; Review and maintenance of policies and procedures for detection of unanticipated uses; Verify response and recovery plans account for the GAI system value chain; Verify response and recovery plans are updated for and include necessary details to communicate with downstream GAI system Actors: Points-of-Contact (POC), Contact information, notification format." *(under MANAGE 2.3)*

> **MG-4.3-001** — "Conduct after-action assessments for GAI system incidents to verify incident response and recovery processes are followed and effective, including to follow procedures for communicating incidents to relevant AI Actors and where applicable, relevant legal and regulatory bodies." *(under MANAGE 4.3: "Incidents and errors are communicated to relevant AI Actors, including affected communities. Processes for tracking, responding to, and recovering from incidents and errors are followed and documented.")*

> **MG-4.3-002** — "Establish and maintain policies and procedures to record and track GAI system reported errors, **near-misses**, and negative impacts." *(GAI Risks: Confabulation; Information Integrity)* — this is the standards hook for §6's near-miss argument.

> **MG-2.4-002 / MG-2.4-003** — "Establish and maintain procedures for escalating GAI system incidents to the organizational risk management authority when specific criteria for deactivation or disengagement is met…" / "Establish and maintain procedures for the remediation of issues which trigger incident response processes for the use of a GAI system, and provide stakeholders timelines associated with the remediation plan."

> **A.1.8 Incident Disclosure** — "AI incidents can be defined as an 'event, circumstance, or series of events where the development, use, or malfunction of one or more AI systems directly or indirectly contributes to one of the following harms: injury or harm to the health of a person or groups of people (including psychological harms and harms to mental health); disruption of the management and operation of critical infrastructure; violations of human rights or a breach of obligations under applicable law intended to protect fundamental, labor, and intellectual property rights; or harm to property, communities, or the environment.' AI incidents can occur in the aggregate (i.e., for systemic discrimination) or acutely (i.e., for one individual)."
> …and, on the state of the field: "Formal channels do not currently exist to report and document AI incidents. However, a number of publicly available databases have been created to document their occurrence. These reporting channels make decisions on an ad hoc basis about what kinds of incidents to track. Some, for example, track by amount of media coverage."
> …and: "Documentation practices including logging, recording, and analyzing GAI incidents can facilitate smoother sharing of information with relevant AI Actors. Regular information sharing, change management records, version history and metadata can also empower AI Actors responding to and…"

> **A.1.7 (provenance)** — "organizations can track and document the provenance of datasets to identify instances in which AI-generated data is a potential root cause of performance issues with the GAI system."

> **GV-1.5-002** (context for §7's recurrence metric) — the GOVERN action pairs "system incident response and incident disclosures, to identify gaps; Update … incident response and incident disclosure processes as required."

> Suggested actions elsewhere name the OECD monitor by name as an external sharing channel: "…external information sharing resources (e.g., AI incident database, AVID, CVE, NVD, or **OECD AI incident monitor**)" — this is the one place the two sources of this post touch, and it is the cleanest justification for §6.

**[2] W3C PROV-O**

> Abstract: the ontology "provides a set of classes, properties, and restrictions that can be used to represent and interchange provenance information generated in different systems and under different contexts."
> **Entity** — "An entity is a physical, digital, conceptual, or other kind of thing with some fixed aspects; entities may be real or imaginary."
> **Activity** — "An activity is something that occurs over a period of time and acts upon or with entities; it may include consuming, processing, transforming, modifying, relocating, using, or generating entities."
> **Agent** — "An agent is something that bears some form of responsibility for an activity taking place, for the existence of an entity, or for another agent's activity."

**[3] PDPA B.E. 2562 — verbatim Thai, with the section numbers**

> **มาตรา ๒๒** (data minimisation) — "การเก็บรวบรวมข้อมูลส่วนบุคคล ให้เก็บรวบรวมได้เท่าที่จำเป็นภายใต้วัตถุประสงค์อันชอบด้วยกฎหมายของผู้ควบคุมข้อมูลส่วนบุคคล"

> **มาตรา ๓๓ (๑)** (erasure when the purpose ends) — "เจ้าของข้อมูลส่วนบุคคลมีสิทธิขอให้ผู้ควบคุมข้อมูลส่วนบุคคลดำเนินการลบหรือทำลาย หรือทำให้ข้อมูลส่วนบุคคลเป็นข้อมูลที่ไม่สามารถระบุตัวบุคคลที่เป็นเจ้าของข้อมูลส่วนบุคคลได้ ในกรณีดังต่อไปนี้ (๑) เมื่อข้อมูลส่วนบุคคลหมดความจำเป็นในการเก็บรักษาไว้ตามวัตถุประสงค์ในการเก็บรวบรวม ใช้ หรือเปิดเผยข้อมูลส่วนบุคคล"

> **มาตรา ๓๗ (๑)** (security measures) — "จัดให้มีมาตรการรักษาความมั่นคงปลอดภัยที่เหมาะสม เพื่อป้องกันการสูญหาย เข้าถึง ใช้ เปลี่ยนแปลง แก้ไข หรือเปิดเผยข้อมูลส่วนบุคคลโดยปราศจากอำนาจหรือโดยมิชอบ และต้องทบทวนมาตรการดังกล่าวเมื่อมีความจำเป็นหรือเมื่อเทคโนโลยีเปลี่ยนแปลงไป … ทั้งนี้ ให้เป็นไปตามมาตรฐานขั้นต่ำที่คณะกรรมการประกาศกำหนด"

> **มาตรา ๓๗ (๓)** (a *system* for deleting data past its retention period — the exact hook for "retention design") — "จัดให้มีระบบการตรวจสอบเพื่อดำเนินการลบหรือทำลายข้อมูลส่วนบุคคลเมื่อพ้นกำหนดระยะเวลาการเก็บรักษา หรือที่ไม่เกี่ยวข้องหรือเกินความจำเป็นตามวัตถุประสงค์ในการเก็บรวบรวมข้อมูลส่วนบุคคลนั้น หรือตามที่เจ้าของข้อมูลส่วนบุคคลร้องขอ หรือที่เจ้าของข้อมูลส่วนบุคคลได้ถอนความยินยอม …"

> **มาตรา ๓๗ (๔)** (the 72-hour clock — the strongest external constraint on the incident loop) — "แจ้งเหตุการละเมิดข้อมูลส่วนบุคคลแก่สำนักงานโดยไม่ชักช้าภายในเจ็ดสิบสองชั่วโมงนับแต่ทราบเหตุเท่าที่จะสามารถกระทำได้ เว้นแต่การละเมิดดังกล่าวไม่มีความเสี่ยงที่จะมีผลกระทบต่อสิทธิและเสรีภาพของบุคคล ในกรณีที่การละเมิดมีความเสี่ยงสูงที่จะมีผลกระทบต่อสิทธิและเสรีภาพของบุคคล ให้แจ้งเหตุการละเมิดให้เจ้าของข้อมูลส่วนบุคคลทราบพร้อมกับแนวทางการเยียวยาโดยไม่ชักช้าด้วย …"

> **มาตรา ๒** (commencement) — "พระราชบัญญัตินี้ให้ใช้บังคับตั้งแต่วันถัดจากวันประกาศในราชกิจจานุเบกษาเป็นต้นไป เว้นแต่บทบัญญัติในหมวด ๒ หมวด ๓ หมวด ๕ หมวด ๖ หมวด ๗ และความในมาตรา ๙๕ และมาตรา ๙๖ ให้ใช้บังคับเมื่อพ้นกำหนดหนึ่งปีนับแต่วันประกาศในราชกิจจานุเบกษาเป็นต้นไป"

**[4] OECD.AI AIM**

> **AI incident** — "An event, circumstance or series of events where the development, use or malfunction of one or more AI systems directly or indirectly leads to" the listed harms.
> **AI hazard** — "An event, circumstance or series of events where the development, use or malfunction of one or more AI systems **could plausibly lead to**" the same categories of harm.
> Method — the AIM "retrieves AI-related incidents from news articles via Event Registry, which processes over 150,000 articles daily, then uses large language models to classify and enrich events with metadata." The listing page labels itself "Automated media discourse monitor of AI incidents and hazards (Beta)".
> Disclaimers — "The OECD cannot guarantee and does not independently verify the accuracy, completeness, or validity of third-party information"; "The information displayed in the AIM should not be reported as representing the official views of the OECD or of its member countries"; information "may contain various errors and omissions"; inclusion implies no endorsement.

---

## Claim classes in this post

| Class | Present? | Where | Handling |
|---|---|---|---|
| Material number | Yes | §2 eight stages · §3 nine groups, seven-item audit test · §3 Thai box 72 hours · §6 AIM entry count · §1/§8 five principles | One number card each, below. No card, no number. |
| Dated legal / standard status | Yes | §3 Thai box (PDPA + PDPC sub-regulations) · §2/§5 (NIST AI 600-1) · §3 (PROV-O) · §6 (AIM beta) | One dated sentence each, below. |
| Study finding | Yes (one, weak) | §6 — the AIM as an external scanning source | Monitor caveat mandatory: media-derived, LLM-classified, not adjudicated. |
| Direct quotation | Yes | §2 "learning is complete…" · §3 "'log everything forever' is not assurance" · §4/§5 "Do not reduce a system incident to 'the model hallucinated.'" · §8 Part-four opener · 💡 Ch9 principle 5 | Verbatim strings supplied below. Do not paraphrase inside quote marks. |
| Framework attribution | Yes | NIST AI RMF Govern/Map/Measure/Manage; PROV-O entity/activity/agent | Never described as equivalent to each other or to the book's loop (WARN W3). |
| Fictional-case value | Yes, heavily | §4 and §5 in full | Every one flagged `(กรณีสมมติจากหนังสือ)` / `(a fictional case from the playbook)` on first mention, and none in a metrics table as a target. |
| r8 paper numbers | **No** | — | Chapter 9's incident half carries no r8 figures. The 517-execution specimen belongs to #14. If a draft reaches for it, the rule below applies. |
| Masterclass video | **No** | — | Not cited in this post. Id verified anyway (below). |

---

## Number cards

Every material number in the post must match a card. Fictional-case values are **not** number cards — they are in "Fictional values".

### Card 1 — eight stages in the loop

- **Value / unit:** 8 stages.
- **Denominator / population:** the stage rows of Artifact 8's "Copy-ready loop" table (printed p 81 / PDF 82): *Detect and declare · Contain · Reconstruct · Classify · Diagnose · Correct · Verify and restore · Learn*.
- **Comparison — this is the trap, read it twice:** the book gives **three different namings** of the same loop and they must never be conflated.
  1. **Chapter 9 prose (printed p 39 / PDF 40) has NINE verbs**, including *Scope*: "Respond by detecting, containing, preserving evidence, **scoping**, diagnosing, remediating, reevaluating, recovering, and learning."
  2. **Figure 13 (drawn for this series) has EIGHT nodes** and drops *Scope*: `DETECT ตรวจพบ · CONTAIN จำกัดผล · PRESERVE รักษาหลักฐาน · DIAGNOSE วินิจฉัย · REMEDIATE แก้ไข · RE-EVALUATE ประเมินใหม่ · RECOVER กู้คืน · LEARN เรียนรู้`, around the core `EVIDENCE / BEFORE CHANGE / เก็บหลักฐาน / ก่อนแก้ระบบ`.
  3. **Appendix C glossary #36 "Incident-learning loop | วงจรเรียนรู้จากเหตุการณ์ผิดปกติ" has SEVEN verbs:** "Detect, contain, reconstruct, remedy, verify, communicate, and update controls so one failure reduces the probability or impact of recurrence."
  So: **§2 (the figure section) uses naming 2 and must say so. §5 (the worksheet) uses naming 1 of Artifact 8 — i.e. list 3 above is off-limits there.** Never write "the book's eight stages" without naming which artifact.
- **Task / setting:** responding to a prohibited effect, a severe or repeated semantic escape, trace loss, a privacy event, a control bypass, a drift signal, or a near miss in a bounded production AI system.
- **Source:** the playbook, Artifact 8 (printed 81–83 / PDF 82–84) and Chapter 9 (printed 39 / PDF 40) — **Synthesis** (author's own artifact), corroborated externally by [1] MG-2.3-001 and MG-4.3-001.
- **Boundary (the book's own):** Artifact 8's closing line — "Preserve the failed case before changing it. Do not reduce a system incident to 'the model hallucinated.' Ask which boundary admitted, trusted, authorized, released, or failed to observe the behavior." The loop is a working template, not a certified incident-management standard.
- **TH sentence:** "รูปที่ 13 วาดวงจรแปดขั้น — ตรวจพบ จำกัดผล รักษาหลักฐาน วินิจฉัย แก้ไข ประเมินใหม่ กู้คืน เรียนรู้ — หมุนรอบแกนกลางเดียวคือ เก็บหลักฐานก่อนแก้ระบบ"
- **EN sentence:** "Figure 13 draws an eight-stage loop — Detect, Contain, Preserve, Diagnose, Remediate, Re-evaluate, Recover, Learn — turning around a single core: evidence before change."

### Card 2 — nine event groups in the trace schema

- **Value / unit:** 9 event groups.
- **Denominator / population:** the rows of Artifact 6's English "Copy-ready schema" table (printed p 77 / PDF 78): *Identity · Release identity · Input and state · Context and retrieval · Checks · Generation · Effect · Release · Operations*.
- **Comparison — bilingual trap:** the book's own Thai mirror of the same table (printed p 78 / PDF 79) shows **eight** rows, because it merges *Release* and *Operations* into a single `Release/Operations` row and shortens *Release identity* to `Release`. **Use the nine-group English structure in BOTH tracks** and render nine rows in both — F8 requires TH and EN to carry identical numbers, and the merge is a book-side compression, not a different schema. Do not mirror the eight-row Thai table.
- **Task / setting:** defining observability, privacy controls, audit sampling, dispute response, and every release or effect path.
- **Source:** the playbook, Artifact 6 (printed 77–78 / PDF 78–79) — **Synthesis**; the vocabulary the schema is an instance of is [2] PROV-O.
- **Boundary (the book's own):** "Auditable means reconstructable, not safe." And: "Encrypt, restrict, redact and limit retention; 'log everything forever' is not assurance."
- **TH sentence:** "Trace schema ของหนังสือมีเก้ากลุ่ม event — Identity, Release identity, Input and state, Context and retrieval, Checks, Generation, Effect, Release และ Operations"
- **EN sentence:** "The playbook's trace schema has nine event groups — Identity, Release identity, Input and state, Context and retrieval, Checks, Generation, Effect, Release, and Operations."

### Card 3 — the auditability test has SEVEN items, not six

- **Value / unit:** 7 test items.
- **Denominator / population:** the single sentence closing Artifact 6's English schema. Verbatim: "Test whether an independent reviewer can identify the release, rebuild decision-time evidence, replay hard checks, **see scores with thresholds**, distinguish proposal from effect, verify final state and explain the route."
- **Comparison:** **the spec's §3 lists six** — it omits *see scores with thresholds*. The book's Thai mirror also has seven ("…เห็นทั้ง Score/Threshold…"). **Write seven.** If the writer keeps six for rhythm, the sentence must not be presented as the book's test.
- **Task / setting:** deciding whether a retained trace is sufficient before an authorized reviewer ever asks for it.
- **Source:** the playbook, Artifact 6 (printed 77 / PDF 78) — **Synthesis**.
- **Boundary:** "Auditable means reconstructable, not safe."
- **TH sentence:** "แบบทดสอบคือผู้ตรวจอิสระต้องทำได้เจ็ดอย่าง — ระบุ Release, สร้างหลักฐาน ณ เวลาตัดสินใจใหม่, Replay hard check, เห็นทั้ง score และ threshold, แยกข้อเสนอออกจากผลจริง, ยืนยัน final state และอธิบาย terminal route"
- **EN sentence:** "The test is whether an independent reviewer can do seven things: identify the release, rebuild decision-time evidence, replay the hard checks, see scores with their thresholds, distinguish proposal from effect, verify the final state, and explain the route."

### Card 4 — PDPA's 72-hour breach-notification clock

- **Value / unit:** 72 hours (เจ็ดสิบสองชั่วโมง).
- **Denominator / population:** counted from the moment the data controller becomes aware of the breach (นับแต่ทราบเหตุ), "as far as practicable" (เท่าที่จะสามารถกระทำได้), owed to the PDPC Office; and, where the breach carries a high risk to a person's rights and freedoms, to the data subject as well, together with remedial guidance, without delay.
- **Comparison:** the exception is explicit in the text — no notification is owed where the breach carries **no** risk to rights and freedoms. The detailed criteria and method are delegated to a PDPC announcement (ตามหลักเกณฑ์และวิธีการที่คณะกรรมการประกาศกำหนด), not fixed in the Act.
- **Task / setting:** the *Detect and declare* and *Contain* stages of the loop — the only externally-imposed clock in this post. Cite it as a design input on the incident runbook, never as advice on whether a given event qualifies.
- **Source:** [3] PDPA มาตรา ๓๗ (๔) — **Law**.
- **Boundary (the book's own, ref [22]):** "this playbook offers no legal interpretation; official text and qualified Thai counsel control."
- **TH sentence:** "PDPA มาตรา ๓๗ (๔) กำหนดให้ผู้ควบคุมข้อมูลส่วนบุคคลแจ้งเหตุละเมิดข้อมูลส่วนบุคคลต่อสำนักงานภายในเจ็ดสิบสองชั่วโมงนับแต่ทราบเหตุ เท่าที่จะสามารถกระทำได้ — บทความนี้ไม่ใช่คำแนะนำทางกฎหมาย"
- **EN sentence:** "PDPA section 37(4) requires a data controller to notify the PDPC Office of a personal-data breach within seventy-two hours of becoming aware of it, as far as practicable — this post is not legal advice."

### Card 5 — the OECD AIM's indexed volume

- **Value / unit:** about **17,392** entries labelled "incidents & hazards".
- **Denominator / population:** the AIM listing with an unfiltered all-time date range (the URL normalises to `from_date=1900-09-05&to_date=2026-09-05`), as displayed on 2026-09-05. It is a count of **media-derived, LLM-classified events**, not of adjudicated incidents, not of distinct systems, and not of harms.
- **Comparison:** none available on the page — no baseline, no rate, no denominator of deployed systems. **Therefore this number may not be used to express a trend, a growth rate, or a per-system probability.** Its only legitimate use is to show that an external corpus of this size exists to scan against.
- **Task / setting:** §6 — external scanning for recurring incident and hazard patterns before your own recurrence data is thick enough.
- **Source:** [4] OECD.AI AIM — **Study (monitor)**.
- **Boundary (the book's own, ref [14]):** "entries may draw on incomplete public reports; inclusion is not an official adjudication of facts or liability." Reinforced by OECD's own: "The OECD cannot guarantee and does not independently verify the accuracy, completeness, or validity of third-party information."
- **TH sentence:** "ณ วันที่ 5 กันยายน 2026 AI Incidents and Hazards Monitor ของ OECD.AI แสดงรายการราว 17,392 รายการ ซึ่งคัดจากข่าวและจัดหมวดด้วยโมเดลภาษา ไม่ใช่การชี้ขาดข้อเท็จจริงหรือความรับผิด"
- **EN sentence:** "On 5 September 2026 the OECD.AI AI Incidents and Hazards Monitor listed about 17,392 entries, drawn from news reporting and classified by language models — not adjudications of fact or liability."

### Card 6 — five operating principles

- **Value / unit:** 5 principles.
- **Denominator / population:** Chapter 9's "Five operating principles" block (printed p 40 / PDF 41). Every chapter in the book carries exactly five; they are never renumbered.
- **Comparison:** Chapter 8's five principles are different and must not be mixed in (the r8 chapter — see "Do not assert").
- **Task / setting:** the 💡 blockquote quotes exactly **principle 5**, per the spec's §6; the other four are listed in prose.
- **Source:** the playbook, Chapter 9 (printed 40 / PDF 41) — **Synthesis**.
- **Boundary:** these are the author's operating principles, not a standard's requirements.
- **Verbatim, all five (English):**
  1. "**Evidence before exposure** Do not increase the affected population ahead of proof."
  2. "**Evaluate the system in context** A model score is not workflow performance."
  3. "**Match gates to impact and reversibility** Stronger consequence demands stronger evidence."
  4. "**Make every release observable and reversible** A live system needs a service owner and kill path."
  5. "**Treat near misses overrides and corrections as evidence** Do not suppress the signals that teach the system." ← **the 💡 quote for this post**
- **Verbatim, all five (Thai, the book's own — use these, do not re-translate):**
  1. "มีหลักฐานก่อนเพิ่ม Exposure ไม่เพิ่มผู้ได้รับผลล่วงหน้ากว่าการพิสูจน์"
  2. "ประเมินระบบในบริบท Model Score ไม่ใช่ Workflow Performance"
  3. "ใช้ Gate ตามผลกระทบและการย้อนกลับ Consequence สูงต้อง Evidence สูง"
  4. "ทุก Release ต้องสังเกตและย้อนกลับได้ ระบบจริงต้องมี Service Owner และ Kill Path"
  5. "เก็บ Near Miss Override และ Correction เป็นหลักฐาน อย่ากดสัญญาณที่ช่วยสอนระบบ" ← **the 💡 quote for this post**

### Card 7 — PROV-O's three starting-point classes

- **Value / unit:** 3 classes.
- **Denominator / population:** PROV-O's "starting point" terms — `prov:Entity`, `prov:Activity`, `prov:Agent`.
- **Comparison:** PROV-O supplies a *vocabulary*; the nine-group schema in Card 2 is a domain instantiation of it. They are not the same artefact and not interchangeable.
- **Task / setting:** §3 — naming what the trace schema's groups *are* in provenance terms (a retrieved passage is an entity; a check is an activity; an approving principal is an agent).
- **Source:** [2] W3C PROV-O — **Standard**.
- **Boundary (the book's own, ref [10]):** "the ontology supplies a vocabulary, not a complete audit policy or storage design."
- **TH sentence:** "PROV-O ของ W3C ให้คำศัพท์กลางสามชนิด — entity (สิ่งที่ถูกกระทำ) activity (การกระทำที่กินเวลา) และ agent (ผู้รับผิดชอบ) — ซึ่งเป็นคำศัพท์ ไม่ใช่นโยบายการตรวจสอบหรือแบบการจัดเก็บ"
- **EN sentence:** "W3C's PROV-O supplies three starting-point classes — entity, activity and agent — a vocabulary for provenance, not an audit policy or a storage design."

---

## Dated statuses

Each is one dated sentence. Use them as written, or keep the date.

1. **NIST AI 600-1** — "NIST published *AI 600-1, the Generative AI Profile of the AI Risk Management Framework*, in **July 2024**; on **5 September 2026** the DOI still resolves to the same edition on `nvlpubs.nist.gov` with no errata or revision notice, and its actions remain **voluntary suggested actions**, not requirements."
2. **W3C PROV-O** — "PROV-O has been a **W3C Recommendation since 30 April 2013**, and on **5 September 2026** the document carries no obsoletion or superseding note."
3. **Thailand's PDPA** — "The Personal Data Protection Act B.E. 2562 was published in the Royal Gazette on **27 May 2019** (เล่ม ๑๓๖ ตอนที่ ๖๙ ก) and its operative chapters — including the controller's duties in section 37 — took effect one year after publication under section 2; it remained in force as checked on **5 September 2026**."
4. **PDPC sub-regulations** — "The PDPC continues to issue sub-regulations under the Act; on **5 September 2026** the committee's announcement index at `pdpc.or.th` listed its most recent announcement as dated **21 July 2026 (๒๑ ก.ค. ๒๕๖๙, on access and copies of personal data)**, which is why section 37(1)'s security measures and section 37(4)'s breach-notification method are described here as *delegated to announcements* rather than fixed in the Act." — *Partial verification: the 2022 announcements on security measures and on breach notification did not appear on the index page as fetched, so this post must not cite them by title or date.*
5. **OECD.AI AIM** — "On **5 September 2026** the OECD.AI AI Incidents and Hazards Monitor described itself as an 'Automated media discourse monitor of AI incidents and hazards (**Beta**)', with its definitions published **May 2024** and its methodology last updated **November 2024**."

### Dated-status re-checks deliberately SKIPPED (and therefore off-limits in this post)

The spec's research targets are four sources and says "No additions." The following were not fetched and **must not appear** anywhere in #15: Thailand's dedicated AI law / ร่างพระราชบัญญัติปัญญาประดิษฐ์ (belongs to #16 — this post only *points forward* to it, with no status claim); EU AI Act application dates or any 2026 amendment (#16); the NIST June 2026 "monitor and update" item (#14/#16); Stanford AI Index 2026 figures; IEA 2026 figures; ISO/IEC 42005:2025 status; ETDA guideline versions.

---

## Fictional values

All of these are illustrative fiction from the playbook. Flag the case `(กรณีสมมติจากหนังสือ)` / `(a fictional case from the playbook)` **on first mention in each track**, and never place any of these numbers in a metrics table as a target or a benchmark.

**Case identity:** Luma Commerce Thailand · scenario `CX-REFUND-01` · regression case `CXGS-241` · manifests `rc4` → `rc5` · review owner "N. Kanya" (Artifact 7's completed decision row) · rollback target `prod2`. The manifest's full identifier, where §4 needs it, is `CX-REFUND-01.2026-09-rc4, parent 2026-08-prod2` (verified by full-text search of the PDF). Scope note from the book: "All examples use CX-REFUND-01, a fictional Luma Commerce Thailand assistant."

> **Correction made during verification, 2026-09-05.** An earlier draft of this ledger listed an "incident record `INC-CX-014`". **That string does not exist anywhere in the book** — a full-text extraction of all 97 pages (`pdftotext -layout`) returns zero matches for `INC-CX`. It was fabricated. **Do not use it.** The incident in Artifact 8 carries no record id; the only ids the book gives this incident are the scenario name `CX-REFUND-01`, the regression case `CXGS-241`, and the manifests `rc4` / `rc5`. If the draft wants an incident-record id for the worked worksheet, it must be introduced as the writer's own placeholder and flagged fictional alongside the rest.

**§4 incident narrative (Artifact 8, printed 81–82 / PDF 82–83):** 25% rollout · a 60-day eligibility statement from an obsolete but allow-listed promotion page · the model proposed **THB 2,400 on day 45** · execution guard blocked the payment · output rail released the wrong explanation · corpus dated `2026-09-01` · classified **severe semantic policy escape plus near miss**, structural execution invariant held · rolled back to manifest `rc4` · new manifest `rc5` · restored at **5% with 24-hour review** · **seven-day** recurrence monitor.

**§3 completed trace (Artifact 6, printed 77–78 / PDF 78–79):** `tr-8A41` · request `rq-771` · customer `c-204` · order `o-919` · Thai locale · manifest `rc4` · `10:42:16+07` · **six** ordered policy/order passages · input accept **0.08 below 0.65** · context-support **0.91 above 0.85** · proposed `issue_refund(order=o-919, amount=1850, currency=THB)` · transaction key `rf-o919-1` · post-state refund **1,850 committed once** · output support **0.97 above 0.92** · **1.8-second** latency · retention class `CX-FIN-24M` · no incident.

**Release-gate figures carried in from Artifact 7 (printed 79–80 / PDF 80–81) — use only if §4 needs the pre-incident baseline:** **94.6%** weighted success · priority slices at least **89.1%** · support **96.8%** · estimated false accepts **1.7%** · p95 **3.4 seconds** · rollback drill **11 minutes** · approve `rc4` at **5%**, then **25%** only after **48-hour** review.

**Series-wide fictional values that belong to OTHER posts and must NOT appear here:** THB 2,000 · 41.3% · 240 cases · 18 min / 46 h · 80,000 letters. **THB 2,500** is Chapter 8's proposal example and may appear only as an explicit callback to #13/#14, flagged as fictional.

---

## Author-supplied and unpublished — the r8 rule

The Mingkhwan r8 paper is **author-supplied and unpublished. Never link it.** It is labelled **Synthesis** with the note "author-supplied, unpublished, no public URL". This post's chapter half carries **no** r8 figures, so the expected outcome is that r8 does not appear at all. If a draft does reach for the 517-execution specimen, it must carry the book's boundary sentence in the same breath, verbatim:

> "The r8 paper includes a deliberately bounded authored specimen of 517 deterministic executions. In its fixed suite, the full envelope completed 30 of 30 benign cases, allowed zero of 40 policy escapes and zero of six prohibited refund effects, and recorded 70 of 70 route traces. Adaptive-to-implementation tests exposed soft-control limits: eight of twelve violating candidates were released, while hard execution mediation blocked all four prohibited effect attempts. **This illustrates wiring and failure localization in author-constructed fixtures. It does not establish production quality, independent red-team robustness, legal compliance, or a population safety rate.**"

Thai boundary, verbatim: "ผลนี้แสดงการเชื่อม Control และตำแหน่ง Failure ใน Fixture ที่ผู้เขียนสร้าง ไม่ได้พิสูจน์ Production Quality, Independent Red Team, Legal Compliance หรือ Population Safety Rate"

The book's own reference-list entry for the paper (D.3 #1, printed p 92) is the citation form to copy, and carries a second, shorter boundary usable when the long one will not fit:

> "Mingkhwan, Anirach. **Engineering AI-Core Systems: A Reference Architecture and Assurance Contract for Software 3.0, revision 8 (September 2026).** Author-supplied paper attached to this project. **Boundary:** the specimen demonstrates mechanisms under declared tests; it is not a production prevalence estimate or universal benchmark."

The same D.3 page states the rule this ledger enforces, in the book's own voice: "The first source is an unpublished, author-supplied paper and therefore has no public URL; it is identified transparently rather than assigned an invented link."

## Masterclass video

Not cited in this post. The id was verified anyway on 2026-09-05: `https://www.youtube.com/watch?v=n_IwUYevRZo` returns the video titled **"AI Transformation: จากการใช้ AI สู่องค์กรที่เรียนรู้เร็วที่สุด | The Masterclass EP01"**. Channel, upload date and duration were **not** recoverable from the fetched page, so none may be asserted. Paraphrase only, never quote; no timestamps are cited in this post, so none were verified.

---

## Verbatim strings the post will quote

Copy these exactly; do not paraphrase inside quote marks.

**§2 — the closing sentence of Chapter 9's incident paragraph (printed 39–40 / PDF 40–41):**
> EN: "Learning is complete only when the corrective control or design change is verified and recurrence is monitored."
> TH: "การเรียนรู้สมบูรณ์เมื่อ Control หรือ Design ใหม่ผ่านการยืนยันและติดตามการเกิดซ้ำ"
> *Note: the spec's §2 shortens this to "the corrective change is verified". If quoted, use the full "corrective control or design change".*

**§1 — incident vs near miss / hazard (printed 39–40 / PDF 40–41):**
> EN: "An incident is a realized harm. A near miss or hazard reveals credible harm before full impact."
> TH: "Incident คือความเสียหายที่เกิดจริง ส่วน Near Miss หรือ Hazard เปิดเผยอันตรายที่น่าเชื่อถือก่อนเกิดเต็มรูปแบบ"
> *Note: the book treats near miss and hazard as one pair. The three-way split the spec asks for needs [4]'s separate hazard definition ("could plausibly lead to") to be honest. Attribute accordingly.*

**§1/§2 — the response sequence (printed 39 / PDF 40), NINE verbs:**
> "Respond by detecting, containing, preserving evidence, scoping, diagnosing, remediating, reevaluating, recovering, and learning. Bound effects first, preserve the manifest and traces before modification, inspect authoritative external state, and add both the actual case and hidden neighboring cases to evaluation."

**§3 — the retention `.alert` (printed 77 / PDF 78):**
> EN: "Encrypt, restrict, redact and limit retention; 'log everything forever' is not assurance."
> TH: "ต้องเข้ารหัส จำกัดสิทธิ แสดงผลแบบ Redact และเก็บตามวัตถุประสงค์ การ 'เก็บทุกอย่างตลอดไป' ไม่ใช่ Assurance"

**§3 — purpose and the auditable line (printed 77 / PDF 78):**
> "Preserve enough evidence for a later authorized reviewer to reconstruct what the system knew, proposed, checked, did, released, and why it chose that route. **Auditable means reconstructable, not safe.**"
> TH: "เก็บหลักฐานให้ผู้ตรวจที่มีสิทธิย้อนสร้างได้ว่าระบบรู้อะไร เสนออะไร ตรวจอะไร ทำอะไร ปล่อยอะไร และเลือก Route เพราะเหตุใด Auditable แปลว่าย้อนสร้างได้ ไม่ได้แปลว่าปลอดภัย"

**§3 — accountable owners (printed 77 / PDF 78):**
> "SRE or platform owner guarantees durable capture; data protection owns minimization and retention; the decision owner reviews meaning."

**§4/§5 — Artifact 8's closing rule (printed 81 / PDF 82):**
> EN: "Preserve the failed case before changing it. Do not reduce a system incident to 'the model hallucinated.' Ask which boundary admitted, trusted, authorized, released, or failed to observe the behavior."
> TH: "เก็บกรณีเสียก่อนแก้ และอย่าสรุปเพียงว่า 'โมเดลหลอน' ต้องถามว่า Boundary ใดยอมรับ เชื่อ อนุญาต ปล่อย หรือมองไม่เห็นพฤติกรรมนั้น"

**§5 — Artifact 8 purpose and trigger (printed 81 / PDF 82):**
> "Turn a failure into containment, evidence, verified correction and organizational memory. **Use when** a prohibited effect, severe or repeated semantic escape, trace loss, privacy event, control bypass, drift signal or near miss occurs. **Accountable owner** Incident commander coordinates; decision, engineering, security, privacy and people owners retain their domain obligations."

**§8 — the Part four opener (printed 42 / PDF 43):**
> "Part four treats **governance as an operating system rather than a committee**, work redesign as a social choice rather than an afterthought, and the first 180 days as a proof of one complete learning loop rather than a competition to launch the most tools."

---

## Worksheet and agenda source text (verbatim, for §5 and §7)

**Artifact 8, "Copy-ready loop" — Stage / Record and decide (printed 81 / PDF 82).** The spec's worksheet columns are Action / Evidence / Owner / Done-when; the book's single "Record and decide" column supplies the content to distribute across them. Do not invent stages.

| Stage | Record and decide (verbatim EN) | Record and decide (verbatim TH) |
|---|---|---|
| Detect and declare | "Signal, time, affected scope, provisional severity, commander" | "Signal เวลา Scope Severity เบื้องต้น Commander" |
| Contain | "Capability, traffic or slice disabled; customer remedy; rollback; evidence preservation" | "ปิด Capability/Traffic/Slice, เยียวยา, Rollback, เก็บหลักฐาน" |
| Reconstruct | "Trace, manifest, context, source, checks, proposal, effect, output, final state" | "Trace, Manifest, Context, Source, Check, Proposal, Effect, Output, Final State" |
| Classify | "Harm and near miss; structural breach versus semantic escape; affected people and obligations" | "Harm/Near Miss, Structural Breach หรือ Semantic Escape, ผู้ได้รับผลและภาระ" |
| Diagnose | "Technical, data, workflow, ownership and incentive causes; why detection or response failed" | "สาเหตุด้านเทคนิค ข้อมูล Workflow Ownership Incentive และเหตุที่ตรวจหรือรับมือไม่ทัน" |
| Correct | "Immediate fix, durable control, owner, due date; update contract, manifest, runbook and training" | "Immediate/Durable Fix, เจ้าของ, Due Date และการปรับ Contract, Manifest, Runbook, Training" |
| Verify and restore | "New regression case, hidden/adaptive tests, state oracle, independent review, staged exposure" | "Regression, Hidden/Adaptive Test, State Oracle, Independent Review, Staged Exposure" |
| Learn | "Communicate, compensate, monitor recurrence, share pattern across products, close only with evidence" | "สื่อสาร ชดเชย เฝ้าการเกิดซ้ำ แชร์ข้ามผลิตภัณฑ์ และปิดด้วยหลักฐานเท่านั้น" |

**Chapter 9 working session, "Release readiness room" (printed 40 / PDF 41), verbatim:**
> "Restate the decision, users, affected parties, and baseline. Identify routine, boundary, adversarial, and severe cases. Review results and evidence gaps. Select the release stage, population, oversight mode, and stop thresholds. **Rehearse detection, containment, rollback, notification, and remedy for one failure.** Record the decision, owner, monitoring cadence, and next review date."
> *Only the fifth step is an incident-loop step; the rest is #14's release-gate material. If §5's worked worksheet needs a rehearsal agenda, this is the sentence to use — do not present the whole agenda as an incident agenda.*

**Chapter 9 "Metrics that matter" (printed 40 / PDF 41), verbatim, complete:**
> "Track quality-adjusted task success, critical-error rate, supported claims, security escapes, subgroup disparity, override and reversal, feedback latency, drift, cost per successful outcome, **time to detect contain and recover, near-miss reporting, recurrence**, and releases with a tested rollback."

**Chapter 9 "Failure patterns" (printed 40 / PDF 41), verbatim, complete:**
> "One average score, irrelevant benchmarks, testing only easy English cases, releasing to everyone, treating vendor testing as sufficient, no versioned evidence, ceremonial approval, **suppressed near misses**, and **closing an incident after service restoration without verifying corrective action**."

### Two metrics in the spec that are NOT in the book — attribute them correctly

The spec's §7 metrics list contains six items. Four are the book's: *time to detect / contain / recover*, *recurrence*, *near-miss reporting rate*, and (by inversion of the failure list) closure discipline. **Two are not in the book's "Metrics that matter" list:**

- "share of incidents with a named regression case" — derivable from Artifact 8's *Verify and restore* row ("New regression case…") and its worked value `CXGS-241`, but it is **author/editorial synthesis**, not a book metric.
- "time from verified incident to reusable control improvement" — derivable from Artifact 8's *Learn* row ("share pattern across products") and from the book's *learning velocity* definition (Appendix C #3), but it is likewise **synthesis**.

Both may be used. Neither may be introduced with "the book tracks…" or footnoted to the chapter's metrics list. Introduce them as extensions, e.g. "สองตัวชี้วัดที่ผมเพิ่มเอง" / "two measures I add to the chapter's list".

The spec's four failure patterns all map to the book: *closing after service restoration without verified correction* (verbatim above), *suppressed near misses* (verbatim above), *"the model hallucinated" as root cause* (Artifact 8's closing rule), *modifying the manifest before preserving it* (Chapter 9: "preserve the manifest and traces before modification"; Artifact 8: "Preserve the failed case before changing it").

---

## Glossary check

Every coinage below must appear in its Appendix C Thai rendering **verbatim on first mention**, English inline afterwards. Renderings confirmed against the book's Appendix C (PDF 85–91), not against the plan summary.

| Coinage | Canonical Thai (Appendix C) | Appendix C # | Notes for this post |
|---|---|---|---|
| Reconstructable trace | ร่องรอยที่สร้างเหตุการณ์ย้อนกลับได้ | 26 | **ย้อนกลับ**, not ย้อนหลัง. Fig 10's core bar in the figure spec reads ย้อนหลัง — that is the figure's own string; prose uses the glossary form. |
| Incident-learning loop | วงจรเรียนรู้จากเหตุการณ์ผิดปกติ | 36 | Its English definition is a **seven-verb** loop (see Card 1). Use the term; do not import its seven verbs as "the stages". |
| Observability | ความสามารถในการสังเกตระบบ | 35 | Tag word for the post. |
| Provenance | ที่มาของข้อมูลและผลลัพธ์ | 25 | Used in §3 (Context and retrieval group) and to link [1]'s provenance actions. |
| Learning loop | วงจรการเรียนรู้ | 2 | Distinct from #36. Do not swap them. |
| Fail-safe state | ภาวะปลอดภัยเมื่อระบบล้มเหลว | 37 | §2 Contain / §4 route-to-people. |
| Structural guarantee | การรับประกันเชิงโครงสร้าง | 30 | §4 — "structural execution invariant held". |
| Semantic estimate | ค่าประเมินเชิงความหมาย | 31 | §4 — "severe semantic policy escape". The escape/guarantee contrast is the post's spine; the plan flags this pair as at-risk of drift. |
| Release gate | ด่านอนุมัติการนำระบบออกใช้ | 34 | Callback to #14 only. |
| Assurance envelope | กรอบการรับประกันรอบระบบ | 27 | Callback to #13/#14 only. Do not confuse with *assurance contract* = สัญญาการรับประกันเชิงระบบ. |
| Runtime-context manifest | บัญชีรายการบริบทขณะทำงาน | 20 | The thing preserved before change (`rc4` → `rc5`). |
| Proposal–effect separation | การแยกข้อเสนอออกจากผลจริง | 21 | §4 — the guard blocked the payment while the output rail leaked. |
| Effect mediation | การควบคุมก่อนเกิดผล | 22 | Same. |
| Human oversight | การกำกับดูแลโดยมนุษย์ | 40 | §4 — promotion cases routed to people. |
| Impact assessment | การประเมินผลกระทบ | 39 | English inline after first mention, per the plan's kept-in-English list. |
| Accountability | ความรับผิดรับชอบ | 44 | §5 owner column. |

**Kept in English inline (the book's own practice):** Trace, Manifest, Rollback, Threshold, Escalation, Release, Regression test, Retrieval, Override, Guard, Canary, Runbook, Dashboard, Fallback.
**No deviations from the canonical renderings are proposed by this post.**

---

## Do not assert

Things searched for and not established, or established only in a weaker form than a draft is likely to want.

1. **Do not assert that OECD AIM entries are verified facts, confirmed incidents, or determinations of liability.** They are media-derived and LLM-classified; the OECD states it "does not independently verify" them. §6 must carry a monitor caveat word.
2. **Do not assert any AIM trend, growth rate, year-on-year change, or per-system incidence.** Only the one-day count in Card 5, with its all-time filter stated. No denominator of deployed systems exists on the page.
3. **Do not assert a "last updated" date for the AIM listing itself.** None was recoverable; only the methodology (November 2024) and definitions (May 2024) dates are verified.
4. **Do not assert that NIST AI 600-1 *requires* anything.** Its content is "Suggested Actions"; the framework is voluntary. "NIST suggests" / "NIST AI 600-1 lists an action to…" — never "NIST mandates".
5. **Do not assert that NIST AI 600-1 defines an incident in its own voice.** A.1.8 quotes the definition from elsewhere ("AI incidents can be defined as an 'event, circumstance, or series of events…'"). Present it as the definition NIST reproduces.
6. **Do not assert that formal AI-incident reporting channels now exist.** NIST's A.1.8 states the opposite as of July 2024 ("Formal channels do not currently exist to report and document AI incidents"), and nothing in the four verified sources updates that. Anything about a 2026 reporting regime is unverified here.
7. **Do not assert that PROV-O is an audit-log standard, a retention standard, or a schema for AI traces.** Book boundary [10]: "the ontology supplies a vocabulary, not a complete audit policy or storage design."
8. **Do not assert any PDPA interpretation** — that a given trace field is or is not personal data, that a given retention class is lawful, that a given event is or is not a reportable breach, or that any specific retention period is required. PDPA fixes no trace-retention period. Book boundary [22]: "this playbook offers no legal interpretation; official text and qualified Thai counsel control." The Thai box must say so and point to #16.
9. **Do not cite the 2022 PDPC announcements by title or date.** The security-measures and breach-notification announcements did not appear on the PDPC announcement index as fetched on 2026-09-05; only secondary sites carried them, and secondary sites are not acceptable here. Say instead that the Act delegates the method to committee announcements (มาตรา 37(1) and 37(4) both say so, verbatim above).
10. **Do not assert anything about Thailand's dedicated AI law, the EU AI Act, ISO/IEC 42005, ETDA guidelines, the NIST June 2026 item, AI Index 2026, or IEA 2026 in this post.** None was a research target, none was fetched, and the spec says "No additions." §8 points forward to #16 without a status claim.
11. **Do not write "the book's eight-stage loop" unqualified.** Three namings exist (Card 1). Name the artifact: "Figure 13's eight stages" or "Artifact 8's eight stages" — and do not blend the two label sets in one list.
12. **Do not write that Chapter 9's prose gives eight stages.** It gives nine verbs, including *Scope*.
13. **Do not write that the auditability test has six parts** without dropping the book attribution. It has seven (Card 3).
14. **Do not mirror the eight-row Thai trace table.** Nine groups in both tracks (Card 2).
15. **Do not present "share of incidents with a named regression case" or "time from verified incident to reusable control improvement" as the book's metrics.** They are synthesis (see above).
16. **Do not let any fictional value into a metrics table as a target, a floor, or a benchmark** — 94.6%, 96.8%, 89.1%, 1.7%, p95 3.4 s, 11 minutes, 1.8 s, 0.65/0.85/0.92 included.
17. **Do not link the r8 paper** under any circumstances, and do not cite its numbers without the boundary sentence in the same breath.
18. **Do not quote the masterclass video**, and do not state its channel, upload date, or duration — none was recoverable.
19. **Do not mix Chapter 8's five operating principles with Chapter 9's.** This post quotes Chapter 9 principle 5 in the 💡 blockquote; the other four Chapter 9 principles go in prose. Principles are never renumbered.
20. **Do not treat "near miss" and "hazard" as the book's two distinct categories.** The book pairs them ("A near miss or hazard reveals credible harm before full impact"); the three-way split in §1 needs [4]'s hazard definition to stand up.
21. **Do not use the string `INC-CX-014`, or any other incident-record id, as if the book supplied one.** Full-text extraction of all 97 pages returns zero matches for `INC-CX`; the id was fabricated in an earlier draft of this ledger and removed on 2026-09-05. The book's ids for this incident are `CX-REFUND-01`, `CXGS-241`, `rc4`, `rc5`, `prod2` and the full manifest identifier `CX-REFUND-01.2026-09-rc4, parent 2026-08-prod2`.
22. **Do not describe the OECD monitor's May 2024 definitions as a standard, a taxonomy in force, or a legal definition.** They are the OECD's published definitions for its own monitor, arrived at through an expert group; they bind nobody. The dated sentence in "Dated statuses" is the only form to use.
23. **Do not date the AIM entry count to anything but the access date, and do not re-use 17,392 in a later edit without re-counting.** The number moves daily; it is a live-page reading, not a published statistic.
