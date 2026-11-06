"""Render article-audited categories. Domain/term discovery is an authoring decision."""
import re
from html import escape
from html.parser import HTMLParser

BIOLOGY=[
 {'id':'gene-protein','label':'基因与蛋白','color':'#d9e8fa'},
 {'id':'method','label':'实验方法','color':'#ffedc5'},
 {'id':'regulatory','label':'调控元件','color':'#daeee5'},
 {'id':'cell-type','label':'细胞与亚型','color':'#f3dfe2'},
 {'id':'concept','label':'生物学概念','color':'#ede0f5'},
]
# Compatibility for previously authored manuscripts; do not reinterpret old terms.
LEGACY=[{'id':k,'label':label,'color':color} for k,label,color in [
 ('object','研究对象','#f3dfe2'),('entity','实体','#d9e8fa'),
 ('process','过程','#ede0f5'),('method','方法','#e0e7ed'),
 ('metric','指标','#ffedc5'),('structure','结构','#daeee5'),
 ('disease','疾病','#f3dfe2'),('gene','基因','#d9e8fa'),
 ('protein','蛋白','#ede0f5'),('phenotype','表型','#ffedc5')]]

def categories(manifest):
 domain=manifest.get('domain')
 custom=manifest.get('legend')
 if domain=='biology':
  if custom is not None:raise ValueError('biology uses the fixed simple categories and colors')
  return BIOLOGY
 if custom is None:
  if domain is not None:raise ValueError('nonbiology or uncertain domain requires an article-specific legend')
  return LEGACY # Old manifests predate domain selection.
 if not isinstance(custom,list) or not custom or len(custom)>5:
  raise ValueError('article legend requires one to five clear categories')
 seen=set()
 for entry in custom:
  key=entry.get('id','');label=entry.get('label','');color=entry.get('color','')
  if not re.fullmatch(r'[a-z][a-z0-9-]{0,31}',key) or key in seen:raise ValueError('invalid or duplicate legend category')
  if not isinstance(label,str) or not label.strip() or len(label)>12:raise ValueError('use a short clear category label')
  if not re.fullmatch(r'#[0-9a-fA-F]{6}',color):raise ValueError('legend color must be six hexadecimal digits')
  seen.add(key)
 return custom

class Used(HTMLParser):
 def __init__(self):super().__init__();self.categories=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);classes=a.get('class','').split()
  if tag=='a' and 'term' in classes:
   self.categories.update(c[5:]for c in classes if c.startswith('term-'))

def render_legend(manifest,content):
 entries=categories(manifest);used=Used();used.feed(content)
 known={e['id']for e in entries}
 if used.categories-known-{'neutral'}:raise ValueError('colored terms must match the article legend')
 active=[e for e in entries if e['id'] in used.categories]
 markup='<div class="reader-legend-grid">'+''.join('<span class="term-'+e['id']+'">'+escape(e['label'])+'</span>'for e in active)+'</div>'
 css=''.join('.term-'+e['id']+'{background:'+e['color']+';--legend-swatch:'+e['color']+'}'for e in active)
 css+='.term-neutral{background:transparent}'
 return markup,css
