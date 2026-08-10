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
    "sidebar.music.play": {"en": "Play Music", "pt": "Play Music"},
    "sidebar.music.pause": {"en": "Pause Music", "pt": "Pausar Música"},
    "sidebar.music.missing": {
        "en": "Background track not found — add an mp3 at `assets/audio/passacaglia-deep-house-remix.mp3` to enable this.",
        "pt": "Faixa de fundo não encontrada — adicione um mp3 em `assets/audio/passacaglia-deep-house-remix.mp3` para habilitar.",
    },
    "sidebar.replay_heli": {"en": "Replay flyby", "pt": "Repetir sobrevoo"},
    "sidebar.spin_heli": {"en": "Spin", "pt": "Girar"},
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
    "about.discovery.missing": {
        "en": "Discovery coordinates CSV not found at `{path}`.",
        "pt": "CSV de coordenadas de descoberta não encontrado em `{path}`.",
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
    "tabs.about": {"en": "👥 About & Team", "pt": "👥 Sobre & Equipe"},
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
    "en": "🟢 **Training Areas (São Paulo)**: regional bounding boxes used to build and validate the training dataset. 🔵 **Discovery Dataset**: helipad candidates identified across other Brazilian states.",
    "pt": "🟢 **Áreas de Treinamento (São Paulo)**: regiões delimitadas por bounding boxes utilizadas na construção e validação do conjunto de treinamento. 🔵 **Dataset de Descoberta**: candidatos a helipontos identificados em outros estados brasileiros.",
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
    "en": "**{sp} training region(s)** 🟢 · **{other} discovered helipad(s)** 🔵",
    "pt": "**{sp} região(ões) de treinamento** 🟢 · **{other} heliponto(s) descoberto(s)** 🔵",
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

"map.density.subheader": {
    "en": "🌡️ Density Map",
    "pt": "🌡️ Mapa de Densidade",
},

"map.density.caption": {
    "en": "Interactive point and heatmap visualization of the Discovery Dataset from other Brazilian states. Rendered locally with Folium and CartoDB—no API key or account required.",
    "pt": "Visualização interativa em pontos e mapa de calor do Dataset de Descoberta em outros estados brasileiros. Renderizada localmente com Folium e CartoDB, sem necessidade de chave de API ou conta.",
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



# ---- Tab: About & Team ----
"about.header": {"en": "👥 About & Team", "pt": "👥 Sobre & Equipe"},

"about.body": {
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

        "This dashboard provides transparent access to the AI pipeline, dataset, model performance, "
        "and documented limitations."
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

        "Este dashboard apresenta de forma transparente o pipeline de IA, o conjunto de dados, "
        "o desempenho do modelo e suas limitações documentadas."
    ),
},

"about.institution": {"en": "Institution", "pt": "Instituição"},
"about.program": {"en": "Program", "pt": "Curso"},
"about.course": {"en": "Course", "pt": "Disciplina"},
"about.professor": {"en": "Professor", "pt": "Professor"},
"about.authors": {"en": "Authors", "pt": "Autores"},

    
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
    "dl.repo_title": {"en": "Explore the full source code", "pt": "Explore o código-fonte completo"},
    "dl.repo_desc": {
        "en": "Architecture, datasets, notebooks, and the complete AI pipeline are all on GitHub.",
        "pt": "Arquitetura, datasets, notebooks e o pipeline completo de IA estão todos no GitHub.",
    },

    # ---- Metrics tab ----
    "metrics.subheader": {"en": "📊 Experiment Metrics", "pt": "📊 Métricas dos Experimentos"},
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
    "field.region_col": {"en": "Region", "pt": "Região"},
    "field.tiles_col": {"en": "Tiles", "pt": "Tiles"},
    "field.detected_col": {"en": "Detected", "pt": "Detectado"},
    "field.rate_col": {"en": "Rate", "pt": "Taxa"},
    "field.top_confidence_col": {"en": "Top Confidence", "pt": "Confiança Máxima"},
    "field.inter_zone_note": {
        "en": "ℹ️ **Inter-Zone Corridor**: a bounding box covering the transition area between "
              "neighboring corporate districts, rather than a single named neighborhood.",
        "pt": "ℹ️ **Inter-Zone Corridor**: uma bounding box cobrindo a área de transição entre "
              "distritos corporativos vizinhos, em vez de um único bairro nomeado.",
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
        border-radius: 14px;
        padding: 20px 20px 18px 20px;
        text-align: left;
        position: relative;
        min-height: 176px;
        display: flex;
        flex-direction: column;
        border: 1px solid rgba(255,255,255,0.25);
        box-shadow: 0 3px 10px rgba(15, 23, 42, 0.12);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        margin-bottom: 18px;
    }
    .flow-step:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 26px rgba(15, 23, 42, 0.22);
    }
    .flow-step .flow-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        border-radius: 8px;
        font-size: 13px;
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
    """Interpolates from vivid blue (t=0, first step) to white (t=1, last step),
    the same blue family used across the dashboard's other blue-scale visuals
    (map detection-rate layer, metrics)."""
    blue, white = _hex_to_rgb("#1E3A8A"), _hex_to_rgb("#FFFFFF")
    return _rgb_to_hex(tuple(int(a + (b - a) * t) for a, b in zip(blue, white)))


