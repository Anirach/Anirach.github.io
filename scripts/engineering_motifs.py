"""Fifteen original diagrams-in-miniature for the engineering course covers."""
def draw(n, d, b, c, o):
    x0, y0, x1, y1 = b
    w, h = x1-x0, y1-y0
    def box(x, y, ww, hh, lit=False):
        d.rounded_rectangle((x-ww/2, y-hh/2, x+ww/2, y+hh/2), radius=12,
                            fill=c['core'] if lit else c['fill'],
                            outline=c['hi'] if lit else c['ln'], width=6)
    def line(a,z,lit=False):
        d.line((a,z), fill=c['hi'] if lit else c['ln'], width=7)
    cy=y0+h*.5
    if n==1:
        for i in range(3):
            box(x0+w*(.15+.35*i),cy,w*.23,h*(.35+.2*i),i==2)
        line((x0+w*.27,cy),(x0+w*.36,cy));line((x0+w*.63,cy),(x0+w*.72,cy))
    elif n==2:
        box(x0+w*.5,cy,w*.86,h*.86)
        box(x0+w*.5,cy,w*.5,h*.45,True)
        for i in range(4):line((x0+w*(.18+.21*i),y0),(x0+w*(.18+.21*i),y0+h*.17))
    elif n==3:
        for i in range(4):
            xx=x0+w*(.12+.25*i); yy=y0+h*(.25 if i%2==0 else .75)
            box(xx,yy,w*.17,h*.26,i==3)
            if i:line((xx-w*.16,cy),(xx,yy))
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
        box(x0+w*.2,cy,w*.25,h*.5)
        for i in range(3):
            yy=y0+h*(.12+.38*i);line((x0+w*.35,cy),(x0+w*.75,yy),i==1)
            box(x0+w*.85,yy,w*.15,h*.2,i==1)
    elif n==8:
        box(x0+w*.5,cy,w*.25,h*.9,True)
        line((x0+w*.05,cy),(x0+w*.34,cy))
        line((x0+w*.66,cy),(x0+w*.95,cy))
        box(x0+w*.5,cy,w*.08,h*.2)
    elif n==9:
        for i in range(3):box(x0+w*(.35+.13*i),y0+h*(.3+.19*i),w*.55,h*.45,i==2)
    elif n==11:
        for i in range(3):
            yy=y0+h*(.15+.35*i);box(x0+w*.2,yy,w*.25,h*.2)
            line((x0+w*.37,yy),(x0+w*.7,yy),True)
            box(x0+w*.83,yy,w*.16,h*.2,True)
    elif n==12:
        for i in range(3):
            yy=y0+h*(.15+.35*i);line((x0+w*.05,yy),(x0+w*.55,yy),True)
        box(x0+w*.68,cy,w*.15,h*.92,True);box(x0+w*.92,cy,w*.12,h*.3)
    elif n==13:
        for i in range(3):box(x0+w*(.16+.34*i),cy,w*.2,h*.4,i==1)
        line((x0+w*.84,cy+h*.25),(x0+w*.84,y1),True)
        line((x0+w*.84,y1),(x0+w*.5,y1),True)
        line((x0+w*.5,y1),(x0+w*.5,cy+h*.25),True)
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
