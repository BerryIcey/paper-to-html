"""Regression checks prevent flattened teaching and preserve approved legacy regions."""
import unittest,subprocess,sys,tempfile
from pathlib import Path
from teaching_contract import render_teaching,check_reader_html

def panel(body):return '<div id="fig-a" data-reader-panel="a"><div class="reader-text">'+body+'</div></div>'
class ContractTests(unittest.TestCase):
 def setUp(self):
  self.data={'question':['当前问题、材料和比较的完整解释。','输入经过筛选和汇总成为图中元素的解释。'],'legend':[{'visual':'横轴原标签','meaning':'对象及单位'},{'visual':'此处颜色','meaning':'组别及比较方向'}],'reasoning':['一个真实可定位的结果和实际比较。','从整体与反例推理到认识及限定。'],'next_question':'上一证据仍差什么，以及后续方法为何合适。'}
 def test_flat_text_rejected(self):
  errors,_=check_reader_html(panel('<h4>一步一步读图</h4><p>横轴是功能，颜色越深越显著，说明参与造血。</p>'))
  self.assertTrue(errors)
 def test_render_keeps_question_example_and_next(self):
  rendered=render_teaching(self.data,'f1-a');errors,coverage=check_reader_html(panel(rendered))
  self.assertEqual(errors,[]);self.assertEqual(coverage,['fig-a'])
  self.assertIn(self.data['question'][1],rendered);self.assertIn(self.data['reasoning'][0],rendered);self.assertIn(self.data['next_question'],rendered)
 def test_empty_statistics_mapping_rejected(self):
  self.data['legend'][1]['meaning']=''
  with self.assertRaises(ValueError):render_teaching(self.data,'x')
 def test_missing_current_question_rejected(self):
  self.data.pop('question')
  with self.assertRaises(ValueError):render_teaching(self.data,'x')
 def test_mismatched_region_order_rejected(self):
  rendered=render_teaching(self.data,'x').replace('data-teaching-role="question"','data-teaching-role="reasoning"',1)
  self.assertTrue(check_reader_html(panel(rendered))[0])
 def test_text_is_escaped(self):
  self.data['question'][0]='<script>untrusted()</script>'
  self.assertNotIn('<script>',render_teaching(self.data,'x'))
 def test_simple_panel_does_not_require_padding(self):
  self.data['question']=self.data['question'][:1]
  self.data['reasoning']=self.data['reasoning'][:1]
  self.data['legend']=self.data['legend'][:1]
  self.assertEqual(check_reader_html(panel(render_teaching(self.data,'simple')))[0],[])
 def test_non_applicable_legend_requires_reason(self):
  self.data['legend']=[]
  with self.assertRaises(ValueError):render_teaching(self.data,'simple')
  self.data['legend_not_applicable']='此图为无编码符号的说明图；对象已在当前问题中指明。'
  self.assertEqual(check_reader_html(panel(render_teaching(self.data,'simple')))[0],[])
 def test_complete_legacy_layout_preserved(self):
  legacy='<h4>带着当前问题读图</h4><p>问题与设计。</p><p>输入到元素。</p><h4>本图图例与元素</h4><table><tr><td>轴</td><td>对象</td></tr><tr><td>色</td><td>读法</td></tr></table><h4>从实际结果读到判断</h4><p>实际例子和判断。</p><p>限制及下一问题。</p>'
  self.assertEqual(check_reader_html(panel(legacy))[0],[])
 def test_build_and_publish_cannot_bypass_flat_teaching(self):
  scripts=Path(__file__).resolve().parent
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);source=root/'content.html'
   source.write_text('<html><body><section id="result" data-section="结果">'+panel('<p>一段压缩说明。</p>')+'</section></body></html>','utf-8')
   for command in [
    [str(scripts/'build_reader.py'),'--content',str(source),'--paper-id','regression','--out',str(root/'built.html')],
    [str(scripts/'publish_reader.py'),'--root',str(root),'--source',str(source),'--title','regression']
   ]:
    result=subprocess.run([sys.executable,*command],capture_output=True,text=True,encoding='utf-8')
    self.assertNotEqual(result.returncode,0)
   self.assertFalse((root/'built.html').exists())
   self.assertFalse((root/'paper-reading.html').exists())
if __name__=='__main__':unittest.main()
