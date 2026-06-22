import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import io
from datetime import datetime
import math
import requests
from pathlib import Path
import tempfile
import shutil

# ========================= CONFIGURAÇÃO =========================
st.set_page_config(
    page_title="Heliponto • São Paulo",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-title {font-size: 42px !important; font-weight: bold; color: #1E3A8A; text-align: center;}
    .subtitle {text-align: center; color: #64748B; font-size: 18px; margin-bottom: 30px;}
    .result-card {background-color: #f8fafc; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0;}
    </style>
""", unsafe_allow_html=True)

# ========================= MODEL =========================
@st.cache_resource
def load_model():
    return YOLO('AI Training/runs/detect/runs/exp1/weights/best.pt')

# ========================= FUNÇÕES DE TILES =========================
def deg2tile(lat, lon, z):
    n = 2.0 ** z
    x = int((lon + 180.0) / 360.0 * n)
    lat_rad = math.radians(lat)
    y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return x, y

def baixar_tile(z, x, y, temp_dir):
    url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    headers = {"User-Agent": "Heliponto-PUC-SP/1.0"}
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

# ========================= DETECÇÃO =========================
def detect_heliponto(image):
    model = load_model()
    result = model.predict(source=image, conf=0.25, verbose=False)[0]
    plotted = result.plot()[:, :, ::-1]  # BGR → RGB
    return plotted, len(result.boxes) > 0

# ========================= INTERFACE =========================
st.markdown('<h1 class="main-title">🚁 Detecção de Helipontos</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Inteligência Artificial + Imagens de Satélite • São Paulo</p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📤 Upload de Imagem", "🔎 Busca por Região (Satélite)"])

# ====================== TAB 1: Upload ======================
with tab1:
    imagems = st.file_uploader("Faça upload de imagens aéreas", 
                               type=["jpg", "jpeg", "png"], 
                               accept_multiple_files=True, max_upload_size=10, help="Recomenda-se imagens de satélite ou drones com boa resolução e o mais próximo do objeto possível.")
    
    if imagems:
        for idx, image_file in enumerate(imagems):
            col1, col2 = st.columns(2)
            original = Image.open(image_file)
            
            with col1:
                st.image(original, caption="Original", use_container_width=True)
            
            with col2:
                result_img, has_helipad = detect_heliponto(original)
                st.image(result_img, caption="Detecção", use_container_width=True)
                if has_helipad:
                    st.success("✅ Heliponto detectado!")
                else:
                    st.warning("Nenhum heliponto encontrado.")

# ====================== TAB 2: Busca por Bounding Box ======================
with tab2:
    st.subheader("🔎 Buscar Helipontos em uma Região")
    st.caption("Use coordenadas da região desejada (ex: Centro de SP)")

    col_a, col_b = st.columns(2)
    with col_a:
        lon_min = st.number_input("Longitude Mínima", value=-46.6583, format="%.6f")
        lat_min = st.number_input("Latitude Mínima", value=-23.5827, format="%.6f")
    with col_b:
        lon_max = st.number_input("Longitude Máxima", value=-46.6311, format="%.6f")
        lat_max = st.number_input("Latitude Máxima", value=-23.5536, format="%.6f")

    zoom = st.slider("Zoom (recomendado: 19)", 16, 20, 19)
    buscar_btn = st.button("🚀 Buscar e Analisar Região", type="primary", use_container_width=True)

    if buscar_btn:
        with st.spinner("Baixando tiles de satélite e analisando com IA... (pode demorar)"):
            temp_dir = Path(tempfile.mkdtemp())
            
            try:
                # Calcula tiles
                x_min, y_max = deg2tile(lat_min, lon_min, zoom)
                x_max, y_min = deg2tile(lat_max, lon_max, zoom)
                
                jobs = [(zoom, x, y) for x in range(x_min, x_max+1) for y in range(y_min, y_max+1)]
                
                st.info(f"Processando **{len(jobs)}** tiles de satélite...")
                progress = st.progress(0, "Progresso: ")
                
                detected_tiles = []
                
                for i, (z, x, y) in enumerate(jobs):
                    progress.progress((i+1)/len(jobs), f"Progresso: {i+1}/{len(jobs)} tiles")
                        
                    
                    tile_path = baixar_tile(z, x, y, temp_dir)
                    if not tile_path:
                        continue
                    
                    img = Image.open(tile_path)
                    result_img, has_detection = detect_heliponto(img)
                    
                    if has_detection:
                        detected_tiles.append((result_img, f"tile_z{z}_x{x}_y{y}.jpg"))
                
                # Resultados
                if detected_tiles:
                    st.success(f"🎯 **{len(detected_tiles)} heliponto(s) encontrado(s)** na região!")
                    
                    cols = st.columns(3)
                    for idx, (img_array, filename) in enumerate(detected_tiles):
                        with cols[idx % 3]:
                            st.image(img_array, caption=filename, use_container_width=True)
                            
                            buf = io.BytesIO()
                            Image.fromarray(img_array).save(buf, format="PNG")
                            buf.seek(0)
                            
                            st.download_button(
                                label="⬇️ Baixar",
                                data=buf,
                                file_name=filename.replace(".jpg", "_detected.png"),
                                mime="image/png",
                                key=f"dl_{idx}"
                            )
                    
                    # Download em lote
                    if len(detected_tiles) > 1:
                        zip_buffer = io.BytesIO()
                        # Para simplicidade, mostramos um por um. Pode expandir para ZIP se quiser.
                        st.info("Use os botões acima para baixar individualmente.")
                else:
                    st.warning("Nenhum heliponto foi encontrado nesta região.")
                    
            finally:
                shutil.rmtree(temp_dir, ignore_errors=True)

# Rodapé
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #64748B; padding: 20px;'>
        Desenvolvido com ❤️ para São Paulo • YOLOv8 + Esri World Imagery
    </div>
""", unsafe_allow_html=True)
