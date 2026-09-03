import sys, json; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)));sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))),'lib'))
from shell import page
from human_data import HUMAN_REFS

ID = {q['title']: q['id'] for q in json.load(open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'questions.json')))}

TB = {'close':  ('Close analogue',   'close'),
      'partial':('Partial analogue', 'part'),
      'poor':   ('Poor analogue',    'poor'),
      'none':   ('No analogue',      'noan')}

# Each block: id, drug or decision class, what the human trials show,
# how far the analogy carries, and the veterinary questions it bears on.
CATS = [
("inotropes", "Oral inotropes", "partial",
 """<p>Two large placebo-controlled trials tested oral phosphodiesterase-3 inhibition
 in chronic heart failure and both were stopped for harm. Milrinone increased all-cause
 mortality by 28% in 1,088 patients with severe heart failure. Vesnarinone increased
 mortality dose-dependently in 3,833 patients, 22.9% against 18.9%, while
 <em>improving</em> quality-of-life scores in the same trial. The excess deaths in both
 were predominantly sudden.</p>""",
 """<p>Milrinone and vesnarinone are phosphodiesterase-3 inhibitors alone. Pimobendan
 combines phosphodiesterase-3 inhibition with calcium sensitisation, which is argued to
 raise contractility with a smaller rise in intracellular calcium and myocardial oxygen
 demand. The trial populations differ as well: those patients had predominantly ischaemic
 systolic dysfunction, in which the arrhythmic substrate thought to drive the excess
 mortality is already present. Myxomatous mitral valve disease is a volume-overload lesion
 in a non-ischaemic ventricle.</p>
 <p>Those differences are real and may be sufficient. What they do not do is dispose of the
 human result. The mechanism of harm was never established, so the mechanistic argument for
 exemption is an assertion rather than a finding; and neither EPIC nor QUEST was designed to
 detect a mortality difference of that size, death being one component of a composite
 primary endpoint in both.</p>""",
 ["Pimobendan in preclinical stage B2 disease",
  "Pimobendan in congestive heart failure",
  "Pimobendan in preclinical dilated cardiomyopathy (Dobermanns)",
  "Pimobendan in feline congestive heart failure",
  "Does preclinical pimobendan shorten survival once heart failure develops?"]),

("raas", "Renin&ndash;angiotensin&ndash;aldosterone blockade", "close",
 """<p>The best-populated area of the comparison. Enalapril in 4,228 asymptomatic patients
 with an ejection fraction of 35% or less cut the combined incidence of death or heart
 failure by 29%, and heart-failure hospitalisation by 20%, but <strong>did not reduce
 mortality</strong> (8% risk reduction, p&nbsp;=&nbsp;0.30). Spironolactone
 reduced mortality by 30% in severe heart failure, 35% against 46%, and eplerenone
 reproduced the effect in mild disease. Sacubitril&ndash;valsartan reduced cardiovascular
 death or heart-failure hospitalisation by 20% and all-cause death by 16% against an active
 comparator in 8,442 patients.</p>""",
 """<p>Neurohormonal activation is the shared final pathway, and the analogy holds better
 here than anywhere else on this page. It is not exact: human trials enrolled reduced
 ejection fraction of ischaemic or idiopathic origin, whereas canine heart failure is
 usually valvular with preserved systolic function until late.</p>
 <p>Read together, the two literatures say the same thing. Blockade before symptoms alters
 progression at best and has never shown a survival benefit in either species, which is
 what SVEP and VETPROOF found in dogs and what SOLVD-Prevention found in people. Blockade
 after symptoms appear is where benefit has been demonstrated. The difference between them
 is one of strength rather than direction: the canine spironolactone result rests on 39
 events, the human one on 1,663 patients.</p>""",
 ["ACE inhibitors before heart failure",
  "Spironolactone with benazepril to delay the onset of heart failure",
  "Spironolactone added to standard heart-failure therapy",
  "Sacubitril&ndash;valsartan (ARNi) in congestive heart failure"]),

("diuretics", "Loop diuretics", "close",
 """<p>Torsemide and furosemide were compared head to head in 2,859 patients discharged
 after a heart-failure hospitalisation, with no difference in all-cause mortality
 (HR&nbsp;1.02). Dose and route have been tested once, in hospital: DOSE randomised 308
 patients with acute decompensated heart failure to high-dose against low-dose intravenous
 furosemide and to bolus against continuous infusion, and both co-primary endpoints were
 null: no difference in symptom relief or creatinine for bolus versus infusion, and
 only a nonsignificant trend favouring the high dose (P&nbsp;=&nbsp;0.06). Outpatient dose
 and dosing interval, which is what most prescribing actually is, have not been settled by
 trial in either species.</p>""",
 """<p>Both species are being asked the same pharmacological question about the same class
 of drug acting on the same segment of the nephron, and the answers agree: the veterinary
 non-inferiority result says what a trial ten times larger says in people. The dosing gap
 is shared, not veterinary-specific, which is worth stating plainly rather than treating as
 a failure peculiar to this field.</p>""",
 ["Torasemide as an alternative to furosemide (dogs)",
  "Furosemide dose and dosing frequency in stage C disease"]),

("ectopy", "Suppression of ventricular ectopy", "partial",
 """<p>CAST randomised 1,727 patients with asymptomatic or minimally symptomatic ectopy
 after myocardial infarction to encainide, flecainide or placebo. The drugs suppressed
 ectopy as intended. Total mortality was 7.7% against 3.0%, a relative risk of about 2.5,
 and the trial was stopped early. No intermediate measure identified the harm: the Holter
 recordings improved throughout.</p>""",
 """<p>At drug level the analogy is weak. Encainide and flecainide are class&nbsp;Ic sodium
 channel blockers acting on scarred post-infarct myocardium, and the proarrhythmia is
 attributed to conduction slowing in that substrate. Sotalol and mexiletine belong to other
 classes, and arrhythmogenic cardiomyopathy in the Boxer is a different substrate again.</p>
 <p>At method level the analogy is exact, and that is the part that transfers. Ectopy count
 is a surrogate. It was suppressed, the surrogate moved in the intended direction, and the
 patients did worse. Any protocol judged on Holter suppression, in any species, is exposed
 to the same failure, and no amount of suppression can serve as evidence of benefit on its
 own.</p>""",
 ["When to treat ventricular arrhythmias in asymptomatic dogs",
  "Sotalol versus mexiletine&ndash;atenolol in Boxer arrhythmogenic cardiomyopathy",
  "Holter thresholds that predict sudden death"]),

("beta", "Beta blockade in hypertrophic cardiomyopathy", "partial",
 """<p>In obstructive disease, metoprolol reduced outflow gradients and improved symptoms
 against placebo, and remains a comparator in current trials. In <strong>non-obstructive</strong>
 disease a placebo-controlled triple-crossover trial found the opposite: bisoprolol reduced
 exercise capacity and quality of life and increased NT-proBNP and left atrial size. No
 trial in either phenotype has tested a hard outcome.</p>""",
 """<p>The diseases are not equivalent. Human hypertrophic cardiomyopathy is a sarcomeric
 genetic disorder with an established mutation in around half of patients; feline
 hypertrophic cardiomyopathy is heterogeneous and, outside two breed-specific mutations, of
 unknown genotype.</p>
 <p>The distinction that does carry across is haemodynamic rather than genetic. Beta
 blockade helps the obstructive phenotype by slowing the heart and reducing the gradient,
 and appears to harm the non-obstructive one by limiting the rate response a stiff ventricle
 depends on. Most cats given atenolol are subclinical and non-obstructive, which is the
 phenotype in which the human evidence is negative rather than merely absent.</p>""",
 ["Atenolol in preclinical hypertrophic cardiomyopathy"]),

("antithrombotic", "Antithrombotic therapy", "poor",
 """<p>Clopidogrel with aspirin was compared directly with oral anticoagulation for stroke
 prevention in atrial fibrillation and was inferior, the trial stopping early
 (RR&nbsp;1.44 favouring anticoagulation). Across the wider trial literature, antiplatelet
 therapy reduced stroke by about 22% and adjusted-dose warfarin by about 64%. In atrial
 fibrillation, antiplatelet therapy is inferior to oral anticoagulation and is not
 considered an equivalent substitute for it where anticoagulation is indicated.</p>""",
 """<p>This is the weakest analogy on the page. The human evidence concerns cerebral
 embolism from the left atrial appendage in atrial fibrillation. Feline arterial
 thromboembolism is usually distal aortic, arises from an atrium enlarged by cardiomyopathy,
 frequently in sinus rhythm, and occurs in a species in which anticoagulant monitoring is
 impractical and the bleeding trade-off is therefore different.</p>
 <p>What transfers is a question rather than an answer. The comparison that settled the
 human field, antiplatelet against anticoagulant, has not been made in cats.
 FAT&nbsp;CAT compared clopidogrel with aspirin, which is a comparison between two members
 of the weaker class.</p>""",
 ["Clopidogrel to prevent recurrent arterial thromboembolism"]),

("rate", "Rate control in atrial fibrillation", "partial",
 """<p>Lenient rate control, defined as a resting rate below 110&nbsp;bpm, was not inferior
 to strict control for a composite of cardiovascular events in 614 patients, and was far
 easier to achieve.</p>""",
 """<p>The arrhythmia is the same; the setting is not. Human atrial fibrillation is
 frequently lone or hypertensive with preserved ventricular function, whereas canine atrial
 fibrillation usually accompanies advanced structural disease at much higher rates. The
 targets are not interchangeable either, being derived from Holter averages in dogs and
 resting rate in people.</p>
 <p>What survives translation is the burden of proof. Aggressive rate targets were assumed
 to be better until they were tested, and then were not.</p>""",
 ["Rate control in atrial fibrillation: diltiazem with digoxin versus monotherapy"]),

("sodium", "Sodium restriction and exercise", "partial",
 """<p>Both have been tested in humans and neither supports restriction. Reducing dietary
 sodium below 100&nbsp;mmol per day made no difference to death or hospitalisation
 (HR&nbsp;0.89, not significant) in 806 randomised patients. Supervised aerobic training in
 2,331 patients with chronic heart failure missed its primary endpoint
 (HR&nbsp;0.93, p&nbsp;=&nbsp;0.13) and reached significance only after adjustment for
 prespecified prognostic variables; it was safe in advanced disease.</p>""",
 """<p>Sodium intake is not comparable between a free-living human adding salt at table and
 a dog eating a formulated diet, and the achievable range of restriction differs
 accordingly. Exercise advice needs separating too: where restriction is advised in a dog
 with an arrhythmogenic cardiomyopathy the aim is preventing sudden death during exertion,
 a different question from functional capacity in stable heart failure, and one the human
 exercise trials do not address.</p>
 <p>For the ordinary case, a dog with stable treated heart failure told to stay
 quiet and fed a sodium-restricted diet, neither practice has a trial behind it in
 either species, and the human trials that do exist are neutral or point the other way.</p>""",
 ["Dietary sodium restriction", "Exercise restriction after diagnosis"]),

("steroids", "Glucocorticoids", "partial",
 """<p>Two separate literatures, and they point different ways. <b>Acute exposure:</b> a
 self-controlled case series of 2,623,327 adults given a single oral burst of fourteen days or
 less found a heart-failure incidence rate ratio of <b>2.37 (2.13&ndash;2.63) at days 5 to
 30</b>, attenuating thereafter, at an absolute rate of 1.3 per 1000 person-years. The commonest
 indications were skin disorders and respiratory infections. <b>Therapeutic use:</b> prednisone
 is given deliberately in heart failure to augment diuresis, and a randomised pilot in acute
 heart failure with raised C-reactive protein reported fewer events at 90 days (HR&nbsp;0.31).</p>
 <p><b>The mechanism has been measured.</b> Six normal subjects given five days each of
 prednisolone, <b>methylprednisolone</b>, <b>triamcinolone</b> and dexamethasone showed no weight
 gain, <em>increased</em> urinary sodium excretion, and plasma volume unchanged on radiolabelled
 albumin. The volume effect belongs to cortisol, not to the synthetics, although
 methylprednisolone <em>pulses</em> do suppress urinary sodium for up to 32 hours, with escape.</p>""",
 """<p>The acute association is the closest human analogue to the feline claim, and it is
 confounded in exactly the same way: people receive steroid bursts because they are acutely
 unwell, and respiratory infection is itself a common precipitant of decompensation. Drug and
 precipitant arrive together, just as illness, handling and stress arrive together in the cat.</p>
 <p>The one population where that confounding was tested directly settles it as far as human data
 can. Among 11,356 patients in acute heart failure, those newly started on a corticosteroid had
 worse crude outcomes &ldquo;essentially because corticosteroid-treated patients were
 sicker&rdquo;, and the difference disappeared on adjustment. Where allocation is random, nothing
 appears: 584 patients randomised to methylprednisolone or placebo for severe pneumonia had
 cardiovascular complications, on a definition explicitly including new or worsening
 congestive heart failure, in 4% against 5% by day 28.</p>
 <p>So the transfer is partial in a specific way. The <em>mechanism</em> proposed in cats is not
 supported: plasma volume was measured after the exact drug classes used in cats and did not
 change. The <em>association</em> transfers completely, including its confounding.</p>""",
 ["Do glucocorticoids precipitate congestive heart failure?"]),

("mtor", "mTOR inhibition", "none",
 """<p>There is no human trial of rapamycin or an analogue in hypertrophic cardiomyopathy.
 The randomised human data concern everolimus and drug-induced left ventricular hypertrophy
 in transplant recipients, where the hypertrophic stimulus is a calcineurin inhibitor that
 is being withdrawn at the same time. The results are small and mixed and the design
 confounds the question.</p>""",
 """<p>Nothing to extrapolate from, in either direction. This is the one question on the map
 where the veterinary evidence leads the human literature, which is a statement about human
 medicine and not an endorsement of the veterinary trial. A single 43-cat study reporting an
 effect below the measurement noise of its own endpoint is weak evidence whether or not
 anyone else has done better.</p>""",
 ["Rapamycin (sirolimus) in subclinical hypertrophic cardiomyopathy"]),
]

