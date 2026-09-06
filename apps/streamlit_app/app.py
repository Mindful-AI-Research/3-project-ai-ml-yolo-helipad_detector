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
import base64
import io
import json
import time
import zipfile
from datetime import datetime
import math
import re
import requests
from pathlib import Path
import tempfile
import shutil

# ========================= LANGUAGE / i18n =========================
# Only static UI copy (labels, headers, captions, button text, messages) is
# translated. Anything that comes from data at runtime — experiment names,
# region names from CSV/JSON, raw dataframe columns (already in Portuguese
# in the source CSVs), file paths — is left as-is, since translating it
# would mean rewriting the underlying data, not just the UI.
if "lang" not in st.session_state:
    st.session_state["lang"] = "en"


def t(key: str) -> str:
    entry = TR.get(key)
    if entry is None:
        return key
    return entry.get(st.session_state["lang"], entry.get("en", key))



TR = {
    # ---- Sidebar ----
    "sidebar.model": {"en": "⚙️ Model", "pt": "⚙️ Modelo"},
    "sidebar.no_model.warning": {
        "en": "No trained model found at `artifacts/runs/detect/*/weights/best.pt` (or `artifacts/runs/runs/detect/*/...`) yet. "
              "Detection features (Upload, Search by Region, Sample Images) are disabled until "
              "one is available — but the Map, Pipeline & Governance, and Downloads tabs below "
              "don't need a model and work right now.",
        "pt": "Nenhum modelo treinado encontrado em `artifacts/runs/detect/*/weights/best.pt` (ou `artifacts/runs/runs/detect/*/...`) ainda. "
              "As funcionalidades de detecção (Upload, Search by Region, Sample Images) ficam desabilitadas até "
              "que um modelo esteja disponível — mas as abas Map, Pipeline & Governance e Downloads abaixo "
              "não precisam de modelo e já funcionam.",
    },
    "sidebar.choose_experiment": {"en": "Choose the trained experiment", "pt": "Escolha o experimento treinado"},
    "sidebar.choose_experiment.help": {
        "en": "Every folder under artifacts/runs/detect/ (or artifacts/runs/runs/detect/) with a ready best.pt shows up here "
              "automatically — including future experiments, no app edits needed.",
        "pt": "Toda pasta em artifacts/runs/detect/ (ou artifacts/runs/runs/detect/) com um best.pt pronto aparece aqui "
              "automaticamente — inclusive experimentos futuros, sem precisar editar o app.",
    },
    "sidebar.confidence": {"en": "Minimum detection confidence", "pt": "Confiança mínima de detecção"},

    # ---- Sidebar: background music ----
    "sidebar.music.title": {"en": "🎶 Passacaglia - Deep House", "pt": "🎶 Passacaglia - Deep House"},
    "sidebar.music.tagline": {
        "en": "🎵 The music carries the story forward. Take it with you.",
        "pt": "🎵 A música leva a história adiante. Leve-a com você.",
    },
    "sidebar.music.play": {"en": "Play Music", "pt": "Play Music"},
    "sidebar.music.pause": {"en": "Pause Music", "pt": "Pausar Música"},
    "sidebar.music.missing": {
        "en": "Background track not found — add an mp3 at `assets/audio/passacaglia-deep-house-remix.mp3` to enable this.",
        "pt": "Faixa de fundo não encontrada — adicione um mp3 em `assets/audio/passacaglia-deep-house-remix.mp3` para habilitar.",
    },
    "sidebar.replay_heli": {"en": "Replay flyby", "pt": "Repetir sobrevoo"},
    "sidebar.spin_heli": {"en": "Spin", "pt": "Girar"},
    "sidebar.pause_heli": {"en": "Pause animation", "pt": "Pausar animação"},
    "sidebar.resume_heli": {"en": "Resume animation", "pt": "Retomar animação"},
    "sidebar.extras": {"en": "🎬 Extras (helicopter animation)", "pt": "🎬 Extras (animação do helicóptero)"},
    "about.discovery.title": {"en": "🗺️ Discovery dataset coverage", "pt": "🗺️ Cobertura do dataset de descoberta"},
    "about.discovery.body": {
        "en": "Points collected by the geospatial automation (`helipad_bot.py`) across Brazil, outside São Paulo — used to widen the search for real helipad coordinates before triage and annotation.",
        "pt": "Pontos coletados pela automação geoespacial (`helipad_bot.py`) pelo Brasil, fora de São Paulo — usados para ampliar a busca por coordenadas reais de helipontos antes da triagem e anotação.",
    },
    "about.discovery.points": {"en": "Points collected", "pt": "Pontos coletados"},
    "about.discovery.regions": {"en": "Distinct locations", "pt": "Locais distintos"},
    "about.discovery.pending": {
        "en": "State-by-state breakdown pending — run `geocode_states.py` to enrich this with a full per-state count.",
        "pt": "Detalhamento por estado pendente — rode `geocode_states.py` para enriquecer isso com contagem completa por estado.",
    },
    "about.discovery.state_col": {"en": "State", "pt": "Estado"},
    "about.discovery.count_col": {"en": "Points", "pt": "Pontos"},
    "about.discovery.missing": {
        "en": "Discovery coordinates CSV not found at `{path}`.",
        "pt": "CSV de coordenadas de descoberta não encontrado em `{path}`.",
    },

    # ---- Top 10 helicopter cities table ----
    "cities.header": {
        "en": "🚁 Top 10 — Cities with the Highest Presence/Traffic of Helicopters",
        "pt": "🚁 Top 10 — Cidades com maior presença/tráfego de helicópteros",
    },
    "cities.why_sao_paulo": {
        "en": "São Paulo leads the global ranking of helicopter presence/traffic — the largest "
              "estimated fleet (400+) and roughly 2,200 rooftop landings and takeoffs per day in "
              "the metropolitan area. That real density of rooftop helicopter activity is why this "
              "project specifically targets São Paulo, rather than a city with sparser or "
              "already-mapped helipad infrastructure.",
        "pt": "São Paulo lidera o ranking global de presença/tráfego de helicópteros — maior frota "
              "estimada (400+) e cerca de 2.200 pousos e decolagens por dia na região metropolitana. "
              "Essa densidade real de atividade de helicópteros em telhados é o motivo pelo qual "
              "este projeto tem como alvo especificamente São Paulo, em vez de uma cidade com "
              "infraestrutura de helipontos mais esparsa ou já mapeada.",
    },
    "cities.table.columns": {
        "en": ["Rank", "City", "Country", "Main Indicator",
               "Estimated Fleet (Helicopters)", "Highlight"],
        "pt": ["Rank", "Cidade", "País", "Indicador principal",
               "Frota estimada (Helicópteros)", "Destaque"],
    },
    # NOTE: this table used to carry a "Rate (%)" column presented as each
    # city's relative helicopter presence/traffic. It was removed — those
    # numbers (27.7%, 25.5%, 23.9%, ...) turned out to be an exact,
    # digit-for-digit copy of this project's own SP field-validation
    # detection-rate-by-region table (see field.rank_col and the Field
    # Detections tab), sorted descending and relabeled onto 10 world cities.
    # That's unrelated data — a region's helipad-detection rate says nothing
    # about a different city's helicopter fleet — so the column was invented
    # precision, not a sourced statistic, and is better left out than kept
    # with a caveat nobody will read. The city ranking and fleet-size figures
    # themselves are left in as general/editorial context (not a project
    # measurement), consistent with Section 13 of the report's transparency
    # about known data-integrity issues once found and corrected.
    "cities.table.data": {
        "en": [
            ["1st", "São Paulo", "🇧🇷 Brazil", "Largest fleet", "400+",
             "~2,200 landings/takeoffs daily in the metropolitan area"],
            ["2nd", "New York", "🇺🇸 USA", "Fleet + intense urban traffic", "—",
             "Strong executive, tourist, and transport use"],
            ["3rd", "Tokyo", "🇯🇵 Japan", "Large fleet", "—",
             "Corporate, emergency, and transport operations"],
            ["4th", "Rio de Janeiro", "🇧🇷 Brazil", "Fleet + offshore operations", "—",
             "Significant activity related to oil and gas"],
            ["5th", "London", "🇬🇧 United Kingdom", "Executive traffic", "—",
             "Strong corporate market and urban heliports"],
            ["6th", "Belo Horizonte", "🇧🇷 Brazil", "Large fleet", "—",
             "Strong executive and corporate aviation"],
            ["7th", "Santiago", "🇨🇱 Chile", "Large fleet", "—",
             "Executive aviation and special operations"],
            ["8th", "Mexico City", "🇲🇽 Mexico", "Large fleet", "—",
             "Executive transport and government operations"],
            ["9th", "Bogotá", "🇨🇴 Colombia", "Large fleet", "—",
             "Executive, emergency, and special operations"],
            ["10th", "Beijing", "🇨🇳 China", "Large fleet", "—",
             "Executive, governmental, and special operations"],
        ],
        "pt": [
            ["1º", "São Paulo", "🇧🇷 Brasil", "Maior frota", "400+",
             "~2.200 pousos/decolagens diários na região metropolitana"],
            ["2º", "Nova York", "🇺🇸 EUA", "Frota + intenso tráfego urbano", "—",
             "Forte uso executivo, turístico e de transporte"],
            ["3º", "Tóquio", "🇯🇵 Japão", "Grande frota", "—",
             "Operações corporativas, emergência e transporte"],
            ["4º", "Rio de Janeiro", "🇧🇷 Brasil", "Frota + operações offshore", "—",
             "Grande atividade ligada ao petróleo e gás"],
            ["5º", "Londres", "🇬🇧 Reino Unido", "Tráfego executivo", "—",
             "Forte mercado corporativo e heliportos urbanos"],
            ["6º", "Belo Horizonte", "🇧🇷 Brasil", "Grande frota", "—",
             "Forte aviação executiva e corporativa"],
            ["7º", "Santiago", "🇨🇱 Chile", "Grande frota", "—",
             "Aviação executiva e operações especiais"],
            ["8º", "Cidade do México", "🇲🇽 México", "Grande frota", "—",
             "Transporte executivo e operações governamentais"],
            ["9º", "Bogotá", "🇨🇴 Colômbia", "Grande frota", "—",
             "Executivo, emergência e operações especiais"],
            ["10º", "Pequim", "🇨🇳 China", "Grande frota", "—",
             "Executivo, governamental e operações especiais"],
        ],
    },

    # ---- Main header ----
    "main.title": {"en": "🚁 Helipad Detection", "pt": "🚁 Detecção de Helipontos"},
    "main.subtitle": {"en": "AI + Satellite Imagery • São Paulo", "pt": "IA + Imagens de Satélite • São Paulo"},
    "main.active_model": {"en": "Active model:", "pt": "Modelo ativo:"},
    "main.active_model.none": {"en": "_none yet — detection tabs disabled_", "pt": "_nenhum ainda — abas de detecção desabilitadas_"},

    
    # ---- Tab labels ----
    "tabs.metrics": {"en": "📊 Experiment Metrics", "pt": "📊 Métricas dos Experimentos"},
    "tabs.field": {"en": "🌍 Field Detections by Region", "pt": "🌍 Detecções de Campo por Região"},
    "tabs.map": {"en": "🗺️ Map", "pt": "🗺️ Mapa"},
    "tabs.search": {"en": "🔎 Search by Region (Satellite)", "pt": "🔎 Buscar por Região (Satélite)"},
    "tabs.samples": {"en": "🖼️ Sample Images", "pt": "🖼️ Imagens de Exemplo"},
    "tabs.upload": {"en": "📤 Upload Image", "pt": "📤 Enviar Imagem"},
    "tabs.pipeline": {"en": "📖 Pipeline", "pt": "📖 Pipeline"},
    "tabs.governance": {"en": "🛡️ Governance", "pt": "🛡️ Governança"},
    "tabs.about": {"en": "👥 About", "pt": "👥 Sobre"},
    "tabs.downloads": {"en": "⬇️ Downloads", "pt": "⬇️ Downloads"},

    # ---- Tab 1: Upload ----
    "upload.no_model.info": {
        "en": "⚠️ No trained model yet — train exp1/exp2/exp3 and this tab will activate automatically.",
        "pt": "⚠️ Ainda não há um modelo treinado — treine exp1/exp2/exp3 e esta aba ativa sozinha.",
    },
    "upload.uploader.label": {"en": "Upload aerial images", "pt": "Envie imagens aéreas"},
    "upload.uploader.help": {
        "en": "Satellite or drone images with good resolution, as close to the target as possible, are recommended.",
        "pt": "Recomenda-se imagens de satélite ou drone com boa resolução, o mais próximas possível do alvo.",
    },
    "upload.original_caption": {"en": "Original", "pt": "Original"},
    "upload.detection_caption": {"en": "Detection", "pt": "Detecção"},
    "upload.success": {"en": "✅ Helipad detected!", "pt": "✅ Heliponto detectado!"},
    "upload.warning_none": {"en": "No helipad found.", "pt": "Nenhum heliponto encontrado."},

    # ---- Tab 2: Search by Region ----
    "search.subheader": {"en": "🔎 Search for Helipads in a Region", "pt": "🔎 Buscar Helipontos em uma Região"},
    "search.caption": {
        "en": "Use the coordinates of the desired region (e.g. Downtown São Paulo)",
        "pt": "Use as coordenadas da região desejada (ex.: Centro de São Paulo)",
    },
    "search.lon_min": {"en": "Min Longitude", "pt": "Longitude Mínima"},
    "search.lat_min": {"en": "Min Latitude", "pt": "Latitude Mínima"},
    "search.lon_max": {"en": "Max Longitude", "pt": "Longitude Máxima"},
    "search.lat_max": {"en": "Max Latitude", "pt": "Latitude Máxima"},
    "search.zoom": {"en": "Zoom (recommended: 19)", "pt": "Zoom (recomendado: 19)"},
    "search.button": {"en": "🚀 Search and Analyze Region", "pt": "🚀 Buscar e Analisar Região"},
    "search.no_model.error": {
        "en": "⚠️ No trained model yet — this feature needs a model to run detection.",
        "pt": "⚠️ Ainda não há um modelo treinado — esta funcionalidade precisa de um modelo para detectar.",
    },
    "search.spinner": {
        "en": "Downloading satellite tiles and analyzing with AI... (this may take a while)",
        "pt": "Baixando tiles de satélite e analisando com IA... (pode demorar um pouco)",
    },
    "search.processing": {"en": "Processing", "pt": "Processando"},
    "search.satellite_tiles": {"en": "satellite tiles...", "pt": "tiles de satélite..."},
    "search.progress": {"en": "Progress:", "pt": "Progresso:"},
    "search.found": {"en": "helipad(s) found", "pt": "heliponto(s) encontrado(s)"},
    "search.in_region": {"en": "in the region!", "pt": "na região!"},
    "search.download": {"en": "⬇️ Download", "pt": "⬇️ Baixar"},
    "search.download_individually": {
        "en": "Use the buttons above to download individually.",
        "pt": "Use os botões acima para baixar individualmente.",
    },
    "search.none_found": {"en": "No helipad was found in this region.", "pt": "Nenhum heliponto foi encontrado nesta região."},

    
    # ---- Tab 3: Sample Images ----
    "samples.subheader": {"en": "🖼️ Test with Sample Images", "pt": "🖼️ Testar com Imagens de Exemplo"},
    "samples.caption": {
        "en": "Don't have your own image handy? Use the satellite images already included in the "
              "repository to test the detector right away.",
        "pt": "Não tem uma imagem sua à mão? Use as imagens de satélite já incluídas no "
              "repositório para testar o detector agora mesmo.",
    },
    "samples.none_found": {
        "en": "No sample images found at `{dir}/`. "
              "If you're running this app outside the cloned repository, download the sample "
              "images directly from GitHub and place them in that folder.",
        "pt": "Nenhuma imagem de exemplo encontrada em `{dir}/`. "
              "Se você está rodando este app fora do repositório clonado, baixe as imagens de exemplo "
              "diretamente do GitHub e coloque-as nessa pasta.",
    },
    "samples.available": {"en": "sample image(s) available.", "pt": "imagem(ns) de exemplo disponível(is)."},
    "samples.more": {"en": "...and {n} more image(s).", "pt": "...e mais {n} imagem(ns)."},
    "samples.run_button": {
        "en": "🚀 Run detection on all sample images",
        "pt": "🚀 Rodar detecção em todas as imagens de exemplo",
    },
    "samples.download_zip": {
        "en": "⬇️ Download all sample images (.zip)",
        "pt": "⬇️ Baixar todas as imagens de exemplo (.zip)",
    },
    "samples.no_model.error": {
        "en": "⚠️ No trained model yet — this feature needs a model to run detection.",
        "pt": "⚠️ Ainda não há um modelo treinado — esta funcionalidade precisa de um modelo para detectar.",
    },
    "samples.analyzing": {"en": "Analyzing", "pt": "Analisando"},
    "samples.sample_images": {"en": "sample image(s)...", "pt": "imagem(ns) de exemplo..."},
    "samples.detected": {"en": "✅ Detected", "pt": "✅ Detectado"},
    "samples.no_detection": {"en": "No detection", "pt": "Nenhuma detecção"},
    "samples.summary": {
        "en": "**Summary:** helipad detected in {hits} of {total} sample image(s).",
        "pt": "**Resumo:** heliponto detectado em {hits} de {total} imagem(ns) de exemplo.",
    },

# ---- Tab 4: Map ----
"map.subheader": {
    "en": "🗺️ Helipad Location Map",
    "pt": "🗺️ Mapa de Localização dos Helipontos",
},

"map.caption": {
    "en": "🔴 **Training Areas (São Paulo)**: regional bounding boxes used to build and validate the training dataset. 🔵 **Discovery Dataset**: helipad candidates identified across other Brazilian states.",
    "pt": "🔴 **Áreas de Treinamento (São Paulo)**: regiões delimitadas por bounding boxes utilizadas na construção e validação do conjunto de treinamento. 🔵 **Dataset de Descoberta**: candidatos a helipontos identificados em outros estados brasileiros.",
},

"map.dark_mode": {
    "en": "🌙 Dark mode",
    "pt": "🌙 Modo escuro",
},

"map.dark_base": {
    "en": "🌙 Dark basemap",
    "pt": "🌙 Mapa-base escuro",
},

"map.light_base": {
    "en": "☀️ Light basemap",
    "pt": "☀️ Mapa-base claro",
},

"map.no_coords.info": {
    "en": "No coordinate files were found at `{sp}` or `{other}`. Please follow the Execution Guide to generate them.",
    "pt": "Nenhum arquivo de coordenadas foi encontrado em `{sp}` ou `{other}`. Consulte o Guia de Execução para gerá-los.",
},

"map.sp_layer": {
    "en": "São Paulo training areas",
    "pt": "Áreas de treinamento em São Paulo",
},

"map.other_layer": {
    "en": "Discovery dataset",
    "pt": "Dataset de descoberta",
},

"map.training_region": {
    "en": "Training region",
    "pt": "Região de treinamento",
},

"map.detection_rate_layer": {
    "en": "🔵 Field detection rate",
    "pt": "🔵 Taxa de detecção em campo",
},

"map.tiles_detected": {
    "en": "Detected tiles",
    "pt": "Tiles detectados",
},

"map.rate": {
    "en": "Detection rate",
    "pt": "Taxa de detecção",
},

"map.summary": {
    "en": "**{sp} training region(s)** 🔴 · **{other} discovered helipad(s)** 🔵",
    "pt": "**{sp} região(ões) de treinamento** 🔴 · **{other} heliponto(s) descoberto(s)** 🔵",
},

"map.layers_caption": {
    "en": "🗂️ Map layers — toggle what's shown",
    "pt": "🗂️ Camadas do mapa — controle o que aparece",
},

"map.raw_data_expander": {
    "en": "📋 Coordinate data",
    "pt": "📋 Dados de coordenadas",
},

"map.raw_data.sp_tab": {
    "en": "São Paulo",
    "pt": "São Paulo",
},

"map.raw_data.other_tab": {
    "en": "Other states",
    "pt": "Outros estados",
},

"map.raw_data.city_hint_col": {
    "en": "Nearest state capital",
    "pt": "Capital estadual mais próxima",
},

"map.density.subheader": {
    "en": "🌡️ Density Map",
    "pt": "🌡️ Mapa de Densidade",
},

"map.density.caption": {
    "en": "Interactive point and heatmap visualization of the Discovery Dataset from other Brazilian states. Rendered locally with Folium and OpenStreetMap—no API key or account required.",
    "pt": "Visualização interativa em pontos e mapa de calor do Dataset de Descoberta em outros estados brasileiros. Renderizada localmente com Folium e OpenStreetMap, sem necessidade de chave de API ou conta.",
},

"map.density.no_coords": {
    "en": "No coordinates were found in `{path}` to generate the density map.",
    "pt": "Nenhuma coordenada foi encontrada em `{path}` para gerar o mapa de densidade.",
},

   
## ---- Tab 5: Pipeline ----
"pipeline.subheader": {
    "en": "📖 End-to-End Project Pipeline",
    "pt": "📖 Pipeline Completo do Projeto",
},
"pipeline.caption": {
    "en": "Follow the complete workflow from public aviation records to a validated Computer Vision model for helipad detection.",
    "pt": "Acompanhe todo o fluxo de trabalho, desde registros públicos de aviação até um modelo de Visão Computacional validado para detecção de helipontos.",
},
"pipeline.step1.title": {
    "en": "Discovery",
    "pt": "Descoberta",
},
"pipeline.step1.desc": {
    "en": "Public aviation records are collected with Selenium, including helipad metadata and geographic coordinates.",
    "pt": "Registros públicos de aviação são coletados com Selenium, incluindo metadados dos helipontos e suas coordenadas geográficas.",
},
"pipeline.step2.title": {
    "en": "Coordinate Conversion",
    "pt": "Conversão de Coordenadas",
},
"pipeline.step2.desc": {
    "en": "Each geographic coordinate is converted into a bounding box defining the satellite imagery extraction area.",
    "pt": "Cada coordenada geográfica é convertida em uma bounding box que define a área de extração da imagem de satélite.",
},
"pipeline.step3.title": {
    "en": "Satellite Imagery",
    "pt": "Imagens de Satélite",
},
"pipeline.step3.desc": {
    "en": "Satellite tiles are downloaded from ESRI World Imagery for every bounding box.",
    "pt": "Imagens de satélite são baixadas do ESRI World Imagery para cada bounding box.",
},
"pipeline.step4.title": {
    "en": "Manual Triage",
    "pt": "Triagem Manual",
},
"pipeline.step4.desc": {
    "en": "Each mosaic is visually inspected, and only images containing visible helipads are retained.",
    "pt": "Cada mosaico é inspecionado visualmente, mantendo apenas as imagens que contêm helipontos visíveis.",
},
"pipeline.step5.title": {
    "en": "Annotation (Roboflow)",
    "pt": "Anotação (Roboflow)",
},
"pipeline.step5.desc": {
    "en": "Helipads are manually annotated with bounding boxes using a single object class.",
    "pt": "Os helipontos são anotados manualmente com bounding boxes utilizando uma única classe de objeto.",
},
"pipeline.step6.title": {
    "en": "Model Training",
    "pt": "Treinamento do Modelo",
},
"pipeline.step6.desc": {
    "en": "Multiple YOLOv8n and YOLOv11n models are trained and compared using Google Colab with GPU acceleration.",
    "pt": "Múltiplos modelos YOLOv8n e YOLOv11n são treinados e comparados utilizando Google Colab com aceleração por GPU.",
},
"pipeline.step7.title": {
    "en": "Model Evaluation",
    "pt": "Avaliação do Modelo",
},
"pipeline.step7.desc": {
    "en": "Performance is measured using Precision, Recall, mAP, confusion matrices, and additional evaluation metrics.",
    "pt": "O desempenho é avaliado por meio de Precision, Recall, mAP, matriz de confusão e outras métricas de avaliação.",
},
"pipeline.step8.title": {
    "en": "Field Validation",
    "pt": "Validação em Campo",
},
"pipeline.step8.desc": {
    "en": "The best-performing model is validated on more than 7,900 real, uncurated satellite tiles collected from ten São Paulo neighborhoods to assess real-world generalization.",
    "pt": "O modelo com melhor desempenho é validado em mais de 7.900 mosaicos reais e não selecionados de dez bairros da cidade de São Paulo para avaliar sua capacidade de generalização em cenários reais.",
},
"pipeline.step9.title": {
    "en": "Interactive Dashboard",
    "pt": "Dashboard Interativo",
},
"pipeline.step9.desc": {
    "en": "The final model powers this interactive dashboard, enabling inference, visualization, and exploration of predictions on new satellite imagery, with a modular architecture that can be extended to drone imagery and other aerial platforms.",
    "pt": "O modelo final alimenta este dashboard interativo, permitindo executar inferências, visualizar resultados e explorar predições em novas imagens de satélite, com uma arquitetura modular que pode ser estendida para imagens capturadas por drones e outras plataformas aéreas.",
},

# ---- Tab 6: Governance ----
"gov.responsible_ai": {
    "en": "🛡️ Responsible AI",
    "pt": "🛡️ IA Responsável",
},
"gov.responsible_ai.body": {
    "en": (
        "- **Purpose & Scope:** The model detects a single object class (helipad) in publicly available satellite imagery. It does not identify, track, or profile individuals.\n"
        "- **Transparency:** This dashboard reports the model's real Precision, Recall, and mAP, together with its known false-positive patterns, including rooftop structures, swimming pools, and sports courts that resemble helipad markings.\n"
        "- **Human Oversight:** Model predictions are intended to support human decision-making rather than replace it. All detections should be reviewed qualitatively as part of the evaluation process.\n"
        "- **Known Limitations:** The model was trained on a relatively small dataset (approximately 150 annotated images) collected from specific neighborhoods in São Paulo. Its performance in other cities or architectural contexts has not yet been systematically evaluated.\n"
    ),
    "pt": (
        "- **Propósito e Escopo:** O modelo detecta apenas uma classe de objeto (heliponto) em imagens de satélite de domínio público. Ele não identifica, rastreia nem cria perfis de pessoas.\n"
        "- **Transparência:** Este dashboard apresenta os valores reais de Precision, Recall e mAP do modelo, além de seus principais padrões conhecidos de falsos positivos, como estruturas de telhado, piscinas e quadras esportivas semelhantes à marcação de um heliponto.\n"
        "- **Supervisão Humana:** As detecções servem como apoio à decisão e não substituem a análise humana. Todos os resultados devem ser revisados qualitativamente durante o processo de avaliação.\n"
        "- **Limitações Conhecidas:** O modelo foi treinado com um conjunto relativamente pequeno de dados (aproximadamente 150 imagens anotadas), proveniente de bairros específicos da cidade de São Paulo. Seu desempenho em outras cidades ou estilos arquitetônicos ainda não foi avaliado de forma sistemática.\n"
    ),
},

"gov.lgpd": {
    "en": "⚖️ LGPD & Data Governance",
    "pt": "⚖️ LGPD e Governança de Dados",
},
"gov.lgpd.body": {
    "en": (
        "- Only publicly available satellite imagery is used. No private property interiors, identifiable individuals, or vehicle license plates are collected or annotated.\n"
        "- Image attribution is preserved in accordance with the original provider: *Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community.*\n"
        "- Data collection procedures, annotation criteria, preprocessing steps, and experimental settings are documented to support reproducibility and independent auditing (see `README.md`, section **Ethics, LGPD and Governance**).\n"
        "- This project is intended exclusively for academic research and technical education. It is not designed or supported for surveillance or monitoring of individuals.\n"
    ),
    "pt": (
        "- São utilizadas apenas imagens de satélite de acesso público. Nenhum interior de propriedade privada, pessoa identificável ou placa de veículo é coletado ou anotado.\n"
        "- A atribuição das imagens é preservada conforme o provedor original: *Fonte: Esri, Maxar, Earthstar Geographics e GIS User Community.*\n"
        "- Os procedimentos de coleta, os critérios de anotação, as etapas de pré-processamento e as configurações dos experimentos são documentados para garantir reprodutibilidade e possibilitar auditorias independentes (consulte o `README.md`, seção **Ethics, LGPD and Governance**).\n"
        "- Este projeto possui finalidade exclusivamente acadêmica e educacional, não sendo desenvolvido nem destinado para aplicações de vigilância ou monitoramento de indivíduos.\n"
    ),
},



# ---- Tab: About ----
"about.header": {"en": "👥 About", "pt": "👥 Sobre"},

"about.body_intro": {
    "en": (
        "**Helipad Detector** is an end-to-end Artificial Intelligence and Computer Vision "
        "platform designed to automatically detect and map rooftop helipads from satellite imagery.\n\n"

        "The project focuses on São Paulo, Brazil, a unique urban environment with the world's "
        "largest helicopter fleet, approximately **2,200 takeoffs and landings per day**, and "
        "**one operation every 45 seconds during peak hours**.\n\n"

        "The city also operates **HELICONTROL**, a dedicated helicopter air traffic control "
        "system created to manage this high-density urban air mobility scenario. This combination "
        "of intense helicopter activity and complex urban infrastructure makes São Paulo a relevant "
        "real-world environment for developing AI-based geospatial intelligence solutions.\n\n"

        "By transforming satellite imagery into structured spatial information, the project "
        "demonstrates how Computer Vision can support urban analysis, infrastructure mapping, "
        "and data-driven decision making for future smart city applications.\n\n"

        "The complete AI workflow includes:\n\n"
        "• Public data collection\n\n"
        "• Satellite imagery acquisition\n\n"
        "• Manual annotation in Roboflow\n\n"
        "• YOLOv8n / YOLOv11n training\n\n"
        "• Field validation on more than **7,900** real satellite tiles\n\n"
    ),

    "pt": (
        "O **Helipad Detector** é uma plataforma completa de Inteligência Artificial e Visão "
        "Computacional desenvolvida para detectar e mapear automaticamente helipontos em imagens "
        "de satélite.\n\n"

        "O projeto tem como foco São Paulo, um ambiente urbano único que possui a maior frota de "
        "helicópteros do mundo, com cerca de **2.200 pousos e decolagens por dia** e "
        "**uma operação a cada 45 segundos nos horários de pico**.\n\n"

        "A cidade também possui o **HELICONTROL**, um sistema dedicado de controle de tráfego "
        "aéreo para helicópteros, criado para organizar esse cenário de alta densidade de "
        "mobilidade aérea urbana.\n\n"

        "Essa combinação entre intensa atividade de helicópteros e complexidade da infraestrutura "
        "urbana torna São Paulo um ambiente relevante para o desenvolvimento de soluções de "
        "inteligência geoespacial baseadas em IA.\n\n"

        "Ao transformar imagens de satélite em informações espaciais estruturadas, o projeto "
        "demonstra como a Visão Computacional pode contribuir para análise urbana, mapeamento "
        "de infraestrutura e apoio à tomada de decisão em aplicações futuras de cidades inteligentes.\n\n"

        "O fluxo completo de IA inclui:\n\n"
        "• Coleta de dados públicos\n\n"
        "• Obtenção de imagens de satélite\n\n"
        "• Anotação manual no Roboflow\n\n"
        "• Treinamento de modelos YOLOv8n / YOLOv11n\n\n"
        "• Validação em campo com mais de **7.900** mosaicos reais\n\n"
    ),
},

"about.body_closing": {
    "en": (
        "This dashboard provides transparent access to the AI pipeline, dataset, model performance, "
        "and documented limitations."
    ),
    "pt": (
        "Este dashboard apresenta de forma transparente o pipeline de IA, o conjunto de dados, "
        "o desempenho do modelo e suas limitações documentadas."
    ),
},

"about.institution": {"en": "Institution", "pt": "Instituição"},
"about.program": {"en": "Program", "pt": "Curso"},
"about.course": {"en": "Course", "pt": "Disciplina"},
"about.professor": {"en": "Professor", "pt": "Professor"},
"about.authors": {"en": "Author", "pt": "Autor"},

    
    # ---- Tab 7: Downloads ----
    "dl.subheader": {"en": "⬇️ Download Center", "pt": "⬇️ Central de Downloads"},
    "dl.caption": {
        "en": "Every file below is a real project artifact available for download directly from this repository. No placeholders, mock files, or dynamically generated content are used.",
        "pt": "Cada arquivo abaixo é um artefato real do projeto, disponível para download diretamente deste repositório. Nenhum placeholder, arquivo fictício ou conteúdo gerado dinamicamente é utilizado.",
    },
    "dl.executive_report": {"en": "**📄 Executive Report**", "pt": "**📄 Relatório Executivo**"},
    "dl.exec_en_button": {"en": "⬇️ Executive Report (English, PDF)", "pt": "⬇️ Relatório Executivo (Inglês, PDF)"},
    "dl.exec_pt_button": {"en": "⬇️ Relatório Executivo (Português, PDF)", "pt": "⬇️ Relatório Executivo (Português, PDF)"},
    "dl.not_found": {"en": "Not found: `{path}`", "pt": "Não encontrado: `{path}`"},
    "dl.dataset_metrics": {"en": "**📦 Dataset & Metrics**", "pt": "**📦 Dataset & Métricas**"},
    "dl.dataset_button": {"en": "⬇️ Annotated Dataset (.rar)", "pt": "⬇️ Dataset Anotado (.rar)"},
    "dl.metrics_button": {"en": "⬇️ Experiment Metrics (.csv)", "pt": "⬇️ Métricas dos Experimentos (.csv)"},
    "dl.no_metrics": {
        "en": "No experiment metrics available yet to export.",
        "pt": "Ainda não há métricas de experimentos disponíveis para exportar.",
    },
    "dl.field_validation": {"en": "**🌍 Field Validation**", "pt": "**🌍 Validação de Campo**"},
    "dl.field_json_button": {"en": "⬇️ Detection Summary by Region (.json)", "pt": "⬇️ Resumo de Detecção por Região (.json)"},
    "dl.field_log_button": {"en": "⬇️ Field Triage Log (.txt)", "pt": "⬇️ Log de Triagem de Campo (.txt)"},
    "dl.session_summary.title": {"en": "📄 This session's summary", "pt": "📄 Resumo desta sessão"},
    "dl.session_summary.body": {
        "en": "A quick one-page PDF snapshot — active model, confidence threshold, experiment table, and field-validation totals — handy to attach without regenerating the full report.",
        "pt": "Um instantâneo rápido de uma página em PDF — modelo ativo, confiança mínima, tabela de experimentos e totais da validação de campo — útil pra anexar sem regenerar o relatório completo.",
    },
    "dl.session_summary.button": {"en": "🧾 Generate summary", "pt": "🧾 Gerar resumo"},
    "dl.session_summary.download_button": {"en": "⬇️ Download session summary (.pdf)", "pt": "⬇️ Baixar resumo da sessão (.pdf)"},
    "dl.music.title": {"en": "🎵 Soundtrack", "pt": "🎵 Trilha sonora"},
    "dl.music.body": {
        "en": "The background track used throughout this dashboard and the executive presentation.",
        "pt": "A faixa de fundo usada em todo o dashboard e na apresentação executiva.",
    },
    "dl.music.download_button": {"en": "⬇️ Download track (.mp3)", "pt": "⬇️ Baixar faixa (.mp3)"},
    "dl.music.missing": {"en": "Audio file not found at `{path}`.", "pt": "Arquivo de áudio não encontrado em `{path}`."},
    "dl.music.credit": {"en": "Passacaglia — Handel, 1708 (Deep House Remix)", "pt": "Passacaglia — Handel, 1708 (Deep House Remix)"},
    "dl.music.poem_l1": {
        "en": "The past may be our foundation,",
        "pt": "O passado pode ser nosso alicerce,",
    },
    "dl.music.poem_l2": {
        "en": "but it doesn't have to be our destiny.",
        "pt": "mas não precisa ser nosso destino.",
    },
    "dl.music.poem_l3": {
        "en": "We don't erase what came before.",
        "pt": "Não apagamos o que veio antes.",
    },
    "dl.music.poem_l4": {
        "en": "We transform it into what comes next.",
        "pt": "Nós o transformamos naquilo que vem a seguir.",
    },

    # ---- Opening epigraph (before the title) and closing echo (in the
    # footer) — a condensed, bookending version of the Passacaglia poem
    # above, framing the project conceptually before the data and
    # resolving it again at the end. ----
    "epigraph.credit": {"en": "𝄢 Passacaglia — Handel, 1708 · Deep House Remix", "pt": "𝄢 Passacaglia — Handel, 1708 · Deep House Remix"},
    "epigraph.line1": {
        "en": "The past may be our foundation, but it doesn't have to be our destiny.",
        "pt": "O passado pode ser nosso alicerce, mas não precisa ser nosso destino.",
    },
    "epigraph.line2": {
        "en": "We don't erase what came before — we transform it into what comes next.",
        "pt": "Não apagamos o que veio antes — nós o transformamos naquilo que vem a seguir.",
    },
    "epigraph.echo": {
        "en": "What remains gives us the ground to imagine what comes next.",
        "pt": "O que permanece nos dá a base para imaginar o que vem a seguir.",
    },
    "dl.repo_title": {"en": "Explore the full source code", "pt": "Explore o código-fonte completo"},
    "dl.repo_desc": {
        "en": "Architecture, datasets, notebooks, and the complete AI pipeline are all on GitHub.",
        "pt": "Arquitetura, datasets, notebooks e o pipeline completo de IA estão todos no GitHub.",
    },

    # ---- Metrics tab ----
    "metrics.subheader": {"en": "📊 Experiment Metrics", "pt": "📊 Métricas dos Experimentos"},
    "metrics.comparison_title": {
        "en": "#### 📋 Side-by-Side Comparison", "pt": "#### 📋 Comparação Lado a Lado"
    },
    "metrics.no_csv": {
        "en": "No `results.csv` found yet under `artifacts/runs/detect/*/` (or `artifacts/runs/runs/detect/*/`).",
        "pt": "Nenhum `results.csv` encontrado ainda em `artifacts/runs/detect/*/` (ou `artifacts/runs/runs/detect/*/`).",
    },
    "metrics.best_epoch": {"en": "Best epoch:", "pt": "Melhor época:"},
    "metrics.netron_view": {"en": "🔎 Open in Netron (new tab)", "pt": "🔎 Abrir no Netron (nova aba)"},
    "metrics.netron_manual": {"en": "🔎 Open Netron (upload manually)", "pt": "🔎 Abrir Netron (upload manual)"},
    "metrics.netron_expander": {"en": "🧠 Preview architecture inline", "pt": "🧠 Prévia da arquitetura aqui"},
    "metrics.netron_load_button": {"en": "▶ Load preview (fetches from netron.app)", "pt": "▶ Carregar prévia (busca do netron.app)"},
    "metrics.outperformed": {
        "en": "**{exp}** outperformed exp1 on mAP@50-95 ({delta}).",
        "pt": "**{exp}** superou o exp1 em mAP@50-95 ({delta}).",
    },
    "metrics.underperformed": {
        "en": "**{exp}** scored lower than exp1 on mAP@50-95 ({delta}) — possible overfitting.",
        "pt": "**{exp}** teve resultado inferior ao exp1 em mAP@50-95 ({delta}) — possível overfitting.",
    },
    "metrics.tied": {
        "en": "**{exp}** is essentially tied with exp1 (Δ {delta}).",
        "pt": "**{exp}** está essencialmente empatado com o exp1 (Δ {delta}).",
    },
    "metrics.evolution": {"en": "#### 📈 Metric evolution per epoch", "pt": "#### 📈 Evolução da métrica por época"},
    "metrics.metric_label": {"en": "Metric", "pt": "Métrica"},
    "metrics.epoch": {"en": "Epoch", "pt": "Época"},
    "metrics.confusion_matrix": {"en": "#### 🔀 Confusion matrix", "pt": "#### 🔀 Matriz de confusão"},
    "metrics.experiment_label": {"en": "Experiment", "pt": "Experimento"},
    "metrics.cm_not_found": {"en": "confusion_matrix.png not found at: `{path}`", "pt": "confusion_matrix.png não encontrado em: `{path}`"},
    "metrics.cm_norm_not_found": {"en": "confusion_matrix_normalized.png not found at: `{path}`", "pt": "confusion_matrix_normalized.png não encontrado em: `{path}`"},
    "metrics.cm_caption": {"en": "confusion matrix", "pt": "matriz de confusão"},
    "metrics.cm_norm_caption": {"en": "normalized", "pt": "normalizada"},

    # ---- Field detections tab ----
    "field.subheader": {"en": "🌍 Field Detections by Region (real-world tiles)", "pt": "🌍 Detecções de Campo por Região (tiles reais)"},
    "field.last_updated": {"en": "🕒 Last updated: {date}", "pt": "🕒 Última atualização: {date}"},
    "field.no_summary": {
        "en": "No field-detection summary found yet at `{path}`. Run `src/geospatial/auto_triage_regions.py` to generate it.",
        "pt": "Nenhum resumo de detecção de campo encontrado ainda em `{path}`. Rode `src/geospatial/auto_triage_regions.py` para gerá-lo.",
    },
    "field.detected_total": {"en": "Helipads detected (total)", "pt": "Helipontos detectados (total)"},
    "field.tiles_processed": {"en": "Tiles processed", "pt": "Tiles processados"},
    "field.overall_rate": {"en": "Overall detection rate", "pt": "Taxa de detecção geral"},
    "field.detection_rate_pct": {"en": "Detection rate (%)", "pt": "Taxa de detecção (%)"},
    "field.rank_col": {"en": "Rank", "pt": "Ranking"},
    "field.segments_combined_suffix": {
        "en": " (Segments 1+2 combined)", "pt": " (Trechos 1+2 combinados)"
    },
    "field.region_col": {"en": "Region", "pt": "Região"},
    "field.tiles_col": {"en": "Tiles", "pt": "Tiles"},
    "field.detected_col": {"en": "Detected", "pt": "Detectado"},
    "field.rate_col": {"en": "Detection Rate", "pt": "Taxa de Detecção"},
    "field.top_confidence_col": {"en": "Top Confidence", "pt": "Confiança Máxima"},
    "field.ranking_title": {
        "en": "🏆 Ranking — Helipads Found by Region", "pt": "🏆 Ranking — Helipontos Encontrados por Região"
    },
    "field.rate_definition": {
        "en": "**Rank** here follows the raw number of helipads found (**Detected**), highest to lowest — not **Detection Rate**, which is Detected ÷ Tiles for that region. A smaller region can show a higher rate with fewer total finds than a larger one (e.g. Inter-Zone Corridor: 133 found, 27.7% rate vs. Itaim Bibi: 191 found, 25.5% rate) simply because it has fewer tiles overall.",
        "pt": "O **ranking** aqui segue o número bruto de helipontos encontrados (**Detectado**), do maior para o menor — não a **Taxa de Detecção**, que é Detectado ÷ Tiles daquela região. Uma região menor pode ter taxa maior com menos achados totais do que uma maior (ex: Inter-Zone Corridor: 133 encontrados, taxa de 27,7% vs. Itaim Bibi: 191 encontrados, taxa de 25,5%) simplesmente por ter menos tiles no total.",
    },
    "field.inter_zone_note": {
        "en": "ℹ️ **Inter-Zone Corridor**: a bounding box covering the transition area between "
              "neighboring corporate districts, rather than a single named neighborhood.",
        "pt": "ℹ️ **Inter-Zone Corridor**: uma bounding box cobrindo a área de transição entre "
              "distritos corporativos vizinhos, em vez de um único bairro nomeado.",
    },
    "field.compare.title": {
        "en": "🔬 Compare all 3 models on the same field validation",
        "pt": "🔬 Comparar os 3 modelos na mesma validação de campo",    },
    "field.compare.table_title": {
        "en": "#### Detection Rate by Region and Experiment",
        "pt": "#### Taxa de Detecção por Região e Experimento",
    },
    "field.compare.body": {
        "en": "Same 7,943 tiles across the same 10 regions, run separately with each experiment's "
              "weights — shows whether the model that scored best on the curated validation set "
              "actually generalizes as well once it meets real, uncurated satellite coverage.",
        "pt": "Os mesmos 7.943 tiles nas mesmas 10 regiões, rodados separadamente com os pesos de "
              "cada experimento — mostra se o modelo que teve a melhor nota no conjunto de "
              "validação curado realmente generaliza bem quando enfrenta cobertura de satélite "
              "real, sem curadoria prévia.",
    },
    "field.compare.reality_check": {
        "en": "exp1 leads the curated validation set on Precision (1.000) — but across these same "
              "7,943 field tiles, it detects roughly half as many real helipads as exp2 (9.6% vs. "
              "21.1% overall detection rate) and exp3 (17.9%). A model that looks best on a small, "
              "curated benchmark is not automatically the model that generalizes best in unfiltered, "
              "real-world coverage — exactly the kind of gap field validation exists to catch.",
        "pt": "O exp1 lidera o conjunto de validação curado em Precision (1.000) — mas, nos mesmos "
              "7.943 tiles de campo, detecta aproximadamente metade dos helipontos reais que o exp2 "
              "(9,6% vs. 21,1% de taxa geral de detecção) e o exp3 (17,9%). Um modelo que parece "
              "melhor num benchmark pequeno e curado não é automaticamente o que generaliza melhor "
              "em cobertura real, sem filtragem — exatamente o tipo de lacuna que a validação de "
              "campo existe para capturar.",
    },
    "field.compare.missing": {
        "en": "Not yet run in the field for: **{missing}** — only showing the experiment(s) with a summary file present.",
        "pt": "Ainda não rodado em campo para: **{missing}** — mostrando só o(s) experimento(s) com arquivo de resumo presente.",
    },

    # ---- Footer ----
    "footer.tagline": {"en": "🚁 *Finding hidden H's in the Concrete Jungle*", "pt": "🚁 *Encontrando \"H\"s escondidos na Selva de Pedra*"},
    "footer.line2": {"en": "One rooftop at a time. ⚡", "pt": "Um telhado de cada vez. ⚡"},
    "footer.line3": {"en": "SÃO PAULO • YOLO • ESRI WORLD IMAGERY", "pt": "SÃO PAULO • YOLO • ESRI WORLD IMAGERY"},
}


