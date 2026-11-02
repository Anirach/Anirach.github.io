"""Content versions for repaired images, preserving their canonical filenames."""
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ROOT=Path(__file__).resolve().parents[1]
VERSIONS=ROOT/'scripts/image-versions.json'
IMAGE_URL=re.compile(r'(?:https://anirach\.com/|\.\./|/)images/[^\s\"\'<>),]+')


def versions():
    return json.loads(VERSIONS.read_text()) if VERSIONS.exists() else {}


def version_url(url, revisions=None):
    revisions=versions() if revisions is None else revisions
    parsed=urlsplit(url)
    revision=revisions.get(Path(parsed.path).name)
    if not revision:return url
    query=dict(parse_qsl(parsed.query));query['v']=revision
    return urlunsplit((parsed.scheme,parsed.netloc,parsed.path,urlencode(query),parsed.fragment))


def version_markup(markup):
    revisions=versions()
    return IMAGE_URL.sub(lambda m:version_url(m.group(0),revisions),markup)


def refresh_versions(paths):
    revisions=versions()
    for path in paths:
        path=Path(path)
        revisions[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()[:12]
    VERSIONS.write_text(json.dumps(dict(sorted(revisions.items())),indent=2)+'\n')
