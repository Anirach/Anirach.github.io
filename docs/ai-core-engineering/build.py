"""Rebuild this course's sheets, figures and companion learning materials.

Run with absolute paths independent of cwd. No network calls. The companion
source must exist; COMPANION_REV pins the links to its tested published commit.
"""
import html
import inspect
import json
import os
from pathlib import Path
import runpy
import re
import subprocess
import sys
import textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
COMPANION = Path('/Users/anirach/Projects/ai-core-engineering-workbench')
PARTS = runpy.run_path(str(HERE/'course.py'))['PARTS']
REV = os.environ.get('COMPANION_REV','18cdfcd4156d3d02acb8badf3b3a0a823113e0ed')
URL = 'https://github.com/Anirach/ai-core-engineering-workbench'
sys.path.insert(0,str(COMPANION))
from workbench import core, runtime
from workbench.labs import lab

INK='#11304b'; BLUE='#226299'; CREAM='#faf7f0'; CLOUD='#dee7e6'; GOLD='#7a5f22'; MUTE='#526174'; WHITE='#ffffff'

def font(size, bold=False):
    f=ImageFont.truetype(str(ROOT/'scripts/fonts/Inter-var.ttf'),size)
    if bold:
        try:f.set_variation_by_name('Bold')
        except OSError:pass
    return f

def lines(d,text,width,size=28,bold=False):
    out=[]; line=''; f=font(size,bold)
    for word in text.split():
        trial=(line+' '+word).strip()
        if d.textlength(trial,font=f)>width and line:out.append(line);line=word
        else:line=trial
    return out+[line]

def label(d,text,x,y,width,size=28,color=INK,bold=False):
    for line in lines(d,text,width,size,bold):
        d.text((x,y),line,font=font(size,bold),fill=color);y+=size*1.4
    return y

def arrow(d,a,b,color=BLUE,width=4):
    import math
    d.line((a,b),fill=color,width=width)
    angle=math.atan2(b[1]-a[1],b[0]-a[0]); r=13
    d.polygon([b,(b[0]-r*math.cos(angle-.5),b[1]-r*math.sin(angle-.5)),
                  (b[0]-r*math.cos(angle+.5),b[1]-r*math.sin(angle+.5))],fill=color)

def diagram(p):
    im=Image.new('RGB',(1600,1000),CREAM);d=ImageDraw.Draw(im)
    d.text((70,45),f'ENGINEERING AI-CORE  /  {p["n"]:02d} OF 15',font=font(24,True),fill=BLUE)
    label(d,p['title'],70,94,1450,47,bold=True)
    d.line((70,235,1530,235),fill=CLOUD,width=3)
    d.text((70,264),'BEFORE  /  FAILURE WE CAN OBSERVE',font=font(23,True),fill=MUTE)
    label(d,p['before'],70,309,1410,31)
    d.text((70,405),'AFTER  /  RESPONSIBILITIES MADE EXPLICIT',font=font(23,True),fill=BLUE)
    for i,node in enumerate(p['nodes']):
        x=70+i*380
        d.rounded_rectangle((x,465,x+320,595),radius=14,fill=INK if i==2 else WHITE,outline=BLUE,width=3)
        label(d,node,x+22,492,275,29,WHITE if i==2 else INK,True)
        if i<3:arrow(d,(x+326,530),(x+367,530))
    arrow(d,(990,604),(990,664),GOLD)
    d.rounded_rectangle((680,672,1510,776),radius=12,fill='#e9e1c4')
    label(d,'Stop / review path: '+p['failure'],704,689,780,25,color=GOLD)
    label(d,'EVIDENCE TO KEEP',70,683,560,22,color=BLUE,bold=True)
    label(d,p['artifact'],70,724,555,27)
    d.line((70,824,1530,824),fill=CLOUD,width=3)
    label(d,'OUTCOME  /  '+p['after'],70,854,1425,30,bold=True)
    d.text((70,952),'Author-designed architecture. Arrows show responsibilities; the companion defines exact execution order.',font=font(20),fill=MUTE)
    path=ROOT/'images'/f'{p["slug"]}-flow.png';im.save(path,optimize=True)

