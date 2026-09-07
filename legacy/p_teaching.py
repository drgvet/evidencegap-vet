import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)));sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))),'lib'))
from shell import page

import os as _os, records as _records
STEPS = _records.as_steps(_os.path.join(
    _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
    'content', 'teaching-steps.txt'))

steps_html = ''.join(
  f'<div class="step"><div class="n">{i+1}</div><div><h3>{t}</h3>{body}'
  f'<p class="bad"><b>Warning sign</b>{bad}</p></div></div>'
  for i,(t,body,bad) in enumerate(STEPS))

TRAPS = [
 ("Surrogate endpoint","A measurement standing in for something that matters. Wall thickness instead of heart failure. Useful for deciding what to study next, weak for deciding what to prescribe."),
 ("Composite endpoint","Several outcomes bundled into one count, so a hospital visit and a death score the same. A positive composite is often driven by the least serious part of it."),
 ("Non-inferiority","The study set out to show the new treatment is not much worse, not that it is better. The margin for \"not much worse\" is chosen by the investigators. Always look at what it was."),
 ("Post hoc","Decided after seeing the data. A post hoc subgroup, endpoint or analysis is a suggestion for the next study, not a result."),
 ("Per protocol","Animals that dropped out were excluded from the analysis. If the sickest ones dropped out, the treatment looks better than it was. Intention to treat keeps everyone in and is the honest version."),
 ("Confounding by indication","The treated animals were different from the untreated ones before anything was given, usually sicker. Very common in retrospective work, and it can point a result in either direction."),
 ("Underpowered","Too few animals to detect a difference that would matter. A negative result from a small study means nobody looked hard enough, not that there is no effect."),
 ("Alpha","The threshold for calling something significant, conventionally 0.05. If a paper sets it higher, or makes several comparisons without adjusting, false positives become likely."),
]
traps = ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a,b in TRAPS)

