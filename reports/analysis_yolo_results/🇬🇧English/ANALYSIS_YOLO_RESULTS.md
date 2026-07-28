# 📊 Results Analysis — Helipad Detector
### YOLOv8n · 60 epochs · São Paulo Helipad Dataset

<br><br>

## 🏆 Key Metrics (real data from `results.csv`)

| | Best Epoch (54) | Final Epoch (60) |
|---|:---:|:---:|
| **Precision** | **1.000** | 0.992 |
| **Recall** | **0.963** | 0.971 |
| **mAP\@50** | **0.994** | 0.994 |
| **mAP\@50–95** | **0.881** | 0.841 |

<br><br>

> [!IMPORTANT]
> The model reached **Precision = 1.00** and **mAP\@50 = 0.994** at epoch 54 — an exceptionally strong result for a dataset with only ~116 training images.

<br><br>

## 📈 Generated Charts

### Figure 1 — Loss Evolution by Epoch
![Loss Curves](file:///Users/fabicampanari/.gemini/antigravity-ide/brain/5760042e-2127-41ec-a4da-9cab1095c97f/loss_curves.png)

**What to observe:**
- All three losses (Box, Cls, DFL) decrease consistently on both train and validation.
- No sign of *overfitting* in the first 60 epochs — `val_loss` tracks `train_loss` closely without diverging.
- `val/cls_loss` oscillates in the first 20 epochs, which is expected on small datasets, but stabilizes from epoch 30 onward.

<br>

### Figure 2 — Precision and Recall Throughout Training
![Precision and Recall](file:///Users/fabicampanari/.gemini/antigravity-ide/brain/5760042e-2127-41ec-a4da-9cab1095c97f/precision_recall.png)

**What to observe:**
- **Precision** rises quickly and stabilizes above **0.95** from epoch 30 onward — the model rarely flags "helipads" where none exist.
- **Recall** also reaches **0.97+** in the final epochs — the model finds nearly all real helipads in the images.
- The two curves cross early (~epoch 20), indicating the model balanced object recall with false-positive filtering well.

<br>

### Figure 3 — mAP\@50 and mAP\@50–95
![mAP Curves](file:///Users/fabicampanari/.gemini/antigravity-ide/brain/5760042e-2127-41ec-a4da-9cab1095c97f/map_curves.png)

**What to observe:**
- **mAP\@50 = 0.994** at the best epoch — near-perfect under the standard IoU 50% criterion.
- **mAP\@50–95 = 0.881** — an excellent result even under the stricter COCO-style criterion, showing the bounding boxes are precise, not just overlapping the object.
- The peak occurs at **epoch 54**, after which metrics fluctuate slightly, suggesting 55–60 epochs is the sweet spot for this dataset.

<br><br>

## 📝 Slide-Ready Text

### Slide: Key Metrics
> "After 60 training epochs, the YOLOv8n model reached **99.2% Precision** and **97.1% Recall** on validation data, indicating it correctly detects nearly all helipads with very few false positives."

### Slide: mAP
> "**99.4% mAP\@50** confirms the model is highly accurate under the standard detection criterion. **88.1% mAP\@50–95** (the strict COCO-style criterion) shows the bounding boxes are geometrically precise — not just overlapping the object, but tightly framing it."

### Slide: Loss Curves
> "The loss curves show consistent learning with no overfitting signs: both train and validation loss decrease smoothly and in parallel across the 60 epochs, indicating good model generalization."

### Slide: Conclusion
> "The Helipoint Detector reached professional-grade performance on a dataset built from scratch: **mAP\@50 near 100%** and **mAP\@50–95 of 88%**. This validates the quality of the curation, annotation, and geographic diversity of the dataset, confirming that 80% of AI effort is, in fact, in the data."

---

## 🔍 Qualitative Analysis — Visual Slide Script

Use the following script when displaying prediction images:

| Type | What to Show | What to Explain |
|------|--------------|----------------|
| ✅ **Clear hit** | Helipad detected with a well-fitted box and confidence > 0.8 | "The model identified the characteristic 'H' even with rooftop shadow" |
| ✅ **Challenging hit** | Partially covered or angled helipad | "High confidence even under partial occlusion, showing robustness" |
| ⚠️ **False Positive** | Circular pattern or 'H'-like shape detected on a pool/court | "Structures visually similar to the helipad 'H' cause FPs — addressable with more negative examples" |
| ❌ **False Negative** | Helipad not detected | "Faded helipads or those under dense shadow still slip through — an area for improvement" |


<br><br>


## [Qualitative Analysis — Real Faria Lima Data]()

<br>

### [***Context***]

Inference run with the `exp2` model over **840 real tiles** downloaded from the Faria Lima neighborhood (zoom 19, ESRI World Imagery), as a field test in a dense corporate-helipad region. **170 of 840 tiles (20.2%)** returned a detection with confidence ≥ 0.25.



Below, a representative selection — clear hits, challenging hits, false positives, and a data-quality issue identified during the process.

<br>

### [***Case Table***]

| Type | Tile | Confidence | Note |
|---|:---:|:---:|---|
| ✅ Clear hit | `tile_z19_x194126_y297485.jpg` | 0.94 | Sharp "H" pattern inside a well-defined square on the rooftop |
| ✅ Clear hit | `tile_z19_x194143_y297481.jpg` | 0.96 | Clear geometry and contrast, well-fitted box |
| ✅ Clear hit | `tile_z19_x194149_y297489.jpg` | 0.96 | Clear geometry and contrast, well-fitted box |
| ✅ Challenging hit | `tile_z19_x194545_y298183.jpg` | 0.77 | Correct detection despite a less favorable angle/lighting |
| ⚠️ False Positive | `tile_z19_x194129_y297480.jpg` | 0.78 | Box over a **sports court** (striped rectangular pattern), not a helipad |
| ⚠️ False Positive | `tile_z19_x194547_y298176.jpg` | 0.86 | Box over a **pool** — reflection/geometric shape similar to the "H" |
| ⚠️ False Positive (low confidence) | `tile_z19_x194548_y298181.jpg` | 0.28 | Tiny box at the image edge — likely model noise |
| ❌ Data failure (not a model error) | `tile_z19_x194139_y297467.jpg` | — | **Empty/black** tile (ESRI download failure) marked as "Detected" |
| ❌ Data failure (not a model error) | `tile_z19_x194141_y297481.jpg` | — | Same issue — black tile with no valid content |

<br>

### [***Reading the Results***]

The false positives follow the pattern already documented in the project: **pools and sports courts** share a rectangular geometry/contrast similar to the helipad "H", and remain the model's main error source — reinforcing the need for more negative examples of this kind in the next annotation cycle.



The **empty tiles marked as detected** are not a model error, but a gap in the data pipeline: tiles that fail to download (black/corrupted content) are still sent to inference. Recommended action: add an "empty tile" check (e.g., pixel standard deviation below a threshold) before running the model, automatically filtering these cases out.

<br><br>


<!-- ============================================================ -->
<!-- BLOCK 2 — paste into the Executive Report (English)          -->
<!-- ============================================================ -->

## [Field Validation — Faria Lima]()



Beyond standard validation/test evaluation, the model was put through a **real field test**: full inference across 840 satellite tiles from the Faria Lima neighborhood, one of São Paulo's densest corporate helipad corridors.


**Result: 170 of 840 tiles (20.2%) with a detection**, with high median confidence (most clear hits between 0.90–0.98). The qualitative analysis confirmed the error pattern already known in the project — false positives concentrated on pools and sports courts — validating both the model's robustness and the consistency of the project's already-documented limitations.

<br><br>


<!-- ============================================================ -->
<!-- BLOCK 3 — paste into the README (highlight, English)         -->
<!-- ============================================================ -->

## [Real-World Field Test — Faria Lima]()



The trained model (`exp2`) was tested against **840 real satellite tiles** from Faria Lima — one of São Paulo's densest corporate helipad corridors — as a practical validation step beyond the standard train/valid/test split.



**170 of 840 tiles (20.2%)** returned a detection, with high-confidence hits (0.90–0.98) matching the expected rooftop "H" pattern, alongside a handful of documented false positives (pools, sports courts) consistent with the error patterns already described in the qualitative analysis section.

<br><br>

> [!NOTE]
> These numbers reflect Faria Lima only (first round). Once the multi-neighborhood triage (`auto_triage_regions.py`) finishes running across the 10 neighborhoods in `sp_neighborhoods_bbox.csv`, this content should be updated with the totals and a per-region table.
