"""Prepare reproducible editorial sheets, manifest and cover rows.

Run with the companion installed in the active Python environment, then use
scripts/build_series.py --series quantum-programmers --all.
"""
import argparse
import hashlib
import html
import importlib
import inspect
import json
import subprocess
import sys
from pathlib import Path
from posts import PARTS

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
URL='https://github.com/Anirach/quantum-algorithms-for-programmers'
DATE='2026-11-24'
REFS={
 'bit-order':('IBM Quantum. Bit ordering in the Qiskit SDK.','https://quantum.cloud.ibm.com/docs/en/qiskit/bit-ordering'),
 'qiskit':('Javadi-Abhari et al. Quantum computing with Qiskit (2024).','https://arxiv.org/abs/2405.08810'),
 'survey':('Montanaro. Quantum algorithms: an overview (2016).','https://arxiv.org/abs/1511.04206'),
 'grover':('Grover. A fast quantum mechanical algorithm for database search (1996).','https://arxiv.org/abs/quant-ph/9605043'),
 'zalka':('Zalka. Grover’s quantum searching algorithm is optimal (1999).','https://arxiv.org/abs/quant-ph/9711070'),
 'overheads':('Babbush et al. Focus beyond quadratic speedups for error-corrected quantum advantage (2021).','https://arxiv.org/abs/2011.04149'),
 'shor':('Shor. Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer (1997).','https://arxiv.org/abs/quant-ph/9508027'),
 'arithmetic':('Beckman et al. Efficient networks for quantum factoring (1996).','https://arxiv.org/abs/quant-ph/9602016'),
 'gidney':('Gidney. How to factor 2048 bit RSA integers with less than a million noisy qubits (2025).','https://arxiv.org/abs/2505.15917'),
 'nist':('NIST. First three finalized post-quantum cryptography standards (2024).','https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards'),
 'hhl':('Harrow, Hassidim & Lloyd. Quantum algorithm for solving linear systems of equations (2009).','https://arxiv.org/abs/0811.3171'),
 'fineprint':('Aaronson. Quantum machine learning algorithms: read the fine print (2015).','https://www.scottaaronson.com/papers/qml.pdf'),
 'precision':('Childs, Kothari & Somma. Quantum linear systems with exponentially improved dependence on precision (2017).','https://arxiv.org/abs/1511.02306'),
 'tang':('Tang. A quantum-inspired classical algorithm for recommendation systems (2019).','https://arxiv.org/abs/1807.04271'),
 'qaoa':('Farhi, Goldstone & Gutmann. A quantum approximate optimization algorithm (2014).','https://arxiv.org/abs/1411.4028'),
 'gw':('Goemans & Williamson. Improved approximation algorithms for maximum cut and satisfiability problems (1995).','https://doi.org/10.1145/227683.227684'),
 'obstacles':('Bravyi et al. Obstacles to state preparation and variational optimization from symmetry protection (2019/2020).','https://arxiv.org/abs/1910.08980'),
 'plateaus':('McClean et al. Barren plateaus in quantum neural network training landscapes (2018).','https://arxiv.org/abs/1803.11173'),
 'feynman':('Feynman. Simulating physics with computers (1982).','https://doi.org/10.1007/BF02650179'),
 'lloyd':('Lloyd. Universal quantum simulators (1996).','https://doi.org/10.1126/science.273.5278.1073'),
 'simulation':('IBM Quantum Learning. Simulating nature.','https://quantum.cloud.ibm.com/learning/en/courses/quantum-computing-in-practice/simulating-nature'),
 'chemistry':('Reiher et al. Elucidating reaction mechanisms on quantum computers (2017).','https://arxiv.org/abs/1605.03590'),
 'errorcorrection':('Google Quantum AI and collaborators. Quantum error correction below the surface code threshold (2024/2025).','https://arxiv.org/abs/2408.13687'),
}

