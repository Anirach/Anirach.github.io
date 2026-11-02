"""Regression checks for the reported connector defect and image-cache refresh.

Exercise actual motif renderers in square and landscape bounds. Check that
every connection endpoint lies on its declared node border and its interior
does not enter either node. Also verify every repaired HTML image URL carries
the hash of the actual asset, including each srcset candidate and share card.
"""
import importlib
import json
import math
from pathlib import Path
import sys
from urllib.parse import parse_qs,urlsplit
from unittest.mock import patch

from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import diagram_geometry
from image_assets import version_markup,version_url,versions
import make_cover


def on_border(point,node):
    x,y=point;l,t,r,b=node
    return ((math.isclose(x,l) or math.isclose(x,r)) and t<=y<=b
            or (math.isclose(y,t) or math.isclose(y,b)) and l<=x<=r)


def inside(point,node):
    x,y=point;l,t,r,b=node
    # Floating point roundoff at a border is not a body intersection.
    return l+1e-6<x<r-1e-6 and t+1e-6<y<b-1e-6


def geometry_check():
    count=0
    for name,limit in [('engineering_motifs',15),('functional_motifs',12),('jev_motifs',10)]:
        module=importlib.import_module(name)
        for n in range(1,limit+1):
            for bounds in [(224,664,1408,1080),(624,189,1158,453)]:
                d=ImageDraw.Draw(Image.new('RGB',(1600,1200),'white'),'RGBA')
                original=diagram_geometry.connect
                def record(draw,source,target,color,**kwargs):
                    nonlocal count
                    points=original(draw,source,target,color,**kwargs)
                    assert on_border(points[0],source),(name,n,'source',points)
                    assert on_border(points[-1],target),(name,n,'target',points)
                    for a,z in zip(points,points[1:]):
                        for step in range(1,100):
                            p=(a[0]+(z[0]-a[0])*step/100,a[1]+(z[1]-a[1])*step/100)
                            assert not inside(p,source),(name,n,'source body',points)
                            assert not inside(p,target),(name,n,'target body',points)
                    assert all(bounds[0]<=x<=bounds[2] and bounds[1]<=y<=bounds[3] for x,y in points)
                    count+=1
                    return points
                with patch.object(module,'connect',record):
                    module.draw(n,d,bounds,make_cover.ink('cloud','blue'),{})
    return count


def cache_check():
    import hashlib
    revisions=versions()
    assert len(revisions)==57
    for name,digest in revisions.items():
        assert hashlib.sha256((ROOT/'images'/name).read_bytes()).hexdigest()[:12]==digest,name
        url='../images/'+name
        assert version_url(version_url(url))==version_url(url),'versioning is not idempotent'
    changed=json.loads((Path(__file__).parent/'changed.json').read_text())
    from audit import ImageReferences
    count=0
    for slug in ['index']+changed:
        markup=(ROOT/'blog'/(slug+'.html')).read_text()
        parser=ImageReferences();parser.feed(markup)
        for url in parser.values:
            parsed=urlsplit(url);name=Path(parsed.path).name
            if name in revisions:
                assert parse_qs(parsed.query).get('v')==[revisions[name]],(slug,url)
                count+=1
        assert version_markup(markup)==markup,('unversioned repaired image',slug)
    return count


if __name__=='__main__':
    print('PASS:',geometry_check(),'connections in 74 square/landscape motif renders')
    print('PASS:',cache_check(),'versioned image references; 57 content hashes')
