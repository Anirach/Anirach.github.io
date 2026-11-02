"""Inventory tutorial image references and create review contact sheets.

Internal QA only. Run from any directory. --remote probes HTTPS with curl's
normal certificate verification; --sheets prepares crops for visual review.
"""
import argparse
import concurrent.futures
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urljoin, urlsplit

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
BASE = 'https://anirach.com'


class ImageReferences(HTMLParser):
    """Inspect real elements; sample code and comments are not page resources."""
    def __init__(self):
        super().__init__();self.values=[];self.images=[];self.in_style=False

    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='img' and a.get('src'):
            self.values.append(a['src']);self.images.append(a['src'])
        if tag in ('img','source') and a.get('srcset'):
            self.values.extend(x.strip().split()[0] for x in a['srcset'].split(','))
        if tag=='video' and a.get('poster'):self.values.append(a['poster'])
        if tag=='meta' and a.get('property',a.get('name')) in ('og:image','twitter:image'):
            self.values.append(a['content'])
        if a.get('style'):self.css(a['style'])
        if tag=='style':self.in_style=True

    def handle_endtag(self,tag):
        if tag=='style':self.in_style=False

    def handle_data(self,data):
        if self.in_style:self.css(data)

    def css(self,text):
        self.values.extend(re.findall(r'url\([\'"]?([^\)\'" ]+)[\'"]?\)',text))


def inventory():
    catalog = (ROOT/'blog/index.html').read_text()
    posts = re.findall(r'<a href="([a-z0-9-]+\.html)" class="card">', catalog)
    refs, covers, figures = {}, [], []
    for rel in ['index.html']+posts:
        source = (ROOT/'blog'/rel).read_text()
        parser=ImageReferences();parser.feed(source)
        for value in parser.values:
            url = urljoin(BASE+'/blog/'+rel,value)
            if urlsplit(url).netloc != 'anirach.com':
                continue
            path = urlsplit(url).path.lstrip('/')
            refs.setdefault(path,[]).append(rel)
        if rel != 'index.html':
            for value in parser.images:
                path=urlsplit(urljoin(BASE+'/blog/'+rel,value)).path.lstrip('/')
                if '-cover.' in path and path not in covers:
                    covers.append(path)
                elif '-cover.' not in path and path not in figures:
                    figures.append(path)
    return posts,refs,covers,figures


def sheets(items,name,crop=False):
    columns, rows = (4,6) if crop else (3,5)
    tilew,tileh = (350,190) if crop else (460,310)
    f=ImageFont.truetype(str(ROOT/'scripts/fonts/Inter-var.ttf'),14)
    for start in range(0,len(items),columns*rows):
        subset=items[start:start+columns*rows]
        im=Image.new('RGB',(columns*tilew,rows*tileh),'white');d=ImageDraw.Draw(im)
        for i,path in enumerate(subset):
            x=(i%columns)*tilew;y=(i//columns)*tileh
            pic=Image.open(ROOT/path).convert('RGB')
            if crop:
                w,h=pic.size;pic=pic.crop((int(w*.1),int(h*.4),int(w*.9),int(h*.69)))
            pic.thumbnail((tilew-16,tileh-46))
            im.paste(pic,(x+(tilew-pic.width)//2,y+8))
            title=Path(path).stem.replace('-cover','').replace('ai-engineering-','eng-')
            d.text((x+8,y+tileh-35),title[:49],font=f,fill='#11304b')
            d.line((x,y+tileh-1,x+tilew,y+tileh-1),fill='#dddddd')
        im.save(OUT/f'{name}-{start//(columns*rows)+1:02d}.jpg',quality=90)


def probe(path):
    p=subprocess.run(['curl','-sS','-I','-L','--retry','1','--retry-delay','1','--max-time','25','--write-out','%{http_code}',BASE+'/'+path],capture_output=True,text=True)
    code=p.stdout.strip().splitlines()[-1] if p.stdout else ''
    return {'path':path,'status':code,'ok':p.returncode==0 and code=='200','error':p.stderr.strip() or None}


def main():
    p=argparse.ArgumentParser();p.add_argument('--sheets',action='store_true');p.add_argument('--remote',action='store_true');a=p.parse_args()
    posts,refs,covers,figures=inventory()
    missing=[];decode=[]
    for path in refs:
        target=ROOT/path
        if not target.exists():missing.append(path);continue
        if target.suffix!='.svg':
            try:
                with Image.open(target) as im:im.verify()
            except Exception as e:decode.append({'path':path,'error':str(e)})
    report={'posts':len(posts),'unique_images':len(refs),'covers':len(covers),'figures':len(figures),
            'missing':missing,'decode_errors':decode,'references':refs}
    (OUT/'inventory.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
    print({k:v for k,v in report.items() if k!='references'})
    if a.sheets:
        sheets(covers,'cover-motifs',True);sheets(figures,'figures')
    if a.remote:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:results=list(pool.map(probe,refs))
        (OUT/'remote.json').write_text(json.dumps(results,indent=2))
        print('Remote images:',len(results),'failed:',[x for x in results if not x['ok']])


if __name__=='__main__':main()
