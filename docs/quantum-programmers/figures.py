"""Extract the owner's vector illustrations and plot verified companion data.

Usage: python figures.py --source '/path/to/the/source.pdf' --results results.json
Requires PyMuPDF and matplotlib. The supplied original is never modified.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'images'
HERE = Path(__file__).resolve().parent
NAVY, VIOLET, TEAL, AMBER, CORAL = '#182747', '#7047eb', '#108c9a', '#bd7414', '#ca4c35'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.labelcolor': NAVY, 'text.color': NAVY,
                     'axes.titleweight': 'bold', 'figure.facecolor': 'white'})

# x0,y0,x1,y1 in PDF points; captions are recreated accessibly in both languages.
CROPS = {
 'bloch': (5, [54, 475, 542, 694], '1.1'),
 'pattern': (6, [54, 480, 542, 736], '1.2'),
 'amplitudes': (10, [54, 54, 542, 227], '3.1'),
 'rotation': (11, [54, 54, 542, 314], '3.2'),
 'overrotation': (11, [54, 470, 542, 713], '3.3'),
 'grover-circuit': (12, [54, 183, 542, 329], '3.4'),
 'oracle-diffuser': (12, [54, 365, 542, 538], '3.5'),
 'queries': (15, [54, 54, 542, 280], '3.7'),
 'shor-flow': (17, [54, 54, 542, 279], '4.1'),
 'period': (17, [54, 400, 542, 609], '4.2'),
 'qft': (18, [54, 431, 542, 568], '4.3'),
 'shor-circuit': (20, [54, 335, 542, 573], '4.4'),
 'hhl-flow': (25, [54, 54, 542, 274], '5.1'),
 'hhl-circuit': (27, [54, 377, 542, 616], '5.2'),
 'qaoa-flow': (30, [54, 54, 542, 257], '6.1'),
 'qaoa-circuit': (32, [54, 54, 542, 227], '6.2'),
}


def save(fig, name):
    fig.savefig(OUT / ('quantum-' + name + '.png'), dpi=180, bbox_inches='tight', pad_inches=.22)
    plt.close(fig)


def flow(name, title, labels, notes):
    fig, ax = plt.subplots(figsize=(11, 3.9))
    ax.set(xlim=(0, 11), ylim=(0, 3.9)); ax.axis('off')
    ax.text(.1, 3.55, title, fontsize=18, weight='bold')
    colors=[NAVY,VIOLET,TEAL,AMBER]
    for i,(label,note) in enumerate(zip(labels,notes)):
        x=.1+2.8*i
        ax.add_patch(FancyBboxPatch((x,1.7),2.3,1,boxstyle='round,pad=0.04',fc=colors[i],ec='none'))
        ax.text(x+1.15,2.2,label,color='white',ha='center',va='center',fontsize=12,weight='bold')
        ax.text(x+1.15,1.35,note,ha='center',va='top',fontsize=11,linespacing=1.6)
        if i<3:ax.add_patch(FancyArrowPatch((x+2.34,2.2),(x+2.74,2.2),arrowstyle='-|>',mutation_scale=16,color=NAVY))
    save(fig,name)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--results',required=True)
    args=ap.parse_args()
    import pymupdf
    doc=pymupdf.open(args.source)
    for name,(page,rect,number) in CROPS.items():
        doc[page-1].get_pixmap(matrix=pymupdf.Matrix(3,3),clip=pymupdf.Rect(rect),alpha=False).save(OUT/('quantum-'+name+'.png'))
    provenance={'source_title':doc.metadata.get('title'),'source_sha256':hashlib.sha256(Path(args.source).read_bytes()).hexdigest(),
                'illustrations':{name:{'page':p,'rect_points':r,'source_figure':f} for name,(p,r,f) in CROPS.items()}}
    (HERE/'source-figures.json').write_text(json.dumps(provenance,indent=2)+'\n')
    result=json.loads(Path(args.results).read_text())
    (HERE/'verified-results.json').write_text(json.dumps(result,indent=2)+'\n')
    # New charts use the rerun, not a redrawn estimate of a PDF histogram.
    fig,ax=plt.subplots(figsize=(10,4))
    counts=result['grover_search']['data']['counts'];labels=[f'{i:04b}' for i in range(16)]
    ax.bar(labels,[counts.get(k,0) for k in labels],color=[VIOLET if k=='1011' else '#adb8ca' for k in labels])
    ax.tick_params(axis='x',labelrotation=60);ax.set(title='Grover: 3,928 marked outcomes in 4,096 ideal shots',ylabel='Count',xlabel='Measured q3 q2 q1 q0')
    save(fig,'grover-results')
    fig,ax=plt.subplots(figsize=(9,4))
    counts=result['shor_factor15']['data']['counts'];values=[0,64,128,192]
    ax.bar([str(v) for v in values],[counts[f'{v:08b}'] for v in values],color=['#adb8ca',VIOLET,'#adb8ca',VIOLET])
    for i,v in enumerate(values):ax.text(i,counts[f'{v:08b}']+10, ['retry','r = 4','retry','r = 4'][i],ha='center')
    ax.set(title='Shor: four Fourier peaks; two reveal the full order',ylabel='Count in 2,048 ideal shots',xlabel='Counting-register integer y',ylim=(0,650))
    save(fig,'shor-results')
    fig,ax=plt.subplots(figsize=(9,4));x=np.arange(2)
    h=result['hhl_2x2']['data']
    for i,(label,vals,c) in enumerate([('Classical normalized',[.9,.1],NAVY),('Exact HHL',h['exact'],VIOLET),('Post-selected shots',h['sampled'],TEAL)]):
        ax.bar(x+(i-1)*.24,vals,.23,label=label,color=c)
    ax.set(xticks=x,xticklabels=['x = 0','x = 1'],ylabel='Conditional probability',ylim=(0,1.15),title='HHL: probability matches; relative sign needs another check');ax.legend(frameon=False)
    save(fig,'hhl-results')
    fig,axs=plt.subplots(1,2,figsize=(11,4),gridspec_kw={'width_ratios':[1,1.4]})
    rows=result['qaoa_maxcut']['data']['rows'];axs[0].bar(['Random','p=1','p=2','p=3'],[4.5]+[r['value'] for r in rows],color=['#adb8ca',VIOLET,VIOLET,TEAL])
    axs[0].axhline(7,color=NAVY,ls='--');axs[0].set(title='Expected cut (optimum = 7)',ylim=(0,7.8),ylabel='Cut edges')
    nodes={0:(0,1),1:(-.85,-.5),2:(.85,-.5),3:(.3,1.4),4:(-.55,-.1),5:(1.15,-.1)}
    edges=[(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)]
    def cut(bits):return sum(bits[::-1][i]!=bits[::-1][j] for i,j in edges)
    counts=result['qaoa_maxcut']['data']['counts'];best=max(counts,key=lambda b:(cut(b),counts[b]));side=best[::-1]
    ax=axs[1];ax.axis('off');ax.set_title('Triangular prism: best sampled cut = 7')
    for i,j in edges:
        a,b=nodes[i],nodes[j];ax.plot([a[0],b[0]],[a[1],b[1]],color=CORAL if side[i]!=side[j] else '#adb8ca',lw=2.5)
    for i,(xx,yy) in nodes.items():
        ax.scatter(xx,yy,s=550,c=VIOLET if side[i]=='0' else TEAL,zorder=3);ax.text(xx,yy,str(i),ha='center',va='center',color='white',weight='bold')
    ax.margins(.23);save(fig,'qaoa-results')
    flow('simulation-flow','Quantum simulation: ask for an observable',
         ['Choose H','Compile evolution','Prepare and run','Estimate <ZZ>'],
         ['H = ZZ + 0.7(XI + IX)','Product formula\nwith m time steps','Start in |00>\napply exp(-iHt)','Repeated measurements\n+ uncertainty'])
    rows=result['quantum_simulation']['data']['rows'];fig,axs=plt.subplots(1,2,figsize=(11,4))
    axs[0].plot([r['steps'] for r in rows],[r['zz'] for r in rows],'o-',color=TEAL,label='Product formula')
    axs[0].axhline(result['quantum_simulation']['data']['exact_zz'],color=NAVY,ls='--',label='Exact expm')
    axs[0].set(xlabel='Product-formula steps m',ylabel='<ZZ>',title='Observable converges');axs[0].legend(frameon=False)
    axs[1].loglog([r['steps'] for r in rows],[r['infidelity'] for r in rows],'o-',color=VIOLET)
    axs[1].set(xlabel='Steps m (more gates)',ylabel='1 - state fidelity',title='Approximation error falls (ideal circuit)')
    save(fig,'simulation-results')
    flow('engineering-flow','An engineering contract around the quantum kernel',
         ['Classical baseline','Input contract','Quantum kernel','Validate output'],
         ['Same task and accuracy\nstrong solver, full cost','State preparation\nmatrix/oracle access','Depth, noise, shots\nretries and correction','Classical postprocessing\nuncertainty + cost'])
    fig,ax=plt.subplots(figsize=(10,3.5));left=0
    for label,value,color in [('Prepare',.8,NAVY),('5 kernel attempts',.5,VIOLET),('Postprocess',.2,TEAL)]:
        ax.barh('Quantum workflow',value,left=left,color=color,label=label);left+=value
    ax.barh('Classical baseline',1,color='#adb8ca');ax.set(xlabel='Hypothetical seconds (illustration, not a measurement)',xlim=(0,1.8),title='A faster kernel can still produce a slower workflow');ax.legend(frameon=False,loc='upper center',bbox_to_anchor=(.5,-.28),ncol=3)
    save(fig,'cost-ledger')
    print('Extracted 16 source illustrations and generated 8 new figures.')


if __name__=='__main__':main()
