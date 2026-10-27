(() => {
'use strict';
const $=s=>document.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const namespace=document.body.dataset.paperId;
if(!namespace)throw Error('A unique data-paper-id is required');
const store={get:(k,d)=>{try{return JSON.parse(localStorage.getItem(namespace+':'+k))??d}catch{return d}},set:(k,v)=>{try{localStorage.setItem(namespace+':'+k,JSON.stringify(v));return true}catch{return false}}};
const stack=[],back=$('#reader-return');
function select(f,key){$$('[data-reader-tab]',f).forEach(b=>{const active=b.dataset.readerTab===key;b.setAttribute('aria-selected',String(active));b.tabIndex=active?0:-1});$$('[data-reader-panel]',f).forEach(p=>{p.hidden=p.dataset.readerPanel!==key;p.tabIndex=0});f.dataset.activePanel=key;}
$$('[data-reader-figure]').forEach(f=>{const tabs=$$('[data-reader-tab]',f);if(!tabs.length)return;tabs.forEach((b,i)=>{b.onclick=()=>select(f,b.dataset.readerTab);b.onkeydown=e=>{if(!['ArrowLeft','ArrowRight'].includes(e.key))return;e.preventDefault();const n=tabs[(i+(e.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length];n.click();n.focus()}});select(f,tabs[0].dataset.readerTab)});
function snapshot(){return {x:scrollX,y:scrollY,figures:$$('[data-reader-figure]').map(f=>({id:f.id,panel:f.dataset.activePanel,scrolls:$$('.reader-text',f).map(t=>({id:t.id,y:t.scrollTop}))}))}}
function jump(el,remember){if(remember){stack.push(snapshot());back.hidden=false}else{stack.length=0;back.hidden=true};const card=el.closest('[data-reader-card]');let node=el;if(card?.tagName==='DETAILS')card.open=true;else if(el.tagName==='DETAILS')el.open=true;const panel=el.closest('[data-reader-panel]');if(panel)select(panel.closest('[data-reader-figure]'),panel.dataset.readerPanel);requestAnimationFrame(()=>{if(card===el&&el.getBoundingClientRect().height>innerHeight*.8)node=el.querySelector('summary,h3,h4')||el;node.scrollIntoView({block:card===el?'center':'start',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})})}
document.addEventListener('click',e=>{const a=e.target.closest('a[href^="#"]');if(!a)return;let id;try{id=decodeURIComponent(a.hash.slice(1))}catch{return}const el=document.getElementById(id);if(!el)return;e.preventDefault();jump(el,!a.closest('#reader-nav')&&(!!el.closest('[data-reader-card]')||a.hasAttribute('data-reader-return')))});
back.onclick=()=>{const s=stack.pop();if(!s)return;s.figures.forEach(v=>{const f=document.getElementById(v.id);if(f){select(f,v.panel);v.scrolls.forEach(t=>{const el=document.getElementById(t.id);if(el)el.scrollTop=t.y})}});window.scrollTo(s.x,s.y);back.hidden=!stack.length};
$$('[data-reader-card-group]').forEach(group=>{const heading=group.querySelector('h2,h3');let bar=group.querySelector('.reader-card-heading');if(!bar){bar=document.createElement('div');bar.className='reader-card-heading';if(heading){heading.before(bar);bar.append(heading)}else group.prepend(bar)}group.querySelectorAll('.reader-card-controls,[data-reader-cards-action]').forEach(e=>e.remove());const button=document.createElement('button');button.dataset.readerCardsToggle='';bar.append(button);const cards=()=>$$('details[data-reader-card]',group);function sync(){const all=cards().length>0&&cards().every(c=>c.open);button.textContent=all?'一键收起':'一键展开';button.setAttribute('aria-expanded',String(all))}button.onclick=()=>{const open=!cards().every(c=>c.open);cards().forEach(c=>c.open=open);sync()};cards().forEach(c=>c.addEventListener('toggle',sync));sync()});
const pen=$('#reader-pen'),penTools=$('#reader-pen-tools'),legend=$('#reader-legend'),legendToggle=$('#reader-legend-toggle');let enabled=false;
// A flex sidebar reserves a footer; expanding upward never displaces its toggles.
const dock=document.querySelector('.reader-dock'),dockRow=dock.querySelector('.reader-dock-row');
const sidebar=document.createElement('aside');sidebar.className='reader-sidebar';sidebar.setAttribute('aria-label','阅读目录与工具');
const originalNav=$('#reader-nav');originalNav.before(sidebar);sidebar.append(originalNav,dock);
dock.insertBefore(penTools,dockRow);dock.insertBefore(legend,dockRow);
pen.setAttribute('aria-controls','reader-pen-tools');legendToggle.setAttribute('aria-controls','reader-legend');
pen.innerHTML='<svg class="reader-dock-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="m14 4 6 6-9 9H5v-6z"/><path d="m11 7 6 6M4 21h9"/></svg><span>荧光笔</span><span class="reader-dock-chevron" aria-hidden="true">⌃</span>';
legendToggle.innerHTML='<svg class="reader-dock-icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="4" width="5" height="5" rx="1"/><rect x="4" y="15" width="5" height="5" rx="1"/><path d="M13 6h7M13 17h7"/></svg><span>图例</span><span class="reader-dock-chevron" aria-hidden="true">⌃</span>';
const penHeading=document.createElement('p');penHeading.className='reader-tool-heading';penHeading.textContent='文本标黄';

const penActions=document.createElement('div');penActions.className='reader-tool-actions';penActions.append($('#reader-pen-enable'),$('#reader-undo'));penTools.append(penHeading,penActions);

function penOpen(v){if(v)legendOpen(false);pen.setAttribute('aria-label',v?'收起荧光笔':'展开荧光笔');if(!v){enabled=false;$('#reader-pen-enable').setAttribute('aria-pressed','false');$('#reader-pen-enable').textContent='开启'};penTools.hidden=!v;pen.setAttribute('aria-expanded',String(v))}
$('#reader-pen-enable').onclick=()=>{enabled=!enabled;$('#reader-pen-enable').setAttribute('aria-pressed',String(enabled));$('#reader-pen-enable').textContent=enabled?'关闭':'开启'};
function colors(v){document.body.classList.toggle('reader-clean',!v);$('#reader-color-toggle').setAttribute('aria-pressed',String(v));$('#reader-color-toggle').textContent=v?'术语彩色：开启':'术语彩色：关闭';store.set('term-colors',v)}$('#reader-color-toggle').onclick=()=>colors(document.body.classList.contains('reader-clean'));colors(store.get('term-colors',true));
pen.onclick=()=>penOpen(penTools.hidden);
function legendOpen(v){if(v)penOpen(false);legendToggle.setAttribute('aria-label',v?'收起图例':'展开图例');legend.hidden=!v;legendToggle.setAttribute('aria-expanded',String(v));store.set('legend-open',v)}legendToggle.onclick=()=>legendOpen(legend.hidden);legendOpen(false);
let marks=store.get('marks',[]);const blocks=()=>$$('[data-highlight-block]');
function textNodes(el){let w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT),out=[];while(w.nextNode())out.push(w.currentNode);return out}
function paint(b,lo,hi){let offset=0;for(const n of textNodes(b)){const l=n.length,start=Math.max(0,lo-offset),end=Math.min(l,hi-offset);offset+=l;if(end<=start)continue;const r=document.createRange();r.setStart(n,start);r.setEnd(n,end);const m=document.createElement('mark');m.className='reader-mark';r.surroundContents(m)}}
function redraw(){for(const m of $$('.reader-mark'))m.replaceWith(...m.childNodes);for(const r of marks){const b=document.getElementById(r.id);if(b&&b.textContent===r.text)paint(b,r.lo,r.hi)}}
$('#reader-undo').onclick=()=>{const op=marks.at(-1)?.op;marks=marks.filter(m=>m.op!==op);redraw();store.set('marks',marks)};
document.addEventListener('pointerup',e=>{if(!enabled||e.target.closest('.reader-dock,.reader-notes'))return;const s=getSelection();if(!s||s.isCollapsed||!s.rangeCount)return;const r=s.getRangeAt(0),op=Date.now()+':'+Math.random();let added=false;for(const b of blocks()){if(!b.id||b.closest('[hidden]'))continue;let offset=0,lo=null,hi=null;for(const n of textNodes(b)){if(r.intersectsNode(n)){const from=n===r.startContainer?r.startOffset:0,to=n===r.endContainer?r.endOffset:n.length;if(to>from){lo??=offset+from;hi=offset+to}}offset+=n.length}if(lo!==null&&hi>lo&&!marks.some(m=>m.id===b.id&&m.lo<hi&&m.hi>lo)){marks.push({id:b.id,text:b.textContent,lo,hi,op});added=true}}if(added){s.removeAllRanges();redraw();if(!store.set('marks',marks))alert('浏览器高亮保存失败')}});redraw();
$$('[data-reader-zoom],#reader-zoom-image').forEach(img=>{img.draggable=false;img.addEventListener('dragstart',e=>e.preventDefault())});
const modal=$('#reader-zoom'),stage=$('#reader-zoom-stage'),im=$('#reader-zoom-image');let scale=1,x=0,y=0,drag,previewTrigger;
function draw(){im.style.transform=`translate(${x}px,${y}px) scale(${scale})`}function reset(){scale=1;x=y=0;draw()}
$$('[data-reader-zoom]').forEach(img=>{img.tabIndex=0;img.setAttribute('role','button');img.setAttribute('aria-haspopup','dialog');img.setAttribute('aria-controls','reader-zoom');img.setAttribute('aria-label','放大查看：'+(img.alt||'论文图片'));const open=()=>{previewTrigger=img;im.src=img.src;im.alt=img.alt||'当前放大图';reset();modal.showModal()};img.onclick=open;img.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();e.stopPropagation();open()}})});$('#reader-zoom-close').onclick=()=>modal.close();let backdropDown=false;modal.addEventListener('pointerdown',e=>{const r=modal.getBoundingClientRect();backdropDown=e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom});modal.addEventListener('click',e=>{const r=modal.getBoundingClientRect();if(backdropDown&&(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom))modal.close();backdropDown=false});modal.addEventListener('close',()=>{touches.clear();drag=null;pinch=null;if(previewTrigger?.isConnected)previewTrigger.focus({preventScroll:true})});$('#reader-zoom-reset').onclick=reset;
function zoom(n){scale=Math.max(.4,Math.min(10,n));draw()}$('#reader-zoom-plus').onclick=()=>zoom(scale*1.25);$('#reader-zoom-minus').onclick=()=>zoom(scale*.8);
stage.addEventListener('wheel',e=>{e.preventDefault();zoom(scale*(e.deltaY<0?1.1:.9))},{passive:false});const touches=new Map();let pinch=null;
stage.onpointerdown=e=>{if(e.button!==0)return;stage.setPointerCapture(e.pointerId);touches.set(e.pointerId,{x:e.clientX,y:e.clientY});if(touches.size===2){const [a,b]=[...touches.values()];pinch={dist:Math.hypot(a.x-b.x,a.y-b.y),scale};drag=null}else drag={sx:e.clientX,sy:e.clientY,x,y}};
stage.onpointermove=e=>{if(!touches.has(e.pointerId))return;touches.set(e.pointerId,{x:e.clientX,y:e.clientY});if(touches.size===2&&pinch){const [a,b]=[...touches.values()];zoom(pinch.scale*Math.hypot(a.x-b.x,a.y-b.y)/Math.max(1,pinch.dist))}else if(drag){x=drag.x+e.clientX-drag.sx;y=drag.y+e.clientY-drag.sy;draw()}};function end(e){touches.delete(e.pointerId);drag=null;pinch=null}stage.onpointerup=end;stage.onpointercancel=end;
const sections=$$('main section[data-section]');const nav=$('#reader-nav');const brand=document.createElement('div');brand.className='reader-nav-brand';brand.textContent=document.body.dataset.paperCitation||'PAPER · READING';const title=document.createElement('h2');title.textContent=document.querySelector('.chinese-title')?.textContent||document.querySelector('h1')?.textContent||'论文共读';nav.replaceChildren(brand,title);for(const [label,tier] of [['基础 · 文章内容','core'],['知识区','knowledge'],['进阶内容','advanced'],['进阶知识区','advanced-knowledge']]){const group=sections.filter(s=>(s.dataset.readingTier||'core')===tier);if(!group.length)continue;const h=document.createElement('h3');h.textContent=label;nav.append(h);for(const s of group){const a=document.createElement('a');a.href='#'+s.id;a.textContent=s.dataset.section;nav.append(a)}}const observer=new IntersectionObserver(entries=>{for(const e of entries)if(e.isIntersecting){for(const a of nav.querySelectorAll('a'))a.classList.toggle('active',a.hash==='#'+e.target.id)}},{rootMargin:'-15% 0px -60% 0px'});sections.forEach(s=>observer.observe(s));$('#reader-note-section').replaceChildren(...sections.map(s=>{const o=document.createElement('option');o.value=s.id;o.textContent=s.dataset.section;return o}));
const notes=$('#reader-notes'),draft=$('#reader-draft'),status=$('#reader-note-status');let editId=null,requestId=null,attachments=store.get('draft-attachments',[]),online=false;
const noteSection=$('#reader-note-section');
let sectionTick=false,editKind='question';
const locationHint=document.createElement('p');locationHint.id='reader-note-location';locationHint.className='reader-note-location';noteSection.after(locationHint);
function showNoteLocation(){locationHint.textContent=(editId?'原记录位置：':'当前阅读：')+(noteSection.selectedOptions[0]?.textContent||'正文')}
function followReadingSection(){
 if(editId){showNoteLocation();return}
 const line=Math.min(innerHeight*.3,220);
 const visible=sections.filter(s=>{const r=s.getBoundingClientRect();return r.bottom>line&&r.top<innerHeight});
 const current=visible.filter(s=>s.getBoundingClientRect().top<=line).at(-1)||visible[0];
 if(current){noteSection.value=current.id;store.set('draft-section',current.id)}showNoteLocation();
}
window.addEventListener('scroll',()=>{if(notes.hidden||sectionTick)return;sectionTick=true;requestAnimationFrame(()=>{sectionTick=false;followReadingSection()})},{passive:true});
function notesOpen(v){if(v)followReadingSection();notes.hidden=!v;$('#reader-notes-toggle').setAttribute('aria-expanded',String(v));store.set('notes-open',v)}

