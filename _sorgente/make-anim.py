# Crea le versioni animate (SVG) del profilo GitHub, chiare e scure.
# Uso: python3 _sorgente/make-anim.py
#
# GitHub mostra le immagini del README come <img>: niente JavaScript, solo animazioni SMIL e CSS dentro l'SVG.
# Il logo è il tracciato originale (logo-paths.txt). Il testo usa Inter Tight se installato, altrimenti il
# sans-serif di sistema: il carattere non è incorporato nel file.
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / '_sorgente'
OUT = ROOT / 'profile' / 'assets'
LOGO = (SRC / 'logo-paths.txt').read_text()
FONT = "'Inter Tight','Inter','Helvetica Neue',Helvetica,Arial,sans-serif"
THEMES = {
    'light': dict(bg='#F8F8F8', ink='#0C0C0C', soft='#6B6B6B', line='#D9D9D9', card='#FFFFFF', acc='#EAF0C2', accInk='#0C0C0C', dim='#BDBDBD'),
    'dark':  dict(bg='#0C0C0C', ink='#F8F8F8', soft='#9A9A9A', line='#2A2A2A', card='#141414', acc='#EAF0C2', accInk='#0C0C0C', dim='#3A3A3A'),
}
REDUCE = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
ESC = lambda s: s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def logo_paths():
    # ogni tracciato si disegna e poi si riempie, uno dopo l'altro; il punto (l'ultimo) pulsa
    paths = re.findall(r'<path[^>]*?\sd="([^"]+)"[^>]*?\stransform="([^"]+)"', LOGO)
    out = []
    for i, (d, tr) in enumerate(paths):
        dot = i == len(paths) - 1
        cls = 'lp dot' if dot else 'lp'
        # il punto pulsa con una trasformazione CSS, che sostituirebbe quella del tracciato: la sua resta sul gruppo
        out.append(f'<g transform="{tr}"><path class="{cls}" style="--i:{i}" pathLength="1" d="{d}"/></g>')
    return ''.join(out)


def banner(t):
    W, H = 1280, 400
    s = 560 / 1272
    nav = ['( longevità )', '( performance )', '( biohacking )', '( dev )']
    # pillole: l'accento passa da una all'altra e si ferma su ( dev )
    xs, x = [], W - 56
    widths = [len(n) * 7.6 + 28 for n in nav]
    for w in reversed(widths): x -= w; xs.insert(0, x); x -= 10
    pills = []
    n = len(nav)
    for i, (lab, px, w) in enumerate(zip(nav, xs, widths)):
        # ciclo di 8 s: ogni pillola accesa per 2 s
        on = f'<animate attributeName="fill-opacity" values="0;0;1;1;0;0" keyTimes="0;{i / n:.3f};{i / n + .01:.3f};{(i + 1) / n - .01:.3f};{(i + 1) / n:.3f};1" dur="8s" repeatCount="indefinite"/>'
        pills.append(f'<g><rect x="{px:.0f}" y="31" width="{w:.0f}" height="28" rx="14" fill="{t["acc"]}" fill-opacity="0">{on}</rect>'
                     f'<text x="{px + w / 2:.0f}" y="50" text-anchor="middle" font-size="13.5" fill="{t["ink"]}"><animate attributeName="fill" values="{t["ink"]};{t["ink"]};{t["accInk"]};{t["accInk"]};{t["ink"]};{t["ink"]}" keyTimes="0;{i / n:.3f};{i / n + .01:.3f};{(i + 1) / n - .01:.3f};{(i + 1) / n:.3f};1" dur="8s" repeatCount="indefinite"/>{ESC(lab)}</text></g>')
    claim = [("Tecnologia", t['ink'], 400), ("al servizio del", t['soft'], 300), ("metodo.", t['ink'], 400)]
    claim_svg = ''.join(f'<text class="cl" style="--i:{i}" x="{W - 496}" y="{150 + i * 41}" font-size="38" font-weight="{fw}" letter-spacing="-1.1" fill="{c}">{ESC(w)}</text>' for i, (w, c, fw) in enumerate(claim))
    ticker = ['Strumenti interni del team GS LOFT:', 'dashboard, automazioni e integrazioni.']
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="GS·LOFT — Coaching per longevità e performance. Tecnologia al servizio del metodo.">
<title>GS·LOFT — Tecnologia al servizio del metodo</title>
<style>
text{{font-family:{FONT};white-space:pre}}
.lp{{fill:{t["ink"]};fill-opacity:0;stroke:{t["ink"]};stroke-width:2.2;stroke-dasharray:1;stroke-dashoffset:1;
  animation:draw 1.3s cubic-bezier(.6,0,.2,1) forwards, fill .7s ease forwards;animation-delay:calc(var(--i)*.14s + .2s),calc(var(--i)*.14s + 1.1s)}}
