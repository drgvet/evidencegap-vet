"""Reads the record files in content/ — the gap map and the human-evidence page.

A record file looks like this:

    # lines starting with a hash are notes to yourself, ignored

    == Myxomatous mitral valve disease (dogs)      a group heading

    question: Pimobendan in preclinical stage B2 disease
    species: dog
    stage: pre
    certainty: moderate
    direction: benefit
    basis: 1 randomised trial, 360 dogs, placebo-controlled
    sources: EPIC, 2016 · [full appraisal](review-pimobendan-b2.html)
    verdict:
      EPIC, the single trial of pimobendan in preclinical stage B2
      disease, supports delaying heart failure in dogs meeting its
      entry criteria.

    ---                                            ends one record

A field runs until the next `key:` line, so long fields like `verdict`
can be written over as many lines as you like.
"""

import re

BOOLS = {'yes': True, 'no': False, 'true': True, 'false': False}


def dashes(t):
    """--- and -- written in a record become real dashes."""
    return t.replace('---', '&mdash;').replace('--', '&ndash;')


def _links(t):
    """[text](page.html) -> a real link. Plain HTML is left alone."""
    return re.sub(r'\[([^\]]+)\]\((\S+?)\)', r'<a href="\2">\1</a>', t)


def parse(path):
    """Return [(group name, [record dict, ...]), ...]"""
    groups, cur_group, cur_rec, key = [], None, {}, None

    def close_record():
        nonlocal cur_rec, key
        if cur_rec and cur_group is not None:
            for k, v in list(cur_rec.items()):
                v = v.strip()
                cur_rec[k] = BOOLS.get(v.lower(), _links(v)) if v else v
            cur_group[1].append(cur_rec)
        cur_rec, key = {}, None

    for raw in open(path, encoding='utf-8'):
        line = raw.rstrip('\n')
        s = line.strip()

        if s.startswith('#'):
            continue
        if s.startswith('== '):
            close_record()
            cur_group = (s[3:].strip(), [])
            groups.append(cur_group)
            continue
        if s == '---':
            close_record()
            continue

        # a field name must sit at the left margin; continuation lines are
        # indented, so ordinary prose beginning "word:" is never swallowed
        m = re.match(r'^([a-z_]+):\s*(.*)$', line) if line[:1] not in ' \t' else None
        if m:
            key = m.group(1)
            cur_rec[key] = m.group(2)
            continue
        if key and s:
            cur_rec[key] = (cur_rec[key] + ' ' + s).strip()

    close_record()
    return [g for g in groups if g[1]]


def as_questions(path):
    """Shape the gap-map records the way the page builder expects."""
    out = []
    for name, recs in parse(path):
        items = []
        for r in recs:
            items.append(dict(
                t=r.get('question', ''),
                sp=r.get('species', ''),
                stage=r.get('stage', 'pre'),
                conf=r.get('certainty', 'none'),
                dirn=r.get('direction', 'unclear'),
                basis=r.get('basis', ''),
                src=r.get('sources', ''),
                verdict=r.get('verdict', ''),
                tags=[t.strip() for t in r.get('limitations', '').split('·') if t.strip()],
                qual=r.get('qualifier', ''),
                surrogate=r.get('surrogate', False),
                more=r.get('appraisal', '') or None,
                soon=r.get('appraisal_in_preparation', False),
            ))
        out.append((name, items))
    return out


def as_classes(path):
    """Shape the human-evidence records the way that page builder expects."""
    import content as _c
    out, refs = [], []
    for name, recs in parse(path):
        if name.lower() == 'references':
            continue
        for r in recs:
            out.append((
                r.get('key', ''), dashes(name), r.get('analogy', 'partial'),
                _c.blocks(r.get('trials', '').split('\n')),
                _c.blocks(r.get('transfer', '').split('\n')),
                [dashes(b.strip()) for b in r.get('bears_on', '').split('·')
                 if b.strip()],
            ))
    for line in open(path, encoding='utf-8'):
        t = line.strip()
        if t.startswith('- '):
            refs.append(_c.inline(t[2:]))
    return out, refs


def as_steps(path):
    """Shape the teaching-page questions the way that page builder expects."""
    import content as _c
    out = []
    for name, recs in parse(path):
        for r in recs:
            out.append((dashes(name),
                        _c.blocks(r.get('body', '').split('\n')),
                        _c.inline(r.get('warning', ''))))
    return out