body = f"""
<div class="kicker">Teaching</div>
<h1>How to read a paper</h1>
<p class="standfirst">This page sets out a method for working out whether a study should change what you do. It is written for students, and for anyone in general practice who does not have an hour to spend on a single paper.</p>
<div class="meta"><span>Six questions</span><span>About ten minutes per paper</span><span>Revised August 2026</span></div>

<section>
  <h2>Before you start</h2>
  <p>Most of us were taught what the literature concludes, and far fewer of us were taught how to check whether a conclusion is any good. Appraisal is a separate skill from clinical knowledge, it can be learned in an afternoon, and it travels with you into every part of practice.</p>
  <p>You do not need statistics in order to do this, but you do need to know which questions to ask and in what order to ask them. Six questions will get you most of the way, and all six can be answered from the abstract and the methods without reading the discussion at all.</p>
  <p>One habit is worth adopting before any of the six questions, which is to read the methods before the abstract. The abstract is where the authors tell you what they would like you to conclude, whereas the methods are where they tell you what they actually did.</p>
</section>

<section>
  <h2>The six questions</h2>
  {steps_html}
</section>

<section>
  <h2>Words that should slow you down</h2>
  <p>The terms below turn up constantly, and each of them changes how much weight a result will carry.</p>
  <div class="tscroll">
  <table class="traps">
    <thead><tr><th>Term</th><th>What it means for you</th></tr></thead>
    <tbody>{traps}</tbody>
  </table>
  </div>
  <p class="scrollhint">Scroll sideways for the full table.</p>
</section>

<section>
  <h2>Turning the answers into a mark</h2>
  <p>Once you have been through the six questions you will have a sense of how much the paper can carry. Resist the urge to turn that into a single number based on what kind of study it was. A design ladder, on which a randomised trial always outranks a cohort study, breaks in a way that matters, because a small industry-funded trial measuring a stand-in outcome would come out ahead of a large and carefully conducted observational study. That ordering is wrong, and the grading systems used in human medicine avoid it by separating two questions rather than one. This site does the same.</p>
  <div class="gradekey">
    <div><div class="k"><span class="cf cf--high">High certainty</span></div><div class="v">Replicated, with consistent findings</div></div>
    <div><div class="k"><span class="cf cf--moderate">Moderate certainty</span></div><div class="v">One sound study, with material limitations</div></div>
    <div><div class="k"><span class="cf cf--low">Low certainty</span></div><div class="v">Serious limitations, or observational only</div></div>
    <div><div class="k"><span class="cf cf--verylow">Very low certainty</span></div><div class="v">Insufficient to support a claim</div></div>
    <div><div class="k"><span class="cf cf--none">No evidence</span></div><div class="v">Not studied</div></div>
  </div>
  <p style="margin-top:22px"><strong>Start from the design, then move down from it.</strong> A randomised trial starts high. Rate the certainty down for whatever your six questions turned up, which will usually be risk of bias, too few animals, a population unlike your patient, or results that disagree between studies. Rate it up for a large effect that appears consistently across different groups. This is how GRADE works, and it is the reason a downgraded trial and a case series can end up in the same place.</p>
  <p><strong>One hard rule about stand-in outcomes.</strong> If the only evidence measures wall thickness, ectopic counts or a blood value rather than something the animal experiences, it cannot rise above the bottom band, whatever the design. This cap is an editorial rule adopted here rather than a part of GRADE. The principle behind it comes from SORT, the grading scheme used in human family medicine, which gives its weakest recommendation grade to evidence resting on disease-oriented outcomes; SORT grades recommendations rather than bodies of evidence, so the hard cap is a choice made here. It exists because improvements in a measurement are not reliably followed by improvements in the patient.</p>
  <p><strong>Record what the evidence points to as a separate mark.</strong> Certainty and direction are different questions, and you can hold low certainty that something helps, or reasonable certainty that it does nothing at all. Keeping the two apart prevents "we do not know" from being read as "it does not work", and prevents "no evidence of benefit" from being read as "evidence of no benefit". These two pairs are confused constantly, and in both directions.</p>
  <p class="note">The ACVIM guidelines on mitral valve disease already define their weakest evidence category as including <em>randomised</em> studies that carry limitations of design or execution, so the specialty has published the same point.</p>
</section>

<section>
  <h2>Practise on something</h2>
  <p>Reading about appraisal achieves less than working through one paper yourself. Two worked examples on this site, both from feline cardiology, are suitable for that purpose.</p>
  <ul class="plain">
    <li>
      <h3><a href="review-rapamycin.html">Rapamycin for subclinical HCM</a></h3>
      <p class="small">This is a licensed drug for which the endpoint was chosen after the data came in, and for which the reported effect is smaller than the measurement error of the test used to find it. It is good practice for questions four and five.</p>
    </li>
    <li>
      <h3><a href="review-steroids-chf.html">Steroids and heart failure in cats</a></h3>
      <p class="small">This is a belief taught almost everywhere, resting on two papers that do not support it. It is good practice for question two, and for recognising when a temporal association is being asked to do work it cannot do.</p>
    </li>
  </ul>
  <p style="margin-top:20px">Work through the six questions on each paper before reading the commentary, and then compare where your reading and the commentary agree.</p>
</section>

<section>
  <h2>Checking that a reference is real</h2>
  <p>Checking a reference is quick and it is worth doing. References are miscopied between papers for years at a time, and software that writes text for you will produce citations that look entirely plausible and do not exist.</p>
  <ol class="numbered">
    <li>
      <h3>Search the title, not the authors</h3>
      <p>Paste the exact title into PubMed, and if nothing comes back try Crossref and the journal's own archive, since a good deal of the veterinary literature is not indexed in PubMed at all. Author names get misspelled and initials get dropped, but a title either matches or it does not.</p>
    </li>
    <li>
      <h3>Resolve the DOI</h3>
      <p>Put doi.org/ in front of the identifier, and it should land on the paper itself. A DOI that fails to resolve is worth a second look, but it is not proof of invention on its own: newly registered DOIs can take time to activate, and links get mistyped or truncated. Check the title in PubMed, Crossref or the journal's own archive before concluding anything. Some journals do not issue DOIs at all, so a missing one means nothing either way.</p>
    </li>
    <li>
      <h3>Check the volume, year and pages against the record</h3>
      <p>Volume and page numbers are where genuine errors hide. A real paper carrying the wrong page range has usually been copied from another paper's reference list rather than read.</p>
    </li>
  </ol>
</section>

<section>
  <h2>The whole thing on one card</h2>
  <div class="checklist">
    <ol>
      <li>Who was in it, and are they like my patient?</li>
      <li>What was it compared with?</li>
      <li>Is the outcome something the animal cares about?</li>
      <li>Was success defined before they looked at the data?</li>
      <li>How big is the effect, and can the test measure it?</li>
      <li>Who paid, and who ran the numbers?</li>
    </ol>
  </div>
  <p class="note" style="margin-top:16px">This page prints cleanly if you want it on paper for a journal club, using your browser's print command.</p>
</section>

<section>
  <h2>Still to come</h2>
  <p>Worked appraisals of common presentations are planned, together with a short glossary of the statistics that recur in veterinary trials and a set of discussion prompts for journal clubs. If there is a paper you would like taken apart here, write to <a href="mailto:contact@evidencegap.vet">contact@evidencegap.vet</a>.</p>
</section>
"""

open('teaching.html','w',encoding='utf-8').write(page(
 'teaching.html','How to read a paper &mdash; evidencegap.vet',
 'A six-question method for working out whether a veterinary study should change what you do. For students and general practitioners.',
 body, width='mid'))
print('wrote teaching.html')