.dot{{transform-box:fill-box;transform-origin:center;animation:draw 1s ease forwards,fill .5s ease forwards,beat 2.4s ease-in-out 2.6s infinite;animation-delay:1.3s,1.9s,2.6s}}
@keyframes draw{{to{{stroke-dashoffset:0}}}} @keyframes fill{{to{{fill-opacity:1;stroke-width:0}}}}
@keyframes beat{{0%,100%{{transform:scale(1)}}15%{{transform:scale(1.5)}}30%{{transform:scale(1)}}}}
.cl{{opacity:0;animation:up .8s cubic-bezier(.2,.8,.2,1) forwards;animation-delay:calc(var(--i)*.22s + 1.4s)}}
.sub,.num,.bot{{opacity:0;animation:up .8s ease forwards}} .sub{{animation-delay:2s}} .num{{animation-delay:2.4s}} .bot{{animation-delay:2.7s}}
@keyframes up{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
.sweep{{animation:sw 6s ease-in-out 3s infinite}} @keyframes sw{{0%{{transform:translateX(-200px)}}45%,100%{{transform:translateX(1500px)}}}}
.rule{{stroke-dasharray:1168;stroke-dashoffset:1168;animation:rl 1.4s ease forwards 2.6s}} @keyframes rl{{to{{stroke-dashoffset:0}}}}
{REDUCE}
</style>
<defs><linearGradient id="sg" x1="0" x2="1"><stop offset="0" stop-color="{t["acc"]}" stop-opacity="0"/><stop offset=".5" stop-color="{t["acc"]}" stop-opacity=".22"/><stop offset="1" stop-color="{t["acc"]}" stop-opacity="0"/></linearGradient></defs>
<rect width="{W}" height="{H}" fill="{t["bg"]}"/>
<rect class="sweep" x="0" y="0" width="160" height="{H}" fill="url(#sg)"/>
<text x="56" y="50" font-size="14" fill="{t["ink"]}"><tspan fill="{t["soft"]}" font-weight="300">(</tspan> GS-Loft-Dev <tspan fill="{t["soft"]}" font-weight="300">)</tspan></text>
{"".join(pills)}
<g transform="translate(56 118) scale({s:.5f})">{logo_paths()}</g>
<text class="sub" x="58" y="276" font-size="25" font-weight="300" letter-spacing="-.25" fill="{t["soft"]}">Coaching per longevità e performance</text>
{claim_svg}
<text class="num" x="{W - 496}" y="276" font-size="14" fill="{t["soft"]}"><tspan>(01)  {ESC(ticker[0])}</tspan><tspan x="{W - 496}" dy="21">{ESC(ticker[1])}</tspan></text>
<path class="rule" d="M56 339.5H{W - 56}" stroke="{t["line"]}"/>
<g class="bot" font-size="14" fill="{t["soft"]}"><text x="56" y="370">gsloft.it</text><text x="{W / 2}" y="370" text-anchor="middle">Desenzano del Garda  ·  Milano</text><text x="{W - 56}" y="370" text-anchor="end">( dal 2019 )</text></g>
</svg>'''


def metodo(t):
    W, H = 1280, 300
    pillars = ['Prevenzione e test di precisione', 'Allenamento', 'Nutrizione', 'Nutraceutica', 'Mindset e gestione dello stress', 'Ottimizzazione del sonno', 'Gestione del tempo']
    n = len(pillars)
    gap, x0 = 10, 56
    cw = (W - 2 * x0 - gap * (n - 1)) / n
    T = 10.5  # un giro: le sette carte si accendono in fila, poi tutte insieme
    cards = []
    for i, p in enumerate(pillars):
        x = x0 + i * (cw + gap)
        a, b = (.4 + i * .8) / T, (.4 + (i + 1) * .8) / T
        hi = f'<animate attributeName="fill" values="{t["card"]};{t["card"]};{t["acc"]};{t["card"]};{t["card"]};{t["acc"]};{t["acc"]};{t["card"]}" keyTimes="0;{a:.4f};{a + .01:.4f};{b:.4f};.85;.86;.97;1" dur="{T}s" repeatCount="indefinite"/>'
        ink = f'<animate attributeName="fill" values="{t["ink"]};{t["ink"]};{t["accInk"]};{t["ink"]};{t["ink"]};{t["accInk"]};{t["accInk"]};{t["ink"]}" keyTimes="0;{a:.4f};{a + .01:.4f};{b:.4f};.85;.86;.97;1" dur="{T}s" repeatCount="indefinite"/>'
        words, lines, cur = p.split(), [], ''
        for w in words:
            if len(cur) + len(w) + 1 > 15 and cur: lines.append(cur); cur = w
            else: cur = (cur + ' ' + w).strip()
        lines.append(cur)
        txt = ''.join(f'<tspan x="{x + 16:.0f}" dy="{0 if k == 0 else 19}">{ESC(l)}</tspan>' for k, l in enumerate(lines))
        cards.append(f'''<g class="cd" style="--i:{i}"><rect x="{x:.0f}" y="96" width="{cw:.0f}" height="150" rx="14" fill="{t["card"]}" stroke="{t["line"]}">{hi}</rect>
<text x="{x + 16:.0f}" y="128" font-size="13" font-weight="500" fill="{t["soft"]}">( 0{i + 1} )</text>
<text x="{x + 16:.0f}" y="196" font-size="16" letter-spacing="-.2" fill="{t["ink"]}">{ink}{txt}</text></g>''')
    # filo che collega le carte, con il punto che lo percorre
    path = f"M{x0 + cw / 2:.0f} 266 H{x0 + (n - 1) * (cw + gap) + cw / 2:.0f}"
    dots = ''.join(f'<circle cx="{x0 + i * (cw + gap) + cw / 2:.0f}" cy="266" r="4" fill="{t["bg"]}" stroke="{t["ink"]}"/>' for i in range(n))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Il metodo GS LOFT: sette pilastri, un solo percorso. {", ".join(pillars)}.">
<style>text{{font-family:{FONT};white-space:pre}} .cd{{opacity:0;animation:up .7s cubic-bezier(.2,.8,.2,1) forwards;animation-delay:calc(var(--i)*.1s + .1s)}}
@keyframes up{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}} {REDUCE}</style>
<rect width="{W}" height="{H}" fill="{t["bg"]}"/>
<text x="56" y="52" font-size="30" letter-spacing="-.8" fill="{t["ink"]}">Sette pilastri, <tspan fill="{t["soft"]}" font-weight="300">un solo percorso.</tspan></text>
<text x="{W - 56}" y="52" font-size="14" text-anchor="end" fill="{t["soft"]}">( il metodo )</text>
{"".join(cards)}
<path d="{path}" stroke="{t["line"]}" stroke-dasharray="3 5"/>{dots}
<circle r="6" fill="{t["acc"]}" stroke="{t["ink"]}"><animateMotion path="{path}" dur="{T * .8:.1f}s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;.85;1" calcMode="linear"/></circle>
</svg>'''


def dev(t):
    W, H = 1280, 420
    sources = ['HubSpot', 'Google Fogli', 'Lovable', 'Database interni']
    outs = [('Dashboard', 'dash-previntegratori · Portale-Sales'), ('Automazioni', 'GS-Bot-Discord · lovableTOhubspot · BIO_Profilo'),
            ('AI', 'assistenteLOFT · gs-mind-memoria'), ('Strumenti', 'Lovable-TO-Hub_WEBAPP · PortaleQuiz'), ('Dati', 'data_management_project')]
    cx, cy = 470, 236
    src, wires, pk = [], [], []
    for i, s in enumerate(sources):
        y = 110 + i * 64
        src.append(f'<g class="in" style="--i:{i}"><rect x="56" y="{y - 20}" width="190" height="40" rx="20" fill="{t["card"]}" stroke="{t["line"]}"/><text x="151" y="{y + 5}" text-anchor="middle" font-size="15" fill="{t["ink"]}">{ESC(s)}</text></g>')
        d = f"M246 {y} C340 {y}, 360 {cy}, {cx - 62} {cy}"
        wires.append(f'<path d="{d}" fill="none" stroke="{t["dim"]}" stroke-dasharray="3 5"><animate attributeName="stroke-dashoffset" from="0" to="-16" dur="1.2s" repeatCount="indefinite"/></path>')
        pk.append(f'<circle r="4" fill="{t["ink"]}"><animateMotion path="{d}" dur="{2.2 + i * .35:.2f}s" begin="{i * .5:.1f}s" repeatCount="indefinite"/></circle>')
    o = []
    for i, (k, v) in enumerate(outs):
        y = 92 + i * 66
        d = f"M{cx + 62} {cy} C{cx + 160} {cy}, {cx + 170} {y}, 742 {y}"
        wires.append(f'<path d="{d}" fill="none" stroke="{t["dim"]}" stroke-dasharray="3 5"><animate attributeName="stroke-dashoffset" from="0" to="-16" dur="1.2s" repeatCount="indefinite"/></path>')
        pk.append(f'<rect x="-5" y="-5" width="10" height="10" rx="3" fill="{t["acc"]}" stroke="{t["ink"]}" stroke-width=".8"><animateMotion path="{d}" dur="{2 + i * .3:.2f}s" begin="{.8 + i * .4:.1f}s" repeatCount="indefinite"/></rect>')
        o.append(f'''<g class="out" style="--i:{i}"><rect x="742" y="{y - 26}" width="482" height="52" rx="14" fill="{t["card"]}" stroke="{t["line"]}">
<animate attributeName="stroke" values="{t["line"]};{t["ink"]};{t["line"]}" dur="1.2s" begin="{2.6 + i * .4:.1f}s;{6.6 + i * .4:.1f}s;{10.6 + i * .4:.1f}s" fill="remove"/></rect>
<text x="762" y="{y - 3}" font-size="15" font-weight="500" fill="{t["ink"]}">{ESC(k)}</text><text x="762" y="{y + 16}" font-size="12.5" fill="{t["soft"]}">{ESC(v)}</text></g>''')
    hub = f'''<g><circle cx="{cx}" cy="{cy}" r="62" fill="{t["ink"]}"/>
<circle cx="{cx}" cy="{cy}" r="62" fill="none" stroke="{t["ink"]}"><animate attributeName="r" values="62;100" dur="2.6s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".45;0" dur="2.6s" repeatCount="indefinite"/></circle>
<text x="{cx}" y="{cy - 4}" text-anchor="middle" font-size="16" font-weight="500" fill="{t["bg"]}">( dev )</text>
<text x="{cx}" y="{cy + 17}" text-anchor="middle" font-size="12" fill="{t["soft"]}">GS-Loft-Dev</text></g>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Come lavora il team dev: i dati di HubSpot, Google Fogli, Lovable e dei database interni passano dagli strumenti di GS-Loft-Dev e diventano dashboard, automazioni, AI, strumenti e dati centralizzati.">
<style>text{{font-family:{FONT};white-space:pre}} .in,.out{{opacity:0;animation:up .6s cubic-bezier(.2,.8,.2,1) forwards}} .in{{animation-delay:calc(var(--i)*.12s + .2s)}} .out{{animation-delay:calc(var(--i)*.12s + .8s)}}
@keyframes up{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}} {REDUCE}</style>
<rect width="{W}" height="{H}" fill="{t["bg"]}"/>
<text x="56" y="48" font-size="14" fill="{t["soft"]}">( dati )</text><text x="{cx}" y="48" font-size="14" text-anchor="middle" fill="{t["soft"]}">( strumenti interni )</text><text x="742" y="48" font-size="14" fill="{t["soft"]}">( per il team )</text>
{"".join(wires)}{"".join(src)}{"".join(o)}{hub}{"".join(pk)}
</svg>'''


OUT.mkdir(parents=True, exist_ok=True)
for name, fn in [('banner', banner), ('metodo', metodo), ('dev', dev)]:
    for theme, t in THEMES.items():
        p = OUT / f'{name}-{theme}.svg'
        p.write_text(fn(t))
        print('scritto', p.relative_to(ROOT), p.stat().st_size // 1024, 'KB')
