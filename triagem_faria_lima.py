"""
Triagem automática dos tiles do Faria Lima usando o modelo já treinado.

O que faz:
1. Roda o YOLO (exp2, o melhor modelo) em todos os tiles baixados
2. Copia SÓ os tiles com heliponto detectado (conf >= 0.25) para data/samples/
3. Gera um preview.jpg mostrando as detecções, pra você conferir rapidinho

Roda a partir da RAIZ do repositório:
    python3 triagem_faria_lima.py
"""
from pathlib import Path
from ultralytics import YOLO
import shutil

# ── CONFIG ──────────────────────────────────────────────────────────
TILES_DIR = Path("src/geospatial")          # onde estão os tiles baixados
MODEL_PATH = Path("artifacts/runs/runs/detect/exp2/weights/best.pt")  # melhor modelo
OUTPUT_DIR = Path("data/samples")            # onde o dashboard lê as amostras
CONF_THRESHOLD = 0.25
MAX_SAMPLES = 12                             # não precisa de centenas, só os melhores

# ── SETUP ───────────────────────────────────────────────────────────
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not MODEL_PATH.exists():
    raise SystemExit(f"❌ Modelo não encontrado em: {MODEL_PATH}")

model = YOLO(str(MODEL_PATH))

tiles = sorted(TILES_DIR.glob("tile_z*_x*_y*.jpg"))
print(f"🔍 {len(tiles)} tile(s) do Faria Lima encontrados em {TILES_DIR}/")

if not tiles:
    raise SystemExit(f"❌ Nenhum tile encontrado em {TILES_DIR}/ — confirma o caminho.")

# ── INFERÊNCIA EM LOTE ──────────────────────────────────────────────
detections = []  # (confidence, tile_path)

for i, tile_path in enumerate(tiles):
    if (i + 1) % 50 == 0 or i == 0:
        print(f"   Processando {i+1}/{len(tiles)}...")

    result = model.predict(source=str(tile_path), conf=CONF_THRESHOLD, verbose=False)[0]

    if len(result.boxes) > 0:
        best_conf = float(result.boxes.conf.max())
        detections.append((best_conf, tile_path))

print(f"\n🎯 {len(detections)} tile(s) com heliponto detectado.")

# ── SELECIONA OS MELHORES E COPIA ───────────────────────────────────
detections.sort(key=lambda x: x[0], reverse=True)
selected = detections[:MAX_SAMPLES]

for conf, tile_path in selected:
    dest = OUTPUT_DIR / tile_path.name
    shutil.copy2(tile_path, dest)
    print(f"   ✅ conf={conf:.2f}  {tile_path.name} → {dest}")

print(f"\n✅ Concluído: {len(selected)} imagem(ns) copiada(s) para {OUTPUT_DIR}/")
print("   Agora é só rodar 'streamlit run apps/streamlit_app/app.py' "
      "e conferir a aba '🖼️ Sample Images'.")