const noteBookmark=$('#reader-notes-toggle');let bookmarkDrag=null,bookmarkSuppress=false;
function bookmarkPlace(ratio){const span=Math.max(0,innerHeight-noteBookmark.offsetHeight-16);noteBookmark.style.top=(8+span*Math.max(0,Math.min(1,ratio)))+'px'}
bookmarkPlace(store.get('notes-bookmark-position',.38));window.addEventListener('resize',()=>bookmarkPlace(store.get('notes-bookmark-position',.38)));
noteBookmark.addEventListener('pointerdown',e=>{if(e.button!==0)return;bookmarkSuppress=false;bookmarkDrag={id:e.pointerId,start:e.clientY,top:noteBookmark.getBoundingClientRect().top,moved:false};noteBookmark.setPointerCapture(e.pointerId)});
noteBookmark.addEventListener('pointermove',e=>{if(!bookmarkDrag||e.pointerId!==bookmarkDrag.id)return;const delta=e.clientY-bookmarkDrag.start;if(Math.abs(delta)>6)bookmarkDrag.moved=true;if(bookmarkDrag.moved){const span=Math.max(0,innerHeight-noteBookmark.offsetHeight-16);const ratio=span?Math.max(0,Math.min(1,(bookmarkDrag.top+delta-8)/span)):0;bookmarkPlace(ratio);store.set('notes-bookmark-position',ratio);e.preventDefault()}});
function bookmarkEnd(e){if(!bookmarkDrag||e.pointerId!==bookmarkDrag.id)return;bookmarkSuppress=bookmarkDrag.moved;bookmarkDrag=null;if(noteBookmark.hasPointerCapture(e.pointerId))noteBookmark.releasePointerCapture(e.pointerId)}
noteBookmark.addEventListener('pointerup',bookmarkEnd);noteBookmark.addEventListener('pointercancel',bookmarkEnd);
noteBookmark.onclick=e=>{if(bookmarkSuppress&&e.detail!==0){bookmarkSuppress=false;return}bookmarkSuppress=false;notesOpen(notes.hidden)};
document.addEventListener('pointerdown',e=>{if(!notes.hidden&&!e.target.closest('#reader-notes,#reader-notes-toggle,#reader-zoom'))notesOpen(false)});document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!modal.open)notesOpen(false)});notesOpen(store.get('notes-open',false));
draft.value=store.get('draft','');draft.oninput=()=>{store.set('draft',draft.value);store.set('draft-section',noteSection.value);requestId=null};
function previews(){$('#reader-attachments').replaceChildren(...attachments.map((a,i)=>{
 const box=document.createElement('span');box.className='reader-attachment';
 const img=document.createElement('img');img.src=a.data;img.alt=a.name||'粘贴的截图';
 const x=document.createElement('button');x.type='button';x.className='reader-attachment-remove';x.textContent='×';x.setAttribute('aria-label',`移除截图 ${i+1}`);x.title='移除这张截图';
 x.onclick=()=>{attachments.splice(i,1);requestId=null;store.set('draft-attachments',attachments);previews()};box.append(img,x);return box
}))}previews();
async function imageFiles(fs){for(const f of fs){if(attachments.length>=4||f.size>5*1024*1024||!['image/png','image/jpeg','image/webp'].includes(f.type))continue;const data=await new Promise((resolve,reject)=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.onerror=reject;r.readAsDataURL(f)});attachments.push({name:f.name,data});requestId=null}store.set('draft-attachments',attachments);previews()}
draft.onpaste=e=>{const fs=[...e.clipboardData.files];if(fs.length){e.preventDefault();imageFiles(fs)}};
async function api(data){if(location.protocol==='file:')throw Error('当前是文件预览，不能保存提问；请从本地服务版打开。');let r;try{r=await fetch('/api/notes',{method:data?'POST':'GET',headers:data?{'Content-Type':'application/json'}:{},body:data?JSON.stringify(data):undefined})}catch(e){throw Error('暂时连接不到本地笔记服务。草稿仍保留；正在自动重连，恢复后可以重试保存。')}const j=await r.json();if(!r.ok)throw Error(j.error||'保存失败');return j}
async function action(data){try{await api(data);await refresh()}catch(e){status.textContent=e.message}}
let noteItems=[],noteFilter=store.get('notes-filter','all');if(!['all','pending','resolved','deleted'].includes(noteFilter))noteFilter='all';
const noteList=$('#reader-note-list'),historyTools=document.createElement('div');historyTools.className='reader-history-tools';historyTools.id='reader-note-history-tools';
const historyHeading=document.createElement('h3');historyHeading.textContent='问题与修改清单';const historyCount=document.createElement('p');historyCount.className='reader-history-count';historyCount.setAttribute('aria-live','polite');
const filterBar=document.createElement('div');filterBar.className='reader-note-filters';filterBar.setAttribute('aria-label','筛选随手记');
for(const [key,label] of [['all','全部'],['pending','待处理'],['resolved','已处理'],['deleted','已删除']]){const b=document.createElement('button');b.type='button';b.dataset.noteFilter=key;b.textContent=label;b.onclick=()=>{noteFilter=key;store.set('notes-filter',key);renderNoteItems()};filterBar.append(b)}
historyTools.append(historyHeading,historyCount,filterBar);noteList.before(historyTools);
function renderNoteItems(){
 const opened=new Set($$('details.reader-note[open]',noteList).map(e=>e.dataset.noteId));noteList.replaceChildren();
 const pending=noteItems.filter(n=>n.status==='pending').length,done=noteItems.filter(n=>n.status==='resolved').length;
 historyCount.textContent=`${pending} 条待处理 · ${done} 条已处理`;
 for(const b of filterBar.querySelectorAll('button'))b.setAttribute('aria-pressed',String(b.dataset.noteFilter===noteFilter));
 const rows=noteItems.slice().reverse().filter(n=>noteFilter==='all'||n.status===noteFilter);
 if(!rows.length){const p=document.createElement('p');p.className='reader-notes-empty';p.textContent=noteFilter==='pending'?'当前没有待处理记录。':'这个分类下还没有记录。';noteList.append(p);return}
 for(const n of rows){
  const box=document.createElement('details');box.className='reader-note reader-note-'+n.status;box.dataset.noteId=n.id;box.open=opened.has(n.id);
  const summary=document.createElement('summary'),check=document.createElement('input');check.type='checkbox';check.checked=n.status==='resolved';check.disabled=true;check.tabIndex=-1;check.setAttribute('aria-label',n.status==='resolved'?'已处理':'尚未处理');
  const title=document.createElement('span');title.className='reader-note-title';title.textContent=n.content.length>96?n.content.slice(0,96)+'…':n.content;
  const badge=document.createElement('span');badge.className='reader-note-badge';badge.textContent=n.status==='resolved'?'已处理':n.status==='deleted'?'已删除':'待处理';const badges=document.createElement('span');badges.className='reader-note-badges';badges.append(badge);
  const resolvedTarget=n.status==='resolved'&&document.getElementById(n.response_section||n.section);
  if(resolvedTarget){const shortcut=document.createElement('a');shortcut.className='reader-note-jump';shortcut.href='#'+resolvedTarget.id;shortcut.textContent='跳转';shortcut.setAttribute('aria-label','跳转到已处理的位置');shortcut.dataset.readerReturn='';shortcut.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();notesOpen(false);jump(resolvedTarget,true)});badges.append(shortcut)}
  summary.append(check,title,badges);box.append(summary);
  const body=document.createElement('div');body.className='reader-note-body';
  const meta=document.createElement('p');meta.className='reader-note-meta';const section=document.getElementById(n.section);const label=section?.dataset.section||'原章节';let time='';try{time=new Date(n.created_at).toLocaleString('zh-CN',{timeZone:'Asia/Shanghai',month:'numeric',day:'numeric',hour:'2-digit',minute:'2-digit'})}catch{}meta.textContent=label+(time?' · '+time:'');body.append(meta);
  const quote=document.createElement('blockquote');quote.className='reader-note-original';quote.textContent=n.content;body.append(quote);
  if((n.attachments||[]).length){const files=document.createElement('details');files.className='reader-note-files';const caption=document.createElement('summary');caption.textContent=`查看 ${n.attachments.length} 张附件`;files.append(caption);for(const a of n.attachments){if(/^data:image\/(png|jpeg|webp);base64,/.test(a.data)){const img=document.createElement('img');img.loading='lazy';img.src=a.data;img.alt=a.name||'随手记附件';files.append(img)}}body.append(files)}
  if(n.response){const response=document.createElement('div');response.className='reader-note-response';const h=document.createElement('strong');h.textContent='处理答复';const text=document.createElement('p');text.textContent=n.response;response.append(h,text);body.append(response)}
  const actions=document.createElement('div');actions.className='reader-note-actions';const target=document.getElementById(n.response_section||n.section);
  if(target){const a=document.createElement('a');a.href='#'+target.id;a.textContent='查看对应内容';a.dataset.readerReturn='';a.addEventListener('click',()=>notesOpen(false));actions.append(a)}
  if(n.status==='pending'){const edit=document.createElement('button');edit.type='button';edit.textContent='编辑';edit.onclick=()=>{editId=n.id;editKind=n.kind||'question';requestId=null;draft.value=n.content;attachments=(n.attachments||[]).map(a=>({...a}));noteSection.value=n.section;previews();notesOpen(true);draft.focus();status.textContent='正在编辑这条待办；保留它原先的章节。'};const del=document.createElement('button');del.type='button';del.textContent='删除';del.onclick=()=>action({action:'delete',id:n.id});actions.append(edit,del)}
  else if(n.status==='deleted'){const restore=document.createElement('button');restore.type='button';restore.textContent='恢复';restore.onclick=()=>action({action:'restore',id:n.id});actions.append(restore)}
  body.append(actions);box.append(body);noteList.append(box)
 }
}
async function refresh(){const j=await api();noteItems=j.notes;renderNoteItems();online=true;$('#reader-note-save').disabled=false}

