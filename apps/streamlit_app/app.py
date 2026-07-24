import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import streamlit.components.v1 as components
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

# ========================= AUTOMATIC MODEL DISCOVERY =========================
# Instead of hardcoding "exp1"/"exp2" in the code, the app scans the runs folder
# and lists any experiment that has a ready best.pt. This way, running a new
# experiment (exp2, exp3...) requires no changes to this file.
MODEL_ROOTS = [
    Path("artifacts/runs/detect"),        # plain convention (no doubled "runs")
    Path("artifacts/runs/runs/detect"),   # convention produced by the notebook's zip flow
]
SAMPLES_DIR = Path("data/samples")
COORDS_CSV = Path("src/geospatial/helipad_coordinates_bbox.csv")
SP_COORDS_CSV = Path("src/geospatial/sp_neighborhoods_bbox.csv")
EXEC_REPORT_EN = Path("reports/executive_analysis/helipoint_detector_performance_en.pdf")
EXEC_REPORT_PT = Path("reports/executive_analysis/helipoint_detector_performance_pt.pdf")
DATASET_RAR = Path("data/raw/helipad_dataset.rar")
KEPLER_HTML = Path("src/geospatial/keplergl_map_loaded.html")


def _all_exp_dirs():
    """Yields experiment directories across all MODEL_ROOTS candidates,
    de-duplicated by experiment name (first root that has a given name wins)."""
    seen = set()
    for root in MODEL_ROOTS:
        if not root.exists():
            continue
        for exp_dir in sorted(root.iterdir()):
            if exp_dir.is_dir() and exp_dir.name not in seen:
                seen.add(exp_dir.name)
                yield exp_dir


def discover_models() -> dict[str, Path]:
    """Returns {friendly_label: path_to_best.pt} for each experiment found,
    across any of MODEL_ROOTS."""
    found = {}
    for exp_dir in _all_exp_dirs():
        weights = exp_dir / "weights" / "best.pt"
        if weights.exists():
            found[f"{exp_dir.name} ({weights.stat().st_size // 1_000_000} MB)"] = weights
    return found


@st.cache_resource(show_spinner="Loading model...")
def load_model(model_path: str) -> YOLO:
    return YOLO(model_path)


def _find_results_csv(exp_dir: Path) -> Path | None:
    """results.csv naming isn't consistent across experiment folders in this
    repo (e.g. exp1 uses 'exp1_results.csv' instead of 'results.csv') — check
    a few known patterns instead of assuming one fixed name."""
    candidates = [
        exp_dir / "results.csv",
        exp_dir / f"{exp_dir.name}_results.csv",
    ]
    for c in candidates:
        if c.exists():
            return c
    # last resort: any *_results.csv or results*.csv in the folder
    matches = list(exp_dir.glob("*results*.csv"))
    return matches[0] if matches else None


@st.cache_data(show_spinner=False)
def load_experiment_metrics() -> pd.DataFrame:
    """Scans every experiment folder (across MODEL_ROOTS) for results.csv and
    builds a comparison table with the best epoch of each one found."""
    rows = []
    for exp_dir in _all_exp_dirs():
        csv_path = _find_results_csv(exp_dir)
        if csv_path is None:
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
                "_dir": str(exp_dir),
            })
        except Exception:
            continue

    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False)
def load_experiment_curves() -> dict[str, pd.DataFrame]:
    """Returns {experiment_name: full results.csv as DataFrame} for the
    per-epoch metric evolution chart, across any of MODEL_ROOTS."""
    curves = {}
    for exp_dir in _all_exp_dirs():
        csv_path = _find_results_csv(exp_dir)
        if csv_path is None:
            continue
        try:
            df = pd.read_csv(csv_path)
            df.columns = df.columns.str.strip()
            curves[exp_dir.name] = df
        except Exception:
            continue
    return curves


