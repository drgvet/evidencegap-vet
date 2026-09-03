import sys, json, html; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)));sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))),'lib'))
from shell import page

Q = json.load(open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'questions.json')))
R = json.load(open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'reviews.json')))
GAPS = sum(1 for q in Q if q['conf'] == 'none')
DOMS = sorted({q['domain'] for q in Q})

def motif(seed, tint='#EBDCBE', dark='#17456F'):
    """Abstract evidence-matrix thumbnail: 4x8 grid, bubbles sized by a fixed pattern."""
    import math
    cells = []
    for r in range(4):
        for c in range(8):
            v = (seed * 7 + r * 5 + c * 3) % 9
            x, y = 26 + c * 30, 24 + r * 26
            if v == 0:
                cells.append(f'<circle cx="{x}" cy="{y}" r="2" fill="{tint}"/>')
            elif v < 4:
                cells.append(f'<circle cx="{x}" cy="{y}" r="{5+v}" fill="{dark}" opacity="{0.25+v*0.16:.2f}"/>')
            elif v < 6:
                cells.append(f'<circle cx="{x}" cy="{y}" r="8" fill="none" stroke="#B87333" '
                             f'stroke-width="1.4" stroke-dasharray="3 2.5"/>')
            else:
                cells.append(f'<circle cx="{x}" cy="{y}" r="{3+(v%3)}" fill="{tint}"/>')
    return ('<svg class="thumb" viewBox="0 0 268 120" preserveAspectRatio="xMidYMid slice" '
            'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">' + ''.join(cells) + '</svg>')

MAPS = [
 ("Small-animal cardiology", "gapmap.html", True,
  "Mitral valve disease, cardiomyopathies, heart-failure management and arrhythmias, "
  "graded against the strongest evidence available for each question.",
  f"{len(Q)} entries", f"{GAPS} open gaps", 1),
 ("Anaesthesia and analgesia", None, False,
  "Protocol selection, multimodal analgesia and monitoring thresholds across "
  "species and procedure types.", "", "", 2),
 ("Antimicrobials", None, False,
  "Empirical selection, duration of therapy and the evidence behind first-line "
  "recommendations in common presentations.", "", "", 3),
 ("Nutrition and supplements", None, False,
  "Therapeutic diets, joint supplements and nutraceuticals, where marketing "
  "claims and trial evidence most often diverge.", "", "", 4),
 ("Dermatology", None, False,
  "Atopic disease, otitis and the long-term management protocols that rest "
  "largely on convention.", "", "", 5),
 ("Oncology", None, False,
  "Protocol comparisons, adjuvant therapy and the outcome measures used to "
  "judge them.", "", "", 6),
]

mapcards = ''
for title, href, live, desc, m1, m2, seed in MAPS:
    tag = ('<span class="pill live">Live</span>' if live else '<span class="pill plan">Planned</span>')
    metas = ''.join(f'<span>{m}</span>' for m in (m1, m2) if m)
    inner = (f'{motif(seed)}<div class="body"><div class="type">Evidence gap map</div>'
             f'<h3>{title}</h3><p>{desc}</p>'
             f'<div class="foot">{tag}{metas}</div></div>')
    mapcards += (f'<a class="mapcard" href="{href}">{inner}</a>' if live
                 else f'<div class="mapcard soon">{inner}</div>')

# ---- A–Z index, grouped by domain, generated from the gap map data ----
CONFLABEL = {'high':'High','moderate':'Moderate','low':'Low','verylow':'Very low','none':'No evidence'}
def gradetag(c):
    return f'<span class="cf cf--{c}">{CONFLABEL[c]}</span>'

az = ''
for dom in [d for d in ["Myxomatous mitral valve disease (dogs)","Dilated cardiomyopathy (dogs)",
                        "Feline cardiomyopathy","Congestive heart failure: management","Arrhythmias"]]:
    rows = ''.join(
      f'<li data-q="{html.escape(q["title"].lower())} {html.escape(dom.lower())}">'
      f'<a href="gapmap.html#{q["id"]}"><span>{q["title"]}</span>{gradetag(q["conf"])}</a></li>'
      for q in Q if q['domain'] == dom)
    az += f'<div class="azgroup" data-azgroup><h3>{dom}</h3><ul class="azlist">{rows}</ul></div>'

