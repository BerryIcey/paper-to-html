/* Real desktop rendering of a canonical v2 fixture through build and publish. */
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),assert=require('node:assert/strict');
const {spawnSync}=require('node:child_process');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const scripts=__dirname,tmp=fs.mkdtempSync(path.join(os.tmpdir(),'reader-v2-fidelity-'));
function python(...args){const result=spawnSync(process.env.PYTHON||'python',['-X','utf8',...args],{encoding:'utf8'});assert.equal(result.status,0,result.stdout+result.stderr);}
const setup=String.raw`import sys,json
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from teaching_contract import render_teaching
from teaching_fidelity import make_manifest
root=Path(sys.argv[2]);panels=[]
for key in ('a','b'):
    front=''.join(f'<p id="{key}-front-{i}" data-reader-preserve="{role}">{text}</p>' for i,(role,text) in enumerate([('caption-original','Original caption.'),('caption-translation','完整中文图注。'),('summary','已有总结。'),('author-conclusion','作者的结果与判断：这是隔离合成测试。')]))
    guide=render_teaching({'blocks':[{'title':'先看这一列','text':'53 名患者约占 31%。此处只验证数字和内容保真。'},{'items':['一列对应一个分析单位。','当前符号按当前来源定义。']},{'table':{'headers':['位置','含义'],'rows':[['合成行','合成读数']]}},*[{'text':f'第 {i} 个合成讲解块，用于验证长内容可以滚动到达。'} for i in range(25)],{'text':f'END-{key}：最后一块必须可以读到。'}]},key+'-guide')
    panels.append(f'<div id="panel-{key}" class="reader-panel" data-reader-panel="{key}" role="tabpanel"><div class="reader-image"><img alt="isolated fixture" src="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'300\' height=\'100\'%3E%3Crect width=\'300\' height=\'100\' fill=\'green\'/%3E%3C/svg%3E"></div><div id="text-{key}" class="reader-text">{front}{guide}</div></div>')
content='<section id="result" data-section="隔离测试"><h1>V2 fixture</h1><div data-reader-figure><div role="tablist"><button data-reader-tab="a" role="tab" aria-controls="panel-a">a</button><button data-reader-tab="b" role="tab" aria-controls="panel-b">b</button></div>'+''.join(panels)+'</div></section>'
(root/'content.html').write_text(content,'utf-8');(root/'baseline.json').write_text(json.dumps(make_manifest(content),ensure_ascii=False),'utf-8')
`;
(async()=>{let browser;try{
fs.writeFileSync(path.join(tmp,'setup.py'),setup);python(path.join(tmp,'setup.py'),scripts,tmp);
python(path.join(scripts,'build_reader.py'),'--content',path.join(tmp,'content.html'),'--paper-id','isolated-v2-fidelity','--out',path.join(tmp,'built.html'),'--teaching-baseline',path.join(tmp,'baseline.json'));
python(path.join(scripts,'publish_reader.py'),'--root',tmp,'--source',path.join(tmp,'built.html'),'--title','test','--teaching-baseline',path.join(tmp,'baseline.json'));
browser=await chromium.launch({headless:true,...(process.env.READER_BROWSER_EXECUTABLE?{executablePath:process.env.READER_BROWSER_EXECUTABLE}:{})});
const page=await browser.newPage({viewport:{width:1280,height:850}}),errors=[];page.on('pageerror',e=>errors.push(e.message));await page.setContent(fs.readFileSync(path.join(tmp,'paper-reading.html'),'utf8'));
for(const key of ['a','b']){
await page.locator(`[data-reader-tab="${key}"]`).click();const panel=page.locator('#panel-'+key),text=panel.locator('.reader-text');assert.ok(await panel.isVisible());
assert.equal(await text.locator('[data-reader-preserve]').count(),4);assert.equal(await text.locator('[data-teaching-block]').count(),29);
assert.ok((await text.innerText()).includes('53 名患者约占 31%'));assert.ok(await text.locator('table').isVisible());
const blocks=text.locator('[data-teaching-block]');for(let i=0;i<await blocks.count();i++)assert.ok(await blocks.nth(i).isVisible(),'all blocks must be displayed');
const last=blocks.last();await last.scrollIntoViewIfNeeded();assert.ok((await last.innerText()).includes('END-'+key));
assert.ok(await last.evaluate(el=>{const r=el.getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight+1}),'last block reachable in viewport');
assert.ok(await text.evaluate(el=>el.scrollWidth<=el.clientWidth+1),'text has no horizontal clipping');
}
assert.deepEqual(errors,[]);console.log('PASS v2 desktop: canonical build/publish, both panels, four preserved parts, all 29 blocks, table, numbers, final block reachable; synthetic fixture only');
}finally{if(browser)await browser.close();fs.rmSync(tmp,{recursive:true,force:true});}})().catch(e=>{console.error(e);process.exitCode=1});