@st.cache_data(show_spinner=False)
def load_helipad_locations(csv_path: Path = COORDS_CSV) -> pd.DataFrame:
    """Reads a helipad-coordinates CSV (same schema as helipad_coordinates_bbox.csv)
    and computes the center point (lat, lon) of each bounding box, for the map view."""
    if not csv_path.exists():
        return pd.DataFrame()

    def parse_center(raw: str):
        parts = str(raw).replace(",", " ").split()
        try:
            lon_min, lat_min, lon_max, lat_max = (float(p) for p in parts[:4])
            return (lat_min + lat_max) / 2, (lon_min + lon_max) / 2
        except Exception:
            return None, None

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        return pd.DataFrame()

    if "Coordenadas da Bounding Box" not in df.columns:
        return pd.DataFrame()

    centers = df["Coordenadas da Bounding Box"].apply(parse_center)
    df["lat"] = centers.apply(lambda t: t[0])
    df["lon"] = centers.apply(lambda t: t[1])
    return df.dropna(subset=["lat", "lon"])


def get_selected_model():
    if not MODEL_OPTIONS:
        return None
    label = st.session_state.get("model_choice") or next(iter(MODEL_OPTIONS))
    return load_model(str(MODEL_OPTIONS[label]))


MODEL_OPTIONS = discover_models()

# ========================= SIDEBAR: MODEL SELECTION =========================
with st.sidebar:
    st.markdown("### ⚙️ Model")
    if not MODEL_OPTIONS:
        st.warning(
            "No trained model found at `artifacts/runs/detect/*/weights/best.pt` (or `artifacts/runs/runs/detect/*/...`) yet. "
            "Detection features (Upload, Search by Region, Sample Images) are disabled until "
            "one is available — but the Map, Pipeline & Governance, and Downloads tabs below "
            "don't need a model and work right now."
        )
        st.session_state["model_choice"] = None
        conf_threshold = 0.25
    else:
        st.selectbox(
            "Choose the trained experiment",
            options=list(MODEL_OPTIONS.keys()),
            key="model_choice",
            help="Every folder under artifacts/runs/detect/ (or artifacts/runs/runs/detect/) with a ready best.pt shows up here "
                 "automatically — including future experiments, no app edits needed."
        )
        conf_threshold = st.slider(
            "Minimum detection confidence", min_value=0.05, max_value=0.95, value=0.25, step=0.05
        )

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
if MODEL_OPTIONS:
    st.caption(f"Active model: **{st.session_state.get('model_choice') or list(MODEL_OPTIONS)[0]}**")
else:
    st.caption("Active model: _none yet — detection tabs disabled_")

model = get_selected_model()

# Load metrics data early (used by both the Downloads tab and the metrics
# panel at the bottom) — only the visual display moved, not the data load.
metrics_df = load_experiment_metrics()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📤 Upload Image", "🔎 Search by Region (Satellite)", "🖼️ Sample Images",
    "🗺️ Map", "📖 Pipeline & Governance", "⬇️ Downloads",
])

# ====================== TAB 1: Upload ======================
with tab1:
    if model is None:
        st.info("⚠️ No trained model yet — train exp1/exp2/exp3 and this tab will activate automatically.")
    else:
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
                        st.success("✅ Helipad detected!")
                    else:
                        st.warning("No helipad found.")

# ====================== TAB 2: Bounding Box Search ======================
with tab2:
    st.subheader("🔎 Search for Helipads in a Region")
    st.caption("Use the coordinates of the desired region (e.g. Downtown São Paulo)")

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
        if model is None:
            st.error("⚠️ No trained model yet — this feature needs a model to run detection.")
        else:
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
                    st.success(f"🎯 **{len(detected_tiles)} helipad(s) found** in the region!")

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
                    st.warning("No helipad was found in this region.")

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
            if model is None:
                st.error("⚠️ No trained model yet — this feature needs a model to run detection.")
            else:
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
                            st.success("✅ Detected")
                        else:
                            st.warning("No detection")

                st.info(f"**Summary:** helipad detected in {hits} of {len(sample_files)} sample image(s).")