body = f"""
<section class="hero2">
  <div class="bar">
    <p class="kick">Evidence gaps in veterinary medicine</p>
    <h1>Not every recommendation has strong evidence behind it.</h1>
    <p class="lede">Some routine practice is supported by sound studies. Some rests on a single small paper, or on convention. This site records which is which, question by question, together with the reasoning behind each judgement.</p>
    <div class="acts">
      <a class="btn light" href="gapmap.html">Browse the gap map</a>
      <a class="btn outline" href="#find">Find a clinical question</a>
    </div>
    <div class="hstats">
      <div><div class="fig">{len(Q)}</div><div class="cap">Clinical questions and practices mapped</div></div>
      <div><div class="fig">{GAPS}</div><div class="cap">With no evidence at all</div></div>
      <div><div class="fig">{len(DOMS)}</div><div class="cap">Cardiology domains</div></div>
      <div><div class="fig">{R["published"]}</div><div class="cap">Appraisals published</div></div>
      <div><div class="fig">1</div><div class="cap">Discipline mapped so far</div></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="bar">
    <div class="bandhead">
      <h2>Evidence gap maps</h2>
      <span class="more"><a href="gapmap.html">Open the cardiology map &rarr;</a></span>
    </div>
    <div class="maps">{mapcards}</div>
    <p class="note" style="margin-top:22px">Each map covers one area of practice, question by question. Cardiology is complete; the remainder are in preparation.</p>
  </div>
</section>

<section class="band band--tint" id="find">
  <div class="bar">
    <div class="bandhead">
      <h2>Find a clinical question or practice</h2>
      <span class="more">{len(Q)} entries indexed</span>
    </div>
    <div class="finder">
      <label for="qsearch">Search every mapped question and practice</label>
      <input id="qsearch" type="search" autocomplete="off"
             placeholder="pimobendan, Holter, furosemide, thromboembolism&hellip;">
      <p class="hint" id="qcount">Showing all {len(Q)} entries. Type to narrow the list.</p>
    </div>
    {az}
    <p class="aznone" id="aznone">Nothing matches that term. Try a drug name, a test, or a condition.</p>
  </div>
</section>

<section class="band">
  <div class="bar">
    <div class="bandhead">
      <h2>Latest commentaries</h2>
      <span class="more"><a href="reviews.html">All commentaries &rarr;</a></span>
    </div>
    <ul class="latest">
      <li>
        <div class="lt">Commentary &middot; Canine cardiology &middot; August 2026</div>
        <h3><a href="review-pimobendan-b2.html">Pimobendan in preclinical stage B2 mitral valve disease</a></h3>
        <p>Reconstructed from the published curves: nine reclassified dogs remove significance, the proportions alone are not significant, and full approval rests on a single-arm study measured against a benchmark it was not required to beat.</p>
      </li>
      <li>
        <div class="lt">Commentary &middot; Feline cardiology &middot; August 2026</div>
        <h3><a href="review-steroids-chf.html">Steroids and heart failure in cats: science, or an old wives' tale?</a></h3>
        <p>The belief rests on two papers from 2004 and 2006. Neither shows it, the controlled studies found no cardiac change, and the largest cohort found no excess.</p>
      </li>
      <li>
        <div class="lt">Editorial appraisal &middot; Feline cardiology &middot; August 2026</div>
        <h3><a href="review-rapamycin.html">Rapamycin (sirolimus) for subclinical hypertrophic cardiomyopathy in cats</a></h3>
        <p>The FDA record and the published paper disagree about whether the endpoint of the single supporting trial was chosen before the data were seen.</p>
      </li>
      <li>
        <div class="lt">Editorial appraisal &middot; Canine cardiology &middot; June 2026</div>
        <h3>Torasemide as an alternative to furosemide in canine congestive heart failure</h3>
        <p>Non-inferiority on a composite endpoint is a weaker claim than the result is generally taken to support. In preparation.</p>
      </li>
    </ul>
  </div>
</section>

<section class="band band--tint">
  <div class="bar">
    <div class="bandhead"><h2>How the marks work</h2></div>
    <div class="gradekey">
      <div><div class="k"><span class="cf cf--moderate">Moderate certainty</span></div><div class="v">One sound study, with material limitations</div></div>
      <div><div class="k"><span class="cf cf--low">Low certainty</span></div><div class="v">Serious limitations, or observational only</div></div>
      <div><div class="k"><span class="cf cf--verylow">Very low certainty</span></div><div class="v">Insufficient to support a claim</div></div>
      <div><div class="k"><span class="cf cf--none">No evidence</span></div><div class="v">Not studied</div></div>
    </div>
    <p class="note" style="margin-top:20px;max-width:76ch">Study design sets the starting point of the assessment, not its conclusion. A trial that was funded by the manufacturer, measured a surrogate outcome and has never been replicated does not outrank a well-conducted observational study by virtue of its design. The specific reasons certainty was not rated higher are recorded against every question, so that each judgement can be examined rather than accepted.</p>
  </div>
</section>

<section class="band">
  <div class="bar">
    <div class="bandhead"><h2>Three ways the evidence falls short</h2></div>
    <ol class="numbered" style="max-width:76ch">
      <li>
        <h3>Absence of direct evidence</h3>
        <p>Interventions in routine use that have never been tested against a control in the species they are given to. Dietary sodium restriction in canine congestive heart failure is one; the practice is near-universal and the trial does not exist.</p>
      </li>
      <li>
        <h3>Borrowed evidence</h3>
        <p>Findings carried across from human medicine, or from one species to another, without data establishing that they transfer. Dose, pharmacokinetics and disease phenotype rarely translate cleanly, and the assumption that they do is seldom stated.</p>
      </li>
      <li>
        <h3>Consensus in place of data</h3>
        <p>Screening intervals, treatment thresholds and monitoring conventions that originate in expert judgement and are subsequently cited as established. Such conventions may well be correct; the point is that they should be labelled as what they are.</p>
      </li>
    </ol>
  </div>
</section>

<section class="band band--tint">
  <div class="bar">
    <div class="bandhead">
      <h2>The same drugs, in people</h2>
      <span class="more"><a href="human-evidence.html">Read the comparison &rarr;</a></span>
    </div>
    <p style="max-width:76ch;font-size:19px;line-height:1.6">Much of small-animal cardiology is extrapolated from human cardiology, and the extrapolation is seldom stated. The diseases differ enough that a human trial rarely settles a veterinary question. Drug classes, though, travel further than diseases do, and several of these have been tested in people at a scale veterinary medicine will never reach.</p>
    <p style="max-width:76ch;font-size:19px;line-height:1.6;margin-top:16px">Oral inotropes increased mortality against placebo. Suppressing asymptomatic ventricular ectopy after myocardial infarction more than doubled it, with no warning on any intermediate measure. Beta blockade in non-obstructive hypertrophic cardiomyopathy reduced exercise capacity. Glucocorticoids are given in human heart failure on purpose, to improve diuresis, rather than withheld.</p>
    <p style="max-width:76ch;font-size:19px;line-height:1.6;margin-top:16px">A companion page takes each intervention class in turn: what was tested, what it showed, and how close the analogy actually is.</p>
    <p style="margin-top:26px"><a class="btn light" href="human-evidence.html">The human evidence, class by class</a></p>
  </div>
</section>

<section class="band band--dark">
  <div class="bar">
    <div class="twoup">
      <div>
        <h3>Scope</h3>
        <p>Small-animal cardiology at present, {len(Q)} entries across {len(DOMS)} domains. The other disciplines listed above are planned rather than started. Within cardiology the map is not exhaustive: it covers the questions and practices that come up often enough to be worth appraising.</p>
      </div>
      <div>
        <h3>Method</h3>
        <p>Entries are written from the primary reports, not from abstracts or from what other papers say about them. A citation that cannot be checked against the record is not used. Gradings are revised when new work appears, and the reasons behind each are listed under the entry.</p>
      </div>
    </div>
    <div style="margin-top:44px;padding-top:32px;border-top:1px solid rgba(255,255,255,.18)">
      <h3 style="font-size:23px;margin:0 0 10px">Corrections and additions</h3>
      <p style="color:#B9C6D6;max-width:62ch;margin:0 0 22px">Proposed entries, disputed gradings and citations that should be here are all welcome. Contributions are credited.</p>
      <a class="btn light" href="mailto:contact@evidencegap.vet">contact@evidencegap.vet</a>
      <p class="fine" style="margin:24px 0 0">Editorial appraisals of published literature. Not peer reviewed, and not clinical advice.</p>
    </div>
  </div>
</section>
"""

