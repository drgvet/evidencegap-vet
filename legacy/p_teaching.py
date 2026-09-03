import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)));sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))),'lib'))
from shell import page

STEPS = [
 ("Who was in it, and are they like my patient?",
  "<p>Species, breed, age, and how sick they were at the start. A trial in young purpose-bred beagles "
  "tells you very little about a fourteen-year-old cat with kidney disease. Check how many animals were "
  "in each group, not just the total. A study of sixty cats split three ways is three studies of twenty.</p>",
  "Numbers only given as a total. Entry criteria so narrow that almost nobody in your waiting room would qualify."),
 ("What was it compared with?",
  "<p>If there was no control group, there is no comparison, and anything that got better might have got "
  "better anyway. Look for what the control animals received. Placebo is the strongest comparison. "
  "Standard treatment is useful. Nothing at all, or a group assembled afterwards from records, is much weaker.</p>",
  "\"Cats improved after treatment.\" Improved compared with what?"),
 ("Was the outcome something the animal cares about?",
  "<p>Survival, freedom from clinical signs, avoiding a hospital admission. Those matter. A number on an "
  "echo, a blood value, a score on a scale, are stand-ins for what matters, and stand-ins can move without "
  "the animal being any better off. Drugs get licensed on stand-ins all the time.</p>",
  "The paper measures wall thickness or a biomarker, and the discussion talks about survival."),
 ("Did they decide what counted as success before they looked?",
  "<p>This is the one most people skip, and it does more damage than anything else on this list. If the "
  "outcome was chosen after the data came in, or a subgroup appeared that was not planned, the result is a "
  "hypothesis and not a finding. Look in the methods for the word prespecified. Look in the results for a "
  "subgroup that was not mentioned in the methods.</p>",
  "A headline result that lives in one subgroup, and that subgroup is described for the first time in the results section."),
 ("How big was the effect, and could they even measure it?",
  "<p>Statistically significant does not mean big enough to matter. Find the actual difference between the "
  "groups, with units. Then ask whether the equipment can reliably detect a difference that size. Repeat "
  "echo measurements on the same animal vary by a few percent, so an effect of a tenth of a millimetre on a "
  "wall seven millimetres thick is inside the noise.</p>",
  "A p-value in the abstract and no effect size anywhere. Or an effect smaller than the known repeatability of the test."),
 ("Who paid, and who did the analysis?",
  "<p>Industry funding does not make a study wrong. Plenty of good trials are company-funded, because "
  "somebody has to pay. It does mean you read the design more carefully, particularly the choice of "
  "comparison and endpoint. Check whether the sponsor's staff did the statistics, and whether the same small "
  "group of investigators appears on every paper about the drug.</p>",
  "No funding statement at all. Or a conflicts section that reads \"the authors declare none\" on a paper about a product two of them consult for."),
]

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
<p class="standfirst">A method for working out whether a study should change what you do. Written for students and for anyone in general practice who does not have an hour to spend on it.</p>
<div class="meta"><span>Six questions</span><span>About ten minutes per paper</span><span>Revised August 2026</span></div>

<section>
  <h2>Before you start</h2>
  <p>Most of us were taught what the literature concludes. Far fewer of us were taught how to check whether a conclusion is any good. That is a separate skill, it is learnable in an afternoon, and it travels with you into every part of practice.</p>
  <p>You do not need statistics for this. You need to know which questions to ask and in what order. Six of them will get you most of the way, and you can ask all six from the abstract and methods without reading the discussion at all.</p>
  <p>One habit first. Read the methods before the abstract. The abstract is where the authors tell you what they want you to conclude. The methods are where they tell you what they actually did.</p>
</section>

<section>
  <h2>The six questions</h2>
  {steps_html}
</section>

