import sys, json; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)));sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))),'lib'))
from shell import page

ID = {q['title']: q['id'] for q in json.load(open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'questions.json')))}

TB = {'close':  ('Close analogue',   'close'),
      'partial':('Partial analogue', 'part'),
      'poor':   ('Poor analogue',    'poor'),
      'none':   ('No analogue',      'noan')}

# Each block: id, drug or decision class, what the human trials show,
# how far the analogy carries, and the veterinary questions it bears on.
import os as _os, records as _records
CATS, HUMAN_REFS = _records.as_classes(_os.path.join(
    _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
    'content', 'human-evidence.txt'))

NOEQ = [
 ("Pimobendan in preclinical stage B2 disease",
  "Inotropes are not given to people before symptoms appear, so no trial exists at this stage."),
 ("Spironolactone with benazepril to delay the onset of heart failure",
  "The corresponding human trials enrolled patients who already had symptoms."),
 ("Diet change and taurine in diet-associated dilated cardiomyopathy",
  "There is no equivalent condition in people, and therefore no equivalent trial."),
 ("Screening intervals in at-risk breeds",
  "Family screening in inherited human cardiomyopathy is set by guideline rather than by trial."),
 ("Any therapy that delays the onset of heart failure in hypertrophic cardiomyopathy",
  "The question is equally unanswered in humans, where no trial has tested delay of onset."),
]

WORD = {2:'Two',3:'Three',4:'Four',5:'Five',6:'Six',7:'Seven',8:'Eight',9:'Nine',
        10:'Ten',11:'Eleven',12:'Twelve'}

def qlinks(titles):
    return '<span class="sep"> &middot; </span>'.join(
      f'<a href="gapmap.html#{ID[t]}">{t}</a>' for t in titles)

blocks = ''
for cid, name, tr, trials, transfer, qs in CATS:
    label, cls = TB[tr]
    blocks += f"""
<section class="hcat" id="{cid}">
  <div class="hcathead"><h2>{name}</h2><span class="tbadge tb--{cls}">{label}</span></div>
  <div class="hgrid">
    <div class="hcol">
      <p class="hlab">What the human trials show</p>
      {trials}
    </div>
    <div class="hcol">
      <p class="hlab">How far it carries across</p>
      {transfer}
    </div>
  </div>
  <p class="xref"><span class="llab">Bears on</span>{qlinks(qs)}</p>
</section>"""

noeq = ''.join(
  f'<li><h3><a href="gapmap.html#{ID[t]}">{t}</a></h3><p class="small">{why}</p></li>'
  for t, why in NOEQ)

key = ''.join(
  f'<div><div class="k"><span class="tbadge tb--{TB[k][1]}">{TB[k][0]}</span></div>'
  f'<div class="v">{v}</div></div>'
  for k, v in [('close',"Same drug class, comparable question, comparable population"),
               ('partial',"Same class or same question, but the disease or the drug differs in ways that matter"),
               ('poor',"Superficially similar, materially different lesion or setting"),
               ('none',"No human trial addresses the question")])

refs = ''.join(f'<li>{r}</li>' for r in HUMAN_REFS)

body = f"""
<div class="kicker">Comparative evidence</div>
<h1>The same drugs, in people</h1>
<p class="standfirst">This page sets out what the human trials tested, what they found, and how far each result can reasonably be carried into small-animal cardiology. It is organised by drug class rather than by disease, because the drug class is what travels between species.</p>
<div class="meta"><span>{WORD[len(CATS)]} intervention classes</span><span>{len(HUMAN_REFS)} human trials cited</span><span>Revised August 2026</span></div>

<section>
  <h2>How far the comparison can be carried</h2>
  <p>Human and small-animal cardiac disease are not the same disease. The human heart-failure trials enrolled patients with predominantly ischaemic or idiopathic systolic dysfunction, whereas the commonest canine cardiac disease is a primary valvular volume overload in a ventricle with normal coronary arteries. Human hypertrophic cardiomyopathy is a sarcomeric genetic disorder, while feline hypertrophic cardiomyopathy is largely of unknown cause. Cardiac embolism in humans arises from atrial fibrillation and causes stroke, whereas in cats it arises from atrial enlargement and causes distal aortic obstruction, usually in an animal in sinus rhythm.</p>
  <p>None of those differences makes the human literature irrelevant, and none of them makes it decisive either. Drug classes travel further between species than diseases do. A phosphodiesterase-3 inhibitor does the same thing to a myocyte in either species, but whether the consequence is the same depends on the substrate it acts on, and the substrate is exactly what differs.</p>
  <p>This page therefore does not claim that a human result determines the veterinary answer. Each class is set out with what was tested, what the trial showed, and an explicit judgement of how close the analogy is. Where a class behaved badly in a large human trial, that is a reason to look for the equivalent signal in the veterinary data and to note when nobody has looked for it. It is not, on its own, evidence that the signal is present.</p>
  <div class="gradekey">{key}</div>
  <p class="note" style="margin-top:18px">The analogy judgements are the editor's own and are open to argument. The trial results are not open in the same way, because every name, figure and effect direction below was checked against the primary report, and the citations are listed at the foot of the page.</p>
</section>

{blocks}

<section>
  <h2>Entries with no human counterpart</h2>
  <p>{WORD[len(NOEQ)]} entries on the map have nothing to compare against. These are recorded separately, because an absent comparison is often mistaken for an unfavourable one.</p>
  <ul class="plain">{noeq}</ul>
</section>

<section>
  <h2>Human trials cited</h2>
  <ol class="reflist">{refs}</ol>
</section>

<section>
  <h2>Status</h2>
  <p>This page covers the intervention classes represented on the cardiology gap map, and it will grow as the map does. Corrections are welcome, as are human trials that should appear here and do not, and the <a href="about.html">about page</a> explains how to send them.</p>
</section>
"""

open('human-evidence.html','w',encoding='utf-8').write(page(
 'human-evidence.html','The same drugs, in people &mdash; evidencegap.vet',
 'What the human trials of the same drug classes tested and found, and how far each result carries into small-animal cardiology.',
 body, width='mid'))
print('wrote human-evidence.html;', len(CATS), 'classes,', len(HUMAN_REFS), 'references')