$('#reader-note-save').onclick=async()=>{if(location.protocol==='file:'){status.textContent='文件预览不能保存，请从本地服务版打开。';return;}const b=$('#reader-note-save');b.disabled=true;requestId??=globalThis.crypto?.randomUUID?.()||Date.now()+'-'+Math.random();try{await api({action:editId?'update':'create',id:editId||requestId,kind:editId?editKind:'question',section:$('#reader-note-section').value,content:draft.value,attachments});draft.value='';attachments=[];editId=requestId=null;editKind='question';followReadingSection();store.set('draft','');store.set('draft-attachments',[]);previews();await refresh();status.textContent='已存入当前论文项目，下轮共读时助手读取；不会自动即时回复。'}catch(e){status.textContent=e.message+'；草稿保留，请重试。'}finally{b.disabled=false}};
let reconnecting=false;
async function reconnectNotes(){if(reconnecting||location.protocol==='file:')return;reconnecting=true;const wasOffline=!online;try{await refresh();if(wasOffline)status.textContent='已连接，写下问题或粘贴截图即可保存。'}catch(e){online=false;status.textContent=e.message}finally{reconnecting=false}}
if(location.protocol==='file:'){status.textContent='文件预览不能保存随手记，请打开本地阅读页。'}else{reconnectNotes();setInterval(()=>{if(!notes.hidden&&!document.hidden)reconnectNotes()},5000);window.addEventListener('online',reconnectNotes);window.addEventListener('focus',reconnectNotes)}

