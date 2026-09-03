"""Migration: read an old generator module and write its prose to a content file.

Run once per appraisal page. The generator modules build their HTML at import
time, so we exec each one in its own namespace and read the data structures back
out. Kept in the repo so the migration can be re-run or audited.
"""

import io
import re
import sys

sys.path.insert(0, '/root/repo/lib')
from tocontent import undo  # noqa: E402


def load(path, extra_dir='/root/build'):
    """Exec a generator module and return its namespace."""
    sys.path.insert(0, extra_dir)
    ns = {'__name__': '__migrate__', '__file__': path}
    code = io.open(path, encoding='utf-8').read()
    exec(compile(code, path, 'exec'), ns)
    return ns


def rail_meta(rail_html):
    """Pull the label/value rows out of the sidebar block."""
    meta = {}
    for k, v in re.findall(r'<p class="row"><span>(.*?)</span>(.*?)</p>', rail_html, re.S):
        meta[re.sub(r'<[^>]+>', '', k).strip().lower().replace(' ', '_')] = \
            re.sub(r'<[^>]+>', '', v).strip()
    m = re.search(r'<p class="type[^"]*">(.*?)</p>', rail_html)
    if m:
        meta['kind'] = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    m = re.search(r'<p class="id">(.*?)</p>', rail_html)
    if m:
        raw = re.sub(r'<[^>]+>', '', m.group(1)).replace('&middot;', '·')
        parts = [p.strip() for p in raw.split('·')]
        meta['id'] = parts[0]
        if len(parts) > 1:
            meta['domain'] = parts[1]
    return meta


def abstract_rows(body_html):
    """Pull the structured abstract out of the assembled page body."""
    m = re.search(r'<div class="abstract">(.*?)</div>', body_html, re.S)
    if not m:
        return []
    rows = []
    for lab, txt in re.findall(
            r'<p><span class="runin">(.*?)</span>(.*?)</p>', m.group(1), re.S):
        rows.append((lab.strip(), undo(txt)))
    return rows


def findings_rows(body_html):
    m = re.search(r'<div class="findings">.*?<dl>(.*?)</dl>', body_html, re.S)
    if not m:
        return []
    return [(re.sub(r'<[^>]+>', '', k).strip(), undo(v))
            for k, v in re.findall(r'<dt>(.*?)</dt><dd>(.*?)</dd>', m.group(1), re.S)]


SPECIAL = ('references', 'declarations')


def sections_from_body(body, figures, fig_dir, slug):
    """Walk the assembled page body and pull out every numbered section."""
    out = []
    for m in re.finditer(
            r'<section class="sec" id="s([\d.]+)">\s*<h2>(.*?)</h2>(.*?)</section>',
            body, re.S):
        num = m.group(1)
        ttl = re.sub(r'<span class="num">.*?</span>', '', m.group(2), flags=re.S)
        ttl = re.sub(r'<[^>]+>', '', ttl).strip()
        inner = m.group(3)
        subs = list(re.finditer(
            r'<div class="subsec" id="s([\d.]+)">\s*(?:<span class="gaptype">.*?</span>)?'
            r'\s*<h3>(.*?)</h3>(.*?)</div>\s*(?=<div class="subsec"|$)', inner, re.S))
        head = inner[:subs[0].start()] if subs else inner
        out.append((num, ttl, undo(stash_figures(head, figures, fig_dir, slug)), 2))
        for sm in subs:
            st = re.sub(r'<span class="num">.*?</span>', '', sm.group(2), flags=re.S)
            st = re.sub(r'<[^>]+>', '', st).strip()
            out.append((sm.group(1), st,
                        undo(stash_figures(sm.group(3), figures, fig_dir, slug)), 3))
    return out


def stash_figures(text, figures, fig_dir, slug):
    """Pull SVG figures out into their own files and leave a marker behind."""
    def keep(m):
        figures.append(m.group(0))
        name = f'{slug}-fig{len(figures)}.html'
        io.open(f'{fig_dir}/{name}', 'w', encoding='utf-8').write(m.group(0))
        return f'\n\n[[figure: {name}]]\n\n'
    text = re.sub(r'<figure.*?</figure>', keep, text, flags=re.S)
    text = re.sub(r'<svg.*?</svg>', keep, text, flags=re.S)
    return text


def write_appraisal(out_path, ns, extra_sections=()):
    """Write one appraisal's content file."""
    import os
    meta = rail_meta(ns.get('RAIL', ''))
    body = ns.get('body', '')
    slug = os.path.basename(out_path).rsplit('.', 1)[0]
    fig_dir = os.path.join(os.path.dirname(out_path), 'figures')
    os.makedirs(fig_dir, exist_ok=True)
    figures = []

    L = []
    title = re.search(r'<h1 class="arttitle">(.*?)</h1>', body, re.S)
    L.append(f"title: {undo(title.group(1)) if title else ''}")
    for k in ('id', 'kind', 'domain', 'first_published', 'published',
              'last_revised', 'certainty', 'endpoint', 'direction',
              'controlled_trials', 'method'):
        if k in meta:
            L.append(f"{k}: {meta[k]}")
    L.append('')

    ab = abstract_rows(body)
    if ab:
        L.append('== abstract')
        for lab, txt in ab:
            L.append(f':{lab}')
            L.append(txt)
            L.append('')

    fr = findings_rows(body)
    if fr:
        L.append('== summary')
        for lab, txt in fr:
            L.append(f'{lab} :: {txt}')
        L.append('')

    for num, ttl, html, level in sections_from_body(body, figures, fig_dir, slug):
        mark = '==' if level == 2 else '==='
        L.append(f'{mark} {num}. {ttl}' if level == 2 else f'{mark} {num} {ttl}')
        L.append(html)
        L.append('')

    m = re.search(r'<p class="note"[^>]*>Related:(.*?)</p>', body, re.S)
    if m:
        L.insert(1, 'related: ' + m.group(1).strip())
    m = re.search(r'<div class="runhead">\s*<span>.*?</span>\s*<span>(.*?)</span>', body, re.S)
    if m:
        L.insert(1, 'short_title: ' + re.sub(r'<[^>]+>', '', m.group(1)).strip())

    m = re.search(r'<p class="keywords">.*?</b>(.*?)</p>', body, re.S)
    if m:
        L.insert(len([x for x in L if x and not x.startswith(('==', ':', '-'))]) * 0 + 1,
                 'keywords: ' + undo(m.group(1)).replace(' · ', ', ').replace('·', ',').strip())

    m = re.search(r'<div class="declare">\s*<dl>(.*?)</dl>', body, re.S)
    if m:
        L.append('== declarations')
        for k, v in re.findall(r'<dt>(.*?)</dt>\s*<dd>(.*?)</dd>', m.group(1), re.S):
            L.append(f'{re.sub(r"<[^>]+>", "", k).strip()} :: {undo(v)}')
        L.append('')

    m = re.search(r'<div class="citeas">.*?<p>(.*?)</p>', body, re.S)
    if m:
        L.append('== cite as')
        L.append(undo(m.group(1)))
        L.append('')

    refs = ns.get('REFS', [])
    if refs:
        L.append('== references')
        for i, r in enumerate(refs, 1):
            L.append(f'{i}. {undo(r)}')
        L.append('')

    io.open(out_path, 'w', encoding='utf-8').write('\n'.join(L).rstrip() + '\n')
    return out_path
