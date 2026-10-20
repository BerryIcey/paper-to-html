"""Assemble paper content with fixed reader components. Python standard library."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import argparse
from urllib.parse import urlsplit
from teaching_contract import check_reader_html
import json
from concept_markup import mark_concepts
from legend_config import render_legend
class Check(HTMLParser):
    def __init__(self): super().__init__(); self.ids=[]; self.links=[]; self.sections=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.append(a['id'])
        if tag=='a' and a.get('href','').startswith('#'): self.links.append(a['href'][1:])
        if tag=='section' and 'data-section' in a: self.sections+=1
p=argparse.ArgumentParser();p.add_argument('--content',type=Path,required=True);p.add_argument('--paper-id',required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--reader-url');p.add_argument('--concepts',type=Path);p.add_argument('--concept-report',type=Path);args=p.parse_args()
if args.reader_url:
    u=urlsplit(args.reader_url)
    if u.scheme!='http' or u.hostname not in ('127.0.0.1','localhost') or u.username or u.password: raise SystemExit('reader-url must be the current loopback HTTP reader')
a=Path(__file__).resolve().parents[1]/'assets/reader-components';content=args.content.read_text('utf-8');manifest={}
if args.concepts:
    manifest=json.loads(args.concepts.read_text('utf-8'))
    content,concept_report=mark_concepts(content,manifest)
    if args.concept_report:
        args.concept_report.parent.mkdir(parents=True,exist_ok=True)
        args.concept_report.write_text(json.dumps(concept_report,ensure_ascii=False,indent=2),'utf-8')
elif args.concept_report:raise SystemExit('--concept-report requires --concepts')
c=Check();c.feed(content)
if not c.sections or len(c.ids)!=len(set(c.ids)) or set(c.links)-set(c.ids): raise SystemExit('Content requires sections, unique ids, and valid internal links')
teaching_errors,_=check_reader_html(content)
if teaching_errors:raise SystemExit('\n'.join(teaching_errors))
s=(a/'shell.html').read_text('utf-8').replace('replace-with-unique-paper-id',escape(args.paper_id,quote=True))
legend,legend_css=render_legend(manifest,content)
import re
s=re.sub(r'<div class="reader-legend-grid">.*?</div>',lambda _:legend,s,count=1,flags=re.S)
if args.reader_url:s=s.replace('<body','<body data-reader-url="'+escape(args.reader_url,quote=True)+'"',1)
s=s.replace('<!--由论文内容替换：section[data-section]与稳定id；图文面板按components.md生成-->',content)
s=s.replace('<link rel="stylesheet" href="reader.css">','<style>'+(a/'reader.css').read_text('utf-8')+legend_css+'</style>')
s=s.replace('<script src="reader.js"></script>','<script>'+(a/'reader.js').read_text('utf-8')+'</script>')
c=Check();c.feed(s)
if len(c.ids)!=len(set(c.ids)): raise SystemExit('Content collides with component ids')
args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(s,'utf-8');print(args.out)
