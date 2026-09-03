import math
from statistics import NormalDist

SWEEP = [(0,162,0.630,'0.46&ndash;0.86',0.0039),(8,158,0.639,'0.46&ndash;0.88',0.0056),
         (16,150,0.640,'0.46&ndash;0.89',0.0072),(23,134,0.709,'0.50&ndash;1.00',0.0501),
         (26,124,0.715,'0.50&ndash;1.03',0.0664),(39,111,0.732,'0.50&ndash;1.07',0.1061),
         (52,91,0.765,'0.50&ndash;1.17',0.2109)]
_nd = NormalDist()
def expected_p(d, hr=0.630):
    """Two-sided log-rank P if the hazard ratio never changed, from the events left.
       SE(log HR) = 2/sqrt(events) under balanced allocation."""
    return 2 * _nd.cdf(math.log(hr) / (2 / math.sqrt(d)))

OBS, EXP = '#A63F00', '#1F6FA8'          # validated on the cream surface
INK, MUT, FAINT, RULE = '#1A1D21', '#5F5852', '#8B8279', '#D9CBAE'

def figure():
    W,H = 780,360
    L,R,T,B = 52,116,26,52
    px, py = W-L-R, H-T-B
    ymin, ymax = math.log(0.002), math.log(0.40)
    def X(w): return L + px*w/52
    def Y(p): return T + py*(math.log(p)-ymax)/(ymin-ymax)

    s = [f'<svg viewBox="0 0 {W} {H}" class="fig" role="img" '
         f'aria-label="Observed log-rank P against the P expected under a constant hazard ratio, '
         f'as more of the early period is removed">']
    # y grid
    for p,lab in [(0.002,'0.002'),(0.005,'0.005'),(0.01,'0.01'),(0.02,'0.02'),
                  (0.05,'0.05'),(0.10,'0.10'),(0.20,'0.20'),(0.40,'0.40')]:
        y=Y(p)
        s.append(f'<line x1="{L}" y1="{y:.1f}" x2="{L+px}" y2="{y:.1f}" '
                 f'stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{L-9}" y="{y+4:.1f}" text-anchor="end" class="ax">{lab}</text>')
    # the 0.05 line, emphasised
    y5=Y(0.05)
    s.append(f'<line x1="{L}" y1="{y5:.1f}" x2="{L+px}" y2="{y5:.1f}" stroke="{INK}" '
             f'stroke-width="1.4" stroke-dasharray="5 4" opacity=".55"/>')
    s.append(f'<text x="{L+px-6}" y="{y5-9:.1f}" text-anchor="end" class="ax em">P = 0.05</text>')
    # x axis
    s.append(f'<line x1="{L}" y1="{T+py}" x2="{L+px}" y2="{T+py}" stroke="{INK}" stroke-width="1.2"/>')
    for w in [0,8,16,23,26,39,52]:
        s.append(f'<text x="{X(w):.1f}" y="{T+py+19}" text-anchor="middle" class="ax">{w}</text>')
    s.append(f'<text x="{L+px/2:.1f}" y="{H-9}" text-anchor="middle" class="ax lab">'
             f'Weeks of follow-up removed from both arms</text>')
    s.append(f'<text transform="translate(13,{T+py/2:.1f}) rotate(-90)" text-anchor="middle" '
             f'class="ax lab">Log-rank P</text>')

    for key,colour,dash in (('exp',EXP,'6 4'),('obs',OBS,'')):
        pts=[]
        for w,d,hr,ci,p in SWEEP:
            v = expected_p(d) if key=='exp' else p
            pts.append((X(w),Y(v),w,d,v))
        path=' '.join(f'{"M" if i==0 else "L"}{x:.1f},{y:.1f}' for i,(x,y,_,_,_) in enumerate(pts))
        da=f' stroke-dasharray="{dash}"' if dash else ''
        s.append(f'<path d="{path}" fill="none" stroke="{colour}" stroke-width="2"'
                 f' stroke-linejoin="round"{da}/>')
        for x,y,w,d,v in pts:
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{colour}" '
                     f'stroke="#FDF6E4" stroke-width="2"><title>{w} weeks removed, '
                     f'{d} events: P = {v:.4f}</title></circle>')
        lx,ly,_,_,_ = pts[-1]
        txt = ('Expected<tspan x="%d" dy="15">if constant</tspan>' % (lx+12)
               if key=='exp' else 'Observed')
        s.append(f'<text x="{lx+12:.1f}" y="{ly+4:.1f}" class="ax key" fill="{colour}">{txt}</text>')
    s.append('</svg>')
    return ''.join(s)

FIGCSS = """
.figwrap{margin:26px 0 8px}
.fig{width:100%;height:auto;display:block}
.fig .ax{font-family:var(--sans);font-size:11.5px;fill:#5F5852}
.fig .ax.lab{font-size:11px;letter-spacing:.09em;text-transform:uppercase;fill:#8B8279}
.fig .ax.em{font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;fill:#1A1D21}
.fig .ax.key{font-size:12px;font-weight:600}
figcaption{font-family:var(--sans);font-size:13px;line-height:1.6;color:#5F5852;
  margin-top:12px;padding-top:11px;border-top:1px solid var(--rule)}
figcaption b{color:var(--ink)}
@media (max-width:620px){.fig .ax.key{font-size:11px}}
"""
