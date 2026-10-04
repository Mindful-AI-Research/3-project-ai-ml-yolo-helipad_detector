# 🇬🇧 Manual — Generate the Demo Videos (exp1 to exp4, all 10 regions)

<br><br>

## [Before You Start]()

<br>

This manual generates, for each of the 4 experiments, a video showing the model detecting helipads on real satellite tiles — this is not a training video, it's inference (the already-trained model running on images it never saw during training).

**About covering all 10 regions:** running literally every ~7,767–7,943 tiles into video would be far too long (at 4 fps, over 30 minutes per experiment) and slow to process 4 times without a GPU. Instead, this manual **samples a fixed number of tiles from each of the 10 regions** — so the video tours every neighborhood without becoming a marathon. The **exact same tiles** are used across all 4 experiments, keeping the comparison fair: same scene, different model.

<br>

### [***Prerequisites***]

<br>

- Terminal open at the repository root (`3-MAINproject-ai-ml-yolo-helipad_detector`)
- `ffmpeg` installed (`brew install ffmpeg` on Mac, if you don't have it yet)
- All 4 trained weights at `artifacts/runs/runs/detect/exp{1,2,3,4}/weights/best.pt`
- Tiles for all 10 regions already downloaded at `src/geospatial/mosaic_*/`

<br><br>

## [Step 1 — Build the Sample (same tiles for all 4 experiments)]()

<br>

This block grabs `N_PER_REGION` tiles from each of the 10 `mosaic_*` folders, numbers the filename by region order (so the final video tours the neighborhoods in sequence, not shuffled), and collects everything into one source folder.

```bash
cd ~/Desktop/3-MAINproject-ai-ml-yolo-helipad_detector

N_PER_REGION=8   # tiles per neighborhood — 10 neighborhoods x 8 = 80 frames in the final video
SRC=reports/demo_src

rm -rf "$SRC" && mkdir -p "$SRC" reports/demo_frames reports/demo_videos

i=0
for REGION in $(ls -d src/geospatial/mosaic_*/ | sort); do
  i=$((i+1))
  PREFIX=$(printf "%02d" $i)
  REGION_NAME=$(basename "$REGION")
  echo "[$PREFIX] $REGION_NAME"

  # if the folder only has the .zip, unpack it first
  unzip -n "$REGION"*.zip -d "$REGION" 2>/dev/null || true

  ls "$REGION"*.jpg | sort | head -$N_PER_REGION | while read -r TILE; do
    cp "$TILE" "$SRC/${PREFIX}_${REGION_NAME}_$(basename "$TILE")"
  done
done

echo "Total tiles in the sample:"
ls "$SRC"/*.jpg | wc -l   # should be ~80 (or N_PER_REGION x number of regions found)
```

<br>

> Want more coverage per neighborhood? Just increase `N_PER_REGION` — the video gets longer, but inference still runs only once per experiment.

<br><br>

## [Step 2 — Run Inference on All 4 Experiments (over the same sample)]()

<br>

Since the sample is already built and small (~80 tiles), this runs fast even without a GPU.

```bash
for EXP in exp1 exp2 exp3 exp4; do
  echo "=== Running $EXP ==="
  python -c "
from ultralytics import YOLO
model = YOLO('artifacts/runs/runs/detect/$EXP/weights/best.pt')
model.predict(source='reports/demo_src', conf=0.25, save=True,
               project='reports/demo_frames', name='$EXP', exist_ok=True)
"
  echo "$EXP: $(ls reports/demo_frames/$EXP/*.jpg | wc -l) frames generated"
done
```

Confirm all 4 generated the same frame count (matching Step 1's sample) — if one comes out different, one of the weight files may have failed to load.

<br><br>

## [Step 3 — Turn Into Video (ffmpeg)]()

<br>

```bash
FPS=2   # tiles per second — with tiles from 10 different neighborhoods, slower helps viewers follow along

for EXP in exp1 exp2 exp3 exp4; do
  cd reports/demo_frames/$EXP
  ffmpeg -y -framerate $FPS -pattern_type glob -i '*.jpg' -pix_fmt yuv420p \
    ../../demo_videos/${EXP}_silent.mp4
  cd -
done
```

At this point you have 4 silent videos in `reports/demo_videos/`, each touring all 10 regions.

<br><br>

## [Step 4 — Add the Soundtrack (Interstellar)]()

<br>

All 4 detection videos deliberately share the same track — since they're compared side by side, changing the music along with the experiment would introduce a variable that confounds the comparison.

```bash
AUDIO="assets/audio/Interstellar - Deep House Remix.m4a"   # check the exact filename in your assets/audio/ folder

for EXP in exp1 exp2 exp3 exp4; do
  ffmpeg -y -i reports/demo_videos/${EXP}_silent.mp4 -i "$AUDIO" \
    -c:v copy -c:a aac -shortest \
    reports/demo_videos/${EXP}_with_audio.mp4
done
```

<br><br>

## [Step 5 — Rename to Final Filenames]()

<br>

```bash
mkdir -p demo
cp reports/demo_videos/exp1_with_audio.mp4 "demo/Helipad-Detection-exp1-YOLOv8n-Deteccao-em-Tiles-Reais.mp4"
cp reports/demo_videos/exp2_with_audio.mp4 "demo/Helipad-Detection-exp2-YOLOv8n-Deteccao-em-Tiles-Reais.mp4"
cp reports/demo_videos/exp3_with_audio.mp4 "demo/Helipad-Detection-exp3-YOLOv8n-Deteccao-em-Tiles-Reais.mp4"
cp reports/demo_videos/exp4_with_audio.mp4 "demo/Helipad-Detection-exp4-YOLO11n-Deteccao-em-Tiles-Reais.mp4"

ls -la demo/*.mp4
```

<br>

### [***Optional — clean up intermediate files***]

<br>

The frames (`reports/demo_frames/`) and source sample (`reports/demo_src/`) take up disk space and don't need to be version-controlled. Once you've checked the final videos:

```bash
rm -rf reports/demo_frames reports/demo_src reports/demo_videos/*_silent.mp4
```

<br><br>

## [Suggested Captions (one line per video)]()

<br>

| Video | Caption |
|---|---|
| exp1 | exp1 (60 epochs, YOLOv8n) — high Precision on the curated benchmark, but detects only ~half the real helipads in the field |
| exp2 | exp2 (100 epochs, YOLOv8n) — the production model, best field generalization |
| exp3 | exp3 (100 epochs, YOLOv8n, augmented dataset) — higher recall, mid-pack field result |
| exp4 | exp4 (100 epochs, YOLO11n) — same base as exp2, newer architecture; did not outperform exp2 in the field |