def overview():
    im=Image.new('RGB',(1600,1150),CREAM);d=ImageDraw.Draw(im)
    label(d,'Patch Workbench: the complete architecture',65,45,1470,46,bold=True)
    label(d,'Ordinary code owns policy and effects. Models supply proposals and fallible judgments.',65,117,1460,27,color=MUTE)
    names=['Input schema','Auth policy','Jev decisions','Semantic input','Context snapshot','Candidate source',
           'Output language','Behavior oracle','Quality gate','Human review']
    for i,name in enumerate(names):
        row,col=divmod(i,5);x=65+col*303;y=240+row*320
        lit=i in (2,5,8)
        d.rounded_rectangle((x,y,x+260,y+145),radius=14,fill=INK if lit else WHITE,outline=BLUE,width=3)
        label(d,f'{i+1:02d}  '+name,x+18,y+24,225,27,WHITE if lit else INK,True)
        label(d,'Model boundary' if lit else 'Deterministic host',x+18,y+104,225,18,WHITE if lit else MUTE)
        if col<4:arrow(d,(x+266,y+73),(x+296,y+73))
    d.line((1530,313,1560,313,1560,455,35,455,35,633),fill=BLUE,width=4)
    arrow(d,(35,633),(58,633))
    label(d,'ALL NON-PASS PATHS STOP, REVIEW, OR USE A BOUNDED REVISION',65,805,1470,28,color=GOLD,bold=True)
    label(d,'Across the workflow: versioned manifest  /  stage trace  /  call and revision budgets',65,865,1470,28)
    label(d,'Separate release decision: held-out evidence + authenticated approval + rollback readiness',65,927,1470,28)
    label(d,'Teaching boundary: in-memory draft only. No repository writes, PR creation, merge or deployment.',65,1020,1470,26,color=MUTE)
    im.save(ROOT/'images/ai-engineering-architecture.png',optimize=True)

def excerpt(p):
    if p['n']==1:
        return 'from workbench.runtime import candidate\nfrom workbench.core import output_check, behavior_check\n\n# Familiar deterministic implementation\ndef discount_cents(price, percent):\n    return price * (100 - percent) // 100\n\nassert discount_cents(1999, 25) == 1499\n\n# A plausible generated proposal still needs independent checks\nproposal = candidate("def discount_cents(price, percent):\\n    return price - percent\\n")\nprint(output_check(proposal).state)    # pass: permitted shape\nprint(behavior_check(proposal).state)  # revise: wrong behavior'
    if p['n']==3:
        return 'from workbench.runtime import run, request, FixtureProvider\n\nresult = run(request(), FixtureProvider())\nprint(result["state"])\nprint([event["stage"] for event in result["trace"]])'
    if p['n']==13:
        return 'from workbench.runtime import run, request, candidate, FixtureProvider\n\nwrong = candidate("def discount_cents(price, percent):\\n    return price - percent\\n")\nresult = run(request(), FixtureProvider(candidates=[wrong, candidate()]),\n             max_calls=5, max_revisions=1, seconds=2)\nprint(result["state"], result["attempts"], result["calls"])'
    if p['n']==14:
        return 'from workbench.evaluation import evaluate\n\nreport = evaluate()\nprint(report["agreements"], report["cases"])\nprint(report["model_accuracy"])  # None: fixtures are not live evidence'
    return '\n\n'.join(inspect.getsource(getattr(core,n)).strip() for n in p['functions'])

