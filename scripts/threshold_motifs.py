"""Distinct house-style diagrams for the ten Below Threshold covers."""
import math
from diagram_geometry import connect


def draw(n,d,b,c,o):
    x0,y0,x1,y1=b;w=x1-x0;h=y1-y0
    def pt(x,y):return x0+w*x,y0+h*y
    def line(points,lit=False,width=5):d.line([pt(x,y) for x,y in points],fill=c['hi'] if lit else c['ln'],width=width)
    def dot(x,y,lit=False,r=.035):
        xx,yy=pt(x,y);rr=min(w,h)*r
        d.ellipse((xx-rr,yy-rr,xx+rr,yy+rr),fill=c['hi'] if lit else c['core'])
    def box(x,y,ww,hh,lit=False):
        a=pt(x,y);z=pt(x+ww,y+hh);bounds=(*a,*z)
        d.rounded_rectangle(bounds,radius=8,fill=c['hif'] if lit else c['fill'],outline=c['hi'] if lit else c['ln'],width=4)
        return bounds
    if n==1:
        for y in (.2,.5,.8):
            line([(.1,y),(.38,y-.12),(.62,y-.12),(.9,y)],True);dot(.1,y);dot(.9,y,True)
        line([(.38,.08),(.38,.92)],False,3);line([(.62,.08),(.62,.92)],False,3)
    elif n==2:
        line([(.02,.5),(.98,.5)],False,3)
        line([(.02+.96*i/150,.5+.16*math.sin(i*.16)+(.22 if 63<i<68 else 0)) for i in range(151)],True)
        dot(.44,.16,True);line([(.44,.23),(.44,.34)],True)
    elif n==3:
        for i in range(3):
            for j in range(3):
                if i<2:line([(.2+i*.3,.2+j*.3),(.5+i*.3,.2+j*.3)],False,3)
                if j<2:line([(.2+i*.3,.2+j*.3),(.2+i*.3,.5+j*.3)],False,3)
        for i in range(3):
            for j in range(3):dot(.2+i*.3,.2+j*.3,(i+j)%2==0,.045)
        box(.3,.3,.1,.1,True);box(.6,.6,.1,.1,True)
    elif n==4:
        layers=[[(.1,y) for y in (.25,.5,.75)],[(.5,y) for y in (.12,.37,.62,.87)],[(.9,y) for y in (.35,.65)]]
        for a,z in zip(layers,layers[1:]):
            for p in a:
                for q in z:line([p,q],False,2)
        for k,layer in enumerate(layers):
            for p in layer:dot(*p,k==1,.045)
    elif n==5:
        boxes=[box(.03+(i%4)*.25,.2 if i<4 else .67,.16,.18,i in (1,4,6)) for i in range(7)]
        for i in (0,1,2,4,5):connect(d,boxes[i],boxes[i+1],c['hi'],head=10,width=4)
        line([(.86,.4),(.86,.54),(.11,.54),(.11,.67)],True,4)
    elif n==6:
        for y in (.25,.5,.75):line([(.02,y),(.98,y)],False,3)
        for x in (.2,.42,.7):
            line([(x,.25),(x,.75)],x==.7);dot(x,.25,x==.7);box(x-.035,.71,.07,.08,x==.7)
        line([(.12,.9),(.5,.08)],True,6)
    elif n==7:
        boxes=[box(.04,.1,.3,.2),box(.65,.1,.3,.2,True),box(.65,.7,.3,.2),box(.04,.7,.3,.2,True)]
        for i,source_side,target_side in ((0,'right','left'),(1,'bottom','top'),(2,'left','right'),(3,'top','bottom')):
            connect(d,boxes[i],boxes[(i+1)%4],c['hi'],source_side=source_side,target_side=target_side,head=13,width=4)
        dot(.5,.5,True,.07)
    elif n==8:
        boxes=[box(.02+i*.26,.33,.17,.34,i%2==0) for i in range(4)]
        for a,z in zip(boxes,boxes[1:]):connect(d,a,z,c['hi'],head=0,width=8)
        for i in range(4):line([(.105+i*.26,.33),(.105+i*.26,.12)],False,4)
    elif n==9:
        for i in range(5):
            y=.07+i*.19;box(.04,y,.18,.12,i==3);line([(.22,y+.06),(.53,.5)],False,3)
        gate=box(.53,.32,.18,.36,True);out=box(.84,.42,.13,.16,True)
        connect(d,gate,out,c['hi'],head=12,width=5);line([(.56,.51),(.6,.56),(.68,.42)],True,4)
    elif n==10:
        dot(.5,.1,True,.045)
        for x in (.2,.8):line([(.5,.1),(.5,.32),(x,.32),(x,.5)],True,4);dot(x,.5)
        for x in (.08,.35,.65,.92):
            parent=.2 if x<.5 else .8
            line([(parent,.5),(parent,.7),(x,.7),(x,.88)],False,3);dot(x,.88,True)


MOTIFS={'bt_'+str(n):(lambda d,b,c,o,n=n:draw(n,d,b,c,o)) for n in range(1,11)}
