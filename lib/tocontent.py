"""One-off helper: turn an existing HTML fragment back into content-file text.

Used to migrate the prose out of the old Python generators. Not needed to build
the site; kept in the repo so the migration is reproducible.
"""

import re


def undo(h):
    """HTML fragment -> content-file text."""
    t = h

    # citations {c(1,2)} macro form and the rendered form
    t = re.sub(r'\{c\(([\d,\s]+)\)\}', lambda m: '[' + re.sub(r'\s+', '', m.group(1)) + ']', t)
    t = re.sub(r'<sup class="cite">(.*?)</sup>',
               lambda m: '[' + ','.join(re.findall(r'>(\d+)<', m.group(1))) + ']', t, flags=re.S)

    t = re.sub(r'<strong>(.*?)</strong>', r'**\1**', t, flags=re.S)
    t = re.sub(r'<b>(.*?)</b>', r'**\1**', t, flags=re.S)
    t = re.sub(r'<em>(.*?)</em>', r'*\1*', t, flags=re.S)

    # tables
    def table(m):
        rows = re.findall(r'<tr>(.*?)</tr>', m.group(0), flags=re.S)
        out = []
        for i, r in enumerate(rows):
            cells = [re.sub(r'<[^>]+>', '', c).strip()
                     for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, flags=re.S)]
            out.append('| ' + ' | '.join(cells) + ' |')
            if i == 0:
                out.append('|' + '---|' * len(cells))
        return '\n' + '\n'.join(out) + '\n'

    t = re.sub(r'<table>.*?</table>', table, t, flags=re.S)

    # paragraphs and notes
    t = re.sub(r'<p class="note"[^>]*>(.*?)</p>', r'\n\n> \1\n', t, flags=re.S)
    t = re.sub(r'</p>\s*<p[^>]*>', '\n\n', t, flags=re.S)
    t = re.sub(r'</?p[^>]*>', '\n\n', t)
    t = re.sub(r'<li>(.*?)</li>', r'\n- \1', t, flags=re.S)
    t = re.sub(r'</?(ul|ol|div|section|tbody|thead)[^>]*>', '\n', t)
    t = re.sub(r'<br\s*/?>', '\n', t)

    ent = {'&mdash;': '---', '&ndash;': '--', '&nbsp;': ' ', '&ldquo;': '"',
           '&rdquo;': '"', '&lsquo;': "'", '&rsquo;': "'", '&minus;': '−',
           '&hellip;': '…', '&amp;': '&', '&middot;': '·',
           '&plusmn;': '±', '&times;': '×', '&deg;': '°',
           '&eacute;': 'é', '&ouml;': 'ö', '&auml;': 'ä',
           '&aring;': 'å', '&ocirc;': 'ô', '&Ograve;': 'Ò',
           '&Agrave;': 'À'}
    for k, v in ent.items():
        t = t.replace(k, v)

    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r' *\n *', '\n', t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()
