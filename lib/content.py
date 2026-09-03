"""
Reads the plain-text files in content/ and turns them into HTML fragments.

Nothing here needs an installed package. The format is deliberately small:

    key: value            at the top of the file, one per line, until a blank line
    == 1. Section title   a numbered section
    === 3.1 Subsection    a subsection
    == references         a section whose name has a special meaning
    :Label                a run-in label inside the abstract
    Text :: value         a row in the summary block
    | a | b |             a table row
    - item                a list item

Inside a paragraph:

    *italic*  **bold**  [3] or [3,4] for a citation  "quotes" become curly
    -- en dash, --- em dash, <a href=...> and other raw HTML pass through

Everything else is an ordinary paragraph. Blank lines separate paragraphs.
"""

import re

# ---------------------------------------------------------------- inline text

_UNITS = r'(?:mm|cm|kg|mg|g|mL|L|U/L|pmol/L|ng/mL|mm\s?Hg|bpm|%|h|hr|hours|days|months|years)'


def inline(t):
    """Turn one run of text into HTML."""
    # protect anything already written as a tag or an entity
    keep = []

    def stash(m):
        keep.append(m.group(0))
        return f'\x00{len(keep) - 1}\x00'

    t = re.sub(r'<[^>]+>|&[a-zA-Z]+;|&#\d+;', stash, t)

    # dashes and quotes first, while the text still contains no generated tags
    t = t.replace('---', '&mdash;').replace('--', '&ndash;')
    t = re.sub(r'(^|[\s(\[])"', r'\1&ldquo;', t)
    t = t.replace('"', '&rdquo;')
    t = re.sub(r"(\w)'(\w)", r'\1&rsquo;\2', t)
    t = re.sub(r"(^|[\s(\[])'", r'\1&lsquo;', t)
    t = t.replace("'", '&rsquo;')

    # emphasis
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)', r'<em>\1</em>', t)

    # citations: [3] or [3,4] -> superscript links
    def cite(m):
        ns = [n.strip() for n in m.group(1).split(',')]
        links = ', '.join(f'<a href="#ref{n}">{n}</a>' for n in ns)
        return f'<sup class="cite">{links}</sup>'

    t = re.sub(r'\[(\d+(?:\s*,\s*\d+)*)\]', cite, t)

    # keep numbers with their units, and p-values, on one line
    t = re.sub(r'(\d)\s+(' + _UNITS + r')\b', r'\1&nbsp;\2', t)
    t = re.sub(r'\b([pP])\s*=\s*', r'\1&nbsp;=&nbsp;', t)
    t = re.sub(r'\bn\s*=\s*', 'n&nbsp;=&nbsp;', t)

    for i, k in enumerate(keep):
        t = t.replace(f'\x00{i}\x00', k)
    return t


# ------------------------------------------------------------------- blocks

def _table(rows):
    head, body = rows[0], rows[2:] if len(rows) > 2 else []
    th = ''.join(f'<th>{inline(c)}</th>' for c in head)
    trs = ''
    for r in body:
        tds = ''.join(
            f'<td class="n">{inline(c)}</td>' if re.match(r'^[\d.−+\-—\s]*$', c)
            and c.strip() not in ('', '—') or re.match(r'^[\d.]+$', c.strip())
            else f'<td>{inline(c)}</td>'
            for c in r)
        trs += f'<tr>{tds}</tr>'
    return (f'<div class="tscroll"><table><thead><tr>{th}</tr></thead>'
            f'<tbody>{trs}</tbody></table></div>')


FIG_DIR = None  # set by build.py


def blocks(lines):
    """Turn a run of body lines into HTML."""
    out, buf, list_buf, tbl = [], [], [], []

    def flush_para():
        if buf:
            out.append(f'<p>{inline(" ".join(buf))}</p>')
            buf.clear()

    def flush_list():
        if list_buf:
            items = ''.join(f'<li>{inline(i)}</li>' for i in list_buf)
            out.append(f'<ul>{items}</ul>')
            list_buf.clear()

    def flush_table():
        if tbl:
            out.append(_table(tbl))
            tbl.clear()

    for raw in lines:
        line = raw.rstrip()
        s = line.strip()
        if not s:
            flush_para(); flush_list(); flush_table()
            continue
        if s.startswith('|'):
            flush_para(); flush_list()
            tbl.append([c.strip() for c in s.strip('|').split('|')])
            continue
        flush_table()
        if s.startswith('- '):
            flush_para()
            list_buf.append(s[2:])
            continue
        flush_list()
        m = re.match(r'^\[\[figure:\s*(.+?)\]\]$', s)
        if m and FIG_DIR:
            flush_para()
            out.append(open(f'{FIG_DIR}/{m.group(1)}', encoding='utf-8').read())
            continue
        if s.startswith('> '):           # a note, set smaller
            flush_para()
            out.append(f'<p class="note">{inline(s[2:])}</p>')
            continue
        buf.append(s)
    flush_para(); flush_list(); flush_table()
    return ''.join(out)


# -------------------------------------------------------------------- files

def read(path):
    """Parse one content file. Returns (meta dict, list of sections)."""
    text = open(path, encoding='utf-8').read().replace('\r\n', '\n')
    lines = text.split('\n')

    meta, i = {}, 0
    while i < len(lines) and lines[i].strip():
        if lines[i].lstrip().startswith('#'):
            i += 1
            continue
        k, _, v = lines[i].partition(':')
        meta[k.strip()] = v.strip()
        i += 1

    sections, cur = [], None
    for line in lines[i:]:
        s = line.strip()
        m = re.match(r'^(={2,3})\s+(.*)$', s)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            num = ''
            t = re.match(r'^(\d+(?:\.\d+)*)\.?\s+(.*)$', title)
            if t:
                num, title = t.group(1), t.group(2)
            cur = {'level': level, 'num': num, 'title': title, 'lines': []}
            sections.append(cur)
            continue
        if cur is None:
            continue
        cur['lines'].append(line)
    return meta, sections
