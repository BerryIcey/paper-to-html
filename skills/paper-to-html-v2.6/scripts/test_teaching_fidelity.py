"""Flexible teaching must preserve approved content through build and publication."""
import importlib, json, subprocess, sys, tempfile, unittest
from pathlib import Path
from teaching_contract import render_teaching, check_reader_html

BLOCKS={'blocks':[
 {'title':'先看这一列','text':'一列对应一名患者；53 名患者约占 31%。'},
 {'title':'核对符号','items':['星号表示复杂核型。','色块表示异常类型。']},
 {'title':'对照读数','table':{'headers':['位置','含义'],'rows':[['NPM1 行','患者层面的异常标记']]}}
]}

def panel(teaching):
    protected=''.join(f'<p id="protect-{i}" data-reader-preserve="{kind}">{text}</p>' for i,(kind,text) in enumerate([
        ('caption-original','Original caption.'),('caption-translation','完整图注翻译。'),
        ('summary','已有总结。'),('author-conclusion','作者的结果与判断：保留原有答案。')]))
    return '<section id="results" data-section="结果"><div id="fig-a" data-reader-panel="a"><div id="fig-a-text" class="reader-text">'+protected+teaching+'</div></div></section>'

class FlexibleTeachingTests(unittest.TestCase):
    def test_short_blocks_need_no_fixed_four_regions(self):
        html=panel(render_teaching(BLOCKS,'guide'))
        self.assertEqual(check_reader_html(html)[0],[])
        self.assertIn('data-reader-teaching="v2"',html)
        self.assertNotIn('带着当前问题读图',html)
        self.assertIn('53 名患者约占 31%',html)

    def test_protected_parts_are_required_in_order(self):
        html=panel(render_teaching(BLOCKS,'guide'))
        for changed in [html.replace('data-reader-preserve="summary"','data-reader-preserve="unused"'),
                        html.replace('data-reader-preserve="summary"','data-reader-preserve="author-conclusion"')]:
            self.assertTrue(check_reader_html(changed)[0])

    def test_flexible_text_is_escaped_and_empty_blocks_rejected(self):
        html=render_teaching({'blocks':[{'text':'<script>bad()</script>'}]},'safe')
        self.assertNotIn('<script>',html)
        for data in [{'blocks':[]},{'blocks':[{'title':'只有标题'}]},{'blocks':[{'table':{'headers':['A','B'],'rows':[['one']]}}]}]:
            with self.assertRaises(ValueError):render_teaching(data,'bad')

    def test_modern_unit_cannot_create_empty_baseline_without_text_container(self):
        fidelity=importlib.import_module('teaching_fidelity')
        html=panel(render_teaching(BLOCKS,'guide')).replace('class="reader-text"','class="wrong-container"')
        self.assertTrue(check_reader_html(html)[0])
        with self.assertRaises(ValueError):fidelity.make_manifest(html)

    def test_hidden_ancestor_is_detected(self):
        fidelity=importlib.import_module('teaching_fidelity')
        html=panel(render_teaching(BLOCKS,'guide'));baseline=fidelity.make_manifest(html)
        for extra in ['hidden','style="display:none"','aria-hidden="true"']:
            changed=html.replace('<section id="results"',f'<section {extra} id="results"')
            self.assertTrue(fidelity.check_fidelity(changed,baseline))

    def test_baseline_preserves_inline_text_order_and_ignores_term_markup(self):
        fidelity=importlib.import_module('teaching_fidelity')
        html=panel(render_teaching(BLOCKS,'guide'))
        baseline=fidelity.make_manifest(html)
        marked=html.replace('53 名患者','<a href="#fig-a">53</a> 名患者')
        self.assertEqual(fidelity.check_fidelity(marked,baseline),[])
        self.assertTrue(fidelity.check_fidelity(html.replace('53 名患者','35 名患者'),baseline))

    def test_deleted_units_blocks_and_hidden_text_are_detected(self):
        fidelity=importlib.import_module('teaching_fidelity')
        html=panel(render_teaching(BLOCKS,'guide'));baseline=fidelity.make_manifest(html)
        for changed in ['',html.replace('星号表示复杂核型。',''),html.replace('id="guide-block-0"','id="guide-block-0" hidden')]:
            self.assertTrue(fidelity.check_fidelity(changed,baseline))

    def test_build_publish_require_baseline_and_reject_content_loss(self):
        fidelity=importlib.import_module('teaching_fidelity')
        scripts=Path(__file__).parent
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);source=root/'content.html';built=root/'built.html';baseline=root/'baseline.json'
            html=panel(render_teaching(BLOCKS,'guide'));source.write_text(html,'utf-8')
            baseline.write_text(json.dumps(fidelity.make_manifest(html),ensure_ascii=False),'utf-8')
            original_baseline=baseline.read_bytes()
            build=[sys.executable,str(scripts/'build_reader.py'),'--content',str(source),'--paper-id','fidelity-test','--out',str(built)]
            missing=subprocess.run(build,capture_output=True,text=True,encoding='utf-8')
            self.assertNotEqual(missing.returncode,0);self.assertFalse(built.exists())
            run=subprocess.run(build+['--teaching-baseline',str(baseline)],capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(run.returncode,0,run.stdout+run.stderr)
            publish=[sys.executable,str(scripts/'publish_reader.py'),'--root',str(root),'--source',str(built),'--title','test']
            missing=subprocess.run(publish,capture_output=True,text=True,encoding='utf-8')
            self.assertNotEqual(missing.returncode,0);self.assertFalse((root/'paper-reading.html').exists())
            run=subprocess.run(publish+['--teaching-baseline',str(baseline)],capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(run.returncode,0,run.stdout+run.stderr)
            published=(root/'paper-reading.html').read_bytes()
            self.assertEqual(fidelity.check_fidelity(published.decode('utf-8'),json.loads(baseline.read_text('utf-8'))),[])
            built.write_text(built.read_text('utf-8').replace('53 名患者','35 名患者'),'utf-8')
            failed=subprocess.run(publish+['--teaching-baseline',str(baseline)],capture_output=True,text=True,encoding='utf-8')
            self.assertNotEqual(failed.returncode,0)
            self.assertEqual((root/'paper-reading.html').read_bytes(),published)
            self.assertEqual(baseline.read_bytes(),original_baseline)

if __name__=='__main__':unittest.main()
