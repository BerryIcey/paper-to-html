/* Coarse navigation and prose ownership regression, isolated from real notes. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const assets=path.resolve(__dirname,'../assets/reader-components');
const content=`<header><h1>Test paper</h1></header><section id="abstract" data-section="Abstract" data-reader-nav="摘要 Abstract" style="height:500px">Abstract</section><h2 id="results" data-reader-nav="结果 Results">Results</h2><section id="lead" data-section="Precise prose location" data-reader-nav-owner="fig1" style="height:600px">Figure one introduction</section><section id="fig1" data-section="Figure one source" data-reader-nav="图1 样本图谱" data-reader-nav-parent="results" style="height:600px">Original figure one</section><section id="bridge" data-section="Cross-figure comparison" data-reader-nav-owner="results" style="height:600px">Cross-figure comparison</section><section id="lead2" data-section="Precise second prose" data-reader-nav-owner="fig2" style="height:600px">Figure two introduction</section><section id="fig2" data-section="Figure two source" data-reader-nav="图2 分型" data-reader-nav-parent="results" style="height:600px">Original figure two</section>`;
let html=fs.readFileSync(path.join(assets,'shell.html'),'utf8').replace('replace-with-unique-paper-id','isolated-navigation-test').replace('<!--由论文内容替换：section[data-section]与稳定id；图文面板按components.md生成-->',content).replace('<link rel="stylesheet" href="reader.css">',()=>'<style>'+fs.readFileSync(path.join(assets,'reader.css'),'utf8')+'</style>').replace('<script src="reader.js"></script>',()=>'<script>'+fs.readFileSync(path.join(assets,'reader.js'),'utf8')+'</script>');
(async()=>{const browser=await chromium.launch({headless:true,...(process.env.READER_BROWSER_EXECUTABLE?{executablePath:process.env.READER_BROWSER_EXECUTABLE}:{})});try{const page=await browser.newPage({viewport:{width:1280,height:850},reducedMotion:'reduce'});await page.setContent(html);
assert.deepEqual(await page.locator('#reader-nav a').allTextContents(),['摘要 Abstract','结果 Results','图1 样本图谱','图2 分型']);
assert.equal(await page.locator('#reader-nav .reader-nav-children a').count(),2);
assert.equal(await page.locator('.reader-version-bar,.reader-version-dialog').count(),0);
for(const [id,owner] of [['lead','fig1'],['bridge','results'],['lead2','fig2']]){await page.locator('#'+id).evaluate(el=>scrollTo(0,el.getBoundingClientRect().top+scrollY-40));await page.waitForFunction(expected=>document.querySelector('#reader-nav a[aria-current="location"]')?.hash==='#'+expected,owner);}
await page.locator('#reader-nav a[href="#fig2"]').click();await page.waitForFunction(()=>{const y=document.querySelector('#fig2').getBoundingClientRect().top;return y>=0&&y<180});
assert.equal(await page.locator('#reader-return').isHidden(),true);
assert.equal(await page.locator('#reader-note-section option[value="lead"]').count(),1);
assert.equal(await page.locator('#reader-note-section option[value="bridge"]').count(),1);
await page.setViewportSize({width:390,height:844});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
console.log('PASS two-level figure navigation, related-prose ownership, cross-figure parent ownership, direct figure jump, precise note locations, no backup UI and narrow layout');
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
