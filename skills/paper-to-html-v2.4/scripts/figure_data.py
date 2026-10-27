"""Render source-audited figure-data captions; never infer assays from pictures."""
from html.parser import HTMLParser
from html import escape

VOID={'img','br','hr','input','meta','link','source','area','base','col','embed','param','track','wbr'}
class Inventory(HTMLParser):
 def __init__(self):super().__init__();self.panels=set();self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  if 'data-reader-panel' in a and a.get('id'):self.panels.add(a['id'])

def caption(panel,item):
 lines=[]
 for layer in item['layers']:
  label=layer.get('label','数据')
  lines.append('<p><span class="reader-data-label">'+escape(label)+'：</span>'+escape(layer['data'])+' → '+escape(layer['processing'])+'</p>')
 return '<div class="reader-data-source" id="'+escape(panel,quote=True)+'-data-source" role="note" aria-label="本图数据来源">'+''.join(lines)+'</div>'

class Injector(HTMLParser):
 def __init__(self,panels):super().__init__(convert_charrefs=False);self.stack=[];self.out=[];self.panels=panels;self.done=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);parent=self.stack[-1][1] if self.stack else None
  panel=a.get('id') if 'data-reader-panel' in a else parent
  image='reader-image' in a.get('class','').split()
  self.out.append(self.get_starttag_text())
  if tag not in VOID:self.stack.append((tag,panel,image))
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==tag:
    _,panel,image=self.stack[i]
    if image and panel in self.panels and panel not in self.done:
     self.out.append(caption(panel,self.panels[panel]));self.done.add(panel)
    del self.stack[i:];break
  self.out.append('</'+tag+'>')
 def handle_startendtag(self,tag,attrs):self.out.append(self.get_starttag_text())
 def handle_data(self,text):self.out.append(text)
 def handle_entityref(self,name):self.out.append('&'+name+';')
 def handle_charref(self,name):self.out.append('&#'+name+';')
 def handle_comment(self,text):self.out.append('<!--'+text+'-->')
 def handle_decl(self,text):self.out.append('<!'+text+'>')

def render_figure_data(content,manifest):
 inventory=Inventory();inventory.feed(content);panels=manifest.get('panels')
 if not isinstance(panels,dict) or not panels:raise ValueError('figure-data requires a nonempty panels mapping')
 for panel,item in panels.items():
  if panel not in inventory.panels:raise ValueError('Unknown figure panel: '+panel)
  if panel+'-data-source' in inventory.ids:raise ValueError('Duplicate figure-data caption: '+panel)
  if not isinstance(item,dict) or not isinstance(item.get('layers'),list) or not item['layers']:raise ValueError('Each panel needs source layers: '+panel)
  if not isinstance(item.get('source_locator'),str) or not item['source_locator'].strip():raise ValueError('Source locator required: '+panel)
  for layer in item['layers']:
   if not isinstance(layer,dict) or any(not isinstance(layer.get(k),str) or not layer[k].strip() for k in ['data','processing']):raise ValueError('Each layer needs data and processing: '+panel)
   if 'label' in layer and (not isinstance(layer['label'],str) or not layer['label'].strip()):raise ValueError('Layer label must be text')
 injector=Injector(panels);injector.feed(content)
 if injector.done!=set(panels):raise ValueError('Caption requires a reader-image container: '+', '.join(set(panels)-injector.done))
 return ''.join(injector.out)
