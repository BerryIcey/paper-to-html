"""Render an audited article-local concept manifest; does not discover or explain terms."""
import argparse,html,json,re,unicodedata
from html.parser import HTMLParser
from pathlib import Path
from legend_config import categories

VOID={'img','br','hr','input','meta','link','source','area','base','col','embed','param','track','wbr'}
SKIP={'a','script','style','code','pre','math','svg','nav','button','textarea','select','summary','head'}
LEAVES={'p','li','td'}
DASHES='‐‑‒–—−'

def normalized(text):
 result=[];positions=[]
 for i,char in enumerate(text):
  part=unicodedata.normalize('NFKC',char)
  for c in part:
   if c in DASHES:c='-'
   if c.isspace():c=' '
   if c==' ' and result and result[-1]==' ':continue
   result.append(c);positions.append(i)
 return ''.join(result),positions

class Targets(HTMLParser):
 def __init__(self):super().__init__();self.stack=[];self.targets=set();self.leaves=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);inside=any(self.stack) or 'data-reader-card' in a
  if inside and a.get('id'):self.targets.add(a['id'])
  if tag in LEAVES and a.get('id'):self.leaves.add(a['id'])
  if tag not in VOID:self.stack.append(inside)
 def handle_endtag(self,tag):
  if tag not in VOID and self.stack:self.stack.pop()

def prepare(manifest,targets,leaves):
 allowed={c['id']for c in categories(manifest)}|{'neutral'}
 records=manifest.get('concepts')
 if not isinstance(records,list):raise ValueError('concepts must be an article-local list')
 ids=set();aliases={};active=[]
 for row in records:
  id=row.get('id')
  if not isinstance(id,str) or not re.fullmatch(r'[A-Za-z0-9_.-]+',id) or id in ids:raise ValueError('concept IDs must be unique stable tokens')
  ids.add(id)
  if row.get('decision') not in {'core','local','identity','excluded','unresolved'}:raise ValueError('concept decision required')
  if row['decision'] in {'excluded','unresolved'}:continue
  if row.get('category') not in allowed:raise ValueError('unknown article category; use neutral if unresolved type')
  if row.get('target') not in targets:raise ValueError('concept target must be an existing card or child: '+id)
  names=row.get('aliases')
  if not isinstance(names,list) or not names or any(not isinstance(n,str) or not n.strip() for n in names):raise ValueError('selected concept requires aliases: '+id)
  scope=row.get('scope_ids')
  if scope is not None and (not isinstance(scope,list) or not scope or not set(scope)<=leaves):raise ValueError('scope_ids must identify existing text blocks: '+id)
  active.append(row)
  for name in names:
   key=normalized(name)[0]
   if key not in aliases:aliases[key]=[]
   if all(r['id']!=id for r in aliases[key]):aliases[key].append(row)
 for name,rows in aliases.items():
  for i,a in enumerate(rows):
   for b in rows[i+1:]:
    if not a.get('scope_ids') or not b.get('scope_ids') or set(a['scope_ids'])&set(b['scope_ids']):
     raise ValueError('ambiguous alias requires disjoint block scopes: '+name)
 return active,aliases

def boundary(text,start,end,name):
 # CJK-adjacent English is valid; partial ASCII identifiers/compounds are not.
 ident=lambda c:c.isascii() and (c.isalnum() or c in '_-')
 if name[0].isascii() and name[0].isalnum() and start and ident(text[start-1]):return False
 if name[-1].isascii() and name[-1].isalnum() and end<len(text) and ident(text[end]):return False
 return True

class Marker(HTMLParser):
 def __init__(self,aliases):
  super().__init__(convert_charrefs=False);self.aliases=aliases;self.stack=[];self.out=[];self.seen=set();self.counts={}
  names=sorted(aliases,key=lambda n:-len(n));self.pattern=re.compile('|'.join(map(re.escape,names))) if names else None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);skip=tag in SKIP or 'data-reader-card' in a or a.get('id')=='reader-dock'
  if tag in LEAVES:self.seen=set()
  if tag=='a' and a.get('data-concept-id'):
   id=a['data-concept-id'];self.seen.add(id);self.counts[id]=self.counts.get(id,0)+1
  self.out.append(self.get_starttag_text())
  if tag not in VOID:self.stack.append((tag,a,skip))
 def handle_startendtag(self,tag,attrs):self.out.append(self.get_starttag_text())
 def handle_endtag(self,tag):
  self.out.append('</'+tag+'>')
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==tag:del self.stack[i:];break
 def handle_data(self,text):
  leaf=next((a for tag,a,_ in reversed(self.stack) if tag in LEAVES),None)
  if not self.pattern or leaf is None or any(s for _,_,s in self.stack):self.out.append(text);return
  norm,pos=normalized(text);cursor=0;out=[]
  for match in self.pattern.finditer(norm):
   if not boundary(norm,match.start(),match.end(),match.group()):continue
   rows=[r for r in self.aliases[match.group()] if not r.get('scope_ids') or leaf.get('id') in r['scope_ids']]
   if not rows:continue
   row=rows[0]
   if row['id'] in self.seen:continue
   start=pos[match.start()];end=pos[match.end()-1]+1
   out.append(text[cursor:start]);out.append('<a class="term term-'+row['category']+'" data-concept-id="'+row['id']+'" href="#'+html.escape(row['target'],quote=True)+'">'+html.escape(text[start:end])+'</a>')
   cursor=end;self.seen.add(row['id']);self.counts[row['id']]=self.counts.get(row['id'],0)+1
  out.append(text[cursor:]);self.out.append(''.join(out))
 def handle_entityref(self,name):self.out.append('&'+name+';')
 def handle_charref(self,name):self.out.append('&#'+name+';')
 def handle_comment(self,data):self.out.append('<!--'+data+'-->')
 def handle_decl(self,data):self.out.append('<!'+data+'>')
 def handle_pi(self,data):self.out.append('<?'+data+'>')

def mark_concepts(content,manifest):
 targets=Targets();targets.feed(content)
 active,aliases=prepare(manifest,targets.targets,targets.leaves)
 marker=Marker(aliases);marker.feed(content)
 report={'selected':len(active),'linked_occurrences':marker.counts,
         'not_rendered':[r['id'] for r in active if r['id'] not in marker.counts],
         'scope':'matching only; not a semantic discovery or comprehension audit'}
 return ''.join(marker.out),report

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--content',type=Path,required=True);p.add_argument('--concepts',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--report',type=Path);a=p.parse_args()
 content,report=mark_concepts(a.content.read_text('utf-8'),json.loads(a.concepts.read_text('utf-8')))
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(content,'utf-8')
 if a.report:a.report.write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8')
 print(json.dumps(report,ensure_ascii=False))
