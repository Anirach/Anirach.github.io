# Research ledger — `ai-transformation-learning-loop` (post #3 of 20)

**Post:** Build a Learning System — วงจรการเรียนรู้ที่คู่แข่งซื้อไม่ได้
**Book source:** *AI Transformation as an Organizational Core — Bilingual Companion Playbook*, Chapter 1 "Build a learning system / บทที่ 1 สร้างระบบการเรียนรู้", printed pp. 8–10 (PDF pp. 9–11).
**Access date for every source below:** **2026-09-05** (Asia/Bangkok).
**Book evidence snapshot:** 5 September 2026 (Asia/Bangkok) — book D.2.
**Layer stamp for this post:** Learning loop · **Q1** ("Which organizational outcome are we trying to improve and how quickly can we learn whether we did", book p2) · Scorecard column **Learning**.

> **Binding rule.** Writers may not introduce a source, a number, a date or a quotation that is not in this ledger. Anything in the "Do not assert" section is out of bounds even if it is true.

---

## 0. Claim classes in this post

| Class | Present in this post? | Where | Ledger section |
|---|---|---|---|
| Material number | Yes — structural counts only (5 moves, 5 principles, 6 canvas steps, 10 metrics, 75 minutes, 7 figure nodes / 3 figure measures) | §2 `five-moves`, §6 `canvas`, §7 `metrics-failures` | Number cards |
| Dated legal/standard status | Yes — NIST AI RMF 1.0; ISO/IEC 42001:2023 | §3 `learning-engine` | Dated statuses |
| Study finding | **No.** This post cites no empirical study. No survey %, no productivity number, no adoption %. | — | Do not assert |
| Direct quotation | Yes — one of the book's five operating principles in the 💡 blockquote (book is the source, label Synthesis). No external source is quoted. | §5 `five-principles` | Number cards / §4 below |
| Framework attribution | Yes — NIST AI RMF (Govern/Map/Measure/Manage), ISO/IEC 42001 (continual improvement), Argyris double-loop learning, Mingkhwan r8 boundary claim | §3 `learning-engine` | Sources |
| Fictional-case value | Yes — Aurora Assurance, 80,000 letters, the three outcomes, the two-policy slice | §4 `aurora` | Fictional values |

---

## Sources

| [N] | Label | Title | URL | Publisher | Pub date | Accessed | Supports |
|---|---|---|---|---|---|---|---|
| [1] | Synthesis | Mingkhwan, Anirach. *Engineering AI-Core Systems: A Reference Architecture and Assurance Contract for Software 3.0*, revision 8 | **none — author-supplied, unpublished. NEVER LINK.** | Author-supplied paper attached to the playbook project | September 2026 | 2026-09-05 | "When model output becomes both authoritative and indispensable for a declared task, assurance must move to the boundaries around the model" → organizationally, learning cannot stop at model tuning; the whole decision system must improve. |
| [3] | Standard | *AI Risk Management Framework* (landing page) + *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*, NIST AI 100-1 | `https://www.nist.gov/itl/ai-risk-management-framework` (HTTP 200) · document: `https://doi.org/10.6028/NIST.AI.100-1` → `https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf` (HTTP 200) | National Institute of Standards and Technology (NIST), U.S. Department of Commerce | Framework released **26 January 2023**; cover date January 2023 | 2026-09-05 | Voluntary lifecycle risk discipline; the four core functions GOVERN, MAP, MEASURE, MANAGE; that the actions "do not constitute a checklist". |
| [11] | Standard | *ISO/IEC 42001:2023 — Information technology — Artificial intelligence — Management system* | `https://www.iso.org/standard/42001` (HTTP 200 in a real browser — see fetch note) | International Organization for Standardization / IEC | Publication date **2023-12**, Edition 1, Status **Published**, stage 60.60 | 2026-09-05 | "Requirements for establishing, implementing, maintaining, and **continually improving** an Artificial Intelligence Management System (AIMS) within organizations." Continual improvement as loop discipline. |
| [A] | Synthesis | Argyris, Chris. "Teaching Smart People How to Learn" | `https://hbr.org/1991/05/teaching-smart-people-how-to-learn` (HTTP 200, paywalled preview) | Harvard Business Review (Harvard Business School Publishing) | **May–June 1991** | 2026-09-05 | That professionals presumed best at learning are in fact poor at it — the intellectual ancestor of "change the right part of the system". |
| [A2] | Synthesis | Argyris, Chris. "Double Loop Learning in Organizations" | `https://hbr.org/1977/09/double-loop-learning-in-organizations` (HTTP 200, paywalled preview) | Harvard Business Review (Harvard Business School Publishing) | **September 1977** | 2026-09-05 | Attributes the *term* "double-loop learning" to Argyris on the publisher's own domain. Use **only** if the post names the term; see the Argyris rule below. |
| [B] | Synthesis | *AI Transformation as an Organizational Core — Bilingual Companion Playbook*, Chapter 1 | (the book itself; no public URL) | Anirach Mingkhwan | 2026 (evidence snapshot 5 Sept 2026) | 2026-09-05 | Everything structural in this post: the five moves, the five operating principles, the canvas agenda, the ten metrics, the failure patterns, Aurora. |

### Fetch notes

