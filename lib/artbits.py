def findings(rows, label='Summary'):
    """A journal-style summary-of-findings block: labelled statements, not soundbites."""
    body = ''.join(f'<div class="frow"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows)
    return (f'<div class="findings"><p class="flab">{label}</p>'
            f'<dl>{body}</dl></div>')
