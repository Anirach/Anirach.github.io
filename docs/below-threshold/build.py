"""Prepare the chapter tutorials, their provenance, and offline examples.

Then run scripts/build_series.py --series below-threshold --all.
Book source files are read only; public download links use the owner's Drive file.
"""
import argparse
import hashlib
import html
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DATE='2026-11-25'
VIEW='https://drive.google.com/file/d/1iG7oSWLC9UI91VsPOzqcxk3_evH8Sn3b/view?usp=sharing'
DOWNLOAD='https://drive.google.com/uc?export=download&id=1iG7oSWLC9UI91VsPOzqcxk3_evH8Sn3b'
ZIP='below-threshold-tutorial-examples.zip'
BOOK_SHA256='08f3f4e402d968a31a173dbfe61cd53ff768ecbdefeb86ce43c33ccd8a239f86'
FIGURE_NUMBERS=dict(zip(
    ['bridges','error-path','repetition','surface-code','threshold','qec-cycle','decoders','mitigation','synthesis','workflow','sb','tt','voting','codegen','sdd','decision-tree','timeline'],
    ['1.1','2.1','3.1','3.2','3.3','4.1','4.2','5.1','6.1','7.1','8.1','8.2','9.1','9.2','9.3','10.1','10.2']))


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def downloads(lang):
    if lang=='th':
        heading='ดาวน์โหลดหนังสือและโค้ดประกอบ'
        label='ดาวน์โหลด Below Threshold ฉบับเต็ม (PDF ภาษาอังกฤษ · 104 หน้า · 5.4 MB)'
        view='อ่านบน Google Drive';code='ดาวน์โหลดตัวอย่าง Python ทั้งสิบบท (ZIP)'
    else:
        heading='Download the book and examples'
        label='Download the complete Below Threshold book (English PDF · 104 pages · 5.4 MB)'
        view='Read on Google Drive';code='Download all ten Python examples (ZIP)'
    return (f'<blockquote><p><strong>{heading}</strong></p><p><a href="{html.escape(DOWNLOAD,quote=True)}">{label}</a><br>'
            f'<a href="{html.escape(VIEW,quote=True)}">{view}</a> · <a href="../downloads/{ZIP}" download>{code}</a></p></blockquote>\n')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--book-root',type=Path,default=Path.home()/'Documents/Below-Threshold-Book')
    args=ap.parse_args()
    pdf=args.book_root/'dist/Below-Threshold.pdf'
    if pdf.exists():
        assert digest(pdf)==BOOK_SHA256, 'Book edition changed: review chapter pages, claims and figures before rebuilding'
    parts=[]
    for f in sorted(HERE.glob('chapters-*.json')):parts+=json.loads(f.read_text())
    parts.sort(key=lambda p:p['n'])
    assert [p['n'] for p in parts]==list(range(1,11)), 'Need exactly ten chapters'
    (ROOT/'.bilingual').mkdir(exist_ok=True)
    figures={};outputs={};posts=[]
    for p in parts:
        n=p['n'];script=ROOT/'examples/below-threshold'/f'ch{n:02d}.py'
        result=subprocess.run([sys.executable,str(script)],check=True,capture_output=True,text=True,timeout=15)
        assert not result.stderr,result.stderr
        outputs[script.name]={'sha256':digest(script),'stdout':result.stdout}
        for fig in p['figures']:
            name=fig['name'];src=args.book_root/'figures'/('fig_'+name.replace('-','_')+'.png')
            dest=ROOT/'images'/('below-threshold-'+name+'.png')
            assert fig['file']==dest.name
            if src.exists():dest.write_bytes(src.read_bytes())
            assert dest.is_file(),dest
            figures[name]={'source_figure':FIGURE_NUMBERS[name],'file':dest.name,'sha256':digest(dest)}
            for lang in ('th','en'):
                credit=(f' Source: Below Threshold, Figure {FIGURE_NUMBERS[name]}. Open for full resolution.' if lang=='en'
                        else f' จากหนังสือ Below Threshold ภาพ {FIGURE_NUMBERS[name]} เปิดภาพเพื่อดูขนาดเต็ม')
                if not ((lang=='en' and re.search(r'Figure \d+\.\d+',fig['caption'][lang]))
                        or (lang=='th' and re.search(r'ภาพ \d+\.\d+',fig['caption'][lang]))):
                    fig['caption'][lang]+=credit
                if lang=='en' and 'Open for full resolution.' not in fig['caption'][lang]:
                    fig['caption'][lang]+=' Open for full resolution.'
                if lang=='th' and 'เปิดภาพ' not in fig['caption'][lang]:
                    fig['caption'][lang]+=' เปิดภาพเพื่อดูขนาดเต็ม'
        for lang in ('th','en'):
            sections=list(p['sections'])
            resources=('Run and check the example' if lang=='en' else 'Run & check — รันตัวอย่างด้วยตัวเอง')
            refs_heading='Sources and scope' if lang=='en' else 'Sources & scope — แหล่งอ้างอิงและขอบเขต'
            heads=[(s['key'],s['heading'][lang]) for s in sections]+[('resources',resources),('references',refs_heading)]
            assert len(set(k for k,_ in heads))==len(heads)
            lines=[f'<!--{lang.upper()}-TOC:{k}-->{h}' for k,h in heads]
            for i,s in enumerate(sections):
                body=s['body'][lang]
                if i==0:
                    intro=(f'<p><strong>Chapter {n}/10.</strong> A tutorial adaptation of <em>Below Threshold: AI, Quantum Errors and Better Code</em>, Edition 1.0, Chapter {n}, pp. {p["source_pages"]}.</p>' if lang=='en'
                           else f'<p><strong>บทที่ {n}/10</strong> · บทเรียนดัดแปลงจาก <em>Below Threshold: AI, Quantum Errors and Better Code</em> ฉบับ 1.0 บทที่ {n} หน้า {p["source_pages"]}</p>')
                    body=downloads(lang)+intro+body
                body=body.replace('<!--EXAMPLE-->','<pre><code>'+html.escape(script.read_text().rstrip())+'</code></pre>')
                body=body.replace('<!--EXAMPLE_OUTPUT-->','<pre><code>'+html.escape(result.stdout.rstrip())+'</code></pre>')
                lines.append(f'<!--{lang.upper()}-SECTION:{s["key"]}-->\n<h2 id="{s["key"]}">{s["heading"][lang]}</h2>\n'+body)
            resource_body=(f'<p>This complete teaching example uses only the Python standard library. Save <a href="../examples/below-threshold/{script.name}" download>{script.name}</a>, then run it with Python 3.10 or later. Its assertions check the stated invariants.</p>' if lang=='en'
                           else f'<p>ตัวอย่างสำหรับสอนนี้ใช้ Python standard library เท่านั้น บันทึก <a href="../examples/below-threshold/{script.name}" download>{script.name}</a> แล้วรันด้วย Python 3.10 ขึ้นไป โดย assertions ตรวจ invariant ที่อธิบายในบท</p>')
            resource_body+=f'<pre><code>python3 {script.name}</code></pre>'
            resource_body+=(f'<p><a href="../downloads/{ZIP}" download>All ten examples and expected output (ZIP)</a> · <a href="https://github.com/Anirach/Anirach.github.io/tree/main/examples/below-threshold">Browse example source on GitHub</a></p>' if lang=='en'
                            else f'<p><a href="../downloads/{ZIP}" download>ตัวอย่างทั้งสิบบทและผลลัพธ์ที่คาดหวัง (ZIP)</a> · <a href="https://github.com/Anirach/Anirach.github.io/tree/main/examples/below-threshold">อ่าน source บน GitHub</a></p>')
            lines.append(f'<!--{lang.upper()}-SECTION:resources-->\n<h2 id="resources">{resources}</h2>\n'+resource_body)
            note=('The author’s book is the source of the chapter structure, credited diagrams and reported lab results (November 2026 snapshot). The short standard-library example above was executed for this web lesson on 25 November 2026. It is a teaching model; the book’s full Stim, neural-network, mitigation and LLM experiments were not rerun for these posts. Hardware, simulator, preprint and company claims retain their stated scope.' if lang=='en'
                  else 'โครงบท ภาพที่ให้เครดิต และผล lab ที่รายงานมาจากหนังสือของผู้เขียน ณ November 2026 ตัวอย่างสั้นที่ใช้ standard library รันเพื่อตรวจบทเรียนเว็บวันที่ 25 November 2026 เป็นแบบจำลองเพื่อสอน ไม่ได้รันซ้ำการทดลอง Stim, neural network, mitigation หรือ LLM ฉบับเต็มในหนังสือ ข้ออ้าง hardware, simulator, preprint และบริษัทคงขอบเขตตามที่ระบุ')
            refbody=f'<section class="references" aria-labelledby="sources"><h3 id="sources">'+('Reading and evidence' if lang=='en' else 'เอกสารและหลักฐาน')+f'</h3><p class="references__note">{note}</p><ol>'
            refbody+=f'<li><a href="{html.escape(VIEW,quote=True)}">Anirach Mingkhwan. Below Threshold: AI, Quantum Errors and Better Code. Edition 1.0 (November 2026), Chapter {n}, pp. {p["source_pages"]}.</a></li>'
            for j,ref in enumerate(p['refs'],1):refbody+=f'<li id="ref-{j}"><a href="{html.escape(ref["url"],quote=True)}">{html.escape(ref["title"])}</a></li>'
            refbody+='</ol></section>'
            lines.append(f'<!--{lang.upper()}-SECTION:references-->\n<h2 id="references">{refs_heading}</h2>\n'+refbody)
            (ROOT/'.bilingual'/f'{p["slug"]}.{lang}.html').write_text('\n\n'.join(lines)+'\n')
        assert 70<=len(p['description'])<=160,(n,len(p['description']))
        posts.append({k:p[k] for k in ('n','slug','title','sub','description','figures')}|{
            'chip':f'#{n} '+p['short'],'nav_title':p['short'],'tags':['Quantum Computing','AI Engineering','Python'],
            'read_min':7,'cover':p['slug']+'-cover.jpg'})
    man=json.loads((ROOT/'scripts/series/quantum-programmers.json').read_text())
    man.update(series='below-threshold',title='Below Threshold: AI, Quantum Errors and Better Code',icon='λ',aria_label='Below Threshold',
               section_id='series-below-threshold',date=DATE,h3='Below Threshold · 10-Chapter Course',hero_series='Below Threshold 2026 • Chapter #%d',
               footer={'th':'จากซีรีส์ Below Threshold','en':'From Below Threshold'},
               description={'th':'บทเรียนสิบตอนตามหนังสือ จาก quantum errors และ AI decoder สู่ quantum-inspired algorithms และโค้ดที่ตรวจสอบได้ พร้อมดาวน์โหลดหนังสือทุกตอน',
                            'en':'Ten chapter-by-chapter tutorials on quantum errors, AI decoders and better code, with the book’s diagrams, runnable examples and a full-book download in every lesson.'},
               covers={'eyebrow':'BELOW THRESHOLD','accent':'violet','grounds':['cloud','parchment'],'motif_prefix':'bt_'},
               posts=posts,references=True,figure_prefix='below-threshold-',extra_css='')
    (ROOT/'scripts/series/below-threshold.json').write_text(json.dumps(man,ensure_ascii=False,indent=1)+'\n')
    rows=[r for r in (ROOT/'scripts/covers.tsv').read_text().splitlines() if not r.startswith('below-threshold-')]
    for p in parts:
        rows.append('\t'.join([p['slug'],p['slug']+'-cover.jpg','bt_'+str(p['n']),'cloud' if p['n']%2 else 'parchment','violet',f'BELOW THRESHOLD · {p["n"]:02d}/10',p['short'],p['title']['th'].split(' — ')[-1],f'part={p["n"]}']))
    (ROOT/'scripts/covers.tsv').write_text('\n'.join(rows)+'\n')
    (HERE/'verified-examples.json').write_text(json.dumps({'verified_date':DATE,'examples':outputs},indent=2)+'\n')
    assert set(figures)==set(FIGURE_NUMBERS), 'The series must include all 17 credited book figures'
    (HERE/'source-figures.json').write_text(json.dumps({'book':'Below Threshold, Edition 1.0','source_pdf_sha256':BOOK_SHA256,'pages':104,'download':DOWNLOAD,'view':VIEW,'illustrations':figures},indent=2)+'\n')
    expected=''.join(f'## {name}\n{v["stdout"]}\n' for name,v in outputs.items()).rstrip()+'\n'
    (ROOT/'examples/below-threshold/expected-output.txt').write_text(expected)
    with zipfile.ZipFile(ROOT/'downloads'/ZIP,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for f in sorted((ROOT/'examples/below-threshold').glob('*')):
            if f.is_file():
                info=zipfile.ZipInfo('below-threshold-examples/'+f.name,date_time=(2026,11,25,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
                z.writestr(info,f.read_bytes())
    print(f'Prepared {len(parts)} bilingual chapters, {len(figures)} figures and {len(outputs)} executed teaching examples.')


if __name__=='__main__':main()
