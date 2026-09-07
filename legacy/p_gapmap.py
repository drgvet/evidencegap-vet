import sys, json, re as _re; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)));sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))),'lib'))
from shell import page

def slug(t):
    t = _re.sub(r'&[a-z]+;', '-', t)
    t = _re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')
    return 'q-' + t[:58].strip('-')

# confidence: high | moderate | low | verylow | none
# direction : benefit | noeffect | against | unclear | untested
# surrogate : True when the evidence rests only on surrogate/disease-oriented outcomes
import os as _os, records as _records
Q = _records.as_questions(_os.path.join(
    _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
    'content', 'gapmap.txt'))

NQ   = sum(len(qs) for _, qs in Q)
NDOM = len(Q)
NGAP = sum(1 for _, qs in Q for q in qs if q['conf'] == 'none')

WORD  = {20:'Twenty',21:'Twenty-one',22:'Twenty-two',23:'Twenty-three',24:'Twenty-four',
         25:'Twenty-five',26:'Twenty-six',27:'Twenty-seven',28:'Twenty-eight',
         2:'Two',3:'Three',4:'Four',5:'Five',6:'Six',7:'Seven',8:'Eight',9:'Nine'}

CONF = {
 'high'    : ("High certainty",     "Replicated, with consistent findings"),
 'moderate': ("Moderate certainty", "One sound study, with material limitations"),
 'low'     : ("Low certainty",      "Serious limitations, or observational only"),
 'verylow' : ("Very low certainty", "Insufficient to support a claim"),
 'none'    : ("No evidence",        "Not studied"),
}
ORDER = ['high','moderate','low','verylow','none']
SLOT = {  # documented categorical palette, fixed order, validated on the cream surface
 "Myxomatous mitral valve disease (dogs)":      ('s1', '#2a78d6'),
 "Dilated cardiomyopathy (dogs)":               ('s2', '#eb6834'),
 "Feline cardiomyopathy":                       ('s3', '#1baf7a'),
 "Congestive heart failure: management":        ('s4', '#eda100'),
 "Arrhythmias":                                 ('s5', '#e87ba4'),
}
STAGES = [('pre','Asymptomatic','Screening, and treating before signs appear'),
          ('clin','Symptomatic','Once the animal is clinically affected')]
DIRN = {
 'benefit' : "Points to benefit",
 'noeffect': "No benefit shown",
 'against' : "Points against",
 'unclear' : "Cannot say either way",
 'untested': "Untested",
}

def chip(conf):
    return f'<span class="cf cf--{conf}">{CONF[conf][0]}</span>'

# ---------------------------------------------- summary-of-findings table
STAGELAB = {'pre':'Asymptomatic','clin':'Symptomatic'}

rowsout = ''
for dom, qs in Q:
    slot = SLOT[dom][0]
    rowsout += (f'<tr class="domrow"><td colspan="4">'
                f'<span class="spdot sp--{slot}"></span>{dom}</td></tr>')
    for sk,_,_ in STAGES:
        for q in [x for x in qs if x['stage']==sk]:
            href = f'<a href="#{slug(q["t"])}">{q["t"]}</a>'
            sur = ' <span class="surro">Surrogate only</span>' if q.get('surrogate') else ''
            rowsout += (f'<tr>'
                        f'<td class="cq">{href}</td>'
                        f'<td class="cs">{STAGELAB[sk]}</td>'
                        f'<td class="ce">{q["basis"] or "No studies"}{sur}</td>'
                        f'<td class="cv">{chip(q["conf"])}'
                        f'<span class="cvd">{DIRN[q["dirn"]]}</span></td></tr>')

compare = ('<table class="compare">'
  '<colgroup><col class="c1"><col class="c2"><col class="c3"><col class="c4"></colgroup>'
  '<thead><tr>'
  '<th>Clinical question or practice</th><th>Stage</th><th>What exists</th><th>Assessment</th>'
  f'</tr></thead><tbody>{rowsout}</tbody></table>')

