#!/usr/bin/env python3
"""
Build evidencegap.vet.

    python3 build.py

Reads the text files in content/, wraps them in the site shell, inlines
assets/site.css into every page, and writes the finished HTML into _site/.
No installed packages are needed: plain Python 3 only.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'lib'))

import shell            # noqa: E402
import pages            # noqa: E402
import inline_css       # noqa: E402
import content          # noqa: E402

content.FIG_DIR = os.path.join(HERE, 'content', 'figures')

OUT = os.path.join(HERE, '_site')
CONTENT = os.path.join(HERE, 'content')

# Appraisals: one content file each, rendered with the appraisal template.
APPRAISALS = [
    ('review-rapamycin',      'Rapamycin for subclinical feline hypertrophic cardiomyopathy',
     'A critical appraisal of RAPACAT, the 43-cat trial supporting conditional '
     'approval of Felycin-CA1 for feline hypertrophic cardiomyopathy.'),
    ('review-steroids-chf',   "Steroids and heart failure in cats: science, or an old wives' tale?",
     'The belief that steroids cause heart failure in cats, and what the '
     'published evidence actually shows.'),
    ('review-pimobendan-b2',  'Pimobendan in preclinical stage B2 mitral valve disease',
     'A re-analysis of the EPIC trial from reconstructed event times, read '
     'alongside the regulatory record.'),
]


def main():
    os.makedirs(OUT, exist_ok=True)

    built = []
    for slug, title, desc in APPRAISALS:
        src = os.path.join(CONTENT, slug + '.txt')
        if not os.path.exists(src):
            print(f'  skip {slug}: no content file')
            continue
        body = pages.appraisal(src)
        html = shell.page(slug + '.html', f'{title} &mdash; evidencegap.vet',
                          desc, body, width='wide')
        open(os.path.join(OUT, slug + '.html'), 'w', encoding='utf-8').write(html)
        built.append(slug + '.html')
        print(f'  built {slug}.html')

    # pages whose prose has not been migrated yet still build from legacy/
    legacy = os.path.join(HERE, 'legacy')
    if os.path.isdir(legacy):
        cwd = os.getcwd()
        os.chdir(OUT)
        sys.path.insert(0, legacy)
        for mod in ('p_home', 'p_gapmap', 'p_topics', 'p_human', 'p_reviews2',
                    'p_teaching', 'p_pages'):
            src = os.path.join(legacy, mod + '.py')
            if not os.path.exists(src):
                continue
            ns = {'__name__': '__legacy__', '__file__': src}
            try:
                exec(compile(open(src, encoding='utf-8').read(), src, 'exec'), ns)
                print(f'  built (legacy) {mod}')
            except Exception as e:
                print(f'  FAILED {mod}: {e}')
        os.chdir(cwd)

    # static files copied through unchanged
    for name in ('robots.txt', 'sitemap.xml', 'favicon.svg'):
        p = os.path.join(HERE, name)
        if os.path.exists(p):
            shutil.copy(p, os.path.join(OUT, name))

    assets_out = os.path.join(OUT, 'assets')
    os.makedirs(assets_out, exist_ok=True)
    shutil.copy(os.path.join(HERE, 'assets', 'site.css'),
                os.path.join(assets_out, 'site.css'))

    n = inline_css.run(OUT, os.path.join(HERE, 'assets', 'site.css'))
    print(f'  inlined the stylesheet into {n} pages')
    print(f'\nDone. {len(built)} pages in _site/')


if __name__ == '__main__':
    main()
