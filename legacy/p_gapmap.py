import sys, json, re as _re; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)));sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))),'lib'))
from shell import page

def slug(t):
    t = _re.sub(r'&[a-z]+;', '-', t)
    t = _re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')
    return 'q-' + t[:58].strip('-')

# confidence: high | moderate | low | verylow | none
# direction : benefit | noeffect | against | unclear | untested
# surrogate : True when the evidence rests only on surrogate/disease-oriented outcomes
Q = [
("Myxomatous mitral valve disease (dogs)", [
 dict(stage="pre", more="review-pimobendan-b2.html", qual="in stage B2 dogs only, on a composite endpoint, in a trial stopped early and never repeated", t="Pimobendan in preclinical stage B2 disease", sp="dog", conf="moderate", dirn="benefit",
   basis="1 randomised trial, 360 dogs, placebo-controlled and double-blind, clinical endpoint",
   src='EPIC, 2016 &middot; FDA NADA 141-273, 2025 &middot; <a href="review-pimobendan-b2.html">full appraisal</a>',
   tags=["Funded by the manufacturer","Stopped early at a pre-planned interim","Nine reclassified dogs remove significance","On proportions alone the result is not significant","Judged by FDA not adequate and well-controlled","Never replicated"],
   verdict="EPIC, the single trial of pimobendan in preclinical stage B2 disease, supports delaying heart failure in dogs meeting its entry criteria, and nothing else on this map is better evidenced. It is also more fragile than the headline suggests: nine reclassified dogs remove significance, and on proportions alone the result is not significant. A 380-day median difference survives removing the first 23 weeks, so the benefit is not only early failures. Whether dogs at the mild end of stage B2 benefit is not answerable from the published data."),
 dict(stage="pre", t="Does preclinical pimobendan shorten survival once heart failure develops?", sp="dog", conf="low", dirn="unclear",
   basis="2 retrospective cohorts, 137 and 143 dogs, no randomisation",
   src='McAulay, 2026 &middot; Park, 2025',
   tags=["Retrospective","Confounding by indication visible in the data","Underpowered"],
   verdict="Two retrospective cohorts report shorter survival after heart failure in dogs treated beforehand, which is a question worth asking. Neither can answer it. In both, the pretreated dogs already had larger hearts at the point failure developed, which is enough on its own to explain the difference. The finding argues for a prospective study, not for a change in practice."),
 dict(stage="clin", soon=True, qual="compared with benazepril, which was itself never shown to beat placebo in heart failure", t="Pimobendan in congestive heart failure", sp="dog", conf="moderate", dirn="benefit",
   basis="1 randomised trial, 260 dogs, active comparator, clinical endpoint",
   src='QUEST, 2008',
   tags=["Single-blinded, owners not blinded","No placebo arm","Composite endpoint includes investigator-judged treatment failure","Manufacturer-affiliated co-author"],
   verdict="The evidence shows pimobendan outperforms benazepril in dogs already in heart failure, and that comparison is sound. It does not show pimobendan outperforms placebo, and benazepril itself was never established against placebo at this stage, so the size of the true benefit is unknown. Owners were not blinded, and part of the composite endpoint was judged by the investigators."),
 dict(stage="pre", soon=True, t="ACE inhibitors before heart failure", sp="dog", conf="moderate", dirn="noeffect",
   basis="2 randomised placebo-controlled trials, 229 and 124 dogs",
   src='SVEP, 2002 &middot; VETPROOF, 2007',
   tags=["Both failed their primary endpoint","SVEP restricted to one breed","VETPROOF conclusions rest on secondary endpoints"],
   verdict="Two placebo-controlled trials set out to show that ACE inhibition delays heart failure in preclinical mitral valve disease, and neither did. That is a reasonably firm negative rather than an absence of evidence. VETPROOF is nonetheless cited as positive on the strength of secondary endpoints its design cannot carry. The same drug behaved the same way in the equivalent human trial."),
 dict(stage="clin", soon=True, qual="on 39 events in a trial two thirds of dogs did not finish", t="Spironolactone added to standard heart-failure therapy", sp="dog", conf="low", dirn="benefit",
   basis="1 randomised trial, 212 dogs, placebo-controlled and double-blind",
   src='Bernay et al., 2010',
   tags=["Funded by the manufacturer, four of seven authors employed there","Around two thirds of dogs did not complete","Only 39 events in total","Composite includes a soft investigator-defined component"],
   verdict="Spironolactone added to standard heart-failure therapy points to benefit, but the result rests on 39 events in a trial that around two thirds of dogs did not complete, and part of the composite endpoint was defined by the investigators. The manufacturer funded the study and employed four of the seven authors. The much larger human trials of the same drug are the stronger reason for using it."),
 dict(stage="pre", t="Spironolactone with benazepril to delay the onset of heart failure", sp="dog", conf="moderate", dirn="noeffect",
   basis="1 randomised trial, 184 dogs, placebo-controlled",
   src='DELAY, 2020',
   tags=["Failed its primary endpoint (p = 0.45)","Single-blinded","Funded by the manufacturer","Conclusion rests on surrogate secondary endpoints"],
   verdict="DELAY, which tested spironolactone with benazepril before heart failure, failed its primary endpoint, and time to heart failure was numerically worse in the treated dogs. The authors state this plainly; the abstract then rests its conclusion on echocardiographic and NT-proBNP changes, which are surrogates. Read as it was designed, this is evidence that the combination does not delay the onset of heart failure."),
 dict(stage="clin", t="Furosemide dose and dosing frequency in stage C disease", sp="dog", conf="none", dirn="untested",
   basis="No studies", src='', tags=["Practice rests on convention"], verdict="No study has compared doses or dosing intervals of furosemide in dogs with heart failure. Practice derives from convention and from what worked in the individual animal. This is among the most frequently made decisions in cardiology and among the least examined, and the same gap exists in human medicine, so it is not a failing peculiar to this field."),
]),
("Dilated cardiomyopathy (dogs)", [
 dict(stage="pre", soon=True, qual="on time to event, not on the primary endpoint as originally analysed; Dobermanns only", t="Pimobendan in preclinical dilated cardiomyopathy (Dobermanns)", sp="dog", conf="low", dirn="benefit",
   basis="1 randomised trial, 76 dogs, placebo-controlled and double-blind",
   src='PROTECT, 2012',
   tags=["Primary endpoint not met by proportion (p = 0.1)","Interim analysis was not pre-planned","76 dogs, from around 1000 screened","One breed only","Funded by the manufacturer"],
   verdict="PROTECT, the preclinical pimobendan trial in Dobermanns, is routinely cited as positive. The proportion of dogs reaching its primary endpoint did not differ; the significant result comes from a time-to-event analysis at an interim look that was not pre-planned. Seventy-six Dobermanns were enrolled from around a thousand screened, so the finding is narrow as well as fragile, and applies to one breed."),
 dict(stage="clin", soon=True, t="Diet change and taurine in diet-associated dilated cardiomyopathy", sp="dog",
   conf="verylow", dirn="unclear",
   basis="1 retrospective review and 2 uncontrolled prospective cohorts, 24 to 71 dogs",
   src='Kaplan, 2018 &middot; Freid, 2021 &middot; Freeman, 2022',
   qual="the improvement cannot be separated from the heart drugs started at the same time",
   tags=["No dog anywhere kept its original diet","No randomisation, no blinding","Echocardiograms read unblinded, by the authors' own admission",
         "Taurine given alongside the diet change","Cardiac medication started at the same time","Cases recruited during an FDA publicity campaign",
         "The 2022 prospective study was funded by a pet food manufacturer"],
   verdict="In the diet-associated dilated cardiomyopathy literature, every dog in every study changed diet, so no comparison group exists. Improvement is confounded with pimobendan and furosemide started at the same time, with taurine supplementation, and with regression to the mean in animals enrolled at their worst measurement. Echocardiograms were read unblinded. The one study without industry funding is also the one stating that causation cannot be shown."),
 dict(stage="pre", t="Screening intervals in at-risk breeds", sp="dog", conf="none", dirn="untested",
   basis="No studies", src='', tags=["Expert opinion only"], verdict="No study has compared screening intervals against any outcome. The intervals in current guidelines are expert judgement, offered as such by their authors and cited afterwards as though established. Whether annual screening detects disease earlier than biennial screening, and whether earlier detection changes what happens to the dog, are both unanswered."),
]),
("Feline cardiomyopathy", [
 dict(stage="clin", soon=True, qual="compared with aspirin, in cats that had already thrown one clot", t="Clopidogrel to prevent recurrent arterial thromboembolism", sp="cat", conf="moderate", dirn="benefit",
   basis="1 randomised trial, 75 cats, double-blind, active comparator, clinical endpoint",
   src='FAT CAT, 2015',
   tags=["Independently funded","Active comparator, no placebo","75 cats, wide confidence intervals","Published in a supplement issue"],
   verdict="Clopidogrel after arterial thromboembolism carries the strongest independently funded evidence on this map: a double-blind randomised trial, paid for by the Morris Animal Foundation, showing longer time to recurrence than aspirin. Seventy-five cats gives wide confidence intervals, and the comparator was aspirin rather than placebo. In human medicine this drug class is the fallback rather than the preferred option, and no comparison against anticoagulation exists in cats."),
 dict(stage="pre", t="Atenolol in preclinical hypertrophic cardiomyopathy", sp="cat", conf="low", dirn="noeffect",
   basis="1 prospective observational cohort, 63 cats, not randomised or blinded",
   src='Schober et al., 2013',
   tags=["Open label, treatment not randomised","Five-year follow-up but no control for why cats were treated"],
   verdict="The atenolol evidence in preclinical hypertrophic cardiomyopathy is frequently described as a trial. It is a prospective observational cohort, open-label and not randomised, so the reason a cat was treated cannot be separated from what happened to it. Within those limits it found no difference in all-cause or cardiac mortality over five years. The human evidence in non-obstructive disease points against treating."),
 dict(stage="clin", t="Pimobendan in feline congestive heart failure", sp="cat", conf="verylow", dirn="unclear",
   basis="Retrospective records only", src='',
   tags=["Retrospective","Selection bias","No prospective study"], verdict="Pimobendan in feline congestive heart failure rests on retrospective records alone, with no prospective study and no control group. Cats given the drug were selected by their clinicians for reasons the records do not capture. The usual justification is extrapolation from dogs, and the human trials of oral inotropes are a reason to be careful about extrapolating this particular class. Widely used, and essentially untested."),
 dict(stage="pre", more="review-rapamycin.html", t="Rapamycin (sirolimus) in subclinical hypertrophic cardiomyopathy", sp="cat", conf="verylow",
   dirn="unclear", surrogate=True,
   basis="1 randomised trial, 43 cats, surrogate endpoint only",
   src='RAPACAT, 2023 &middot; FDA FOI summary 141-604, 2025 &middot; <a href="review-rapamycin.html">full appraisal</a>',
   tags=["FDA records that the endpoint was chosen after exploratory analysis; the paper does not","The report calls itself nonpivotal, exploratory and dose-determining","Alpha set at 0.10, three contrasts, no correction","Overall treatment effect not significant","No individual wall measurement significant at day 180","Analysed per protocol","All cardiac withdrawals in the high-dose arm","Transaminase elevations in 15 of 24 cats in the laboratory safety study, with no dose-response","No safety study enrolled a cat with cardiomyopathy or used the label regimen","Funded by the sponsor"],
   verdict="RAPACAT is a dose-finding study, described as such by its own authors, that is now carrying a marketing approval. Wall thickness at six months was 7.41&nbsp;mm on low dose against 8.40&nbsp;mm on placebo, but the overall treatment effect was not significant and alpha was set at 0.10 across three uncorrected contrasts. The FDA record states that the endpoint was selected after exploratory analysis, which the published paper does not disclose. Wall thickness is in any case a proxy for heart failure rather than heart failure."),
 dict(stage="pre", t="Any therapy that delays the onset of heart failure in hypertrophic cardiomyopathy", sp="cat",
   conf="none", dirn="untested", basis="No study with a clinical endpoint", src='',
   tags=["Every trial to date has measured wall thickness"], verdict="No study with a clinical endpoint has tested whether any drug delays the onset of heart failure in feline hypertrophic cardiomyopathy. Every trial so far has measured wall thickness instead. Until one measures heart failure, survival or quality of life, this question is unanswered rather than answered in the negative, and the two should not be confused."),
 dict(stage="pre", more="review-steroids-chf.html", t="Do glucocorticoids precipitate congestive heart failure?", sp="cat", conf="low", dirn="against",
   basis="1 case series, 3 dosing studies, 1 cohort of 1042 cats",
   src='Smith, 2004 &middot; Ployngam, 2006 &middot; Khelik, 2019 &middot; Dutch, 2023 &middot; <a href="review-steroids-chf.html">full commentary</a>',
   tags=["Original series had no control group, no denominator and no pre-treatment echocardiograms","Dosing studies are mixed: two negative, one found larger atrial and ventricular dimensions","No dosing study has enrolled a cat with cardiomyopathy","Largest cohort found no excess","Steroid exposure equal in transient thickening and true cardiomyopathy"],
   verdict="That glucocorticoids precipitate congestive heart failure in cats is widely taught, and the evidence does not establish it. The experimental literature is mixed rather than negative: plasma volume expansion has been demonstrated after methylprednisolone acetate, and one study found larger atrial and ventricular dimensions after short oral courses, while two others found nothing. No cat in any of them developed heart failure, and none of them enrolled a cat with cardiomyopathy, which is the population in which the effect is supposed to occur. In the only cohort with a control group, heart failure occurred in 0.82% of treated cats against 1.90% of untreated ones."),
]),
("Congestive heart failure: management", [
 dict(stage="clin", soon=True, qual="not much worse than furosemide over three months; superiority was not shown", t="Torasemide as an alternative to furosemide (dogs)", sp="dog", conf="low", dirn="noeffect",
   basis="1 randomised non-inferiority trial, 366 dogs, active comparator, 3 months",
   src='TEST, 2017',
   tags=["Non-inferiority margin set at minus 20%","Survival composite was secondary and analysed after the fact","Two trials pooled with different dosing rules","Three-month follow-up only","Funded by the manufacturer, five of nine authors employed there"],
   verdict="TEST was designed to show that torasemide is not appreciably worse than furosemide, and it showed that, against a non-inferiority margin of minus 20% chosen by the investigators. The survival hazard ratio widely quoted from it was a secondary endpoint analysed after the fact, pooled across two trials with different dosing rules. Follow-up was three months."),
 dict(stage="clin", t="Sacubitril&ndash;valsartan (ARNi) in congestive heart failure", sp="dog", conf="verylow", dirn="unclear",
   basis="1 retrospective cohort, 50 dogs, no control group",
   src='Carlson &amp; Stern, 2026',
   tags=["No control group","Cardiologist-selected cases","Dosing extrapolated from human medicine","Survival compared against expectation, not a comparator"], verdict="The evidence for sacubitril&ndash;valsartan in dogs is fifty animals, retrospective, with no control group, cases selected by cardiologists, dosing extrapolated from human medicine, and survival compared against expectation rather than against a comparator. No design of that kind can separate a drug effect from case selection. The human evidence for this drug is among the strongest in cardiology, which is a reason to run the trial rather than to skip it."),
 dict(stage="clin", t="Dietary sodium restriction", sp="dog", conf="none", dirn="untested",
   basis="No studies in dogs", src='', tags=["Extrapolated from human medicine"], verdict="No trial in dogs has tested sodium restriction against any outcome. The practice is extrapolated from human medicine, where a randomised trial has since found no effect on death or hospitalisation. Restriction also reduces palatability in animals that frequently eat poorly already, so the cost of the advice is not zero even if the benefit were real."),
 dict(stage="clin", t="Exercise restriction after diagnosis", sp="dog", conf="none", dirn="untested",
   basis="No studies", src='', tags=["Convention only"], verdict="Exercise restriction is advised almost universally after a cardiac diagnosis, on no evidence in either species. Human patients with heart failure are prescribed supervised aerobic training instead, and it is safe in advanced disease. Restricting exertion to prevent sudden death in an arrhythmogenic cardiomyopathy is a different question from restricting it in stable heart failure, and is equally untested."),
]),
("Arrhythmias", [
 dict(stage="clin", qual="for heart rate, which is not the same as feeling better or living longer", t="Rate control in atrial fibrillation: diltiazem with digoxin versus monotherapy", sp="dog",
   conf="low", dirn="benefit", surrogate=True,
   basis="1 randomised crossover study, 18 dogs, surrogate endpoint",
   src='Gelzer et al., 2009',
   tags=["18 dogs","Two weeks per arm","Measures heart rate, not survival or signs"],
   verdict="Diltiazem with digoxin controls ventricular rate in atrial fibrillation better than either drug alone. That much is shown, in eighteen dogs over two weeks per arm. Whether controlling rate in this way changes clinical signs, survival, or anything an owner would notice has not been studied. The endpoint here is a measurement rather than an outcome."),
 dict(stage="clin", qual="for ectopy counts; syncope did not differ between the two effective arms", t="Sotalol versus mexiletine&ndash;atenolol in Boxer arrhythmogenic cardiomyopathy", sp="dog",
   conf="low", dirn="benefit", surrogate=True,
   basis="1 randomised four-arm study, 49 Boxers, surrogate endpoint",
   src='Meurs et al., 2002',
   tags=["Around 11 to 16 dogs per arm","21 to 28 days","Measures VPC counts","Syncope did not differ between the two effective arms"],
   verdict="Sotalol and mexiletine&ndash;atenolol both reduce ventricular ectopy in Boxers, across four arms and forty-nine dogs over three to four weeks. Whether either reduces sudden death is untested, and syncope did not differ between the two effective arms. Suppressing ectopy is the exact intervention that raised mortality in human trials, which is why the distinction matters here."),
 dict(stage="pre", t="When to treat ventricular arrhythmias in asymptomatic dogs", sp="dog", conf="none", dirn="untested",
   basis="No outcome data", src='', tags=["No study links treatment to survival"], verdict="No study links antiarrhythmic treatment of asymptomatic ventricular ectopy in dogs to survival, in either direction. The same question was asked directly in human medicine and answered against treatment: mortality rose while the Holter recordings improved. Practice rests on the assumption that fewer ectopics is better, and that assumption is the one that failed."),
 dict(stage="pre", t="Holter thresholds that predict sudden death", sp="dog", conf="low", dirn="unclear",
   basis="Screening cohorts, 28 Dobermanns on seven-day monitoring",
   src='Wess et al., 2017 &middot; Gunasekaran et al., 2020',
   tags=["Breed cutoffs are screening conventions","No prospective outcome validation found","Positivity depends on how long you record"],
   verdict="The Holter cutoffs used to predict sudden death are screening conventions rather than thresholds validated prospectively against outcome. Whether a dog falls above or below one depends partly on how long it was recorded: six of eleven positive Dobermanns in a seven-day study were identified only after the first day. The same animal can be classified either way by the same test."),
]),
]

