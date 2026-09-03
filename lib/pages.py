"""Page templates. Each takes a parsed content file and returns the page body."""

import re

from content import blocks, inline, read


def _rows(lines):
    """Lines of the form  Label :: text  ->  [(label, html)]"""
    out = []
    for line in lines:
        if '::' in line:
            k, _, v = line.partition('::')
            out.append((k.strip(), inline(v.strip())))
    return out


def _abstract(lines):
    """Lines of the form  :Label  followed by a paragraph."""
    out, lab, buf = [], None, []
    for line in lines:
        s = line.strip()
        if s.startswith(':') and not s.startswith('::'):
            if lab:
                out.append((lab, inline(' '.join(buf))))
            lab, buf = s[1:].strip(), []
        elif s:
            buf.append(s)
    if lab:
        out.append((lab, inline(' '.join(buf))))
    return out


def appraisal(path):
    meta, secs = read(path)

    named = {s['title'].lower(): s for s in secs if not s['num']}
    numbered = [s for s in secs if s['num']]

    # ---- sidebar -------------------------------------------------------
    rail_rows = ''
    for key, label in (('first_published', 'First published'),
                       ('published', 'Published'),
                       ('last_revised', 'Last revised'),
                       ('certainty', 'Certainty'),
                       ('direction', 'Direction'),
                       ('endpoint', 'Endpoint'),
                       ('method', 'Method'),
                       ('controlled_trials', 'Controlled trials')):
        if meta.get(key):
            rail_rows += f'<p class="row"><span>{label}</span>{meta[key]}</p>'
    known = {'first_published', 'published', 'last_revised', 'certainty', 'direction',
             'endpoint', 'method', 'controlled_trials', 'title', 'short_title', 'id',
             'kind', 'domain', 'keywords', 'related', 'abstract_heading', 'affil'}
    for k, v in meta.items():
        if k not in known and v:
            rail_rows += (f'<p class="row"><span>{k.replace("_", " ").capitalize()}'
                          f'</span>{v}</p>')

    top = [s for s in numbered if s['level'] == 2]
    contents = ''.join(
        f'<li><a href="#s{s["num"]}"><span class="n">{s["num"]}</span>{s["title"]}</a></li>'
        for s in top)
    if 'references' in named:
        contents += '<li><a href="#sR"><span class="n">&mdash;</span>References</a></li>'
    if 'declarations' in named:
        contents += '<li><a href="#sD"><span class="n">&mdash;</span>Declarations</a></li>'

    rail = f'''
  <div class="blk">
    <p class="type commentary">{meta.get('kind', 'Commentary')}</p>
    <p class="id">{meta.get('id', '')} &middot; {meta.get('domain', '')}</p>
  </div>
  <div class="blk">{rail_rows}</div>
  <div class="blk"><p class="lab">Contents</p><ol>{contents}</ol></div>
  <div class="blk"><p class="flag">Not peer reviewed</p></div>'''

    # ---- abstract and summary -----------------------------------------
    abstract = ''
    if 'abstract' in named:
        rows = _abstract(named['abstract']['lines'])
        inner = ''.join(f'<p><span class="runin">{k}</span>{v}</p>' for k, v in rows)
        head = meta.get('abstract_heading', 'Abstract')
        abstract = f'<div class="abstract"><h2>{head}</h2>{inner}</div>'

    summary = ''
    if 'summary' in named:
        rows = _rows(named['summary']['lines'])
        body_rows = ''.join(f'<div class="frow"><dt>{k}</dt><dd>{v}</dd></div>'
                            for k, v in rows)
        summary = (f'<div class="findings"><p class="flab">Summary</p>'
                   f'<dl>{body_rows}</dl></div>')

    # ---- body sections -------------------------------------------------
    out, i = '', 0
    while i < len(numbered):
        s = numbered[i]
        if s['level'] == 3:
            i += 1
            continue
        inner = blocks(s['lines'])
        subs = ''
        j = i + 1
        while j < len(numbered) and numbered[j]['level'] == 3:
            t = numbered[j]
            subs += (f'<div class="subsec" id="s{t["num"]}">'
                     f'<h3><span class="num">{t["num"]}</span>{inline(t["title"])}</h3>'
                     f'{blocks(t["lines"])}</div>')
            j += 1
        out += (f'<section class="sec" id="s{s["num"]}">'
                f'<h2><span class="num">{s["num"]}</span>{inline(s["title"])}</h2>'
                f'{inner}{subs}</section>')
        i = j

    # ---- references, declarations, cite-as -----------------------------
    if 'references' in named:
        items = ''
        for line in named['references']['lines']:
            m = re.match(r'^\s*(\d+)\.\s+(.*)$', line)
            if m:
                items += f'<li id="ref{m.group(1)}">{inline(m.group(2))}</li>'
        out += (f'<section class="sec" id="sR">'
                f'<h2><span class="num">&mdash;</span>References</h2>'
                f'<ol class="reflist">{items}</ol></section>')

    if 'declarations' in named:
        rows = _rows(named['declarations']['lines'])
        dl = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in rows)
        cite = ''
        if 'cite as' in named:
            txt = inline(' '.join(l.strip() for l in named['cite as']['lines'] if l.strip()))
            cite = f'<div class="citeas"><p class="lab">Cite as</p><p>{txt}</p></div>'
        out += (f'<section class="sec" id="sD">'
                f'<h2><span class="num">&mdash;</span>Declarations</h2>'
                f'<div class="notpeer">Not peer reviewed. This is an editorial appraisal.</div>'
                f'<div class="declare"><dl>{dl}</dl></div>{cite}</section>')

    kw = ''
    if meta.get('keywords'):
        kw = ('<p class="keywords"><b>Keywords:</b> '
              + ' &middot; '.join(k.strip() for k in meta['keywords'].split(','))
              + '</p>')

    related = ''
    if meta.get('related'):
        related = f'<p class="note" style="margin-top:36px">Related: {meta["related"]}</p>'

    return f'''
<div class="artgrid">
<aside class="rail">{rail}</aside>
<div class="article">

<div class="runhead">
  <span>evidencegap.vet &middot; {meta.get('kind', 'Commentary')}</span>
  <span>{meta.get('short_title', meta.get('domain', ''))}</span>
  <span>{meta.get('id', '')}</span>
</div>

<strong class="commentary">{meta.get('kind', 'Commentary')}</strong>
<div class="artmeta">
  <span>{meta.get('domain', '')}</span><span class="sep">|</span>
  <span class="id">{meta.get('id', '')}</span>
</div>

<h1 class="arttitle">{inline(meta.get('title', ''))}</h1>

<p class="affil">{meta.get('affil', 'Editorial appraisal published by '
  '<strong style="color:var(--ink)">evidencegap.vet</strong>')}<br>
Correspondence: <a href="mailto:contact@evidencegap.vet">contact@evidencegap.vet</a></p>

{abstract}
{kw}
{summary}
{out}
{related}
</div>
</div>
'''
