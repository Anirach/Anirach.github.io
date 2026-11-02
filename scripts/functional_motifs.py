"""Original functional-workflow cover motifs, kept within the house renderer."""
from diagram_geometry import connect

def draw(n,d,b,c,o):
 x0,y0,x1,y1=b;w=x1-x0;h=y1-y0
 def box(x,y,ww,hh,lit=False):
  bounds=(x-ww/2,y-hh/2,x+ww/2,y+hh/2)
  d.rounded_rectangle(bounds,radius=10,fill=c['core'] if lit else c['fill'],outline=c['hi'] if lit else c['ln'],width=6)
  return bounds
 def line(a,z,lit=False):d.line((a,z),fill=c['hi'] if lit else c['ln'],width=6)
 def link(a,z,lit=False,**kwargs):return connect(d,a,z,c['hi'] if lit else c['ln'],head=max(10,h*.035),**kwargs)
 if n==1:
  nodes=[box(x0+w*(.14+.36*k),y0+h*.5,w*.2,h*.45,k==1) for k in range(3)]
  link(nodes[0],nodes[1]);link(nodes[1],nodes[2])
 elif n==2:
  for k in range(3):box(x0+w*.5,y0+h*(.2+.3*k),w*(.75-.15*k),h*.2,k==1)
 elif n in [3,7]:
  for k in range(4):box(x0+w*(.12+.25*k),y0+h*.5,w*.13,h*(.35+.12*k),k==(0 if n==3 else 3))
 elif n in [4,8]:
  source=box(x0+w*.2,y0+h*.5,w*.25,h*.6)
  for k in range(3):
   yy=y0+h*(.15+.35*k);target=box(x0+w*.84,yy,w*.2,h*.21,k==1);link(source,target,k==1)
 elif n==5:
  gate=box(x0+w*.5,y0+h*.5,w*.32,h*.85,True)
  start=(x0+w*.05,y0+h*.5,x0+w*.05,y0+h*.5)
  link(start,gate)
  line((gate[2],y0+h*.5),(x0+w*.7,y0+h*.5),True)
  line((x0+w*.7,y0),(x0+w*.7,y1))
 elif n==6:
  for k,v in enumerate([.3,.7,.48,.9]):box(x0+w*(.15+.23*k),y1-h*v/2,w*.12,h*v,k==3)
 elif n==9:
  for k in range(3):
   yy=y0+h*(.2+.3*k);box(x0+w*.25,yy,w*.22,h*.2,k==2);line((x0+w*.43,yy),(x0+w*.9,yy),k==2)
 elif n==10:
  nodes=[box(x0+w*(.1+.2*k),y0+h*(.3 if k%2 else .7),w*.12,h*.24,k==4) for k in range(5)]
  link(nodes[1],nodes[3]);link(nodes[0],nodes[2],True);link(nodes[2],nodes[4],True)
 elif n==11:
  for k in range(3):box(x0+w*(.17+.33*k),y0+h*.5,w*.22,h*(.45+.18*k),k==2)
 else:
  source=box(x0+w*.2,y0+h*.5,w*.22,h*.6);target=box(x0+w*.72,y0+h*.5,w*.35,h*.85,True)
  link(source,target);line((x0+w*.42,y0),(x0+w*.42,y1))
MOTIFS={}
for n in range(1,13):
 def motif(d,b,c,o,n=n):return draw(n,d,b,c,o)
 MOTIFS['fn_'+str(n)]=motif