# ====================== TAB 4: Interactive Map ======================
with tab4:
    st.subheader("🗺️ Helipad Locations — two layers")
    st.caption(
        "🟢 **São Paulo training neighborhoods** (region-level bounding boxes from "
        "`src/data_preparation/image_preprocessing.ipynb`) · "
        "🔵 **Discovery dataset** — helipad candidates found by "
        "`src/geospatial/helipad_scraper.py` across other Brazilian states."
    )

    sp_df = load_helipad_locations(SP_COORDS_CSV)
    other_df = load_helipad_locations(COORDS_CSV)

    if sp_df.empty and other_df.empty:
        st.info(
            f"No coordinates found at `{SP_COORDS_CSV}` or `{COORDS_CSV}`. "
            "See the Execution Guide to generate them."
        )
    else:
        lat_parts = [df["lat"] for df in (sp_df, other_df) if not df.empty]
        lon_parts = [df["lon"] for df in (sp_df, other_df) if not df.empty]
        center_lat = pd.concat(lat_parts).mean() if lat_parts else -23.5505  # fallback: São Paulo center
        center_lon = pd.concat(lon_parts).mean() if lon_parts else -46.6333

        fmap = folium.Map(location=[center_lat, center_lon], zoom_start=5, tiles="CartoDB positron")

        sp_layer = folium.FeatureGroup(name=f"🟢 São Paulo ({len(sp_df)})", show=True)
        for _, row in sp_df.iterrows():
            name = row.get("Nome do Bairro", "Unknown")
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=folium.Popup(f"<b>{name}</b><br>São Paulo training region", max_width=250),
                tooltip=name,
                icon=folium.Icon(color="green", icon="home"),
            ).add_to(sp_layer)
        sp_layer.add_to(fmap)

        other_layer = folium.FeatureGroup(name=f"🔵 Other states ({len(other_df)})", show=True)
        for _, row in other_df.iterrows():
            neighborhood = row.get("Nome do Bairro", "Unknown")
            timestamp = row.get("Carimbo de data/hora", "")
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=folium.Popup(f"<b>{neighborhood}</b><br>{timestamp}", max_width=250),
                tooltip=neighborhood,
                icon=folium.Icon(color="blue", icon="info-sign"),
            ).add_to(other_layer)
        other_layer.add_to(fmap)

        folium.LayerControl(collapsed=False).add_to(fmap)

        st.write(f"**{len(sp_df)} São Paulo region(s)** 🟢  ·  **{len(other_df)} other-state helipad(s)** 🔵")
        st_folium(fmap, use_container_width=True, height=520)

        with st.expander("📋 Raw coordinate data"):
            t1, t2 = st.tabs(["São Paulo", "Other states"])
            with t1:
                st.dataframe(sp_df, use_container_width=True)
            with t2:
                st.dataframe(other_df, use_container_width=True)

        st.divider()
        st.subheader("🌡️ Density view (dark mode)")
        st.caption(
            "Discovery dataset (other states), rendered as a dark-themed point + heatmap "
            "view — generated live with Folium/CartoDB, no API key or account required."
        )
        if other_df.empty:
            st.info(f"No coordinates found at `{COORDS_CSV}` to render a density view.")
        else:
            dark_map = folium.Map(
                location=[other_df["lat"].mean(), other_df["lon"].mean()],
                zoom_start=5,
                tiles="CartoDB dark_matter",
            )
            for _, row in other_df.iterrows():
                folium.CircleMarker(
                    location=[row["lat"], row["lon"]],
                    radius=5,
                    color="#00CED1",
                    fill=True,
                    fill_color="#00CED1",
                    fill_opacity=0.8,
                    tooltip=row.get("Nome do Bairro", "Unknown"),
                ).add_to(dark_map)
            HeatMap(
                other_df[["lat", "lon"]].values.tolist(),
                radius=18,
                blur=22,
                gradient={"0.2": "#FFF8DC", "0.5": "#FFA855", "0.8": "#FF7804", "1.0": "#FF6800"},
            ).add_to(dark_map)
            st_folium(dark_map, use_container_width=True, height=550, key="density_map")