# ========================= MAP TILE PROVIDERS =========================
# Using explicit URL templates (instead of Folium's built-in preset strings
# like "CartoDB dark_matter") because Folium ignores the custom `name=` we
# pass for known presets and falls back to its own internal identifier
# (e.g. "cartodbdarkmatter") in the layer control. A raw URL template has no
# such special-casing, so our friendly name is always used.
CARTO_DARK_URL = "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
CARTO_LIGHT_URL = "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
CARTO_ATTR = (
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
    'contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
)


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


@st.cache_data(show_spinner=False)
def load_discovery_dataset_stats(csv_path: Path = COORDS_CSV) -> dict | None:
    """Quick coverage summary of the national helipad-discovery dataset
    (src/geospatial/helipad_bot.py output) — total points collected and
    how many distinct location names appear, as a proxy for geographic
    diversity. A full per-state breakdown needs geocode_states.py to have
    been run first (pending as of this writing), so this only shows what's
    derivable from the raw CSV today."""
    if not csv_path.exists():
        return None
    try:
        df = pd.read_csv(csv_path)
    except Exception:
        return None
    bairro_col = "Nome do Bairro" if "Nome do Bairro" in df.columns else None
    return {
        "total_points": len(df),
        "distinct_locations": df[bairro_col].nunique() if bairro_col else None,
    }


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

    story.append(Paragraph("🚁 Helipad Detector" if not is_pt else "🚁 Helipad Detector", title_style))
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


# ========================= FIELD DETECTIONS BY REGION (data) =========================
# reports/detection_summary_by_region.json is generated by
# src/geospatial/auto_triage_regions.py. Defined here (before it's first used
# in the Map tab) so both the Map tab and the Field Detections tab can read it.
FIELD_SUMMARY_PATH = Path("reports/detection_summary_by_region.json")


