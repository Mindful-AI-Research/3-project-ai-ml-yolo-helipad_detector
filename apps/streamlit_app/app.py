import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import zipfile
from datetime import datetime
import math
import requests
from pathlib import Path
import tempfile
import shutil

# ========================= PAGE CONFIG =========================
st.set_page_config(
    page_title="Helipad Detector • São Paulo",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-title {font-size: 42px !important; font-weight: bold; color: #1E3A8A; text-align: center;}
    .subtitle {text-align: center; color: #64748B; font-size: 18px; margin-bottom: 30px;}
    .result-card {background-color: #f8fafc; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0;}
    .metric-card {background-color: #f8fafc; padding: 18px; border-radius: 14px; border: 1px solid #e2e8f0; text-align: center;}
    .sample-btn > button {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.75em 1.4em;
        border-radius: 10px;
        box-shadow: 0 4px 14px rgba(30, 58, 138, 0.35);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .sample-btn > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(30, 58, 138, 0.45);
    }
    </style>
""", unsafe_allow_html=True)

# ========================= RESPONSIBLE-USE NOTICE =========================
# A detection is only a visual, image-based result. It is never evidence that a
# site is safe, certified, active, available for landing or approved for any use.
DISCLAIMER = (
    "Automated image-based visual detection, subject to errors and not equivalent to "
    "operational, legal, safety or aeronautical validation."
)

# ========================= AUTOMATIC MODEL DISCOVERY =========================
# Instead of hardcoding "exp1"/"exp2" in the code, the app scans the runs folder
# and lists any experiment that has a ready best.pt. This way, running a new
# experiment (exp2, exp3...) requires no changes to this file.
MODEL_ROOT = Path("artifacts/runs/detect")
SAMPLES_DIR = Path("data/samples")


def discover_models() -> dict[str, Path]:
    """Returns {friendly_label: path_to_best.pt} for each experiment found."""
    found = {}
    if MODEL_ROOT.exists():
        for exp_dir in sorted(MODEL_ROOT.iterdir()):
            weights = exp_dir / "weights" / "best.pt"
            if weights.exists():
                found[f"{exp_dir.name} ({weights.stat().st_size // 1_000_000} MB)"] = weights
    return found


@st.cache_resource(show_spinner="Loading model...")
def load_model(model_path: str) -> YOLO:
    return YOLO(model_path)


@st.cache_data(show_spinner=False)
def load_experiment_metrics() -> pd.DataFrame:
    """Scans artifacts/runs/detect/*/results.csv and builds a comparison table
    with the best epoch of each experiment found (today: exp1; exp2 shows up
    on its own as soon as it exists, no code changes needed)."""
    rows = []
    if not MODEL_ROOT.exists():
        return pd.DataFrame()

    for exp_dir in sorted(MODEL_ROOT.iterdir()):
        csv_path = exp_dir / "results.csv"
        if not csv_path.exists():
            continue
        try:
            df = pd.read_csv(csv_path)
            df.columns = df.columns.str.strip()
            best = df.loc[df["metrics/mAP50-95(B)"].idxmax()]
            rows.append({
                "Experiment": exp_dir.name,
                "Best Epoch": int(best["epoch"]),
                "Total Epochs": int(df["epoch"].max()),
                "Precision": round(float(best["metrics/precision(B)"]), 4),
                "Recall": round(float(best["metrics/recall(B)"]), 4),
                "mAP@50": round(float(best["metrics/mAP50(B)"]), 4),
                "mAP@50-95": round(float(best["metrics/mAP50-95(B)"]), 4),
            })
        except Exception:
            continue

    return pd.DataFrame(rows)


def get_selected_model() -> YOLO:
    label = st.session_state.get("model_choice", next(iter(MODEL_OPTIONS)))
    return load_model(str(MODEL_OPTIONS[label]))


MODEL_OPTIONS = discover_models()

# ========================= SIDEBAR: MODEL SELECTION =========================
with st.sidebar:
    st.markdown("### ⚙️ Model")
    if not MODEL_OPTIONS:
        st.error(
            "No model found at `artifacts/runs/detect/*/weights/best.pt`. "
            "Train at least one experiment before running the app."
        )
        st.stop()

    st.selectbox(
        "Choose the trained experiment",
        options=list(MODEL_OPTIONS.keys()),
        key="model_choice",
        help="Every folder under artifacts/runs/detect/ with a ready best.pt shows up here "
             "automatically — including future experiments, no app edits needed."
    )
    conf_threshold = st.slider(
        "Minimum detection confidence", min_value=0.05, max_value=0.95, value=0.25, step=0.05
    )
    st.caption(DISCLAIMER)

# ========================= TILE HELPERS =========================
def deg2tile(lat, lon, z):
    n = 2.0 ** z
    x = int((lon + 180.0) / 360.0 * n)
    lat_rad = math.radians(lat)
    y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return x, y

def download_tile(z, x, y, temp_dir):
    url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    headers = {"User-Agent": "Helipad-Detector-PUC-SP/1.0"}
    path = temp_dir / f"tile_z{z}_x{x}_y{y}.jpg"

    if path.exists():
        return path

    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200 and len(r.content) > 2000:
            path.write_bytes(r.content)
            return path
    except:
        pass
    return None

# ========================= DETECTION =========================
def detect_helipad(image, model: YOLO, conf: float):
    result = model.predict(source=image, conf=conf, verbose=False)[0]
    plotted = result.plot()[:, :, ::-1]  # BGR -> RGB
    return plotted, len(result.boxes) > 0

# ========================= INTERFACE =========================
st.markdown('<h1 class="main-title">🚁 Helipad Detection</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI + Satellite Imagery • São Paulo</p>', unsafe_allow_html=True)
st.caption(f"Active model: **{st.session_state.get('model_choice', list(MODEL_OPTIONS)[0])}**")
st.info(f"ℹ️ {DISCLAIMER}")

model = get_selected_model()

# ========================= METRICS DASHBOARD =========================
metrics_df = load_experiment_metrics()

with st.expander("📊 Experiment Metrics", expanded=True):
    if metrics_df.empty:
        st.info("No `results.csv` found yet under `artifacts/runs/detect/*/`.")
    else:
        n_exp = len(metrics_df)
        cols = st.columns(n_exp) if n_exp <= 4 else [st.container()]

        for i, row in metrics_df.iterrows():
            target = cols[i] if n_exp <= 4 else st
            with target:
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="margin:0 0 8px 0;">{row['Experiment']}</h4>
                    <p style="margin:2px 0; color:#64748B; font-size:13px;">
                        Best epoch: {row['Best Epoch']} / {row['Total Epochs']}
                    </p>
                    <p style="margin:6px 0; font-size:22px; font-weight:700; color:#1E3A8A;">
                        {row['mAP@50-95']:.3f}
                    </p>
                    <p style="margin:0; color:#64748B; font-size:12px;">mAP@50-95</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("")
        st.dataframe(
            metrics_df.set_index("Experiment").style.format({
                "Precision": "{:.3f}", "Recall": "{:.3f}",
                "mAP@50": "{:.3f}", "mAP@50-95": "{:.3f}",
            }).background_gradient(cmap="Blues", subset=["mAP@50-95"]),
            use_container_width=True,
        )

        # The experiments are NOT a controlled comparison: exp1 and exp2 share the data
        # content (dataset version 2) but differ in author, environment and Ultralytics
        # version; exp3 uses a separately augmented fork; exp4 changes the architecture.
        # Differences below are shown as numbers only, without causal interpretation.
        if n_exp >= 2 and "exp1" in metrics_df["Experiment"].values:
            exp1_row = metrics_df[metrics_df["Experiment"] == "exp1"].iloc[0]
            for _, row in metrics_df.iterrows():
                if row["Experiment"] == "exp1":
                    continue
                delta = row["mAP@50-95"] - exp1_row["mAP@50-95"]
                st.caption(f"{row['Experiment']} vs. exp1 on mAP@50-95: Δ {delta:+.4f}")

        st.warning(
            "These experiments are not a controlled comparison (author, environment, "
            "Ultralytics version and dataset version differ between runs). Small differences "
            "on a 226-image dataset are within expected noise and should not be attributed "
            "to a single factor such as the number of epochs."
        )

with st.expander("🧬 Data lineage & limitations", expanded=False):
    st.markdown(
        """
- **Annotated dataset (version 2):** 226 images — 178 train / 34 validation / 14 test. Version 2 has no data augmentation; only the exp3 fork does (Ultralytics 8.4.98, like exp2).
- **Labels:** mostly polygons (170 of 178 training label files and all validation/test files), converted to boxes for detection training. Three training label files mix polygons and boxes and are flagged by Ultralytics 8.4.163.
- **Field run:** 7,943 tiles in the production run (10 neighborhoods); the comparison set has 7,767 region × tile pairs and 5,540 distinct tiles.
- **Overlap:** 125 of the 225 annotated images with coordinates are copies of field tiles (2.3% of the 5,540 distinct tiles), so the field run is not fully independent of the annotated set. See `reports/lineage_audit/`.
- **Detection rate is not precision or recall:** field detection rates have no ground-truth labels behind them.
        """
    )
    st.caption(DISCLAIMER)

tab1, tab2, tab3 = st.tabs(["📤 Upload Image", "🔎 Search by Region (Satellite)", "🖼️ Sample Images"])

# ====================== TAB 1: Upload ======================
with tab1:
    images = st.file_uploader("Upload aerial images",
                               type=["jpg", "jpeg", "png"],
                               accept_multiple_files=True, max_upload_size=10, help="Satellite or drone images with good resolution, as close to the target as possible, are recommended.")

    if images:
        for idx, image_file in enumerate(images):
            col1, col2 = st.columns(2)
            original = Image.open(image_file)

            with col1:
                st.image(original, caption="Original", use_container_width=True)

            with col2:
                result_img, has_helipad = detect_helipad(original, model, conf_threshold)
                st.image(result_img, caption="Detection", use_container_width=True)
                if has_helipad:
                    st.success("✅ Possible helipad detected (visual detection only — human review required).")
                else:
                    st.warning("No helipad detected.")

# ====================== TAB 2: Bounding Box Search ======================
with tab2:
    st.subheader("🔎 Search for Helipads in a Region")
    st.caption("Use the coordinates of the desired region (e.g. Downtown São Paulo)")
    st.caption(
        "Results are visual detections on satellite tiles, not a validated inventory of helipads. "
        + DISCLAIMER
    )

    col_a, col_b = st.columns(2)
    with col_a:
        lon_min = st.number_input("Min Longitude", value=-46.6583, format="%.6f")
        lat_min = st.number_input("Min Latitude", value=-23.5827, format="%.6f")
    with col_b:
        lon_max = st.number_input("Max Longitude", value=-46.6311, format="%.6f")
        lat_max = st.number_input("Max Latitude", value=-23.5536, format="%.6f")

    zoom = st.slider("Zoom (recommended: 19)", 16, 20, 19)
    search_btn = st.button("🚀 Search and Analyze Region", type="primary", use_container_width=True)

    if search_btn:
        with st.spinner("Downloading satellite tiles and analyzing with AI... (this may take a while)"):
            temp_dir = Path(tempfile.mkdtemp())

            try:
                x_min, y_max = deg2tile(lat_min, lon_min, zoom)
                x_max, y_min = deg2tile(lat_max, lon_max, zoom)

                jobs = [(zoom, x, y) for x in range(x_min, x_max+1) for y in range(y_min, y_max+1)]

                st.info(f"Processing **{len(jobs)}** satellite tiles...")
                progress = st.progress(0, "Progress: ")

                detected_tiles = []

                for i, (z, x, y) in enumerate(jobs):
                    progress.progress((i+1)/len(jobs), f"Progress: {i+1}/{len(jobs)} tiles")

                    tile_path = download_tile(z, x, y, temp_dir)
                    if not tile_path:
                        continue

                    img = Image.open(tile_path)
                    result_img, has_detection = detect_helipad(img, model, conf_threshold)

                    if has_detection:
                        detected_tiles.append((result_img, f"tile_z{z}_x{x}_y{y}.jpg"))

                if detected_tiles:
                    st.success(f"🎯 **{len(detected_tiles)} tile(s) with possible helipad detections** in the region (human review required).")

                    cols = st.columns(3)
                    for idx, (img_array, filename) in enumerate(detected_tiles):
                        with cols[idx % 3]:
                            st.image(img_array, caption=filename, use_container_width=True)

                            buf = io.BytesIO()
                            Image.fromarray(img_array).save(buf, format="PNG")
                            buf.seek(0)

                            st.download_button(
                                label="⬇️ Download",
                                data=buf,
                                file_name=filename.replace(".jpg", "_detected.png"),
                                mime="image/png",
                                key=f"dl_{idx}"
                            )

                    if len(detected_tiles) > 1:
                        st.info("Use the buttons above to download individually.")
                else:
                    st.warning("No helipad detected in this region.")

            finally:
                shutil.rmtree(temp_dir, ignore_errors=True)

# ====================== TAB 3: Sample Images ======================
with tab3:
    st.subheader("🖼️ Test with Sample Images")
    st.caption(
        "Don't have your own image handy? Use the satellite images already included in the "
        f"repository at `{SAMPLES_DIR}/` to test the detector right away."
    )

    sample_files = []
    if SAMPLES_DIR.exists():
        sample_files = sorted(
            [p for p in SAMPLES_DIR.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png")]
        )

    if not sample_files:
        st.info(
            f"No sample images found at `{SAMPLES_DIR}/`. "
            "If you're running this app outside the cloned repository, download the sample "
            "images directly from GitHub and place them in that folder."
        )
    else:
        st.write(f"**{len(sample_files)} sample image(s) available.**")

        preview_cols = st.columns(min(len(sample_files), 6))
        for i, path in enumerate(sample_files[:6]):
            with preview_cols[i % len(preview_cols)]:
                st.image(str(path), use_container_width=True, caption=path.name)
        if len(sample_files) > 6:
            st.caption(f"...and {len(sample_files) - 6} more image(s).")

        col_run, col_dl = st.columns(2)

        with col_run:
            st.markdown('<div class="sample-btn">', unsafe_allow_html=True)
            run_samples = st.button(
                "🚀 Run detection on all sample images",
                use_container_width=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

        with col_dl:
            # Build the ZIP on demand, only when the user requests the download —
            # useful for anyone running the hosted app without having cloned the repo.
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                for path in sample_files:
                    zf.write(path, arcname=path.name)
            zip_buffer.seek(0)

            st.download_button(
                "⬇️ Download all sample images (.zip)",
                data=zip_buffer,
                file_name="helipad_sample_images.zip",
                mime="application/zip",
                use_container_width=True,
            )

        if run_samples:
            with st.spinner(f"Analyzing {len(sample_files)} sample image(s)..."):
                progress = st.progress(0, "Progress:")
                result_cols = st.columns(3)
                hits = 0

                for i, path in enumerate(sample_files):
                    progress.progress((i + 1) / len(sample_files), f"Progress: {i+1}/{len(sample_files)}")
                    img = Image.open(path)
                    result_img, has_detection = detect_helipad(img, model, conf_threshold)
                    if has_detection:
                        hits += 1
                    with result_cols[i % 3]:
                        st.image(result_img, caption=path.name, use_container_width=True)
                        if has_detection:
                            st.success("✅ Possible detection")
                        else:
                            st.warning("No detection")

                st.info(f"**Summary:** possible helipad detected in {hits} of {len(sample_files)} sample image(s).")

# Footer
st.markdown("---")

st.markdown("""
<p style="text-align:center; color:rgba(255,255,255,0.30); margin:0;">
🚁 <em>Finding hidden H's in the Concrete Jungle</em>
</p>

<p style="text-align:center; color:rgba(255,255,255,0.35); margin:4px 0;">
One rooftop at a time. ⚡
</p>

<p style="text-align:center; color:rgba(255,255,255,0.30); margin:6px 0 0 0; font-size:12px;">
SÃO PAULO • YOLOv8 / YOLO11 • ESRI WORLD IMAGERY
</p>
""", unsafe_allow_html=True)
