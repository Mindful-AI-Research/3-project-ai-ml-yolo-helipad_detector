"""
Automatic triage of the Faria Lima tiles using the already-trained model.

What it does:
1. Runs YOLO (exp2, the best-performing model) on every downloaded tile
2. Copies ONLY the tiles with a detected helipad (conf >= 0.25) to data/samples/
3. Prints a summary so you can quickly confirm what was found

Run from the ROOT of the repository:
    python3 auto_triage_faria_lima.py
"""
from pathlib import Path
from ultralytics import YOLO
import shutil

# ── CONFIG ──────────────────────────────────────────────────────────
TILES_DIR = Path("src/geospatial")          # where the downloaded tiles live
MODEL_PATH = Path("artifacts/runs/runs/detect/exp2/weights/best.pt")  # best model
OUTPUT_DIR = Path("data/samples")            # where the dashboard reads samples from
CONF_THRESHOLD = 0.25
MAX_SAMPLES = 12                             # no need for hundreds, just the best ones

# ── SETUP ───────────────────────────────────────────────────────────
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not MODEL_PATH.exists():
    raise SystemExit(f"❌ Model not found at: {MODEL_PATH}")

model = YOLO(str(MODEL_PATH))

tiles = sorted(TILES_DIR.glob("tile_z*_x*_y*.jpg"))
print(f"🔍 {len(tiles)} Faria Lima tile(s) found in {TILES_DIR}/")

if not tiles:
    raise SystemExit(f"❌ No tiles found in {TILES_DIR}/ — check the path.")

# ── BATCH INFERENCE ─────────────────────────────────────────────────
detections = []  # (confidence, tile_path)

for i, tile_path in enumerate(tiles):
    if (i + 1) % 50 == 0 or i == 0:
        print(f"   Processing {i+1}/{len(tiles)}...")

    result = model.predict(source=str(tile_path), conf=CONF_THRESHOLD, verbose=False)[0]

    if len(result.boxes) > 0:
        best_conf = float(result.boxes.conf.max())
        detections.append((best_conf, tile_path))

print(f"\n🎯 {len(detections)} tile(s) with a detected helipad.")

# ── PICK THE BEST ONES AND COPY ─────────────────────────────────────
detections.sort(key=lambda x: x[0], reverse=True)
selected = detections[:MAX_SAMPLES]

for conf, tile_path in selected:
    dest = OUTPUT_DIR / tile_path.name
    shutil.copy2(tile_path, dest)
    print(f"   ✅ conf={conf:.2f}  {tile_path.name} -> {dest}")

print(f"\n✅ Done: {len(selected)} image(s) copied to {OUTPUT_DIR}/")
print("   Now just run 'streamlit run apps/streamlit_app/app.py' "
      "and check the '🖼️ Sample Images' tab.")