# ====================== TAB 5: Pipeline & Governance ======================
with tab5:
    st.subheader("📖 Project Pipeline")
    st.caption("How raw satellite imagery becomes a validated helipad detector.")

    pipeline_steps = [
        ("🔍", "Discovery", "Selenium scrapes a public aviation website for helipad records and coordinates."),
        ("📐", "Coordinate conversion", "Each point becomes a geographic bounding box (±0.0005°)."),
        ("🛰️", "Tile download", "ESRI World Imagery tiles are downloaded for each bounding box."),
        ("🖼️", "Manual triage", "A human reviews mosaics and keeps only tiles with a visible helipad."),
        ("🏷️", "Annotation (Roboflow)", "Bounding boxes are drawn, single class: helipad."),
        ("🧠", "Training (Colab, GPU)", "YOLOv8n is trained on the annotated dataset."),
        ("📊", "Evaluation", "Precision, recall, mAP, and confusion matrix are computed."),
        ("🚁", "This app", "The trained model runs inference on new images or regions."),
    ]

    cols = st.columns(len(pipeline_steps))
    for col, (icon, title, desc) in zip(cols, pipeline_steps):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="min-height:180px;">
                <div style="font-size:28px;">{icon}</div>
                <p style="font-weight:700; margin:8px 0 4px 0; font-size:13px;">{title}</p>
                <p style="font-size:11px; color:#64748B; margin:0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🛡️ Responsible AI")
    st.markdown("""
- **Fairness & scope**: the model detects a single object class (helipad) on public-area satellite
  imagery; it does not identify, track, or profile individuals.
- **Transparency**: this dashboard shows the real precision/recall/mAP of the model, including its
  known false-positive patterns (rooftop structures, pools, sports courts resembling the helipad "H").
- **Human oversight**: detections are a decision-support signal, not an automated final judgment —
  qualitative review of hits, false positives, and false negatives is part of the evaluation process.
- **Known limitations**: trained on a small dataset (~150 images) from specific São Paulo
  neighborhoods; generalization to other cities/architectural styles is untested.
""")

    st.subheader("⚖️ LGPD & Data Governance")
    st.markdown("""
- Only **public-area** satellite imagery is used — no private property interiors, no people, no
  license plates are annotated.
- Attribution is preserved for all imagery: *Source: Esri, Maxar, Earthstar Geographics, and the
  GIS User Community.*
- Data collection, annotation criteria, and experiment seeds are documented for reproducibility
  and audit purposes (see `README.md`, section "Ethics, LGPD and Governance").
- The scope is strictly academic/technical — no individual surveillance use case is intended or
  supported by this project.
""")

# ====================== TAB 6: Downloads ======================
with tab6:
    st.subheader("⬇️ Download Center")
    st.caption("Everything below is a real file already in this repository — nothing is generated on the fly with placeholder data.")

    dl_col1, dl_col2 = st.columns(2)

    with dl_col1:
        st.markdown("**📄 Executive Report**")
        if EXEC_REPORT_EN.exists():
            with open(EXEC_REPORT_EN, "rb") as f:
                st.download_button("⬇️ Executive Report (English, PDF)", f, file_name=EXEC_REPORT_EN.name,
                                    mime="application/pdf", use_container_width=True)
        else:
            st.caption(f"Not found: `{EXEC_REPORT_EN}`")

        if EXEC_REPORT_PT.exists():
            with open(EXEC_REPORT_PT, "rb") as f:
                st.download_button("⬇️ Relatório Executivo (Português, PDF)", f, file_name=EXEC_REPORT_PT.name,
                                    mime="application/pdf", use_container_width=True)
        else:
            st.caption(f"Not found: `{EXEC_REPORT_PT}`")

    with dl_col2:
        st.markdown("**📦 Dataset & Metrics**")
        if DATASET_RAR.exists():
            with open(DATASET_RAR, "rb") as f:
                st.download_button("⬇️ Annotated Dataset (.rar)", f, file_name=DATASET_RAR.name,
                                    mime="application/octet-stream", use_container_width=True)
        else:
            st.caption(f"Not found: `{DATASET_RAR}`")

        if not metrics_df.empty:
            csv_bytes = metrics_df.drop(columns=["_dir"], errors="ignore").to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Experiment Metrics (.csv)", csv_bytes, file_name="experiment_metrics.csv",
                                mime="text/csv", use_container_width=True)
        else:
            st.caption("No experiment metrics available yet to export.")

    st.markdown("---")
    st.markdown("""
    <div class="metric-card">
        <h4 style="margin:0 0 8px 0;">🐙 Explore the full source code</h4>
        <p style="color:#64748B; font-size:14px;">
            Architecture, datasets, notebooks, and the complete AI pipeline are all on GitHub.
        </p>
        <a href="https://github.com/Mindful-AI-Research/3-project-ai-ml-yolo-helipad_detector" target="_blank">
            github.com/Mindful-AI-Research/3-project-ai-ml-yolo-helipad_detector
        </a>
    </div>
    """, unsafe_allow_html=True)

