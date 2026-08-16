"""
Generalized version of auto_triage_faria_lima.py: runs the trained model
over every mosaico_* folder found (one per neighborhood), copies the best
detections per region into data/samples/, and writes a per-region summary
(reports/detection_summary_by_region.json) that the dashboard can read to
build "detections found" cards.

Run from the ROOT of the repository:
    python3 src/geospatial/auto_triage_regions.py
"""
import json
from datetime import datetime
from pathlib import Path
import shutil

from ultralytics import YOLO

# ── CONFIG ──────────────────────────────────────────────────────────
GEOSPATIAL_DIR = Path("src/geospatial")
MODEL_PATH = Path("artifacts/runs/runs/detect/exp1/weights/best.pt")  # exp1
OUTPUT_DIR = Path("data/samples")
SUMMARY_PATH = Path("reports/detection_summary_by_region_exp1.json")
CONF_THRESHOLD = 0.25
MAX_SAMPLES_PER_REGION = 6  # keep the sample gallery from getting huge with 10 regions

# ── SETUP ───────────────────────────────────────────────────────────
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)

if not MODEL_PATH.exists():
    raise SystemExit(f"❌ Model not found at: {MODEL_PATH}")

model = YOLO(str(MODEL_PATH))

region_dirs = sorted(GEOSPATIAL_DIR.glob("mosaico_*"))
if not region_dirs:
    raise SystemExit(f"❌ No mosaico_* folders found under {GEOSPATIAL_DIR}/")

print(f"📍 {len(region_dirs)} region folder(s) found:\n")
for d in region_dirs:
    print(f"   - {d.name}")
print()

regions_summary = []
grand_total_tiles = 0
grand_total_detected = 0

for region_dir in region_dirs:
    region_name = region_dir.name.replace("mosaico_", "")
    tiles = sorted(region_dir.glob("tile_z*_x*_y*.jpg"))

    if not tiles:
        print(f"⚠️  {region_name}: no tiles found, skipping.")
        continue

    print(f"── {region_name}: {len(tiles)} tile(s)")

    detections = []  # (confidence, tile_path)
    for i, tile_path in enumerate(tiles):
        if (i + 1) % 100 == 0:
            print(f"     Processing {i+1}/{len(tiles)}...")

        result = model.predict(source=str(tile_path), conf=CONF_THRESHOLD, verbose=False)[0]
        if len(result.boxes) > 0:
            best_conf = float(result.boxes.conf.max())
            detections.append((best_conf, tile_path))

    detections.sort(key=lambda x: x[0], reverse=True)
    selected = detections[:MAX_SAMPLES_PER_REGION]

    for conf, tile_path in selected:
        dest = OUTPUT_DIR / tile_path.name
        shutil.copy2(tile_path, dest)

    n_detected = len(detections)
    n_total = len(tiles)
    rate = round(n_detected / n_total, 4) if n_total else 0.0
    top_conf = round(detections[0][0], 4) if detections else None

    print(f"   🎯 {n_detected}/{n_total} detected ({rate*100:.1f}%) "
          f"— {len(selected)} sample(s) copied to data/samples/\n")

    regions_summary.append({
        "region": region_name,
        "tiles_total": n_total,
        "tiles_detected": n_detected,
        "detection_rate": rate,
        "top_confidence": top_conf,
        "samples_copied": len(selected),
    })

    grand_total_tiles += n_total
    grand_total_detected += n_detected

# ── SAVE SUMMARY ────────────────────────────────────────────────────
summary = {
    "generated_at": datetime.now().isoformat(timespec="seconds"),
    "model": str(MODEL_PATH),
    "confidence_threshold": CONF_THRESHOLD,
    "regions": regions_summary,
    "totals": {
        "tiles_total": grand_total_tiles,
        "tiles_detected": grand_total_detected,
        "detection_rate": round(grand_total_detected / grand_total_tiles, 4) if grand_total_tiles else 0.0,
    },
}

with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

# ── PRINT FINAL TABLE ───────────────────────────────────────────────
print("=" * 60)
print("SUMMARY BY REGION")
print("=" * 60)
for r in regions_summary:
    print(f"{r['region']:<25} {r['tiles_detected']:>4}/{r['tiles_total']:<4} "
          f"({r['detection_rate']*100:>5.1f}%)")
print("-" * 60)
print(f"{'TOTAL':<25} {grand_total_detected:>4}/{grand_total_tiles:<4} "
      f"({summary['totals']['detection_rate']*100:>5.1f}%)")
print("=" * 60)
print(f"\n✅ Summary saved to {SUMMARY_PATH}")
print("   Next: add cards to the dashboard reading this file.")