# Every caption carries the diagram's teaching point; labels inside source art
# remain English, while alt text, captions and explanation have both tracks.
FIGURES={
 'bloch':('A pure qubit has probabilities set by θ and a relative phase φ that later gates can reveal.','pure qubit มี θ กำหนด probability และมี relative phase φ ที่ gate ถัดไปเปลี่ยนให้วัดเห็นได้'),
 'pattern':('Prepare, encode, interfere, measure: Grover, Shor, HHL and QAOA share a pattern, with classical work after readout.','Grover, Shor, HHL และ QAOA ใช้ prepare, encode, interfere, measure และมี classical work ต่อจากการวัด'),
 'amplitudes':('For N=16, the oracle changes a sign; the diffuser raises the marked amplitude. Three rounds give 96.13% success.','N=16: oracle กลับเครื่องหมาย แล้ว diffuser ขยาย marked amplitude หลังสามรอบมีโอกาสสำเร็จ 96.13%'),
 'rotation':('Two reflections rotate by 2θ per round; three rounds at N=16 stop just beyond the solution axis.','reflection สองครั้งหมุน state ครั้งละ 2θ สำหรับ N=16 สามรอบหยุดเลยแกนคำตอบเล็กน้อย'),
 'overrotation':('Success oscillates with iteration count. Running beyond the chosen stopping point reduces success.','โอกาสสำเร็จขึ้นลงตามจำนวนรอบ การรันเกิน stopping point ทำให้คำตอบแย่ลง'),
 'grover-circuit':('Four qubits: H preparation, three oracle–diffuser pairs, then computational-basis measurement.','สี่ qubits: เตรียมด้วย H ทำ oracle–diffuser สามคู่ แล้ววัดใน computational basis'),
 'oracle-diffuser':('The oracle maps target 1011 to 1111 before a controlled phase flip; the diffuser wraps another phase flip in H and X.','oracle map 1011 ไป 1111 ก่อน controlled phase flip ส่วน diffuser ใช้ H และ X ครอบ phase flip อีกครั้ง'),
 'queries':('Oracle-query scaling only: N and N/2 versus approximately π√N/4. Per-query gates and data access are excluded.','นับเฉพาะ oracle queries: N และ N/2 เทียบกับประมาณ π√N/4 ยังไม่นับ gate ภายในและ data access'),
 'shor-flow':('Shor is a classical loop around quantum order finding. Unusable orders or trivial factors require another attempt.','Shor เป็น classical loop ที่ครอบ quantum order finding หาก order ใช้ไม่ได้หรือได้ trivial factors ต้องลองใหม่'),
 'period':('Powers of 7 modulo 15 repeat as 1,7,4,13, giving the order r=4.','กำลังของ 7 modulo 15 วนเป็น 1,7,4,13 จึงมี order r=4'),
 'qft':('Four-qubit QFT with controlled phase rotations and final swaps. The companion verifies its inverse against the inverse DFT.','QFT สี่ qubits ใช้ controlled phase rotations และ final swaps โดย companion ตรวจ inverse กับ inverse DFT โดยตรง'),
 'shor-circuit':('Eight counting qubits control modular multiplications on four work qubits before inverse QFT and readout.','counting qubits แปดตัวควบคุม modular multiplication บน work qubits สี่ตัว ก่อน inverse QFT และอ่านผล'),
 'hhl-flow':('HHL prepares a normalized solution state through phase estimation, reciprocal rotations, uncomputation and post-selection.','HHL เตรียม normalized solution state ผ่าน phase estimation, reciprocal rotation, uncomputation และ post-selection'),
 'hhl-circuit':('For this spectrum only, clock 01 and 10 select rotations π and π/3, followed by uncomputation and ancilla measurement.','เฉพาะ spectrum นี้ clock 01 กับ 10 เลือก rotation π กับ π/3 จากนั้น uncompute และวัด ancilla'),
 'qaoa-flow':('The classical optimizer chooses angles; the quantum circuit prepares states and supplies samples.','classical optimizer เลือกมุม ส่วน quantum circuit เตรียม state และส่ง samples กลับมา'),
 'qaoa-circuit':('One prism-graph layer has nine RZZ cost gates and six RX mixer gates. More layers add parameters and depth.','หนึ่ง layer ของ prism graph มี RZZ เก้า gates และ RX หก gates การเพิ่ม layer เพิ่มทั้ง parameters และ depth'),
 'grover-results':('Rerun: 3,928 of 4,096 ideal shots measured 1011, consistent with the exact probability 0.961319.','ผลรันซ้ำ: ideal shots 3,928 จาก 4,096 ครั้งได้ 1011 สอดคล้องกับ exact probability 0.961319'),
 'shor-results':('Rerun: phases 1/4 and 3/4 recover r=4; phases 0 and 1/2 require a retry in this implementation.','ผลรันซ้ำ: phase 1/4 และ 3/4 กู้ r=4 ได้ ส่วน 0 และ 1/2 ต้อง retry ใน implementation นี้'),
 'hhl-results':('Rerun: classical, exact-state and accepted-shot probabilities agree near 0.9:0.1; probabilities hide relative sign.','ผลรันซ้ำ: classical, exact state และ shots ที่ผ่านให้โอกาสใกล้ 0.9:0.1 แต่ probability ซ่อน relative sign'),
 'qaoa-results':('Rerun: expected cut rises with depth on this instance; the best sampled partition cuts seven of nine prism edges.','ผลรันซ้ำ: expected cut เพิ่มตาม depth ใน instance นี้ ส่วน partition ที่ดีที่สุด cut ได้เจ็ดจากเก้า edges'),
 'simulation-flow':('Choose a Hamiltonian, compile time evolution, prepare the state and estimate a specified observable.','เลือก Hamiltonian, compile time evolution, เตรียม state แล้วประมาณ observable ที่กำหนด'),
 'simulation-results':('New experiment: increasing product-formula steps approaches the exact ZZ expectation and reduces state infidelity in an ideal circuit.','experiment ใหม่: เพิ่ม product-formula steps ทำให้ค่า ZZ เข้าใกล้ exact และลด state infidelity ใน ideal circuit'),
 'engineering-flow':('Define the classical baseline, input contract, quantum resource budget and output validation as one system.','นิยาม classical baseline, input contract, quantum resource budget และ output validation เป็นระบบเดียวกัน'),
 'cost-ledger':('Illustration: 0.8 seconds preparation + five 0.1-second attempts + 0.2 seconds postprocessing exceeds a one-second baseline.','ตัวอย่างสมมติ: prepare 0.8 วินาที + ห้า attempts ครั้งละ 0.1 วินาที + postprocess 0.2 วินาที รวมช้ากว่า baseline หนึ่งวินาที'),
}

