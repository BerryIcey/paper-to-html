import unittest, subprocess, sys, tempfile, json
from pathlib import Path
from concept_markup import mark_concepts
from legend_config import render_legend

def row(category):return {'id':'x','aliases':['目标词'],'category':category,'decision':'core','target':'card'}
BODY='<section id="s" data-section="结果"><p id="p">目标词</p><details id="card" data-reader-card><summary>定义</summary></details></section>'

class LegendTests(unittest.TestCase):
 def test_biology_uses_simple_identity_and_only_used_categories(self):
  manifest={'domain':'biology','concepts':[row('gene-protein')]}
  content,_=mark_concepts(BODY,manifest);legend,css=render_legend(manifest,content)
  self.assertIn('基因与蛋白',legend);self.assertNotIn('细胞与亚型',legend);self.assertIn('.term-gene-protein',css)
 def test_other_domain_accepts_article_specific_categories(self):
  m={'domain':'engineering','legend':[{'id':'material','label':'材料','color':'#d9e8fa'}],'concepts':[row('material')]}
  content,_=mark_concepts(BODY,m);legend,_=render_legend(m,content)
  self.assertIn('材料',legend);self.assertNotIn('基因',legend)
 def test_other_domain_does_not_fall_back_to_biology(self):
  with self.assertRaises(ValueError):render_legend({'domain':'engineering','concepts':[]},BODY)
 def test_biology_colors_are_fixed(self):
  with self.assertRaises(ValueError):render_legend({'domain':'biology','legend':[{'id':'method','label':'方法','color':'#ffffff'}],'concepts':[]},BODY)
 def test_unused_categories_not_shown(self):
  legend,_=render_legend({'domain':'biology','concepts':[row('gene-protein')]},BODY)
  self.assertNotIn('基因与蛋白',legend)
 def test_invalid_custom_category_or_color_rejected(self):
  for spec in [{'id':'bad id','label':'材料','color':'#123456'},{'id':'material','label':'材料','color':'red;display:none'}]:
   with self.assertRaises(ValueError):render_legend({'domain':'engineering','legend':[spec],'concepts':[]},BODY)
 def test_legacy_manifest_keeps_existing_category_identity(self):
  m={'concepts':[row('structure')]};content,_=mark_concepts(BODY,m);legend,_=render_legend(m,content)
  self.assertIn('term-structure',legend);self.assertNotIn('基因',legend)
 def test_build_displays_nonbiology_legend_and_matching_color(self):
  with tempfile.TemporaryDirectory()as tmp:
   r=Path(tmp);(r/'content.html').write_text(BODY,'utf-8');m={'domain':'engineering','legend':[{'id':'material','label':'材料','color':'#d9e8fa'}],'concepts':[row('material')]};(r/'concepts.json').write_text(json.dumps(m,ensure_ascii=False),'utf-8')
   p=subprocess.run([sys.executable,str(Path(__file__).with_name('build_reader.py')),'--content',str(r/'content.html'),'--concepts',str(r/'concepts.json'),'--paper-id','test','--out',str(r/'out.html')],capture_output=True,text=True,encoding='utf-8')
   self.assertEqual(p.returncode,0,p.stderr);out=(r/'out.html').read_text('utf-8');self.assertIn('term-material',out);self.assertIn('>材料</span>',out);self.assertNotIn('>基因与蛋白</span>',out)

if __name__=='__main__':unittest.main()