# ========================= METRICS DASHBOARD =========================
with st.expander("📊 Experiment Metrics", expanded=True):
    if metrics_df.empty:
        st.info("No `results.csv` found yet under `artifacts/runs/detect/*/` (or `artifacts/runs/runs/detect/*/`).")
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

        if n_exp >= 2 and "exp1" in metrics_df["Experiment"].values:
            exp1_row = metrics_df[metrics_df["Experiment"] == "exp1"].iloc[0]
            for _, row in metrics_df.iterrows():
                if row["Experiment"] == "exp1":
                    continue
                delta = row["mAP@50-95"] - exp1_row["mAP@50-95"]
                if delta > 0.005:
                    st.success(f"**{row['Experiment']}** outperformed exp1 on mAP@50-95 ({delta:+.4f}).")
                elif delta < -0.005:
                    st.warning(f"**{row['Experiment']}** scored lower than exp1 on mAP@50-95 ({delta:+.4f}) — possible overfitting.")
                else:
                    st.info(f"**{row['Experiment']}** is essentially tied with exp1 (Δ {delta:+.4f}).")

        # ---- Per-epoch metric evolution (real data from results.csv) ----
        curves = load_experiment_curves()
        if curves:
            st.markdown("#### 📈 Metric evolution per epoch")
            metric_choice = st.selectbox(
                "Metric",
                ["metrics/mAP50-95(B)", "metrics/mAP50(B)", "metrics/precision(B)", "metrics/recall(B)"],
                format_func=lambda m: m.replace("metrics/", "").replace("(B)", ""),
                key="metric_choice_curve",
            )
            fig = go.Figure()
            for exp_name, df_curve in curves.items():
                if metric_choice in df_curve.columns:
                    fig.add_trace(go.Scatter(
                        x=df_curve["epoch"], y=df_curve[metric_choice],
                        mode="lines", name=exp_name,
                    ))
            fig.update_layout(
                xaxis_title="Epoch", yaxis_title=metric_choice.replace("metrics/", "").replace("(B)", ""),
                height=320, margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
            )
            st.plotly_chart(fig, use_container_width=True)

        # ---- Confusion matrix per experiment (real image already generated by YOLO) ----
        if not metrics_df.empty and "_dir" in metrics_df.columns:
            st.markdown("#### 🔀 Confusion matrix")
            cm_exp = st.selectbox(
                "Experiment", metrics_df["Experiment"].tolist(), key="cm_exp_choice"
            )
            exp_dir_str = metrics_df.loc[metrics_df["Experiment"] == cm_exp, "_dir"].iloc[0]
            cm_path = Path(exp_dir_str) / "confusion_matrix.png"
            cm_norm_path = Path(exp_dir_str) / "confusion_matrix_normalized.png"
            cm_col1, cm_col2 = st.columns(2)
            with cm_col1:
                if cm_path.exists():
                    st.image(str(cm_path), caption=f"{cm_exp} — confusion matrix", use_container_width=True)
                else:
                    st.info("confusion_matrix.png not found for this experiment.")
            with cm_col2:
                if cm_norm_path.exists():
                    st.image(str(cm_norm_path), caption=f"{cm_exp} — normalized", use_container_width=True)
                else:
                    st.info("confusion_matrix_normalized.png not found for this experiment.")

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
SÃO PAULO • YOLO • ESRI WORLD IMAGERY
</p>
""", unsafe_allow_html=True)
