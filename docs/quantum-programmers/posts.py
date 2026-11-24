"""Authored bilingual editorial source. HTML is rendered by the house builder.

The owner's PDF is source material, not an instruction file. New experiments
and statements distinguish mathematical guarantees, measurements and estimates.
"""

def S(key, th, en, thai, english):
    return dict(key=key, heading={'th':th,'en':en},body={'th':thai,'en':english})


PARTS = [
dict(n=1, slug='quantum-programmers-foundations', short='Amplitudes',
 title={'th':'Quantum Basics — เข้าใจ amplitude','en':'Quantum Foundations: From Bits to Amplitudes and Interference'},
 sub={'th':'เริ่มจาก Python และ linear algebra เล็กน้อย ทดลองให้เห็นว่า phase เปลี่ยนคำตอบได้อย่างไร ก่อนอ่าน Grover, Shor, HHL และ QAOA',
      'en':'Start with Python and a little linear algebra. See how phase changes an answer before learning Grover, Shor, HHL and QAOA.'},
 module='foundations', test='FoundationsTests', figures=['bloch','pattern'],
 functions=['interference','bell'],
 refs=['bit-order','qiskit','survey'],
 sections=[
 S('start','Start here — programmer ต้องเปลี่ยนมุมมองอะไร','Start here: change the programming model',
 '''<p>ซีรีส์ <strong>Quantum Algorithms for Programmers</strong> นี้พาจาก Python ไปสู่สี่อัลกอริทึมที่มักถูกอ้างว่าเร็วกว่า classical computer แล้วกลับมาถามคำถามที่วิศวกรต้องตอบให้ได้ว่า “เร็วกว่าในการทำงานเดียวกันจริงหรือไม่” บทความดัดแปลงจาก Technical Guide ฉบับ November 2026 ของผู้เขียน โดยแยกเป็นเจ็ดบทเรียนพร้อมโค้ดที่รันได้</p>
 <p>พื้นฐานที่ใช้คือ function, array, complex number และ Big-O ไม่ต้องเคยเรียน quantum mechanics เราจะใช้ <strong>Qiskit</strong> บนเครื่องตัวเอง ทุกตัวอย่างเป็น simulation ขนาดเล็ก ไม่ต้องมี cloud account ผลที่ได้พิสูจน์ความเข้าใจของอัลกอริทึม ส่วนการอ้างความได้เปรียบต้องมีการวัดอีกแบบหนึ่ง</p>
 <p>ถ้าเคยคิดว่า quantum computer คือ CPU ที่วนทุกคำตอบพร้อมกัน ให้เริ่มจากข้อจำกัดของการอ่านผล: register มี n qubits แต่ measurement หนึ่งครั้งให้ bit string เพียง n bits งานของโปรแกรมคือจัด <strong>amplitude</strong> ให้คำตอบที่ต้องการมีโอกาสปรากฏสูงขึ้น</p>''',
 '''<p>This <strong>Quantum Algorithms for Programmers</strong> series moves from Python to four famous quantum algorithms, then returns to the engineering question: faster at exactly what task? It adapts the author's November 2026 Technical Guide into seven lessons with executable code.</p>
 <p>You need functions, arrays, complex numbers and Big-O notation. No previous quantum mechanics is assumed. We use <strong>Qiskit</strong> locally, with small simulations and no cloud account. These experiments check how algorithms work; practical advantage requires a different experiment.</p>
 <p>Start with the output constraint. A register has n qubits, but one computational-basis measurement returns just an n-bit string. You cannot inspect every candidate encoded in the state. Your program must arrange <strong>amplitudes</strong> so that useful answers become likely.</p>'''),
 S('state','State — ตัวเลขที่อ่านตรง ๆ ไม่ได้','State: numbers you cannot simply print on hardware',
 '''<p>pure qubit เขียนเป็น |ψ⟩ = α|0⟩ + β|1⟩ โดย α และ β เป็น complex number และ |α|² + |β|² = 1 เมื่อวัดใน computational basis จะได้ 0 ด้วยโอกาส |α|² และ 1 ด้วยโอกาส |β|² หลังวัด state จะสอดคล้องกับผลที่อ่านได้</p>
 <!--FIGURE:bloch-->
 <p>Bloch sphere ในภาพแทน pure state ของ qubit เดียว มุม θ กำหนดสัดส่วนโอกาส ส่วน φ เป็น relative phase ที่มีผลเมื่อ state ถูกนำไป interfere กับ operation ถัดไป การมีโอกาส 50:50 จึงบอก state ทั้งหมดไม่ได้ |+⟩ และ |−⟩ ให้โอกาสเท่ากันเมื่อวัดทันที แต่ตอบสนองต่อ gate ถัดไปต่างกัน</p>
 <p>สำหรับ n qubits เราเขียน statevector ที่มี 2<sup>n</sup> amplitudes ได้บน simulator แต่ memory โตเป็น exponential ด้วย ตัวเลขที่ <code>Statevector</code> เปิดให้ดูเป็นสิทธิ์ของผู้จำลองทาง classical เครื่อง quantum จริงไม่ได้มี API สำหรับอ่าน amplitude ทุกตัวจากสำเนาเดียว</p>''',
 '''<p>A pure qubit is |ψ⟩ = α|0⟩ + β|1⟩, with complex α and β and normalization |α|² + |β|² = 1. Computational-basis measurement returns 0 with probability |α|² and 1 with probability |β|². After measurement, the state is consistent with that observed outcome.</p>
 <!--FIGURE:bloch-->
 <p>The Bloch sphere represents one pure qubit. The angle θ sets the measurement probabilities; φ describes a relative phase that matters when later operations interfere. A 50:50 distribution does not specify the state. The states |+⟩ and |−⟩ look identical if measured immediately, yet respond differently to the next gate.</p>
 <p>An n-qubit statevector has 2<sup>n</sup> amplitudes. A classical simulator can print them, at an exponentially growing memory cost. That debugging access belongs to the simulator. A quantum device does not expose every amplitude from one copy of its state.</p>'''),
 S('interference','Interference — ทดลอง H·H กับ H·Z·H','Interference: compare H–H with H–Z–H',
 '''<p><strong>Hadamard gate H</strong> เปลี่ยน |0⟩ เป็น |+⟩ = (|0⟩ + |1⟩)/√2 หากทำ H อีกครั้งจะกลับไป |0⟩ แต่ถ้าแทรก Z ก่อน H ตัวสุดท้าย Z จะกลับเครื่องหมายของ amplitude ฝั่ง |1⟩ ทำให้ผลสุดท้ายเป็น |1⟩ ทั้งสองเส้นทางยังเป็น 50:50 ก่อน H ตัวสุดท้าย</p>
 <!--CODE-->
 <p>อ่านโค้ดโดยมองว่า gate เปลี่ยน state ไม่ได้เปลี่ยน probability โดยตรง <code>qc.z(0)</code> เปลี่ยน phase แล้ว <code>qc.h(0)</code> จึงเปลี่ยน phase ให้กลายเป็นความต่างที่วัดเห็นได้ หากตัด H ตัวสุดท้ายออก เราจะมองไม่เห็นผลของ Z จาก histogram ใน basis นี้</p>
 <p>นี่คือแกนของ <strong>interference</strong>: เส้นทางที่ลงท้ายด้วย outcome เดียวกันรวมกันด้วย amplitude ก่อนยกกำลังสอง ไม่ใช่บวก probability ของทุกเส้นทางตั้งแต่ต้น จึงมีทั้ง reinforcement และ cancellation</p>''',
 '''<p>The <strong>Hadamard gate H</strong> maps |0⟩ to |+⟩ = (|0⟩ + |1⟩)/√2. A second H returns |0⟩. Insert Z before the final H and the |1⟩ amplitude changes sign; the final state becomes |1⟩ instead. Immediately before that last H, both paths still have 50:50 measurement probabilities.</p>
 <!--CODE-->
 <p>Read gates as transformations of the state rather than direct edits to probabilities. <code>qc.z(0)</code> changes phase. The final <code>qc.h(0)</code> converts that phase difference into an observable difference. Remove the final H and the histogram in this basis hides the effect of Z.</p>
 <p>This is the useful part of <strong>interference</strong>: paths ending at the same outcome combine as amplitudes before taking the squared magnitude. Adding path probabilities too early loses both reinforcement and cancellation.</p>'''),
 S('register','Registers — superposition และ entanglement','Registers: superposition and entanglement',
 '''<p><strong>Superposition</strong> หมายถึงมี amplitude ไม่เป็นศูนย์บนหลาย basis states เช่น H ทุก qubit ทำให้ทุก bit string มีโอกาสเท่ากัน แต่หากวัดทันทีจะได้เพียง random string ยังไม่มีการแก้โจทย์ใดเกิดขึ้น</p>
 <p><strong>Entanglement</strong> หมายถึง joint state แยกเป็น state ราย qubit ไม่ได้ ตัวอย่าง <code>bell()</code> ใช้ H บน qubit 0 แล้ว controlled-X ไปยัง qubit 1 ได้ (|00⟩ + |11⟩)/√2 แต่ละ qubit ดูสุ่มเมื่ออ่านเดี่ยว ๆ ขณะที่ผลทั้งคู่สัมพันธ์กันเสมอ การส่งข้อมูลเร็วกว่าแสงไม่ได้ตามมาจาก correlation นี้</p>
 <p>Qiskit เก็บ qubit 0 เป็น least significant bit ใน integer และเป็นอักษรขวาสุดของ count string ตาม mapping ที่เราใช้ เช่น <code>1011</code> คือ q3=1, q2=0, q1=1, q0=1 อย่าสลับตำแหน่งใน oracle เพราะบาง bit string เป็น palindrome จนบั๊กดูเหมือนไม่เกิด</p>''',
 '''<p><strong>Superposition</strong> means nonzero amplitude on several basis states. Applying H to every qubit makes all bitstrings equally likely, but immediate measurement merely produces a random string. Preparing many candidates is not yet solving the problem.</p>
 <p><strong>Entanglement</strong> means the joint state cannot be factored into independent qubit states. Our <code>bell()</code> function applies H on qubit 0 and a controlled-X onto qubit 1, preparing (|00⟩ + |11⟩)/√2. Each qubit looks random alone, while the joint outcomes agree. This correlation does not provide faster-than-light communication.</p>
 <p>In the integer and count-string conventions used here, Qiskit treats qubit 0 as the least significant bit and the rightmost displayed character. Thus <code>1011</code> means q3=1, q2=0, q1=1, q0=1. Test an asymmetric target: a palindrome can hide a reversed oracle.</p>'''),
 S('pattern','Algorithm map — สี่ขั้นที่ใช้ซ้ำ','Algorithm map: four stages that recur',
 '''<!--FIGURE:pattern-->
 <p>ทั้งสี่อัลกอริทึมมีรูปแบบร่วมกัน: prepare state → encode problem → interfere → measure และทำงานต่อด้วย classical code สำหรับ Grover เรากลับ phase ของคำตอบแล้วขยาย amplitude สำหรับ Shor เรา encode period แล้วให้ inverse QFT สร้าง peak สำหรับ HHL เราใช้ eigenvalue เพื่อสร้าง amplitude ใหม่ ส่วน QAOA ให้ classical optimizer ปรับมุมของ circuit ซ้ำ</p>
 <div class="table-wrapper"><table><thead><tr><th>Classical habit</th><th>Quantum programming habit</th></tr></thead><tbody><tr><td>print intermediate value</td><td>ใช้ simulator ตรวจ state หรือออกแบบ measurement เพิ่ม</td></tr><tr><td>loop มากขึ้นมักได้ข้อมูลเพิ่ม</td><td>gate เพิ่มอาจหมุน state เลยคำตอบหรือสะสม noise</td></tr><tr><td>input/output คือ array</td><td>ต้องระบุ state preparation และ observable ที่อ่าน</td></tr><tr><td>นับ runtime เฉพาะ function</td><td>รวม compilation, shots, retries และ classical work</td></tr></tbody></table></div>
 <p>บทถัดไปจะใช้ Grover ทำให้เห็นขั้น encode และ interfere แยกกันชัดเจน เราจะดู amplitude ติดลบ โอกาสที่สูงขึ้น และการรันมากเกินจนผลแย่ลง</p>''',
 '''<!--FIGURE:pattern-->
 <p>The recurring pattern is prepare → encode → interfere → measure, followed by classical work. Grover marks an answer through phase and amplifies its amplitude. Shor encodes a period and uses an inverse QFT to create peaks. HHL uses eigenvalues to reweight amplitudes. QAOA repeatedly changes circuit angles through a classical optimizer.</p>
 <div class="table-wrapper"><table><thead><tr><th>Classical habit</th><th>Quantum programming habit</th></tr></thead><tbody><tr><td>Print an intermediate value</td><td>Inspect a simulator state or design additional measurements</td></tr><tr><td>More loop iterations reveal more information</td><td>More gates may overshoot the answer or accumulate noise</td></tr><tr><td>Inputs and outputs are arrays</td><td>Specify state preparation and the observable to read</td></tr><tr><td>Time only the function</td><td>Include compilation, shots, retries and classical work</td></tr></tbody></table></div>
 <p>Next, Grover makes encoding and interference visibly separate. We will track a negative amplitude, rising success probability, and the point where running longer makes the answer worse.</p>''')],
 exercise={'th':'เปลี่ยน Z เป็น phase gate P(π/2) แล้วเปรียบเทียบ probability ก่อนและหลัง H ตัวสุดท้าย จากนั้นอธิบายว่าเหตุใด Bell distribution จึงต่างจาก qubit สองตัวที่โยนเหรียญแยกกัน',
           'en':'Replace Z with P(π/2), compare probabilities before and after the final H, and explain why the Bell distribution differs from two independent coin flips.'}),

dict(n=2,slug='quantum-programmers-grover',short='Grover Search',
 title={'th':'Grover Search — ขยาย amplitude','en':'Grover Search: Amplify the Answer and Know When to Stop'},
 sub={'th':'สร้าง phase oracle สำหรับ 1011 ตรวจ diffuser ด้วย linear algebra แล้วเปรียบเทียบจำนวน query โอกาสสำเร็จ และต้นทุนจริง',
      'en':'Build a phase oracle for 1011, check the diffuser with linear algebra, and distinguish query savings from total execution cost.'},
 module='grover_search',test='GroverTests',figures=['amplitudes','rotation','overrotation','grover-circuit','oracle-diffuser','grover-results','queries'],
 functions=['phase_oracle','diffuser'],refs=['grover','zalka','overheads','bit-order'],
 sections=[
 S('problem','Search contract — ค้นหาอะไรและนับอะไร','Search contract: define the task and the unit of cost',
 '''<p><strong>Grover’s algorithm</strong> หาคำตอบหนึ่งรายการจาก N candidates ที่ไม่มีโครงสร้างให้ใช้ โดยเรียก predicate f(x) ราว (π/4)√N ครั้ง เทียบกับ classical search ที่ใช้ Θ(N) queries นี่เป็น <strong>quadratic speedup</strong> ใน oracle model และเป็นขอบเขตที่ optimal สำหรับ unstructured search</p>
 <p>สมมติเรามี candidate 16 รายการและคำตอบคือ <code>1011</code> ตัวอย่างจะสร้าง oracle ที่รู้ marked string นี้เพื่อให้ตรวจ circuit ได้ การรู้คำตอบล่วงหน้าเป็น fixture สำหรับการสอน ในโจทย์จริงเราต้องมี reversible predicate ที่ตรวจ candidate ได้โดยไม่ต้องรู้คำตอบก่อน เช่นวงจรตรวจเงื่อนไขที่ต้องการ</p>
 <p>ผลเปรียบเทียบต้องนับงานเดียวกัน การอ่าน array ธรรมดา การค้นด้วย index และการคำนวณ reversible predicate มี cost ต่างกัน ถ้าข้อมูลมีโครงสร้างที่ classical algorithm ใช้ได้ เราต้องใช้ baseline นั้นแทนการบังคับให้ classical scan ทุกครั้ง</p>''',
 '''<p><strong>Grover's algorithm</strong> finds one marked candidate among N unstructured possibilities using roughly (π/4)√N predicate queries. A classical search needs Θ(N) queries. This is a <strong>quadratic speedup</strong> in the oracle model, and the scaling is optimal for unstructured search.</p>
 <p>Our search space has 16 items and the marked string is <code>1011</code>. The example deliberately knows this string to construct a testable oracle. That is a teaching fixture. In a real problem, you need an independently supplied reversible predicate that recognizes a valid candidate without already knowing the answer.</p>
 <p>Compare equal tasks. Scanning ordinary memory, using an index, and computing a reversible predicate have different costs. If a classical method can exploit sorting, an index or other structure, that method belongs in the baseline.</p>'''),
 S('amplitude','Flip and reflect — probability ยังไม่เปลี่ยนหลัง oracle','Flip and reflect: the oracle alone changes no probability',
 '''<p>เริ่มด้วย H บน qubit ทั้งสี่ ได้ amplitude 1/√16 = 0.25 เท่ากันทุก state <strong>Phase oracle</strong> เปลี่ยนเฉพาะ amplitude ของ |1011⟩ เป็น −0.25 ขนาดกำลังสองยังเป็น 0.0625 เหมือนเดิม ถ้าวัดตรงนี้จะยังสุ่มเท่าเดิม</p>
 <!--FIGURE:amplitudes-->
 <p>จากนั้น <strong>diffuser</strong> เปลี่ยน amplitude a<sub>x</sub> เป็น 2ā − a<sub>x</sub> โดย ā เป็นค่าเฉลี่ยหลัง oracle สำหรับรอบแรก ā = 0.21875 ทำให้ marked amplitude เป็น 0.6875 ส่วนรายการอื่นเป็น 0.1875 probability ของคำตอบจึงกลายเป็น 0.47265625</p>
 <p>การกลับเครื่องหมายเป็นการ encode ส่วน diffuser ทำให้ phase ส่งผลต่อ measurement นี่คือรูปแบบเดียวกับ H–Z–H ในตอนแรก แต่ขยายจากสอง amplitudes เป็นสิบหก amplitudes</p>''',
 '''<p>Apply H to all four qubits. Every amplitude starts at 1/√16 = 0.25. The <strong>phase oracle</strong> changes only the |1011⟩ amplitude to −0.25. Its squared magnitude remains 0.0625, so immediate measurement is still uniform.</p>
 <!--FIGURE:amplitudes-->
 <p>The <strong>diffuser</strong> replaces amplitude a<sub>x</sub> by 2ā − a<sub>x</sub>, where ā is the mean after the oracle. In the first round, ā = 0.21875. The marked amplitude becomes 0.6875, and each other amplitude becomes 0.1875. Success probability is now 0.47265625.</p>
 <p>The sign flip encodes the predicate; the diffuser makes that phase observable. This repeats the logic of H–Z–H from part 1, now across sixteen amplitudes.</p>'''),
 S('geometry','Rotation — เหตุใดเพิ่มรอบแล้วแย่ลง','Rotation: why additional rounds can hurt',
 '''<!--FIGURE:rotation-->
 <p>มอง state ในระนาบที่มีแกน “คำตอบ” และ “ผลรวม non-solutions” กำหนด θ = arcsin(1/√N) การทำ oracle และ diffuser คือ reflection สองครั้ง รวมเป็น rotation 2θ หลัง k รอบ success probability เท่ากับ sin²((2k+1)θ)</p>
 <!--FIGURE:overrotation-->
 <p>เลือกจำนวนรอบให้ (2k+1)θ ใกล้ π/2 สำหรับ N=16, θ ≈ 14.48° และ k=3 ให้โอกาส 96.13% แต่ k=5 เหลือ 12.55% อัลกอริทึมจึงต้องมี stopping rule สำหรับกรณีหนึ่งคำตอบในตัวอย่าง <code>floor((π/4)√N)</code> ให้สามรอบ หากมี M คำตอบ ให้แทน sin θ ด้วย √(M/N) และถ้าไม่ทราบ M ต้องใช้นโยบายค้นหาอีกแบบ</p>
 <p>อย่านำ histogram รอบเดียวไปใช้เลือก stopping rule บนข้อมูลทดสอบแล้วอ้างความสำเร็จบนข้อมูลเดียวกัน เรามีทฤษฎีให้กำหนดจำนวนรอบก่อนรัน และมี statevector test ตรวจสูตรอย่างอิสระ</p>''',
 '''<!--FIGURE:rotation-->
 <p>View the state in the plane spanned by the solution and the uniform combination of non-solutions. Set θ = arcsin(1/√N). The oracle and diffuser are two reflections, producing a rotation by 2θ. After k rounds, success probability is sin²((2k+1)θ).</p>
 <!--FIGURE:overrotation-->
 <p>Choose an integer k that brings (2k+1)θ close to π/2. For N=16, θ ≈ 14.48° and k=3 gives 96.13% success. At k=5 it falls to 12.55%. The one-solution rule <code>floor((π/4)√N)</code> gives three rounds here. With M solutions, sin θ becomes √(M/N); unknown M requires a different search schedule.</p>
 <p>Do not choose a stopping rule from one test histogram and report success on the same data. Here theory sets the count before execution, and independent statevector checks verify the probability formula.</p>'''),
 S('circuit','Implementation — เปิด oracle และ diffuser','Implementation: open the oracle and diffuser',
 '''<!--FIGURE:grover-circuit-->
 <!--FIGURE:oracle-diffuser-->
 <!--CODE-->
 <p><code>reversed(marked)</code> เป็นเรื่องสำคัญ เพราะ qubit 0 อยู่ทางขวาสุดของ string เราใส่ X บนตำแหน่งที่ target เป็น 0 เพื่อ map marked state ไป |1111⟩ แล้ว H–MCX–H ทำ multi-controlled Z จากนั้น undo X ให้ basis กลับตำแหน่งเดิม</p>
 <p>diffuser ใช้ H และ X ครอบ phase flip อีกชั้น วงจรนี้เท่ากับ negative ของ D = 2|s⟩⟨s| − I ซึ่งต่างกันเพียง global phase จึงวัดเหมือนกัน test ตรวจ matrix ทั้งก้อนโดยยอมรับ global phase นี้ ไม่ได้ตรวจแค่ outcome ที่โชคดีตัวเดียว</p>''',
 '''<!--FIGURE:grover-circuit-->
 <!--FIGURE:oracle-diffuser-->
 <!--CODE-->
 <p><code>reversed(marked)</code> matters because qubit 0 is the rightmost character. X gates map zero positions in the target to ones. H–MCX–H implements a multi-controlled Z, and undoing X restores the original basis labels.</p>
 <p>The diffuser wraps another phase flip in H and X layers. This circuit implements the negative of D = 2|s⟩⟨s| − I, differing only by a global phase. Measurement is unchanged. Our test checks the entire matrix with this global sign, rather than checking one fortunate sample.</p>'''),
 S('results','Measured outcome — query saving ไม่ใช่ wall-clock saving','Measured outcome: query savings versus wall-clock savings',
 '''<!--OUTPUT-->
 <!--FIGURE:grover-results-->
 <p>รันบน ideal Aer simulator 4,096 shots ได้คำตอบ 3,928 ครั้ง หรือ 95.90% เทียบกับ exact probability 96.13% ความต่างเป็น sampling noise ค่า standard error ตามทฤษฎีประมาณ 0.30 percentage points ตัวเลขนี้ไม่ใช่ hardware error rate และเวลาที่ simulator ใช้ไม่ใช่เวลา quantum computer</p>
 <!--FIGURE:queries-->
 <div class="table-wrapper"><table><thead><tr><th>N</th><th>Classical scan ≈ N/2</th><th>Grover queries ≈ π√N/4</th></tr></thead><tbody><tr><td>10³</td><td>500</td><td>24</td></tr><tr><td>10⁶</td><td>500,000</td><td>785</td></tr><tr><td>10⁹</td><td>500,000,000</td><td>24,836</td></tr></tbody></table></div>
 <p>ตัวเลข classical เป็นค่าประมาณของการไล่ตรวจตำแหน่งแบบสุ่มเท่ากัน จำนวนจริงเฉลี่ย (N+1)/2 หากนับการตรวจที่พบด้วย ส่วน Grover นับ oracle calls เท่านั้น ต้นทุนต่อ call รวม reversible computation, ancilla และ error correction ได้มาก งานของ Babbush และคณะอธิบายว่าค่า overhead ทำให้ quadratic advantage เปลี่ยนเป็นประโยชน์จริงได้ยากบนเครื่อง fault-tolerant รุ่นแรก</p>
 <blockquote><p>ผลที่บทนี้แสดงได้: circuit ขยาย probability ตามทฤษฎี ผลที่ยังสรุปไม่ได้: การค้นข้อมูลจริงเร็วกว่าระบบ classical ที่จัด index หรือทำ parallel search อย่างเหมาะสม</p></blockquote>''',
 '''<!--OUTPUT-->
 <!--FIGURE:grover-results-->
 <p>The ideal Aer run produces 3,928 hits in 4,096 shots: 95.90%, compared with exact probability 96.13%. The theoretical standard error is about 0.30 percentage points. This difference is sampling noise, not a hardware error rate. Simulator execution time is not quantum-device runtime.</p>
 <!--FIGURE:queries-->
 <div class="table-wrapper"><table><thead><tr><th>N</th><th>Classical scan ≈ N/2</th><th>Grover queries ≈ π√N/4</th></tr></thead><tbody><tr><td>10³</td><td>500</td><td>24</td></tr><tr><td>10⁶</td><td>500,000</td><td>785</td></tr><tr><td>10⁹</td><td>500,000,000</td><td>24,836</td></tr></tbody></table></div>
 <p>The classical column approximates a uniformly located target in a sequential scan; the exact mean including the successful query is (N+1)/2. The quantum column counts only oracle calls. Each call can require substantial reversible computation, ancillas and error correction. Babbush and colleagues analyze why these overheads can make quadratic advantage difficult on early fault-tolerant devices.</p>
 <blockquote><p>Established here: the circuit amplifies probability as predicted. Unestablished: faster real-world search than a suitably indexed or parallel classical system.</p></blockquote>''')],
 exercise={'th':'เปลี่ยน target เป็น 0010 และเปรียบเทียบ k=0, 1, 3, 5 ตรวจว่า oracle กลับ phase ของ state ที่ถูกต้อง แล้วอธิบายต้นทุนที่ query table ยังไม่นับ',
 'en':'Change the target to 0010, compare k=0,1,3,5, verify the phase flip lands on the correct basis state, and list the costs omitted by the query table.'}),

dict(n=3,slug='quantum-programmers-shor',short='Shor & Periods',
 title={'th':'Shor — จาก period สู่ตัวประกอบ','en':'Shor’s Algorithm: From Periods to Factors with the QFT'},
 sub={'th':'แยก classical number theory ออกจาก quantum period finding ทำความเข้าใจ Fourier peaks และตรวจว่าตัวอย่าง factor 15 บอกอะไรได้จริง',
 'en':'Separate classical number theory from quantum period finding, interpret Fourier peaks, and understand what factoring 15 actually demonstrates.'},
 module='shor_factor15',test='ShorTests',figures=['shor-flow','period','qft','shor-circuit','shor-results'],functions=['period_finding_circuit','factors_from_measurement'],refs=['shor','arithmetic','gidney','nist'],
 sections=[
 S('problem','The reduction — factoring ไม่ได้กลายเป็น search','The reduction: factoring becomes order finding',
 '''<p><strong>Shor’s algorithm</strong> factor integer N ด้วยจำนวน operation ที่เป็น polynomial ในจำนวน bits n = ⌈log₂N⌉ ขณะที่ general number field sieve ซึ่งเป็น classical baseline สำคัญมี asymptotic cost แบบ sub-exponential นี่จึงเป็น superpolynomial improvement เทียบกับวิธีที่รู้จัก ไม่ใช่ Grover ที่เอา square root มาครอบ brute force</p>
 <p>เลือก base a ที่ 1 &lt; a &lt; N ก่อน ถ้า gcd(a,N) &gt; 1 ก็พบตัวประกอบโดยไม่ต้องใช้ quantum step ถ้า gcd=1 ให้หา <strong>order r</strong> ซึ่งเป็นจำนวนบวกน้อยที่สุดที่ a<sup>r</sup> mod N = 1 หาก r เป็นเลขคู่และ a<sup>r/2</sup> mod N ไม่เท่ากับ −1 จะใช้ gcd(a<sup>r/2</sup> ± 1,N) เพื่อหา nontrivial factors แล้วตรวจผล</p>
 <!--FIGURE:shor-flow-->
 <p>classical code ทำทั้งการเลือก base, modular arithmetic, continued fractions และการตรวจตัวประกอบ quantum subroutine รับผิดชอบการหา order เส้นแบ่งนี้ช่วยให้เราเขียน test แยก classical recovery จาก quantum distribution ได้</p>''',
 '''<p><strong>Shor's algorithm</strong> factors an integer N with work polynomial in its bit length n = ⌈log₂N⌉. The general number field sieve, an important classical baseline, has sub-exponential asymptotic cost. The improvement is superpolynomial relative to known classical methods; it does not come from taking a square root of brute force.</p>
 <p>Choose 1 &lt; a &lt; N. If gcd(a,N) &gt; 1, a factor is already available classically. Otherwise find the <strong>order r</strong>, the smallest positive integer with a<sup>r</sup> mod N = 1. If r is even and a<sup>r/2</sup> is not −1 modulo N, compute gcd(a<sup>r/2</sup> ± 1,N), then validate the factors.</p>
 <!--FIGURE:shor-flow-->
 <p>Base selection, modular arithmetic, continued fractions and factor verification remain classical. The quantum subroutine supplies order information. This boundary lets us test classical recovery separately from the quantum distribution.</p>'''),
 S('period','Worked example — 7ˣ mod 15','Worked example: the period of 7ˣ mod 15',
 '''<!--FIGURE:period-->
 <p>สำหรับ N=15 และ a=7 ลำดับเป็น 1, 7, 4, 13, 1, 7, 4, 13, … จึงมี r=4 แล้ว 7² mod 15 = 4 ทำให้ gcd(4−1,15)=3 และ gcd(4+1,15)=5 เราเห็น period ได้ด้วยตาเพราะโจทย์เล็ก แต่สำหรับ N ที่มีหลายพัน bits การประเมินทุกตำแหน่งไม่ใช่วิธีที่มีประสิทธิภาพ</p>
 <p>counting register t qubits เริ่มด้วย equal superposition ของ x=0…2<sup>t</sup>−1 ส่วน work register เริ่มที่ |1⟩ controlled modular multiplication แต่ละตัวคำนวณ a<sup>2ʲ</sup> mod N เข้ากับ work register จึงได้ joint state ที่ผูก x กับ a<sup>x</sup> mod N โดยไม่ต้องอ่านค่าทุก x</p>
 <p>ไม่จำเป็นต้องวัด work register ก่อน ข้อมูล period อยู่ใน correlation ระหว่างสอง registers การนำ inverse QFT ไปใช้กับ counting register แล้ววัดจะสร้าง distribution ที่มี peak ใกล้ y/2<sup>t</sup> ≈ s/r</p>''',
 '''<!--FIGURE:period-->
 <p>For N=15 and a=7, the sequence is 1,7,4,13,1,7,4,13,…, giving r=4. Since 7² mod 15 = 4, gcd(4−1,15)=3 and gcd(4+1,15)=5. The period is obvious at this size; evaluating the entire sequence is not efficient when N has thousands of bits.</p>
 <p>The t-qubit counting register starts uniformly over x=0…2<sup>t</sup>−1, while the work register starts at |1⟩. Controlled modular multiplications by a<sup>2ʲ</sup> mod N build the joint state associating x with a<sup>x</sup> mod N. The program never reads every value of x.</p>
 <p>Measuring the work register first is optional. Period information is present in the correlation between registers. Applying the inverse QFT to the counting register creates peaks near y/2<sup>t</sup> ≈ s/r.</p>'''),
 S('fourier','QFT — เปลี่ยน period เป็น peak','QFT: turn periodic structure into measurable peaks',
 '''<!--FIGURE:qft-->
 <p><strong>Quantum Fourier transform</strong> เป็น DFT บน amplitudes ของ register วงจร textbook บน t qubits ใช้ gate ระดับ O(t²) และ final swaps จัด bit order การเปรียบเทียบกับ FFT ของ array ยาว 2<sup>t</sup> ต้องระวัง เพราะ QFT ให้ quantum state ไม่ได้ส่ง transformed array ทุกตัวออกมา</p>
 <p>ในตัวอย่างใช้ t=8 จึงมี 256 counting values และ r=4 หาร 256 ลงตัว peak จึงอยู่ตรง 0,64,128,192 แทน phase 0,1/4,1/2,3/4 โดยไม่มี rounding error ของ phase ในกรณีทั่วไป peak ไม่จำเป็นต้องตรง bin พอดี ต้องมี precision พอและทำ classical recovery อย่างรอบคอบ</p>
 <p>test ของ companion สร้าง matrix ของ inverse QFT สี่ qubits แล้วเทียบกับ inverse DFT 16×16 โดยตรง เพื่อจับลำดับ gate, เครื่องหมาย phase และ swap ที่กลับผิด ก่อนใช้มันใน Shor หรือ HHL</p>''',
 '''<!--FIGURE:qft-->
 <p>The <strong>quantum Fourier transform</strong> is a DFT on a register's amplitudes. A textbook t-qubit circuit uses O(t²) gates, with final swaps arranging bit order. Comparing it with an FFT over 2<sup>t</sup> classical numbers requires care: the QFT returns a quantum state, not an array of all transformed coefficients.</p>
 <p>Here t=8 gives 256 counting values. Since r=4 divides 256 exactly, peaks land at 0,64,128,192, corresponding to phases 0,1/4,1/2,3/4. There is no phase-rounding error in this example. General orders need sufficient precision and careful classical recovery.</p>
 <p>The companion tests the four-qubit inverse-QFT matrix directly against the 16×16 inverse DFT. That catches gate ordering, phase signs and swaps before reusing this subroutine in Shor or HHL.</p>'''),
 S('implementation','Implementation — recovery ต้องยอมรับ retry','Implementation: recovery must permit a retry',
 '''<!--FIGURE:shor-circuit-->
 <!--CODE-->
 <p><code>Fraction(measured, 256)</code> เก็บสัดส่วนอย่าง exact ก่อนจำกัด denominator ถ้าวัด y=64 จะได้ 1/4 จึงเสนอ r=4 แต่ y=128 ให้ 1/2 ซึ่งมี denominator 2 แม้ true order เป็น 4 ตัวตรวจ <code>pow(A, r, N) == 1</code> จึงจำเป็น ไม่ควรถือว่า denominator ทุกครั้งเป็น period</p>
 <p>ในโปรแกรมนี้ failed sample ทำให้ retry ได้ การรวม denominator หลายครั้งด้วย LCM เป็นการพัฒนาต่อที่เป็นไปได้ หลังได้ตัวประกอบต้องตรวจว่าแต่ละตัวไม่ใช่ 1 หรือ N และคูณกันกลับเป็น N จริง</p>
 <p>modular multiplier ใน companion เป็น dense 16×16 permutation matrix โดย map y&lt;15 ไป a·y mod15 และปล่อย y=15 ไว้เดิม เพื่อให้ unitary ครบ register วิธีนี้ใช้ได้เพราะ a เป็น coprime กับ 15 แต่ขยาย N แล้ว matrix จะโตแบบ exponential การ factor ขนาดจริงต้องใช้ reversible arithmetic circuits</p>''',
 '''<!--FIGURE:shor-circuit-->
 <!--CODE-->
 <p><code>Fraction(measured, 256)</code> preserves the exact rational before limiting its denominator. At y=64, phase 1/4 suggests r=4. At y=128, phase 1/2 reduces to denominator 2 even though the true order is 4. The check <code>pow(A, r, N) == 1</code> prevents treating every denominator as the order.</p>
 <p>This program permits a failed sample to trigger a retry. Combining denominators from several samples using an LCM is a possible extension. Accepted factors must each be nontrivial and multiply back to N.</p>
 <p>The companion uses a dense 16×16 permutation matrix: y&lt;15 maps to a·y mod15, and y=15 stays fixed. Coprimality makes this reversible. Increasing N makes such a matrix exponentially large in register width. Scalable factoring requires reversible arithmetic circuits instead.</p>'''),
 S('outcomes','Evidence — factor 15 และความเสี่ยงด้าน cryptography','Evidence: factoring 15 and the cryptography implication',
 '''<!--OUTPUT-->
 <!--FIGURE:shor-results-->
 <p>ผลรัน 2,048 shots ได้ four peaks ตามทฤษฎี โดย 1,049 shots จาก phase 1/4 และ 3/4 พาไปถึง factors ทันที สัดส่วนประมาณครึ่งหนึ่งที่ต้อง retry เป็นพฤติกรรมที่คาดไว้ ไม่ใช่บั๊ก การแสดง r=4 ในโจทย์เล็กยังไม่ใช่หลักฐานว่า hardware factor RSA-2048 ได้</p>
 <p>ผลของ Shor ยังครอบคลุม discrete logarithm จึงเกี่ยวกับ RSA และ elliptic-curve public-key systems งานประมาณ resource ของ Gidney (2025) ระบุ scenario ที่ใช้ noisy physical qubits ต่ำกว่าหนึ่งล้านและเวลาต่ำกว่าหนึ่งสัปดาห์สำหรับ RSA-2048 ภายใต้สมมติฐาน error rate, connectivity และ cycle time ที่ระบุ นี่เป็น estimate ของระบบที่ต้องสร้าง ไม่ใช่ผลรันจริงหรือวันที่ทำนายการโจมตีได้</p>
 <p>งานที่ software team เริ่มได้คือทำ inventory ของ public-key cryptography และวางแผน crypto-agility NIST มีมาตรฐาน ML-KEM สำหรับ key establishment และ ML-DSA / SLH-DSA สำหรับ signatures แล้ว การเลือก library, protocol และ migration ต้องอิงมาตรฐานและบริบทระบบ ส่วน blog นี้สอน algorithm และแยก evidence แต่ละระดับให้ชัด</p>''',
 '''<!--OUTPUT-->
 <!--FIGURE:shor-results-->
 <p>The 2,048-shot run produces the predicted four peaks. Phases 1/4 and 3/4 yield factors directly in 1,049 shots. Requiring a retry roughly half the time is expected here. Demonstrating r=4 in a small simulation does not show that hardware can factor RSA-2048.</p>
 <p>Shor also applies to discrete logarithms, creating a threat to RSA and elliptic-curve public-key systems. Gidney's 2025 resource estimate describes a scenario below one million noisy physical qubits and below one week for RSA-2048, under stated error, connectivity and timing assumptions. It is a system estimate, not an executed attack or a prediction of its arrival date.</p>
 <p>Software teams can inventory public-key cryptography and plan crypto-agility. NIST has standardized ML-KEM for key establishment and ML-DSA and SLH-DSA for signatures. Library, protocol and migration decisions belong in a standards-based system plan. This lesson establishes the algorithm and keeps the evidence levels distinct.</p>''')],
 exercise={'th':'อธิบายว่าเหตุใด y=128 ไม่ให้ r=4 โดยตรง แล้วเพิ่มวิธีรวม denominator หลาย sample พร้อม test ว่า factor ที่รับต้องคูณกลับเป็น 15 อย่าเปลี่ยน N โดยถือว่า dense matrix นี้ scalable',
 'en':'Explain why y=128 does not directly recover r=4. Add a multi-sample denominator strategy and verify accepted factors multiply to 15. Do not treat a larger dense matrix as scalable arithmetic.'}),

dict(n=4,slug='quantum-programmers-hhl',short='HHL & Readout',
 title={'th':'HHL — คำตอบเป็น quantum state','en':'HHL Linear Systems: A Solution State Is Not a Solution Array'},
 sub={'th':'แก้ระบบ 2×2 ที่ตรวจด้วยมือได้ ติดตาม post-selection และ relative sign แล้วเปิดต้นทุน input, condition number และ readout',
 'en':'Solve a hand-checkable 2×2 system, track post-selection and relative signs, and expose the input, conditioning and readout costs.'},
 module='hhl_2x2',test='HHLTests',figures=['hhl-flow','hhl-circuit','hhl-results'],functions=['hhl_circuit','exact_result'],refs=['hhl','fineprint','precision','tang'],
 sections=[
 S('contract','Output contract — |x⟩ ต่างจาก x','Output contract: |x⟩ differs from x',
 '''<p><strong>HHL</strong> เตรียม quantum state ที่ amplitudes เป็นสัดส่วนกับคำตอบของ Ax=b กล่าวคือ |x⟩ = A⁻¹|b⟩ / ‖A⁻¹|b⟩‖ ผลลัพธ์จึงเป็น normalized state ไม่ใช่ array ที่เทียบแทน <code>numpy.linalg.solve</code> ได้ทันที หากโจทย์ต้องใช้ทุก x<sub>i</sub> ต้องนับต้นทุนอ่านผลเพิ่ม</p>
 <p>ความน่าสนใจของ quantum linear-systems algorithms อยู่ที่ dependence ต่อ dimension N ซึ่งอาจเป็น polylogarithmic ภายใต้ efficient access, sparsity หรือโครงสร้างที่เหมาะสม และ condition number ที่ควบคุมได้ สูตร original HHL มี dependence ต่อ sparsity s, condition number κ และ precision ε ที่สำคัญมาก การอ่านเฉพาะ log N ทำให้เข้าใจ promise ผิด</p>
 <p>สำหรับบทนี้เราจะยังไม่อ้าง advantage ใช้ matrix เล็กที่ classical solve ตรวจได้ตรง ๆ เพื่อมองเห็น data contract ของ HHL ทั้งการเตรียม |b⟩ การจัดการ eigenvalues และความต่างระหว่าง amplitude กับ probability</p>''',
 '''<p><strong>HHL</strong> prepares a quantum state with amplitudes proportional to the solution of Ax=b: |x⟩ = A⁻¹|b⟩ / ‖A⁻¹|b⟩‖. It returns a normalized state, not an array interchangeable with <code>numpy.linalg.solve</code>. If every x<sub>i</sub> is required, include the cost of recovering those entries.</p>
 <p>Quantum linear-systems algorithms can have polylogarithmic dependence on dimension N under suitable access and structural assumptions. Sparsity s, condition number κ and precision ε also affect runtime. Reading only the log N term hides much of the contract.</p>
 <p>We make no advantage claim for this lesson. A tiny matrix lets classical arithmetic verify the entire example while exposing state preparation, eigenvalue processing, and the distinction between amplitudes and probabilities.</p>'''),
 S('math','Worked example — คำตอบมีเครื่องหมายลบ','Worked example: keep track of the negative entry',
 '''<p>เลือก A = [[1.5, 0.5], [0.5, 1.5]] และ b = [1,0] จะได้ x = [0.75,−0.25] มี eigenvalues 1 และ 2 จึงมี κ=2 ส่วน normalized solution เป็น [3/√10,−1/√10] และ probability ของสอง outcomes เป็น [0.9,0.1]</p>
 <p>ใน eigenbasis ของ A การกลับ matrix คือการเปลี่ยน coefficient β<sub>j</sub> เป็น β<sub>j</sub>/λ<sub>j</sub> เราใช้ <strong>phase estimation</strong> เพื่อเขียน eigenvalue ลง clock register แล้ว controlled rotation บน ancilla ทำให้ amplitude ฝั่ง ancilla=1 เป็น C/λ<sub>j</sub> เมื่อ uncompute clock และเลือกเฉพาะ ancilla=1 จะเหลือ solution state</p>
 <!--FIGURE:hhl-flow-->
 <p>เลือก evolution time t=π/2 ทำให้ eigenvalue 1 และ 2 มี phase 1/4 กับ 1/2 พอดีใน clock สอง qubits ไม่เกิด finite-precision error ในตัวอย่างนี้ เมื่อ C=1 โอกาสผ่าน post-selection คือ ½·1² + ½·(½)² = 0.625 การสุ่มที่ไม่ผ่านเป็นส่วนหนึ่งของต้นทุน</p>''',
 '''<p>Choose A = [[1.5,0.5],[0.5,1.5]] and b = [1,0]. The classical solution is x = [0.75,−0.25]. Eigenvalues are 1 and 2, giving κ=2. The normalized solution is [3/√10,−1/√10], so measurement probabilities are [0.9,0.1].</p>
 <p>In A's eigenbasis, inversion replaces coefficient β<sub>j</sub> with β<sub>j</sub>/λ<sub>j</sub>. <strong>Phase estimation</strong> writes eigenvalue information to a clock. A controlled ancilla rotation places amplitude C/λ<sub>j</sub> on ancilla=1. Uncompute the clock and post-select that ancilla outcome to retain the solution state.</p>
 <!--FIGURE:hhl-flow-->
 <p>Evolution time t=π/2 maps eigenvalues 1 and 2 to phases 1/4 and 1/2, exactly representable by two clock qubits. With C=1, post-selection succeeds with probability ½·1² + ½·(½)² = 0.625. Rejected attempts belong in the cost ledger.</p>'''),
 S('code','Implementation — circuit นี้ผูกกับ spectrum','Implementation: this circuit is tied to its spectrum',
 '''<!--FIGURE:hhl-circuit-->
 <!--CODE-->
 <p>clock 01 หมายถึง λ=1 และ clock 10 หมายถึง λ=2 จึงใช้ rotation π กับ π/3 จากสูตร 2·arcsin(C/λ) ได้ตรง ๆ ตัวควบคุมทีละ clock bit ใช้ได้เพราะมีเฉพาะสอง clock states นี้ ถ้าเปลี่ยน A ให้มี phase 11 หรือ phase ไม่ลง bin การใส่ rotation เดิมจะไม่ใช่ reciprocal lookup ที่ถูกต้องอีกต่อไป</p>
 <p>โค้ด helper สร้าง exp(iAt) ด้วย dense <code>scipy.linalg.expm</code> เพื่อสาธิต matrix 2×2 เท่านั้น การสร้าง unitary ของ matrix ใหญ่แบบนี้ไม่ใช่ efficient Hamiltonian simulation ใน HHL theorem ต้องมีวิธีเข้าถึง A และ implement evolution อย่างเหมาะสม</p>
 <p>ใน <code>exact_result()</code> qubit ordering คือ x,clock1,clock0,anc จากซ้ายไปขวา เราจึงเลือก indices 1 และ 9 ซึ่งเป็น clock=00 และ anc=1 แล้ว normalize ด้วยโอกาสผ่านทั้งหมด test อีกตัวตรวจว่า clock กลับเป็น 00 จริงหลัง uncomputation</p>''',
 '''<!--FIGURE:hhl-circuit-->
 <!--CODE-->
 <p>Clock 01 encodes λ=1 and clock 10 encodes λ=2. The rotation rule 2·arcsin(C/λ) gives π and π/3. Controlling each clock bit separately is valid because only these two exact states occur. Changing A to produce clock 11 or off-grid phases invalidates this simple reciprocal lookup.</p>
 <p>The helper constructs exp(iAt) using dense <code>scipy.linalg.expm</code> for a 2×2 demonstration. Building a large dense unitary this way is not the efficient Hamiltonian access required by the theorem.</p>
 <p>In <code>exact_result()</code>, displayed state order is x,clock1,clock0,anc. Indices 1 and 9 have clock=00 and anc=1. We normalize those amplitudes using the total acceptance probability. A separate test confirms that uncomputation actually resets the clock.</p>'''),
 S('measurement','Readout — probability ตรงยังไม่พอ','Readout: matching probabilities is insufficient',
 '''<!--OUTPUT-->
 <!--FIGURE:hhl-results-->
 <p>ผล exact ตรง [0.9,0.1] และ shots ที่ผ่าน 12,597 จาก 20,000 ให้ [0.8997,0.1003] แต่ histogram นี้ไม่แสดงเครื่องหมายลบใน x<sub>1</sub> state [3/√10,+1/√10] จะให้ histogram เดียวกัน จึงต้องตรวจ state รวม relative phase ด้วย</p>
 <p>tests ใช้ solution จาก <code>np.linalg.solve</code> เป็น reference แล้วเทียบ conditional statevector โดยยอมให้ต่าง global phase ได้ แต่ไม่ยอมให้ relative sign เปลี่ยน หากอยู่บน hardware ต้องออกแบบ measurement ใน basis อื่น เช่นหา expectation ของ X เพื่อแยก relative sign ของตัวอย่าง real-valued นี้</p>
 <p>HHL ตัด norm ของ x ออกด้วย normalization และการอ่านทุกองค์ประกอบของ vector ขนาด N ที่ precision กำหนดต้องใช้หลายสำเนาของ state ความหวังจึงอยู่กับ observable หรือคุณสมบัติสรุปที่วัดได้ด้วย budget ที่เหมาะสม ไม่ใช่การอ่าน array ใหญ่ทั้งหมดฟรี</p>''',
 '''<!--OUTPUT-->
 <!--FIGURE:hhl-results-->
 <p>The exact probabilities match [0.9,0.1]. Of 20,000 shots, 12,597 pass selection and give [0.8997,0.1003]. Yet the histogram hides the negative sign of x<sub>1</sub>. The state [3/√10,+1/√10] would produce the same histogram.</p>
 <p>Our tests compare the conditional statevector with the normalized <code>np.linalg.solve</code> reference, allowing a global phase but preserving relative sign. On hardware, additional measurement bases are needed. For this real-valued example, an X expectation can distinguish the relative sign.</p>
 <p>Normalization also removes the scale of x. Recovering every entry of a large vector to specified precision requires many state copies. The useful output contract is often an observable or aggregate property with a manageable estimation budget, not free access to a large array.</p>'''),
 S('fineprint','Fine print — ตรวจสามขอบเขตก่อนพูดว่า exponential','Fine print: inspect the boundaries before claiming exponential gain',
 '''<div class="table-wrapper"><table><thead><tr><th>Boundary</th><th>Engineering question</th></tr></thead><tbody><tr><td>Input</td><td>เตรียม |b⟩ จาก compact recipe ได้หรือจำเป็นต้องโหลด N ค่า</td></tr><tr><td>Matrix access</td><td>A มี sparsity หรือโครงสร้างที่ทำ evolution ได้มีประสิทธิภาพหรือไม่</td></tr><tr><td>Conditioning</td><td>κ โตอย่างไรเมื่อขนาดระบบเพิ่ม และ precision ที่ต้องการคือเท่าไร</td></tr><tr><td>Output</td><td>ต้องการ observable กี่ตัว หรือ solution vector ทุกค่า</td></tr><tr><td>Classical baseline</td><td>ใช้ sparse solver, preconditioning หรือ sampling algorithm ที่ดีแล้วหรือยัง</td></tr></tbody></table></div>
 <p>บทความ “Read the fine print” ของ Aaronson ชี้ให้เห็นต้นทุนเหล่านี้ ขณะที่งาน quantum-inspired algorithms เช่นของ Tang แสดงว่าบาง data-access assumptions เปิดโอกาสให้ classical algorithm แข็งแรงขึ้นด้วย การเปรียบเทียบต้องให้ทั้งสองฝ่ายเข้าถึง input ภายใต้เงื่อนไขที่เทียบกันได้</p>
 <p>ข้อสรุปของตัวอย่างคือเราเตรียม normalized solution state ได้ถูกต้องสำหรับ spectrum ที่ออกแบบไว้ ยังไม่มี end-to-end speedup ในการแก้ linear system บนเครื่องของเรา ขั้นต่อไปคือ QAOA ซึ่งมี quantum circuit อยู่ใน optimization loop แทนการคำนวณคำตอบด้วยสูตรสำเร็จ</p>''',
 '''<div class="table-wrapper"><table><thead><tr><th>Boundary</th><th>Engineering question</th></tr></thead><tbody><tr><td>Input</td><td>Can |b⟩ be prepared from a compact recipe, or must N entries be loaded?</td></tr><tr><td>Matrix access</td><td>Does A permit efficient evolution through sparsity or other structure?</td></tr><tr><td>Conditioning</td><td>How does κ grow with size, and what precision is required?</td></tr><tr><td>Output</td><td>Are a few observables sufficient, or is the full vector required?</td></tr><tr><td>Classical baseline</td><td>Have sparse solvers, preconditioning and sampling methods been considered?</td></tr></tbody></table></div>
 <p>Aaronson's “Read the fine print” explains these boundary costs. Quantum-inspired work such as Tang's also shows how some data-access assumptions can strengthen classical algorithms. Both sides need comparable input access.</p>
 <p>This experiment correctly prepares a normalized solution state for its engineered spectrum. It establishes no end-to-end linear-solving speedup. Next comes QAOA, where a parameterized quantum circuit sits inside a classical optimization loop.</p>''')],
 exercise={'th':'คำนวณ ⟨X⟩ ของ normalized solution แล้วเปรียบเทียบกับ state ที่เปลี่ยน −0.25 เป็น +0.25 อธิบายว่าทำไม histogram ใน Z basis เหมือนกันแต่ state ไม่เหมือนกัน อย่าเปลี่ยน A โดยคง reciprocal rotation เดิม',
 'en':'Compute ⟨X⟩ for the normalized solution and for the state with −0.25 changed to +0.25. Explain why their Z-basis histograms agree while their states differ. Do not change A without redesigning reciprocal rotations.'}),

dict(n=5,slug='quantum-programmers-qaoa',short='QAOA & MaxCut',
 title={'th':'QAOA — ฝึก circuit แก้ MaxCut','en':'QAOA Optimization: Train a Circuit and Keep the Classical Baseline'},
 sub={'th':'แก้ MaxCut บน triangular prism ทำความเข้าใจ cost/mixer layers และแยก expected cut, best sample, guarantee และ quantum advantage',
 'en':'Solve MaxCut on a triangular prism, understand cost and mixer layers, and separate expectation, best samples, guarantees and advantage.'},
 module='qaoa_maxcut',test='QAOATests',figures=['qaoa-flow','qaoa-circuit','qaoa-results'],functions=['cut_value','qaoa_circuit','expected_cut','optimize'],refs=['qaoa','gw','obstacles','plateaus'],
 sections=[
 S('problem','MaxCut — กำหนด baseline ก่อนฝึก','MaxCut: establish the baseline before training',
 '''<p><strong>QAOA</strong> เป็น variational algorithm ที่ให้ classical optimizer เลือกมุมของ quantum circuit เพื่อให้ sampling distribution มีคำตอบคุณภาพดีขึ้น ตัวอย่างนี้ใช้ <strong>MaxCut</strong>: แบ่ง vertices เป็นสองกลุ่มให้มี edges ข้ามกลุ่มมากที่สุด</p>
 <p>graph เป็น triangular prism มีสอง triangles และสาม rungs รวม 6 vertices กับ 9 edges แต่ละ triangle ต้องมีอย่างน้อยหนึ่ง edge ที่ไม่ถูก cut จึงมี upper bound เท่ากับ 7 เรา enumerate bitstrings ทั้ง 64 แบบแล้วพบว่ามี 6 แบบที่ให้ cut=7 และ random assignment มี expected cut=4.5</p>
 <p>การ enumerate นี้มีไว้ตรวจคำตอบ ไม่ได้ทำให้ QAOA มี advantage เพราะ classical computer แก้โจทย์เล็กนี้ได้ทันที เมื่อเปรียบเทียบคุณภาพต้องแยก random baseline ซึ่งใช้สอนการเปลี่ยน distribution ออกจาก strong classical solver ซึ่งใช้พิสูจน์ประโยชน์จริง</p>''',
 '''<p><strong>QAOA</strong> is a variational algorithm: a classical optimizer chooses quantum-circuit angles to improve the quality of sampled answers. Our task is <strong>MaxCut</strong>, partitioning vertices into two groups to maximize the number of edges crossing between them.</p>
 <p>The triangular prism has two triangles, three rungs, six vertices and nine edges. Each triangle must leave at least one edge uncut, so the optimum is at most seven. Enumerating all 64 bitstrings confirms six optimal strings with cut=7. Random assignment has expected cut 4.5.</p>
 <p>Enumeration supplies a verification reference; it also solves this tiny instance immediately. A random baseline helps explain distribution shaping. A strong classical solver is needed to evaluate practical usefulness.</p>'''),
 S('hamiltonian','Encoding — bit string กลายเป็น energy','Encoding: a cut becomes an energy',
 '''<p>ให้ z<sub>i</sub> เป็น +1 หรือ −1 ตามด้านของ partition edge (i,j) ถูก cut เมื่อ z<sub>i</sub> ≠ z<sub>j</sub> จึงเขียน C(z) = Σ<sub>(i,j)∈E</sub>(1−z<sub>i</sub>z<sub>j</sub>)/2 ได้ เมื่อแทน z ด้วย Pauli Z จะได้ diagonal cost operator ซึ่งให้ eigenvalue เป็น cut value ของ bit string</p>
 <p>เริ่มจาก |+⟩ ทุก qubit แล้วสลับ <strong>cost layer</strong> กับ <strong>mixer layer</strong> เป็นจำนวน p รอบ cost layer ใส่ phase ตาม cut ส่วน mixer ที่ประกอบด้วย X rotations ทำให้ amplitudes ของ bitstrings interfere เป้าหมายของ optimizer คือ maximize ⟨C⟩ ไม่ใช่อ่าน eigenvalue ทุกตัว</p>
 <!--FIGURE:qaoa-flow-->
 <p>ในโค้ด <code>rzz(2*gamma)</code> ทำ exp(−iγZ<sub>i</sub>Z<sub>j</sub>) ซึ่งเท่ากับ cost convention exp(−iγ<sub>C</sub>C) เมื่อ γ<sub>C</sub>=−2γ โดยละ global phase การอ่านสูตรจากอีก library จึงต้องตรวจ sign และ factor 2 ก่อนย้าย parameter</p>''',
 '''<p>Let z<sub>i</sub> be +1 or −1 for the two partition sides. Edge (i,j) is cut when z<sub>i</sub> ≠ z<sub>j</sub>, giving C(z) = Σ<sub>(i,j)∈E</sub>(1−z<sub>i</sub>z<sub>j</sub>)/2. Replacing spins with Pauli Z operators produces a diagonal cost operator whose eigenvalue is the bitstring's cut value.</p>
 <p>Start every qubit in |+⟩, then alternate a <strong>cost layer</strong> and a <strong>mixer layer</strong> p times. The cost layer adds cut-dependent phase. X rotations in the mixer turn those phases into interference. The optimizer maximizes ⟨C⟩ without reading every eigenvalue.</p>
 <!--FIGURE:qaoa-flow-->
 <p>Our <code>rzz(2*gamma)</code> implements exp(−iγZ<sub>i</sub>Z<sub>j</sub>). This matches the convention exp(−iγ<sub>C</sub>C) when γ<sub>C</sub>=−2γ, up to global phase. Check signs and factors of two before transferring parameters between implementations.</p>'''),
 S('code','Hybrid loop — งานอยู่ทั้งสองฝั่ง','Hybrid loop: account for both sides',
 '''<!--FIGURE:qaoa-circuit-->
 <!--CODE-->
 <p><code>expected_cut()</code> อ่าน exact probabilities จาก statevector แล้ว dot กับ cut values ที่ classical code เตรียมไว้ นี่เป็น objective สำหรับการสอนบน simulator บน hardware ไม่มี probability vector ทั้งก้อน ต้องประเมิน ⟨C⟩ จาก shots พร้อม uncertainty และ optimizer อาจเดินต่างไป</p>
 <p>ใช้ COBYLA และ random restarts 20 ครั้งต่อ depth เพราะ landscape มีหลายจุดสูงต่ำ seed=0 ตรึงจุดเริ่มต้น โค้ดนับ objective evaluations ของทุก restart รวมกัน จึงไม่ซ่อนงานฝึกที่ถูกทิ้งระหว่างเลือก best run</p>
 <p>p=3 มี parameters หกตัว แต่ละ objective call ต้องเตรียม state ใหม่ ในรันนี้สาม depths ใช้ 762, 3,137 และ 9,157 calls ตามลำดับ หากเปลี่ยนเป็น hardware และใช้ 1,000 shots ต่อ call ต้องเพิ่มงบหลายล้าน circuit executions ก่อน final sampling อีก 4,096 shots</p>''',
 '''<!--FIGURE:qaoa-circuit-->
 <!--CODE-->
 <p><code>expected_cut()</code> reads exact statevector probabilities and takes their dot product with classically computed cut values. This is a simulator teaching objective. Hardware does not expose the full probability vector; it needs shot-based estimates with uncertainty, potentially changing the optimization trajectory.</p>
 <p>We use COBYLA and twenty random restarts per depth because the landscape has multiple peaks and valleys. Seed 0 fixes starting points. Objective-call totals include every restart, including runs discarded when selecting the best result.</p>
 <p>At p=3 there are six parameters, but every objective evaluation prepares a new state. The three depths use 762, 3,137 and 9,157 calls in this run. A hypothetical hardware conversion with 1,000 shots per call would require millions of executions before the final 4,096-shot sample.</p>'''),
 S('results','Results — expected value ต่างจาก best sample','Results: expected value differs from the best sample',
 '''<!--OUTPUT-->
 <!--FIGURE:qaoa-results-->
 <div class="table-wrapper"><table><thead><tr><th>Method</th><th>Expected cut</th><th>Expected / optimum</th></tr></thead><tbody><tr><td>Random</td><td>4.500</td><td>0.643</td></tr><tr><td>QAOA p=1</td><td>5.939</td><td>0.848</td></tr><tr><td>QAOA p=2</td><td>6.603</td><td>0.943</td></tr><tr><td>QAOA p=3</td><td>6.878</td><td>0.983</td></tr></tbody></table></div>
 <p>0.983 เป็นอัตราส่วนของ expected cut ต่อ optimum บน graph เดียว ไม่ใช่ probability ที่ได้ optimum และไม่ใช่ความเร็วที่เพิ่ม 98.3% ใน final sampling มี 3,791 จาก 4,096 shots ที่ให้ cut=7 หรือ 92.55% ขณะที่ random guessing ให้โอกาส 6/64 = 9.375%</p>
 <p>best sample อาจเป็น optimum แม้ expected cut ยังต่ำ จึงควรรายงานทั้ง expectation, success probability, objective calls และ total shots ถ้ารายงานเพียง bit string ที่ดีที่สุดจะซ่อนความยากในการสุ่มพบมัน</p>''',
 '''<!--OUTPUT-->
 <!--FIGURE:qaoa-results-->
 <div class="table-wrapper"><table><thead><tr><th>Method</th><th>Expected cut</th><th>Expected / optimum</th></tr></thead><tbody><tr><td>Random</td><td>4.500</td><td>0.643</td></tr><tr><td>QAOA p=1</td><td>5.939</td><td>0.848</td></tr><tr><td>QAOA p=2</td><td>6.603</td><td>0.943</td></tr><tr><td>QAOA p=3</td><td>6.878</td><td>0.983</td></tr></tbody></table></div>
 <p>The ratio 0.983 means expected cut divided by optimum on this graph. It is neither the probability of reaching the optimum nor a speed increase of 98.3%. Final sampling finds cut=7 in 3,791 of 4,096 shots, or 92.55%. Random guessing succeeds with probability 6/64 = 9.375%.</p>
 <p>The best sample can be optimal even while expectation is low. Report expectation, optimum-hit probability, objective evaluations and total shots. Showing only the best bitstring hides how difficult it was to obtain.</p>'''),
 S('limits','Limits — heuristic ต้องมี evidence','Limits: a heuristic needs evidence',
 '''<p>original QAOA paper ให้ guarantee อย่างน้อย 0.6924 สำหรับ p=1 บน 3-regular MaxCut ส่วน Goemans–Williamson มี classical approximation guarantee ประมาณ 0.87856 ขอบเขตเหล่านี้ใช้กับกลุ่มโจทย์ที่ theorem ระบุ ไม่ใช่ค่าที่ทุก instance จะทำได้พอดี ผล 0.848 ในตัวอย่างจึงไม่ขัดกับ guarantee ของ QAOA</p>
 <p>การเพิ่ม p ขยาย expressive power ของ circuit แต่การฝึกอาจติด local optimum และ circuit ยาวขึ้นบน hardware จะรับ noise เพิ่ม งานเรื่อง symmetry/locality แสดงข้อจำกัดของ shallow QAOA ในบาง graph families ส่วน barren plateaus เป็นอุปสรรคของ variational circuits ภายใต้เงื่อนไขต่าง ๆ ไม่ควรสรุปว่าทุก QAOA instance ฝึกไม่ได้</p>
 <p>ตัวอย่างนี้แสดงว่าปรับ distribution ให้ดีขึ้นได้ใน ideal simulation ยังไม่ได้พิสูจน์ practical advantage คำอ้างที่แรงขึ้นต้องใช้ instance ที่มีความหมาย เปรียบเทียบกับ classical solvers ที่แข็งแรง และนับ tuning กับ repeated sampling ทั้งหมด</p>''',
 '''<p>The original QAOA analysis guarantees at least 0.6924 for p=1 on 3-regular MaxCut. Goemans–Williamson gives a classical approximation guarantee around 0.87856. These bounds describe their theorem's problem families; they do not predict the exact result of each instance. Our observed 0.848 therefore does not contradict QAOA's guarantee.</p>
 <p>Increasing p expands the circuit family, but optimization can stall and deeper hardware circuits accumulate noise. Locality and symmetry results limit shallow QAOA on certain graph families. Barren plateaus can obstruct variational training under relevant conditions; they do not imply every QAOA instance is untrainable.</p>
 <p>This experiment shows distribution improvement in an ideal simulation. It establishes no practical advantage. A stronger claim requires meaningful instances, strong classical competitors and accounting for tuning and repeated sampling.</p>''')],
 exercise={'th':'รัน p=1 ด้วย restarts=1 และ 20 บน seed เดียวกัน บันทึก objective calls และ expected cut ทั้งหมด แล้วคำนวณงบ shots สมมติ 1,000 shots ต่อ call เปลี่ยน graph ได้เมื่อแก้ classical baseline และ tests พร้อมกัน',
 'en':'Compare p=1 with one and twenty restarts using the same seed. Record objective calls and expectation, then budget 1,000 hypothetical shots per call. If changing the graph, update the classical reference and tests too.'}),

dict(n=6,slug='quantum-programmers-simulation',short='Simulate Physics',
 title={'th':'Quantum Simulation — จำลอง physics','en':'Quantum Simulation: Simulate Physics and Measure an Observable'},
 sub={'th':'ต่อยอดบท quantum simulation ในเอกสารด้วย experiment สอง qubits เปรียบเทียบ exact evolution กับ product formula และเห็น trade-off ของความแม่นกับ depth',
 'en':'Extend the guide with a two-qubit experiment: compare exact evolution with a product formula and inspect the accuracy–depth trade-off.'},
 module='quantum_simulation',test='SimulationTests',figures=['simulation-flow','simulation-results'],functions=['trotter'],refs=['feynman','lloyd','simulation','chemistry'],
 sections=[
 S('task','Native problem — เลือกคำถามที่ output ไม่ใหญ่','Native problem: choose a compact output',
 '''<p><strong>Quantum simulation</strong> ใช้ระบบ quantum จำลอง dynamics หรือคุณสมบัติของอีกระบบ quantum จุดเริ่มที่ Feynman เสนอคือ classical representation ของ many-body state อาจโตแบบ exponential ขณะที่ quantum processor ใช้ qubits เพื่อแทนระบบโดยตรง งานนี้จึงมีโครงสร้างที่สอดคล้องกับเครื่องมากกว่าการนำฐานข้อมูล classical ขนาดใหญ่มาโหลดทั้งหมด</p>
 <p>โจทย์สำคัญใน chemistry และ materials เกี่ยวกับ Hamiltonian ซึ่งเป็น operator ที่บอก energy และ evolution แต่ไม่ได้แปลว่าทุก molecule ต้องใช้ quantum computer classical approximations และ tensor-network methods ทำงานได้ดีในหลาย regime การอ้าง advantage ต้องระบุว่า classical method ติดขัดตรงไหน</p>
 <p>ในเอกสารต้นทางบทนี้เป็นภาพรวม เราเพิ่ม runnable experiment ใหม่: สอง qubits เริ่มที่ |00⟩ วิวัฒน์เวลา t=1 แล้วถามค่า <strong>⟨Z₀Z₁⟩</strong> ซึ่งเป็นตัวเลขเดียว ตัวอย่างเล็กนี้ไม่มี speedup แต่เปิดให้ตรวจทั้ง approximation และ output contract อย่างครบถ้วน</p>''',
 '''<p><strong>Quantum simulation</strong> uses one quantum system to model the dynamics or properties of another. Feynman's motivating observation was that classical representations of many-body states can grow exponentially, whereas a quantum processor represents the system with qubits. This creates a natural structure without necessarily loading a large arbitrary classical dataset.</p>
 <p>Chemistry and materials problems are expressed through Hamiltonians, operators describing energy and evolution. That does not make every molecule a quantum-computing target: classical approximations and tensor-network methods work well in many regimes. An advantage claim must identify where those methods fail.</p>
 <p>The guide presents this topic as an overview. We add a new executable experiment: two qubits start in |00⟩, evolve to t=1, and return one number, <strong>⟨Z₀Z₁⟩</strong>. This small system offers no speedup, but exposes both approximation error and the output contract.</p>'''),
 S('model','Model — Hamiltonian และ observable คนละหน้าที่','Model: distinguish the Hamiltonian from the observable',
 '''<p>ใช้ H = Z₀Z₁ + 0.7(X₀ + X₁) โดย X คือ bit-flip Pauli operator ส่วน Z ใส่เครื่องหมาย +1 บน |0⟩ และ −1 บน |1⟩ evolution ที่ต้องการคือ U(t)=exp(−iHt) เมื่อใช้หน่วยที่ ℏ=1 Hamiltonian บอกว่าจะ evolve อย่างไร ส่วน observable Z₀Z₁ บอกว่าจะวัดอะไร</p>
 <!--FIGURE:simulation-flow-->
 <p>สำหรับสอง qubits เราสร้าง matrix 4×4 แล้วใช้ <code>scipy.linalg.expm</code> หาค่า exact เพื่อเป็น reference ได้ คำว่า exact ในที่นี้หมายถึงการ exponentiate matrix โดยตรงภายใน floating-point accuracy ไม่ได้หมายถึงผล hardware ไร้ error</p>
 <p>เมื่อวัด qubits ทั้งสองใน Z basis outcome ที่ bits เหมือนกันให้ค่า ZZ=+1 และต่างกันให้ −1 ค่าเฉลี่ยของ shots จึงประมาณ ⟨ZZ⟩ ได้โดยไม่ต้อง reconstruct amplitudes ทั้งหมด หากใช้ S shots standard error ของ sample mean จะไม่เกิน 1/√S ในการสุ่มอิสระของ observable ±1 นี้</p>''',
 '''<p>Use H = Z₀Z₁ + 0.7(X₀ + X₁). X is the Pauli bit-flip operator; Z assigns +1 to |0⟩ and −1 to |1⟩. With ℏ=1, evolution is U(t)=exp(−iHt). The Hamiltonian specifies how the state evolves; the observable Z₀Z₁ specifies what we ask it to reveal.</p>
 <!--FIGURE:simulation-flow-->
 <p>At two qubits, a 4×4 matrix and <code>scipy.linalg.expm</code> provide a direct reference. Here “exact” means direct matrix exponentiation within floating-point accuracy, not an error-free hardware measurement.</p>
 <p>Computational-basis outcomes with matching bits contribute ZZ=+1; differing bits contribute −1. Averaging shots estimates ⟨ZZ⟩ without reconstructing all amplitudes. For S independent ±1 measurements, the sample mean's standard error is at most 1/√S.</p>'''),
 S('formula','Product formula — noncommuting terms ต้องแบ่งเวลา','Product formula: split time for noncommuting terms',
 '''<p>terms ZZ และ X₀+X₁ ไม่ commute กัน จึงไม่สามารถแทน exp(−i(A+B)t) ด้วย exp(−iAt)exp(−iBt) เพียงครั้งเดียวแล้วอ้างว่าตรงได้ เราแบ่งเวลาเป็น m steps และทำ product formula ซ้ำ โดย dt=t/m แต่ละ step ใช้ RZZ(2dt) แล้ว RX(1.4dt) บนสอง qubits</p>
 <!--CODE-->
 <p>ลำดับ gate ใน code ต้องอ่านให้ตรงกับ matrix multiplication: gate ที่ apply ก่อนอยู่ด้านขวาของ product เมื่อคูณ statevector ตัวทดสอบจึงเทียบ full circuit unitary กับ exp(−iHt) โดยตรงด้วย ไม่ได้เทียบแค่ observable ที่อาจบังข้อผิดพลาดบางอย่าง</p>
 <p>first-order product formula มี error ที่ลดลงเมื่อเพิ่ม m สำหรับ fixed time และ Hamiltonian ที่เหมาะสม ในตัวอย่างนี้ state infidelity ลดใกล้ O(1/m²) แต่ scaling นี้เป็นผลของ metric และกรณีที่กำลังดู ไม่ควรใช้ตัวเลขเดียวนี้แทน complexity bound ของทุก quantum simulation</p>''',
 '''<p>ZZ and X₀+X₁ do not commute. A single exp(−iAt)exp(−iBt) therefore cannot be substituted for exp(−i(A+B)t) as an exact identity. Divide time into m steps with dt=t/m. Each step applies RZZ(2dt), then RX(1.4dt) on both qubits.</p>
 <!--CODE-->
 <p>Match circuit order to matrix multiplication: the first applied gate sits on the right of the matrix product acting on a statevector. Our test compares the full circuit unitary with exp(−iHt), as well as inspecting an observable that might hide some errors.</p>
 <p>For fixed time and a suitable Hamiltonian, first-order product-formula error decreases as m increases. State infidelity in this example falls approximately as O(1/m²). That observed metric is not a universal complexity bound for quantum simulation.</p>'''),
 S('results','Convergence — ชัดเจนว่า approximation ดีขึ้น','Convergence: make the approximation error visible',
 '''<!--OUTPUT-->
 <!--FIGURE:simulation-results-->
 <p>exact expectation เท่ากับ 0.352560 สำหรับ m=1 ได้ 0.028889 ซึ่งยังห่างมาก เมื่อเพิ่มเป็น 16 steps ได้ 0.351014 และ infidelity เหลือ 0.000862 ผลนี้คำนวณจาก ideal statevector ไม่ได้เก็บ shots จึงไม่มี sampling uncertainty ใน plot มีเฉพาะ approximation และ floating-point error</p>
 <div class="table-wrapper"><table><thead><tr><th>Steps m</th><th>Two-qubit RZZ gates</th><th>State infidelity</th></tr></thead><tbody><tr><td>1</td><td>1</td><td>0.351853</td></tr><tr><td>4</td><td>4</td><td>0.014434</td></tr><tr><td>16</td><td>16</td><td>0.000862</td></tr></tbody></table></div>
 <p>ใน hardware การเพิ่ม steps เพิ่ม two-qubit gate count และอาจเพิ่ม routing gates ด้วย จึงมีจุดที่ approximation ดีขึ้นแต่ noise แย่ลง ต้องแยก error budget เป็น model error, product-formula error, gate/readout error และ sampling error ก่อนเลือก depth</p>''',
 '''<!--OUTPUT-->
 <!--FIGURE:simulation-results-->
 <p>The direct reference is 0.352560. One step gives 0.028889, a large discrepancy. Sixteen steps give 0.351014 with state infidelity 0.000862. These are ideal statevector calculations, not shot samples; the chart contains approximation and floating-point error, without sampling uncertainty.</p>
 <div class="table-wrapper"><table><thead><tr><th>Steps m</th><th>Two-qubit RZZ gates</th><th>State infidelity</th></tr></thead><tbody><tr><td>1</td><td>1</td><td>0.351853</td></tr><tr><td>4</td><td>4</td><td>0.014434</td></tr><tr><td>16</td><td>16</td><td>0.000862</td></tr></tbody></table></div>
 <p>On hardware, extra steps add two-qubit gates and may require routing gates. Approximation can improve while noise worsens. Separate model error, product-formula error, gate/readout error and sampling error before choosing depth.</p>'''),
 S('scope','Why it matters — simulation ไม่ใช่ HHL','Why it matters: simulation is distinct from HHL',
 '''<p>HHL ใช้ Hamiltonian evolution เป็น subroutine เพื่อ invert matrix แต่ chemistry simulation ใช้ evolution, energy estimation หรือ correlation measurements เป็นงานหลัก เป้าหมายและ output จึงต่างกัน แม้ใช้ phase estimation หรือเทคนิควงจรร่วมกันได้</p>
 <p>การหา ground-state energy ยังมีโจทย์ state preparation และ spectral overlap เพิ่ม ไม่ใช่แค่เรียก QPE แล้วได้ ground state ทันที งาน resource estimate สำหรับ FeMoco ของ Reiher และคณะแสดงตัวอย่างการผูก scientific target เข้ากับความต้องการของ fault-tolerant machine อย่างเป็นรูปธรรม แต่ไม่ได้เป็นผลจำลอง molecule นั้นบน hardware ที่ใช้ได้ทั่วไปแล้ว</p>
 <p>เมื่ออ่านคำอ้างเรื่อง quantum advantage ให้ระบุ observable, precision, verification method และ classical competitor ทุกครั้ง การจำลองระบบ quantum มีเหตุผลเชิงโครงสร้างที่แข็งแรง ส่วนความคุ้มค่าของ workload เฉพาะยังเป็นคำถามที่ต้องพิสูจน์ด้วย evidence</p>''',
 '''<p>HHL borrows Hamiltonian evolution to invert a matrix. Chemistry simulation uses evolution, energy estimation or correlation measurements as the task itself. The objectives and outputs differ even when they share phase-estimation machinery.</p>
 <p>Ground-state energy estimation also needs suitable state preparation and spectral overlap. Calling QPE does not automatically prepare the ground state. Reiher and colleagues' FeMoco resource study illustrates how a scientific target can be translated into fault-tolerant resource requirements; it is not a completed general-purpose hardware simulation of that target.</p>
 <p>For any advantage claim, specify the observable, precision, verification method and classical competitor. Quantum simulation has a strong structural motivation. Whether a particular workload is useful remains an evidence question.</p>''')],
 exercise={'th':'เปลี่ยน t เป็น 0 แล้วตรวจว่า unitary เป็น identity จากนั้นเพิ่มการสุ่มวัด ZZ และรายงาน confidence interval เปรียบเทียบ 100 กับ 10,000 shots แยก sampling error จาก product-formula error ให้ชัด',
 'en':'Set t=0 and verify identity evolution. Then sample ZZ measurements, report an uncertainty interval for 100 versus 10,000 shots, and separate sampling error from product-formula error.'}),

dict(n=7,slug='quantum-programmers-scorecard',short='Engineering Verdict',
 title={'th':'Quantum Engineering — ตรวจต้นทุน','en':'Quantum Engineering: A Scorecard, a Cost Ledger and a Decision'},
 sub={'th':'รวมทั้งซีรีส์เป็น engineering decision ตรวจ input/output, oracle, logical qubits และ baseline ก่อนรับคำอ้างว่า quantum เร็วกว่า',
 'en':'Turn the series into an engineering decision: inspect input/output, oracles, logical resources and baselines before accepting a speedup claim.'},
 module='engineering_scorecard',test='ScorecardTests',figures=['engineering-flow','cost-ledger'],functions=['Budget'],refs=['survey','overheads','gidney','errorcorrection','nist'],
 sections=[
 S('scorecard','Scorecard — สี่ algorithms แก้คนละโจทย์','Scorecard: four algorithms, four different contracts',
 '''<p>หลังรันหกบทแรก เรามีวิธีอ่าน quantum algorithm เป็น software component: ระบุ input ที่เข้าถึงได้ operation ที่ทำได้ output ที่อ่าน และ cost model ที่นับ การพูดว่า “quantum เร็วกว่า” โดยไม่ระบุสี่อย่างนี้ยังไม่พอสำหรับ architecture decision</p>
 <div class="table-wrapper"><table><thead><tr><th>Algorithm</th><th>Mathematical opportunity</th><th>Boundary to inspect</th><th>What our lab establishes</th></tr></thead><tbody><tr><td>Grover</td><td>Θ(√N) oracle queries</td><td>reversible predicate และ per-query cost</td><td>amplification และ over-rotation ตรงทฤษฎี</td></tr><tr><td>Shor</td><td>polynomial ใน bit length</td><td>scalable arithmetic และ fault tolerance</td><td>period 4 → factors 3,5 สำหรับ 15</td></tr><tr><td>HHL</td><td>dimension dependence ต่ำภายใต้เงื่อนไข</td><td>state preparation, κ, precision, readout</td><td>normalized solution state ของระบบ 2×2</td></tr><tr><td>QAOA</td><td>parameterized heuristic</td><td>training, noise, classical solver</td><td>distribution ดีขึ้นบน graph หก vertices</td></tr><tr><td>Simulation</td><td>quantum dynamics ที่มีโครงสร้าง</td><td>observable, preparation, error budget</td><td>product formula converge บนสอง qubits</td></tr></tbody></table></div>
 <p>ไม่มีแล็บใดในซีรีส์นี้พิสูจน์ practical advantage และไม่มีข้อไหนบอกว่า simulation ที่ใช้ classical computer ทำงานเร็วกว่า classical computer ทุกกรณี สิ่งที่ได้คือพื้นฐานและการตรวจ implementation ที่ตรวจซ้ำได้</p>''',
 '''<p>After six experiments, we can read a quantum algorithm as a software component: accessible inputs, permitted operations, readable outputs and a cost model. “Quantum is faster” without those contracts is insufficient for an architecture decision.</p>
 <div class="table-wrapper"><table><thead><tr><th>Algorithm</th><th>Mathematical opportunity</th><th>Boundary to inspect</th><th>What our lab establishes</th></tr></thead><tbody><tr><td>Grover</td><td>Θ(√N) oracle queries</td><td>Reversible predicate and per-query cost</td><td>Predicted amplification and over-rotation</td></tr><tr><td>Shor</td><td>Polynomial in bit length</td><td>Scalable arithmetic and fault tolerance</td><td>Order 4 gives factors 3,5 for 15</td></tr><tr><td>HHL</td><td>Low dimension dependence under conditions</td><td>Preparation, κ, precision and readout</td><td>A normalized solution state for a 2×2 system</td></tr><tr><td>QAOA</td><td>Parameterized heuristic</td><td>Training, noise and classical solvers</td><td>Improved distribution on one six-node graph</td></tr><tr><td>Simulation</td><td>Structured quantum dynamics</td><td>Observable, preparation and error budget</td><td>Product-formula convergence on two qubits</td></tr></tbody></table></div>
 <p>None of these labs demonstrates practical advantage. A classical simulation of a quantum algorithm does not establish that a quantum device beats classical computing. The deliverable is a reproducible foundation and a checked implementation.</p>'''),
 S('architecture','System boundary — ให้ quantum kernel เป็นส่วนหนึ่ง','System boundary: place the quantum kernel inside a workflow',
 '''<!--FIGURE:engineering-flow-->
 <p>ใน production quantum processor จะเป็น resource ที่ classical service เรียกใช้ โค้ดรอบนอกยังต้องจัด task schema, state preparation, circuit compilation, calibration assumptions, batching, shot allocation, retry และ validation ผล การมี quantum kernel ไม่ได้ลบความรับผิดชอบของ software engineering</p>
 <p>กำหนด output ให้เทียบกันได้ เช่น observable หนึ่งตัวที่ additive error ε และ confidence ที่กำหนด หรือ cut ที่ถึง quality threshold ภายใต้งบเดียวกัน ถ้าฝั่ง quantum คืน quantum state แต่ฝั่ง classical คืน array ครบ การเทียบเวลาโดยตรงกำลังนับคนละ task</p>
 <p>เก็บ experiment record อย่างน้อยเป็น problem instance, input access model, circuit/algorithm revision, parameter settings, backend และ compilation settings, shot budget, success criterion, raw measurements และ classical baseline revision ข้อมูลเหล่านี้ทำให้แยก algorithm effect ออกจากการเปลี่ยน environment ได้</p>''',
 '''<!--FIGURE:engineering-flow-->
 <p>A production quantum processor is a resource called by a classical workflow. Surrounding code still owns task schemas, state preparation, compilation, calibration assumptions, batching, shot allocation, retries and validation. A quantum kernel retains the need for ordinary software engineering.</p>
 <p>Specify comparable outputs: an observable to additive error ε and a stated confidence, or a cut meeting a quality threshold under a fixed budget. A quantum state and a complete classical array are different deliverables. Timing them without accounting for that difference compares different tasks.</p>
 <p>Record the problem instance, input-access model, algorithm revision, parameters, backend and compiler settings, shots, success criterion, raw measurements and baseline revision. These records separate algorithm changes from environment changes.</p>'''),
 S('cost','Cost ledger — kernel เร็ว แต่ workflow ช้า','Cost ledger: a fast kernel can produce a slow workflow',
 '''<!--CODE-->
 <!--OUTPUT-->
 <!--FIGURE:cost-ledger-->
 <p>ตัวเลขนี้เป็น scenario ที่กำหนดเพื่อสอนการนับต้นทุน ไม่ใช่ benchmark ให้ classical baseline ใช้ 1 วินาที quantum kernel ใช้ 0.1 วินาทีต่อ attempt แต่ต้องมี preparation 0.8 วินาที ทำ 5 attempts และ postprocess อีก 0.2 วินาที จึงรวม 1.5 วินาที หรือ end-to-end speedup เพียง 0.667×</p>
 <p>formula ของแล็บสมมติ preparation เกิดครั้งเดียว ถ้าต้องเตรียมใหม่ต่อ attempt ให้ย้ายต้นทุนส่วนนั้นเข้า per-attempt term สำหรับ QAOA ยังต้องรวม optimizer calls ทุก restart ส่วน HHL ต้องรวม post-selection failures และการประมาณ observable ด้วย</p>
 <p>รายงานทั้งเวลารวม เวลา queue หากเป็น remote service ค่าใช้จ่าย และผลที่ยังไม่สำเร็จ จะใช้ค่าเฉลี่ยของ successful attempts อย่างเดียวไม่ได้เมื่อ failure probability ทำให้ต้องรันซ้ำหลายครั้ง</p>''',
 '''<!--CODE-->
 <!--OUTPUT-->
 <!--FIGURE:cost-ledger-->
 <p>These are hypothetical inputs for teaching cost accounting. A classical baseline takes one second. A quantum kernel takes 0.1 seconds per attempt, but preparation adds 0.8 seconds, five attempts are needed, and postprocessing adds 0.2 seconds. Total time is 1.5 seconds: an end-to-end speedup of only 0.667×.</p>
 <p>This ledger assumes preparation occurs once. If it repeats per attempt, move that work into the per-attempt term. For QAOA, include every optimizer restart. For HHL, include post-selection failures and observable estimation.</p>
 <p>Report total elapsed time, remote queue time when applicable, cost and unresolved runs. Averaging only successful attempts hides the work needed to reach one accepted result.</p>'''),
 S('resources','Resources — physical และ logical qubits','Resources: physical and logical qubits',
 '''<p><strong>Physical qubit</strong> คืออุปกรณ์ที่มี error ส่วน <strong>logical qubit</strong> encode ข้อมูลด้วย error-correcting code บน physical qubits หลายตัว จำนวนที่ต้องใช้ขึ้นกับ code, error rates, target logical error และงานที่รัน ไม่มี conversion ratio เดียวที่ใช้ได้ทุก architecture</p>
 <p>งานของ Google Quantum AI เรื่อง below-threshold surface-code error correction แสดงว่าการเพิ่ม code distance สามารถลด logical error ใน regime ที่ทดลองได้ เป็นหลักฐานด้าน error correction ที่สำคัญ แต่ไม่ได้ทำให้ every circuit fault-tolerant โดยอัตโนมัติ resource estimate ของ application ต้องรวม reliable gate count, logical depth และ overhead ที่ใช้จริง</p>
 <p>simulator แบบ dense complex128 ต้องเก็บ state อย่างน้อย 16·2<sup>n</sup> bytes สำหรับ n=30 คือ 16 GiB ก่อน workspaces และสำเนา การเพิ่ม qubits บน simulator จึงไม่ใช่วิธีวัดว่า quantum hardware จะ scale ได้อย่างไร ส่วน roadmap ของ vendor เป็นแผนที่ควรติดตามแยกจากผลที่ตรวจซ้ำแล้ว</p>''',
 '''<p>A <strong>physical qubit</strong> is a noisy device. A <strong>logical qubit</strong> encodes information using an error-correcting code over multiple physical qubits. The ratio depends on the code, error rates, target logical error and workload; there is no universal conversion factor.</p>
 <p>Google Quantum AI's below-threshold surface-code experiment demonstrates decreasing logical error as code distance increases in the tested regime. That is important error-correction evidence, not automatic fault tolerance for arbitrary application circuits. Application estimates also require reliable gate counts, logical depth and actual overheads.</p>
 <p>A dense complex128 simulator stores at least 16·2<sup>n</sup> bytes for an n-qubit state. At n=30 that is 16 GiB before workspaces and copies. Simulator scaling is not a measure of quantum-hardware scaling. Vendor roadmaps should be tracked separately from reproduced results.</p>'''),
 S('decision','Decision — ใช้ทักษะนี้อย่างไรต่อ','Decision: what to do with this knowledge',
 '''<ol><li><strong>เลือก structure:</strong> มี hidden period, compact quantum dynamics หรือ predicate ที่เหมาะสมหรือไม่</li><li><strong>ตรึง input/output:</strong> เตรียม state ได้อย่างไร และต้องอ่านอะไรที่ precision เท่าใด</li><li><strong>ใช้ strong baseline:</strong> รวม indexing, sparse methods, preconditioning และ heuristic ที่ใช้จริงตามโจทย์</li><li><strong>เปิด cost ทั้งหมด:</strong> oracle gates, compilation, fault tolerance, training, shots, failures และ postprocessing</li><li><strong>แยกระดับ evidence:</strong> theorem → ideal simulation → noisy experiment → verified workload benefit</li></ol>
 <p>สำหรับ programmer งานที่ทำได้ทันทีคือรักษา tests ที่ตรวจ amplitude, phase และ classical postprocessing แยกกัน ฝึกอ่าน complexity พร้อม assumptions และเริ่มทำ cryptography inventory กับทีมที่รับผิดชอบความปลอดภัย มาตรฐาน PQC เป็น classical algorithms ที่ใช้บนระบบปัจจุบัน ไม่ต้องซื้อ quantum computer ก่อน</p>
 <p>เมื่อจบซีรีส์ควรอธิบายได้ว่า Grover ประหยัด queries, Shor ใช้ period, HHL คืน state, QAOA ปรับ distribution และ quantum simulation ถาม observable จาก physics ความเข้าใจที่แยกสิ่งเหล่านี้ได้จะช่วยเลือกงานและประเมินคำอ้างอย่างเป็นวิศวกร</p>''',
 '''<ol><li><strong>Identify structure:</strong> is there a hidden period, compact quantum dynamics or a suitable predicate?</li><li><strong>Freeze input/output:</strong> how is the state prepared, and what must be read at what precision?</li><li><strong>Use a strong baseline:</strong> include indexing, sparse methods, preconditioning and practical heuristics where relevant.</li><li><strong>Expose full cost:</strong> oracle gates, compilation, fault tolerance, training, shots, failures and postprocessing.</li><li><strong>Separate evidence levels:</strong> theorem → ideal simulation → noisy experiment → verified workload benefit.</li></ol>
 <p>Programmers can act now by preserving separate tests for amplitudes, phases and classical postprocessing, reading complexity together with its assumptions, and inventorying cryptography with the responsible security team. PQC standards describe classical algorithms deployable on existing systems; they do not require buying a quantum computer.</p>
 <p>You should now be able to explain why Grover saves queries, Shor finds periods, HHL returns a state, QAOA shapes a distribution, and quantum simulation asks physics for an observable. Those distinctions make a quantum proposal concrete enough for engineering review.</p>''')],
 exercise={'th':'เลือก workload ที่รู้จักหนึ่งงาน เขียน input/output contract และ strong classical baseline แล้วเติม cost ledger ด้วยค่าที่วัดได้จริง เก็บค่าที่ไม่ทราบเป็น unknown และสรุปว่าหลักฐานที่มีรองรับการตัดสินใจระดับใด',
 'en':'Choose one familiar workload, write its input/output contract and strong classical baseline, and fill a ledger with measured costs. Keep unmeasured values unknown and state which decision the available evidence supports.'}),
]
