"""Adds soft, GPU-cheap animations to the TikZ-exported SVGs (pdftocairo output)."""
import re, sys, pathlib

CSS = """<style>
.hd-flow{stroke-dasharray:18 4;animation:hdflow 2.4s linear infinite}
@keyframes hdflow{to{stroke-dashoffset:-22}}
.hd-badge,.hd-badgefill{animation:hdpulse 3.6s ease-in-out infinite}
@keyframes hdpulse{0%,100%{opacity:1}50%{opacity:.5}}
.hd-hot{animation:hdhot 4.2s ease-in-out infinite}
@keyframes hdhot{0%,100%{stroke-opacity:.45}50%{stroke-opacity:.95}}
@media (prefers-reduced-motion:reduce){.hd-flow,.hd-badge,.hd-badgefill,.hd-hot{animation:none}}
</style>"""

FLOW  = r'stroke="rgb\(7\.8\d*%, 72\.1\d*%, 65\.0\d*%\)"'
BADGE = r'stroke="rgb\(8\.2\d*%, 72\.1\d*%, 65\.0\d*%\)"'
HOT   = r'stroke="rgb\(86\.\d*%, 0%, 0%\)"'

def add_class(svg, pattern, cls, need_fill_none=True, delay_step=0.0):
    out, n = [], 0
    pos = 0
    for m in re.finditer(r'<path [^>]*>', svg):
        tag = m.group(0)
        if re.search(pattern, tag) and (not need_fill_none or 'fill="none"' in tag):
            style = f' style="animation-delay:{(n*delay_step):.2f}s"' if delay_step else ''
            new = tag.replace('<path ', f'<path class="{cls}"{style} ', 1)
            out.append(svg[pos:m.start()]); out.append(new); pos = m.end(); n += 1
    out.append(svg[pos:])
    return ''.join(out), n

def process(path):
    s = pathlib.Path(path).read_text()
    s, nf = add_class(s, FLOW, 'hd-flow', True, 0.0)
    s, nb = add_class(s, BADGE, 'hd-badge', True, 0.45)
    s, nh = add_class(s, HOT, 'hd-hot', True, 0.0)
    # badge fills: the dark-teal fill used only by badges
    s, nbf = add_class(s, r'fill="rgb\(4\.8\d*%, 21\.6\d*%, 22\.5\d*%\)"', 'hd-badgefill', False, 0.45)
    s = s.replace('</defs>', '</defs>' + CSS, 1) if '</defs>' in s else s
    pathlib.Path(path).write_text(s)
    return nf, nb, nh, nbf

def gradient(path):
    s = pathlib.Path(path).read_text()
    w = float(re.search(r'viewBox="0 0 ([\d.]+)', s).group(1))
    target = r'rgb\(49\.\d*%, 87\.\d*%, 83\.\d*%\)'
    n = len(re.findall(target, s))
    s = re.sub(target, 'url(#hdg)', s)
    grad = (f'<linearGradient id="hdg" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w/2:.1f}" y2="0" spreadMethod="reflect">'
            '<stop offset="0" stop-color="#0E9C8E"/><stop offset=".5" stop-color="#B4F5EA"/><stop offset="1" stop-color="#14B8A6"/>'
            f'<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="{w:.1f} 0" dur="7s" repeatCount="indefinite"/>'
            '</linearGradient>')
    css = '<style>@media (prefers-reduced-motion:reduce){animateTransform{display:none}}</style>'
    s = s.replace('</defs>', grad + '</defs>', 1)
    pathlib.Path(path).write_text(s)
    return n

if __name__ == '__main__':
    for p in sys.argv[1:]:
        name = pathlib.Path(p).name
        print(name, gradient(p) if 'fig2f' in name else process(p))