- **[3] NIST** — landing page fetched at HTTP 200; publication date on the page is 26 January 2023. The AI RMF 1.0 PDF was fetched from `nvlpubs.nist.gov` (via the DOI 302) at HTTP 200 and the verbatim passages below are taken from it.
- **[11] ISO** — `iso.org` returns **HTTP 403 to every automated fetcher** (curl with a browser UA, WebFetch, Firecrawl all 403 — Cloudflare bot mitigation). Retrieved successfully with a **real browser (Playwright)** on 2026-09-05: page title `ISO/IEC 42001:2023 - AI management systems`, General information block reads `Status: Published`, `Publication date: 2023-12`, `Stage: International Standard published [60.60]`, `Edition: 1`, `Number of pages: 51`. **Handoff to the fact-check agent: F2 on this URL must be checked in a browser, not with curl — a 403 here is bot mitigation, not a dead link.**
- **[A]/[A2] HBR** — both URLs return HTTP 200 with a free preview and a subscription wall. The free preview of the 1991 article shows **only the opening paragraph**; the single-loop / double-loop / thermostat / defensive-reasoning passages are behind the wall and were **not** verified verbatim on the publisher's domain.
- **Masterclass video** (instruction 8, verified even though this post does not cite it): id **`n_IwUYevRZo`** confirmed live at HTTP 200. Title `AI Transformation: จากการใช้ AI สู่องค์กรที่เรียนรู้เร็วที่สุด | The Masterclass EP01`, uploader **The Foundation (th)**, uploaded **2026-08-28**, duration **52 minutes** — matches book source [2] exactly. **No timestamp is cited in this post, and this post must not cite the video at all** (not in the spec's Research targets). If a later edit adds it: paraphrase only, never quote, and never attribute the book's own synthesis to the presenter.

### Verbatim supporting passages

**[B] The chapter argument — §1 `cannot-buy` (book p8, EN):**
> "The durable advantage is not access to a model. It is the ability to convert operating experience into safer and more valuable behavior."
>
> "AI transformation is not the installation of a model. It is the creation of an organizational learning system that can improve decisions faster than its environment changes. Models, policies, customer behavior, data, and threats all move. Competitors can often obtain similar foundation models and cloud services. What they cannot buy in one transaction is the ability to see what happened, preserve the evidence, change the right part of the system, and verify the result before the next release."

**[B] The chapter argument (book p9, TH):**
> "การเปลี่ยนผ่านด้วย AI ไม่ใช่การติดตั้งโมเดล แต่คือการสร้างระบบการเรียนรู้ขององค์กร ที่ทำให้การตัดสินใจดีขึ้นได้เร็วกว่าสภาพแวดล้อมที่เปลี่ยนไป ทั้งโมเดล นโยบาย พฤติกรรมลูกค้า ข้อมูล และภัยคุกคามล้วนไม่หยุดนิ่ง คู่แข่งอาจซื้อโมเดลและบริการ Cloud แบบเดียวกันได้ แต่ไม่สามารถซื้อความสามารถในการมองเห็นสิ่งที่เกิดขึ้น เก็บหลักฐาน ปรับส่วนที่ถูกต้องของระบบ และยืนยันผลก่อนปล่อยรุ่นถัดไปได้ในครั้งเดียว"

**[B] The chapter's epigraph, TH (book p8, under the bilingual chapter title):** บทที่ 1 สร้างระบบการเรียนรู้ — the EN epigraph above is the book's; there is no separate Thai epigraph line.

**[3] NIST AI RMF 1.0 — voluntary (p. 2):**
> "The Framework is intended to be voluntary, rights-preserving, non-sector-specific, and use-case agnostic, providing flexibility to organizations of all sizes and in all sectors and throughout society to implement the approaches in the Framework."

**[3] NIST AI RMF 1.0 — the four functions (p. 3):**
> "Part 2 comprises the 'Core' of the Framework. It describes four specific functions to help organizations address the risks of AI systems in practice. These functions – GOVERN, MAP, MEASURE, and MANAGE – are broken down further into categories and subcategories. While GOVERN applies to all stages of organizations' AI risk management processes and procedures, the MAP, MEASURE, and MANAGE functions can be applied in AI system-specific contexts and at specific stages of the AI lifecycle."

**[3] NIST AI RMF 1.0 — not a checklist (§5, Core):**
> "Actions do not constitute a checklist, nor are they necessarily an ordered set of steps."

**[11] ISO/IEC 42001:2023 — overview, verbatim from iso.org:**
> "ISO/IEC 42001 is an international standard that specifies requirements for establishing, implementing, maintaining, and continually improving an Artificial Intelligence Management System (AIMS) within organizations. It is designed for entities providing or utilizing AI-based products or services, ensuring responsible development and use of AI systems."

**[11] ISO/IEC 42001:2023 — who it is for, verbatim from iso.org:**
> "Organizations of any size involved in developing, providing, or using AI-based products or services. It is applicable across all industries and relevant for public sector agencies as well as companies or non-profits."

**[A] Argyris 1991 — the only text visible without a subscription, verbatim from hbr.org:**
> "Any company that aspires to succeed in the tougher business environment of the 1990s must first resolve a basic dilemma: success in the marketplace increasingly depends on learning, yet most people don't know how to learn. What's more, those members of the organization that many assume to be the best at learning are, in fact, not very good at it. I am talking about the well-educated, high-powered, high-commitment professionals who occupy key leadership positions in the modern corporation."

**The book's own boundary sentence on the two frameworks (p8) — MUST accompany any use of [3] or [11]:**
> "These frameworks support the discipline of a loop; they do not promise a financial return."
> ไทย (p9): "แต่กรอบเหล่านี้ไม่ได้ให้ประกันผลตอบแทนทางธุรกิจในอัตราใด"

### The Argyris rule (binding)

The spec's addition is Argyris 1991 → "double-loop learning as the intellectual ancestor of 'change the right part of the system'". What is verified and what is not:

- **Verified on hbr.org:** the article exists at the URL, title "Teaching Smart People How to Learn", author Chris Argyris, "From the Magazine (May–June 1991)", and the opening-paragraph thesis quoted above.
- **Verified on hbr.org:** an earlier Argyris article titled **"Double Loop Learning in Organizations"**, HBR **September 1977** — this is the publisher-domain evidence that the term is Argyris's.
- **NOT verified on the publisher's domain:** any definition of single-loop vs double-loop learning, the thermostat analogy, "defensive reasoning", or any sentence beyond the opening paragraph.

Therefore the writer **may**: attribute double-loop learning to Chris Argyris, citing [A] (and [A2] for the term itself), and *describe in the writer's own words* the distinction between correcting an error inside the existing rules and questioning the rules that produced it. The writer **may not**: quote either article beyond the paragraph above, reproduce the thermostat analogy as Argyris's words, or cite a page number. Label both **Synthesis**, not Study — neither article declares a sample or method, and the site's `Study` label is reserved for that.

---

## Number cards

Every number the post may print. **No card, no number.** None of these is an empirical finding; all are the book's structural design or a fictional illustration, and each card says so.

### NC-1 · Five moves of the learning loop

- **Value / unit:** 5 (moves)
- **Denominator / population:** the book's own model of a working learning loop; not a count of anything observed
- **Comparison:** none — this is a definition, not a measurement
- **Task / setting:** Chapter 1, the operating definition of a learning loop
- **Source:** [B] book p8 / p9
- **Boundary line (book, D.1 "Author synthesis"):** "A framework built by connecting engineering, organization, workforce, and governance evidence. It is offered as a testable design, not as settled fact."
- **EN sentence as it will appear:** "A useful learning loop has five moves. Observe what happened. Preserve the context, route, action, and outcome. Compare the result with a declared expectation. Change the workflow, data, controls, model, or human role. Verify the change on representative, hidden, and severe cases before increasing exposure." *(verbatim, book p8)*
- **TH sentence as it will appear:** "วงจรการเรียนรู้ที่ใช้งานได้จริงมีห้าท่า ได้แก่ สังเกตสิ่งที่เกิดขึ้น เก็บบริบท เส้นทาง การกระทำ และผลลัพธ์ เปรียบเทียบผลจริงกับความคาดหมายที่ประกาศไว้ ปรับ Workflow ข้อมูล ตัวควบคุม โมเดล หรือบทบาทมนุษย์ แล้วตรวจสอบกับกรณีที่เป็นตัวแทน กรณีซ่อน และกรณีรุนแรงก่อนเพิ่มการเปิดรับ" *(verbatim, book p9)*

### NC-2 · Seven operating assets

- **Value / unit:** 7 (asset classes)
- **Denominator / population:** the classes the book names as operating assets rather than project debris
- **Comparison:** implicit — "operating assets, **not** project debris"
- **Task / setting:** Chapter 1, immediately after the five moves
- **Source:** [B] book p8 / p9
- **Boundary line:** author synthesis (as NC-1)
- **EN verbatim (book p8):** "Prompts, context templates, corpus snapshots, tool schemas, evaluation cases, thresholds, and release manifests are therefore operating assets, not project debris."
- **TH verbatim (book p9):** "Prompt แม่แบบบริบท รุ่นของคลังความรู้ Tool Schema ชุดทดสอบ Threshold และ Release Manifest จึงต้องถูกดูแลเสมือนสินทรัพย์ปฏิบัติการ"
- **Note for the table:** the spec's §2 table columns (owner / version / where it lives) are an **editorial addition** — the book names the seven assets but assigns them no owner, version or location. Present the table as the post's own worksheet, never as the book's.

### NC-3 · Five operating principles

- **Value / unit:** 5 (principles)
- **Denominator / population:** Chapter 1's principle set; **never renumber, never merge**
- **Comparison:** none
- **Task / setting:** book p8 ("Five operating principles") / p9 ("หลักปฏิบัติห้าประการ")
- **Source:** [B]
- **Boundary line:** author synthesis
- **EN verbatim (book p8) — quote exactly one in the 💡 blockquote, list the rest in prose:**
  1. **Learn from released behavior** — "A polished demonstration says little about live case variation."
  2. **Bind change to evidence** — "State the intended improvement, affected slice, threshold, and rollback condition."
  3. **Treat traces as capability** — "If a decision cannot be reconstructed, the organization cannot learn reliably from it."
  4. **Keep value quality risk cost and human load separate** — "One aggregate score conceals tradeoffs."
  5. **Assign an owner to the loop** — "Someone must own the time from signal to verified improvement."
- **TH verbatim (book p9):**
  1. **เรียนรู้จากพฤติกรรมที่ปล่อยจริง** ไม่ใช่เดโมที่คัดกรณีมาแล้ว
  2. **ผูกการเปลี่ยนแปลงกับหลักฐาน** ระบุกลุ่มกรณี เกณฑ์ผ่าน และเงื่อนไขย้อนกลับ
  3. **มอง Trace เป็นความสามารถของผลิตภัณฑ์** หากย้อนสร้างเหตุการณ์ไม่ได้ องค์กรเรียนรู้อย่างน่าเชื่อถือไม่ได้
  4. **แยกคุณค่า คุณภาพ ความเสี่ยง ต้นทุน และภาระมนุษย์** คะแนนเดียวซ่อนการแลกเปลี่ยน
  5. **ตั้งเจ้าของวงจร** ต้องมีผู้รับผิดชอบตั้งแต่พบสัญญาณจนยืนยันว่าแก้ได้ผล
- **Recommended 💡 pick:** principle **5**, which is the one the key-takeaways line "Loop owner" restates.

### NC-4 · 75 minutes (the canvas)

- **Value / unit:** 75 minutes
- **Denominator / population:** one working session, one workflow — a prescribed agenda length, **not** an observed or benchmarked duration
- **Comparison:** none
- **Task / setting:** book p8 "Working session The learning loop canvas" / p10 "เวิร์กช็อป Learning loop canvas"
- **Source:** [B]
- **Boundary line:** author synthesis — the book prescribes the session; it reports no trial of it and no outcome from running it
- **EN verbatim (book p8):** "Run a 75-minute session with the process owner, frontline practitioner, product lead, data or engineering lead, risk representative, and one person affected by the workflow."
- **TH verbatim (book p10):** "จัดเวลา 75 นาทีร่วมกับเจ้าของกระบวนการ ผู้ปฏิบัติงาน ผู้นำผลิตภัณฑ์ ทีมข้อมูลหรือวิศวกรรม ตัวแทนความเสี่ยง และผู้ได้รับผลกระทบหนึ่งคน"
- **⚠ Two editorial additions the writer must own, not attribute to the book:**
  1. **The book names SIX participants, not seven.** Process owner · frontline practitioner · product lead · data or engineering lead · risk representative · one person affected by the workflow = **6**. The spec's seventh role, **facilitator**, is **not in the book**. Either drop it, or introduce it explicitly as the post's addition ("plus someone to facilitate"). Do not write "the book's seven roles".
  2. **The book allocates no minutes per step.** It gives 75 minutes total and six agenda steps with no split. Any Minute column in the canvas table is the post's own allocation and must read as guidance, not as the book's schedule.

### NC-5 · Six canvas steps

- **Value / unit:** 6 (agenda steps)
- **Denominator / population:** the bullets under "Working session The learning loop canvas"
- **Comparison:** none
- **Task / setting:** book p8–9 / p10
- **Source:** [B]
- **Boundary line:** author synthesis
- **EN verbatim (book p8–9), in order:**
  1. "Name one business outcome and one harm that must not increase."
  2. "Draw the current decision from trigger to consequence and mark every handoff."
  3. "Inventory outcomes, corrections, complaints, incidents, traces, and missing signals."
  4. "Define the review cadence, decision owner, and escalation path."
  5. "Select one case slice, baseline, target, and rollback condition."
  6. "Assign the first evidence review date."
  → "The output is a one-page loop charter, not a technology roadmap."
- **TH verbatim (book p10), in order:**
  1. "ระบุผลลัพธ์ธุรกิจหนึ่งข้อและความเสียหายหนึ่งข้อที่ห้ามเพิ่ม"
  2. "วาดเส้นทางการตัดสินใจตั้งแต่จุดเริ่มจนถึงผลลัพธ์และทำเครื่องหมายทุกจุดส่งต่อ"
  3. "รวบรวมผลลัพธ์ การแก้ไข ข้อร้องเรียน Incident, Trace และสัญญาณที่ยังขาด"
  4. "กำหนดรอบทบทวน เจ้าของการตัดสินใจ และเส้นทาง Escalation"
  5. "เลือกกลุ่มกรณี ค่าเริ่มต้น เป้าหมาย และเงื่อนไข Rollback"
  6. "นัดวันทบทวนหลักฐานครั้งแรก"
  → "ผลลัพธ์คือกฎบัตรวงจรการเรียนรู้หนึ่งหน้า ไม่ใช่แผนจัดซื้อเทคโนโลยี"
- **Note on the spec's loop-charter template:** the spec lists nine charter fields (outcome, harm that must not increase, decision path & handoffs, review cadence, decision owner, escalation, case slice / baseline / target / rollback, first evidence review date). All nine are recoverable from the six steps above — the template is a **re-arrangement of the book's own bullets**, which is legitimate. Do not add a tenth field.

### NC-6 · Ten metrics that matter

- **Value / unit:** 10 (metrics)
- **Denominator / population:** Chapter 1's metric list; the count is exactly ten as enumerated below
- **Comparison:** the list carries its own comparison rule — "Read them together. Faster throughput with more severe escapes is not progress."
- **Task / setting:** book p9 "Metrics that matter" / p10 "ตัวชี้วัดสำคัญ"
- **Source:** [B]
- **Boundary line:** author synthesis; **these are metric definitions, not targets.** No threshold value appears in Chapter 1 and none may be invented.
- **EN verbatim (book p9):** "Track outcome by case slice, first-pass acceptance, median time from detected failure to regression test, releases with a predeclared hypothesis and threshold, trace completeness, severe-case pass rate, post-release escape, reviewer minutes, override reasons, and the share of corrected cases reused in data, retrieval, policy, or evaluation. Read them together. Faster throughput with more severe escapes is not progress."
- **TH verbatim (book p10):** "ติดตามผลธุรกิจแยกตามกลุ่มกรณี อัตราผ่านครั้งแรก เวลาจากพบปัญหาถึงเพิ่ม Regression Test สัดส่วน Release ที่มีสมมติฐานและเกณฑ์ล่วงหน้า ความครบถ้วนของ Trace อัตราผ่านกรณีรุนแรง อัตราความผิดพลาดที่หลุดจริง เวลาตรวจต่อกรณี เหตุผลการ Override และสัดส่วนกรณีแก้ไขที่นำกลับไปปรับข้อมูล Retrieval นโยบาย หรือการประเมิน ต้องอ่านตัวเลขร่วมกัน งานเร็วขึ้นแต่ความผิดพลาดรุนแรงเพิ่มขึ้นไม่ใช่ความก้าวหน้า"
- **The ten, split for the table (order is the book's — keep it):** 1 outcome by case slice · 2 first-pass acceptance · 3 median time from detected failure to regression test · 4 releases with a predeclared hypothesis and threshold · 5 trace completeness · 6 severe-case pass rate · 7 post-release escape · 8 reviewer minutes · 9 override reasons · 10 share of corrected cases reused in data, retrieval, policy, or evaluation.
- **Scorecard column** (required by the series convention; mapped from the book's board scorecard, p4): 1 Value · 2 Quality · 3 Learning · 4 Learning · 5 Risk · 6 Risk · 7 Risk · 8 People · 9 People · 10 Learning. This mapping is the post's own; the book does not print it. Present the column as the post's mapping, not the book's.

### NC-7 · Six failure patterns

- **Value / unit:** 6 (patterns)
- **Denominator / population:** Chapter 1's failure list
- **Comparison:** none
- **Task / setting:** book p9 "Failure patterns" / p10 "รูปแบบความล้มเหลว"
- **Source:** [B]
- **Boundary line:** author synthesis
- **EN verbatim (book p9):** "Pilot theatre, dashboards without a decision owner, averages that erase weak groups, repeated prompt patching without workflow diagnosis, learning only after incidents, and explanations that dismiss frontline feedback as user error."
- **TH verbatim (book p10):** "Pilot เพื่อการแสดงผล Dashboard ที่ไม่มีผู้มีอำนาจตัดสินใจ ค่าเฉลี่ยที่กลบจุดอ่อนของบางกลุ่ม การแก้ Prompt ซ้ำโดยไม่วิเคราะห์ Workflow การเรียนรู้เฉพาะหลังเกิดเหตุ และการทิ้งข้อเสนอแนะหน้างานด้วยคำว่า User Error"

### NC-8 · Figure 1 — seven nodes, three measures

- **Value / unit:** 7 (cycle nodes) and 3 (measures)
- **Denominator / population:** the figure's own composition, fixed by the manifest
- **Comparison:** none
- **Task / setting:** Figure 1 alt/caption (manifest strings — reproduce verbatim, do not re-translate)
- **Source:** manifest `scripts/series/ai-transformation.json`, post 3, figure `learning-engine`; the seven-node chain itself is the book's "one sentence strategy" (p3 EN / p5 TH)
- **Boundary line:** author synthesis
- **The seven nodes, verbatim — the safest prose anchor for the figure (book p3, "The one sentence strategy"):**
  > EN: "Build the organizational capability to convert data into context, context into intelligence, intelligence into judgment, judgment into authorized action, action into observable outcomes, and outcomes into verified learning faster than the environment changes."
  > TH (p5): "สร้างความสามารถขององค์กรในการเปลี่ยนข้อมูลเป็นบริบท บริบทเป็นปัญญา ปัญญาเป็นดุลยพินิจ ดุลยพินิจเป็นการกระทำที่ได้รับอนุญาต การกระทำเป็นผลลัพธ์ที่สังเกตได้ และผลลัพธ์เป็นการเรียนรู้ที่ตรวจสอบได้ เร็วกว่าสภาพแวดล้อมที่เปลี่ยนไป"
- **⚠ Wording collision the writer must not blur:** the figure's three measures are **feedback latency · decision adaptation time · time to scaled improvement**. The book's board scorecard **Learning** column (p4) names a *different* triple: **"Feedback latency, time to verified improvement, recurrence"** (ไทย p5: "Learning จาก Feedback Latency และเวลาถึงการปรับปรุงที่พิสูจน์"). Use the figure's wording **only** inside the figure's alt and caption. In prose, if the post cites the board scorecard, use the book's wording. Never write "the book's three measures of learning velocity are feedback latency, decision adaptation time and time to scaled improvement" — the book does not say that.
- **Learning velocity, the book's definition (Appendix C, entry 3) — this is the safe prose anchor:**
  - EN: "How quickly an organization converts reliable outcome evidence into better decisions, workflows, controls, and reusable knowledge."
  - TH: "ความเร็วที่องค์กรเปลี่ยนหลักฐานจากผลลัพธ์จริงให้เป็นการตัดสินใจ กระบวนงาน มาตรการควบคุม และความรู้ที่ดีขึ้นและนำกลับมาใช้ได้"

### NC-9 · r8's 517-run specimen — **NOT USED IN THIS POST**

Carded here only so that no writer reaches for it. The spec's §3 asks for "r8's **boundary claim**" — the authority/indispensability→boundaries argument on p8 — **not** the specimen numbers, which belong to the assurance posts later in the series.

- **Value / unit:** 517 deterministic executions (30/30 benign; 0/40 policy escapes; 0/6 prohibited refund effects; 70/70 route traces; 8/12 violating candidates released under adaptive tests; 4/4 prohibited effects blocked by hard execution mediation)
- **Denominator / population:** one author-constructed fixed test suite; author-constructed fixtures
- **Comparison:** full envelope vs. soft controls alone
- **Task / setting:** a bounded authored specimen in the r8 paper, `CX-REFUND-01`-style refund workflow
- **Source:** [1] — **never linked**
- **Boundary line (book p35, MUST be printed with any of these numbers):** "This illustrates wiring and failure localization in author-constructed fixtures. It does not establish production quality, independent red-team robustness, legal compliance, or a population safety rate." · ไทย: "ผลนี้แสดงการเชื่อม Control และตำแหน่ง Failure ใน Fixture ที่ผู้เขียนสร้าง ไม่ได้พิสูจน์ Production Quality, Independent Red Team, Legal Compliance หรือ Population Safety Rate"
- **Ruling for post #3: do not print any of these numbers.** Use only the r8 boundary claim in NC-10.

### NC-10 · The r8 boundary claim (this is what §3 needs)

- **Value / unit:** none — a qualitative claim
- **Source:** [1], as reported by the book p8 / p9
- **Boundary line:** author-supplied, unpublished paper; the claim is a design argument, not an empirical result. Cite as "Mingkhwan's 2026 r8 paper (author-supplied, unpublished)". **Never link it.**
- **EN verbatim (book p8):** "Mingkhwan's 2026 r8 paper argues that when model output becomes both authoritative and indispensable for a declared task, assurance must move to the boundaries around the model. In organizational terms, learning cannot stop at model tuning. The entire decision system must improve. This is consistent with the lifecycle disciplines in NIST AI RMF and the continual-improvement logic of ISO IEC 42001. These frameworks support the discipline of a loop; they do not promise a financial return."
- **TH verbatim (book p9):** "งาน r8 ของ Mingkhwan เสนอว่า เมื่อผลจากโมเดลมีทั้งอำนาจสูงและเป็นองค์ประกอบที่ขาดไม่ได้สำหรับงานที่ประกาศไว้ ภาระการรับรองความถูกต้องต้องกระจายไปยัง Boundary รอบโมเดล ในระดับองค์กร การเรียนรู้จึงต้องครอบคลุมระบบการตัดสินใจทั้งหมด ไม่ใช่เพียงการปรับโมเดล แนวคิดนี้สอดคล้องกับวงจรชีวิตของ NIST AI RMF และการปรับปรุงต่อเนื่องของ ISO IEC 42001 แต่กรอบเหล่านี้ไม่ได้ให้ประกันผลตอบแทนทางธุรกิจในอัตราใด"

---

## Dated statuses

Each is one dated sentence. Reproduce the date; do not write "currently" or "as of today".

**DS-1 · NIST AI RMF — status at 2026-09-05.**
> EN: "NIST released the AI Risk Management Framework (AI RMF 1.0) on 26 January 2023; as of 5 September 2026 it remains at version 1.0, it is explicitly voluntary, and it confers no certification."
> TH: "NIST เผยแพร่ AI Risk Management Framework (AI RMF 1.0) เมื่อ 26 มกราคม 2023 และ ณ วันที่ 5 กันยายน 2569 ยังคงเป็นรุ่น 1.0 เป็นกรอบโดยสมัครใจ และไม่ใช่การรับรอง"
> Checked: nist.gov landing page (200) + NIST AI 100-1 PDF (200) on 2026-09-05. NIST's own versioning plan schedules a community review "no later than 2028"; a Critical Infrastructure Profile **concept note** was published 7 April 2026 and a GenAI Profile (NIST AI 600-1) exists since 26 July 2024 — **neither supersedes AI RMF 1.0, and neither may be described as a new version.**

**DS-2 · ISO/IEC 42001 — status at 2026-09-05.**
> EN: "ISO/IEC 42001:2023, *Information technology — Artificial intelligence — Management system*, has a publication date of December 2023 and, checked on 5 September 2026, is Edition 1 with status Published at stage 60.60."
> TH: "ISO/IEC 42001:2023 (Information technology — Artificial intelligence — Management system) มีวันเผยแพร่ธันวาคม 2023 และเมื่อตรวจสอบวันที่ 5 กันยายน 2569 ยังเป็น Edition 1 สถานะ Published ที่ระยะ 60.60"
> Checked in a real browser on 2026-09-05 (iso.org 403s automated fetchers). The book relies only on ISO's public description; **do not reproduce clause text or requirements, and do not describe the standard as law or as a guarantee of AI system quality.**

**DS-3 · NIST June 2026 monitor-and-update item — verified, but OPTIONAL for this post.**
> EN: "NIST published a research summary on 9 June 2026 reporting a mathematical result that 'there is no finite set of guardrails that is universally robust against adversarial prompts,' which supports a continuous monitor-and-update posture after release rather than a fixed set of defenses."
> TH: "NIST เผยแพร่บทสรุปงานวิจัยเมื่อ 9 มิถุนายน 2026 ระบุผลทางคณิตศาสตร์ว่า ไม่มีชุดการ์ดเรลจำกัดชุดใดที่ทนทานต่อ Adversarial Prompt ได้ทุกกรณี ซึ่งสนับสนุนแนวทางเฝ้าระวังและปรับปรุงต่อเนื่องหลังปล่อยใช้ แทนการวางการป้องกันชุดตายตัว"
> Source: `https://www.nist.gov/news-events/news/2026/06/nist-mathematical-proof-supports-transition-continuous-monitor-and-update` (HTTP 200, 2026-09-05), headline "NIST Mathematical Proof Supports Transition to a Continuous-Monitor-and-Update Security Model for AI Systems", 9 June 2026. **Book boundary [7]:** "a mathematical result does not specify the correct cadence or controls for every operational context."
> **Ruling:** this is a dated-status re-check required by the protocol, not one of the spec's Research targets. It is available to the writer if the Verify move needs external support; if used it becomes reference [7] with the Standard label and the boundary above. If unused, it stays here.

**Dated statuses that do NOT apply to this post** (checked against the spec's sections and deliberately not researched further, so the writer knows they are unavailable): Thailand's dedicated AI law / ETDA `law_ai` / ร่างพระราชบัญญัติ ปัญญาประดิษฐ์ (no legal claim in this post); EU AI Act application dates and 2026 amendments (no legal claim); Stanford AI Index 2026 figures (no adoption or survey number in this post — the 88%/70% pair belongs to post #1); IEA 2026 energy figures; ISO/IEC 42005:2025 impact-assessment status; ETDA guideline versions; PDPA/PDPC sub-regulations. **None of these may appear in post #3.**

---

## Fictional values

All flagged on first mention: `(กรณีสมมติจากหนังสือ)` / `(a fictional case from the playbook)`. **None may enter a metrics table as a target, a benchmark or a threshold.**

| Value | Where | Ruling |
|---|---|---|
| **Aurora Assurance** (company) | §4 `aurora` | Fictional. Book p8: "Consider the **fictional** Aurora Assurance." Keep the name exactly. |
| **80,000 AI-assisted claim letters** ("eighty thousand") | §4 | Illustrative-fictional. It is the *activity target Aurora abandoned* — the whole point is that it measured nothing. Never present it as an outcome, a benchmark, or a scale claim. |
| **The three replacement outcomes** — correct explanation on first contact · fewer avoidable callbacks · no unsupported coverage statement | §4 | Illustrative-fictional but reusable as a *shape* of outcome definition. No numeric target attaches to any of them; the book gives none. |
| **The two-policy slice** (weak performance when two policies interacted) | §4 | Illustrative-fictional. No rate, no percentage, no case count is given in the book — **do not invent one.** |
| **Weekly review cadence** | §4 | Illustrative-fictional; Aurora's cadence, not a recommended cadence. |
| Kiri Foods · HarborLight Retail · LannaBuild Engineering · Luma Commerce Thailand · `CX-REFUND-01` | — | Fictional, and **not in this post.** Do not import them. |
| THB 2,000 / 2,400 / 2,500 / 1,850 · 94.6% / 41.3% · 240 cases · 18 min / 46 h | — | Fictional, and **not in this post.** Do not import them. |

**Book text quality note for §4:** the English on p8 reads "Weekly review found acceptable performance for single-policy claims, **or** weak performance when two policies interacted." The Thai on p9 reads "…ทำงานได้ดีในกรณีกรมธรรม์เดียว **แต่** พลาดเมื่อสองกรมธรรม์เชื่อมกัน" — i.e. *but*, which is the sense. The "or" is a defect in the book's English. **Render the sense with "but" in the EN track and do not present that sentence as a verbatim quotation.** Every other Aurora sentence quoted above is safe verbatim.

---

## Glossary check

Coinages this post uses, matched to the plan's canonical Appendix C Thai rendering. Verbatim on first mention, English inline afterwards.

| Coinage | Canonical Thai (plan / Appendix C) | Verified in book? | Note |
|---|---|---|---|
| AI transformation | **การเปลี่ยนผ่านองค์กรด้วย AI** | ✅ Appendix C entry 1, verbatim | Chapter 1's own Thai prose uses the shorter "การเปลี่ยนผ่านด้วย AI". **Use the Appendix C form on first mention**, then English inline. |
| Learning loop | **วงจรการเรียนรู้** | ✅ Appendix C entry 2 | Book EN definition: "A closed cycle that turns data into decisions, actions, observed outcomes, evidence, and improvements to the next cycle." TH: "วงจรปิดที่เปลี่ยนข้อมูลเป็นการตัดสินใจ การลงมือทำ ผลลัพธ์ที่สังเกตได้ หลักฐาน และการปรับปรุงรอบถัดไป" |
| Learning velocity | **ความเร็วในการเรียนรู้** | ✅ Appendix C entry 3 | Definition quoted in NC-8. |
| Operating model | **รูปแบบการดำเนินงาน** | ✅ Appendix C | Only if the post mentions the six layers. |
| Operating assets | **สินทรัพย์ปฏิบัติการ** | ✅ book p9 (not a numbered Appendix C entry) | Use the book's own Thai; it is not in the plan's canonical list, so the book text is the authority. |
| Loop charter | **กฎบัตรวงจรการเรียนรู้** | ✅ book p10 verbatim | Not in Appendix C; the book's Chapter 1 Thai is the authority. |
| Kept English inline (as the book does) | Workflow · Trace · Threshold · Manifest · Prompt · Release · Rollback · Escalation · Dashboard · Pilot · Override · Retrieval · Baseline · Incident · Regression Test · Tool Schema | ✅ all appear untranslated in the book's Thai on pp9–10 | Do not translate these. |
| Section labels | หลักปฏิบัติห้าประการ · เวิร์กช็อป · ตัวชี้วัดสำคัญ · รูปแบบความล้มเหลว | ✅ book pp9–10 verbatim | Exactly the plan's labels — no deviation. |

**No glossary deviations.** One near-miss recorded above: "AI transformation" — Chapter 1's body Thai differs from Appendix C; the Appendix C form wins on first mention.

**Ladder rule:** this post touches **no** five-level ladder. Do not import the maturity levels (สำรวจ / ช่วยงาน / บริหารอย่างเป็นระบบ / บูรณาการ / ปฏิบัติการแบบ AI-core) — they are post #4's, and the next-post hook must point to them without naming the levels.

---

## Do not assert

Searched for and could not verify, or verified as out of bounds. A writer who needs any of these must drop the sentence.

1. **Any quotation from Argyris beyond the opening paragraph.** hbr.org's free preview stops there; "single-loop", "double-loop", the thermostat analogy and "defensive reasoning" were **not** found on the publisher's domain. Attribute the concept; never quote it, never give a page number.
2. **That the book's Chapter 1 cites Argyris.** It does not. Argyris appears nowhere in the playbook (grep: zero hits for "Argyris", "double-loop", "double loop"). Introduce him as the post's own historical framing, not as the book's citation.
3. **A seventh canvas participant.** The book names six. The facilitator is the spec's addition — see NC-4.
4. **Any minute-by-minute split of the 75 minutes as the book's.** The book gives 75 minutes and six steps, no allocation.
5. **Any threshold, target or benchmark value for the ten metrics.** Chapter 1 prints none.
6. **Any number attached to Aurora's two-policy slice** — no rate, no volume, no improvement percentage exists in the source.
7. **"Feedback latency, decision adaptation time and time to scaled improvement" as the book's learning measures.** That triple is the figure's; the book's board scorecard says "feedback latency, time to verified improvement, recurrence". See NC-8.
8. **The r8 517-run numbers in this post** — out of scope (NC-9), and unusable anywhere without their boundary sentence.
9. **A URL for the r8 paper.** It has none; it is author-supplied and unpublished. Never link, never DOI, never "available on request".
10. **Any claim that NIST AI RMF or ISO/IEC 42001 improves a financial or productivity outcome.** The book's own sentence forecloses it: "These frameworks support the discipline of a loop; they do not promise a financial return." Neither may be described as law, as certification, or as evidence that a given system is trustworthy.
11. **That AI RMF has a version newer than 1.0**, or that the April 2026 Critical Infrastructure Profile concept note or the 2024 GenAI Profile supersede it. They do not.
12. **Any ISO/IEC 42001 clause text, requirement, Annex A control, or the phrase "certified to ISO 42001"** — the book relies on ISO's public overview only, and reproducing protected text is out of bounds.
13. **Any adoption statistic** (88% / 70% / agent use in single digits). Verified in the book at p4/p5 and sourced to Stanford AI Index 2026, but it is **post #1's** number and is not in this post's Research targets. It also carries a survey-not-census caveat that this post has no room to state.
14. **Anything from the masterclass video.** Verified live (id `n_IwUYevRZo`, The Foundation (th), 2026-08-28, 52 min) per the protocol, but not a Research target for this post. Never quote it; never attribute the playbook's synthesis to the presenter.
15. **Any legal or regulatory status** — Thailand's AI bill, the EU AI Act, PDPA sub-regulations. Not researched for this post because no section needs them; asserting one from memory would be unsourced.
16. **Any ISO or NIST "conformance" of the canvas, the charter or the ten metrics.** The canvas is the book's design; no standard endorses it.

---

*Ledger compiled 2026-09-05 (Asia/Bangkok). Book pages read: PDF 9–11 (printed 8–10) in full, plus p2 (eight questions), p3 (the one-sentence strategy), p4–5 (board scorecard, executive summary), p35 (r8 specimen boundary), p91–92 (D.1 evidence policy, D.2 status date, D.3 sources 1–12), Appendix C entries 1–5.*

*Sources verified: 5 of 5 fetchable targets at HTTP 200 ([3] NIST landing page, [3] NIST AI 100-1 PDF, [11] ISO/IEC 42001 — browser only, [A] HBR 1991, [A2] HBR 1977), plus [7] NIST June 2026 (optional) and the masterclass video id. 0 UNVERIFIED. [1] r8 and [B] the book are unlinkable by design, not unverified.*