splegend = ''.join(
  f'<span class="lgitem"><span class="spdot sp--{SLOT[d][0]}"></span>'
  f'{d.replace(" (dogs)","").replace(": management","")}</span>' for d, _ in Q)

# ------------------------------------------------------------ question list
total = sum(len(qs) for _,qs in Q)
groups = ''
for dom, qs in Q:
    inner = ''
    for sk, slabel, sblurb in STAGES:
        sub = [q for q in qs if q['stage'] == sk]
        if not sub: continue
        items = ''
        for q in sub:
            tags = ''
            src  = f'<p class="qsrc">{q["src"]}</p>' if q['src'] else ''
            verd = f'<p class="qverdict">{q["verdict"]}</p>'
            sur  = '<span class="surro">Surrogate endpoint only</span>' if q.get('surrogate') else ''
            qual = f' &mdash; {q["qual"]}' if q.get('qual') else ''
            if q.get('more'):
                more = f'<p class="seemore"><a href="{q["more"]}">&#42; Read the full appraisal for the caveats</a></p>'
            elif q.get('soon'):
                more = '<p class="seemore soon">&#42; Full appraisal in preparation</p>'
            else:
                more = ''
            items += (f'<div class="q" id="{slug(q["t"])}" data-species="{q["sp"]}" '
                      f'data-conf="{q["conf"]}" data-stage="{q["stage"]}">'
                      f'<div class="qhead"><div class="qtitle">{q["t"]}</div>{chip(q["conf"])}</div>'
                      f'<p class="qbasis">{q["basis"]}<br><b>{DIRN[q["dirn"]]}</b>{qual}{sur}</p>'
                      f'{verd}{src}{more}{tags}</div></div>')
        inner += (f'<div class="stageblock" data-stageblock>'
                  f'<h4 class="stagelab">{slabel}<span>{sblurb}</span></h4>{items}</div>')
    groups += (f'<div class="qgroup" data-group>'
               f'<h3><span class="spdot sp--{SLOT[dom][0]}"></span>{dom}</h3>{inner}</div>')

key = ''.join(
  f'<div><div class="k"><span class="cf cf--{k}">{CONF[k][0]}</span></div>'
  f'<div class="v">{CONF[k][1]}</div></div>' for k in ORDER)

DIRNDEF = [
 ('benefit',  'The studies that exist point to the treatment helping.'),
 ('noeffect', 'The studies looked for a benefit and did not find one.'),
 ('against',  'The studies point to the treatment being unhelpful or harmful.'),
 ('unclear',  'Studies exist, but they cannot answer the question either way.'),
 ('untested', 'Nobody has studied the question, so there is nothing to point anywhere.'),
]
dirkey = ''.join(
  f'<div><div class="k"><span class="cvd">{DIRN[k]}</span></div>'
  f'<div class="v">{v}</div></div>' for k, v in DIRNDEF)

