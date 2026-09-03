import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)));sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))),'lib'))
from shell import page

CONFLABEL = {'high':'High certainty','moderate':'Moderate certainty',
             'low':'Low certainty','verylow':'Very low certainty','none':'No evidence'}
def meter(c):
    return f'<span class="cf cf--{c}">{CONFLABEL[c]}</span>'

ART = [
 ("EG-2026-006","Commentary","Canine cardiology","August 2026",
  "review-pimobendan-b2.html",
  "Pimobendan in preclinical stage B2 mitral valve disease: where the effect comes from, how fragile it is, and what the regulatory record shows",
  "The EPIC survival curves were digitised and individual dogs reconstructed, reproducing the published medians, hazard ratio and P value. Nine reclassified dogs remove significance and the proportions alone are not significant, yet a 380-day median difference survives removing the first 23 weeks. Three non-identical versions of the trial sit on the public record, and full approval rests on a single-arm study whose success threshold was set below its own historical control rate.",
  "moderate", "EPIC 2016; FDA NADA 141-273, 2025", True),
 ("EG-2026-005","Commentary","Feline cardiology","August 2026",
  "review-steroids-chf.html",
  "Steroids and heart failure in cats: science, or an old wives' tale?",
  "Two papers from 2004 and 2006 are cited repeatedly as the literature behind this. Neither supports it. Two studies dosing cats deliberately found no cardiac change, steroid exposure was no more common in transient thickening than in true cardiomyopathy, and in people prednisone is used to increase diuresis in heart failure.",
  "low", "Smith, 2004 to Poissonnier, 2025", True),
 ("EG-2026-004","Editorial appraisal","Feline cardiology","August 2026",
  "review-rapamycin.html",
  "Rapamycin (sirolimus) for subclinical hypertrophic cardiomyopathy in cats: a critical appraisal of the evidence supporting conditional approval",
  "Conditional approval of Felycin-CA1 rests on a single 43-cat trial that its own authors describe as nonpivotal, exploratory and dose-determining. The FDA record states that the endpoint was selected after exploratory analysis; the published paper presents it as prespecified and does not disclose the sequence.",
  "verylow", "RAPACAT, 2023; FDA NADA 141-604, 2025", True),
 ("EG-2026-003","Editorial appraisal","Canine cardiology","July 2026", None,
  "Does preclinical pimobendan shorten survival once congestive heart failure develops?",
  "Two retrospective cohorts report shorter post-CHF survival among dogs treated before the onset of failure. The signal warrants prospective study, but confounding by indication is a sufficient explanation on the present data.",
  "low", "Two retrospective cohorts, 2025&ndash;26", False),
 ("EG-2026-002","Editorial appraisal","Canine cardiology","June 2026", None,
  "Torasemide as an alternative to furosemide in canine congestive heart failure",
  "TEST supports torasemide as a reasonable alternative to furosemide. Non-inferiority demonstrated on a composite endpoint is, however, a materially weaker claim than the way the result is generally presented.",
  "low", "TEST, 2017", False),
 ("EG-2026-001","Editorial appraisal","Nutrition and supplements","May 2026", None,
  "Cannabidiol for osteoarthritis pain in dogs",
  "Several small placebo-controlled trials point in different directions. Outcomes are owner-reported throughout, and caregiver placebo effects are large enough in this setting to account for much of the reported signal.",
  "low", "Multiple small RCTs, 2018&ndash;2025", False),
]

import json
PUB  = sum(1 for r in ART if r[-1])
PREP = len(ART) - PUB
json.dump({'published':PUB,'inprep':PREP,'total':len(ART)},
          open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'reviews.json'),'w'))

items = ''
for aid, atype, dom, date, href, title, summ, grade, src, live in ART:
    t = f'<a href="{href}">{title}</a>' if live else title
    status = '' if live else '<span style="color:#8A4B1F">In preparation</span>'
    items += f"""
    <article>
      <div class="lhs"><span class="type">{atype}</span>{aid}<br>{date}</div>
      <div>
        <h3>{t}</h3>
        <p class="auth">{dom}</p>
        <p class="sum">{summ}</p>
        <div class="foot">{meter(grade)}<span>{src}</span>{status}</div>
      </div>
    </article>"""

body = f"""
<div class="kicker">Editorial appraisals</div>
<h1>Appraisals of the veterinary evidence base</h1>
<p class="standfirst">Close readings of single studies. What the paper claims, and whether its methods can carry the claim.</p>
<div class="meta"><span>{PUB} published &middot; {PREP} in preparation</span><span>Signed editorial appraisals</span><span>Revised August 2026</span></div>

<section>
  <h2>Scope and method</h2>
  <p>Each appraisal states the claim under examination, sets out the design and the data as reported, then works through the specific features of the study that bear on whether the claim follows. Where a limitation is identified it is named by type &mdash; methodological, measurement, safety, practice, regulatory &mdash; so that the shape of the deficiency is legible, not merely its existence.</p>
  <p>Appraisals are written from the published record: the primary report, its supplementary material, and, where the intervention is licensed, the regulatory summary. Where an analysis is unavailable, that absence is recorded rather than inferred around. Each carries a stable identifier, a revision date, and a full declarations block.</p>
  <p class="note" style="margin-top:20px"><strong>Editorial status.</strong> These are signed editorial appraisals, not peer-reviewed articles. They are presented in journal format for legibility and citation, and each states its review status explicitly.</p>
</section>

<section>
  <h2>Contents</h2>
  <div class="issue">{items}</div>
</section>

<section>
  <h2>Related</h2>
  <p>The <a href="gapmap.html">gap map</a> places these appraisals in context, mapping twenty-four clinical questions in small-animal cardiology against the strongest evidence available for each. Mapping proceeds one discipline at a time; anaesthesia and analgesia, antimicrobials, nutrition and supplements, dermatology, behaviour, oncology, surgery, equine and food-animal medicine are planned and not yet mapped.</p>
</section>
"""

open('reviews.html','w',encoding='utf-8').write(page(
 'reviews.html','Editorial appraisals &mdash; evidencegap.vet',
 'Close readings of single veterinary studies: what the paper claims, and whether its methods can carry the claim.',
 body, width='mid'))
print('wrote reviews.html')