NQ    = sum(len(qs) for _, qs in Q)
NDOM  = len(Q)
NGAP  = sum(1 for _, qs in Q for q in qs if q['conf'] == 'none')
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
                more = f'<p class="seemore"><a href="{q["more"]}">&#42; Caveats in full &mdash; read the appraisal</a></p>'
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

body = f"""
<div class="kicker">Evidence and gap map</div>
<h1>Small-animal cardiology</h1>
<p class="standfirst">{WORD[NQ]} clinical questions and practices in small-animal cardiology, each assessed for the certainty of the evidence behind it and for what that evidence actually says. {WORD[NGAP]} have no supporting evidence of any kind.</p>
<div class="meta"><span>Living document</span><span>{NQ} entries &middot; {NDOM} domains</span><span>Revised August 2026</span></div>

<section>
  <h2>How each question is assessed</h2>
  <p>Study design determines where the assessment begins; it does not determine where it ends. A randomised trial that measured a surrogate outcome, was funded by the manufacturer of the drug under test and has never been replicated may warrant less confidence than a well-conducted observational study. Each question therefore carries two marks rather than one composite score.</p>
  <p><strong>Certainty</strong> is the first mark. It is a GRADE-informed editorial judgement rather than a formal GRADE assessment: design sets the starting point, certainty is then rated down for risk of bias, imprecision, indirectness and inconsistency, and may be rated up for a large and consistent effect. GRADE itself has four levels; the fifth label used here, <em>No evidence</em>, is an editorial category for questions nobody has studied and has no GRADE equivalent.</p>
  <p><strong>Direction</strong> is the second, with the studies on which it rests. The reasons certainty was not rated higher are set out in the assessment of each entry, so that the judgement can be examined and disputed.</p>
  <div class="gradekey">{key}</div>
  <p class="note" style="margin-top:18px">One editorial rule is applied without exception: <strong>evidence resting solely on a surrogate outcome cannot be rated above Very low, irrespective of design.</strong> Wall thickness, ectopic counts and circulating biomarkers are proxies for outcomes that matter to the patient, and a proxy can improve without the patient benefiting. The principle is taken from SORT, the grading scheme used in human primary care, which assigns its weakest recommendation grade to evidence resting on disease-oriented outcomes; the hard cap applied here is this site's rule, not SORT's, since SORT grades recommendations rather than bodies of evidence. Those questions are flagged.</p>
</section>

<section>
  <h2>Summary of findings</h2>
  <p>Every entry on the map, with the evidence that exists behind it and the assessment that follows. Each row links to the full entry below, where the verdict and the specific limitations are set out.</p>
  <div class="maplegend">
    <p class="lgrow"><span class="lglab">Domain</span>{splegend}</p>
  </div>
  <div class="tscroll">{compare}</div>
  <p class="scrollhint scrollhint--cmp">Scroll the table sideways for the assessment column.</p>
  <p class="note" style="margin-top:16px"><strong>Table 1.</strong> Certainty is a GRADE-informed editorial judgement and direction is recorded separately; neither is derived from study design alone.</p>
</section>

<section class="callout">
  <h2>The same drugs, in people</h2>
  <p>Much of small-animal cardiology is extrapolated from human cardiology, and the extrapolation is seldom stated. Human and animal cardiac disease differ enough that a human trial rarely settles a veterinary question &mdash; but drug classes travel further than diseases do, and several of these classes have been tested in people at a scale veterinary medicine will never reach.</p>
  <p>Oral inotropes increased mortality in two placebo-controlled trials. Suppressing asymptomatic ventricular ectopy after myocardial infarction more than doubled it, with no warning on any intermediate measure. Beta blockade in non-obstructive hypertrophic cardiomyopathy reduced exercise capacity against placebo. Glucocorticoids are given in human heart failure deliberately, to improve diuresis, rather than withheld.</p>
  <p>A companion page sets out each intervention class: what was tested in people, what it showed, and an explicit judgement of how close the analogy is &mdash; from close, through partial, to no analogue at all.</p>
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
  <p>This map is incomplete and under revision. Every mark is a judgement; the reasons behind each are listed rather than summarised so that they can be checked and disputed. Corrections and omitted citations are welcome. See <a href="about.html">about</a>.</p>
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
