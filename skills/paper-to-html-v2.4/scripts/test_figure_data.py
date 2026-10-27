import unittest
from figure_data import render_figure_data
CONTENT='<section id="s" data-section="1"><div id="p" data-reader-panel="a"><div class="reader-image"><img src="data:image/png;base64,AA==" alt="原图"><p>放大提示</p></div><div class="reader-text">原文保持</div></div></section>'
def manifest():return {'panels':{'p':{'source_locator':'Fig1a','layers':[{'data':'ATAC-seq','processing':'motif分数'}]}}}
class FigureDataTests(unittest.TestCase):
 def test_caption_is_below_image_not_in_text(self):
  out=render_figure_data(CONTENT,manifest());self.assertIn('原文保持',out);self.assertIn('src="data:image/png;base64,AA=="',out);self.assertLess(out.index('放大提示'),out.index('p-data-source'));self.assertLess(out.index('p-data-source'),out.index('class="reader-text"'))
 def test_joint_layers_and_escaping(self):
  m=manifest();m['panels']['p']['layers'].append({'label':'外部参考','data':'K562 <p300>','processing':'参考 & 轨道'});out=render_figure_data(CONTENT,m);self.assertIn('外部参考',out);self.assertIn('&lt;p300&gt;',out);self.assertIn('&amp;',out)
 def test_bad_target(self):
  m=manifest();m['panels']['absent']=m['panels'].pop('p')
  with self.assertRaisesRegex(ValueError,'Unknown'):render_figure_data(CONTENT,m)
 def test_missing_provenance(self):
  m=manifest();del m['panels']['p']['source_locator']
  with self.assertRaisesRegex(ValueError,'locator'):render_figure_data(CONTENT,m)
 def test_missing_measurement(self):
  m=manifest();del m['panels']['p']['layers'][0]['processing']
  with self.assertRaisesRegex(ValueError,'processing'):render_figure_data(CONTENT,m)
 def test_no_image_container(self):
  with self.assertRaisesRegex(ValueError,'reader-image'):render_figure_data(CONTENT.replace('class="reader-image"','class="other"'),manifest())
 def test_duplicates_rejected(self):
  out=render_figure_data(CONTENT,manifest())
  with self.assertRaisesRegex(ValueError,'Duplicate'):render_figure_data(out,manifest())
if __name__=='__main__':unittest.main()
