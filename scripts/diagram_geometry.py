"""Small geometry helpers for code-drawn tutorial cover diagrams.

Connections are defined by node bounds and named ports, so an endpoint cannot
drift when a node is resized or the renderer switches from square to OG layout.
"""
import math


def port(bounds, side, fraction=.5):
    if not 0 <= fraction <= 1:
        raise ValueError('port fraction must be between zero and one')
    x0,y0,x1,y1=bounds
    if side=='left':return x0,y0+(y1-y0)*fraction
    if side=='right':return x1,y0+(y1-y0)*fraction
    if side=='top':return x0+(x1-x0)*fraction,y0
    if side=='bottom':return x0+(x1-x0)*fraction,y1
    raise ValueError('unknown node side: '+side)


def connect(draw, source, target, color, *, source_side='right', target_side='left',
            source_fraction=.5, target_fraction=.5, via=(), width=6, head=16):
    points=[port(source,source_side,source_fraction),*via,port(target,target_side,target_fraction)]
    if any(not math.isfinite(v) for point in points for v in point):
        raise ValueError('connection coordinates must be finite')
    if any(math.dist(a,b)<1 for a,b in zip(points,points[1:])):
        raise ValueError('connection contains an empty segment')
    # The tip touches the target border; the head stays outside its body.
    draw.line(points,fill=color,width=width,joint='curve')
    a,z=points[-2:];length=math.dist(a,z)
    size=min(head,length*.4)
    angle=math.atan2(z[1]-a[1],z[0]-a[0])
    bx,by=z[0]-size*math.cos(angle),z[1]-size*math.sin(angle)
    half=size*.45
    draw.polygon([z,(bx-half*math.sin(angle),by+half*math.cos(angle)),
                    (bx+half*math.sin(angle),by-half*math.cos(angle))],fill=color)
    return points
