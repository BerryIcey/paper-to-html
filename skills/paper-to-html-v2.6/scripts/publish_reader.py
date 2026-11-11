"""Publish one current local-service reader, overwriting its stable destination."""
from pathlib import Path
from html.parser import HTMLParser
import re,os
from teaching_contract import check_reader_html
from teaching_fidelity import require_fidelity

class Resources(HTMLParser):
    def __init__(self):super().__init__();self.external=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        value=a.get('src') if tag in ('img','script','iframe','video','audio') else a.get('href') if tag=='link' and a.get('rel')=='stylesheet' else None
        if value and not value.startswith('data:'):self.external.append(value)

def atomic_text(path,text):
    temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(text,'utf-8');os.replace(temp,path)

def publish(root,source,title,desktop=None,teaching_baseline=None):
    if desktop is not None:
        raise ValueError('Separate desktop HTML copies are no longer published; use a shortcut to the local reading address')
    root=Path(root).resolve();root.mkdir(parents=True,exist_ok=True);source=Path(source).resolve()
    content=source.read_text('utf-8')
    if '<body' not in content:raise ValueError('HTML requires body')
    teaching_errors,_=check_reader_html(content)
    if teaching_errors:raise ValueError('\n'.join(teaching_errors))
    resources=Resources();resources.feed(content)
    if resources.external:raise ValueError('Publish requires embedded reader resources: '+', '.join(resources.external[:3]))
    pdf=root/'source-paper.pdf'
    if 'href="source-paper.pdf"' in content:
        if not pdf.is_file():raise ValueError('Source PDF link has no PDF file')
    # Stable current file only. Retired settings/archives are neither read nor pruned.
    content=re.sub(r' data-(?:reader-release|backup-count)="[^"]*"','',content)
    require_fidelity(content,teaching_baseline)
    latest=root/'paper-reading.html'
    atomic_text(latest,content)
    return latest

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--source',required=True);p.add_argument('--title',required=True);p.add_argument('--desktop',help=argparse.SUPPRESS);p.add_argument('--teaching-baseline');a=p.parse_args();print(publish(a.root,a.source,a.title,a.desktop,a.teaching_baseline))
