import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)));sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))),'lib'))
from shell import page

teaching_body = """
<div class="kicker">Teaching</div>
<h1>Materials on reading the veterinary literature</h1>
<p class="standfirst">These pages set out how to read a veterinary paper and judge it for yourself. They are being written at present.</p>
<div class="meta"><span>In preparation</span><span>Revised August 2026</span></div>

<section>
  <h2>Rationale</h2>
  <p>Clinical training reliably conveys what the literature currently concludes, and it conveys much less reliably how to determine whether a given conclusion is well founded. Judging that requires knowing whether an endpoint was prespecified, whether a subgroup was defined before or after unblinding, and whether an effect size exceeds the measurement error of the instrument that produced it. These are learnable skills, and they generalise across every domain in which a clinician will subsequently work.</p>
</section>

<section>
  <h2>Planned</h2>
  <ul class="plain">
    <li><h3>Study-design primers</h3><p class="small">These primers describe what each design can and cannot establish, covering randomised trials, non-inferiority designs, prospective cohorts and retrospective series, together with the specific inferential limits of each.</p></li>
    <li><h3>Worked appraisals</h3><p class="small">Each worked appraisal reads a published veterinary trial in full, setting out the reasoning step by step and making the judgement calls explicit.</p></li>
    <li><h3>A statistical glossary</h3><p class="small">The glossary defines the measures that recur in veterinary trials, including hazard ratios, composite endpoints, non-inferiority margins and coefficients of variation, in the terms in which they are actually reported.</p></li>
    <li><h3>Journal-club materials</h3><p class="small">These are discussion prompts built on the appraisals published here, intended for use in resident teaching rounds.</p></li>
  </ul>
</section>

<section>
  <h2>In the interim</h2>
  <p>The <a href="reviews.html">appraisals</a> are written to serve as teaching material in their own right: each of them works through what a study claims, what it actually demonstrates, and where the distance between the two opens up. The <a href="gapmap.html">gap map</a> is a useful source of questions to assign, because every entry marked as having no evidence identifies a point at which the literature runs out.</p>
</section>
"""

about_body = """
<div class="kicker">About</div>
<h1>About this project</h1>
<p class="standfirst">This page explains what the site is for, how the grading works, and who to write to about it.</p>
<div class="meta"><span>Established 2026</span><span>Unaffiliated</span><span>No commercial funding</span></div>

<section>
  <h2>Purpose</h2>
  <p>Veterinary evidence is unevenly distributed. Some questions have been addressed by adequately powered randomised trials; many more rest on a single small study, on data borrowed from human medicine, or on convention that has never been tested. The distribution itself is rarely documented, which makes it difficult for a clinician to know how much weight a given recommendation will bear.</p>
  <p>This site documents that distribution. It grades the evidence behind individual clinical questions, appraises the studies on which those grades rest, and records explicitly where no evidence exists. The intention is descriptive rather than polemical, and the blank regions of the map are treated as findings in their own right.</p>
</section>

<section>
  <h2>Editorial approach</h2>
  <p>Grades are appraisals of the published literature and are stated as such. They do not constitute a formal GRADE assessment, and reasonable readers may grade a question differently. Where that is likely, the specific limitations driving the grade are listed so that the judgement can be inspected and disputed. Entries are revised as evidence accumulates, and the revision date is shown on each page.</p>
  <p>Appraisals draw on the primary report, on supplementary material, and on regulatory summaries where an intervention is licensed. Where an analysis has not been published, that is recorded as an absence rather than filled in by inference.</p>
</section>

<section>
  <h2>Editorial status</h2>
  <p>Everything published here is an editorial appraisal. Nothing on this site has been peer reviewed, and it is presented in journal format for legibility and citation rather than to imply refereed status. Each appraisal states its review status explicitly in its declarations.</p>
  <p>The work is written and maintained by a board-certified veterinary cardiologist in clinical practice. Authorship details will be added to this page.</p>
</section>

<section>
  <h2>Independence and funding</h2>
  <p>This is a personal project. It receives no funding from any institution, journal, manufacturer or professional body, carries no advertising, and nothing published here should be read as the position of any employer. Where an appraisal concerns a licensed product, the sponsor of the underlying trial is named.</p>
</section>

<section id="contact">
  <h2>Contact and corrections</h2>
  <p>Corrections, missed citations and proposed additions are welcome and will be acknowledged. Where a correction changes a grade or a conclusion, the revision is dated on the page concerned.</p>
  <p>Write to <a href="mailto:contact@evidencegap.vet">contact@evidencegap.vet</a>.</p>
</section>

<section>
  <h2>Limits</h2>
  <p>Appraisals are commentary on published literature. They are not clinical advice, do not establish a standard of care, and are not a substitute for the judgement of the attending clinician.</p>
</section>
"""

nf_body = """
<div class="kicker">Error 404</div>
<h1>That page does not exist</h1>
<p class="standfirst">The address is either wrong, or the page has moved since someone linked to it.</p>
<section style="margin-top:40px">
  <h2>Try instead</h2>
  <ul class="plain">
    <li><h3><a href="index.html">Home</a></h3><p class="small">The home page describes what the project records and how the grades work.</p></li>
    <li><h3><a href="gapmap.html">Gap map</a></h3><p class="small">The map covers twenty-four clinical questions in small-animal cardiology.</p></li>
    <li><h3><a href="reviews.html">Appraisals</a></h3><p class="small">Individual studies are read closely here, one at a time.</p></li>
  </ul>
  <p style="margin-top:24px">If you followed a link from elsewhere and it should work, please report it to <a href="mailto:contact@evidencegap.vet">contact@evidencegap.vet</a>.</p>
</section>
"""

for fn, title, desc, body in [
 ('about.html','About &mdash; evidencegap.vet',
  'An independent, non-commercial record of what small-animal veterinary medicine has and has not established.', about_body),
 ('404.html','Page not found &mdash; evidencegap.vet','That page does not exist.', nf_body),
]:
    open(fn,'w',encoding='utf-8').write(page(fn, title, desc, body))
    print('wrote', fn)
