"""Validate the static portfolio without third-party dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
root = Path(__file__).resolve().parents[1]
class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids = set(); self.local = []; self.fragments = []; self.errors = []; self.heading_count = 0; self.video_ids = set(); self.categories = {}; self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids: self.errors.append('Duplicate id: ' + a['id'])
            self.ids.add(a['id'])
        if tag == 'h1': self.heading_count += 1
        if tag == 'img':
            if 'alt' not in a: self.errors.append('Image missing alt: ' + a.get('src', ''))
            if not all(k in a for k in ['width', 'height']): self.errors.append('Image missing dimensions: ' + a.get('src', ''))
            if 'profile' in a.get('src', ''): self.errors.append('Personal portrait present')
        if 'data-video' in a: self.video_ids.add(a['data-video'])
        if 'data-category' in a: self.categories[a['data-category']] = self.categories.get(a['data-category'], 0) + 1
        if tag == 'a' and a.get('target') == '_blank' and 'noopener' not in a.get('rel',''): self.errors.append('External link missing noopener')
        for key in ['src', 'href', 'data-graphic']:
            value = a.get(key, '')
            if not value: continue
            if value.startswith('#'): self.fragments.append(value[1:]); continue
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc: continue
            self.local.append(unquote(parsed.path))
p = SiteParser(); p.feed((root/'index.html').read_text())
for file in set(p.local):
    if not (root/file).is_file(): p.errors.append('Missing file: ' + file)
for fragment in p.fragments:
    if fragment not in p.ids: p.errors.append('Missing anchor: ' + fragment)
if p.heading_count != 1: p.errors.append('Expected one h1')
expected = {'t2UfAnDebfo','yOVhuCKtams','y9YaJLOLpq8','ZAl17OtuZ2I','lpftOO7GkgQ','rGNWl_Wt4Aw','HJYRQWEnPnE','JMZIBYHA0cI','N5bW5uU-H2Q'}
if p.video_ids != expected: p.errors.append('Supplied video set does not match')
if '6819126241' in (root/'index.html').read_text(): p.errors.append('Unfinished app featured')
print(json.dumps({'passed': not p.errors, 'errors':p.errors,'unique_local_assets':len(set(p.local)),'videos':len(p.video_ids),'gallery_categories':p.categories},indent=2))
raise SystemExit(bool(p.errors))