@st.cache_data(show_spinner=False)
def load_field_detection_summary():
    if not FIELD_SUMMARY_PATH.exists():
        return None
    try:
        with open(FIELD_SUMMARY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


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
    st.caption(t("sidebar.music.title"))
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

    with st.expander(t("sidebar.extras"), expanded=False):
        heli_col1, heli_col2 = st.columns(2)
        with heli_col1:
            if st.button("🚁 " + t("sidebar.replay_heli"), use_container_width=True):
                st.session_state["heli_flight_start"] = time.time()
                st.rerun()
        with heli_col2:
            if st.button("🌀 " + t("sidebar.spin_heli"), use_container_width=True):
                st.session_state["heli_spin_start"] = time.time()
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

# ---- Flying helicopter (self-contained iframe — no cross-frame access) ----
#
# Earlier version tried to inject the helicopter into the PARENT document
# (window.parent.document) so it could float above every tab. That relies
# on the components.html iframe being same-origin with the main app; if
# Streamlit ever adds a `sandbox` attribute without `allow-same-origin`,
# that access throws and gets silently swallowed by the try/catch —
# nothing renders, no visible error. This version never leaves its own
# iframe, so there's no cross-origin gamble.
#
# The next version after that gated rendering behind a fixed 18-second
# real-time window from session start, to survive mid-flight Streamlit
# reruns. That backfired for actually *seeing* it: if more than 18 real
# seconds passed between the page loading and someone looking at it
# (extremely likely — plenty else on the page to read first), the window
# had already closed and nothing rendered — indistinguishable from it
# never having worked at all. Simpler and much more reliable: loop the
# flight forever (CSS `infinite`), so it's simply always visible,
# whenever anyone looks. Same negative-animation-delay trick keeps it
# looking continuous (not restarting) across Streamlit reruns.
LAP_SECONDS = 6

if "heli_flight_start" not in st.session_state:
    st.session_state["heli_flight_start"] = time.time()
if "heli_spin_start" not in st.session_state:
    st.session_state["heli_spin_start"] = None

_heli_elapsed = time.time() - st.session_state["heli_flight_start"]

_heli_spinning = False
_spin_elapsed = 0.0
if st.session_state["heli_spin_start"] is not None:
    _spin_elapsed = time.time() - st.session_state["heli_spin_start"]
    _heli_spinning = _spin_elapsed < 2.2

components.html(f"""
<style>
  html, body {{ margin:0; padding:0; overflow:hidden; background:transparent; border: 3px solid red; }}
  @keyframes heli-fly-across {{
    0%   {{ left: 0%;   top: 24px; transform: rotate(-4deg)  scale(1);    opacity: 0; }}
    4%   {{ opacity: 1; }}
    18%  {{ top: 10px;  transform: rotate(14deg)  scale(1.04); }}
    34%  {{ top: 30px;  transform: rotate(-16deg) scale(1); }}
    50%  {{ left: 48%;  top: 14px;  transform: rotate(10deg)  scale(1.05); }}
    66%  {{ top: 32px;  transform: rotate(-14deg) scale(1); }}
    82%  {{ top: 8px;   transform: rotate(16deg)  scale(1.04); }}
    96%  {{ opacity: 1; }}
    100% {{ left: 94%;  top: 22px;  transform: rotate(-5deg)  scale(1);   opacity: 0; }}
  }}
  @keyframes heli-spin {{
    0%   {{ transform: rotate(0deg)   scale(1);    opacity: 1; }}
    85%  {{ transform: rotate(360deg) scale(1.15); opacity: 1; }}
    100% {{ transform: rotate(360deg) scale(1);    opacity: 0; }}
  }}
  .heli-flyby {{
    position: absolute; font-size: 34px;
    filter: drop-shadow(0 2px 6px rgba(0,0,0,.35));
  }}
  @media (prefers-reduced-motion: reduce) {{
    .heli-flyby {{ display: none; }}
  }}
</style>
<div style="position:absolute; top:2px; left:6px; color:yellow; font-family:monospace; font-size:10px; z-index:9999;">
  DEBUG: elapsed={_heli_elapsed % LAP_SECONDS:.2f}s spinning={_heli_spinning}
</div>
{"<div class='heli-flyby' style='animation: heli-spin 2.2s ease-in-out 1 forwards; animation-delay: -" + f"{_spin_elapsed:.4f}" + "s; left:46%; top:14px;'>🚁</div>" if _heli_spinning else
 "<div class='heli-flyby' style='animation: heli-fly-across " + str(LAP_SECONDS) + "s cubic-bezier(.45,.05,.55,.95) infinite alternate; animation-delay: -" + f"{_heli_elapsed % LAP_SECONDS:.4f}" + "s;'>🚁</div>"}
""", height=60)


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
    st.caption(t("search.caption"))

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

    map_tiles = "CartoDB dark_matter" if dark_mode else "CartoDB positron"
    map_tiles_label = t("map.dark_base") if dark_mode else t("map.light_base")

    sp_df = load_helipad_locations(SP_COORDS_CSV)
    other_df = load_helipad_locations(COORDS_CSV)

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
        tile_url = CARTO_DARK_URL if dark_mode else CARTO_LIGHT_URL
        fmap = folium.Map(location=[center_lat, center_lon], zoom_start=5, tiles=None)
        folium.TileLayer(tiles=tile_url, attr=CARTO_ATTR, name=map_tiles_label, control=True).add_to(fmap)

        sp_layer = folium.FeatureGroup(name=f"🟢 {t('map.sp_layer')} ({len(sp_df)})", show=True)
        for _, row in sp_df.iterrows():
            name = format_region_display(row.get("Nome do Bairro", "Unknown"))
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=folium.Popup(f"<b>{name}</b><br>{t('map.training_region')}", max_width=250),
                tooltip=name,
                icon=folium.Icon(color="green", icon="home"),
            ).add_to(sp_layer)
        sp_layer.add_to(fmap)

        other_layer = folium.FeatureGroup(name=f"🔵 {t('map.other_layer')} ({len(other_df)})", show=True)
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

        # ---- Layer 3: field detection rate by region (blue scale, same as tables) ----
        field_summary_for_map = load_field_detection_summary()
        if field_summary_for_map and not sp_df.empty:
            regions_by_slug = {r["region"]: r for r in field_summary_for_map.get("regions", [])}
            rates = [r["detection_rate"] for r in regions_by_slug.values()]
            min_rate, max_rate = (min(rates), max(rates)) if rates else (0.0, 1.0)

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
                folium.CircleMarker(
                    location=[row["lat"], row["lon"]],
                    radius=10 + rate * 40,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.85,
                    tooltip=f"{display_name}: {region_stats['tiles_detected']}/{region_stats['tiles_total']} ({rate*100:.1f}%)",
                    popup=folium.Popup(
                        f"<b>{display_name}</b><br>"
                        f"{region_stats['tiles_detected']} {t('map.tiles_detected')}<br>"
                        f"{t('map.rate')}: {rate*100:.1f}%",
                        max_width=250,
                    ),
                ).add_to(detection_layer)
            if matched:
                detection_layer.add_to(fmap)

        folium.LayerControl(collapsed=False).add_to(fmap)
        _force_leaflet_resize(fmap)

        st.write(t("map.summary").format(sp=len(sp_df), other=len(other_df)))
        st_folium(fmap, use_container_width=True, height=520, key=f"main_map_{map_tiles}")

        with st.expander(t("map.raw_data_expander")):
            t1, t2 = st.tabs([t("map.raw_data.sp_tab"), t("map.raw_data.other_tab")])
            with t1:
                sp_df_display = sp_df.copy()
                if "Nome do Bairro" in sp_df_display.columns:
                    _segment_word = "Trecho" if st.session_state.get("lang") == "pt" else "Segment"
                    sp_df_display["Nome do Bairro"] = sp_df_display["Nome do Bairro"].astype(str).str.replace(
                        r"\btrecho\b", _segment_word, regex=True, case=False
                    )
                st.dataframe(sp_df_display, use_container_width=True)
            with t2:
                st.dataframe(other_df, use_container_width=True)

        st.divider()
        col_density_title, col_density_toggle = st.columns([4, 1])
        with col_density_title:
            st.subheader(t("map.density.subheader"))
            st.caption(t("map.density.caption"))
        with col_density_toggle:
            density_dark_mode = st.toggle(t("map.dark_mode"), value=True, key="density_map_theme")

        density_tiles = "CartoDB dark_matter" if density_dark_mode else "CartoDB positron"
        density_tile_url = CARTO_DARK_URL if density_dark_mode else CARTO_LIGHT_URL

        if other_df.empty:
            st.info(t("map.density.no_coords").format(path=COORDS_CSV))
        else:
            dark_map = folium.Map(
                location=[other_df["lat"].mean(), other_df["lon"].mean()],
                zoom_start=5,
                tiles=None,
            )
            folium.TileLayer(tiles=density_tile_url, attr=CARTO_ATTR, control=False).add_to(dark_map)
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
            bg_light = _shade(base, 0.22)
            bg_dark = _shade(base, -0.22)
            gradient = f"linear-gradient(135deg, {bg_light} 0%, {base} 55%, {bg_dark} 100%)"
            accent_rgb = _hex_to_rgb(base)
            glow = f"rgba({accent_rgb[0]},{accent_rgb[1]},{accent_rgb[2]},0.38)"
            is_light = frac >= 0.6
            title_color = "#0F172A" if is_light else "#FFFFFF"
            desc_color = "#334155" if is_light else "#DBEAFE"
            badge_bg = "rgba(15,23,42,0.10)" if is_light else "rgba(255,255,255,0.20)"
            badge_color = "#1E3A8A" if is_light else "#FFFFFF"
            with col:
                st.markdown(f"""
                <div class="flow-step" style="background:{gradient}; border-top:3px solid {bg_dark}; box-shadow: 0 4px 16px {glow};">
                    <span class="flow-badge" style="background:{badge_bg}; color:{badge_color};">{step_idx+1:02d}</span>
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

# ====================== TAB: About & Team ======================
with tab_about:
    st.header(t("about.header"))
    st.markdown(t("about.body"))
    st.markdown(f"""
    <div class="dark-card" style="text-align:left;">
        <table style="width:100%; font-size:14px; color:#E2E8F0; border-collapse:collapse;">
            <tr><td style="padding:6px 0; color:#93C5FD; width:160px; vertical-align:top;">{t("about.institution")}</td>
                <td style="padding:6px 0;"><b>PUC-SP — FACEI</b></td></tr>
            <tr><td style="padding:6px 0; color:#93C5FD; vertical-align:top;">{t("about.program")}</td>
                <td style="padding:6px 0;">BSc in Human Centered-AI & Data Science</td></tr>
            <tr><td style="padding:6px 0; color:#93C5FD; vertical-align:top;">{t("about.course")}</td>
                <td style="padding:6px 0;">Machine Learning / Computer Vision — Project P2</td></tr>
            <tr><td style="padding:6px 0; color:#93C5FD; vertical-align:top;">{t("about.professor")}</td>
                <td style="padding:6px 0;">Rooney Ribeiro Albuquerque Coelho</td></tr>
            <tr><td style="padding:6px 0; color:#93C5FD; vertical-align:top;">{t("about.authors")}</td>
                <td style="padding:6px 0;">
                    Carlos Antonio dos Santos Roth Gorham<br>
                    Fabiana Campanari<br>
                    Pedro Vyctor Almeida
                </td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

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
        st.caption(t("about.discovery.pending"))

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

        for i, row in metrics_df.iterrows():
            target = cols[i] if n_exp <= 4 else st
            with target:
                netron_link = netron_url_for(row['Experiment']) or "https://netron.app/"
                netron_label = t("metrics.netron_view") if row['Experiment'] in MODEL_WEIGHTS_BY_EXP else t("metrics.netron_manual")
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="margin:0 0 8px 0;">{row['Experiment']}</h4>
                    <p style="margin:2px 0; color:#64748B; font-size:13px;">
                        {t('metrics.best_epoch')} {row['Best Epoch']} / {row['Total Epochs']}
                    </p>
                    <p style="margin:6px 0; font-size:22px; font-weight:700; color:#1E3A8A;">
                        {row['mAP@50-95']:.3f}
                    </p>
                    <p style="margin:0; color:#64748B; font-size:12px;">mAP@50-95</p>
                    <p style="margin:8px 0 0 0;">
                        <a href="{netron_link}" target="_blank" rel="noopener noreferrer"
                           style="font-size:12px; color:#0E756D; font-weight:600; text-decoration:none;">
                            {netron_label}
                        </a>
                    </p>
                </div>
                """, unsafe_allow_html=True)

        # Netron previews render full-width, stacked one per row below the
        # metric cards — a narrow column (1 of up to 4) is too cramped for
        # an interactive graph viewer with its own zoom/pan controls.
        # Loaded on demand (not expanded=True) so opening the Metrics tab
        # doesn't eagerly fire 3 external requests to netron.app on every
        # rerun — only the experiment(s) you actually want to inspect.
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
                    st.success(t("metrics.outperformed").format(exp=row['Experiment'], delta=f"{delta:+.4f}"))
                elif delta < -0.005:
                    st.warning(t("metrics.underperformed").format(exp=row['Experiment'], delta=f"{delta:+.4f}"))
                else:
                    st.info(t("metrics.tied").format(exp=row['Experiment'], delta=f"{delta:+.4f}"))

        # ---- Per-epoch metric evolution (real data from results.csv) ----
        curves = load_experiment_curves()
        if curves:
            st.markdown(t("metrics.evolution"))
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
            st.markdown(t("metrics.confusion_matrix"))
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
        with card_cols[0]:
            st.markdown(f"""
            <div class="metric-card">
                <p style="margin:6px 0; font-size:26px; font-weight:700; color:#1E3A8A;">{total_detected}</p>
                <p style="margin:0; color:#64748B; font-size:12px;">{t("field.detected_total")}</p>
            </div>
            """, unsafe_allow_html=True)
        with card_cols[1]:
            st.markdown(f"""
            <div class="metric-card">
                <p style="margin:6px 0; font-size:26px; font-weight:700; color:#1E3A8A;">{total_tiles}</p>
                <p style="margin:0; color:#64748B; font-size:12px;">{t("field.tiles_processed")}</p>
            </div>
            """, unsafe_allow_html=True)
        with card_cols[2]:
            st.markdown(f"""
            <div class="metric-card">
                <p style="margin:6px 0; font-size:26px; font-weight:700; color:#1E3A8A;">{total_rate*100:.1f}%</p>
                <p style="margin:0; color:#64748B; font-size:12px;">{t("field.overall_rate")}</p>
            </div>
            """, unsafe_allow_html=True)

        if regions:
            st.markdown("")
            regions_df = pd.DataFrame(regions).sort_values("detection_rate", ascending=False)
            regions_df["region"] = regions_df["region"].apply(format_region_display)
            regions_df_display = regions_df.rename(columns={
                "region": t("field.region_col"), "tiles_total": t("field.tiles_col"),
                "tiles_detected": t("field.detected_col"), "detection_rate": t("field.rate_col"),
                "top_confidence": t("field.top_confidence_col"),
            })

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

            st.dataframe(
                regions_df_display.set_index(t("field.region_col")).style.format({
                    t("field.rate_col"): "{:.1%}", t("field.top_confidence_col"): "{:.2f}",
                }).background_gradient(cmap="Blues", subset=[t("field.rate_col")]),
                use_container_width=True,
            )

            if "Inter-Zone Corridor" in regions_df["region"].values:
                st.caption(t("field.inter_zone_note"))

        generated_at = field_summary.get("generated_at")
        if generated_at:
            st.caption(f"{t('field.last_updated').format(date=generated_at)}")

# Footer
st.markdown("---")

components.html("""
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&display=swap" rel="stylesheet">
<style>
  html, body { margin:0; padding:0; overflow:hidden; background:transparent; }
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
    <img src="https://img.shields.io/badge/Sponsor-%E0%A5%90%20%E2%8B%86%20Mindful%20AI%20%F0%96%A4%90%20%E2%8B%86-00FFFF?style=flat-square&logo=githubsponsors&logoColor=white&labelColor=0a1f44" alt="Sponsor ॐ ⋆ Mindful AI 𖤐 ⋆" height="28" style="vertical-align:middle;">
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
""", unsafe_allow_html=True)