body = f"""
<div class="kicker">Evidence gap map</div>
<h1>Small-animal cardiology</h1>
<p class="standfirst">This map sets out {WORD[NQ].lower()} clinical questions and practices in small-animal cardiology. Each one is assessed for the certainty of the evidence behind it and for what that evidence actually says, and {WORD[NGAP].lower()} of them have no supporting evidence of any kind.</p>
<p class="note" style="max-width:74ch;margin-top:14px">This is one of six specialty maps. The others cover anaesthesia and analgesia, antimicrobials, nutrition and supplements, dermatology and oncology, and all of them are being expanded. The <a href="index.html">home page</a> lists them.</p>
<div class="meta"><span>Living document</span><span>{NQ} entries &middot; {NDOM} domains</span><span>Revised August 2026</span></div>

<section>
  <h2>How each question is assessed</h2>
  <p>Every question on this map carries two marks, and they answer two different
  questions. <strong>Certainty</strong> says how much the evidence can be relied on.
  <strong>Direction</strong> says which way that evidence points. A question can score
  low on the first and still be clear on the second, and the two are recorded
  separately for that reason.</p>

  <p>Take atenolol in preclinical hypertrophic cardiomyopathy as an example. The
  certainty is <em>Low</em>, because the only study is an open-label observational
  cohort in 63 cats rather than a randomised trial. The direction is <em>No benefit
  shown</em>, because that cohort looked for a survival difference over five years and
  did not find one. Reporting a single combined score would lose one of those two
  facts.</p>

  <h3>Certainty: how far the evidence can be relied on</h3>
  <div class="gradekey">{key}</div>
  <p style="margin-top:18px">These five labels follow GRADE, the system used for the
  same purpose in human medicine. The starting point is the study design, and the
  certainty is then rated down for risk of bias, for imprecision, for evidence that
  is indirect, and for findings that disagree between studies. It may be rated up
  where an effect is large and consistent. GRADE has four levels, and the fifth label
  used here, <em>No evidence</em>, marks a question nobody has studied at all.</p>

  <h3>Direction: which way the evidence points</h3>
  <div class="gradekey">{dirkey}</div>
  <p style="margin-top:18px">The last two are frequently confused with each other, and
  the distinction matters at the bedside. <em>No benefit shown</em> means somebody
  looked and found nothing, which is a finding. <em>Untested</em> means nobody looked,
  which is not.</p>

  <h3>Why the two marks are kept apart</h3>
  <p>Study design determines where an assessment begins, and it does not determine
  where it ends. A randomised trial that measured a surrogate outcome, was funded by
  the manufacturer of the drug under test and has never been replicated may warrant
  less confidence than a well-conducted observational study. A single ranking that
  puts every trial above every cohort would get that case backwards, which is why
  design here sets the starting point and the specific problems with each study then
  move the mark.</p>
  <p>The reasons why certainty was not rated higher are listed under each entry rather
  than summarised, so that any judgement on this map can be checked against the studies
  it came from and disputed.</p>

  <h3>One rule applied without exception</h3>
  <p><strong>Evidence resting only on a surrogate outcome cannot be rated above Very
  low, whatever its design.</strong> A surrogate is a measurement that stands in for
  something the animal experiences: wall thickness in place of heart failure, ectopic
  counts in place of sudden death, a blood marker in place of survival. A surrogate can
  improve while the animal is no better off, and in human cardiology drugs have
  improved the surrogate and increased mortality at the same time. Entries resting on a
  surrogate are marked <em>Surrogate endpoint only</em> beneath the question,
  and <em>Surrogate only</em> in the table above. The rule is
  this site\'s own, adapted from SORT, the grading scheme used in human primary
  care.</p>
</section>

<section>
  <h2>Summary of findings</h2>
  <p>The table lists every entry on the map together with the evidence that exists behind it and the assessment that follows from that evidence. Each row links to the full entry below, where the verdict and the specific limitations are set out.</p>
  <div class="maplegend">
    <p class="lgrow"><span class="lglab">Domain</span>{splegend}</p>
  </div>
  <div class="tscroll">{compare}</div>
  <p class="scrollhint scrollhint--cmp">Scroll the table sideways for the assessment column.</p>
  <p class="note" style="margin-top:16px"><strong>Table 1.</strong> Certainty and direction are recorded as separate marks, and neither of them is derived from study design alone.</p>
</section>

<section class="callout">
  <h2>The same drugs, in people</h2>
  <p>Much of small-animal cardiology is extrapolated from human cardiology, and the extrapolation is seldom stated. Human and animal cardiac disease differ enough that a human trial rarely settles a veterinary question. Drug classes, however, travel further than diseases do, and several of the classes used here have been tested in people at a scale veterinary medicine will never reach.</p>
  <p>Oral inotropes increased mortality in two placebo-controlled trials. Suppressing asymptomatic ventricular ectopy after myocardial infarction more than doubled it, with no warning on any intermediate measure. Beta blockade in non-obstructive hypertrophic cardiomyopathy reduced exercise capacity against placebo. Glucocorticoids are given in human heart failure deliberately, to improve diuresis, rather than withheld.</p>
  <p>A companion page sets out each intervention class in turn, describing what was tested in people, what the trials showed, and how close the analogy to the veterinary question is judged to be. The judgements range from close, through partial, to no analogue at all.</p>
  <p class="cta"><a class="btn solid" href="human-evidence.html">The human evidence, class by class</a></p>
</section>

<section>
  <h2>Clinical questions and practices</h2>
  <div class="filterbar">
    <p class="flab">Species</p>
    <div class="chips" data-filter="species">
      <button class="chip" data-value="all" aria-pressed="true">All</button>
      <button class="chip" data-value="dog" aria-pressed="false">Dogs</button>
      <button class="chip" data-value="cat" aria-pressed="false">Cats</button>
    </div>
    <p class="flab" style="margin-top:14px">Disease stage</p>
    <div class="chips" data-filter="stage">
      <button class="chip" data-value="all" aria-pressed="true">All</button>
      <button class="chip" data-value="pre" aria-pressed="false">Asymptomatic</button>
      <button class="chip" data-value="clin" aria-pressed="false">Symptomatic</button>
    </div>
    <p class="flab" style="margin-top:14px">Certainty of evidence</p>
    <div class="chips" data-filter="conf">
      <button class="chip" data-value="all" aria-pressed="true">All</button>
      <button class="chip" data-value="moderate" aria-pressed="false">Moderate</button>
      <button class="chip" data-value="low" aria-pressed="false">Low</button>
      <button class="chip" data-value="verylow" aria-pressed="false">Very low</button>
      <button class="chip" data-value="none" aria-pressed="false">No evidence</button>
    </div>
  </div>
  <p class="count" id="count">Showing {total} of {total} entries</p>
  {groups}
</section>

<section>
  <h2>Status</h2>
  <p>This map is incomplete and remains under revision. Every mark on it is a judgement, and the reasons behind each are listed rather than summarised so that they can be checked and disputed. Corrections and citations that have been omitted are welcome, and the <a href="about.html">about page</a> explains how to send them.</p>
</section>
"""

