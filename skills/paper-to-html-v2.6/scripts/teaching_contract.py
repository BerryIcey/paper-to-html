"""Preserve the reader's teaching blocks; validate structure, not scientific truth."""
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import argparse

ROLES = ('question', 'legend', 'reasoning', 'next')

def _paragraphs(value, field):
    if not isinstance(value, list) or not value or any(not isinstance(p, str) or not p.strip() for p in value):
        raise ValueError(f'{field} requires a substantive explanation; adequacy needs semantic review')
    return value

def render_teaching(data, prefix, text_renderer=escape):
    if 'blocks' in data:
        blocks=data['blocks']
        if not isinstance(blocks,list) or not blocks:raise ValueError('blocks requires nonempty teaching content')
        rendered=[]
        for i,block in enumerate(blocks):
            if not isinstance(block,dict):raise ValueError('each block must be an object')
            kinds=[k for k in ('text','items','table') if k in block]
            if len(kinds)!=1:raise ValueError('each block requires exactly one content kind')
            base=f'{prefix}-block-{i}';title=block.get('title','')
            if not isinstance(title,str):raise ValueError('title must be text')
            body=f'<h4>{text_renderer(title)}</h4>' if title.strip() else ''
            kind=kinds[0]
            if kind=='text':
                _paragraphs([block[kind]],'text')
                body+=f'<p id="{base}-text" data-highlight-block>{text_renderer(block[kind])}</p>'
            elif kind=='items':
                body+='<ul>'+''.join(f'<li id="{base}-item-{j}" data-highlight-block>{text_renderer(t)}</li>' for j,t in enumerate(_paragraphs(block[kind],'items')))+'</ul>'
            else:
                table=block[kind]
                if not isinstance(table,dict):raise ValueError('table must be an object')
                headers=_paragraphs(table.get('headers'),'headers');rows=table.get('rows')
                if not isinstance(rows,list) or not rows:raise ValueError('table requires rows')
                body+='<table><thead><tr>'+''.join(f'<th>{text_renderer(t)}</th>' for t in headers)+'</tr></thead><tbody>'
                for j,row in enumerate(rows):
                    _paragraphs(row,'row')
                    if len(row)!=len(headers):raise ValueError('table row width differs from headers')
                    body+='<tr>'+''.join(f'<td id="{base}-cell-{j}-{k}" data-highlight-block>{text_renderer(t)}</td>' for k,t in enumerate(row))+'</tr>'
                body+='</tbody></table>'
            rendered.append(f'<div id="{base}" data-teaching-block>{body}</div>')
        return '<div data-reader-teaching="v2">'+''.join(rendered)+'</div>'
    question = _paragraphs(data.get('question'), 'question')
    reasoning = _paragraphs(data.get('reasoning'), 'reasoning')
    legend = data.get('legend')
    if not isinstance(legend, list) or any(not all(isinstance(r.get(k), str) and r[k].strip() for k in ('visual', 'meaning')) for r in legend):
        raise ValueError('legend requires explicit visual-to-meaning rows')
    if not legend and not str(data.get('legend_not_applicable', '')).strip():
        raise ValueError('empty legend requires an explicit non-applicability reason')
    next_question = data.get('next_question')
    if not isinstance(next_question, str) or not next_question.strip():
        raise ValueError('next_question requires the remaining question, parallel role, or final synthesis')
    def paras(items, role):
        return ''.join(f'<p id="{prefix}-{role}-{i}" data-highlight-block>{text_renderer(t)}</p>' for i,t in enumerate(items))
    rows = ''.join(f'<tr><td id="{prefix}-visual-{i}" data-highlight-block>{text_renderer(r["visual"])}</td><td id="{prefix}-meaning-{i}" data-highlight-block>{text_renderer(r["meaning"])}</td></tr>' for i,r in enumerate(legend))
    legend_content = ('<table><thead><tr><th>图中位置／元素</th><th>含义与读法</th></tr></thead><tbody>'+rows+'</tbody></table>') if legend else '<p data-teaching-not-applicable="legend">'+text_renderer(data['legend_not_applicable'])+'</p>'
    return (f'<div data-reader-teaching="v1">'
            f'<div data-teaching-role="question"><h4>带着当前问题读图</h4>{paras(question,"question")}</div>'
            f'<div data-teaching-role="legend"><h4>本图图例与元素</h4>{legend_content}</div>'
            f'<div data-teaching-role="reasoning"><h4>从实际结果读到判断</h4>{paras(reasoning,"reasoning")}</div>'
            f'<div data-teaching-role="next"><h4>结论边界与后续联系</h4><p id="{prefix}-next" data-highlight-block>{text_renderer(next_question)}</p></div></div>')

