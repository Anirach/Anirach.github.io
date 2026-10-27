"""Ten original Jev-lab motifs for the existing cover renderer."""
import math

def draw(n,d,b,c,o):
    x0,y0,x1,y1=b;w=x1-x0;h=y1-y0;cy=(y0+y1)/2
    def rect(x,y,ww,hh,lit=False):
        d.rounded_rectangle((x-ww/2,y-hh/2,x+ww/2,y+hh/2),radius=int(h*.08),fill=c['core'] if lit else c['fill'],outline=c['hi'] if lit else c['ln'],width=6)
    def line(a,z,hi=False):d.line((a,z),fill=c['hi'] if hi else c['ln'],width=7)
    def dot(x,y,r,hi=False):d.ellipse((x-r,y-r,x+r,y+r),fill=c['hi'] if hi else c['core'])
    if n==1: # workbench: terminal window and decision cartridge
        rect(x0+w*.3,cy,w*.42,h*.8);line((x0+w*.12,cy-h*.15),(x0+w*.48,cy-h*.15));line((x0+w*.16,cy),(x0+w*.23,cy+h*.1));line((x0+w*.23,cy+h*.1),(x0+w*.16,cy+h*.2));rect(x0+w*.78,cy,w*.25,h*.65,True)
    elif n==2: # paired baseline lanes
        for k in range(2):
            yy=y0+h*(.27+.46*k);line((x0+w*.1,yy),(x0+w*.85,yy));rect(x0+w*(.35+.25*k),yy,w*.24,h*.27,k==1)
    elif n==3: # typed fan-out
        rect(x0+w*.15,cy,w*.18,h*.6,True)
        for k in range(3):yy=y0+h*(.14+.36*k);line((x0+w*.26,cy),(x0+w*.68,yy));rect(x0+w*.8,yy,w*.24,h*.24)
    elif n==4: # schema gate and accepted fields
        rect(x0+w*.5,cy,w*.36,h*.92,True)
        for k in range(3):yy=y0+h*(.22+.28*k);line((x0+w*.07,yy),(x0+w*.28,yy));dot(x0+w*.81,yy,h*.06,k==1)
    elif n==5: # abstention fork
        dot(x0+w*.4,cy,h*.18,True)
        for k in range(3):yy=y0+h*(.15+.35*k);line((x0+w*.45,cy),(x0+w*.8,yy),k==1);dot(x0+w*.84,yy,h*.075,k==1)
    elif n==6: # disjoint holdout blocks
        for k in range(3):rect(x0+w*(.18+.32*k),cy,w*.22,h*(.5+.18*k),k==2)
    elif n==7: # effect boundary: closed barrier and separate key
        line((x0+w*.5,y0),(x0+w*.5,y1));rect(x0+w*.26,cy,w*.24,h*.5);rect(x0+w*.76,cy,w*.24,h*.5,True);dot(x0+w*.44,y0+h*.18,h*.08,True)
    elif n==8: # broken connection: attack + containment
        for k in range(4):rect(x0+w*(.12+.25*k),cy,w*.13,h*.4,k==2)
        line((x0+w*.22,cy),(x0+w*.28,cy));line((x0+w*.5,cy-h*.15),(x0+w*.58,cy+h*.15),True)
    elif n==9: # latency distribution and cost ledger
        for k,hh in enumerate([.22,.46,.83,.55,.3]):rect(x0+w*(.1+.1*k),y1-hh*h/2,w*.06,hh*h,k==2)
        rect(x0+w*.82,cy,w*.23,h*.82);line((x0+w*.75,cy),(x0+w*.9,cy))
    else: # release boxes and shadow track
        for k in range(3):rect(x0+w*(.16+.34*k),cy,w*.2,h*.65,k==2)
        line((x0+w*.16,y1),(x0+w*.84,y1),True)

MOTIFS={}
for number,name in enumerate(['workbench','baseline','questions','schema','abstain','holdout','guard','attacks','cost','release'],1):
    def motif(d,b,c,o,n=number):return draw(n,d,b,c,o)
    MOTIFS['jv_'+name]=motif
