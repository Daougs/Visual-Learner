def table(pre, head, rows, show=None, cls=''):
    """rows: list of tuples of cell html. Each row gets id pre+i and class rv."""
    show = range(len(rows)) if show is None else show
    th = ''.join(f'<th>{h}</th>' for h in head)
    body = ''.join(
        f'<tr class="rv" id="{pre}{i}">' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>'
        for i, r in enumerate(rows) if i in show)
    return f'<table class="tbl {cls}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>'

def checks(pre, items, nxt):
    li = ''.join(f'<li class="rv" id="{pre}{i}"><span class="box"></span><span>{x}</span></li>' for i, x in enumerate(items))
    return f'<div class="eyebrow">Practice</div><ul class="checks">{li}</ul><p class="note rv" id="{pre}{len(items)}">{nxt}</p>'
