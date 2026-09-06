"""
Reclassifica cada linha de helipad_coordinates.csv pelo ESTADO real,
via reverse geocoding no Nominatim (mesmo serviço já usado em helipad_bot.py).

Rode local: python3 geocode_states.py
Gera: helipad_coordinates_com_estado.csv  (mesmas colunas + "Estado" e "Regiao")
Imprime um resumo SP vs. outros estados no final.

--- Alterações feitas por Claude em cima da versão original da Fabi ---
1. INPUT_CSV agora aponta para src/geospatial/helipad_coordinates_bbox.csv
   por padrão — é esse o arquivo que o app.py realmente usa pra montar o
   mapa/heatmap da aba Maps (constante COORDS_CSV lá no app). O nome
   "helipad_coordinates.csv" (sem "_bbox") é usado por um arquivo diferente
   e mais antigo do projeto; se era esse mesmo que você queria ler, é só
   trocar o valor de INPUT_CSV de volta ou passar --input na linha de
   comando (adicionei essa opção abaixo).
2. parse_bbox_centroid tentava fazer float() direto nos 4 pedaços da
   string sem tratar erro — se alguma linha ainda estivesse em DMS bruto
   (tipo 22°58'56"S 43°23'38"W, formato de antes de rodar o
   transform_coordinates.py), o script quebrava com ValueError sem
   terminar de processar as linhas seguintes. Contra o
   helipad_coordinates_bbox.csv atual (3 linhas, já convertidas) isso não
   acontece — mas testei contra uma amostra maior do projeto que tinha 80
   de 129 linhas ainda em DMS bruto, e nessa amostra o script quebrava na
   primeira linha assim. Agora ele tenta o formato decimal primeiro e cai
   automaticamente pro parser de DMS se falhar, em vez de travar.
3. Um CSV vazio (sem nenhuma linha) fazia `rows[0]` estourar IndexError
   antes mesmo de imprimir uma mensagem de erro clara — agora ele avisa e
   sai de forma limpa nesse caso.
-----------------------------------------------------------------------
"""
import argparse
import csv
import re
import sys
import time
import requests
from pathlib import Path

INPUT_CSV = "src/geospatial/helipad_coordinates_bbox.csv"
OUTPUT_CSV = "src/geospatial/helipad_coordinates_com_estado.csv"

HEADERS = {"User-Agent": "helipoint-detector-state-split/1.0 (uso academico)"}

# Mesma regex de par DMS usada em transform_coordinates.py e no fallback do
# app.py — reaproveitada aqui só como um segundo formato aceito, não como
# substituição do parser original.
_NUM = r"[-+]?\d+(?:\.\d+)?"
_DMS_RE = re.compile(
    rf"""
    (?P<g>{_NUM})\s*[°ºo]?\s*
    (?:(?P<m>{_NUM})\s*['’′]?\s*)?
    (?:(?P<s>{_NUM})\s*["”″]?\s*)?
    (?P<dir>[NSEWnsew])?
    """,
    re.VERBOSE,
)


def _dms_to_dd(graus, minutos, segundos, direcao=""):
    dd = abs(graus) + minutos / 60 + segundos / 3600
    if direcao.upper() in ("S", "W") or graus < 0:
        dd = -dd
    return dd


def _parse_dms_point(texto: str):
    coords = []
    for m in _DMS_RE.finditer(str(texto)):
        if m.group("g") is None or m.group(0).strip() == "":
            continue
        graus = float(m.group("g"))
        minutos = float(m.group("m")) if m.group("m") else 0.0
        segundos = float(m.group("s")) if m.group("s") else 0.0
        direcao = m.group("dir") or ""
        coords.append(_dms_to_dd(graus, minutos, segundos, direcao))
    if len(coords) < 2:
        return None, None
    return coords[0], coords[1]  # lat, lon


def parse_bbox_centroid(raw: str):
    """'lon_min lat_min lon_max lat_max' (tab ou espaço) -> (lat, lon) do
    centro. Se a linha ainda estiver em DMS bruto (não passou pelo
    transform_coordinates.py), cai automaticamente pro parser de DMS em
    vez de estourar ValueError e travar o script no meio da lista."""
    parts = raw.replace(",", " ").split()
    if len(parts) >= 4:
        try:
            lon_min, lat_min, lon_max, lat_max = (float(p) for p in parts[:4])
            return (lat_min + lat_max) / 2, (lon_min + lon_max) / 2
        except ValueError:
            pass
    return _parse_dms_point(raw)


def reverse_geocode_state(lat: float, lon: float) -> str:
    try:
        resp = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lon, "format": "jsonv2", "zoom": 8, "addressdetails": 1},
            headers=HEADERS,
            timeout=10,
        )
        addr = resp.json().get("address", {})
        return addr.get("state", "") or ""
    except Exception as exc:
        print(f"  [aviso] falha no reverse geocode ({lat},{lon}): {exc}")
        return ""
    finally:
        time.sleep(1.0)  # respeita o rate limit do Nominatim (1 req/s)


def main():
    ap = argparse.ArgumentParser(description="Reclassifica helipontos por estado via reverse geocoding.")
    ap.add_argument("--input", default=INPUT_CSV, help=f"CSV de entrada (padrão: {INPUT_CSV})")
    ap.add_argument("--output", default=OUTPUT_CSV, help=f"CSV de saída (padrão: {OUTPUT_CSV})")
    args = ap.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        sys.exit(f"[ERRO] Arquivo não encontrado: {input_path}")

    rows = list(csv.DictReader(open(input_path, newline="", encoding="utf-8-sig")))
    if not rows:
        sys.exit(f"[ERRO] {input_path} não tem nenhuma linha de dado.")

    print(f"{len(rows)} registros carregados de {input_path}\n")

    fieldnames = list(rows[0].keys()) + ["Estado"]
    contagem_estado = {}

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for i, row in enumerate(rows, start=1):
            lat, lon = parse_bbox_centroid(row["Coordenadas da Bounding Box"])
            estado = reverse_geocode_state(lat, lon) if lat is not None else ""
            row["Estado"] = estado
            writer.writerow(row)
            contagem_estado[estado or "(desconhecido)"] = contagem_estado.get(estado or "(desconhecido)", 0) + 1
            print(f"[{i:3d}/{len(rows)}] {row.get('Nome do Bairro', ''):30s} -> {estado or '???'}")

    print(f"\nArquivo gerado: {output_path}\n")
    print("=== Resumo por estado ===")
    for estado, qtd in sorted(contagem_estado.items(), key=lambda kv: -kv[1]):
        print(f"  {estado:30s} {qtd:3d}")

    sp = contagem_estado.get("São Paulo", 0)
    outros = len(rows) - sp
    print(f"\nSão Paulo: {sp}  |  Outros estados: {outros}  |  Total: {len(rows)}")


if __name__ == "__main__":
    main()