class Node:
    def __init__(self, tag='', attrs=None):
        self.tag=tag;self.attrs=attrs or {};self.children=[];self.text=[];self.parts=[]
    def descendants(self):
        for c in self.children:
            yield c
            yield from c.descendants()
    def words(self):
        return ''.join(self.text)+''.join(c.words() for c in self.children)
    def ordered_text(self):
        if self.tag in ('script','style'):return ''
        return ''.join(p if isinstance(p,str) else p.ordered_text() for p in self.parts)

class ReaderTree(HTMLParser):
    def __init__(self):
        super().__init__();self.root=Node();self.stack=[self.root]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        # Embedded pixels are irrelevant to the block contract and can be large.
        a.pop('src',None)
        node=Node(tag,a);node.parent=self.stack[-1];self.stack[-1].children.append(node);self.stack[-1].parts.append(node)
        if tag not in ('img','br','hr','meta','link','input','source','area','base','embed','wbr'):self.stack.append(node)
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==tag:
                del self.stack[i:];break
    def handle_data(self, data):
        self.stack[-1].text.append(data);self.stack[-1].parts.append(data)

def check_reader_html(content):
    tree=ReaderTree();tree.feed(content);errors=[];coverage=[]
    all_nodes=list(tree.root.descendants())
    by_id={}
    for node in all_nodes:
        if node.attrs.get('id'):by_id.setdefault(node.attrs['id'],[]).append(node)
    def is_unit(node):
        return ('data-reader-teaching-unit' in node.attrs or
                ('data-reader-panel' in node.attrs and
                 (node.attrs['data-reader-panel']!='overview' or 'data-reader-teaching-mode' in node.attrs)))
    for panel in all_nodes:
        if not is_unit(panel):continue
        key=panel.attrs.get('id',panel.attrs.get('data-reader-panel','unnamed-unit'))
        mode=panel.attrs.get('data-reader-teaching-mode','detailed')
        wrappers=[n for n in panel.descendants() if 'data-reader-teaching' in n.attrs]
        modern=[n for n in wrappers if n.attrs['data-reader-teaching']=='v2']
        if modern:
            if len(wrappers)!=1:errors.append(f'{key}: requires exactly one teaching wrapper')
            texts=[n for n in panel.descendants() if 'reader-text' in n.attrs.get('class','').split()]
            if len(texts)!=1 or modern[0] not in list(texts[0].descendants()):
                errors.append(f'{key}: teaching requires one reader-text containing the guide')
            if 'data-reader-panel' in panel.attrs:
                nodes=list(panel.descendants())
                protected=[n for n in nodes if 'data-reader-preserve' in n.attrs]
                required=('caption-original','caption-translation','summary','author-conclusion')
                if tuple(n.attrs['data-reader-preserve'] for n in protected)!=required:
                    errors.append(f'{key}: protected caption / translation / summary / author-conclusion order required')
                if any(not n.attrs.get('id') or not n.ordered_text().strip() for n in protected):errors.append(f'{key}: protected parts require stable ids and content')
                if len(texts)==1 and any(n not in list(texts[0].descendants()) for n in protected):errors.append(f'{key}: protected parts must be inside reader-text')
                if any(nodes.index(n)>nodes.index(modern[0]) for n in protected):errors.append(f'{key}: protected parts must precede teaching')
            blocks=[n for n in modern[0].children if 'data-teaching-block' in n.attrs]
            if not blocks or any(not n.attrs.get('id') or not any(c.tag in ('p','li','td') and c.ordered_text().strip() for c in n.descendants()) for n in blocks):
                errors.append(f'{key}: flexible blocks require stable ids and explanatory content')
            if mode=='detailed':coverage.append(key);continue
        if mode not in ('detailed','brief','shared'):
            errors.append(f'{key}: unknown teaching mode {mode}');continue
        if mode in ('brief','shared'):
            if not panel.attrs.get('data-reader-teaching-reason','').strip():
                errors.append(f'{key}: {mode} requires a source-based granularity reason')
            texts=[n for n in panel.descendants() if 'reader-text' in n.attrs.get('class','').split()]
            if len(texts)!=1 or not any(n.tag=='p' and n.words().strip() for n in texts[0].descendants()):
                errors.append(f'{key}: {mode} requires retained caption or local context')
            if mode=='shared':
                target=panel.attrs.get('data-reader-teaching-target','')
                matches=by_id.get(target,[])
                if (len(matches)!=1 or matches[0] is panel or not is_unit(matches[0]) or
                    matches[0].attrs.get('data-reader-teaching-mode','detailed')!='detailed'):
                    errors.append(f'{key}: shared teaching must point to one detailed unit')
                links=[n for n in panel.descendants() if n.tag=='a' and n.attrs.get('href')=='#'+target]
                if not links:errors.append(f'{key}: shared teaching requires a visible lookup link')
            coverage.append(key);continue
        wrappers=[n for n in panel.descendants() if 'data-reader-teaching' in n.attrs]
        if len(wrappers)==0:
            # Preserve the reviewed legacy reader's three complete visible regions.
            texts=[n for n in panel.descendants() if 'reader-text' in n.attrs.get('class','').split()]
            legacy=[]
            if len(texts)==1:
                active=None
                mapping={'带着当前问题读图':'question','本图图例与元素':'legend','从实际结果读到判断':'reasoning'}
                for n in texts[0].children:
                    title=n.words().strip() if n.tag in ('h3','h4') else ''
                    if title in mapping:
                        active=Node('div',{'data-teaching-role':mapping[title]});legacy.append(active)
                    elif active is not None:active.children.append(n)
            if tuple(n.attrs['data-teaching-role'] for n in legacy)==ROLES[:3]:
                remainder=Node('div',{'data-teaching-role':'next'})
                ps=[n for n in legacy[-1].descendants() if n.tag=='p']
                if ps:remainder.children.append(ps[-1])
                wrapper=Node();wrapper.children=legacy+[remainder];wrappers=[wrapper]
        if len(wrappers)!=1:
            errors.append(f'{key}: teaching blocks missing; an explain paragraph is not the complete reading guide');continue
        blocks=[n for n in wrappers[0].children if n.attrs.get('data-teaching-role')]
        if tuple(n.attrs['data-teaching-role'] for n in blocks)!=ROLES:
            errors.append(f'{key}: teaching block order must be question / legend / reasoning / next');continue
        for block in blocks:
            role=block.attrs['data-teaching-role'];nodes=list(block.descendants())
            if role in ('question','reasoning'):
                ps=[n for n in nodes if n.tag=='p' and n.words().strip()]
                if not ps:errors.append(f'{key}: {role} needs an explanation; substantive adequacy needs semantic review')
            elif role=='legend':
                rows=[n for n in nodes if n.tag=='tr' and sum(c.tag=='td' and bool(c.words().strip()) for c in n.children)>=2]
                reasons=[n for n in nodes if n.attrs.get('data-teaching-not-applicable')=='legend' and n.words().strip()]
                if not rows and not reasons:errors.append(f'{key}: legend lacks local mapping or non-applicability reason')
            elif not any(n.tag=='p' and n.words().strip() for n in nodes):errors.append(f'{key}: remaining question missing')
        coverage.append(key)
    return errors,coverage

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--html',type=Path,required=True);ap.add_argument('--snapshot',type=Path);a=ap.parse_args()
    content=a.html.read_text('utf-8');errors,coverage=check_reader_html(content)
    if errors:raise SystemExit('\n'.join(errors))
    if a.snapshot:
        from teaching_fidelity import make_manifest
        import json
        a.snapshot.parent.mkdir(parents=True,exist_ok=True)
        a.snapshot.write_text(json.dumps(make_manifest(content),ensure_ascii=False,indent=2),'utf-8')
    print(f'Teaching structure PASS: {len(coverage)} units/panels. This does not validate granularity choices, source labels, scientific reasoning, or reader understanding.')