HEADINGS={
'en':[('problem','1. The engineering problem'),('architecture','2. The boundary to design'),('code','3. Read the implementation'),('outcome','4. Compare the outcomes'),('practice','5. Run, break, and explain'),('references','6. Sources and limits')],
'th':[('problem','1. ปัญหาทางวิศวกรรม'),('architecture','2. ขอบเขตที่ต้องออกแบบ'),('code','3. อ่าน implementation'),('outcome','4. เปรียบเทียบผลที่ได้'),('practice','5. รัน ทำให้พัง และอธิบาย'),('references','6. แหล่งอ้างอิงและขอบเขต')]}

def sheets(p):
    for lang in ('th','en'):
        h=dict(HEADINGS[lang]); prose=p['thai' if lang=='th' else 'en']; E=html.escape
        def prose_html(text):
            text=E(text)
            for term in ['accepted_draft','input_check','authorize','output_check','behavior_check','quality_gate','release_gate','assemble_context','candidate_hash','evidence_id','permission_denied','action_denied','possible_injection','source_language','input_type','model_accuracy','live_latency_ms','live_cost','FixtureProvider','JevProvider']:
                text=re.sub(r'(?<![A-Za-z0-9_])'+re.escape(term)+r'(?![A-Za-z0-9_])', '<code>'+term+'</code>',text)
            return re.sub(r'\[(\d+)\]',lambda m:'<a href="#ref-'+m[1]+'">['+m[1]+']</a>',text)
        out=[f'<!--{lang.upper()}-TOC:{key}-->{title}' for key,title in HEADINGS[lang]]
        def section(key,body):
            out.append(f'<!--{lang.upper()}-SECTION:{key}-->\n<h2 id="{key}">{h[key]}</h2>\n'+body)
        label0='เป้าหมายบทนี้' if lang=='th' else 'Learning outcome'
        prerequisites=''
        if p['n']==1:
            prerequisites=('<p><strong>พื้นฐานที่ใช้:</strong> อ่าน function, dictionary และ test ง่าย ๆ ได้ ใช้ Python 3.11+ และ Git ไม่ต้องมีบัญชีโมเดลสำหรับแล็บออฟไลน์ อ่านบทก่อน แล้วรันแล็บและจดผลตามหัวข้อ 5</p>' if lang=='th' else '<p><strong>Prerequisites:</strong> basic functions, dictionaries and tests; Python 3.11+ and Git. Offline labs need no model account. Read the chapter, run its lab, and record the outcome in section 5.</p>')
        section('problem',f'<div class="callout"><h3>{label0}</h3><p>{E(p["subth" if lang=="th" else "sub"])}</p></div>\n'+prerequisites+f'<p>{prose_html(prose[0])}</p>\n<p>{prose_html(prose[1])}</p>')
        sec=f'<!--FIGURE:flow-->\n<p>{prose_html(prose[2])}</p>'
        if p['n'] in (1,15): sec+='\n<!--FIGURE:overview-->'
        section('architecture',sec)
        note=('ส่วนโค้ดจาก companion เพื่ออ่านประกอบ ใช้คำสั่งในหัวข้อ 5 เพื่อรันตัวอย่างที่ครบ dependency' if lang=='th' else 'Implementation excerpt from the companion. Run the complete lesson below with its imports and fixtures.')
        extra=''
        if p['n']==5:
            payload={'model':core.MODEL,'state':{'issue':'Fix integer-cent discount rounding'},'questions':core.QUESTION}
            extra=('<h3>สัญญา HTTP จริงที่ adapter ใช้</h3><p>ส่ง JSON นี้ด้วย POST ไปยัง endpoint ทางการ เก็บ API key ฝั่ง server เท่านั้น ตัวอย่างที่รันปกติยังใช้ fixture; ดู workbench/jev.py สำหรับ adapter และ README สำหรับคำสั่งเลือกเรียกจริง</p>' if lang=='th' else '<h3>The real HTTP adapter contract</h3><p>The adapter sends this JSON by POST to the official endpoint. Keep the API key server-side. Normal lessons use fixtures; see workbench/jev.py and the README for the explicit live command.</p>')
            extra+='<pre><code>POST https://api.typesafe.ai/v1/systemone\nContent-Type: application/json\nAuthorization: Bearer &lt;server-side key&gt;\n\n'+E(json.dumps(payload,indent=2))+'</code></pre>'
        if p['n']==6:
            extra='<h3>SKILL.md</h3><pre><code>'+E((COMPANION/'skills/pricing-patch/SKILL.md').read_text())+'</code></pre>'
        if p['n']==12:
            extra='<h3>'+('คำถาม rubric ที่ใช้จริง' if lang=='th' else 'The actual rubric questions')+'</h3><pre><code>'+E(json.dumps(core.QUALITY_QUESTIONS,indent=2))+'</code></pre>'
        if p['n']==15:
            extra='<h3>'+('ประกอบ pipeline ครบชุด' if lang=='th' else 'Compose the complete workflow')+'</h3><pre><code>'+E('from workbench.runtime import run, request, FixtureProvider\nfrom workbench.core import release_gate\n\nresult = run(request(), FixtureProvider())\nassert result["state"] == "accepted_draft"\nassert result["external_effects"] == 0\nprint(result["trace"])\nprint(release_gate({}).state)  # review: missing release evidence')+'</code></pre>'
        section('code',f'<p>{note}</p>\n<pre><code>{E(excerpt(p))}</code></pre>\n'+extra+f'<p>{prose_html(prose[3])}</p>')
        headers=['เส้นทาง','ผลที่สังเกตได้'] if lang=='th' else ['Approach','Observable outcome']
        old,new=(p['beforeth'],p['afterth']) if lang=='th' else (p['before'],p['after'])
        oldlabel,newlabel=('ก่อนเพิ่มด่านนี้','หลังเพิ่มด่านนี้') if lang=='th' else ('Before this control','After this control')
        section('outcome',f'<div class="table-wrapper"><table><thead><tr><th>{headers[0]}</th><th>{headers[1]}</th></tr></thead><tbody><tr><td>{oldlabel}</td><td>{E(old)}</td></tr><tr><td>{newlabel}</td><td>{E(new)}</td></tr></tbody></table></div>\n'+
            ('<p>ผลต่อไปนี้มาจาก fixture ที่กำหนดคำตอบไว้เพื่อตรวจสถาปัตยกรรม ไม่ใช่ผลวัดความแม่น ความเร็ว หรือต้นทุนของ Jev จริง</p>' if lang=='th' else '<p>The following output comes from scripted fixtures that verify architecture behavior. It is not a measurement of live Jev accuracy, latency, or cost.</p>')+
            f'<pre><code>{E(json.dumps(lab(p["n"]),ensure_ascii=False,indent=2))}</code></pre>')
        n=p['n']; file=f'lessons/part_{n:02d}.py'; exercise=f'exercises/part_{n:02d}.md'
        testsfile='tests/test_boundaries.py'
        sourcefile='workbench/evaluation.py' if n==14 else ('workbench/runtime.py' if n in (1,3,13,15) else 'workbench/core.py')
        test_lines=(COMPANION/testsfile).read_text().splitlines()
        test_line=next(i+1 for i,line in enumerate(test_lines) if 'def '+p['test']+'(' in line)
        links=f'<p><a href="{URL}/blob/{REV}/{file}">Part {n:02d} code</a> · <a href="{URL}/blob/{REV}/{sourcefile}">Implementation</a> · <a href="{URL}/blob/{REV}/{testsfile}#L{test_line}">Tests: {E(p["test"])}</a> · <a href="{URL}/blob/{REV}/{exercise}">Exercise</a></p>'
        if n==5:links+=f'<p><a href="{URL}/blob/{REV}/workbench/jev.py">Jev HTTP adapter</a> · <a href="{URL}/blob/{REV}/tests/test_jev_adapter.py">Adapter contract tests</a></p>'
        command=f'git clone {URL}.git\ncd ai-core-engineering-workbench\ngit checkout {REV}\npython3 -m workbench.lesson {n}\npython3 -m unittest tests.test_boundaries.BoundaryTests.{p["test"]} -v'
        practice=links+f'<pre><code>{E(command)}</code></pre>'
        practice+=f'<h3>{"ลองทำด้วยตัวเอง" if lang=="th" else "Your turn"}</h3><p>{E(p["exerciseth" if lang=="th" else "exercise"])}</p>'
        practice+=('<p>สิ่งที่ต้องส่ง: input ที่ลอง สถานะและเหตุผลที่ได้ และคำอธิบายว่าด่านใดเป็นผู้รับผิดชอบ ห้ามแก้ expected result เพียงเพื่อให้ test ผ่าน</p>' if lang=='th' else '<p>Keep three artifacts: the input you tried, the resulting state and reason, and an explanation of which boundary owns that result. Do not change an expected result merely to make a test pass.</p>')
        section('practice',practice)
        refs='<section class="references" aria-labelledby="sources"><h3 id="sources">'+('เอกสารต้นทางและข้อจำกัด' if lang=='th' else 'Primary sources and evidence limits')+'</h3>'
        refs+=('<p class="references__note">ตรวจเอกสาร 2 พฤศจิกายน 2026 ตัวอย่างและ threshold เป็นการออกแบบเพื่อการสอน การอ้าง [1], [2] ตรงกับลำดับข้างล่าง ยังไม่ได้วัด live API</p>' if lang=='th' else '<p class="references__note">Sources checked 2 November 2026. Examples and thresholds are teaching designs. Inline [1], [2] follow the order below. Live API performance has not been measured.</p>')
        refs+='<ol class="references__list">'
        for refnum,(name,url,supports) in enumerate(p['refs'],1):
            refs+=f'<li id="ref-{refnum}"><a href="{url}">{E(name)}</a><span class="ref-supports" lang="en">{E(supports)}</span></li>'
        refs+='</ol></section>'
        section('references',refs)
        (ROOT/'.bilingual'/f'{p["slug"]}.{lang}.html').write_text('\n\n'.join(out)+'\n')

