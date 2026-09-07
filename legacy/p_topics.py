"""Specialty and subtopic pages.

The gap map stays as the one-page view of everything. These add the layer
above it: a specialty hub listing its subtopics, and one page per subtopic
carrying only that subtopic's questions. Nothing here has its own text —
every word comes from content/gapmap.txt, so the two views can never
disagree.
"""

import os as _os
import re as _re
import sys

sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), 'lib'))

import records as _records                                    # noqa: E402
from shell import page                                        # noqa: E402

ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
Q = _records.as_questions(_os.path.join(ROOT, 'content', 'gapmap.txt'))

CONF = {'high': 'High certainty', 'moderate': 'Moderate certainty',
        'low': 'Low certainty', 'verylow': 'Very low certainty',
        'none': 'No evidence'}
DIRN = {'benefit': 'Points to benefit', 'noeffect': 'No benefit shown',
        'against': 'Points against', 'unclear': 'Cannot say either way',
        'untested': 'Untested'}
STAGES = [('pre', 'Asymptomatic'), ('clin', 'Symptomatic')]


def slug(t):
    t = _re.sub(r'&[a-z]+;', '-', t)
    return _re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')[:58].strip('-')


def qslug(t):
    return 'q-' + slug(t)


SPECIALTY = ('Cardiology', 'cardiology.html',
             'Small-animal cardiology: what the evidence behind each practice '
             'actually is, question by question.')


def entry(q):
    """One question, rendered the same way the gap map renders it."""
    sur = ('<span class="surro">Surrogate endpoint only</span>'
           if q.get('surrogate') else '')
    qual = f' &mdash; {q["qual"]}' if q.get('qual') else ''
    src = f'<p class="qsrc">{q["src"]}</p>' if q['src'] else ''
    if q.get('more'):
        more = (f'<p class="seemore"><a href="{q["more"]}">'
                f'&#42; Caveats in full &mdash; read the appraisal</a></p>')
    elif q.get('soon'):
        more = '<p class="seemore soon">&#42; Full appraisal in preparation</p>'
    else:
        more = ''
    return (f'<div class="q" id="{qslug(q["t"])}">'
            f'<div class="qhead"><div class="qtitle">{q["t"]}</div>'
            f'<span class="cf cf--{q["conf"]}">{CONF[q["conf"]]}</span></div>'
            f'<p class="qbasis">{q["basis"]}<br><b>{DIRN[q["dirn"]]}</b>'
            f'{qual}{sur}</p>'
            f'<p class="qverdict">{q["verdict"]}</p>{src}{more}</div>')


def counts(qs):
    n = len(qs)
    gaps = sum(1 for q in qs if q['conf'] == 'none')
    appraised = sum(1 for q in qs if q.get('more'))
    bits = [f'{n} question' + ('' if n == 1 else 's')]
    if gaps:
        bits.append(f'{gaps} with no evidence')
    if appraised:
        bits.append(f'{appraised} appraised in full')
    return ' &middot; '.join(bits)


# ------------------------------------------------------------- subtopics
built = []
for domain, qs in Q:
    fn = f'topic-{slug(domain)}.html'
    inner = ''
    for sk, slabel in STAGES:
        sub = [q for q in qs if q['stage'] == sk]
        if not sub:
            continue
        inner += (f'<div class="stageblock"><h4 class="stagelab">{slabel}</h4>'
                  + ''.join(entry(q) for q in sub) + '</div>')

    body = f"""
<div class="kicker">Cardiology</div>
<h1>{domain}</h1>
<p class="standfirst">{counts(qs)}. Each question carries the certainty of the
evidence behind it and, separately, what that evidence points to.</p>
<div class="meta"><span><a href="{SPECIALTY[1]}">All of cardiology</a></span>
<span><a href="gapmap.html">The full map, all domains on one page</a></span></div>

<div class="qgroup">{inner}</div>

<p class="note" style="margin-top:36px">
<a href="{SPECIALTY[1]}">&larr; Back to cardiology</a></p>
"""
    open(fn, 'w', encoding='utf-8').write(page(
        fn, f'{domain} &mdash; evidencegap.vet',
        f'The evidence behind clinical practice in {domain.lower()}.',
        body, width='mid'))
    built.append((domain, fn, qs))

# ------------------------------------------------------------- specialty
cards = ''
for domain, fn, qs in built:
    cards += (f'<li><h3><a href="{fn}">{domain}</a></h3>'
              f'<p class="cardmeta">{counts(qs)}</p></li>')

nq = sum(len(qs) for _, _, qs in built)
body = f"""
<div class="kicker">Specialty</div>
<h1>{SPECIALTY[0]}</h1>
<p class="standfirst">{SPECIALTY[2]}</p>
<div class="meta"><span>{nq} questions</span><span>{len(built)} subtopics</span>
<span><a href="gapmap.html">Or see the full map on one page</a></span></div>

<section class="sec">
  <h2>Subtopics</h2>
  <ul class="topiclist">{cards}</ul>
</section>
"""
open(SPECIALTY[1], 'w', encoding='utf-8').write(page(
    SPECIALTY[1], f'{SPECIALTY[0]} &mdash; evidencegap.vet',
    SPECIALTY[2], body, width='mid'))

print(f'wrote {SPECIALTY[1]} and {len(built)} subtopic pages')
