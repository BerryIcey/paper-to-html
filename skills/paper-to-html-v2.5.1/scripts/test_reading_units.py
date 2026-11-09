"""Explicit granularity decisions must work through build and publish."""
import unittest, tempfile, subprocess, sys
from pathlib import Path
from teaching_contract import check_reader_html, render_teaching

DATA={'question':['比较相同条件下的对照、干预与救援。'],
      'legend':[{'visual':'纵轴存活比例','meaning':'相对对应对照的存活，单位%。'}],
      'reasoning':['干预降低存活，救援使存活回升；是否完全恢复需看原值。'],
      'next_question':'救援支持该靶点参与效应，但尚需排除非特异作用。'}

def brief(reason='仪器外观不承担独立结论，保留身份与原图注即可。'):
 return ('<div id="setup" data-reader-panel="a" data-reader-teaching-mode="brief" '
         'data-reader-teaching-reason="'+reason+'"><div class="reader-text">'
         '<p>图1a：成像仪器外观，使用方式见实验设计。</p></div></div>')

def shared(target='comparison'):
 return ('<div id="rescue" data-reader-panel="b" data-reader-teaching-mode="shared" '
         'data-reader-teaching-target="'+target+'" '
         'data-reader-teaching-reason="同一问题的干预与救援需要合并比较。">'
         '<div class="reader-text"><p>本面板是救援组，与共同讲解中的对照及干预组配对。</p>'
         '<a href="#'+target+'" data-reader-return>对照、干预与救援一起看</a></div></div>')

def group():
 return '<section id="comparison" data-reader-teaching-unit>'+render_teaching(DATA,'comparison')+'</section>'

class ReadingUnitTests(unittest.TestCase):
 def test_simple_source_figure_does_not_need_four_filler_blocks(self):
  self.assertEqual(check_reader_html(brief())[0],[])
 def test_simplification_requires_recorded_reason(self):
  self.assertTrue(check_reader_html(brief(''))[0])
 def test_shared_teaching_accepts_real_group_and_local_context(self):
  self.assertEqual(check_reader_html(shared()+group())[0],[])
 def test_missing_shared_target_is_rejected(self):
  self.assertTrue(check_reader_html(shared('missing')+group())[0])
 def test_reference_cannot_replace_detailed_teaching(self):
  self.assertTrue(check_reader_html(shared('setup')+brief())[0])
 def test_merged_complex_unit_still_needs_reasoning(self):
  incomplete=group().replace('data-teaching-role="reasoning"','data-teaching-role="unused"')
  self.assertTrue(check_reader_html(shared()+incomplete)[0])
 def test_unmarked_complex_panel_remains_strict(self):
  self.assertTrue(check_reader_html('<div id="heatmap" data-reader-panel="a"><p>红高蓝低。</p></div>')[0])
 def test_unknown_mode_cannot_silently_skip_review(self):
  self.assertTrue(check_reader_html(brief().replace('"brief"','"skip"'))[0])
 def test_build_and_publish_accept_a_mixed_reading_plan(self):
  scripts=Path(__file__).resolve().parent
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);source=root/'content.html';built=root/'built.html'
   source.write_text('<section id="results" data-section="结果">'+brief()+shared()+group()+'</section>','utf-8')
   build=subprocess.run([sys.executable,str(scripts/'build_reader.py'),'--content',str(source),'--paper-id','reading-unit-test','--out',str(built)],capture_output=True,text=True,encoding='utf-8')
   self.assertEqual(build.returncode,0,build.stdout+build.stderr)
   publish=subprocess.run([sys.executable,str(scripts/'publish_reader.py'),'--root',str(root),'--source',str(built),'--title','test'],capture_output=True,text=True,encoding='utf-8')
   self.assertEqual(publish.returncode,0,publish.stdout+publish.stderr)
   self.assertTrue((root/'paper-reading.html').exists())

if __name__=='__main__':unittest.main()