<section>
  <h2>Words that should slow you down</h2>
  <p>These turn up constantly and each one changes how much weight a result will carry.</p>
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
  <p>Once you have been through the six questions you will have a sense of how much the paper can carry. Resist the urge to turn that into a single number based on what kind of study it was. A design ladder, where a randomised trial always beats a cohort study, breaks in a way that matters: a small industry-funded trial measuring a stand-in outcome comes out ahead of a large, careful observational study. That ordering is wrong. The grading systems used in human medicine avoid it by separating two questions, and this site does the same.</p>
  <div class="gradekey">
    <div><div class="k"><span class="cf cf--high">High certainty</span></div><div class="v">Replicated, with consistent findings</div></div>
    <div><div class="k"><span class="cf cf--moderate">Moderate certainty</span></div><div class="v">One sound study, with material limitations</div></div>
    <div><div class="k"><span class="cf cf--low">Low certainty</span></div><div class="v">Serious limitations, or observational only</div></div>
    <div><div class="k"><span class="cf cf--verylow">Very low certainty</span></div><div class="v">Insufficient to support a claim</div></div>
    <div><div class="k"><span class="cf cf--none">No evidence</span></div><div class="v">Not studied</div></div>
  </div>
  <p style="margin-top:22px"><strong>Start from the design, then move down.</strong> A randomised trial starts high. Rate certainty down for the things your six questions turned up: risk of bias, too few animals, a population unlike your patient, results that disagree between studies. Take it up for a large effect that keeps appearing across different groups. This is how GRADE works, and it is why a downgraded trial and a case series can end up in the same place.</p>
  <p><strong>One hard rule about stand-in outcomes.</strong> If the only evidence measures wall thickness, ectopic counts or a blood value rather than something the animal experiences, it cannot rise above the bottom band, whatever the design. That is an editorial rule rather than a part of GRADE. The principle behind it comes from SORT, the grading scheme used in human family medicine, which gives its weakest recommendation grade to evidence resting on disease-oriented outcomes; SORT grades recommendations rather than bodies of evidence, so the hard cap is a choice made here. It exists because improvements in a measurement are not reliably followed by improvements in the patient.</p>
  <p><strong>Say what the evidence points to, separately.</strong> Certainty and direction are different questions. You can hold low certainty that something helps, or reasonable certainty that it does nothing. Keeping them apart stops "we do not know" being read as "it does not work", and stops "no evidence of benefit" being read as "evidence of no benefit". Those get confused constantly, in both directions.</p>
  <p class="note">Worth knowing: the ACVIM guidelines on mitral valve disease already define their weakest evidence category as including <em>randomised</em> studies with limitations of design or execution. The specialty has published the same point.</p>
</section>

<section>
  <h2>Practise on something</h2>
  <p>Reading about this does less than doing it once. Two worked examples on this site, both feline cardiology:</p>
  <ul class="plain">
    <li>
      <h3><a href="review-rapamycin.html">Rapamycin for subclinical HCM</a></h3>
      <p class="small">A licensed drug where the endpoint was chosen after the data came in, and the reported effect is smaller than the measurement error of the test used to find it. Good practice for questions 4 and 5.</p>
    </li>
    <li>
      <h3><a href="review-steroids-chf.html">Steroids and heart failure in cats</a></h3>
      <p class="small">A belief taught everywhere, resting on two papers that do not support it. Good practice for question 2, and for spotting when a temporal association is doing work it cannot do.</p>
    </li>
  </ul>
  <p style="margin-top:20px">Try the six questions on each before you read the commentary, then see where you agree.</p>
</section>

<section>
  <h2>Checking that a reference is real</h2>
  <p>Worth doing, and quick. References get miscopied between papers for years, and software that writes text for you will produce citations that look perfect and do not exist.</p>
  <ol class="numbered">
    <li>
      <h3>Search the title, not the authors</h3>
      <p>Paste the exact title into PubMed, and if nothing comes back try Crossref and the journal's own archive, since a good deal of the veterinary literature is not indexed in PubMed at all. Author names get misspelled and initials get dropped, but a title either matches or it does not.</p>
    </li>
    <li>
      <h3>Resolve the DOI</h3>
      <p>Put doi.org/ in front of it. It should land on the paper. A DOI that fails to resolve is worth a second look, but it is not proof of invention on its own: newly registered DOIs can take time to activate, and links get mistyped or truncated. Check the title in PubMed, Crossref or the journal's own archive before concluding anything. Some journals do not issue DOIs at all, so a missing one means nothing either way.</p>
    </li>
    <li>
      <h3>Check the volume, year and pages against the record</h3>
      <p>This is where genuine errors hide. A real paper with the wrong page range has usually been copied from another paper's reference list rather than read.</p>
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
  <p class="note" style="margin-top:16px">This page prints cleanly if you want it on paper for a journal club. Use your browser's print command.</p>
</section>

<section>
  <h2>Still to come</h2>
  <p>Worked appraisals of common presentations, a short glossary of the statistics that keep appearing in veterinary trials, and discussion prompts for journal clubs. If there is a paper you would like taken apart here, write to <a href="mailto:contact@evidencegap.vet">contact@evidencegap.vet</a>.</p>
</section>
"""

open('teaching.html','w',encoding='utf-8').write(page(
 'teaching.html','How to read a paper &mdash; evidencegap.vet',
 'A six-question method for working out whether a veterinary study should change what you do. For students and general practitioners.',
 body, width='mid'))
print('wrote teaching.html')
