import unittest
from concept_markup import mark_concepts

def entry(id,alias,category='method',**extra):
 return {'id':id,'aliases':[alias],'category':category,'decision':'core','target':'concept-'+id,**extra}
def page(text):return '<section><p id="en" class="original">'+text+'</p><p id="cn" class="translation">相位边界 相位边界</p><details id="concept-phase" data-reader-card><summary>概念</summary><p>phase boundary</p></details></section>'
class Tests(unittest.TestCase):
 def test_original_translation_and_first_per_paragraph(self):
  e=entry('phase','phase boundary','structure');e['aliases'].append('相位边界')
  s,report=mark_concepts(page('phase boundary and phase boundary'),{'concepts':[e]})
  self.assertEqual(s.count('class="term term-structure"'),2)
  self.assertIn('phase boundary and phase boundary',s.replace('<a class="term term-structure" data-concept-id="phase" href="#concept-phase">','').replace('</a>',''))
 def test_unicode_hyphen_and_longest_expression(self):
  body='<p id="p">cross–validation cross-validation error</p><details id="concept-long" data-reader-card></details><details id="concept-short" data-reader-card></details>'
  s,_=mark_concepts(body,{'concepts':[entry('long','cross-validation error'),entry('short','cross-validation')]})
  self.assertIn('>cross–validation</a>',s);self.assertIn('>cross-validation error</a>',s)
 def test_skip_existing_links_code_attributes_and_cards(self):
  body='<p id="p" title="phase boundary"><a href="/x">phase boundary</a><code>phase boundary</code> phase boundary</p><details id="concept-phase" data-reader-card><p>phase boundary</p></details>'
  s,_=mark_concepts(body,{'concepts':[entry('phase','phase boundary')]})
  self.assertEqual(s.count('data-concept-id='),1);self.assertIn('title="phase boundary"',s)
 def test_ambiguous_alias_requires_disjoint_scopes(self):
  body='<p id="p1">instrument</p><p id="p2">instrument</p><details id="concept-a" data-reader-card></details><details id="concept-b" data-reader-card></details>'
  with self.assertRaises(ValueError):mark_concepts(body,{'concepts':[entry('a','instrument'),entry('b','instrument')]})
  s,_=mark_concepts(body,{'concepts':[entry('a','instrument',scope_ids=['p1']),entry('b','instrument',scope_ids=['p2'])]})
  self.assertIn('href="#concept-a">instrument',s);self.assertIn('href="#concept-b">instrument',s)
 def test_missing_target_rejected(self):
  with self.assertRaises(ValueError):mark_concepts('<p id="p">phase boundary</p>',{'concepts':[entry('phase','phase boundary')]})
 def test_substrings_and_excluded_decisions(self):
  s,_=mark_concepts(page('microphase boundary phase boundary'),{'concepts':[entry('phase','phase boundary')]})
  self.assertEqual(s.count('data-concept-id='),1)
  e=entry('phase','phase boundary');e['decision']='excluded';s,_=mark_concepts(page('phase boundary'),{'concepts':[e]});self.assertNotIn('data-concept-id=',s)
 def test_child_card_target_and_repeat_build(self):
  body='<p id="p">phase boundary</p><details id="group" data-reader-card><p id="concept-phase">定义</p></details>'
  data={'concepts':[entry('phase','phase boundary')]}
  s,r=mark_concepts(body,data);ss,rr=mark_concepts(s,data)
  self.assertEqual(s,ss);self.assertEqual(r['linked_occurrences'],rr['linked_occurrences'])
 def test_invalid_scope_rejected(self):
  with self.assertRaises(ValueError):mark_concepts(page('phase boundary'),{'concepts':[entry('phase','phase boundary',scope_ids=['absent'])]})
if __name__=='__main__':unittest.main()