def companion_materials():
    (COMPANION/'lessons').mkdir(exist_ok=True);(COMPANION/'exercises').mkdir(exist_ok=True)
    (COMPANION/'lessons/__init__.py').write_text('')
    for p in PARTS:
        n=p['n']
        (COMPANION/f'lessons/part_{n:02d}.py').write_text(f'"""Part {n}: {p["title"]}. Run from repo root with python3 -m lessons.part_{n:02d}."""\nimport json\nfrom workbench.labs import lab\n\nif __name__ == "__main__":\n    print(json.dumps(lab({n}), indent=2))\n')
        text=f'# Part {n:02d} — {p["title"]}\n\n{p["exercise"]}\n\n{p["exerciseth"]}\n\nRun `python3 -m workbench.lesson {n}`.\n\nTarget test: `{p["test"]}` in `tests/test_boundaries.py`.\n\nKeep input, actual state/reason and your explanation. The test protects a boundary; do not weaken policy to force a pass.\n\nExpected architectural change: {p["after"]}\n\nSee [the lesson](https://anirach.com/blog/{p["slug"]}.html).\n'
        (COMPANION/f'exercises/part_{n:02d}.md').write_text(text)
    mapping='\n'.join(f'| {p["n"]:02d} | [{p["short"]}](https://anirach.com/blog/{p["slug"]}.html) | [Code](lessons/part_{p["n"]:02d}.py) · [Exercise](exercises/part_{p["n"]:02d}.md) | `{p["test"]}` |' for p in PARTS)
    readme='''# Software Engineering with AI-Core, Jev & Skills

The runnable companion to **15 bilingual engineering lessons on [anirach.com](https://anirach.com/blog/#series-ai-engineering)**. Start with familiar functions; end with a guarded issue-to-patch workflow whose permissions, decisions and outcomes are inspectable.

The capstone is **Patch Workbench**: an issue selects a reviewed pricing skill, a candidate is proposed, exact checks inspect its structure and behavior, and a separate quality gate assesses the explanation. Its output is an in-memory draft for human review. It does not open a PR, merge, deploy, write a repository, or execute generated Python.

## Quick start

Python **3.11+**, Git, and a terminal. No packages, API keys or network access are needed after cloning. Windows: replace `python3` with `py -3` if needed.

```sh
git clone https://github.com/Anirach/ai-core-engineering-workbench.git
cd ai-core-engineering-workbench
python3 -m unittest discover -v
python3 -m workbench.lesson 1
python3 -m workbench.lesson all
python3 -m workbench.evaluation
```

Run from the repository root. You can also run one standalone entry point with `python3 -m lessons.part_01`. No installation or virtual environment is required. The release tag `v1.0.0` identifies the original tested course snapshot.

## Architecture

```mermaid
flowchart TD
    A[Decoded issue] --> B[Exact input checks]
    B --> C[Authenticated host policy]
    C --> D[Jev: typed route and bypass judgment]
    D --> E[Validate response, then interpret uncertainty]
    E --> F[Reviewed skill and context snapshot]
    F --> G[Candidate provider]
    G --> H[Output envelope and restricted AST]
    H --> I[Independent behavior oracle]
    I --> J[Separate explanation quality gate]
    J --> K[Accepted in-memory draft]
    I -->|revise within budget| G
    J -->|revise within budget| G
    B -->|invalid| R[Reject or human review]
    C -->|denied| R
    E -->|uncertain| R
    H -->|invalid| R
    K --> L[Human review; no external effect]
```

`workbench/core.py` is the functional core. `runtime.py` coordinates provider calls, gates, revisions and trace assembly. `jev.py` is the optional HTTP decision adapter. `skills/pricing-patch/SKILL.md` describes the task; the host-side `SKILL` contract enforces scope. The small duplication is explicit and must be reviewed together when changing the skill.

## Three visibly different outcomes

| Experiment | Command | Key result |
|---|---|---|
| Malformed issue | `python3 -m workbench.lesson 4` | `reject`, zero provider calls |
| Forbidden merge action | `python3 -m workbench.lesson 8` | `action_denied`, zero effects |
| Valid syntax, wrong arithmetic | `python3 -m workbench.lesson 11` | shape passes, behavior requests revision |
| Correct behavior, weak explanation | `python3 -m workbench.lesson 12` | final `review` |
| Wrong candidate followed by correct candidate | `python3 -m workbench.lesson 13` | accepted draft, 2 attempts, 4 logical calls |
| Passing draft, missing release evidence | `python3 -m workbench.lesson 15` | runtime accepted, release review |

All default decisions are **scripted fixtures**. They prove control-flow behavior, not Jev accuracy, detection quality, latency or cost. Unknown usage and live metrics remain `null`. Logical provider calls are not HTTP calls or token counts.

## Lesson-to-code map

Each lesson links the implementation, a matching boundary test and an exercise. Tests live in `tests/test_boundaries.py`.

| Part | Website | Companion | Matching test |
|---|---|---|---|
MAPPING

## Optional real Jev decisions

The official API contract was checked on **2 November 2026** against [TypeSafe API docs](https://docs.typesafe.ai/api/system-one), [Choice](https://docs.typesafe.ai/primitives/choice), [Noul](https://docs.typesafe.ai/primitives/noul) and [confidence](https://docs.typesafe.ai/confidence). The adapter pins `jev-1.14.0`; verify that your account can use it. No live paid API call was made while authoring this companion.

Set `TYPESAFE_API_KEY` through your shell's secret mechanism, then intentionally opt in:

```sh
python3 -m workbench.live --allow-paid-api
```

This sends a synthetic issue and synthetic summary to `https://api.typesafe.ai/v1/systemone`. It makes real routing and quality decisions, but **generation remains a reviewed local fixture**. Jev does not write code here. `candidate_hash` is a local response-envelope field, not a Jev API field or signature. Provider usage is retained separately; this example does not calculate monetary cost. A genuine generative-model adapter is an extension exercise, not an implemented integration.

The adapter makes no automatic transport retries, follows no redirects, limits response size and uses an HTTP timeout. The shell checks elapsed time before and after calls; it cannot interrupt a blocking call. A production deadline needs cancellation and remaining-time propagation. HTTP 401/422 require configuration/request repair; 429/529 may justify bounded backoff in a separately tested adapter. Any provider failure returns review.

## Limits that matter

- The candidate language is one integer expression using `+ - * //`. AST parsing plus a small interpreter is a teaching language, **not a general Python sandbox**. No `eval`, `exec`, imports or subprocess runs are used for candidates.
- The pricing domain is integer price >= 0 and integer percent in [0,100]. Trusted examples satisfy it; a real service must validate its numeric invocation inputs too.
- Six examples and selected monotonicity checks do not prove correctness for all inputs. Keep an independent oracle and held-out cases.
- Semantic screening and quality judging are fallible. The `.8`, `.2` and `.9` thresholds are illustrative; validate against labeled local traffic and language slices.
- The release checklist is a toy. It does not authenticate signoff or verify CI artifacts. An accepted draft does not authorize production release.
- The manifest is a tutorial subset. Production also needs application/runtime revision, generator configuration, immutable evidence and evaluation data identities.
- There is no persistence, concurrency control, remote idempotency ledger, PR gateway, or production isolation layer. Add those before granting effectful tools.

## Evaluation protocol

Keep development, validation and held-out data disjoint. Freeze thresholds before running held-out evaluation. Report acceptance coverage with accepted-error rate, review/reject rates, language/task slices and human label agreement. Include decisions, generation, retries, fallback, review and rework in cost per successful task. A scripted perfect agreement is not model performance; a missing metric is not zero.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `No module named workbench` | Run from the cloned repository root. |
| Python syntax/version error | Use Python 3.11 or later. |
| Live run requests a key | Offline lessons need no key; live calls require your own TypeSafe account. |
| Live run returns review | Inspect stage/reason and provider usage; check model availability, schema and transport status. Do not weaken a gate to force acceptance. |
| Correct code is rejected | Check the intentionally small language contract. General Python is outside the tutorial scope. |
| Cost or accuracy is `null` | No valid live measurement was collected; retain the unknown value. |

## Extend it responsibly

Add a second reviewed skill, implement a separate generator adapter, build a held-out evaluator, or design a PR gateway with approval bound to repository/base revision/candidate hash. Preserve all gates and re-run the boundary suite. Exercises state expected architectural outcomes without supplying a pretend production guarantee.

MIT licensed. Author: Anirach Mingkhwan. Educational code; source and model documentation can evolve after the pinned snapshot.
'''.replace('MAPPING',mapping)
    (COMPANION/'README.md').write_text(readme)

