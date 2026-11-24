"""Seven distinct code-native cover motifs for the quantum series."""
import math
from diagram_geometry import connect


def draw(n,d,b,c,o):
    x0,y0,x1,y1=b;w=x1-x0;h=y1-y0
    def pt(x,y):return (x0+w*x,y0+h*y)
    def line(points,lit=False,width=6):d.line([pt(x,y) for x,y in points],fill=c['hi'] if lit else c['ln'],width=width)
    def dot(x,y,lit=False,r=.035):
        xx,yy=pt(x,y);rr=min(w,h)*r
        d.ellipse((xx-rr,yy-rr,xx+rr,yy+rr),fill=c['hi'] if lit else c['core'])
    if n==1:
        for row,phase in ((.3,0),(.72,math.pi)):
            points=[(.02+.96*i/120,row+.16*math.sin(2*math.pi*i/120+phase)) for i in range(121)]
            line(points,True)
        line([(.5,.04),(.5,.96)],False,3)
    elif n==2:
        for i in range(12):
            xx=.04+i*.08;top=.08 if i==8 else .72
            a=pt(xx,top);z=pt(xx+.045,.94)
            d.rounded_rectangle((*a,*z),radius=4,fill=c['hi'] if i==8 else c['dimf'],outline=c['ln'],width=3)
        line([(.02,.95),(.98,.95)],False,3)
    elif n==3:
        ys=[.85,.42,.67,.12]*3
        line([(.04+i*.083,yy) for i,yy in enumerate(ys)])
        for i,yy in enumerate(ys):dot(.04+i*.083,yy,i%4==0,.03)
    elif n==4:
        boxes=[]
        for xx,yy,ww,hh in ((.1,.26,.22,.48),(.43,.12,.18,.76),(.74,.26,.22,.48)):
            a=pt(xx,yy);z=pt(xx+ww,yy+hh);r=(*a,*z);boxes.append(r)
            d.rounded_rectangle(r,radius=7,outline=c['ln'],fill=c['hif'] if len(boxes)==2 else c['fill'],width=5)
        connect(d,boxes[0],boxes[1],c['hi'],head=12);connect(d,boxes[1],boxes[2],c['hi'],head=12)
    elif n==5:
        nodes=[(.38,.08),(.12,.78),(.67,.78),(.65,.24),(.39,.94),(.94,.94)]
        for a,z in [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)]:line([nodes[a],nodes[z]],(a+z)%2==1,5)
        for i,p in enumerate(nodes):dot(*p,i%2==0,.055)
    elif n==6:
        for row in (.25,.75):
            line([(.02,row),(.98,row)],False,4)
            for xx in (.2,.5,.8):
                a=pt(xx-.055,row-.14);z=pt(xx+.055,row+.14)
                d.rounded_rectangle((*a,*z),radius=5,fill=c['hif'],outline=c['hi'],width=4)
        for xx in (.35,.65):line([(xx,.25),(xx,.75)],True,4);dot(xx,.25);dot(xx,.75)
    elif n==7:
        widths=[.35,.55,.82]
        for i,ww in enumerate(widths):
            a=pt(.08,.08+i*.31);z=pt(.08+ww,.29+i*.31)
            d.rounded_rectangle((*a,*z),radius=6,fill=c['hi'] if i==2 else c['fill'],outline=c['ln'],width=4)
        line([(.94,.04),(.94,.98)],False,3)


MOTIFS={'qp_'+str(n):(lambda d,b,c,o,n=n:draw(n,d,b,c,o)) for n in range(1,8)}