NOEQ = [
 ("Pimobendan in preclinical stage B2 disease",
  "Inotropes are not given to people before symptoms appear, so no trial exists at this stage."),
 ("Spironolactone with benazepril to delay the onset of heart failure",
  "The corresponding human trials enrolled patients who already had symptoms."),
 ("Diet change and taurine in diet-associated dilated cardiomyopathy",
  "No equivalent condition, and no equivalent trial."),
 ("Screening intervals in at-risk breeds",
  "Family screening in inherited human cardiomyopathy is set by guideline, not by trial."),
 ("Any therapy that delays the onset of heart failure in hypertrophic cardiomyopathy",
  "Equally unanswered in humans; no trial has tested delay of onset."),
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
<p class="standfirst">What the human trials tested, what they found, and how far each result can reasonably be carried into small-animal cardiology. Organised by drug class rather than by disease, because it is the drug class that travels.</p>
<div class="meta"><span>{WORD[len(CATS)]} intervention classes</span><span>{len(HUMAN_REFS)} human trials cited</span><span>Revised August 2026</span></div>

<section>
  <h2>How far the comparison can be carried</h2>
  <p>Human and small-animal cardiac disease are not the same disease. Human heart-failure trials enrolled patients with predominantly ischaemic or idiopathic systolic dysfunction; the commonest canine cardiac disease is a primary valvular volume overload in a ventricle with normal coronary arteries. Human hypertrophic cardiomyopathy is a sarcomeric genetic disorder; feline hypertrophic cardiomyopathy is largely of unknown cause. Cardiac embolism in humans is atrial fibrillation causing stroke; in cats it is atrial enlargement causing distal aortic obstruction, usually in sinus rhythm.</p>
  <p>None of that makes the human literature irrelevant, and none of it makes the human literature decisive. Drug classes travel further than diseases do. A phosphodiesterase-3 inhibitor does the same thing to a myocyte in either species; whether the consequence is the same depends on the substrate it acts on, which is exactly what differs.</p>
  <p>This page therefore does not claim that a human result determines the veterinary answer. Each class is set out with what was tested, what it showed, and an explicit judgement of how close the analogy is. Where a class behaved badly in a large human trial, that is a reason to look for the equivalent signal in the veterinary data, and to notice when nobody has looked. It is not, by itself, evidence that the signal is there.</p>
  <div class="gradekey">{key}</div>
  <p class="note" style="margin-top:18px">The analogy judgements are the editor's and are open to argument. The trial results are not: every name, figure and effect direction below was checked against the primary report, and the citations are listed at the foot of the page.</p>
</section>

{blocks}

<section>
  <h2>Entries with no human counterpart</h2>
  <p>{WORD[len(NOEQ)]} entries on the map have nothing to compare against. That is worth recording separately, because an absent comparison is often mistaken for an unfavourable one.</p>
  <ul class="plain">{noeq}</ul>
</section>

<section>
  <h2>Human trials cited</h2>
  <ol class="reflist">{refs}</ol>
</section>

<section>
  <h2>Status</h2>
  <p>This page covers the intervention classes represented on the cardiology gap map and will grow with it. Corrections, and human trials that should be here and are not, are welcome. See <a href="about.html">about</a>.</p>
</section>
"""

open('human-evidence.html','w',encoding='utf-8').write(page(
 'human-evidence.html','The same drugs, in people &mdash; evidencegap.vet',
 'What the human trials of the same drug classes tested and found, and how far each result carries into small-animal cardiology.',
 body, width='mid'))
print('wrote human-evidence.html;', len(CATS), 'classes,', len(HUMAN_REFS), 'references')
