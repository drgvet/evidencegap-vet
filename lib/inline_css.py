"""Fold assets/site.css into every built page, so each page stands alone."""

import glob
import os
import re

LINK = '<link rel="stylesheet" href="assets/site.css">'


def run(out_dir, css_path):
    css = open(css_path, encoding='utf-8').read()
    mini = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    mini = re.sub(r'\n\s+', '\n', mini)
    mini = re.sub(r'\n{2,}', '\n', mini).strip()
    block = '<style>\n' + mini + '\n</style>'

    n = 0
    for f in sorted(glob.glob(os.path.join(out_dir, '*.html'))):
        s = open(f, encoding='utf-8').read()
        if LINK not in s:
            continue
        open(f, 'w', encoding='utf-8').write(s.replace(LINK, block, 1))
        n += 1
    return n