SCRIPT = """
<script>
(function(){
  var input=document.getElementById('qsearch');
  if(!input) return;
  var items=[].slice.call(document.querySelectorAll('.azlist li'));
  var groups=[].slice.call(document.querySelectorAll('[data-azgroup]'));
  var count=document.getElementById('qcount');
  var none=document.getElementById('aznone');
  var total=items.length;
  function run(){
    var t=input.value.trim().toLowerCase();
    var shown=0;
    items.forEach(function(li){
      var ok=!t||li.dataset.q.indexOf(t)>-1;
      li.hidden=!ok; if(ok) shown++;
    });
    groups.forEach(function(g){ g.hidden=!g.querySelector('li:not([hidden])'); });
    none.style.display=shown?'none':'block';
    count.textContent = t
      ? 'Showing '+shown+' of '+total+' entries matching \\u201c'+input.value.trim()+'\\u201d.'
      : 'Showing all '+total+' entries. Type to narrow the list.';
  }
  input.addEventListener('input',run);
  run();
})();
</script>
"""

open('index.html','w',encoding='utf-8').write(page(
 'index.html','Evidence gaps in veterinary medicine &mdash; evidencegap.vet',
 'Some of what we do in small-animal practice is backed by good studies. Some rests on one small paper, or on habit. This site works out which is which.',
 body, raw=True, script=SCRIPT))
print('wrote index.html')
