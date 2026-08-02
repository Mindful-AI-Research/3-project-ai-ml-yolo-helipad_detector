"""
Downloads ESRI World Imagery tiles for every neighborhood listed in
src/geospatial/sp_neighborhoods_bbox.csv.

Resumable: tiles already on disk are skipped, so you can stop (Ctrl+C)
and re-run later without losing progress or re-downloading anything.

Run from the ROOT of the repository:
    python3 src/geospatial/download_all_regions.py
"""
import math
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests

# ── CONFIG ──────────────────────────────────────────────────────────
CSV_PATH = Path("src/geospatial/sp_neighborhoods_bbox.csv")
OUT_ROOT = Path("src/geospatial")
ZOOM = 19
TILE_URL = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
HEADERS = {"User-Agent": "Helipad-Detector-PUC-SP/1.0"}
MAX_WORKERS = 4

BBOX_COL = "Coordenadas da Bounding Box"
NAME_COL = "Nome do Bairro"


def deg2tile(lat, lon, z):
    n = 2.0 ** z
    x = int((lon + 180.0) / 360.0 * n)
    lat_rad = math.radians(lat)
    y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return x, y


def parse_bbox(raw):
    parts = str(raw).replace(",", " ").split()
    return tuple(float(p) for p in parts)  # lon_min, lat_min, lon_max, lat_max


def slugify(name):
    return str(name).strip().replace(" ", "_").replace("/", "-").replace("(", "").replace(")", "")


def download_tile(args):
    z, x, y, out_dir = args
    path = out_dir / f"tile_z{z}_x{x}_y{y}.jpg"
    if path.exists():
        return path, True, "cached"
    for attempt in range(3):
        try:
            r = requests.get(TILE_URL.format(z=z, x=x, y=y), headers=HEADERS, timeout=25)
            if r.status_code == 200 and len(r.content) > 2000:
                path.write_bytes(r.content)
                return path, True, "downloaded"
        except Exception:
            time.sleep(0.5)
    return path, False, "failed"


def main():
    if not CSV_PATH.exists():
        raise SystemExit(f"❌ CSV not found: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    if BBOX_COL not in df.columns or NAME_COL not in df.columns:
        raise SystemExit(f"❌ Expected columns not found. Got: {list(df.columns)}")

    print(f"📍 {len(df)} region(s) found in {CSV_PATH}\n")

    for _, row in df.iterrows():
        name = row[NAME_COL]
        slug = slugify(name)
        out_dir = OUT_ROOT / f"mosaico_{slug}"
        out_dir.mkdir(exist_ok=True)

        try:
            lon_min, lat_min, lon_max, lat_max = parse_bbox(row[BBOX_COL])
        except Exception as e:
            print(f"⚠️  Skipping '{name}' — could not parse bbox: {e}")
            continue

        x_min, y_max = deg2tile(lat_min, lon_min, ZOOM)
        x_max, y_min = deg2tile(lat_max, lon_max, ZOOM)

        jobs = [(ZOOM, x, y, out_dir)
                for x in range(x_min, x_max + 1)
                for y in range(y_min, y_max + 1)]

        already = sum(1 for j in jobs if (out_dir / f"tile_z{j[0]}_x{j[1]}_y{j[2]}.jpg").exists())
        print(f"── {name} ({slug}) — {len(jobs)} tile(s) total, {already} already on disk")

        ok = failed = 0
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
            for path, success, status in ex.map(download_tile, jobs):
                if success:
                    ok += 1
                else:
                    failed += 1

        print(f"   ✅ {ok} OK  |  ❌ {failed} failed\n")

    print("✅ All regions processed. Next step: run auto_triage_regions.py")


if __name__ == "__main__":
    main()