SCRIPT = """
<script>
(function(){
  var state={species:'all',conf:'all',stage:'all'};
  var qs=[].slice.call(document.querySelectorAll('.q[data-species]'));
  var groups=[].slice.call(document.querySelectorAll('[data-group]'));
  var count=document.getElementById('count');
  var total=qs.length;
  function apply(){
    var shown=0;
    qs.forEach(function(q){
      var ok=(state.species==='all'||q.dataset.species===state.species)
          && (state.conf==='all'||q.dataset.conf===state.conf)\n          && (state.stage==='all'||q.dataset.stage===state.stage);
      q.hidden=!ok; if(ok) shown++;
    });
    document.querySelectorAll('[data-stageblock]').forEach(function(sb){ sb.hidden=!sb.querySelector('.q:not([hidden])'); });\n    groups.forEach(function(g){ g.hidden=!g.querySelector('.q:not([hidden])'); });
    count.textContent='Showing '+shown+' of '+total+' entries';
  }
  document.querySelectorAll('.chips').forEach(function(row){
    var key=row.dataset.filter;
    row.addEventListener('click',function(e){
      var b=e.target.closest('.chip'); if(!b) return;
      row.querySelectorAll('.chip').forEach(function(c){c.setAttribute('aria-pressed', c===b?'true':'false');});
      state[key]=b.dataset.value; apply();
    });
  });
  apply();
})();
</script>
"""

INDEX = [{'domain':dom,'title':q['t'],'conf':q['conf'],'dirn':q['dirn'],'stage':q['stage'],
          'species':q['sp'],'id':slug(q['t'])} for dom,qs in Q for q in qs]
json.dump(INDEX, open('questions.json','w'), indent=1)

open('gapmap.html','w',encoding='utf-8').write(page(
 'gapmap.html','Gap map: small-animal cardiology &mdash; evidencegap.vet',
 f'{NQ} clinical questions and practices in small-animal cardiology, each assessed for the certainty of the evidence behind it and for what that evidence says.',
 body, width='wide', script=SCRIPT))
print('questions:', len(INDEX))
for k in ORDER:
    print(' ', CONF[k][0], sum(1 for x in INDEX if x['conf']==k))
