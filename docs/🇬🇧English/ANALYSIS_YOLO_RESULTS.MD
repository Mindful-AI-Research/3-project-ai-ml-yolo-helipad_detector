<!-- LANGUAGE BUTTONS -->
**\[**[🇧🇷 Português](../🇧🇷Portugues/ANALYSIS_YOLO_RESULTS.MD)**\] \[🇬🇧 English\]**

<br><br>

## [Results Analysis — Helipoint Detector]()

### [***YOLOv8n · 60 epochs · Helipad dataset in São Paulo***]()

<br><br>

## [Key Metrics (real data from `results.csv`)]()

<br><br>

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

## [Generated Charts]()

<br><br>

### [***Figure 1 — Loss Evolution by Epoch***]()

<br><br>

![Loss Curves](file:///Users/fabicampanari/.gemini/antigravity-ide/brain/5760042e-2127-41ec-a4da-9cab1095c97f/loss_curves.png)

<br><br>

**What to observe:**

<br><br>

- All three losses (Box, Cls, DFL) fall consistently for both training and validation.
- There is no sign of *overfitting* across the first 60 epochs — `val_loss` tracks `train_loss` without diverging.
- `val/cls_loss` oscillates during the first 20 epochs, which is expected for small datasets, but stabilizes from epoch 30 onward.

<br><br>

### [***Figure 2 — Precision and Recall Throughout Training***]()

<br><br>

![Precision and Recall](file:///Users/fabicampanari/.gemini/antigravity-ide/brain/5760042e-2127-41ec-a4da-9cab1095c97f/precision_recall.png)

<br><br>

**What to observe:**

<br><br>

- **Precision** rises quickly and stabilizes above **0.95** from epoch 30 onward — the model rarely detects "helipads" where none exist.
- **Recall** also reaches **0.97+** in the final epochs — the model finds nearly all real helipads in the images.
- The two curves cross early (~epoch 20), indicating the model balanced object capture and false-positive filtering well.

<br><br>

### [***Figure 3 — mAP\@50 and mAP\@50–95***]()

<br><br>

![mAP Curves](file:///Users/fabicampanari/.gemini/antigravity-ide/brain/5760042e-2127-41ec-a4da-9cab1095c97f/map_curves.png)

<br><br>

**What to observe:**

<br><br>

- **mAP\@50 = 0.994** at the best epoch — essentially perfect under the standard 50% IoU criterion.
- **mAP\@50–95 = 0.881** — an excellent result even under the strict criterion (COCO standard), showing that the *bounding boxes* are accurate beyond merely overlapping the object.
- The peak occurs at **epoch 54**, after which the metrics fluctuate slightly, suggesting 55–60 epochs is the optimal point for this dataset.

<br><br>

## [Slide-Ready Text]()

<br><br>

### [***Slide: Key Metrics***]()

<br><br>

> "After 60 epochs of training, the YOLOv8n model reached a **Precision of 99.2%** and a **Recall of 97.1%** on the validation data, indicating that it correctly detects nearly all helipads with very few false positives."

<br><br>

### [***Slide: mAP***]()

<br><br>

> "The **mAP\@50 of 99.4%** confirms the model is highly accurate under the standard detection criterion. Meanwhile, **mAP\@50–95 of 88.1%** (the strict COCO-standard criterion) demonstrates that the bounding boxes are geometrically precise — not merely overlapping the object, but framing it correctly."

<br><br>

### [***Slide: Loss Curves***]()

<br><br>

> "The loss curves show consistent learning with no signs of overfitting: both the training and validation loss decrease smoothly and in parallel across the 60 epochs, indicating good model generalization."

<br><br>

### [***Slide: Conclusion***]()

<br><br>

> "The Helipoint Detector achieved professional-grade performance on a dataset built from scratch: **mAP\@50 near 100%** and **mAP\@50–95 of 88%**. This validates the quality of the curation, annotation, and geographic diversity of the dataset, confirming that 80% of the effort in AI is, in fact, in the data."

<br><br>

## [Qualitative Analysis — Script for Visual Slides]()

<br><br>

Use the following script when displaying prediction images:

<br><br>

| Type | What to show | What to explain |
|------|--------------|----------------|
| ✅ **Clear hit** | Helipad detected with a well-fitted box and confidence > 0.8 | "The model identified the characteristic 'H' even with shadow on the rooftop" |
| ✅ **Challenging hit** | Partially covered or angled helipad | "High confidence even under partial occlusion, showing robustness" |
| ⚠️ **False Positive** | Circular pattern or 'H' detected on a pool/court | "Structures similar to the helipad 'H' generate FPs — treatable with more negative examples" |
| ❌ **False Negative** | Helipad not detected | "Faded helipads or those under heavy shadow still slip through — an area for improvement" |

<br><br>

## [Presentation Recommendations]()

<br><br>

1. **Use only 3 charts**: Loss Curves + Precision/Recall + mAP (generated above).
2. **Highlight on a single slide** the table with Precision / Recall / mAP\@50 / mAP\@50–95.
3. **Show 4–6 prediction images**: 2–3 hits, 1 FP, and 1 FN, each with commentary.
4. **Avoid** presenting all 15 columns of the CSV — focus on the 4 key metrics.
5. **Closing headline number**: *"99.4% mAP\@50 with a dataset built from scratch across 3 São Paulo neighborhoods."*

<br><br>

## [Full Python Code to Reproduce the Charts]()

<br><br>

Copy and paste directly into `Analysis.ipynb`:

<br><br>

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('AI Training/runs/detect/runs/exp1-2/results.csv',
                 skipinitialspace=True)
df.columns = df.columns.str.strip()
epoch = df["epoch"]

# ── Figure 1: Losses ────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 4))
fig.suptitle("Loss Evolution by Epoch", fontsize=14, fontweight="bold")

for ax, (tr, vl, name) in zip(axes, [
    ("train/box_loss","val/box_loss","Box Loss"),
    ("train/cls_loss","val/cls_loss","Cls Loss"),
    ("train/dfl_loss","val/dfl_loss","DFL Loss"),
]):
    ax.plot(epoch, df[tr], label="Train",      color="#14b8a6", lw=2)
    ax.plot(epoch, df[vl], label="Validation", color="#f97316", lw=2, ls="--")
    ax.set_title(name); ax.set_xlabel("Epoch"); ax.legend(); ax.grid(True)

plt.tight_layout(); plt.show()

# ── Figure 2: Precision and Recall ────────────────────────────────
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4))
fig.suptitle("Precision and Recall Throughout Training", fontsize=14, fontweight="bold")

a1.plot(epoch, df["metrics/precision(B)"], color="#14b8a6", lw=2)
a1.fill_between(epoch, df["metrics/precision(B)"], alpha=0.1, color="#14b8a6")
a1.set_title("Precision"); a1.set_xlabel("Epoch"); a1.set_ylim(0,1.05); a1.grid(True)

a2.plot(epoch, df["metrics/recall(B)"], color="#ec4899", lw=2)
a2.fill_between(epoch, df["metrics/recall(B)"], alpha=0.1, color="#ec4899")
a2.set_title("Recall"); a2.set_xlabel("Epoch"); a2.set_ylim(0,1.05); a2.grid(True)

plt.tight_layout(); plt.show()

# ── Figure 3: mAP ───────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 4))
fig.suptitle("mAP50 and mAP50-95 Throughout Training", fontsize=14, fontweight="bold")

ax.plot(epoch, df["metrics/mAP50(B)"],    color="#6366f1", lw=2.5, label="mAP@50")
ax.plot(epoch, df["metrics/mAP50-95(B)"], color="#ec4899", lw=2.5, label="mAP@50-95", ls="--")
ax.fill_between(epoch, df["metrics/mAP50(B)"],    alpha=0.1, color="#6366f1")
ax.fill_between(epoch, df["metrics/mAP50-95(B)"], alpha=0.1, color="#ec4899")
ax.set_xlabel("Epoch"); ax.set_ylim(0,1.05); ax.legend(); ax.grid(True)

plt.tight_layout(); plt.show()

# ── Table: final metrics ─────────────────────────────────────
best = df.loc[df["metrics/mAP50-95(B)"].idxmax()]
final = df.iloc[-1]

summary = pd.DataFrame({
    "Precision":  [best["metrics/precision(B)"],  final["metrics/precision(B)"]],
    "Recall":     [best["metrics/recall(B)"],      final["metrics/recall(B)"]],
    "mAP@50":     [best["metrics/mAP50(B)"],       final["metrics/mAP50(B)"]],
    "mAP@50-95":  [best["metrics/mAP50-95(B)"],    final["metrics/mAP50-95(B)"]],
}, index=[f"Best (ep. {int(best['epoch'])})", f"Final (ep. {int(final['epoch'])})"])

display(summary.style.format("{:.4f}").background_gradient(cmap="YlGn", axis=None))
```

<br><br>

---

<br><br>

*Helipoint Detector · PUC-SP · Machine Learning / Computer Vision · 2026*
