# Crea i banner del profilo GitHub (chiaro e scuro) da banner.html con Chrome headless.
# Uso: python3 _sorgente/make-banner.py
import os, subprocess, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / '_sorgente'
OUT = ROOT / 'profile' / 'assets'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
LOGO = (SRC / 'logo-paths.txt').read_text()

THEMES = {
    'light': dict(bg='#F8F8F8', ink='#0C0C0C', soft='#6B6B6B', line='#D9D9D9', acc='#EAF0C2', accInk='#0C0C0C'),
    'dark':  dict(bg='#0C0C0C', ink='#F8F8F8', soft='#9A9A9A', line='#2A2A2A', acc='#EAF0C2', accInk='#0C0C0C'),
}

def html(t):
    return f'''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@300;400;500&display=block" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1280px;height:400px;background:{t['bg']};color:{t['ink']};font-family:'Inter Tight',Arial,sans-serif;-webkit-font-smoothing:antialiased;overflow:hidden}}
.b{{position:relative;width:1280px;height:400px;padding:34px 56px}}
.top,.bot{{position:absolute;left:56px;right:56px;display:flex;align-items:center;justify-content:space-between;font-size:14px;letter-spacing:.01em}}
.top{{top:34px}} .bot{{bottom:30px;padding-top:16px;border-top:1px solid {t['line']};color:{t['soft']}}}
.nav{{display:flex;align-items:center;gap:30px}}
.nav span{{white-space:nowrap}}
.tag{{display:inline-flex;align-items:center;height:28px;padding:0 14px;border-radius:99px;background:{t['acc']};color:{t['accInk']};font-weight:500;font-size:13.5px}}
.logo{{position:absolute;left:56px;top:118px;width:560px;height:auto;color:{t['ink']}}}
.sub{{position:absolute;left:58px;top:250px;font-size:25px;font-weight:300;letter-spacing:-.01em;color:{t['soft']}}}
.claim{{position:absolute;right:56px;top:112px;width:440px;font-size:38px;line-height:1.08;font-weight:400;letter-spacing:-.03em}}
.claim i{{font-style:normal;color:{t['soft']};font-weight:300}}
.num{{position:absolute;right:56px;top:262px;width:440px;font-size:14px;color:{t['soft']};line-height:1.5}}
.pp{{font-weight:300;color:{t['soft']}}}
</style></head><body><div class="b">
<div class="top"><span><span class="pp">(</span> GS-Loft-Dev <span class="pp">)</span></span>
<div class="nav"><span>( longevità )</span><span>( performance )</span><span>( biohacking )</span><span class="tag">( dev )</span></div></div>
<svg class="logo" viewBox="0 0 1272 252.247" fill="currentColor">{LOGO}</svg>
<div class="sub">Coaching per longevità e performance</div>
<div class="claim">Tecnologia<br><i>al servizio del</i><br>metodo.</div>
<div class="num">(01) &nbsp;Strumenti interni del team GS LOFT:<br>dashboard, automazioni e integrazioni.</div>
<div class="bot"><span>gsloft.it</span><span>Desenzano del Garda &nbsp;·&nbsp; Milano</span><span>( dal 2019 )</span></div>
</div></body></html>'''

for name, t in THEMES.items():
    page = SRC / f'banner-{name}.html'
    page.write_text(html(t), encoding='utf-8')
    out = OUT / f'banner-{name}.png'
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=2',
                    '--window-size=1280,400', '--virtual-time-budget=6000', f'--screenshot={out}', page.as_uri()],
                   check=True, capture_output=True)
    print(out, out.stat().st_size)