// First-launch release policy: preferences are project-level, never delete notes/assets.
const versionBar=document.createElement('div');versionBar.className='reader-version-bar';
const releaseLabel=document.createElement('span');releaseLabel.textContent=document.body.dataset.readerRelease||'工作稿 · 尚未正式编号';
const versionButton=document.createElement('button');versionButton.textContent='版本设置';versionBar.append(releaseLabel,versionButton);document.querySelector('h1')?.after(versionBar);
const versionDialog=document.createElement('dialog');versionDialog.className='reader-version-dialog';versionDialog.innerHTML='<h2>保留网站历史版本吗？</h2><p>最新版另计；选择两个备份时，共保留最近三版。只在正式交付时更新，笔记和附件不受影响。</p><label>保存方式<select id="reader-backup-choice"><option value="" selected disabled>请选择</option><option value="0">覆盖，不留历史备份</option><option value="1">保留 1 个备份（共 2 版）</option><option value="2">保留 2 个备份（共 3 版）</option></select></label><p class="reader-policy-status" role="status"></p><button id="reader-policy-save">保存选择</button><button id="reader-policy-later">稍后选择</button>';document.body.append(versionDialog);
const choice=versionDialog.querySelector('select'),policyStatus=versionDialog.querySelector('.reader-policy-status');let versionPolicy=null;
versionButton.onclick=()=>{choice.value=versionPolicy===null?'':String(versionPolicy);versionDialog.showModal()};
versionDialog.querySelector('#reader-policy-later').onclick=()=>versionDialog.close();
versionDialog.querySelector('#reader-policy-save').onclick=async()=>{if(choice.value===''){policyStatus.textContent='请选择保存方式';return}const count=Number(choice.value);try{if(location.protocol==='file:')return;if(location.protocol!=='file:'){const r=await fetch('/api/settings',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({backup_count:count})});if(!r.ok)throw Error('项目设置保存失败')}versionPolicy=count;versionDialog.close()}catch(e){policyStatus.textContent=e.message+'，请稍后重试；未更改项目选择。'}};
if(location.protocol==='file:'){
    versionPolicy=document.body.dataset.backupCount===undefined?null:Number(document.body.dataset.backupCount);
    versionDialog.innerHTML='<h2>项目版本设置</h2><p>此文件是离线快照，备份方式以项目设置为准。</p><p>导出时的设置：'+(versionPolicy===null?'尚未选择':versionPolicy===0?'覆盖，不留历史备份':'保留 '+versionPolicy+' 个历史备份')+'</p>';
    const localUrl=document.body.dataset.readerUrl;
    if(localUrl){const link=document.createElement('a');link.href=localUrl;link.textContent='打开本地阅读页，修改项目设置';versionDialog.append(link)}else{const p=document.createElement('p');p.textContent='请让助手在项目中配置备份方式；此文件不单独保存设置。';versionDialog.append(p)}
    const close=document.createElement('button');close.textContent='关闭';close.onclick=()=>versionDialog.close();versionDialog.append(close);
    versionButton.onclick=()=>versionDialog.showModal();
}else{
    (async()=>{try{const r=await fetch('/api/settings');if(!r.ok)throw Error();const p=await r.json();versionPolicy=Number.isInteger(p.backup_count)?p.backup_count:null;if(versionPolicy===null)versionDialog.showModal()}catch{policyStatus.textContent='暂时无法读取项目设置。连接恢复后可从版本设置重试。'}})();
}

})();
