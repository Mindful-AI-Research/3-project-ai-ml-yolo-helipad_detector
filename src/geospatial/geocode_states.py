"""
Reclassifica cada linha de helipad_coordinates.csv pelo ESTADO real,
via reverse geocoding no Nominatim (mesmo serviço já usado em helipad_bot.py).

Rode local: python3 geocode_states.py
Gera: helipad_coordinates_com_estado.csv  (mesmas colunas + "Estado" e "Regiao")
Imprime um resumo SP vs. outros estados no final.
"""
import csv
import time
import requests
from pathlib import Path

INPUT_CSV = "helipad_coordinates.csv"   # ajuste o caminho se necessário
OUTPUT_CSV = "helipad_coordinates_com_estado.csv"

HEADERS = {"User-Agent": "helipoint-detector-state-split/1.0 (uso academico)"}


def parse_bbox_centroid(raw: str):
    """'lon_min lat_min lon_max lat_max' (tab ou espaço) -> (lat, lon) do centro."""
    parts = raw.replace(",", " ").split()
    if len(parts) < 4:
        return None, None
    lon_min, lat_min, lon_max, lat_max = (float(p) for p in parts[:4])
    return (lat_min + lat_max) / 2, (lon_min + lon_max) / 2


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
    rows = list(csv.DictReader(open(INPUT_CSV, newline="", encoding="utf-8-sig")))
    print(f"{len(rows)} registros carregados de {INPUT_CSV}\n")

    fieldnames = list(rows[0].keys()) + ["Estado"]
    contagem_estado = {}

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for i, row in enumerate(rows, start=1):
            lat, lon = parse_bbox_centroid(row["Coordenadas da Bounding Box"])
            estado = reverse_geocode_state(lat, lon) if lat is not None else ""
            row["Estado"] = estado
            writer.writerow(row)
            contagem_estado[estado or "(desconhecido)"] = contagem_estado.get(estado or "(desconhecido)", 0) + 1
            print(f"[{i:3d}/{len(rows)}] {row.get('Nome do Bairro', ''):30s} -> {estado or '???'}")

    print(f"\nArquivo gerado: {OUTPUT_CSV}\n")
    print("=== Resumo por estado ===")
    for estado, qtd in sorted(contagem_estado.items(), key=lambda kv: -kv[1]):
        print(f"  {estado:30s} {qtd:3d}")

    sp = contagem_estado.get("São Paulo", 0)
    outros = len(rows) - sp
    print(f"\nSão Paulo: {sp}  |  Outros estados: {outros}  |  Total: {len(rows)}")


if __name__ == "__main__":
    main()
