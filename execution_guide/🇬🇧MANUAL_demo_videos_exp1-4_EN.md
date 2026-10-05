# 🇺🇸 Manual — Demo Video Generation

**Helipad Detection · YOLOv8n / YOLO11n · São Paulo**

<br>

## 📑 Table of Contents

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
- [9. Step 5 — Create the Final Demo Videos](#9-step-5--create-the-final-demo-videos)
- [10. Experiment Captions](#10-experiment-captions)
- [11. Demo 5 — Automated Helipad Scraping](#11-demo-5--automated-helipad-scraping)
- [12. Clean Up Intermediate Files](#12-clean-up-intermediate-files)
- [13. Final Output](#13-final-output)
  - [Comparability Criterion](#comparability-criterion)

<br><br>

## 1. Objective

This manual documents the procedure used to generate the demonstration videos for the four helipad detection experiments:

- `exp1` — YOLOv8n
- `exp2` — YOLOv8n
- `exp3` — YOLOv8n + augmented dataset
- `exp4` — YOLO11n

The videos present **model inference on real satellite imagery tiles**, allowing the behavior of each trained model to be visually inspected on images that were not used during training.

> **Important:** these videos represent **inference**, not training.

The four detection videos are presented as:

- **🎥 Demo 1** — `exp1`
- **🎥 Demo 2** — `exp2`
- **🎥 Demo 3** — `exp3`
- **🎥 Demo 4** — `exp4`

A fifth demonstration covers the automated geospatial data collection process:

- **🎥 Demo 5** — Automated Helipad Scraping

<br>

---

## 2. Experimental Methodology

### 2.1 Controlled Sampling

The geospatial dataset contains approximately **7,767–7,943 tiles**, depending on the dataset version. Running inference on every tile and converting the complete set into video would produce excessively long demonstrations and significantly increase processing time.

For the demonstrations, a **fixed number of tiles is sampled from each of the 10 regions**.

With the default configuration:

```text
10 regions × 8 tiles per region = 80 tiles
```

The sample is created **once** and reused across all four detection experiments.

### 2.2 Comparability

Using the same sample ensures that:

- all four models receive the same images;
- the analyzed regions are identical;
- the presentation order remains consistent;
- the soundtrack is identical;
- observed differences can be attributed to model behavior.

In other words:

> **Same scene. Different model.**

This prevents image selection from becoming an additional variable in the visual comparison.

<br>

---

## 3. Prerequisites

Before starting, confirm that:

- the repository is located at `3-MAINproject-ai-ml-yolo-helipad_detector`;
- `ffmpeg` is installed;
- the Python environment is configured;
- the `ultralytics` package is available;
- the four trained weights are available at:

```text
artifacts/runs/runs/detect/
├── exp1/weights/best.pt
├── exp2/weights/best.pt
├── exp3/weights/best.pt
└── exp4/weights/best.pt
```

- the regional satellite tiles are available under:

```text
src/geospatial/mosaic_*/
```

- the required audio files are available under:

```text
assets/audio/
```

### FFmpeg — macOS

If necessary:

```bash
brew install ffmpeg
```

<br>

---

## 4. Generation Pipeline

The complete workflow is:

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
Silent MP4 Videos
        │
        ▼
Common Soundtrack
        │
        ▼
Demo 1 · Demo 2 · Demo 3 · Demo 4
```

The scraping demonstration follows a separate workflow:

```text
Automated Data Collection
        │
        ▼
Selenium / helipad_bot.py
        │
        ▼
Helipad Coordinates
        │
        ▼
Demo 5
        │
        ▼
Soundtrack
```

> **Demo 1–4** demonstrate model inference.  
> **Demo 5** demonstrates automated helipad data collection.

<br>

---

## 5. Step 1 — Build the Tile Sample

Define the number of tiles selected from each region:

```bash
cd ~/Desktop/3-MAINproject-ai-ml-yolo-helipad_detector

N_PER_REGION=8
SRC=reports/demo_src

rm -rf "$SRC"
rm -rf reports/demo_frames
mkdir -p "$SRC" reports/demo_frames reports/demo_videos
```

> Removing `reports/demo_frames` before inference is intentional. It prevents frames from a previous execution from being mixed with the current sample.

Build the controlled sample:

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

With `N_PER_REGION=8`, the expected sample size is:

```text
80 tiles
```

To create a longer demonstration, increase the value:

```bash
N_PER_REGION=12
```

> **Do not change the sample between experiments.** The same `reports/demo_src/` directory must be used for `exp1`, `exp2`, `exp3`, and `exp4`.

<br>

---

## 6. Step 2 — Run Inference for the Four Experiments

Run inference on the same sample:

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

The resulting structure will be:

```text
reports/demo_frames/
├── exp1/
├── exp2/
├── exp3/
└── exp4/
```

Each directory contains the annotated frames generated by the corresponding model.

### Consistency Check

All four experiments should generate the same number of frames.

For an 80-tile sample:

```text
exp1 → 80 frames
exp2 → 80 frames
exp3 → 80 frames
exp4 → 80 frames
```

If the frame counts differ, stop and investigate before proceeding to video generation.

<br>

---

## 7. Step 3 — Convert Frames to Video

Convert the annotated frames into MP4 videos using `ffmpeg`.

A frame rate of **2 FPS** is recommended so that the detections remain visible long enough for visual inspection.

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

The intermediate videos will be created under:

```text
reports/demo_videos/
├── exp1_silent.mp4
├── exp2_silent.mp4
├── exp3_silent.mp4
└── exp4_silent.mp4
```

<br>

---

## 8. Step 4 — Add the Soundtrack

All four inference videos use the **same soundtrack**.

This is intentional: because the videos are used to visually compare the four models, the soundtrack should remain constant and should not introduce an additional experimental variable.

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

> Confirm the exact filename under `assets/audio/` before running the command.

The resulting files are:

```text
reports/demo_videos/
├── exp1_with_audio.mp4
├── exp2_with_audio.mp4
├── exp3_with_audio.mp4
└── exp4_with_audio.mp4
```

<br>

---

## 9. Step 5 — Create the Final Demo Videos

Create the `demo/` directory:

```bash
mkdir -p demo
```

Copy the final videos using descriptive filenames.

The filenames intentionally include the **Demo number**, **inference purpose**, **experiment**, **model**, and relevant configuration. Since GitHub displays the video filename above the embedded player, this naming convention also serves as the visual title of each demo.

```bash
cp reports/demo_videos/exp1_with_audio.mp4 \
  "demo/🎥 Demo 1 — Inference — Helipad Detection · exp1 · YOLOv8n · 60 epochs.mp4"

cp reports/demo_videos/exp2_with_audio.mp4 \
  "demo/🎥 Demo 2 — Inference — Helipad Detection · exp2 · YOLOv8n · 100 epochs.mp4"

cp reports/demo_videos/exp3_with_audio.mp4 \
  "demo/🎥 Demo 3 — Inference — Helipad Detection · exp3 · YOLOv8n · 100 epochs · Augmented Dataset.mp4"

cp reports/demo_videos/exp4_with_audio.mp4 \
  "demo/🎥 Demo 4 — Inference — Helipad Detection · exp4 · YOLO11n · 100 epochs.mp4"
```

Verify the final files:

```bash
ls -lh demo/*.mp4
```

The four files should now be:

```text
demo/
├── 🎥 Demo 1 — Inference — Helipad Detection · exp1 · YOLOv8n · 60 epochs.mp4
├── 🎥 Demo 2 — Inference — Helipad Detection · exp2 · YOLOv8n · 100 epochs.mp4
├── 🎥 Demo 3 — Inference — Helipad Detection · exp3 · YOLOv8n · 100 epochs · Augmented Dataset.mp4
└── 🎥 Demo 4 — Inference — Helipad Detection · exp4 · YOLO11n · 100 epochs.mp4
```

<br>

---

## 10. Experiment Captions

| Demo | Experiment | Description |
|---|---|---|
| **Demo 1** | `exp1` | **YOLOv8n · 60 epochs** — high precision on the curated benchmark, but lower coverage of helipads observed under field conditions. |
| **Demo 2** | `exp2` | **YOLOv8n · 100 epochs** — reference model, with the best observed generalization under field conditions. |
| **Demo 3** | `exp3` | **YOLOv8n · 100 epochs · Augmented Dataset** — higher recall, with intermediate field performance. |
| **Demo 4** | `exp4` | **YOLO11n · 100 epochs** — same experimental base as `exp2`, using a newer architecture, but without outperforming `exp2` in the field evaluation. |

> Keep these descriptions consistent with the results reported in the project's final experimental analysis.

<br>

---

## 11. Demo 5 — Automated Helipad Scraping

**Demo 5** is independent from the four model inference demonstrations.

It presents the **automated collection of helipad coordinates** using Selenium and `helipad_bot.py`.

Therefore, it does **not** use the inference pipeline described in Steps 5–9.

The purpose of Demo 5 is to document the geospatial data acquisition stage of the project.

### Add the Soundtrack

```bash
cd ~/Desktop/3-MAINproject-ai-ml-yolo-helipad_detector

SCRAPING_VIDEO="demo/🚁Automated Helipad Scraping Demo.mp4"
SCRAPING_AUDIO="assets/audio/feel-good_nina-simone_house remix.mp3"

ffmpeg -y \
  -i "$SCRAPING_VIDEO" \
  -i "$SCRAPING_AUDIO" \
  -c:v copy \
  -c:a aac \
  -shortest \
  "demo/🎥 Demo 5 — Automated Helipad Scraping · Selenium · Coordinate Collection.mp4"
```

This creates a new version of the video while preserving the original scraping demo.

The final directory will therefore contain:

```text
demo/
├── 🎥 Demo 1 — Inference — Helipad Detection · exp1 · YOLOv8n · 60 epochs.mp4
├── 🎥 Demo 2 — Inference — Helipad Detection · exp2 · YOLOv8n · 100 epochs.mp4
├── 🎥 Demo 3 — Inference — Helipad Detection · exp3 · YOLOv8n · 100 epochs · Augmented Dataset.mp4
├── 🎥 Demo 4 — Inference — Helipad Detection · exp4 · YOLO11n · 100 epochs.mp4
└── 🎥 Demo 5 — Automated Helipad Scraping · Selenium · Coordinate Collection.mp4
```

> [!TIP]
> If the original scraping video already contains narration or another audio track, the command above replaces the existing audio. To preserve and mix both audio sources, use `amix`.

<br>

---

## 12. Clean Up Intermediate Files

After verifying all five final videos, the intermediate files can be removed:

```bash
rm -rf reports/demo_frames
rm -rf reports/demo_src
rm -f reports/demo_videos/*_silent.mp4
```

The final videos under `demo/` are preserved.

> **Do not run this cleanup before verifying the final videos.**

<br>

---

## 13. Final Output

After completing the complete workflow, the `demo/` directory should contain exactly five final demonstrations:

```text
demo/
├── 🎥 Demo 1 — Inference — Helipad Detection · exp1 · YOLOv8n · 60 epochs.mp4
├── 🎥 Demo 2 — Inference — Helipad Detection · exp2 · YOLOv8n · 100 epochs.mp4
├── 🎥 Demo 3 — Inference — Helipad Detection · exp3 · YOLOv8n · 100 epochs · Augmented Dataset.mp4
├── 🎥 Demo 4 — Inference — Helipad Detection · exp4 · YOLO11n · 100 epochs.mp4
└── 🎥 Demo 5 — Automated Helipad Scraping · Selenium · Coordinate Collection.mp4
```

### Comparability Criterion

For **Demo 1–4**, the validity of the visual comparison depends on keeping three elements constant:

**same input images · same order · same soundtrack**

The experimental variable that changes across the four inference demonstrations is the **model used for inference**.

> **Same scene. Different model.**

**Demo 5 is intentionally excluded from this model comparison**, because it documents automated data collection rather than model inference.
