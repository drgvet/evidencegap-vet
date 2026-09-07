"""Specialty and subtopic pages.

Laid out the way a journal lays out its article list: a row of tabs across the
top, then a grid of items. Each item carries a small label line, a title, and
the studies it rests on. No counts, no summaries of the collection.

Nothing here has its own text. Every word comes from content/gapmap.txt.
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


def slug(t):
    t = _re.sub(r'&[a-z]+;', '-', t)
    return _re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')[:58].strip('-')


HUB = 'cardiology.html'
PAGES = [(d, f'topic-{slug(d)}.html', qs) for d, qs in Q]


def tabs(active):
    """The row across the top, one per subtopic, the way a journal does it."""
    out = f'<a href="{HUB}"' + (' class="on"' if active is None else '') + '>All</a>'
    for domain, fn, _ in PAGES:
        on = ' class="on"' if active == domain else ''
        out += f'<a href="{fn}"{on}>{domain}</a>'
    return f'<nav class="tabrow">{out}</nav>'


def card(q):
    """One question, set as an item in the grid."""
    title = q['t']
    if q.get('more'):
        title = f'<a href="{q["more"]}">{title}</a>'
    src = q.get('src') or ''
    src = _re.sub(r'\s*(&middot;|·)\s*<a [^>]*>[^<]*(appraisal|commentary)</a>\s*$',
                  '', src)
    src = f'<p class="isrc">{src}</p>' if src.strip() else ''
    read = ''
    if q.get('more'):
        read = f'<p class="iread"><a href="{q["more"]}">Read the appraisal</a></p>'
    elif q.get('soon'):
        read = '<p class="iread soon">Appraisal in preparation</p>'
    return (f'<article class="item">'
            f'<p class="ilab"><span class="cf cf--{q["conf"]}">{CONF[q["conf"]]}</span>'
            f'<span class="idir">{DIRN[q["dirn"]]}</span></p>'
            f'<h3>{title}</h3>{src}{read}</article>')


def grid(qs):
    return '<div class="itemgrid">' + ''.join(card(q) for q in qs) + '</div>'


# ------------------------------------------------------------- subtopics
for domain, fn, qs in PAGES:
    body = f"""
<div class="kicker">Cardiology</div>
<h1>{domain}</h1>
{tabs(domain)}
{grid(qs)}
"""
    open(fn, 'w', encoding='utf-8').write(page(
        fn, f'{domain} &mdash; evidencegap.vet',
        f'The evidence behind clinical practice in {domain.lower()}.',
        body, width='wide'))

# ------------------------------------------------------------- specialty
featured = [q for _, qs in Q for q in qs if q.get('more')]
rest = [q for _, qs in Q for q in qs if not q.get('more')]

feat = ''
if featured:
    feat = (f'<section class="sec"><h2>Appraised in full</h2>'
            f'{grid(featured)}</section>')

body = f"""
<div class="kicker">Specialty</div>
<h1>Cardiology</h1>
<p class="standfirst">What the evidence behind each practice actually is,
question by question.</p>
{tabs(None)}
{feat}
<section class="sec"><h2>Everything else on the map</h2>
{grid(rest)}
<p class="note" style="margin-top:26px"><a href="gapmap.html">See the whole map
on one page, with the summary table</a></p>
</section>
"""
open(HUB, 'w', encoding='utf-8').write(page(
    HUB, 'Cardiology &mdash; evidencegap.vet',
    'Small-animal cardiology: what the evidence behind each practice actually is.',
    body, width='wide'))

print(f'wrote {HUB} and {len(PAGES)} subtopic pages')
