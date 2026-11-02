"""Fifteen original diagrams-in-miniature for the engineering course covers."""
from diagram_geometry import connect

def draw(n, d, b, c, o):
    x0, y0, x1, y1 = b
    w, h = x1-x0, y1-y0
    def box(x, y, ww, hh, lit=False):
        bounds=(x-ww/2, y-hh/2, x+ww/2, y+hh/2)
        d.rounded_rectangle(bounds, radius=12,
                            fill=c['core'] if lit else c['fill'],
                            outline=c['hi'] if lit else c['ln'], width=6)
        return bounds
    def line(a,z,lit=False):
        d.line((a,z), fill=c['hi'] if lit else c['ln'], width=7)
    cy=y0+h*.5
    def link(a,z,lit=False,**kwargs):
        return connect(d,a,z,c['hi'] if lit else c['ln'],head=max(10,h*.035),**kwargs)
    if n==1:
        nodes=[]
        for i in range(3):
            nodes.append(box(x0+w*(.15+.35*i),cy,w*.23,h*(.35+.2*i),i==2))
        link(nodes[0],nodes[1]);link(nodes[1],nodes[2],True)
    elif n==2:
        box(x0+w*.5,cy,w*.86,h*.86)
        box(x0+w*.5,cy,w*.5,h*.45,True)
        for i in range(4):line((x0+w*(.18+.21*i),y0),(x0+w*(.18+.21*i),y0+h*.07))
    elif n==3:
        nodes=[]
        for i in range(4):
            xx=x0+w*(.12+.25*i); yy=y0+h*(.25 if i%2==0 else .75)
            nodes.append(box(xx,yy,w*.17,h*.26,i==3))
        for a,z in zip(nodes,nodes[1:]):link(a,z)
    elif n in (4,10):
        for i in range(4):
            box(x0+w*(.12+.25*i),cy,w*.13,h*(.3+.17*i),i==(0 if n==4 else 3))
        line((x0+w*(.27 if n==4 else .72),y0),(x0+w*(.27 if n==4 else .72),y1),True)
    elif n==5:
        for i,hh in enumerate((.2,.8,.4)):
            box(x0+w*(.2+.3*i),y1-h*hh/2,w*.2,h*hh,i==1)
    elif n==6:
        for i in range(3):
            xx=x0+w*(.2+.3*i);box(xx,cy,w*.24,h*.65,i==1)
            line((xx-w*.06,cy-h*.12),(xx+w*.06,cy-h*.12),i==1)
            line((xx-w*.06,cy+h*.1),(xx+w*.06,cy+h*.1))
    elif n==7:
        source=box(x0+w*.2,cy,w*.25,h*.5)
        for i in range(3):
            yy=y0+h*(.12+.38*i)
            target=box(x0+w*.85,yy,w*.15,h*.2,i==1)
            link(source,target,i==1)
    elif n==8:
        gate=box(x0+w*.5,cy,w*.25,h*.9,True)
        source=box(x0+w*.12,cy,w*.14,h*.35)
        target=box(x0+w*.88,cy,w*.14,h*.35)
        link(source,gate);link(gate,target,True)
        box(x0+w*.5,cy,w*.08,h*.2)
    elif n==9:
        for i in range(3):box(x0+w*(.35+.13*i),y0+h*(.3+.19*i),w*.55,h*.45,i==2)
    elif n==11:
        for i in range(3):
            yy=y0+h*(.15+.35*i)
            source=box(x0+w*.2,yy,w*.25,h*.2)
            target=box(x0+w*.83,yy,w*.16,h*.2,True)
            link(source,target,True)
    elif n==12:
        gate=box(x0+w*.58,cy,w*.16,h*.92,True)
        for i in range(3):
            yy=y0+h*(.15+.35*i)
            source=box(x0+w*.12,yy,w*.15,h*.2)
            link(source,gate,True,target_fraction=(yy-gate[1])/(gate[3]-gate[1]))
        target=box(x0+w*.89,cy,w*.16,h*.3)
        link(gate,target,True)
    elif n==13:
        nodes=[box(x0+w*(.16+.34*i),cy,w*.2,h*.4,i==1) for i in range(3)]
        link(nodes[0],nodes[1]);link(nodes[1],nodes[2])
        link(nodes[2],nodes[1],True,source_side='bottom',target_side='bottom',
             via=[(x0+w*.84,y0+h*.94),(x0+w*.5,y0+h*.94)])
    elif n==14:
        for i in range(3):
            for j in range(3):box(x0+w*(.18+.32*i),y0+h*(.15+.35*j),w*.22,h*.23,i==j)
    else:
        box(x0+w*.25,cy,w*.35,h*.65)
        box(x0+w*.75,cy,w*.35,h*.85,True)
        line((x0+w*.48,y0),(x0+w*.48,y1),True)

MOTIFS = {}
for number in range(1,16):
    def motif(d,b,c,o,n=number): return draw(n,d,b,c,o)
    MOTIFS['eng_'+str(number)] = motif