INLINE={1:{'state':['bit-order'],'pattern':['survey']},
 2:{'problem':['grover','zalka'],'results':['overheads']},
 3:{'problem':['shor'],'fourier':['arithmetic'],'outcomes':['gidney','nist']},
 4:{'contract':['hhl','precision'],'fineprint':['fineprint','tang']},
 5:{'hamiltonian':['qaoa'],'limits':['gw','obstacles','plateaus']},
 6:{'task':['feynman','lloyd'],'scope':['simulation','chemistry']},
 7:{'resources':['errorcorrection'],'decision':['nist']}}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--companion',type=Path,default=Path.home()/'Projects/quantum-algorithms-for-programmers')
    args=ap.parse_args();comp=args.companion.resolve();sys.path.insert(0,str(comp))
    rev=subprocess.check_output(['git','rev-parse','HEAD'],cwd=comp,text=True).strip()
    results=json.loads((HERE/'verified-results.json').read_text())
    provenance=json.loads((HERE/'source-figures.json').read_text())['illustrations']
    posts=[];(ROOT/'.bilingual').mkdir(exist_ok=True)
    for p in PARTS:
        mod=importlib.import_module(p['module'])
        code='\n\n'.join(inspect.getsource(getattr(mod,name)).strip() for name in p['functions'])
        figures=[]
        for name in p['figures']:
            en,th=FIGURES[name];source=provenance.get(name)
            addon_en=(f' Source: author’s guide, Figure {source["source_figure"]}.' if source else ' Generated from the companion experiment or teaching model.')+' Open for full resolution.'
            addon_th=(f' จากเอกสารผู้เขียน ภาพ {source["source_figure"]}' if source else ' สร้างจาก companion experiment หรือแบบจำลองเพื่อการสอน')+' เปิดภาพเพื่อดูขนาดเต็ม'
            figures.append({'name':name,'file':'quantum-'+name+'.png','alt':{'en':en,'th':th},'caption':{'en':en+addon_en,'th':th+addon_th}})
        for lang in ('th','en'):
            headings=[(s['key'],s['heading'][lang]) for s in p['sections']]+[('practice','Run & explore — ลงมือทดลอง' if lang=='th' else 'Run and explore'),('references','Sources & verification — แหล่งอ้างอิง' if lang=='th' else 'Sources and verification')]
            lines=[f'<!--{lang.upper()}-TOC:{key}-->{title}' for key,title in headings]
            def section(key,title,body):lines.append(f'<!--{lang.upper()}-SECTION:{key}-->\n<h2 id="{key}">{title}</h2>\n'+body)
            for i,s in enumerate(p['sections']):
                body=s['body'][lang]
                if i==0:
                    source_pages={1:'5–8',2:'9–15',3:'16–23',4:'24–28',5:'29–34',6:'35',7:'36–40'}[p['n']]
                    body=('<p><strong>บทที่ '+str(p['n'])+'/7</strong> · ดัดแปลงจากเอกสาร Quantum Algorithms for Programmers, Edition 1.0 หน้า '+source_pages+' พร้อมโค้ดและคำอธิบายที่ตรวจซ้ำสำหรับเว็บ</p>' if lang=='th' else '<p><strong>Part '+str(p['n'])+'/7.</strong> Adapted from Quantum Algorithms for Programmers, Edition 1.0, pp. '+source_pages+', with web explanations and rerun code.</p>')+body
                if '<!--CODE-->' in body:
                    note=('ส่วนโค้ดสำหรับอ่านแนวคิด ใช้ไฟล์เต็มพร้อม imports จาก companion และคำสั่งใน Run &amp; explore ด้านล่าง' if lang=='th' else 'Implementation excerpt. Use the complete companion file with its imports and the Run and explore commands below.')
                    body=body.replace('<!--CODE-->','<p>'+note+'</p>\n<pre><code>'+html.escape(code)+'</code></pre>')
                body=body.replace('<!--OUTPUT-->','<p><strong>'+('ผลรันที่บันทึก 24 November 2026' if lang=='th' else 'Captured run, 24 November 2026')+'</strong></p>\n<pre><code>'+html.escape(results[p['module']]['stdout'].rstrip())+'</code></pre>')
                # Part 1 also needs its measured experiment, without duplicating a section.
                if p['n']==1 and s['key']=='interference':body+='<pre><code>'+html.escape(results[p['module']]['stdout'].rstrip())+'</code></pre>'
                keys=INLINE.get(p['n'],{}).get(s['key'],[])
                if keys:
                    links=' · '.join(f'<a href="#ref-{p["refs"].index(k)+1}">[{p["refs"].index(k)+1}]</a>' for k in keys)
                    body+='<p>'+('อ้างอิง: ' if lang=='th' else 'Sources: ')+links+'</p>'
                section(s['key'],s['heading'][lang],body)
            testlines=(comp/'tests/test_algorithms.py').read_text().splitlines()
            testline=next(i+1 for i,line in enumerate(testlines) if line.startswith('class '+p['test']+'('))
            links=f'<p><a href="{URL}/blob/{rev}/{p["module"]}.py">Complete code</a> · <a href="{URL}/blob/{rev}/tests/test_algorithms.py#L{testline}">{p["test"]}</a> · <a href="{URL}/blob/{rev}/exercises/{p["n"]:02d}.md">Exercise</a> · <a href="{URL}/blob/{rev}/README.md">Setup &amp; troubleshooting</a></p>'
            commands=''
            if p['n']==1:
                commands=f'git clone {URL}.git\ncd quantum-algorithms-for-programmers\ngit checkout {rev}\npython3 -m venv .venv\nsource .venv/bin/activate\npython -m pip install -r requirements.txt\n'
            else:commands='# From the companion root, with the virtual environment active\n'
            commands+=f'python {p["module"]}.py\npython -m unittest discover -s tests -p test_algorithms.py -k {p["test"]} -v'
            prereq=('ใช้ Python 3.12–3.13 และ virtual environment ตาม README ไม่ต้องใช้ API key หรือ quantum hardware หากยังไม่ติดตั้งให้ทำตามตอน 1 หรือ README' if lang=='th' else 'Use Python 3.12–3.13 and the README virtual environment. No API key or quantum hardware is required. If setup is incomplete, follow part 1 or the README.')
            practice=links+'<p>'+prereq+'</p><pre><code>'+html.escape(commands)+'</code></pre><h3>'+('ลองต่อด้วยตัวเอง' if lang=='th' else 'Your experiment')+'</h3><p>'+p['exercise'][lang]+'</p>'
            section('practice',headings[-2][1],practice)
            refs='<section class="references" aria-labelledby="sources"><h3 id="sources">'+('Primary sources และขอบเขตการตรวจ' if lang=='th' else 'Primary sources and verification scope')+'</h3>'
            refs+='<p class="references__note">'+('เอกสารผู้เขียนเป็นต้นทางของคำอธิบายและภาพที่ระบุ ส่วนลิงก์ข้างล่างเป็นเอกสารวิจัยและมาตรฐานที่ใช้ตรวจข้ออ้าง โค้ดรันซ้ำบน Python 3.13, Qiskit 2.6.2, Aer 0.18.4, NumPy 2.5.5 และ SciPy 1.18.1 วันที่ 24 November 2026 ผลทั้งหมดเป็น local simulation หรือค่าตัวอย่างที่ระบุ ไม่มีการรัน hardware' if lang=='th' else 'The author’s guide supplies the credited explanations and illustrations. Linked papers and standards support the claims. Code was rerun locally on 24 November 2026 with Python 3.13, Qiskit 2.6.2, Aer 0.18.4, NumPy 2.5.5 and SciPy 1.18.1. Results are local simulations or explicitly hypothetical inputs; no quantum hardware was used.')+'</p><ol>'
            for i,key in enumerate(p['refs'],1):
                title,url=REFS[key];refs+=f'<li id="ref-{i}"><a href="{url}">{html.escape(title)}</a></li>'
            refs+='</ol></section>'
            section('references',headings[-1][1],refs)
            (ROOT/'.bilingual'/(p['slug']+'.'+lang+'.html')).write_text('\n\n'.join(lines)+'\n')
        descriptions={
            1:'เรียน amplitude, phase และ interference ด้วย Python ทดลอง H–H เทียบกับ H–Z–H พร้อมภาพจากเอกสาร โค้ด Qiskit และ tests',
            2:'สร้าง Grover oracle และ diffuser ค้นหา 1011 ด้วยสามรอบ ตรวจผล 4,096 shots และเห็นเหตุใดจำนวน query ที่ลดลงยังไม่ใช่ runtime ที่เร็วขึ้น',
            3:'แยก classical factoring จาก quantum order finding อ่าน Fourier peaks และ continued fractions พร้อมตัวอย่าง factor 15 และข้อจำกัดของ dense gates',
            4:'รัน HHL บนระบบ 2×2 ตรวจ post-selection และ relative sign แล้วเปิดข้อจำกัดด้าน input, condition number, precision และการอ่าน solution state',
            5:'ฝึก QAOA แก้ MaxCut บน triangular prism เปรียบเทียบ expected cut กับ optimum และนับ optimizer calls โดยไม่สับสน heuristic กับ quantum advantage',
            6:'ทดลอง quantum simulation สอง qubits เปรียบเทียบ product formula กับ exact evolution วัด ZZ observable และแยก approximation error จาก hardware noise',
            7:'สรุป quantum algorithms เป็น engineering scorecard ตรวจ input/output contract, classical baseline, logical resources และต้นทุน workflow ทั้งชุด'
        }
        desc=descriptions[p['n']]
        assert 70 <= len(desc) <= 160, (p['n'],len(desc))
        posts.append({'n':p['n'],'slug':p['slug'],'chip':f'#{p["n"]} '+p['short'],'nav_title':p['short'],
                      'title':p['title'],'sub':p['sub'],'tags':['Quantum Computing','Qiskit','Algorithms'],
                      'description':desc,'read_min':7,'cover':p['slug']+'-cover.jpg','figures':figures})
    template=json.loads((ROOT/'scripts/series/ai-core-functional.json').read_text())
    template.update(series='quantum-programmers',title='Quantum Algorithms for Programmers',icon='ψ',
        aria_label='Quantum Algorithms for Programmers',section_id='series-quantum-programmers',date=DATE,
        h3='Quantum Algorithms for Programmers · 7-Part Course',hero_series='Quantum Algorithms for Programmers 2026 • Post #%d',
        footer={'th':'จากซีรีส์ Quantum Algorithms for Programmers','en':'From Quantum Algorithms for Programmers'},
        description={'th':'คอร์สเจ็ดตอนจาก amplitude สู่ Grover, Shor, HHL, QAOA และ quantum simulation พร้อมทดลองและตรวจต้นทุนจริง','en':'Seven programmer-first lessons on amplitudes, Grover, Shor, HHL, QAOA, quantum simulation and engineering evidence.'},
        covers={'eyebrow':'QUANTUM FOR PROGRAMMERS','accent':'teal','grounds':['cloud','parchment'],'motif_prefix':'qp_'},posts=posts,
        references=True,figure_prefix='quantum-',extra_css='')
    template.pop('groups',None)
    (ROOT/'scripts/series/quantum-programmers.json').write_text(json.dumps(template,ensure_ascii=False,indent=1)+'\n')
    rows=[r for r in (ROOT/'scripts/covers.tsv').read_text().splitlines() if not r.startswith('quantum-programmers-')]
    for p in PARTS:
        rows.append('\t'.join([p['slug'],p['slug']+'-cover.jpg','qp_'+str(p['n']),
                    'cloud' if p['n']%2 else 'parchment','teal',f'QUANTUM PROGRAMMING · {p["n"]:02d}/07',p['short'],p['title']['th'].split(' — ')[-1],f'part={p["n"]}']))
    (ROOT/'scripts/covers.tsv').write_text('\n'.join(rows)+'\n')
    evidence={'verified_date':DATE,'companion_url':URL,'revision':rev,'tag':'v1.0.1','tests':26,
              'files':{path.name:hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(comp.glob('*.py'))}}
    (HERE/'companion.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print('Prepared seven bilingual pairs, manifest and cover rows; companion '+rev)


if __name__=='__main__':main()
