"""Compare approved panel prose with assembled HTML; scientific review is separate."""
import json,re
from pathlib import Path
from teaching_contract import ReaderTree

STRUCTURAL={'p','li','th','td','h2','h3','h4','h5','table','ul','ol','tr','thead','tbody','dl','dt','dd','blockquote'}

def normalized(text):
    return re.sub(r'\s+',' ',text).strip()

def make_manifest(content):
    tree=ReaderTree();tree.feed(content);units=[]
    for node in tree.root.descendants():
        if 'data-reader-panel' not in node.attrs and 'data-reader-teaching-unit' not in node.attrs:continue
        texts=[n for n in node.descendants() if 'reader-text' in n.attrs.get('class','').split()]
        if len(texts)!=1:raise ValueError('fidelity requires exactly one reader-text per unit')
        key=node.attrs.get('id')
        if not key:raise ValueError('fidelity requires stable unit ids')
        root=texts[0];blocks=[]
        for n in [root,*root.descendants()]:
            if n.tag in ('script','style'):continue
            if n.tag in STRUCTURAL or 'data-teaching-block' in n.attrs or 'data-reader-preserve' in n.attrs or any(k in n.attrs for k in ('hidden','aria-hidden','style')):
                blocks.append({'tag':n.tag,'id':n.attrs.get('id',''),'text':normalized(n.ordered_text()),
                               'preserve':n.attrs.get('data-reader-preserve',''),
                               'hidden':'hidden' in n.attrs,'aria-hidden':n.attrs.get('aria-hidden',''),
                               'style':normalized(n.attrs.get('style',''))})
        ancestors=[];ancestor=node
        while ancestor is not None:
            if any(k in ancestor.attrs for k in ('hidden','aria-hidden','style')):
                ancestors.append({'tag':ancestor.tag,'id':ancestor.attrs.get('id',''),
                                  'hidden':'hidden' in ancestor.attrs,'aria-hidden':ancestor.attrs.get('aria-hidden',''),
                                  'style':normalized(ancestor.attrs.get('style',''))})
            ancestor=getattr(ancestor,'parent',None)
        units.append({'id':key,'text':normalized(root.ordered_text()),'blocks':blocks,'ancestors':ancestors})
    if len({u['id'] for u in units})!=len(units):raise ValueError('duplicate fidelity unit ids')
    return {'schema':'reader-teaching-fidelity-v1','units':units}

def check_fidelity(content,manifest):
    if not isinstance(manifest,dict) or manifest.get('schema')!='reader-teaching-fidelity-v1' or not isinstance(manifest.get('units'),list):
        return ['Invalid teaching baseline']
    try:actual=make_manifest(content)
    except ValueError as error:return [str(error)]
    expected=manifest['units'];observed=actual['units'];errors=[]
    if [u.get('id') for u in expected]!=[u['id'] for u in observed]:errors.append('Teaching units missing, added, or reordered')
    by_id={u['id']:u for u in observed}
    for unit in expected:
        key=unit.get('id')
        if key in by_id and unit!=by_id[key]:errors.append(f'{key}: approved prose, numbers, block order, or visibility changed')
    return errors

def require_fidelity(content,baseline=None):
    tree=ReaderTree();tree.feed(content)
    modern=any(n.attrs.get('data-reader-teaching')=='v2' for n in tree.root.descendants())
    if baseline is None:
        if modern:raise ValueError('v2 teaching requires --teaching-baseline from the approved content before assembly')
        return
    errors=check_fidelity(content,json.loads(Path(baseline).read_text('utf-8')))
    if errors:raise ValueError('\n'.join(errors))