st.set_page_config(
    page_title="Helipad Detector • São Paulo",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# `.streamlit/config.toml` forces Streamlit's own theme colors to dark,
# but that alone doesn't stop the BROWSER's native "color-scheme" hint —
# a separate CSS-level signal that controls default rendering for form
# controls, scrollbars, and any color not explicitly set by our CSS. If
# the visitor's OS/browser is set to light mode, the browser still assumes
# `color-scheme: light` unless told otherwise, which can make text look
# washed out for light-mode visitors even with the theme forced. This
# forces the browser itself to treat the whole page as dark, regardless
# of the visitor's OS/browser preference.
st.markdown(
    "<style>:root, html, body { color-scheme: dark !important; }</style>",
    unsafe_allow_html=True,
)

# streamlit-folium's map components (used in the Map tab) are unreliable on
# the very first script execution of a session — they can mount with a 0-size
# viewport and stay blank until something triggers another rerun (this is why
# toggling Dark mode "fixed" it: the toggle itself causes a rerun). Rather
# than rely on the user accidentally triggering that fix, force exactly one
# automatic rerun on the first load of each session, before anything heavy
# renders, so every map is already past that broken first pass by the time
# the user actually sees the page.
if "_warmed_up" not in st.session_state:
    st.session_state["_warmed_up"] = True
    st.rerun()

st.markdown("""
    <style>
    .main-title {font-size: 42px !important; font-weight: bold; color: #1E3A8A; text-align: center;}
    .subtitle {text-align: center; color: #64748B; font-size: 18px; margin-bottom: 30px;}
    /* Subtle frame + vignette on every detection image (Sample Images,
       Upload, Search by Region) so satellite tiles read as part of the
       same designed piece instead of looking like raw, unstyled crops. */
    [data-testid="stImage"] img {
        border-radius: 10px;
        border: 1px solid rgba(20,184,166,0.28);
        box-shadow:
            inset 0 0 34px rgba(0,0,0,0.30),
            0 4px 18px rgba(0,0,0,0.35);
    }
    /* Same rounded, teal-bordered "netron box" outline applied to native
       Streamlit inputs that otherwise blend flat into the dark background:
       dropdowns (Metric / Experiment pickers), number inputs (Min/Max
       Longitude/Latitude), and the file-uploader's drop zone. */
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stNumberInput"] > div,
    [data-testid="stFileUploaderDropzone"] {
        border: 1px solid rgba(20,184,166,0.35) !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.25);
    }
    /* Same teal outline extended to every st.dataframe table in the app
       (Top 10 cities, Coordinate data, Field Detections, Experiment
       Metrics, etc.) and every st.expander panel — Streamlit's own default
       border on these is barely visible against the dark background, which
       read as an unstyled white/near-transparent edge next to everything
       else above that already gets this treatment. overflow:hidden clips
       the inner grid's own square corners to the rounded border instead of
       poking past it. */
    [data-testid="stDataFrame"],
    [data-testid="stExpander"] {
        border: 1px solid rgba(20,184,166,0.35) !important;
        border-radius: 10px !important;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.25);
    }
    /* Same teal outline on every button and download button (Downloads tab's
       "quadradinhos" — Annotated Dataset, Experiment Metrics, Detection
       Summary, Field Triage Log, etc., plus Play/Pause Music and the
       Search-by-Region buttons) — same reasoning as the tables/expanders
       above: these had no border at all against the dark background, which
       stood out as unstyled next to everything else. `> button` targets the
       actual clickable element inside Streamlit's wrapper div, which is
       where the visible edges are. */
    [data-testid="stDownloadButton"] > button,
    [data-testid="stButton"] > button {
        border: 1px solid rgba(20,184,166,0.35) !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.25);
    }
    .result-card {background-color: #f8fafc; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0;}
    .metric-card {
        background-color: #f8fafc;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        text-align: center;
        box-shadow: 0 3px 10px rgba(15, 23, 42, 0.08);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 24px rgba(15, 23, 42, 0.16);
    }
    .flow-step {
        border-radius: 16px;
        padding: 22px 20px 20px 20px;
        text-align: left;
        position: relative;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 3px 10px rgba(15, 23, 42, 0.12);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
        margin-bottom: 18px;
    }
    .flow-step:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 30px rgba(15, 23, 42, 0.28);
    }
    .flow-step .flow-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        border-radius: 999px;
        font-size: 12.5px;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .flow-step .flow-icon {
        font-size: 26px;
        margin-bottom: 8px;
        display: block;
    }
    .flow-step .flow-title {
        font-weight: 700; font-size: 15px; margin: 0 0 6px 0; line-height: 1.3;
    }
    .flow-step .flow-desc {
        font-size: 12.5px; margin: 0; line-height: 1.5; flex-grow: 1;
    }
    .flow-arrow {
        text-align: center; color: #cbd5e1; font-size: 16px; padding-top: 40px;
    }
    .dark-card {
        background: linear-gradient(135deg, #16213E 0%, #1E3A8A 100%);
        padding: 28px 26px;
        border-radius: 14px;
        border: 1px solid rgba(147, 197, 253, 0.25);
        box-shadow: 0 6px 22px rgba(15, 23, 42, 0.35), inset 0 1px 0 rgba(255,255,255,0.06);
        text-align: center;
    }
    .dark-card .repo-icon {
        font-size: 44px;
        display: block;
        text-align: center;
        margin: 0 auto 10px auto;
        line-height: 1;
    }
    .dark-card h4 {
        text-align: center;
        margin: 0 0 8px 0;
        color: #FFFFFF;
    }
    .sample-btn > button {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        font-weight: 600;
        border: none !important;
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

# ========================= COLOR HELPERS =========================
def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def _shade(hex_color: str, amount: float) -> str:
    """amount > 0 lightens toward white; amount < 0 darkens toward deep navy."""
    rgb = _hex_to_rgb(hex_color)
    target = _hex_to_rgb("#FFFFFF") if amount > 0 else _hex_to_rgb("#0B1220")
    factor = abs(amount)
    blended = tuple(int(c + (t - c) * factor) for c, t in zip(rgb, target))
    return _rgb_to_hex(blended)


def blue_scale(t: float) -> str:
    """Interpolates from deep navy (t=0, first step) to the project's teal
    accent (t=1, last step) — the same blue-to-teal family used across the
    dashboard's tables and metrics, but staying dark end-to-end so no card
    ever turns near-white and breaks the dark theme."""
    start, end = _hex_to_rgb("#1E3A8A"), _hex_to_rgb("#0E756D")
    return _rgb_to_hex(tuple(int(a + (b - a) * t) for a, b in zip(start, end)))


# ========================= MAP TILE PROVIDERS =========================
# Using explicit URL templates (instead of Folium's built-in preset strings
# like "CartoDB dark_matter") because Folium ignores the custom `name=` we
# pass for known presets and falls back to its own internal identifier
# (e.g. "cartodbdarkmatter") in the layer control. A raw URL template has no
# such special-casing, so our friendly name is always used.
#
# NOTE (basemap provider history): this used to point at CartoDB's free
# endpoint, then briefly at Esri's "Canvas" gray basemaps. Both were dropped:
#   - CartoDB's free/anonymous endpoint now requires an account + API key;
#     without one it silently serves tiles stamped with an "API KEY
#     REQUIRED" watermark instead of erroring out.
#   - Esri's Canvas Dark/Light Gray basemaps are a generalized cartographic
#     style (not real street-level data) with a native max zoom around 16;
#     zooming past that returned an explicit "Map data not yet available"
#     placeholder tile instead of the requested imagery, and even at their
#     native max zoom, street names were already sparse/abstracted.
# OpenStreetMap's own raster tile server is used instead: real, detailed
# street-level cartography (actual OSM road/place data, not a generalized
# style) with genuine tile coverage up to zoom 19 almost everywhere, no
# account/key needed. It ships one style (light), so "dark mode" is done
# with a CSS filter (`invert` + `hue-rotate`) applied only to the tile pane
# of a given map instance — a standard, widely-used technique — which never
# touches markers/popups/labels since those live in separate Leaflet panes.
OSM_TILE_URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
OSM_ATTR = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
OSM_MAX_ZOOM = 19
# Applied via a scoped <style> (per Folium map container id) rather than a
# global rule, so it only affects the specific map it's added to.
OSM_DARK_FILTER_CSS = "invert(1) hue-rotate(180deg) brightness(0.95) contrast(0.9) saturate(0.85)"


def add_osm_tile_layer(fmap: "folium.Map", dark_mode: bool, name: str | None = None,
                        control: bool = True, container_id: str | None = None) -> None:
    """Adds the OpenStreetMap base layer to `fmap` and, if dark_mode, injects
    a CSS filter scoped to that map's own container so only its tile pane is
    inverted — other maps on the same page and this map's own markers/popups
    are unaffected.

    `container_id`: which DOM id to scope the filter to. Matters because the
    two ways this app renders a folium.Map end up with DIFFERENT real ids:
      - st_folium(fmap, ...) (the main Maps-tab map): confirmed directly in
        streamlit-folium's own frontend bundle that it hardcodes the map into
        a div with id="map_div", discarding whatever fmap.get_name() was.
        Pass container_id="map_div" for anything rendered this way.
      - components.html(fmap.get_root().render(), ...) (the density map):
        keeps Folium's own generated id, so fmap.get_name() (the default
        here) is correct.
    Getting this wrong doesn't error — the <style> tag still renders, it just
    never matches anything, so the map silently stays in light mode. That's
    exactly what was happening on the main map before this fix.
    """
    folium.TileLayer(
        tiles=OSM_TILE_URL, attr=OSM_ATTR, name=(name or "OpenStreetMap"),
        max_zoom=OSM_MAX_ZOOM, control=control,
    ).add_to(fmap)
    if dark_mode:
        scope_id = container_id or fmap.get_name()
        fmap.get_root().html.add_child(folium.Element(
            f"<style>#{scope_id} .leaflet-tile-pane "
            f"{{ filter: {OSM_DARK_FILTER_CSS}; }}</style>"
        ))





def _force_leaflet_resize(fmap: folium.Map) -> None:
    """Leaflet maps rendered inside a container that isn't fully laid out yet
    (e.g. below a heavier component that's still mounting, like the main map
    above this one) can compute a 0-size viewport and stay blank until
    something forces a relayout — this is what was happening with the
    Density view map, which only appeared after toggling Dark mode (that
    toggle triggers a rerun that happens to fix it). A single delayed resize
    event wasn't reliable enough, so this calls invalidateSize() directly on
    the actual Leaflet map instance, retried at a few increasing delays and
    again on window 'load', to reliably catch whichever moment the container
    finishes settling."""
    map_var = fmap.get_name()
    fmap.get_root().html.add_child(folium.Element(f"""
    <script>
    (function() {{
        function fixSize() {{
            if (typeof {map_var} !== 'undefined') {{
                {map_var}.invalidateSize();
            }}
        }}
        [100, 300, 700, 1200, 2000].forEach(function(ms) {{ setTimeout(fixSize, ms); }});
        window.addEventListener('load', fixSize);
    }})();
    </script>
    """))


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
EXEC_REPORT_EN = Path("reports/helipad_detector_full_report/🇬🇧Helipad_Detector_Full_Report.pdf")
EXEC_REPORT_PT = Path("reports/helipad_detector_full_report/🇧🇷Helipad_Detector_Relatorio_Completo.pdf")
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


@st.cache_resource(show_spinner="🚁 Loading YOLO weights and warming up the detector...")
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


_DMS_NUM = r"[-+]?\d+(?:\.\d+)?"
_DMS_COORD_RE = re.compile(
    rf"""
    (?P<g>{_DMS_NUM})\s*[°ºo]?\s*
    (?:(?P<m>{_DMS_NUM})\s*['’′]?\s*)?
    (?:(?P<s>{_DMS_NUM})\s*["”″]?\s*)?
    (?P<dir>[NSEWnsew])?
    """,
    re.VERBOSE,
)


def _dms_to_dd(graus: float, minutos: float, segundos: float, direcao: str = "") -> float:
    dd = abs(graus) + minutos / 60 + segundos / 3600
    if direcao.upper() in ("S", "W") or graus < 0:
        dd = -dd
    return dd


def _parse_dms_point(texto: str):
    """Same DMS-pair regex/logic as src/geospatial/transform_coordinates.py's
    parse_dms_pair, reused here as a fallback for rows that were scraped by
    helipad_bot.py but never actually run through transform_coordinates.py —
    i.e. still a raw 'DD°MM'SS"H DD°MM'SS"H' pair instead of the converted
    'lon_min lat_min lon_max lat_max' bbox format. Returns a single (lat, lon)
    point directly rather than fabricating a bounding box, since the only
    thing load_helipad_locations ever does with the box is average it back
    down to a center point anyway."""
    coords = []
    for m in _DMS_COORD_RE.finditer(str(texto)):
        if m.group("g") is None or m.group(0).strip() == "":
            continue
        graus = float(m.group("g"))
        minutos = float(m.group("m")) if m.group("m") else 0.0
        segundos = float(m.group("s")) if m.group("s") else 0.0
        direcao = m.group("dir") or ""
        coords.append(_dms_to_dd(graus, minutos, segundos, direcao))
    if len(coords) < 2:
        return None, None
    return coords[0], coords[1]  # lat, lon


@st.cache_data(show_spinner=False)
def load_helipad_locations(csv_path: Path = COORDS_CSV) -> pd.DataFrame:
    """Reads a helipad-coordinates CSV (same schema as helipad_coordinates_bbox.csv)
    and computes the center point (lat, lon) of each bounding box, for the map view.

    Some rows in this CSV are the direct output of helipad_bot.py's scraper
    but were never run through transform_coordinates.py's DMS-to-decimal
    conversion (or that step failed silently for them), so they're still raw
    'DD°MM'SS"H DD°MM'SS"H' pairs rather than a converted bounding box. Those
    used to be dropped by the bbox parser below and silently vanish from
    every map in the app — confirmed against the project's own
    helipad_coordinates.csv: 80 of 129 rows (62%) were still in this raw
    format, including a 7-point Belo Horizonte cluster that never showed up
    on the Discovery Dataset map. parse_center() now falls back to the same
    DMS parser transform_coordinates.py uses, so those rows render too
    instead of requiring the conversion script to be re-run first.
    """
    if not csv_path.exists():
        return pd.DataFrame()

    def parse_center(raw: str):
        parts = str(raw).replace(",", " ").split()
        try:
            lon_min, lat_min, lon_max, lat_max = (float(p) for p in parts[:4])
            return (lat_min + lat_max) / 2, (lon_min + lon_max) / 2
        except Exception:
            pass
        return _parse_dms_point(raw)

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


@st.cache_data(show_spinner=False)
def load_discovery_dataset_stats(csv_path: Path = COORDS_CSV) -> dict | None:
    """Quick coverage summary of the national helipad-discovery dataset
    (src/geospatial/helipad_bot.py output) — total points collected and
    how many distinct location names appear, as a proxy for geographic
    diversity. If src/geospatial/geocode_states.py has been run, its output
    CSV (helipad_coordinates_com_estado.csv, next to csv_path) is picked up
    here too and grouped into "by_state" counts — this is what lets the
    About tab replace its "State-by-state breakdown pending" caption with
    real numbers once that script has actually been run."""
    if not csv_path.exists():
        return None
    try:
        df = pd.read_csv(csv_path)
    except Exception:
        return None
    bairro_col = "Nome do Bairro" if "Nome do Bairro" in df.columns else None
    stats = {
        "total_points": len(df),
        "distinct_locations": df[bairro_col].nunique() if bairro_col else None,
        "by_state": None,
    }

    by_state_path = csv_path.parent / "helipad_coordinates_com_estado.csv"
    if by_state_path.exists():
        try:
            state_df = pd.read_csv(by_state_path)
            if "Estado" in state_df.columns:
                counts = state_df["Estado"].fillna("").replace("", "(desconhecido)").value_counts()
                stats["by_state"] = counts.to_dict()
        except Exception:
            pass  # malformed/partial CSV — fall back to the pending caption, don't crash the tab

    return stats


def build_session_summary_pdf(metrics_df: pd.DataFrame, selected_model, conf_threshold, lang: str) -> bytes:
    """One-page PDF snapshot of the current dashboard session — active
    model, confidence threshold, the full experiment comparison table, and
    field-validation totals if available. Meant as something quick to
    attach to an email or the repo without regenerating the full 25-page
    Word report every time a small thing changes."""
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import cm

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter, topMargin=2 * cm, bottomMargin=2 * cm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("HeliTitle", parent=styles["Title"], textColor=colors.HexColor("#0E756D"))
    h2_style = ParagraphStyle("HeliH2", parent=styles["Heading2"], textColor=colors.HexColor("#1E3A8A"),
                               spaceBefore=14, spaceAfter=6)
    body_style = styles["Normal"]

    is_pt = lang == "pt"
    story = []

    story.append(Paragraph("🚁 Helipad Detector", title_style))
    story.append(Paragraph(
        "Session summary — Helipad Detector dashboard" if not is_pt else "Resumo de sessão — dashboard Helipad Detector",
        styles["Heading3"]))
    story.append(Paragraph(datetime.now().strftime("%Y-%m-%d %H:%M"), body_style))
    story.append(Spacer(1, 14))

    story.append(Paragraph("Active configuration" if not is_pt else "Configuração ativa", h2_style))
    config_rows = [
        ["Model" if not is_pt else "Modelo", str(selected_model) if selected_model else "—"],
        ["Confidence threshold" if not is_pt else "Confiança mínima", f"{conf_threshold:.2f}" if conf_threshold is not None else "—"],
        ["Language" if not is_pt else "Idioma", "Português" if is_pt else "English"],
    ]
    config_table = Table(config_rows, colWidths=[6 * cm, 9 * cm])
    config_table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#0E756D")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    story.append(config_table)

    if not metrics_df.empty:
        story.append(Paragraph("Experiments" if not is_pt else "Experimentos", h2_style))
        cols = ["Experiment", "Best Epoch", "Total Epochs", "Precision", "Recall", "mAP@50", "mAP@50-95"]
        available_cols = [c for c in cols if c in metrics_df.columns]
        table_data = [available_cols] + metrics_df[available_cols].astype(str).values.tolist()
        exp_table = Table(table_data, colWidths=[2.1 * cm] * len(available_cols))
        exp_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0E756D")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ]))
        story.append(exp_table)

    field_summary = load_field_detection_summary()
    if field_summary:
        story.append(Paragraph("Field validation" if not is_pt else "Validação de campo", h2_style))
        try:
            total_tiles = sum(r.get("total_tiles", 0) for r in field_summary.values())
            total_detected = sum(r.get("detected", 0) for r in field_summary.values())
            rate = (total_detected / total_tiles * 100) if total_tiles else 0
            story.append(Paragraph(
                f"{total_detected} / {total_tiles} tiles ({rate:.1f}%) across {len(field_summary)} regions"
                if not is_pt else
                f"{total_detected} / {total_tiles} tiles ({rate:.1f}%) em {len(field_summary)} regiões",
                body_style))
        except Exception:
            pass

    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "Generated from the Helipad Detector Streamlit dashboard — PUC-SP FACEI, Machine Learning / Computer Vision, Project P2."
        if not is_pt else
        "Gerado a partir do dashboard Streamlit do Helipad Detector — PUC-SP FACEI, Machine Learning / Visão Computacional, Projeto P2.",
        ParagraphStyle("Footer", parent=body_style, fontSize=8, textColor=colors.HexColor("#64748B"))))

    doc.build(story)
    return buf.getvalue()


def get_selected_model():
    if not MODEL_OPTIONS:
        return None
    label = st.session_state.get("model_choice") or next(iter(MODEL_OPTIONS))
    return load_model(str(MODEL_OPTIONS[label]))


def slugify_region(name: str) -> str:
    """Matches the slug format used by src/geospatial/download_all_regions.py
    and auto_triage_regions.py, so map markers can be joined with the
    per-region detection summary by name."""
    return str(name).strip().replace(" ", "_").replace("/", "-").replace("(", "").replace(")", "")


# Approximate coordinates of the capital of each state helipad_bot.py is
# configured to search (see DEFAULT_ESTADOS in src/geospatial/helipad_bot.py),
# used only to add a city hint to Discovery Dataset marker labels. A bairro
# name alone can be ambiguous — e.g. "Centro" showed up for Rio de Janeiro,
# and could just as easily show up for Belo Horizonte or Fortaleza in a
# future scrape — but its coordinates aren't. This is a label hint for
# readability, not a claim about which municipality a point administratively
# belongs to: if no capital is within CITY_HINT_RADIUS_DEG, no hint is added
# rather than guessing one.
BRAZIL_STATE_CAPITALS = {
    "Rio de Janeiro": (-22.9068, -43.1729),
    "Belo Horizonte": (-19.9167, -43.9345),
    "Porto Alegre": (-30.0346, -51.2177),
    "Curitiba": (-25.4284, -49.2733),
    "Salvador": (-12.9714, -38.5014),
    "Fortaleza": (-3.7172, -38.5433),
    "Goiânia": (-16.6869, -49.2648),
    "Florianópolis": (-27.5954, -48.5480),
    "Recife": (-8.0476, -34.8770),
    "Brasília": (-15.7939, -47.8828),
    "Manaus": (-3.1190, -60.0217),
    "Belém": (-1.4558, -48.5039),
    "Vitória": (-20.3155, -40.3128),
    "Cuiabá": (-15.6014, -56.0979),
    "Campo Grande": (-20.4697, -54.6201),
}
CITY_HINT_RADIUS_DEG = 0.6  # ~65 km — the city + close metro area, not the whole state


def city_hint(lat: float, lon: float) -> str | None:
    """Nearest state capital within CITY_HINT_RADIUS_DEG, or None if the
    point is too far from any of them to guess responsibly."""
    best_city, best_dist = None, CITY_HINT_RADIUS_DEG
    for city, (clat, clon) in BRAZIL_STATE_CAPITALS.items():
        dist = ((lat - clat) ** 2 + (lon - clon) ** 2) ** 0.5
        if dist < best_dist:
            best_city, best_dist = city, dist
    return best_city


@st.cache_data(show_spinner=False)
def load_state_lookup(csv_path: Path = COORDS_CSV) -> dict:
    """Reads src/geospatial/helipad_coordinates_com_estado.csv (produced by
    geocode_states.py) if it exists, keyed by the raw 'Coordenadas da
    Bounding Box' string — a stable, unique-per-point join key that doesn't
    depend on row order matching between this file and the main coordinates
    CSV. Used as a fallback wherever city_hint() comes back empty: a point
    can be too far from any of the 15 hardcoded state capitals to guess a
    *city* responsibly (city_hint's job), while still having a known
    *state* from geocode_states.py's real Nominatim lookup — a materially
    more precise, distance-independent source for that one field."""
    state_csv = csv_path.parent / "helipad_coordinates_com_estado.csv"
    if not state_csv.exists():
        return {}
    try:
        df = pd.read_csv(state_csv)
        if "Coordenadas da Bounding Box" not in df.columns or "Estado" not in df.columns:
            return {}
        return dict(zip(df["Coordenadas da Bounding Box"], df["Estado"]))
    except Exception:
        return {}


def location_hint(lat: float, lon: float, raw_bbox: str, state_lookup: dict) -> str | None:
    """Best available human-readable hint for a Discovery Dataset point:
    nearest state capital if close enough (city_hint), otherwise the real
    geocoded state from geocode_states.py's output if that's been run,
    otherwise None (let the caller decide how to render "we don't know")."""
    hint = city_hint(lat, lon)
    if hint:
        return hint
    state = state_lookup.get(raw_bbox)
    return state if isinstance(state, str) and state.strip() else None


# Region names that need a specific English translation, not just a literal
# word swap (display-only — source CSV/folder names are untouched).
REGION_NAME_TRANSLATIONS = {
    "inter zonas": "Inter-Zone Corridor",
}


def format_region_display(name: str) -> str:
    """Human-friendly display name for a region, regardless of whether it
    comes from a raw CSV name (e.g. 'Av_Paulista (trecho 1)') or a JSON
    slug (e.g. 'Av_Paulista_trecho_1'). Display-only — does not rename any
    file, folder, or CSV entry. Follows the active language: 'Segment N'
    in English, 'Trecho N' in Português (e.g. 'Av Paulista Trecho 1')."""
    word = "Trecho" if st.session_state.get("lang") == "pt" else "Segment"
    display = str(name).replace("_", " ")
    display = re.sub(r"\btrecho\b", word, display, flags=re.IGNORECASE)
    display = re.sub(r"\s+", " ", display).strip()
    translated = REGION_NAME_TRANSLATIONS.get(display.lower())
    return translated if translated else display


def detection_rate_to_color(rate: float, min_rate: float, max_rate: float) -> str:
    """Maps a detection rate to a hex color on a light-to-dark blue scale,
    matching the same Blues gradient used in the Experiment/Field tables."""
    if max_rate <= min_rate:
        t = 0.5
    else:
        t = (rate - min_rate) / (max_rate - min_rate)
    t = max(0.0, min(1.0, t))
    # light blue (#dbeafe) -> navy (#1E3A8A)
    light = (0xDB, 0xEA, 0xFE)
    dark = (0x1E, 0x3A, 0x8A)
    rgb = tuple(int(light[i] + (dark[i] - light[i]) * t) for i in range(3))
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def readable_text_color(hex_color: str) -> str:
    """Black or white, whichever reads better on top of hex_color — used to
    keep the detection-rate tooltip's text legible across the full range of
    detection_rate_to_color's light-blue-to-navy gradient (light backgrounds
    need dark text, navy backgrounds need white text)."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#0a1f2b" if luminance > 0.55 else "#ffffff"


def rate_popup_html(inner_html: str, bg_color: str, text_color: str) -> str:
    """Wraps popup content in a div that bleeds into Leaflet's default popup
    padding (negative margin) so the popup's visible content area reads as
    fully colored, not just white-with-colored-text. Leaflet's own
    .leaflet-popup-content-wrapper chrome (rounded corners, drop shadow,
    little tip/arrow) stays its default white — Folium doesn't expose a
    stable per-popup id to scope a CSS override at that layer — but this
    covers the entire readable content area, which is what actually carries
    the color signal."""
    return (
        f'<div style="background:{bg_color}; color:{text_color}; '
        f'margin:-13px -20px; padding:12px 18px; border-radius:10px;">'
        f'{inner_html}</div>'
    )


# ========================= FIELD DETECTIONS BY REGION (data) =========================
# reports/detection_summary_by_region.json is generated by
# src/geospatial/auto_triage_regions.py. Defined here (before it's first used
# in the Map tab) so both the Map tab and the Field Detections tab can read it.
FIELD_SUMMARY_PATH = Path("reports/detection_summary_by_region.json")

# Per-experiment field-validation summaries — same JSON shape as
# FIELD_SUMMARY_PATH above (that one is exp2, the model actually used for
# the "main" Field Detections view). exp1/exp3 are optional: if their
# files aren't present in the repo yet, the 3-way comparison section
# below simply doesn't render, no error.
FIELD_SUMMARY_PATHS_BY_EXP = {
    "exp1": Path("reports/detection_summary_by_region_exp1.json"),
    "exp2": FIELD_SUMMARY_PATH,
    "exp3": Path("reports/detection_summary_by_region_exp3.json"),
}


@st.cache_data(show_spinner=False)
def load_field_detection_summary():
    if not FIELD_SUMMARY_PATH.exists():
        return None
    try:
        with open(FIELD_SUMMARY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def load_field_summaries_by_exp() -> dict:
    """{exp_name: parsed_json} for every experiment whose field-validation
    summary file actually exists in reports/ — used to build the 3-model
    comparison table. Missing files are silently skipped."""
    out = {}
    for exp_name, path in FIELD_SUMMARY_PATHS_BY_EXP.items():
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    out[exp_name] = json.load(f)
            except Exception:
                pass
    return out


MODEL_OPTIONS = discover_models()

# {exp_dir.name: weights_path} — used to build "view architecture in
# Netron" links per experiment (Netron reads the file straight from its
# raw GitHub URL, no upload needed).
MODEL_WEIGHTS_BY_EXP = {exp_dir.name: (exp_dir / "weights" / "best.pt")
                         for exp_dir in _all_exp_dirs()
                         if (exp_dir / "weights" / "best.pt").exists()}

GITHUB_REPO_RAW_BASE = (
    "https://raw.githubusercontent.com/"
    "Mindful-AI-Research/3-project-ai-ml-yolo-helipad_detector/main"
)


def netron_url_for(exp_name: str) -> str | None:
    """Netron.app link that auto-loads a given experiment's best.pt
    straight from its raw GitHub URL — no manual upload needed. Returns
    None if that experiment's weights aren't tracked locally (Netron
    still works via plain https://netron.app + manual upload in that case)."""
    weights_path = MODEL_WEIGHTS_BY_EXP.get(exp_name)
    if not weights_path:
        return None
    raw_url = f"{GITHUB_REPO_RAW_BASE}/{weights_path.as_posix()}"
    return f"https://netron.app/?url={raw_url}"

# ========================= BACKGROUND MUSIC (sidebar widget) =========================
# Track: "Passacaglia – Deep House Remix" — used here for educational /
# academic-presentation purposes. Embedded as base64 so no separate static
# file server is needed; loops indefinitely once started. The app never
# autoplays audio (browsers block that anyway) — it always waits for the
# person to click the 🔇/🔊 icon below, which starts fully muted/paused.
AUDIO_PATH = Path("assets/audio/passacaglia-deep-house-remix.mp3")


@st.cache_data(show_spinner=False)
def _load_audio_base64(path: str):
    p = Path(path)
    if not p.exists():
        return None
    return base64.b64encode(p.read_bytes()).decode("ascii")


def render_music_toggle():
    audio_b64 = _load_audio_base64(str(AUDIO_PATH))
    st.markdown(f"### {t('sidebar.music.title')}")
    if not audio_b64:
        st.caption(t("sidebar.music.missing"))
        return

    label_play = t("sidebar.music.play")
    label_pause = t("sidebar.music.pause")

    components.html(f"""
    <button id="music-toggle-btn" title="{label_play}" style="
      width:100%; display:flex; align-items:center; justify-content:center; gap:10px;
      background:#0E756D; color:#fff; border:1.5px solid #14b8a6; border-radius:12px;
      padding:12px 14px; font-family:'Inter',sans-serif; font-size:14px; font-weight:700;
      letter-spacing:.02em; cursor:pointer; box-shadow:0 3px 14px rgba(14,117,109,.45);
      transition:transform .15s, box-shadow .2s; animation:music-pulse 2.2s ease-in-out infinite;
    ">
      <span id="music-icon" style="font-size:18px;">🔇</span>
      <span id="music-label">{label_play}</span>
    </button>
    <style>
      @keyframes music-pulse {{
        0%, 100% {{ box-shadow: 0 3px 14px rgba(14,117,109,.45); }}
        50% {{ box-shadow: 0 3px 22px rgba(20,184,166,.85); }}
      }}
      #music-toggle-btn:hover {{ transform: translateY(-1px); }}
      #music-toggle-btn.playing {{ animation: none; background:#134e4a; }}
    </style>
    <audio id="bg-music" src="data:audio/mp3;base64,{audio_b64}" loop preload="auto" muted></audio>
    <script>
      const btn = document.getElementById('music-toggle-btn');
      const icon = document.getElementById('music-icon');
      const label = document.getElementById('music-label');
      const audio = document.getElementById('bg-music');
      audio.volume = 0.35;
      let playing = false;

      function start() {{
        if (playing) return;
        audio.muted = false;
        audio.play().then(() => {{
          playing = true;
          icon.textContent = '🔊';
          btn.title = '{label_pause}';
          label.textContent = '{label_pause}';
          btn.classList.add('playing');
        }}).catch(() => {{}});
      }}
      function stop() {{
        audio.pause();
        playing = false;
        icon.textContent = '🔇';
        btn.title = '{label_play}';
        label.textContent = '{label_play}';
        btn.classList.remove('playing');
      }}

      btn.addEventListener('click', () => {{ playing ? stop() : start(); }});

      /* Auto-start on the very first interaction anywhere in the dashboard
         (click, tap, or key press) — not just a click on this button.
         The <audio> tag itself is muted/paused until then, so this never
         violates the browser's autoplay-with-sound policy; it just widens
         the trigger from "click this exact icon" to "do literally
         anything in the app". Listening on window.parent.document works
         because Streamlit's components.html iframe is same-origin with
         the main app (srcdoc without a sandbox override inherits the
         parent's origin) — if that ever changes in a future Streamlit
         version, this silently no-ops and the button above still works
         normally on its own. */
      try {{
        const parentDoc = window.parent.document;
        const startOnce = () => {{
          start();
          parentDoc.removeEventListener('click', startOnce, true);
          parentDoc.removeEventListener('keydown', startOnce, true);
          parentDoc.removeEventListener('touchstart', startOnce, true);
        }};
        parentDoc.addEventListener('click', startOnce, {{ once: true, capture: true }});
        parentDoc.addEventListener('keydown', startOnce, {{ once: true, capture: true }});
        parentDoc.addEventListener('touchstart', startOnce, {{ once: true, capture: true, passive: true }});
      }} catch (e) {{ /* cross-origin iframe — fallback: only the button click above starts the music */ }}
    </script>
    """, height=64)

    # Download lives right next to the player — one contextual music
    # experience in the sidebar (play + download together), instead of
    # a separate, disconnected download link buried in another tab.
    if AUDIO_PATH.exists():
        st.markdown(
            f"<p style='font-style:italic; font-size:12.5px; color:#9FB0B8; margin:10px 0 6px 0;'>"
            f"{t('sidebar.music.tagline')}</p>",
            unsafe_allow_html=True,
        )
        with open(AUDIO_PATH, "rb") as f:
            st.download_button(
                t("dl.music.download_button"),
                data=f,
                file_name="passacaglia-deep-house-remix.mp3",
                mime="audio/mpeg",
                use_container_width=True,
            )


# ========================= SIDEBAR: LANGUAGE + MODEL SELECTION =========================
with st.sidebar:
    lang_choice = st.radio(
        "Language / Idioma",
        options=["🇬🇧 English", "🇧🇷 Português"],
        index=0 if st.session_state["lang"] == "en" else 1,
        horizontal=True,
        label_visibility="collapsed",
        key="lang_radio",
    )
    st.session_state["lang"] = "en" if lang_choice.startswith("🇬🇧") else "pt"

    render_music_toggle()

    if "heli_paused" not in st.session_state:
        st.session_state["heli_paused"] = False

    with st.expander(t("sidebar.extras"), expanded=False):
        heli_col1, heli_col2 = st.columns(2)
        with heli_col1:
            if st.button("🚁 " + t("sidebar.replay_heli"), use_container_width=True):
                st.session_state["heli_replay_nonce"] += 1
                st.session_state["heli_paused"] = False
                st.rerun()
        with heli_col2:
            if st.button("🌀 " + t("sidebar.spin_heli"), use_container_width=True):
                st.session_state["heli_spin_nonce"] += 1
                st.rerun()

        pause_label = t("sidebar.resume_heli") if st.session_state["heli_paused"] else t("sidebar.pause_heli")
        pause_icon = "▶️" if st.session_state["heli_paused"] else "⏸️"
        if st.button(f"{pause_icon} {pause_label}", use_container_width=True):
            st.session_state["heli_paused"] = not st.session_state["heli_paused"]
            st.rerun()

    st.markdown(f"### {t('sidebar.model')}")
    if not MODEL_OPTIONS:
        st.warning(t("sidebar.no_model.warning"))
        st.session_state["model_choice"] = None
        conf_threshold = 0.25
    else:
        st.selectbox(
            t("sidebar.choose_experiment"),
            options=list(MODEL_OPTIONS.keys()),
            key="model_choice",
            help=t("sidebar.choose_experiment.help"),
        )
        conf_threshold = st.slider(
            t("sidebar.confidence"), min_value=0.05, max_value=0.95, value=0.25, step=0.05
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

# ---- Flying helicopter, present on every tab (self-contained iframe
# injecting into the PARENT document) ----
#
# Streamlit's tabs never trigger a script rerun — all tab content is
# already in the DOM at once, and switching tabs is purely a client-side
# CSS show/hide. So a Python-only "run once at the top" approach can never
# know when the user changes tabs. Instead: the iframe below injects a
# single persistent helicopter element straight into the PARENT document
# (works because a components.html iframe using srcdoc, without a sandbox
# override, inherits the parent's origin) with position:fixed, so it
# floats above every tab, plus a click-listener on Streamlit's tab
# buttons that restarts the flight animation whenever a different tab is
# selected. Matches BOTH role="tab" (the ARIA attribute BaseWeb always
# sets, most reliable) and data-baseweb="tab" (belt-and-suspenders) since
# relying on only one turned out to miss real clicks. The style/element/
# listener are only created once (guarded by DOM id) even though
# Streamlit re-executes this components.html call on every rerun; small
# "nonce" values let the sidebar buttons force a replay/spin on demand.
# Flight path now varies per tab (4 distinct paths, picked by the clicked
# tab's position — language-independent) and spins vary too (clockwise,
# counter-clockwise, or a double spin, chosen at random each time), so it
# reads as a helicopter actually patrolling the dashboard rather than one
# looping clip. See FLIGHTS/SPINS inside the injected script below.

if "heli_replay_nonce" not in st.session_state:
    st.session_state["heli_replay_nonce"] = 0
if "heli_spin_nonce" not in st.session_state:
    st.session_state["heli_spin_nonce"] = 0

components.html(f"""
<script>
(function() {{
  try {{
    var doc = window.parent.document;
    var flyNonce = "{st.session_state['heli_replay_nonce']}";
    var spinNonce = "{st.session_state['heli_spin_nonce']}";
    var isPt = "{st.session_state.get('lang', 'pt')}" === 'pt';
    var isPaused = {"true" if st.session_state.get("heli_paused") else "false"};

    if (!doc.getElementById('heli-flyby-style')) {{
      var style = doc.createElement('style');
      style.id = 'heli-flyby-style';
      style.textContent = `
        /* Four distinct flight paths — different height range, duration
           and number of undulations — so each tab feels like its own
           little flight instead of one animation repeating everywhere. */
        @keyframes heli-fly-v0 {{
          0%   {{ left: 0%;   top: 44px; transform: rotate(-4deg)  scale(1);    opacity: 0; }}
          8%   {{ opacity: 1; }}
          25%  {{ top: 30px;  transform: rotate(12deg)  scale(1.03); }}
          50%  {{ left: 48%;  top: 50px;  transform: rotate(-8deg)  scale(1); }}
          75%  {{ top: 28px;  transform: rotate(12deg)  scale(1.03); }}
          92%  {{ opacity: 1; }}
          100% {{ left: 94%;  top: 42px;  transform: rotate(-4deg)  scale(1);   opacity: 0; }}
        }}
        @keyframes heli-fly-v1 {{
          0%   {{ left: 0%;   top: 90px;  transform: rotate(-6deg)  scale(1);    opacity: 0; }}
          8%   {{ opacity: 1; }}
          20%  {{ top: 60px;  transform: rotate(10deg)  scale(1.04); }}
          40%  {{ top: 105px; transform: rotate(-12deg) scale(1); }}
          60%  {{ top: 65px;  transform: rotate(10deg)  scale(1.04); }}
          80%  {{ top: 100px; transform: rotate(-10deg) scale(1); }}
          92%  {{ opacity: 1; }}
          100% {{ left: 94%;  top: 70px;  transform: rotate(-5deg)  scale(1);   opacity: 0; }}
        }}
        @keyframes heli-fly-v2 {{
          0%   {{ left: 0%;   top: 56px; transform: rotate(-8deg)  scale(1);    opacity: 0; }}
          6%   {{ opacity: 1; }}
          30%  {{ left: 30%;  top: 36px;  transform: rotate(14deg)  scale(1.05); }}
          50%  {{ left: 50%;  top: 66px;  transform: rotate(-14deg) scale(1); }}
          70%  {{ left: 70%;  top: 36px;  transform: rotate(14deg)  scale(1.05); }}
          94%  {{ opacity: 1; }}
          100% {{ left: 96%;  top: 56px;  transform: rotate(-6deg)  scale(1);   opacity: 0; }}
        }}
        @keyframes heli-fly-v3 {{
          0%   {{ left: 0%;   top: 34px; transform: rotate(-3deg) scale(0.95); opacity: 0; }}
          10%  {{ opacity: 1; }}
          50%  {{ left: 48%;  top: 40px; transform: rotate(3deg)  scale(1.08); }}
          90%  {{ opacity: 1; }}
          100% {{ left: 94%;  top: 32px; transform: rotate(-3deg) scale(0.95); opacity: 0; }}
        }}
        @keyframes heli-spin-cw {{
          0%   {{ transform: rotate(0deg)   scale(1);    opacity: 1; }}
          85%  {{ transform: rotate(360deg) scale(1.15); opacity: 1; }}
          100% {{ transform: rotate(360deg) scale(1);    opacity: 0; }}
        }}
        @keyframes heli-spin-ccw {{
          0%   {{ transform: rotate(0deg)    scale(1);    opacity: 1; }}
          85%  {{ transform: rotate(-360deg) scale(1.15); opacity: 1; }}
          100% {{ transform: rotate(-360deg) scale(1);    opacity: 0; }}
        }}
        @keyframes heli-spin-double {{
          0%   {{ transform: rotate(0deg)   scale(1);    opacity: 1; }}
          90%  {{ transform: rotate(720deg) scale(1.2);  opacity: 1; }}
          100% {{ transform: rotate(720deg) scale(1);    opacity: 0; }}
        }}
        #heli-flyby-global {{
          position: fixed; left: 0; top: 64px; font-size: 52px; z-index: 999999;
          pointer-events: none;
          filter: drop-shadow(0 2px 6px rgba(0,0,0,.35));
        }}
        #heli-tab-toast {{
          position: fixed; left: 50%; bottom: 22px; transform: translate(-50%, 12px);
          background: rgba(10,14,20,0.85); color: #C9D6DE; font-size: 12.5px;
          font-family: 'Inter', 'Segoe UI', sans-serif; letter-spacing: .02em;
          padding: 7px 16px; border-radius: 999px; border: 1px solid rgba(20,184,166,0.35);
          pointer-events: none; z-index: 999998; opacity: 0;
          transition: opacity .35s ease, transform .35s ease;
          white-space: nowrap;
        }}
        #heli-tab-toast.show {{
          opacity: 1; transform: translate(-50%, 0);
        }}
      `;
      doc.head.appendChild(style);
    }}

    var heli = doc.getElementById('heli-flyby-global');
    if (!heli) {{
      heli = doc.createElement('div');
      heli.id = 'heli-flyby-global';
      heli.textContent = '🚁';
      heli.dataset.lastFlyNonce = flyNonce;   // don't fly again on the render that creates it — replayFlight() below handles the first flight
      heli.dataset.lastSpinNonce = spinNonce; // don't spin on creation, only on an actual button click later
      doc.body.appendChild(heli);
    }}

    var toast = doc.getElementById('heli-tab-toast');
    if (!toast) {{
      toast = doc.createElement('div');
      toast.id = 'heli-tab-toast';
      doc.body.appendChild(toast);
    }}
    var toastTimer = null;
    function showTabToast(tabLabel) {{
      var prefix = isPt ? '🚁 Sobrevoando ' : '🚁 Flying over ';
      toast.textContent = prefix + tabLabel + '...';
      toast.classList.add('show');
      if (toastTimer) clearTimeout(toastTimer);
      toastTimer = setTimeout(function() {{ toast.classList.remove('show'); }}, 2000);
    }}

    var FLIGHTS = [
      {{ name: 'heli-fly-v0', duration: 7  }},
      {{ name: 'heli-fly-v1', duration: 11 }},
      {{ name: 'heli-fly-v2', duration: 9  }},
      {{ name: 'heli-fly-v3', duration: 6  }},
    ];
    var SPINS = ['heli-spin-cw', 'heli-spin-ccw', 'heli-spin-double'];
    var currentFlightIdx = 0;

    function replayFlight(idx) {{
      if (typeof idx === 'number') currentFlightIdx = idx;
      var f = FLIGHTS[currentFlightIdx % FLIGHTS.length];
      heli.style.left = '0';
      heli.style.animation = 'none';
      void heli.offsetWidth; // force reflow so the restart actually takes effect
      heli.style.animation = f.name + ' ' + f.duration + 's cubic-bezier(.45,.05,.55,.95) infinite alternate';
    }}

    function spinFlight() {{
      if (isPaused) return;
      var spinName = SPINS[Math.floor(Math.random() * SPINS.length)];
      var rect = heli.getBoundingClientRect();
      heli.style.left = Math.max(10, Math.min(90, (rect.left / doc.documentElement.clientWidth) * 100)) + '%';
      heli.style.animation = 'none';
      void heli.offsetWidth;
      heli.style.animation = spinName + ' 2.2s ease-in-out 1 forwards';
      // resume the continuous flight loop once the spin finishes
      setTimeout(function() {{ replayFlight(); }}, 2300);
    }}

    // Applied on every run (cheap, idempotent) so the pause/resume button
    // takes effect immediately without needing its own nonce dance —
    // pausing freezes the animation exactly where it is via CSS
    // animation-play-state, rather than stopping/losing position.
    heli.style.animationPlayState = isPaused ? 'paused' : 'running';

    // First-ever mount: fly in once immediately, and keep flying forever
    // — every tab, no stopping — with an occasional smooth spin thrown in
    // automatically (not only from the sidebar button), like a helicopter
    // doing a lazy loop rather than a straight back-and-forth commute.
    if (heli.dataset.mounted !== '1') {{
      heli.dataset.mounted = '1';
      if (!isPaused) replayFlight(0);
      var scheduleAutoSpin = function() {{
        var delay = 18000 + Math.random() * 20000; // every ~18-38s
        setTimeout(function() {{
          spinFlight();
          scheduleAutoSpin();
        }}, delay);
      }};
      scheduleAutoSpin();
    }} else {{
      if (heli.dataset.lastFlyNonce !== flyNonce) {{
        heli.dataset.lastFlyNonce = flyNonce;
        if (!isPaused) replayFlight();
      }}
      if (heli.dataset.lastSpinNonce !== spinNonce) {{
        heli.dataset.lastSpinNonce = spinNonce;
        spinFlight();
      }}
    }}

    if (!doc.body.dataset.heliListenerAttached) {{
      doc.body.dataset.heliListenerAttached = '1';
      // Thematic mapping by tab position (About, Metrics, Field, Map,
      // Search, Samples, Upload, Pipeline, Governance, Downloads): Map
      // and Governance get the slow, low "survey" path (v1) since they're
      // about surveying/overseeing; Field and Search get the looping
      // exploration path (v2); the rest get quicker, lighter passes.
      var TAB_FLIGHT_MAP = [3, 0, 2, 1, 2, 0, 3, 0, 1, 3];
      doc.addEventListener('click', function(e) {{
        var tabBtn = e.target.closest('[role="tab"], [data-baseweb="tab"]');
        if (!tabBtn) return;
        var allTabs = Array.prototype.slice.call(
          doc.querySelectorAll('[role="tab"], [data-baseweb="tab"]')
        );
        var idx = allTabs.indexOf(tabBtn);
        var flightIdx = (idx >= 0 && idx < TAB_FLIGHT_MAP.length) ? TAB_FLIGHT_MAP[idx] : (idx % FLIGHTS.length);
        if (!isPaused) replayFlight(flightIdx);
        showTabToast(tabBtn.textContent.trim());
      }}, true);
    }}
  }} catch (e) {{ /* cross-origin iframe — feature unavailable in this Streamlit setup */ }}
}})();
</script>
""", height=0)


# ---- Ambient starfield background, behind every tab (parent-document
# injection, same technique as the helicopter above) ----
#
# Matches the HTML presentation's visual identity (which renders its
# starfield with real Three.js/WebGL — 850 silver points at #C9D6DE).
# Both stars and particles use that same silver (#C9D6DE), not teal — the
# whole field reads as one coherent silver starfield, like the reference.
# Pulling an actual Three.js scene from a CDN into the parent document
# here would add a real external dependency and a new failure surface
# (CDN blocked, WebGL context denied, etc.) on top of everything already
# debugged for the helicopter — not worth the risk for a background
# decoration. This version reproduces the same *feel* — an orbiting,
# mouse-reactive camera drifting slowly through a silver starfield — using
# only CSS 3D transforms (perspective + rotateX/rotateY) driven by
# requestAnimationFrame, with zero external dependencies.
components.html("""
<script>
(function() {
  try {
    var doc = window.parent.document;
    if (doc.getElementById('starfield-style')) return;

    var style = doc.createElement('style');
    style.id = 'starfield-style';
    style.textContent = `
      /* Streamlit's own app containers have an opaque background by
         default, which sat ABOVE our z-index:-1 stage and hid it
         completely. Making those specific containers transparent lets
         the fixed starfield show through everywhere behind the actual
         widgets (which each keep their own opaque card/table backgrounds
         and stay perfectly readable on top). */
      .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"],
      [data-testid="stHeader"], .main, .block-container {
        background: transparent !important;
      }
      /* Force Streamlit's real content to stack ABOVE the starfield
         regardless of DOM insertion order, so the dashboard itself is
         never accidentally covered by the background layer. */
      [data-testid="stAppViewContainer"] {
        position: relative; z-index: 1;
      }
      #starfield-stage {
        position: fixed; top:0; left:0; width:100vw; height:100vh;
        pointer-events: none; z-index: 0; overflow: hidden;
        perspective: 900px; perspective-origin: 50% 50%;
        background: #05070a radial-gradient(ellipse at 50% 30%, rgba(14,117,109,0.10), transparent 60%);
      }
      #starfield-layer {
        position: absolute; top:-10%; left:-10%; width:120%; height:120%;
        transform-style: preserve-3d;
        will-change: transform;
      }
      .sf-star {
        position: absolute; border-radius: 50%; background: #E8EEF2;
        animation: sf-twinkle ease-in-out infinite;
      }
      @keyframes sf-twinkle {
        0%, 100% {
          opacity: 0.22; transform: scale(0.88);
          box-shadow: 0 0 1px 0px rgba(201,214,222,0.12);
        }
        50% {
          opacity: 0.95; transform: scale(1.2);
          box-shadow: 0 0 6px 2px rgba(201,214,222,0.55);
        }
      }
      .sf-particle {
        position: absolute; background: #C9D6DE; border-radius: 2px;
        box-shadow: 0 0 4px rgba(201,214,222,0.6);
        animation: sf-drift linear infinite;
      }
      @keyframes sf-drift {
        0%   { transform: translate(0,0); opacity: 0; }
        12%  { opacity: 0.6; }
        88%  { opacity: 0.6; }
        100% { transform: translate(var(--dx), var(--dy)); opacity: 0; }
      }
      @media (prefers-reduced-motion: reduce) {
        .sf-star { animation-duration: 6s !important; }
        .sf-particle { animation: none !important; opacity: 0.35; }
        #starfield-layer { transform: none !important; }
      }
    `;
    doc.head.appendChild(style);

    var stage = doc.createElement('div');
    stage.id = 'starfield-stage';
    var layer = doc.createElement('div');
    layer.id = 'starfield-layer';
    stage.appendChild(layer);
    doc.body.appendChild(stage);

    var starCount = 140;
    for (var i = 0; i < starCount; i++) {
      var s = doc.createElement('div');
      s.className = 'sf-star';
      var size = (Math.random() * 2.4 + 1.4).toFixed(1);
      s.style.width = size + 'px';
      s.style.height = size + 'px';
      s.style.top = (Math.random() * 100) + '%';
      s.style.left = (Math.random() * 100) + '%';
      s.style.animationDuration = (2.5 + Math.random() * 6.5).toFixed(2) + 's';
      s.style.animationDelay = (Math.random() * -10).toFixed(2) + 's';
      layer.appendChild(s);
    }

    var particleCount = 24;
    for (var j = 0; j < particleCount; j++) {
      var p = doc.createElement('div');
      p.className = 'sf-particle';
      var psize = (Math.random() * 3 + 2).toFixed(1);
      p.style.width = psize + 'px';
      p.style.height = psize + 'px';
      p.style.top = (Math.random() * 100) + '%';
      p.style.left = (Math.random() * 100) + '%';
      var dx = (Math.random() * 160 - 80).toFixed(0) + 'px';
      var dy = (Math.random() * -140 - 40).toFixed(0) + 'px';
      p.style.setProperty('--dx', dx);
      p.style.setProperty('--dy', dy);
      p.style.animationDuration = (14 + Math.random() * 14).toFixed(1) + 's';
      p.style.animationDelay = (Math.random() * 10).toFixed(1) + 's';
      layer.appendChild(p);
    }

    // Pseudo-3D "orbiting camera": the whole starfield slowly auto-rotates
    // forever (like the presentation's `stars.rotation.y += 0.00015`),
    // plus the mouse nudges azimuth/tilt further — same lerp-towards-target
    // approach the presentation uses for its real Three.js camera, just
    // driving a CSS rotateY/rotateX instead of an actual camera matrix.
    var mouseX = 0, mouseY = 0;
    var azimuth = 0, tilt = 0, autoAzimuth = 0;
    var reduceMotion = doc.defaultView.matchMedia &&
      doc.defaultView.matchMedia('(prefers-reduced-motion: reduce)').matches;

    doc.addEventListener('mousemove', function(e) {
      mouseX = (e.clientX / doc.documentElement.clientWidth) * 2 - 1;
      mouseY = (e.clientY / doc.documentElement.clientHeight) * 2 - 1;
    });

    function tick() {
      if (!reduceMotion) {
        autoAzimuth += 0.008;
        azimuth += ((autoAzimuth + mouseX * 6) - azimuth) * 0.03;
        tilt += ((mouseY * -3) - tilt) * 0.03;
        layer.style.transform = 'rotateY(' + azimuth.toFixed(3) + 'deg) rotateX(' + tilt.toFixed(3) + 'deg)';
        requestAnimationFrame(tick);
      }
    }
    if (!reduceMotion) requestAnimationFrame(tick);
  } catch (e) { /* cross-origin iframe — feature unavailable in this Streamlit setup */ }
})();
</script>
""", height=0)

# ---- Animated count-up for headline numbers (parent-document injection,
# same technique as everything else above) ----
#
# Targets Streamlit's own st.metric() values (used for "Points collected"
# / "Distinct locations" in the discovery-coverage section) and the
# mAP@50-95 figure inside each custom .metric-card in the Metrics tab.
# Runs once per element (guarded by a data-counted flag) and re-scans
# periodically so it also catches cards that appear later — e.g. after
# switching to a tab that wasn't rendered yet, or the field-summary cards
# once their async data loads.
components.html("""
<script>
(function() {
  try {
    var doc = window.parent.document;
    if (doc.getElementById('heli-counter-marker')) return;
    var marker = doc.createElement('div');
    marker.id = 'heli-counter-marker';
    marker.style.display = 'none';
    doc.body.appendChild(marker);

    function animateCount(el) {
      if (el.dataset.counted) return;
      var raw = el.textContent.trim();
      var m = raw.match(/^([^\\d\\-]*)([\\d.,]+)(.*)$/);
      if (!m) return;
      var prefix = m[1], numStr = m[2].replace(/,/g, ''), suffix = m[3];
      var decimals = numStr.indexOf('.') !== -1 ? numStr.split('.')[1].length : 0;
      var target = parseFloat(numStr);
      if (isNaN(target)) return;
      el.dataset.counted = '1';
      var duration = 1000, start = null;
      function step(ts) {
        if (!start) start = ts;
        var progress = Math.min((ts - start) / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = prefix + (target * eased).toFixed(decimals) + suffix;
        if (progress < 1) requestAnimationFrame(step);
        else el.textContent = raw;
      }
      requestAnimationFrame(step);
    }

    function scan() {
      var candidates = doc.querySelectorAll(
        '[data-testid="stMetricValue"], .metric-card p[style*="font-size:22px"]'
      );
      for (var i = 0; i < candidates.length; i++) animateCount(candidates[i]);
    }
    scan();
    setInterval(scan, 700);
  } catch (e) { /* cross-origin iframe — feature unavailable in this Streamlit setup */ }
})();
</script>
""", height=0)

# ---- Opening epigraph — condensed Passacaglia manifesto, shown before the
# title so the visitor reads the conceptual frame ("we don't erase what
# came before, we transform it") before encountering any data. Quiet and
# small on purpose — an epigraph, not a banner competing with the title.
st.markdown(f"""
<div style="text-align:center; max-width:640px; margin:6px auto 22px auto;">
    <p style="color:#7C8B93; font-style:italic; font-size:12.5px; letter-spacing:.03em; margin:0 0 6px 0;">
        {t('epigraph.credit')}
    </p>
    <p style="color:#9FB0B8; font-style:italic; font-size:13.5px; line-height:1.6; margin:0 0 4px 0;">
        {t('epigraph.line1')}
    </p>
    <p style="color:#C9D6DE; font-weight:700; font-size:13.5px; line-height:1.6; margin:0;">
        {t('epigraph.line2')}
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<h1 class="main-title">{t("main.title")}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="subtitle">{t("main.subtitle")}</p>', unsafe_allow_html=True)
if MODEL_OPTIONS:
    st.caption(f"{t('main.active_model')} **{st.session_state.get('model_choice') or list(MODEL_OPTIONS)[0]}**")
else:
    st.caption(f"{t('main.active_model')} {t('main.active_model.none')}")

model = get_selected_model()

# Load metrics data early (used by both the Downloads tab and the metrics
# panel at the bottom) — only the visual display moved, not the data load.
metrics_df = load_experiment_metrics()

tab_about, tab_metrics, tab_field, tab4, tab2, tab3, tab1, tab5, tab6, tab7 = st.tabs([
    t("tabs.about"), t("tabs.metrics"), t("tabs.field"), t("tabs.map"),
    t("tabs.search"), t("tabs.samples"), t("tabs.upload"),
    t("tabs.pipeline"), t("tabs.governance"), t("tabs.downloads"),
])

# ====================== TAB 1: Upload ======================
with tab1:
    if model is None:
        st.info(t("upload.no_model.info"))
    else:
        images = st.file_uploader(t("upload.uploader.label"),
                                   type=["jpg", "jpeg", "png"],
                                   accept_multiple_files=True, max_upload_size=10, help=t("upload.uploader.help"))

        if images:
            for idx, image_file in enumerate(images):
                col1, col2 = st.columns(2)
                original = Image.open(image_file)

                with col1:
                    st.image(original, caption=t("upload.original_caption"), use_container_width=True)

                with col2:
                    result_img, has_helipad = detect_helipad(original, model, conf_threshold)
                    st.image(result_img, caption=t("upload.detection_caption"), use_container_width=True)
                    if has_helipad:
                        st.success(t("upload.success"))
                    else:
                        st.warning(t("upload.warning_none"))

# ====================== TAB 2: Bounding Box Search ======================
with tab2:
    st.subheader(t("search.subheader"))

    with st.expander(t("search.caption"), expanded=True):
        col_a, col_b = st.columns(2)
        with col_a:
            lon_min = st.number_input(t("search.lon_min"), value=-46.6583, format="%.6f")
            lat_min = st.number_input(t("search.lat_min"), value=-23.5827, format="%.6f")
        with col_b:
            lon_max = st.number_input(t("search.lon_max"), value=-46.6311, format="%.6f")
            lat_max = st.number_input(t("search.lat_max"), value=-23.5536, format="%.6f")

    zoom = st.slider(t("search.zoom"), 16, 20, 19)
    search_btn = st.button(t("search.button"), type="primary", use_container_width=True)

    if search_btn:
        if model is None:
            st.error(t("search.no_model.error"))
        else:
          with st.spinner(t("search.spinner")):
            temp_dir = Path(tempfile.mkdtemp())

            try:
                x_min, y_max = deg2tile(lat_min, lon_min, zoom)
                x_max, y_min = deg2tile(lat_max, lon_max, zoom)

                jobs = [(zoom, x, y) for x in range(x_min, x_max+1) for y in range(y_min, y_max+1)]

                st.info(f"{t('search.processing')} **{len(jobs)}** {t('search.satellite_tiles')}")
                progress = st.progress(0, f"{t('search.progress')} ")

                detected_tiles = []

                for i, (z, x, y) in enumerate(jobs):
                    progress.progress((i+1)/len(jobs), f"{t('search.progress')} {i+1}/{len(jobs)} tiles")

                    tile_path = download_tile(z, x, y, temp_dir)
                    if not tile_path:
                        continue

                    img = Image.open(tile_path)
                    result_img, has_detection = detect_helipad(img, model, conf_threshold)

                    if has_detection:
                        detected_tiles.append((result_img, f"tile_z{z}_x{x}_y{y}.jpg"))

                if detected_tiles:
                    st.success(f"🎯 **{len(detected_tiles)} {t('search.found')}** {t('search.in_region')}")

                    cols = st.columns(3)
                    for idx, (img_array, filename) in enumerate(detected_tiles):
                        with cols[idx % 3]:
                            st.image(img_array, caption=filename, use_container_width=True)

                            buf = io.BytesIO()
                            Image.fromarray(img_array).save(buf, format="PNG")
                            buf.seek(0)

                            st.download_button(
                                label=t("search.download"),
                                data=buf,
                                file_name=filename.replace(".jpg", "_detected.png"),
                                mime="image/png",
                                key=f"dl_{idx}"
                            )

                    if len(detected_tiles) > 1:
                        st.info(t("search.download_individually"))
                else:
                    st.warning(t("search.none_found"))

            finally:
                shutil.rmtree(temp_dir, ignore_errors=True)

# ====================== TAB 3: Sample Images ======================
with tab3:
    st.subheader(t("samples.subheader"))
    st.caption(t("samples.caption"))

    sample_files = []
    if SAMPLES_DIR.exists():
        sample_files = sorted(
            [p for p in SAMPLES_DIR.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png")]
        )

    if not sample_files:
        st.info(t("samples.none_found").format(dir=SAMPLES_DIR))
    else:
        st.write(f"**{len(sample_files)} {t('samples.available')}**")

        preview_cols = st.columns(min(len(sample_files), 6))
        for i, path in enumerate(sample_files[:6]):
            with preview_cols[i % len(preview_cols)]:
                st.image(str(path), use_container_width=True, caption=path.name)
        if len(sample_files) > 6:
            st.caption(t("samples.more").format(n=len(sample_files) - 6))

        col_run, col_dl = st.columns(2)

        with col_run:
            st.markdown('<div class="sample-btn">', unsafe_allow_html=True)
            run_samples = st.button(
                t("samples.run_button"),
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
                t("samples.download_zip"),
                data=zip_buffer,
                file_name="helipad_sample_images.zip",
                mime="application/zip",
                use_container_width=True,
            )

        if run_samples:
            if model is None:
                st.error(t("samples.no_model.error"))
            else:
              with st.spinner(f"{t('samples.analyzing')} {len(sample_files)} {t('samples.sample_images')}"):
                progress = st.progress(0, t("search.progress"))
                result_cols = st.columns(3)
                hits = 0

                for i, path in enumerate(sample_files):
                    progress.progress((i + 1) / len(sample_files), f"{t('search.progress')} {i+1}/{len(sample_files)}")
                    img = Image.open(path)
                    result_img, has_detection = detect_helipad(img, model, conf_threshold)
                    if has_detection:
                        hits += 1
                    with result_cols[i % 3]:
                        st.image(result_img, caption=path.name, use_container_width=True)
                        if has_detection:
                            st.success(t("samples.detected"))
                        else:
                            st.warning(t("samples.no_detection"))

                st.info(t("samples.summary").format(hits=hits, total=len(sample_files)))

# ====================== TAB 4: Interactive Map ======================
with tab4:
    st.subheader(t("map.subheader"))

    col_caption, col_toggle = st.columns([4, 1])
    with col_caption:
        st.caption(t("map.caption"))
    with col_toggle:
        dark_mode = st.toggle(t("map.dark_mode"), value=True, key="map_theme")

    map_tiles = "OSM dark" if dark_mode else "OSM light"
    map_tiles_label = t("map.dark_base") if dark_mode else t("map.light_base")

    sp_df = load_helipad_locations(SP_COORDS_CSV)
    other_df = load_helipad_locations(COORDS_CSV)
    state_lookup = load_state_lookup(COORDS_CSV)

    if sp_df.empty and other_df.empty:
        st.info(t("map.no_coords.info").format(sp=SP_COORDS_CSV, other=COORDS_CSV))
    else:
        lat_parts = [df["lat"] for df in (sp_df, other_df) if not df.empty]
        lon_parts = [df["lon"] for df in (sp_df, other_df) if not df.empty]
        center_lat = pd.concat(lat_parts).mean() if lat_parts else -23.5505  # fallback: São Paulo center
        center_lon = pd.concat(lon_parts).mean() if lon_parts else -46.6333

        # tiles=None avoids Folium auto-adding a base layer with an internal,
        # unreadable name (e.g. "cartodbdarkmatter") to the layer control —
        # we add our own TileLayer below, built from an explicit URL template
        # (not a Folium preset string) so our friendly `name=` is always honored.
        fmap = folium.Map(location=[center_lat, center_lon], zoom_start=5, tiles=None)
        # container_id="map_div": this map is rendered via st_folium() further
        # down, which hardcodes the map into a div with that literal id
        # regardless of Folium's own generated name — see add_osm_tile_layer's
        # docstring for how this was confirmed.
        # control=False: the layer-control panel that used to float on top of
        # the map (basemap name + the 3 feature-group checkboxes below) was
        # moved out of the map canvas entirely, into the Streamlit checkboxes
        # right below — this tile layer has nothing left to be listed in.
        add_osm_tile_layer(fmap, dark_mode, name=map_tiles_label, control=False, container_id="map_div")

        # Field-validation results (helipads found per region), loaded early so
        # the training-region markers below can show a count, not just a name.
        field_summary_for_map = load_field_detection_summary()
        regions_by_slug = {}
        min_rate, max_rate = 0.0, 1.0
        if field_summary_for_map:
            regions_by_slug = {r["region"]: r for r in field_summary_for_map.get("regions", [])}
            rates = [r["detection_rate"] for r in regions_by_slug.values()]
            min_rate, max_rate = (min(rates), max(rates)) if rates else (0.0, 1.0)

        # Layer visibility now lives here, as ordinary Streamlit checkboxes
        # above the map, instead of Leaflet's own floating control panel that
        # used to sit on top of (and cover part of) the map canvas.
        st.caption(t("map.layers_caption"))
        col_l1, col_l2, col_l3 = st.columns(3)
        with col_l1:
            show_sp_layer = st.checkbox(f"🔴 {t('map.sp_layer')} ({len(sp_df)})", value=True, key="map_show_sp")
        with col_l2:
            show_other_layer = st.checkbox(f"🔵 {t('map.other_layer')} ({len(other_df)})", value=True, key="map_show_other")
        with col_l3:
            show_detection_layer = st.checkbox(t("map.detection_rate_layer"), value=True, key="map_show_detection")

        sp_layer = folium.FeatureGroup(name=f"🔴 {t('map.sp_layer')} ({len(sp_df)})", show=True)
        for _, row in sp_df.iterrows():
            raw_name = row.get("Nome do Bairro", "Unknown")
            name = format_region_display(raw_name)
            region_stats = regions_by_slug.get(slugify_region(raw_name))

            if region_stats is not None:
                found = region_stats["tiles_detected"]
                rate = region_stats["detection_rate"]
                tooltip_text = f"{name} · {found} {t('map.tiles_detected')} ({rate*100:.1f}%)"
                # Same blue_scale color-coding as the detection-rate circles
                # (detection_rate_to_color), applied to BOTH the hover
                # tooltip and the click popup here — per explicit request,
                # one shared blue signal for "how many points this region
                # has" everywhere that number shows up, rather than a
                # separate color per marker family.
                color = detection_rate_to_color(rate, min_rate, max_rate)
                text_color = readable_text_color(color)
                tooltip_style = (
                    f"background-color:{color}; color:{text_color}; "
                    f"border:1px solid {text_color}22; border-radius:4px; "
                    f"padding:4px 8px; font-weight:600; box-shadow:0 1px 4px rgba(0,0,0,0.35);"
                )
                tooltip = folium.Tooltip(tooltip_text, style=tooltip_style)
                popup_html = rate_popup_html(
                    f"<b>{name}</b><br>{t('map.training_region')}<br>"
                    f"🚁 <b>{found}</b> {t('map.tiles_detected')} "
                    f"({region_stats['tiles_detected']}/{region_stats['tiles_total']} · {rate*100:.1f}%)",
                    color, text_color,
                )
            else:
                tooltip = tooltip_text = name
                popup_html = f"<b>{name}</b><br>{t('map.training_region')}"

            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=tooltip,
                icon=folium.Icon(color="red", icon="home"),
            ).add_to(sp_layer)
        if show_sp_layer:
            sp_layer.add_to(fmap)

        other_layer = folium.FeatureGroup(name=f"🔵 {t('map.other_layer')} ({len(other_df)})", show=True)
        for _, row in other_df.iterrows():
            neighborhood = row.get("Nome do Bairro", "Unknown")
            hint = location_hint(row["lat"], row["lon"], row.get("Coordenadas da Bounding Box", ""), state_lookup)
            display_name = f"{neighborhood} ({hint})" if hint else neighborhood
            timestamp = row.get("Carimbo de data/hora", "")
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=folium.Popup(f"<b>{display_name}</b><br>{timestamp}", max_width=250),
                tooltip=display_name,
                icon=folium.Icon(color="blue", icon="info-sign"),
            ).add_to(other_layer)
        if show_other_layer:
            other_layer.add_to(fmap)

        # ---- Layer 3: field detection rate by region (blue scale, same as tables) ----
        if regions_by_slug and not sp_df.empty:
            detection_layer = folium.FeatureGroup(name=t("map.detection_rate_layer"), show=True)
            matched = 0
            for _, row in sp_df.iterrows():
                name = row.get("Nome do Bairro", "")
                slug = slugify_region(name)
                region_stats = regions_by_slug.get(slug)
                if region_stats is None:
                    continue
                matched += 1
                display_name = format_region_display(name)
                rate = region_stats["detection_rate"]
                color = detection_rate_to_color(rate, min_rate, max_rate)
                text_color = readable_text_color(color)
                # Tooltip background matches this marker's own fill color (same
                # blue_scale gradient, light=low rate -> navy=high rate), so
                # the hover balloon reads as an extension of the marker's own
                # color-coding instead of a plain white Leaflet default.
                tooltip = folium.Tooltip(
                    f"{display_name}: {region_stats['tiles_detected']}/{region_stats['tiles_total']} ({rate*100:.1f}%)",
                    style=(
                        f"background-color:{color}; color:{text_color}; "
                        f"border:1px solid {text_color}22; border-radius:4px; "
                        f"padding:4px 8px; font-weight:600; box-shadow:0 1px 4px rgba(0,0,0,0.35);"
                    ),
                )
                folium.CircleMarker(
                    location=[row["lat"], row["lon"]],
                    radius=10 + rate * 40,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.85,
                    tooltip=tooltip,
                    popup=folium.Popup(
                        rate_popup_html(
                            f"<b>{display_name}</b><br>"
                            f"{region_stats['tiles_detected']} {t('map.tiles_detected')}<br>"
                            f"{t('map.rate')}: {rate*100:.1f}%",
                            color, text_color,
                        ),
                        max_width=250,
                    ),
                ).add_to(detection_layer)
            if matched and show_detection_layer:
                detection_layer.add_to(fmap)

        # The layer-control panel that used to render here (folium.LayerControl,
        # floating over the map's top-right corner) was replaced by the
        # Streamlit checkboxes above, outside the map canvas.
        _force_leaflet_resize(fmap)

        st.write(t("map.summary").format(sp=len(sp_df), other=len(other_df)))
        map_state = st_folium(fmap, use_container_width=True, height=520, key=f"main_map_{map_tiles}")

        # ---- Helicopter reacts to real zoom: turn, land, pause, take off ----
        # st_folium returns the live zoom/center of the Leaflet map after every
        # pan/zoom, so "zoomed into a region" below is real map state, not a
        # simulated one. When the visible center sits close enough to one of
        # the SP training-region markers at a close-enough zoom, the ambient
        # helicopter (persistent overlay defined earlier in this file) plays a
        # bank-turn > land > pause > take-off sequence and a toast names the
        # region, then it resumes its normal patrol.
        #
        # The touchdown spot is viewport-relative (bottom-center), not a
        # pixel-accurate landing on the Leaflet marker itself: the map lives
        # inside streamlit-folium's own nested iframe with its own coordinate
        # system, and translating a lat/lon into the parent page's pixel
        # space would need a second round-trip through Leaflet's internal
        # projection — too fragile to chase for a decorative flourish.
        #
        # This runs as its OWN components.html call (its own iframe/script
        # scope) rather than reusing the functions defined in the main
        # helicopter script above, because two separate components.html
        # iframes never share JS scope even though both inject into the same
        # parent document. The one thing they DO share is the actual DOM node
        # (`#heli-flyby-global`) and its `dataset` attributes, which is used
        # here the same way `heli_replay_nonce`/`heli_spin_nonce` are used
        # above: a nonce written by Python, compared against the last nonce
        # the DOM element remembers, so the sequence fires once per landing
        # rather than once per rerun.
        LAND_ZOOM_THRESHOLD = 12
        LAND_DISTANCE_DEG = 0.08  # ~9 km at this latitude — generous on purpose

        landed_region = None
        if map_state and not sp_df.empty:
            zoom_level = map_state.get("zoom")
            center = map_state.get("center") or {}
            center_lat_live, center_lon_live = center.get("lat"), center.get("lng")
            if zoom_level is not None and zoom_level >= LAND_ZOOM_THRESHOLD \
                    and center_lat_live is not None and center_lon_live is not None:
                distances = ((sp_df["lat"] - center_lat_live) ** 2 + (sp_df["lon"] - center_lon_live) ** 2) ** 0.5
                nearest_idx = distances.idxmin()
                if distances.loc[nearest_idx] <= LAND_DISTANCE_DEG:
                    landed_region = format_region_display(sp_df.loc[nearest_idx, "Nome do Bairro"])

        if landed_region != st.session_state.get("heli_landed_region"):
            st.session_state["heli_landed_region"] = landed_region
            st.session_state["heli_land_nonce"] = st.session_state.get("heli_land_nonce", 0) + 1

        if landed_region:
            region_name_js = json.dumps(landed_region)
            components.html(f"""
            <script>
            (function() {{
              try {{
                var doc = window.parent.document;
                var heli = doc.getElementById('heli-flyby-global');
                if (!heli) return; // main helicopter overlay hasn't mounted yet — skip this run

                var landNonce = "{st.session_state['heli_land_nonce']}";
                if (heli.dataset.lastLandNonce === landNonce) return; // already played this landing
                heli.dataset.lastLandNonce = landNonce;

                var isPt = "{st.session_state.get('lang', 'pt')}" === 'pt';
                var isPaused = {"true" if st.session_state.get("heli_paused") else "false"};
                if (isPaused) return; // respect the sidebar pause toggle — don't force a landing over it
                var regionName = {region_name_js};

                if (!doc.getElementById('heli-landing-style')) {{
                  var style = doc.createElement('style');
                  style.id = 'heli-landing-style';
                  style.textContent = `
                    @keyframes heli-land-sequence {{
                      0%   {{ top: var(--heli-cur-top); left: var(--heli-cur-left); transform: rotate(0deg) scale(1); }}
                      25%  {{ transform: rotate(-22deg) scale(0.95); }}
                      50%  {{ top: calc(100vh - 150px); left: 48%; transform: rotate(8deg) scale(0.88); }}
                      75%  {{ top: calc(100vh - 110px); left: 48%; transform: rotate(-4deg) scale(0.80); }}
                      100% {{ top: calc(100vh - 92px);  left: 48%; transform: rotate(0deg)  scale(0.72); }}
                    }}
                    @keyframes heli-takeoff-sequence {{
                      0%   {{ top: calc(100vh - 92px);  left: 48%; transform: rotate(0deg)   scale(0.72); }}
                      35%  {{ top: calc(100vh - 150px); left: 48%; transform: rotate(-14deg) scale(0.85); }}
                      100% {{ top: 64px; left: 48%; transform: rotate(-4deg) scale(1); }}
                    }}
                    #heli-landing-pad {{
                      position: fixed; left: 48%; top: calc(100vh - 58px); width: 46px; height: 14px;
                      transform: translateX(-50%); border-radius: 50%;
                      background: radial-gradient(ellipse at center, rgba(14,117,109,0.55), rgba(14,117,109,0) 72%);
                      z-index: 999997; opacity: 0; transition: opacity .4s ease; pointer-events: none;
                    }}
                    #heli-landing-pad.show {{ opacity: 1; }}
                  `;
                  doc.head.appendChild(style);
                }}

                var pad = doc.getElementById('heli-landing-pad');
                if (!pad) {{
                  pad = doc.createElement('div');
                  pad.id = 'heli-landing-pad';
                  doc.body.appendChild(pad);
                }}

                var toast = doc.getElementById('heli-tab-toast');
                function announce(text, ms) {{
                  if (!toast) return;
                  toast.textContent = text;
                  toast.classList.add('show');
                  clearTimeout(toast.dataset._landTimer);
                  toast.dataset._landTimer = setTimeout(function() {{
                    toast.classList.remove('show');
                  }}, ms);
                }}

                // Same 4 patrol flights the main script uses, duplicated here
                // (small maintenance cost) since this iframe can't reach the
                // other iframe's FLIGHTS array — see comment above.
                var FLIGHTS = [
                  {{ name: 'heli-fly-v0', duration: 7  }},
                  {{ name: 'heli-fly-v1', duration: 11 }},
                  {{ name: 'heli-fly-v2', duration: 9  }},
                  {{ name: 'heli-fly-v3', duration: 6  }},
                ];

                // 1) Freeze current position into CSS vars, then bank-turn + descend.
                var rect = heli.getBoundingClientRect();
                heli.style.setProperty('--heli-cur-top', rect.top + 'px');
                heli.style.setProperty('--heli-cur-left', ((rect.left / doc.documentElement.clientWidth) * 100) + '%');
                heli.style.animation = 'none';
                void heli.offsetWidth;
                heli.style.animation = 'heli-land-sequence 2.2s cubic-bezier(.3,.6,.3,1) forwards';
                announce((isPt ? '🚁 Pousando em ' : '🚁 Landing in ') + regionName + '...', 2200);

                // 2) Touch down: glow the pad, pause on the ground.
                setTimeout(function() {{
                  pad.classList.add('show');
                }}, 2100);

                // 3) Take back off after a short dwell on the ground.
                setTimeout(function() {{
                  pad.classList.remove('show');
                  announce((isPt ? '🚁 Decolando de ' : '🚁 Taking off from ') + regionName + '...', 2000);
                  heli.style.animation = 'none';
                  void heli.offsetWidth;
                  heli.style.animation = 'heli-takeoff-sequence 1.8s cubic-bezier(.3,.1,.3,1) forwards';
                }}, 4300);

                // 4) Resume normal patrol once the take-off climb finishes.
                setTimeout(function() {{
                  var f = FLIGHTS[Math.floor(Math.random() * FLIGHTS.length)];
                  heli.style.left = '0';
                  heli.style.animation = 'none';
                  void heli.offsetWidth;
                  heli.style.animation = f.name + ' ' + f.duration + 's cubic-bezier(.45,.05,.55,.95) infinite alternate';
                }}, 6150);
              }} catch (e) {{ /* cross-origin iframe — feature unavailable in this Streamlit setup */ }}
            }})();
            </script>
            """, height=0)

        st.markdown(f"#### {t('map.raw_data_expander')}")
        with st.expander(t("map.raw_data_expander"), expanded=True):
            t1, t2 = st.tabs([t("map.raw_data.sp_tab"), t("map.raw_data.other_tab")])
            with t1:
                sp_df_display = sp_df.copy()
                if "Nome do Bairro" in sp_df_display.columns:
                    _segment_word = "Trecho" if st.session_state.get("lang") == "pt" else "Segment"
                    sp_df_display["Nome do Bairro"] = sp_df_display["Nome do Bairro"].astype(str).str.replace(
                        r"\btrecho\b", _segment_word, regex=True, case=False
                    )
                sp_df_display.index = range(1, len(sp_df_display) + 1)
                st.dataframe(sp_df_display, use_container_width=True)
            with t2:
                other_df_display = other_df.copy()
                if not other_df_display.empty:
                    city_col = t("map.raw_data.city_hint_col")
                    other_df_display[city_col] = other_df_display.apply(
                        lambda r: location_hint(
                            r["lat"], r["lon"], r.get("Coordenadas da Bounding Box", ""), state_lookup
                        ) or "—",
                        axis=1,
                    )
                    # Most human-readable/general first (which state, which
                    # neighborhood), then the precise numbers, then the raw
                    # source string, timestamp metadata last — a zoom-in
                    # from "where is this, in words" to "the exact technical
                    # record it came from".
                    _preferred_order = [
                        city_col, "Nome do Bairro", "lat", "lon",
                        "Coordenadas da Bounding Box", "Carimbo de data/hora",
                    ]
                    other_df_display = other_df_display[
                        [c for c in _preferred_order if c in other_df_display.columns]
                        + [c for c in other_df_display.columns if c not in _preferred_order]
                    ]
                    other_df_display.index = range(1, len(other_df_display) + 1)
                st.dataframe(other_df_display, use_container_width=True)

        st.divider()
        col_density_title, col_density_toggle = st.columns([4, 1])
        with col_density_title:
            st.subheader(t("map.density.subheader"))
            st.caption(t("map.density.caption"))
        with col_density_toggle:
            density_dark_mode = st.toggle(t("map.dark_mode"), value=True, key="density_map_theme")

        if other_df.empty:
            st.info(t("map.density.no_coords").format(path=COORDS_CSV))
        else:
            dark_map = folium.Map(
                location=[other_df["lat"].mean(), other_df["lon"].mean()],
                zoom_start=5,
                tiles=None,
            )
            add_osm_tile_layer(dark_map, density_dark_mode, control=False)
            for _, row in other_df.iterrows():
                hint = location_hint(row["lat"], row["lon"], row.get("Coordenadas da Bounding Box", ""), state_lookup)
                display_name = f"{row.get('Nome do Bairro', 'Unknown')} ({hint})" if hint else row.get("Nome do Bairro", "Unknown")
                folium.CircleMarker(
                    location=[row["lat"], row["lon"]],
                    radius=5,
                    color="#00CED1",
                    fill=True,
                    fill_color="#00CED1",
                    fill_opacity=0.8,
                    tooltip=display_name,
                ).add_to(dark_map)
            HeatMap(
                other_df[["lat", "lon"]].values.tolist(),
                radius=18,
                blur=22,
                gradient={"0.2": "#FFF8DC", "0.5": "#FFA855", "0.8": "#FF7804", "1.0": "#FF6800"},
            ).add_to(dark_map)
            _force_leaflet_resize(dark_map)
            # Rendered as a plain HTML embed (not st_folium) because this view never
            # needs the map's returned click/data — st_folium is a bidirectional custom
            # component that negotiates its iframe height with the browser on mount, and
            # that handshake was unreliable as the *second* such component on this tab
            # (it kept rendering at 0 height until some later rerun, e.g. toggling Dark
            # mode, happened to re-trigger it). components.html() just embeds static HTML
            # in a fixed-height iframe, no handshake needed, so it always paints on the
            # very first render.
            components.html(dark_map.get_root().render(), height=550, scrolling=False)

# ====================== TAB 5: Pipeline & Governance ======================
with tab5:
    st.subheader(t("pipeline.subheader"))
    st.caption(t("pipeline.caption"))

    pipeline_steps = [
        ("🔍", t("pipeline.step1.title"), t("pipeline.step1.desc")),
        ("📐", t("pipeline.step2.title"), t("pipeline.step2.desc")),
        ("🛰️", t("pipeline.step3.title"), t("pipeline.step3.desc")),
        ("🖼️", t("pipeline.step4.title"), t("pipeline.step4.desc")),
        ("🏷️", t("pipeline.step5.title"), t("pipeline.step5.desc")),
        ("🧠", t("pipeline.step6.title"), t("pipeline.step6.desc")),
        ("📊", t("pipeline.step7.title"), t("pipeline.step7.desc")),
        ("🌍", t("pipeline.step8.title"), t("pipeline.step8.desc")),
        ("🚁", t("pipeline.step9.title"), t("pipeline.step9.desc")),
    ]

    n = len(pipeline_steps)
    rows = [pipeline_steps[i:i + 3] for i in range(0, n, 3)]
    step_idx = 0
    for row in rows:
        row_cols = st.columns(3)
        for col, (icon, title, desc) in zip(row_cols, row):
            frac = step_idx / (n - 1) if n > 1 else 0.0
            base = blue_scale(frac)
            bg_light = _shade(base, 0.16)
            bg_dark = _shade(base, -0.30)
            gradient = f"linear-gradient(145deg, {bg_light} 0%, {base} 55%, {bg_dark} 100%)"
            accent_rgb = _hex_to_rgb(base)
            glow = f"rgba({accent_rgb[0]},{accent_rgb[1]},{accent_rgb[2]},0.45)"
            title_color = "#FFFFFF"
            desc_color = "#E2E8F0"
            badge_bg = "rgba(255,255,255,0.16)"
            badge_color = "#FFFFFF"
            with col:
                st.markdown(f"""
                <div class="flow-step" style="background:{gradient}; border-top:3px solid rgba(255,255,255,0.35); box-shadow: 0 6px 20px {glow}, inset 0 1px 0 rgba(255,255,255,0.12);">
                    <span class="flow-badge" style="background:{badge_bg}; color:{badge_color}; box-shadow: 0 0 0 1px rgba(255,255,255,0.25);">{step_idx+1:02d}</span>
                    <span class="flow-icon">{icon}</span>
                    <p class="flow-title" style="color:{title_color};">{title}</p>
                    <p class="flow-desc" style="color:{desc_color};">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
            step_idx += 1

# ====================== TAB 6: Governance ======================
with tab6:
    st.subheader(t("gov.responsible_ai"))
    st.markdown(t("gov.responsible_ai.body"))

    st.subheader(t("gov.lgpd"))
    st.markdown(t("gov.lgpd.body"))

# ====================== TAB: About ======================
with tab_about:
    st.header(t("about.header"))
    st.markdown(t("about.body_intro"))

    # ---- Top 10 helicopter cities table ----
    # This used to apply a Blues background_gradient to a "Rate" column, the
    # same styling technique as the Field Detections table. That column was
    # removed (see the comment above cities.table.data) since its numbers
    # weren't sourced — there's no real per-city percentage left to shade, so
    # this now renders as a plain table like the rest of the About tab.
    st.markdown(f"### {t('cities.header')}")
    _cities_cols = t("cities.table.columns")
    _cities_rows = t("cities.table.data")
    _rank_col = _cities_cols[0]
    cities_df = pd.DataFrame(_cities_rows, columns=_cities_cols).set_index(_rank_col)

    # Same "Blues" gradient look as "Compare all 3 models" (Field Detections
    # tab) — matplotlib's actual colormap, not an approximation, so the
    # shades genuinely match. Gradiented by Rank position (1st..10th), not
    # by a measured value: the old "Rate (%)" column this table used to
    # carry was removed earlier (it turned out to be an unrelated table's
    # numbers copy-pasted in, not a real per-city statistic — see the
    # comment above cities.table.data) and there's no other numeric column
    # here that isn't itself editorial ("Estimated Fleet" is "400+"/"—"
    # strings, not something you can average or gradient). Rank is just
    # display order, so coloring by it doesn't imply a precision the table
    # doesn't have — it's a reading aid, not a re-introduced statistic.
    # Applied across the WHOLE row (every column, same shade) rather than
    # one narrow column, which reads as more deliberate/cohesive than a
    # single colored strip next to otherwise-plain cells.
    def _rank_row_style(row):
        rank_num = int(re.sub(r"\D", "", str(row.name)) or 1)
        frac = 1 - (rank_num - 1) / max(len(cities_df) - 1, 1)
        rgba = plt.colormaps["Blues"](frac)
        hexcolor = "#{:02x}{:02x}{:02x}".format(*(int(c * 255) for c in rgba[:3]))
        text_color = readable_text_color(hexcolor)
        return [f"background-color:{hexcolor}; color:{text_color};"] * len(row)

    st.dataframe(cities_df.style.apply(_rank_row_style, axis=1), use_container_width=True)

    st.markdown(f"""
    <div style="border-left:3px solid #14b8a6; background:rgba(14,117,109,0.08);
                border-radius:8px; padding:14px 18px; margin:14px 0 4px 0;">
        <p style="margin:0; color:#E2E8F0; font-size:14px; line-height:1.65;">
            {t('cities.why_sao_paulo')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(t("about.body_closing"))

    st.markdown(f"### {t('about.discovery.title')}")
    st.caption(t("about.discovery.body"))
    _disc_stats = load_discovery_dataset_stats()
    if _disc_stats is None:
        st.caption(t("about.discovery.missing").format(path=COORDS_CSV))
    else:
        disc_col1, disc_col2 = st.columns(2)
        with disc_col1:
            st.metric(t("about.discovery.points"), _disc_stats["total_points"])
        with disc_col2:
            if _disc_stats["distinct_locations"] is not None:
                st.metric(t("about.discovery.regions"), _disc_stats["distinct_locations"])
        if _disc_stats["by_state"]:
            _count_col = t("about.discovery.state_col"), t("about.discovery.count_col")
            _count_col = t("about.discovery.count_col")
            _state_by_count_df = pd.DataFrame(
                list(_disc_stats["by_state"].items()),
                columns=[t("about.discovery.state_col"), _count_col],
            )
            # No gradient here (unlike the other ranked tables in this app):
            # with only a handful of distinct values (mostly 1s and 2s)
            # spread across 13 states, a continuous gradient just produces
            # a few repeated blocks of identical color instead of a smooth,
            # readable progression — it looked broken rather than
            # harmonious.
            #
            # Alignment note: text-align via a pandas Styler (.set_properties)
            # is NOT one of the style properties st.dataframe actually
            # honors — it only respects a limited subset (background-color
            # from .background_gradient()/.apply(), and .format() for number
            # display), so the last two attempts at this silently did
            # nothing visually despite the code changing. Converting the
            # column to plain text instead of a numeric dtype is what
            # actually works: st.dataframe left-aligns text/object columns
            # by default, no styling call needed to get there.
            _state_by_count_df[_count_col] = _state_by_count_df[_count_col].astype(str)
            st.dataframe(
                _state_by_count_df,
                use_container_width=True, hide_index=True,
            )
        else:
            st.caption(t("about.discovery.pending"))

    st.markdown(f"""
    <div class="dark-card" style="text-align:left;">
        <table style="width:100%; font-size:14px; color:#E2E8F0; border-collapse:collapse;">
            <tr><td style="padding:6px 0; color:#93C5FD; width:160px; vertical-align:top;">{t("about.institution")}</td>
                <td style="padding:6px 0;"><b>PUC-SP — FACEI</b></td></tr>
            <tr><td style="padding:6px 0; color:#93C5FD; vertical-align:top;">{t("about.program")}</td>
                <td style="padding:6px 0;">BSc in Human Centered-AI & Data Science</td></tr>
            <tr><td style="padding:6px 0; color:#93C5FD; vertical-align:top;">{t("about.course")}</td>
                <td style="padding:6px 0;">Machine Learning / Computer Vision — Project P2</td></tr>
            <tr><td style="padding:6px 0; color:#93C5FD; vertical-align:top;">{t("about.authors")}</td>
                <td style="padding:6px 0;">
                    Fabiana ⚡️ Campanari
                </td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

# ====================== TAB 7: Downloads ======================
with tab7:
    st.subheader(t("dl.subheader"))
    st.caption(t("dl.caption"))

    dl_col1, dl_col2 = st.columns(2)

    with dl_col1:
        st.markdown(t("dl.executive_report"))
        if EXEC_REPORT_EN.exists():
            with open(EXEC_REPORT_EN, "rb") as f:
                st.download_button(t("dl.exec_en_button"), f, file_name=EXEC_REPORT_EN.name,
                                    mime="application/pdf", use_container_width=True)
        else:
            st.caption(t("dl.not_found").format(path=EXEC_REPORT_EN))

        if EXEC_REPORT_PT.exists():
            with open(EXEC_REPORT_PT, "rb") as f:
                st.download_button(t("dl.exec_pt_button"), f, file_name=EXEC_REPORT_PT.name,
                                    mime="application/pdf", use_container_width=True)
        else:
            st.caption(t("dl.not_found").format(path=EXEC_REPORT_PT))

    with dl_col2:
        st.markdown(t("dl.dataset_metrics"))
        if DATASET_RAR.exists():
            with open(DATASET_RAR, "rb") as f:
                st.download_button(t("dl.dataset_button"), f, file_name=DATASET_RAR.name,
                                    mime="application/octet-stream", use_container_width=True)
        else:
            st.caption(t("dl.not_found").format(path=DATASET_RAR))

        if not metrics_df.empty:
            csv_bytes = metrics_df.drop(columns=["_dir"], errors="ignore").to_csv(index=False).encode("utf-8")
            st.download_button(t("dl.metrics_button"), csv_bytes, file_name="experiment_metrics.csv",
                                mime="text/csv", use_container_width=True)
        else:
            st.caption(t("dl.no_metrics"))

        st.markdown(t("dl.field_validation"))
        if FIELD_SUMMARY_PATH.exists():
            with open(FIELD_SUMMARY_PATH, "rb") as f:
                st.download_button(t("dl.field_json_button"), f, file_name=FIELD_SUMMARY_PATH.name,
                                    mime="application/json", use_container_width=True)
        else:
            st.caption(t("dl.not_found").format(path=FIELD_SUMMARY_PATH))

        TRIAGE_LOG_PATH = Path("reports/auto_triage_regions_log.txt")
        if TRIAGE_LOG_PATH.exists():
            with open(TRIAGE_LOG_PATH, "rb") as f:
                st.download_button(t("dl.field_log_button"), f, file_name=TRIAGE_LOG_PATH.name,
                                    mime="text/plain", use_container_width=True)
        else:
            st.caption(t("dl.not_found").format(path=TRIAGE_LOG_PATH))

    st.markdown("---")
    st.markdown(f"### {t('dl.session_summary.title')}")
    st.caption(t("dl.session_summary.body"))
    if st.button(t("dl.session_summary.button")):
        st.session_state["session_pdf_bytes"] = build_session_summary_pdf(
            metrics_df=metrics_df,
            selected_model=st.session_state.get("model_choice"),
            conf_threshold=conf_threshold,
            lang=st.session_state.get("lang", "pt"),
        )
    if st.session_state.get("session_pdf_bytes"):
        st.download_button(
            t("dl.session_summary.download_button"),
            data=st.session_state["session_pdf_bytes"],
            file_name=f"helipad_detector_session_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    st.markdown("---")
    st.markdown(f"""
    <div class="dark-card">
        <span class="repo-icon">🚁</span>
        <h4>{t("dl.repo_title")}</h4>
        <p style="color:#CBD5E1; font-size:14px;">
            {t("dl.repo_desc")}
        </p>
        <a href="https://github.com/Mindful-AI-Research/3-project-ai-ml-yolo-helipad_detector" target="_blank" style="color:#93C5FD; font-weight:600;">
            github.com/Mindful-AI-Research/3-project-ai-ml-yolo-helipad_detector
        </a>
    </div>
    """, unsafe_allow_html=True)

# ========================= METRICS DASHBOARD =========================
with tab_metrics:
    st.subheader(t("metrics.subheader"))
    if metrics_df.empty:
        st.info(t("metrics.no_csv"))
    else:
        n_exp = len(metrics_df)
        cols = st.columns(n_exp) if n_exp <= 4 else [st.container()]
        _metric_card_style = (
            "padding:18px; border-radius:14px; text-align:center; "
            "box-shadow:0 3px 10px rgba(15,23,42,0.25); "
            "border:1px solid rgba(255,255,255,0.10);"
        )

        for i, row in metrics_df.iterrows():
            target = cols[i] if n_exp <= 4 else st
            with target:
                netron_link = netron_url_for(row['Experiment']) or "https://netron.app/"
                netron_label = t("metrics.netron_view") if row['Experiment'] in MODEL_WEIGHTS_BY_EXP else t("metrics.netron_manual")
                card_bg = blue_scale(i / (n_exp - 1) if n_exp > 1 else 0.0)
                st.markdown(f"""
                <div style="{_metric_card_style} background:{card_bg};">
                    <h4 style="margin:0 0 8px 0; color:#FFFFFF;">{row['Experiment']}</h4>
                    <p style="margin:2px 0; color:#DCE8F5; font-size:13px;">
                        {t('metrics.best_epoch')} {row['Best Epoch']} / {row['Total Epochs']}
                    </p>
                    <p style="margin:6px 0; font-size:22px; font-weight:700; color:#FFFFFF;">
                        {row['mAP@50-95']:.3f}
                    </p>
                    <p style="margin:0; color:#DCE8F5; font-size:12px;">mAP@50-95</p>
                    <p style="margin:8px 0 0 0;">
                        <a href="{netron_link}" target="_blank" rel="noopener noreferrer"
                           style="font-size:12px; color:#FFFFFF; font-weight:600; text-decoration:underline;">
                            {netron_label}
                        </a>
                    </p>
                </div>
                """, unsafe_allow_html=True)

        # Netron previews render full-width, stacked one per row below the
        # metric cards — a narrow column (1 of up to 4) is too cramped for
        # an interactive graph viewer with its own zoom/pan controls.
        # Loaded on demand (not eagerly) so opening the Metrics tab doesn't
        # fire 3 external requests to netron.app on every rerun.
        for i, row in metrics_df.iterrows():
            if row['Experiment'] not in MODEL_WEIGHTS_BY_EXP:
                continue
            netron_link = netron_url_for(row['Experiment'])
            with st.expander(f"{t('metrics.netron_expander')} — {row['Experiment']}", expanded=True):
                load_key = f"netron_loaded_{row['Experiment']}"
                if st.session_state.get(load_key):
                    components.iframe(netron_link, height=560, scrolling=True)
                else:
                    if st.button(t("metrics.netron_load_button"), key=f"netron_btn_{row['Experiment']}"):
                        st.session_state[load_key] = True
                        st.rerun()

        st.markdown(t("metrics.comparison_title"))
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
                    st.success(t("metrics.outperformed").format(exp=row['Experiment'], delta=f"{delta:+.4f}"))
                elif delta < -0.005:
                    st.warning(t("metrics.underperformed").format(exp=row['Experiment'], delta=f"{delta:+.4f}"))
                else:
                    st.info(t("metrics.tied").format(exp=row['Experiment'], delta=f"{delta:+.4f}"))

        # ---- Per-epoch metric evolution (real data from results.csv) ----
        curves = load_experiment_curves()
        if curves:
            with st.expander(t("metrics.evolution").lstrip("#").strip(), expanded=True):
                metric_choice = st.selectbox(
                    t("metrics.metric_label"),
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
                    xaxis_title=t("metrics.epoch"), yaxis_title=metric_choice.replace("metrics/", "").replace("(B)", ""),
                    height=320, margin=dict(l=10, r=10, t=10, b=10),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02),
                )
                st.plotly_chart(fig, use_container_width=True)

        # ---- Confusion matrix per experiment (real image already generated by YOLO) ----
        if not metrics_df.empty and "_dir" in metrics_df.columns:
            with st.expander(t("metrics.confusion_matrix").lstrip("#").strip(), expanded=True):
                cm_exp = st.selectbox(
                    t("metrics.experiment_label"), metrics_df["Experiment"].tolist(), key="cm_exp_choice"
                )
                exp_dir_str = metrics_df.loc[metrics_df["Experiment"] == cm_exp, "_dir"].iloc[0]
                cm_path = Path(exp_dir_str) / "confusion_matrix.png"
                cm_norm_path = Path(exp_dir_str) / "confusion_matrix_normalized.png"
                cm_col1, cm_col2 = st.columns(2)
                with cm_col1:
                    if cm_path.exists():
                        st.image(str(cm_path), caption=f"{cm_exp} — {t('metrics.cm_caption')}", use_container_width=True)
                    else:
                        st.info(t("metrics.cm_not_found").format(path=cm_path.resolve()))
                with cm_col2:
                    if cm_norm_path.exists():
                        st.image(str(cm_norm_path), caption=f"{cm_exp} — {t('metrics.cm_norm_caption')}", use_container_width=True)
                    else:
                        st.info(t("metrics.cm_norm_not_found").format(path=cm_norm_path.resolve()))

# ========================= FIELD DETECTIONS BY REGION =========================
with tab_field:
    st.subheader(t("field.subheader"))
    field_summary = load_field_detection_summary()

    if FIELD_SUMMARY_PATH.exists():
        last_updated = datetime.fromtimestamp(FIELD_SUMMARY_PATH.stat().st_mtime)
        st.caption(t("field.last_updated").format(date=last_updated.strftime('%b %d, %Y at %H:%M')))

    if field_summary is None:
        st.info(t("field.no_summary").format(path=FIELD_SUMMARY_PATH))
    else:
        totals = field_summary.get("totals", {})
        regions = field_summary.get("regions", [])

        total_tiles = totals.get("tiles_total", 0)
        total_detected = totals.get("tiles_detected", 0)
        total_rate = totals.get("detection_rate", 0.0)

        card_cols = st.columns(3)
        _field_card_style = (
            "padding:18px; border-radius:14px; text-align:center; "
            "box-shadow:0 3px 10px rgba(15,23,42,0.25); "
            "border:1px solid rgba(255,255,255,0.10);"
        )
        with card_cols[0]:
            bg0 = blue_scale(0.0)
            st.markdown(f"""
            <div style="{_field_card_style} background:{bg0};">
                <p style="margin:6px 0; font-size:26px; font-weight:700; color:#FFFFFF;">{total_detected}</p>
                <p style="margin:0; color:#DCE8F5; font-size:12px;">{t("field.detected_total")}</p>
            </div>
            """, unsafe_allow_html=True)
        with card_cols[1]:
            bg1 = blue_scale(0.5)
            st.markdown(f"""
            <div style="{_field_card_style} background:{bg1};">
                <p style="margin:6px 0; font-size:26px; font-weight:700; color:#FFFFFF;">{total_tiles}</p>
                <p style="margin:0; color:#DCE8F5; font-size:12px;">{t("field.tiles_processed")}</p>
            </div>
            """, unsafe_allow_html=True)
        with card_cols[2]:
            bg2 = blue_scale(1.0)
            st.markdown(f"""
            <div style="{_field_card_style} background:{bg2};">
                <p style="margin:6px 0; font-size:26px; font-weight:700; color:#FFFFFF;">{total_rate*100:.1f}%</p>
                <p style="margin:0; color:#DCE8F5; font-size:12px;">{t("field.overall_rate")}</p>
            </div>
            """, unsafe_allow_html=True)

        if regions:
            st.markdown("")
            regions_df = pd.DataFrame(regions).sort_values("detection_rate", ascending=False)
            regions_df["region"] = regions_df["region"].apply(format_region_display)

            # Avenida Paulista is split into two survey segments ("Segment
            # 1"/"Segment 2", "Trecho 1"/"Trecho 2" in Português) because the
            # full avenue didn't fit one tile-download batch — it's one
            # physical street, so for a "most helipads found" ranking
            # against other, single-piece regions, the two segments are
            # summed into one combined row instead of quietly competing
            # against each other as if they were two different places.
            # Wrapped in try/except so a JSON schema surprise falls back to
            # the unmerged table instead of breaking this whole tab.
            try:
                _segment_suffix_re = re.compile(r"\s*\(?\s*(?:Trecho|Segment)\s*\d+\s*\)?\s*$", re.IGNORECASE)
                regions_df["region_group"] = regions_df["region"].apply(lambda s: _segment_suffix_re.sub("", s).strip())
                regions_df_grouped = regions_df.groupby("region_group", as_index=False).agg(
                    tiles_total=("tiles_total", "sum"),
                    tiles_detected=("tiles_detected", "sum"),
                    top_confidence=("top_confidence", "max"),
                    n_segments=("region", "count"),
                )
                regions_df_grouped["detection_rate"] = regions_df_grouped["tiles_detected"] / regions_df_grouped["tiles_total"]
                _combined_suffix = t("field.segments_combined_suffix")
                regions_df_grouped["region"] = regions_df_grouped.apply(
                    lambda r: r["region_group"] + (_combined_suffix if r["n_segments"] > 1 else ""), axis=1
                )
                regions_df = regions_df_grouped.drop(columns=["region_group", "n_segments"]).sort_values(
                    "detection_rate", ascending=False
                )
            except Exception:
                pass  # fall back to the unmerged per-segment rows below

            fig_regions = go.Figure(go.Bar(
                x=regions_df["region"],
                y=regions_df["detection_rate"] * 100,
                marker_color="#1E3A8A",
                text=[f"{v}/{tot}" for v, tot in zip(regions_df["tiles_detected"], regions_df["tiles_total"])],
                textposition="outside",
            ))
            fig_regions.update_layout(
                yaxis_title=t("field.detection_rate_pct"), xaxis_title="",
                height=340, margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig_regions, use_container_width=True)

            # Table is ranked by absolute helipads found (tiles_detected),
            # not by rate — rate and raw count don't always agree (e.g. a
            # small region can have a higher rate but fewer total finds
            # than a bigger one), so an explicit rank column makes the
            # "most helipads found overall" reading unambiguous.
            regions_df_ranked = regions_df.sort_values("tiles_detected", ascending=False).reset_index(drop=True)
            regions_df_ranked.insert(0, t("field.rank_col"), range(1, len(regions_df_ranked) + 1))
            regions_df_display = regions_df_ranked.rename(columns={
                "region": t("field.region_col"), "tiles_total": t("field.tiles_col"),
                "tiles_detected": t("field.detected_col"), "detection_rate": t("field.rate_col"),
                "top_confidence": t("field.top_confidence_col"),
            })
            # Rank, Region, Detected, Tiles, Detection Rate, Top Confidence —
            # leads with the headline number (Detected) right after the
            # region name, instead of Tiles (the denominator) coming first.
            regions_df_display = regions_df_display[[
                t("field.rank_col"), t("field.region_col"), t("field.detected_col"),
                t("field.tiles_col"), t("field.rate_col"), t("field.top_confidence_col"),
            ]]

            st.markdown(f"#### {t('field.ranking_title')}")
            st.dataframe(
                regions_df_display.set_index(t("field.rank_col")).style.format({
                    t("field.rate_col"): "{:.1%}", t("field.top_confidence_col"): "{:.2f}",
                }).background_gradient(cmap="Blues", subset=[t("field.detected_col")]),
                use_container_width=True,
            )
            st.caption(t("field.rate_definition"))

            if "Inter-Zone Corridor" in regions_df["region"].values:
                st.caption(t("field.inter_zone_note"))

        generated_at = field_summary.get("generated_at")
        if generated_at:
            st.caption(f"{t('field.last_updated').format(date=generated_at)}")

        # ---- 3-model comparison on the same field validation ----
        # Same 7,943 tiles / 10 regions, run separately with exp1, exp2
        # and exp3's weights — shows whether the "best" model on the
        # curated val set (exp1, by Precision) actually generalizes as
        # well in the field as exp2/exp3 do.
        all_summaries = load_field_summaries_by_exp()
        if len(all_summaries) >= 2:
            with st.expander(t("field.compare.title"), expanded=True):
                st.caption(t("field.compare.body"))

                def _norm_region(name: str) -> str:
                    return str(name).strip().lower().replace("segment", "trecho")

                comparison_rows = {}
                for exp_name, summary in all_summaries.items():
                    for r in summary.get("regions", []):
                        key = _norm_region(r["region"])
                        comparison_rows.setdefault(key, {"__display__": format_region_display(r["region"])})
                        comparison_rows[key][exp_name] = r["detection_rate"]

                exp_names_sorted = sorted(all_summaries.keys())
                comp_df = pd.DataFrame([
                    {"Region": v["__display__"], **{e: v.get(e) for e in exp_names_sorted}}
                    for v in comparison_rows.values()
                ]).sort_values(exp_names_sorted[0], ascending=False, na_position="last")

                st.markdown(t("field.compare.table_title"))
                st.dataframe(
                    comp_df.set_index("Region").style.format(
                        {e: "{:.1%}" for e in exp_names_sorted}, na_rep="—"
                    ).background_gradient(cmap="Blues", subset=exp_names_sorted),
                    use_container_width=True,
                )

                comp_totals = {
                    exp_name: summary.get("totals", {}).get("detection_rate", 0.0)
                    for exp_name, summary in all_summaries.items()
                }
                total_cols = st.columns(len(comp_totals))
                for col, (exp_name, rate) in zip(total_cols, sorted(comp_totals.items())):
                    with col:
                        st.metric(exp_name, f"{rate*100:.1f}%")

                if {"exp1", "exp2", "exp3"} <= set(all_summaries):
                    st.markdown(f"""
                    <div style="border-left:3px solid #14b8a6; background:rgba(14,117,109,0.08);
                                border-radius:8px; padding:14px 18px; margin-top:14px;">
                        <p style="margin:0; color:#E2E8F0; font-size:14px; line-height:1.65;">
                            {t('field.compare.reality_check')}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                missing = set(FIELD_SUMMARY_PATHS_BY_EXP) - set(all_summaries)
                if missing:
                    st.caption(t("field.compare.missing").format(missing=", ".join(sorted(missing))))

# Footer
st.markdown("---")

components.html("""
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&display=swap" rel="stylesheet">
<style>
  html, body { margin:0; padding:0; overflow:visible; background:transparent; }
  @keyframes mindful-glow {
    0%   { text-shadow: 0 0 6px rgba(0,255,255,0.35), 0 0 14px rgba(0,255,255,0.15); }
    50%  { text-shadow: 0 0 20px rgba(0,255,255,0.95), 0 0 42px rgba(0,255,255,0.55), 0 0 60px rgba(0,255,255,0.25); }
    100% { text-shadow: 0 0 6px rgba(0,255,255,0.35), 0 0 14px rgba(0,255,255,0.15); }
  }
  .mindful-brand {
    display: block; text-align: center; text-decoration: none;
    font-family: 'Cormorant Garamond', Georgia, 'Times New Roman', serif;
    font-weight: 700; font-size: 34px; letter-spacing: .02em;
    animation: mindful-glow 3.2s ease-in-out infinite;
  }
  .mindful-brand span { text-decoration: none; }
  @media (prefers-reduced-motion: reduce) {
    .mindful-brand { animation: none; }
  }
</style>
<a class="mindful-brand" href="https://github.com/Mindful-AI-Research" target="_blank" rel="noopener noreferrer">
  <span style="color:#ffffff;">𖤐</span><span style="color:#00FFFF;"> Mindful</span><span style="color:#ffffff;"> AI</span><span style="color:#00FFFF;"> ॐ</span>
</a>
""", height=52)

st.markdown(f"""
<p align="center" style="margin: 10px 0 22px 0;">
  <a href="https://github.com/sponsors/Mindful-AI-Research" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/Sponsor-%E0%A5%90%20%E2%8B%86%20Mindful%20AI%20%E2%8B%86%20Research%20%26%20Consulting%20%F0%96%A4%90%20%E2%8B%86-3A424C?style=for-the-badge&logo=githubsponsors&logoColor=white&labelColor=07111F" alt="Sponsor ॐ ⋆ Mindful AI ⋆ Research & Consulting 𖤐 ⋆" height="36" style="vertical-align:middle;">
  </a>
</p>

<hr style="border:none; border-top:1px solid rgba(255,255,255,0.15); max-width: 900px; margin: 0 auto 24px auto;">

<p style="text-align:center; color:rgba(255,255,255,0.30); margin:0;">
{t("footer.tagline")}
</p>

<p style="text-align:center; color:rgba(255,255,255,0.35); margin:4px 0;">
{t("footer.line2")}
</p>

<p style="text-align:center; color:rgba(255,255,255,0.30); margin:6px 0 0 0; font-size:12px;">
{t("footer.line3")}
</p>

<hr style="border:none; border-top:1px solid rgba(255,255,255,0.15); max-width: 900px; margin: 20px auto 0 auto;">

<p style="text-align:center; color:#C9D6DE; font-weight:700; font-size:13px; letter-spacing:.02em; margin:20px 0 0 0; max-width:520px; margin-left:auto; margin-right:auto;">
{t("epigraph.echo")}
</p>
""", unsafe_allow_html=True)
