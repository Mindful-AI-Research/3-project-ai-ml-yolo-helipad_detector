"""Gera assets/globe_intro.js a partir de globe_intro.template.js.

Dados de costa: Natural Earth 110m (domínio público) via npm `world-atlas`,
amostrados numa grade equiárea (~178 km). Entrada: land_real.json
(lista plana [lat*10, lon*10, ...]). Uso (a partir da raiz do repo):  python tools/globe/build_globe_intro.py  ->  grava assets/globe_intro.js
"""
import json, pathlib

here = pathlib.Path(__file__).parent
flat = json.loads((here / "land_real.json").read_text())
pts = list(zip(flat[0::2], flat[1::2]))           # (lat10, lon10)

rows = {}
for lat10, lon10 in pts:
    rows.setdefault(lat10, []).append(lon10)

def b36(n: int) -> str:
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    if n == 0:
        return "0"
    s = ""
    while n:
        n, r = divmod(n, 36)
        s = digits[r] + s
    return s

enc_rows = []
for lat10 in sorted(rows, reverse=True):
    lons = sorted(rows[lat10])
    out, prev = [], None
    for lon10 in lons:
        out.append(b36(lon10 + 1800) if prev is None else b36(lon10 - prev))
        prev = lon10
    enc_rows.append(f"{lat10}:{','.join(out)}")
encoded = ";".join(enc_rows)

tpl = (here / "globe_intro.template.js").read_text(encoding="utf-8")
assert "__LAND__" in tpl and "</script" not in tpl.lower()
out = here.parent.parent / "assets" / "globe_intro.js"
out.parent.mkdir(exist_ok=True)
out.write_text(tpl.replace("__LAND__", encoded), encoding="utf-8")
print(f"{len(pts)} pontos -> {len(encoded)} bytes codificados -> {out}")