def main():
    (ROOT/'.bilingual').mkdir(exist_ok=True)
    overview()
    for p in PARTS:diagram(p);sheets(p)
    companion_materials()
    template=json.loads((ROOT/'scripts/series/ai-core-functional.json').read_text())
    template.update(series='ai-engineering',title='Software Engineering with AI-Core',aria_label='Software Engineering with AI-Core',
        section_id='series-ai-engineering',date='2026-11-02',h3='Software Engineering with AI-Core · 15-Part Course',
        hero_series='Software Engineering with AI-Core 2026 • Post #%d',icon='⌘',
        description={'en':'An architecture course for programmers: build one guarded coding workbench with functions, Jev, skills and independent quality gates.',
                     'th':'คอร์สสถาปัตยกรรมสำหรับโปรแกรมเมอร์ สร้าง coding workbench ผ่าน function, Jev, skill และด่านคุณภาพที่ตรวจแยกได้'},
        groups=[{'key':'design','label':'Design · ออกแบบ'},{'key':'control','label':'Control · ควบคุม'},{'key':'prove','label':'Prove · พิสูจน์'}])
    template['footer']={'th':'จากซีรีส์ Software Engineering with AI-Core','en':'From Software Engineering with AI-Core'}
    template['extra_css']='''    .callout { background: var(--cloud); border-left: 4px solid var(--blue);
      border-radius: var(--radius); padding: 1.2rem 1.4rem; margin: 1.5rem 0; }
    .callout h3 { margin-top: 0; }
    .callout p:last-child { margin-bottom: 0; }'''
    template['covers']={'eyebrow':'AI-CORE ENGINEERING','accent':'blue','grounds':['cloud','parchment'],'motif_prefix':'eng_'}
    posts=[]
    for p in PARTS:
        fig={'name':'flow','file':p['slug']+'-flow.png','alt':{'en':f'Part {p["n"]}: '+p['before']+' The controlled path is '+' to '.join(p['nodes'])+'. '+p['after'],
            'th':f'ตอน {p["n"]}: '+p['beforeth']+' → '+p['afterth']},'caption':{'en':'Figure 1. '+p['artifact']+'. Open the diagram for full resolution.',
            'th':'ภาพที่ 1 ขอบเขตหน้าที่และเส้นทางหยุด เปิดภาพเพื่อดูขนาดเต็ม'}}
        figs=[fig]
        if p['n'] in (1,15):figs.append({'name':'overview','file':'ai-engineering-architecture.png','alt':{
            'en':'Complete pipeline: input, policy, Jev response validation, semantic input, context, candidate, output language, behavior, quality, human review. All non-pass paths stop or use bounded revision.',
            'th':'ทางเดินครบ: input, policy, Jev, semantic input, context, candidate, output, behavior, quality และมนุษย์ตรวจ งานไม่ผ่านต้องหยุดหรือแก้ภายในงบ'},
            'caption':{'en':'Figure 2. The complete workflow. Models propose; host code mediates. Release approval is separate.',
                       'th':'ภาพที่ 2 workflow ครบชุด โมเดลเสนอ host ควบคุม และแยกการอนุมัติ release'}})
        desc=f'AI-Core Engineering #{p["n"]}: '+p['subth']
        if len(desc)>160:desc=desc[:157]+'...'
        posts.append({'n':p['n'],'slug':p['slug'],'chip':p['chip'],'nav_title':p['short'],
            'title':{'th':p['th'],'en':p['title']},'sub':{'th':p['subth'],'en':p['sub']},
            'tags':['AI-Core','Jev','Software Architecture'],'description':desc,'read_min':7,
            'cover':p['slug']+'-cover.jpg','figures':figs,'group':('design' if p['n']<=5 else 'control' if p['n']<=10 else 'prove')})
    template['posts']=posts
    (ROOT/'scripts/series/ai-engineering.json').write_text(json.dumps(template,ensure_ascii=False,indent=1)+'\n')
    rows=(ROOT/'scripts/covers.tsv').read_text().splitlines()
    rows=[r for r in rows if not r.startswith('ai-engineering-')]
    for p in PARTS:
        rows.append('\t'.join([p['slug'],p['slug']+'-cover.jpg','eng_'+str(p['n']),
            'cloud' if p['n']%2 else 'parchment','blue',f'AI-CORE ENGINEERING · {p["n"]:02d}/15',p['short'],p['th'].split(' — ')[-1],f'part={p["n"]}']))
    (ROOT/'scripts/covers.tsv').write_text('\n'.join(rows)+'\n')
    print('Prepared 15 bilingual sheet pairs, 16 diagrams, manifest, cover rows and companion materials.')

if __name__=='__main__':main()
