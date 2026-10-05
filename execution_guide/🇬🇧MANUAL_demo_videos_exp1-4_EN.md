# 🇺🇸 [Manual — Demo Video Generation](#-manual--demo-video-generation)

**[Helipad Detection · YOLOv8n / YOLO11n · São Paulo](#1-objective)**

<br>

## 📑 [Table of Contents](#-table-of-contents)

<br>

- [1. Objective](#1-objective)
- [2. Experimental Methodology](#2-experimental-methodology)
  - [2.1 Controlled Sampling](#21-controlled-sampling)
  - [2.2 Comparability](#22-comparability)
- [3. Prerequisites](#3-prerequisites)
  - [FFmpeg — macOS](#ffmpeg--macos)
- [4. Generation Pipeline](#4-generation-pipeline)
- [5. Step 1 — Build the Tile Sample](#5-step-1--build-the-tile-sample)
- [6. Step 2 — Run Inference for the Four Experiments](#6-step-2--run-inference-for-the-four-experiments)
  - [Consistency Check](#consistency-check)
- [7. Step 3 — Convert Frames to Video](#7-step-3--convert-frames-to-video)
- [8. Step 4 — Add the Soundtrack](#8-step-4--add-the-soundtrack)
- [9. Step 5 — Create the Final Files](#9-step-5--create-the-final-files)
- [10. Experiment Captions](#10-experiment-captions)
- [11. Additional Demo — Automated Helipad Scraping](#11-additional-demo--automated-helipad-scraping)
- [12. Cleaning Intermediate Files](#12-cleaning-intermediate-files)
- [13. Final Output](#13-final-output)
  - [Comparability Criterion](#comparability-criterion)

<br>

---

<br>

## [1. Objective](#1-objective)

<br>

This manual documents the procedure used to generate demonstration videos for the four helipad detection experiments:

<br>

- `exp1` — YOLOv8n
- `exp2` — YOLOv8n
- `exp3` — YOLOv8n + augmented dataset
- `exp4` — YOLO11n

<br>

The videos present **model inference on real satellite imagery tiles**, allowing the behavior of each model to be visually inspected on images that were not used during training.

<br>

> **Important:** these videos represent **inference**, not training.

<br>

---

<br>

## [2. Experimental Methodology](#2-experimental-methodology)

<br>

### [2.1 Controlled Sampling](#21-controlled-sampling)

<br>

The geospatial dataset contains approximately **7,767–7,943 tiles**, depending on the dataset version. Running inference on every tile and converting the complete set into video would produce excessively long demonstrations and significantly increase computational cost.

<br>

For the demonstration, a **fixed sample of tiles per region** is used.

<br>

With the default configuration:

<br>

```text
10 regions × 8 tiles per region = 80 tiles
```

<br>

The sample is created **once** and reused across all four experiments.

<br>

### [2.2 Comparability](#22-comparability)

<br>

Using the same sample ensures that:

<br>

- all four models receive the same images;
- the analyzed regions are identical;
- the presentation order remains consistent;
- the soundtrack is the same;
- observed differences can be attributed to model behavior.

<br>

In other words:

<br>

> **Same scene, different model.**

<br>

This procedure prevents image selection from becoming an additional variable in the visual comparison of the experiments.

<br>

---

<br>

## [3. Prerequisites](#3-prerequisites)

<br>

Before starting, confirm that:

<br>

- the repository is located at `3-project-ai-ml-yolo-helipad_detector`;
- `ffmpeg` is installed;
- the Python environment is configured;
- the `ultralytics` package is available;
- the trained weights are available at:

<br>

```text
artifacts/runs/runs/detect/
├── exp1/weights/best.pt
├── exp2/weights/best.pt
├── exp3/weights/best.pt
└── exp4/weights/best.pt
```

<br>

- regional tiles are available under:

<br>

```text
src/geospatial/mosaic_*/
```

<br>

### [FFmpeg — macOS](#ffmpeg--macos)

<br>

If necessary:

<br>

```bash
brew install ffmpeg
```

<br>

---

<br>

## [4. Generation Pipeline](#4-generation-pipeline)

<br>

The complete process follows four main stages:

<br>

```text
Real Satellite Tiles
        │
        ▼
Controlled Sample
10 Regions
        │
        ▼
Inference
exp1 · exp2 · exp3 · exp4
        │
        ▼
Annotated Frames
        │
        ▼
MP4 Videos
        │
        ▼
Common Soundtrack
        │
        ▼
Final Demos
```

<br>

---

<br>

## [5. Step 1 — Build the Tile Sample](#5-step-1--build-the-tile-sample)

<br>

Define the number of tiles selected from each region:

<br>

```bash
cd ~/Desktop/3-project-ai-ml-yolo-helipad_detector

N_PER_REGION=8
SRC=reports/demo_src

rm -rf "$SRC"
mkdir -p "$SRC" reports/demo_frames reports/demo_videos
```

<br>

Then build the sample:

<br>

```bash
i=0

for REGION in $(ls -d src/geospatial/mosaic_*/ | sort); do
  i=$((i+1))
  PREFIX=$(printf "%02d" $i)
  REGION_NAME=$(basename "$REGION")

  echo "[$PREFIX] $REGION_NAME"

  # Extract tiles if the region still contains ZIP archives.
  unzip -n "$REGION"*.zip -d "$REGION" 2>/dev/null || true

  ls "$REGION"*.jpg | sort | head -$N_PER_REGION | while read -r TILE; do
    cp "$TILE" "$SRC/${PREFIX}_${REGION_NAME}_$(basename "$TILE")"
  done
done

echo "Total tiles:"
ls "$SRC"/*.jpg | wc -l
```

<br>

With `N_PER_REGION=8`, the expected result is approximately:

<br>

```text
80 tiles
```

<br>

Increase `N_PER_REGION` if a longer demonstration is required:

<br>

```bash
N_PER_REGION=12
```

<br>

> **Do not change the sample between experiments.** The same `reports/demo_src/` directory must be used by `exp1`, `exp2`, `exp3`, and `exp4`.

<br>

---

<br>

## [6. Step 2 — Run Inference for the Four Experiments](#6-step-2--run-inference-for-the-four-experiments)

<br>

Run inference on the same sample:

<br>

```bash
for EXP in exp1 exp2 exp3 exp4; do
  echo "=== Running $EXP ==="

  python -c "
from ultralytics import YOLO

model = YOLO(
    'artifacts/runs/runs/detect/$EXP/weights/best.pt'
)

model.predict(
    source='reports/demo_src',
    conf=0.25,
    save=True,
    project='reports/demo_frames',
    name='$EXP',
    exist_ok=True
)
"

  echo "$EXP: $(ls reports/demo_frames/$EXP/*.jpg | wc -l) frames"
done
```

<br>

The resulting structure will be:

<br>

```text
reports/demo_frames/
├── exp1/
├── exp2/
├── exp3/
└── exp4/
```

<br>

Each directory contains the annotated frames generated by the corresponding model.

<br>

### [Consistency Check](#consistency-check)

<br>

All four experiments should generate the same number of frames.

<br>

For an 80-tile sample:

<br>

```text
exp1 → 80 frames
exp2 → 80 frames
exp3 → 80 frames
exp4 → 80 frames
```

<br>

A difference in frame count indicates that the execution should be checked before generating the videos.

<br>

---

<br>

## [7. Step 3 — Convert Frames to Video](#7-step-3--convert-frames-to-video)

<br>

Use `ffmpeg` to convert the annotated frames into MP4 videos.

<br>

A rate of **2 FPS** is recommended so that the detections remain clearly visible.

<br>

```bash
FPS=2

for EXP in exp1 exp2 exp3 exp4; do
  cd reports/demo_frames/$EXP

  ffmpeg -y \
    -framerate $FPS \
    -pattern_type glob \
    -i '*.jpg' \
    -pix_fmt yuv420p \
    ../../demo_videos/${EXP}_silent.mp4

  cd -
done
```

<br>

The intermediate videos will be created under:

<br>

```text
reports/demo_videos/
├── exp1_silent.mp4
├── exp2_silent.mp4
├── exp3_silent.mp4
└── exp4_silent.mp4
```

<br>

---

<br>

## [8. Step 4 — Add the Soundtrack](#8-step-4--add-the-soundtrack)

<br>

All four videos use the **same soundtrack**.

<br>

This standardization is intentional: since the purpose is to compare model behavior visually, the soundtrack should not introduce an additional variable between experiments.

<br>

```bash
AUDIO="assets/audio/Interstellar - Deep House Remix.m4a"

for EXP in exp1 exp2 exp3 exp4; do
  ffmpeg -y \
    -i reports/demo_videos/${EXP}_silent.mp4 \
    -i "$AUDIO" \
    -c:v copy \
    -c:a aac \
    -shortest \
    reports/demo_videos/${EXP}_with_audio.mp4
done
```

<br>

> Confirm the exact filename under `assets/audio/` before running the command.

<br>

---

<br>

## [9. Step 5 — Create the Final Files](#9-step-5--create-the-final-files)

<br>

Create the demo directory:

<br>

```bash
mkdir -p demo
```

<br>

Copy the final videos:

<br>

```bash
cp reports/demo_videos/exp1_with_audio.mp4 \
  "demo/Helipad-Detection-exp1-YOLOv8n-Deteccao-em-Tiles-Reais.mp4"

cp reports/demo_videos/exp2_with_audio.mp4 \
  "demo/Helipad-Detection-exp2-YOLOv8n-Deteccao-em-Tiles-Reais.mp4"

cp reports/demo_videos/exp3_with_audio.mp4 \
  "demo/Helipad-Detection-exp3-YOLOv8n-Deteccao-em-Tiles-Reais.mp4"

cp reports/demo_videos/exp4_with_audio.mp4 \
  "demo/Helipad-Detection-exp4-YOLO11n-Deteccao-em-Tiles-Reais.mp4"
```

<br>

Verify the files:

<br>

```bash
ls -lh demo/*.mp4
```

<br>

---

<br>

## [10. Experiment Captions](#10-experiment-captions)

<br>

| Experiment | Description |
|---|---|
| **exp1** | **60 epochs · YOLOv8n** — high precision on the curated benchmark, but lower coverage of helipads observed in field conditions. |
| **exp2** | **100 epochs · YOLOv8n** — reference model, with the best observed generalization under field conditions. |
| **exp3** | **100 epochs · YOLOv8n + augmented dataset** — higher recall, with intermediate field performance. |
| **exp4** | **100 epochs · YOLO11n** — same experimental base as `exp2`, using a newer architecture, but without outperforming `exp2` in the field evaluation. |

<br>

> The descriptions should remain consistent with the results reported in the project's final experimental analysis.

<br>

---

<br>

## [11. Additional Demo — Automated Helipad Scraping](#11-additional-demo--automated-helipad-scraping)

<br>

The **Automated Helipad Scraping Demo** serves a different purpose from the four detection videos.

<br>

It demonstrates the **automated collection of helipad coordinates**, performed using Selenium and `helipad_bot.py`.

<br>

Therefore, it **does not use the inference pipeline described in Steps 5–9**.

<br>

To add the soundtrack:

<br>

```bash
cd ~/Desktop/3-project-ai-ml-yolo-helipad_detector

SCRAPING_VIDEO="demo/🚁Automated Helipad Scraping Demo.mp4"
SCRAPING_AUDIO="assets/audio/feel-good_nina-simone_house remix.mp3"

ffmpeg -y \
  -i "$SCRAPING_VIDEO" \
  -i "$SCRAPING_AUDIO" \
  -c:v copy \
  -c:a aac \
  -shortest \
  "demo/🚁Automated-Helipad-Scraping-Demo-com-trilha.mp4"
```

<br>

This procedure creates a new version of the video while preserving the original file.

<br>

> [!TIP]
> If the original video already contains narration or another audio track, the command above will replace it. To preserve and combine both audio sources, use `amix`.

<br>

---

<br>

## [12. Cleaning Intermediate Files](#12-cleaning-intermediate-files)

<br>

After validating the final videos, the intermediate files can be removed:

<br>

```bash
rm -rf reports/demo_frames
rm -rf reports/demo_src
rm -f reports/demo_videos/*_silent.mp4
```

<br>

The final files in `demo/` remain preserved.

<br>

---

<br>

## [13. Final Output](#13-final-output)

<br>

At the end of the process, the `demo/` directory should contain the four experiment videos:

<br>

```text
demo/
├── Helipad-Detection-exp1-YOLOv8n-Deteccao-em-Tiles-Reais.mp4
├── Helipad-Detection-exp2-YOLOv8n-Deteccao-em-Tiles-Reais.mp4
├── Helipad-Detection-exp3-YOLOv8n-Deteccao-em-Tiles-Reais.mp4
├── Helipad-Detection-exp4-YOLO11n-Deteccao-em-Tiles-Reais.mp4
└── 🚁Automated-Helipad-Scraping-Demo-com-trilha.mp4
```

<br>

### [Comparability Criterion](#comparability-criterion)

<br>

The validity of the visual demonstration depends on three elements remaining constant:

<br>

**same input images · same order · same soundtrack**

<br>

The only experimental variable changed across the four detection videos is the **model used for inference**.

<br>

> **Same scene. Different model.**
