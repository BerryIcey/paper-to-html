"""Publish standalone readers; preserve current + selected historical releases."""
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime,timezone,timedelta
import json,re,os,hashlib,base64
from teaching_contract import check_reader_html

class Resources(HTMLParser):
    def __init__(self):super().__init__();self.external=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        value=a.get('src') if tag in ('img','script','iframe','video','audio') else a.get('href') if tag=='link' and a.get('rel')=='stylesheet' else None
        if value and not value.startswith('data:'):self.external.append(value)

def atomic_text(path,text):
    temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(text,'utf-8');os.replace(temp,path)

def publish(root,source,title,desktop=None):
    root=Path(root).resolve();root.mkdir(parents=True,exist_ok=True);source=Path(source).resolve()
    policy_path=root/'reader-settings.json'
    policy=json.loads(policy_path.read_text('utf-8')) if policy_path.exists() else {}
    count=policy.get('backup_count')
    if count is not None and (type(count) is not int or count not in (0,1,2)):raise ValueError('backup_count must be 0, 1 or 2')
    manifest=root/'reader-versions.json'
    data=json.loads(manifest.read_text('utf-8')) if manifest.exists() else {'sequence':0,'releases':[]}
    stamp=datetime.now(timezone(timedelta(hours=8)))
    content=source.read_text('utf-8')
    if '<body' not in content:raise ValueError('HTML requires body')
    teaching_errors,_=check_reader_html(content)
    if teaching_errors:raise ValueError('\n'.join(teaching_errors))
    resources=Resources();resources.feed(content)
    if resources.external:raise ValueError('Publish requires embedded offline resources: '+', '.join(resources.external[:3]))
    pdf=root/'source-paper.pdf'
    if 'href="source-paper.pdf"' in content:
        if not pdf.is_file():raise ValueError('Source PDF link has no PDF file')
        content=content.replace('href="source-paper.pdf"','href="data:application/pdf;base64,'+base64.b64encode(pdf.read_bytes()).decode()+'" download="source-paper.pdf"')
    seq=data['sequence']+1
    label=(f'v{seq}.0' if count is not None else '工作版 · 尚未正式编号')+f' · {stamp:%Y-%m-%d %H:%M} 北京时间'
    content=re.sub(r' data-reader-release="[^"]*"| data-backup-count="[^"]*"','',content)
    attributes=' data-reader-release="'+label+'"'+(f' data-backup-count="{count}"' if count is not None else '')
    content=content.replace('<body','<body'+attributes,1)
    latest=root/'paper-reading.html'
    folder=root/'versions'
    if count is not None:
        folder.mkdir(exist_ok=True)
        short=re.sub(r'[<>:"/\\|?*\x00-\x1f]','',title).strip()[:60] or '论文'
        dest=folder/f'{short}_v{seq}.0_{stamp:%Y-%m-%d_%H%M%S}.html'
        atomic_text(dest,content)
    else:dest=latest
    # Synchronize desktop before committing the release manifest or pruning old files.
    if desktop:
        share=Path(desktop).expanduser().resolve();share.parent.mkdir(parents=True,exist_ok=True);atomic_text(share,content)
    atomic_text(latest,content)
    if count is None:return dest
    rows=data['releases']+[{'file':dest.name,'version':f'v{seq}.0','time':stamp.isoformat(),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}]
    removed=rows[:max(0,len(rows)-count-1)];rows=rows[-(count+1):]
    atomic_text(manifest,json.dumps({'sequence':seq,'releases':rows,'backup_count':count},ensure_ascii=False,indent=2))
    for row in removed:
        target=(folder/row['file']).resolve()
        if target.parent==folder.resolve() and target.suffix=='.html' and target.is_file():target.unlink()
    return dest

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--source',required=True);p.add_argument('--title',required=True);p.add_argument('--desktop');a=p.parse_args();print(publish(a.root,a.source,a.title,a.desktop))
