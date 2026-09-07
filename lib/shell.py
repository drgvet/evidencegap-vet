FONTS = ''  # system font stacks only; no webfont request

NAV = [('index.html','Home'),('cardiology.html','Cardiology'),('gapmap.html','Gap map'),
       ('human-evidence.html','Human evidence'),('reviews.html','Appraisals'),
       ('teaching.html','Teaching'),('about.html','About')]

FOOTER = (
 '<div class="footgrid">'
   '<div>'
     '<div class="fmark">evidencegap<span class="tld">.vet</span></div>'
     '<p class="fnote">Working out which bits of small-animal practice are '
     'actually backed by evidence.</p>'
   '</div>'
   '<div><p class="fh">Browse</p><ul>'
     '<li><a href="index.html">Home</a></li>'
     '<li><a href="gapmap.html">Gap map</a></li>'
     '<li><a href="human-evidence.html">Human evidence</a></li>'
     '<li><a href="reviews.html">Appraisals</a></li>'
   '</ul></div>'
   '<div><p class="fh">About</p><ul>'
     '<li><a href="teaching.html">Teaching</a></li>'
     '<li><a href="about.html">About the project</a></li>'
     '<li><a href="about.html#contact">Contact</a></li>'
   '</ul></div>'
   '<div><p class="fh">Contact</p><ul>'
     '<li><a href="mailto:contact@evidencegap.vet">contact@evidencegap.vet</a></li>'
   '</ul></div>'
 '</div>'
 '<div class="footrow">'
   '<span>&copy; 2026 evidencegap.vet</span>'
   '<span>Editorial appraisals of published literature. Not peer reviewed, and not clinical advice.</span>'
   '<span>Unaffiliated with any institution, journal or sponsor.</span>'
 '</div>')

import re as _re

_HEAD = _re.compile(
  r'^\s*(<div class="kicker">.*?</div>)\s*(<h1>.*?</h1>)\s*'
  r'(<p class="standfirst">.*?</p>)\s*(<div class="meta">.*?</div>)?\s*', _re.S)

_ART = ('<svg class="pheroart" viewBox="0 0 300 200" aria-hidden="true" '
        'xmlns="http://www.w3.org/2000/svg">'
        '<circle cx="232" cy="58" r="62" fill="var(--pab)" opacity=".16"/>'
        '<circle cx="150" cy="140" r="40" fill="var(--pab)" opacity=".10"/>'
        '<circle cx="252" cy="150" r="26" fill="var(--accent)" opacity=".13"/>'
        '<circle cx="176" cy="46" r="30" fill="none" stroke="var(--accent)" '
        'stroke-width="2" stroke-dasharray="9 7" opacity=".34"/>'
        '<circle cx="286" cy="106" r="11" fill="var(--pab)" opacity=".30"/></svg>')

def split_hero(body):
    """Lift a leading kicker / h1 / standfirst / meta block into a coloured band."""
    m = _HEAD.match(body)
    if not m:
        return '', body
    parts = ''.join(x for x in m.groups() if x)
    hero = ('<section class="phero"><div class="bar">'
            f'<div class="pheroin">{parts}</div>{_ART}</div></section>')
    return hero, body[m.end():]

def masthead(current):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ''
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    return ('<header class="topbar"><div class="bar">'
            '<div class="mark"><a href="index.html">evidencegap<span class="tld">.vet</span></a></div>'
            '<nav class="nav">' + ''.join(links) + '</nav>'
            '</div></header>')

THEME = {'gapmap.html':'navy', 'human-evidence.html':'green',
         'reviews.html':'rust', 'review-rapamycin.html':'rust',
         'review-steroids-chf.html':'rust', 'review-pimobendan-b2.html':'rust',
         'teaching.html':'plum',
         'about.html':'navy', '404.html':'navy', 'index.html':'navy'}

def page(fn, title, desc, body, width='', extra_head='', script='', raw=False, hero=True):
    cls = 'col' if not width else 'col--' + width
    if raw:
        return _shell(fn, title, desc, body, extra_head, script,
                      open_tag='<main class="flow">', close_tag='</main>')
    band, body = split_hero(body) if hero else ('', body)
    pagecls = 'page page--hero' if band else 'page'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:site_name" content="evidencegap.vet">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://evidencegap.vet/{fn}">
<meta name="twitter:card" content="summary">
<link rel="canonical" href="https://evidencegap.vet/{fn}">
{FONTS}
<link rel="stylesheet" href="assets/site.css">{extra_head}
</head>
<body class="t-{THEME.get(fn,'navy')}">
{masthead(fn)}
{band}
<main class="{pagecls}"><div class="{cls}">
{body}
</div></main>
<footer class="botbar"><div class="bar">{FOOTER}</div></footer>{script}
</body>
</html>
"""


def _shell(fn, title, desc, body, extra_head, script, open_tag, close_tag):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:site_name" content="evidencegap.vet">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://evidencegap.vet/{fn}">
<meta name="twitter:card" content="summary">
<link rel="canonical" href="https://evidencegap.vet/{fn}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="favicon.svg">
<meta name="theme-color" content="#FDFCFA">
{FONTS}
<link rel="stylesheet" href="assets/site.css">{extra_head}
</head>
<body class="t-{THEME.get(fn,'navy')}">
{masthead(fn)}
{open_tag}
{body}
{close_tag}
<footer class="botbar"><div class="bar">{FOOTER}</div></footer>{script}
</body>
</html>
"""
