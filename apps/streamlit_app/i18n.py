"""UI strings (EN/PT-BR). Pure data — edit here to change any label.

Keys are looked up by `t()` in app.py; unknown keys fall back to the key itself.
"""

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
    "about.discovery.location_col": {"en": "Neighborhood", "pt": "Bairro"},
    "about.discovery.date_col": {"en": "Collected on", "pt": "Coletado em"},
    "about.discovery.missing": {
        "en": "Discovery coordinates CSV not found at `{path}`.",
        "pt": "CSV de coordenadas de descoberta não encontrado em `{path}`.",
    },

    # ---- Global Context — helicopter air mobility worldwide ----
    # This table used to be a "Top 10" ranking with a fabricated "Rate (%)"
    # column (those numbers were an exact copy of this project's own SP
    # field-validation detection-rate-by-region table, relabeled onto 10
    # world cities — unrelated data, invented precision, not a sourced
    # statistic). It has been replaced with a non-ranked Global Context
    # table: City / Country / Helicopter Air Mobility Context / Reference
    # Source, one real official source per city, no numeric column at all.
    # Mirrors the "Global Context" table and its [!NOTE]/[!TIP] callouts in
    # README.md exactly — see conteudo_pt_traduzido.md for the approved text.
    "cities.header": {
        "en": "🌍 Global Context — Helicopter Air Mobility Worldwide",
        "pt": "🌍 Contexto Global — Mobilidade Aérea por Helicóptero no Mundo",
    },
    # Holds the [!TIP] callout text, rendered as the highlighted teal card
    # right below the table.
    "cities.why_sao_paulo": {
        "en": "São Paulo was selected as the focus of **Helipad Detector** due to the combination "
              "of high urban density, a large concentration of buildings, a significant presence "
              "of rooftop heliport infrastructure, and intense helicopter traffic. This context "
              "demonstrates how Computer Vision and satellite data can support the automated "
              "mapping of urban infrastructure. The model's detections represent **visual "
              "candidates** and do not constitute regulatory, operational, or aeronautical "
              "confirmation of the existence of a heliport.",
        "pt": "São Paulo foi escolhida como foco do **Helipad Detector** pela combinação de "
              "elevada densidade urbana, grande concentração de edifícios, presença significativa "
              "de infraestrutura de helipontos em coberturas e tráfego intenso de helicópteros. "
              "Esse contexto permite demonstrar como a Visão Computacional e os dados de satélite "
              "podem apoiar o mapeamento automatizado de infraestrutura urbana. As detecções do "
              "modelo representam **candidatos visuais** e não constituem confirmação regulatória, "
              "operacional ou aeronáutica da existência de um heliponto.",
    },
    # Holds the [!NOTE] callout, rendered as a blockquote right below the table.
    "cities.interpretation.title": {
        "en": "📌 Note on This Table",
        "pt": "📌 Nota sobre esta tabela",
    },
    "cities.interpretation.text": {
        "en": "The cities presented in this table are qualitative references to urban "
              "environments where helicopters are used in different operational contexts. The "
              "selection does not constitute an official global ranking, a standardized "
              "statistical comparison of fleets, or an operational database directly equivalent "
              "across all locations. São Paulo is the primary study area of **Helipad Detector** "
              "and presents a specific operational context, including specialized helicopter "
              "traffic management through **HELICONTROL**.",
        "pt": "As cidades apresentadas nesta tabela são referências qualitativas de ambientes "
              "urbanos que utilizam helicópteros em diferentes contextos operacionais. A seleção "
              "não constitui um ranking global oficial, uma comparação estatística padronizada de "
              "frotas ou uma base de dados operacional diretamente equivalente entre todas as "
              "localidades. São Paulo é a principal área de estudo do **Helipad Detector** e "
              "apresenta um contexto operacional específico, incluindo o gerenciamento "
              "especializado do tráfego de helicópteros por meio do **HELICONTROL**.",
    },
    "cities.table.columns": {
        "en": ["City", "Country", "Helicopter Air Mobility Context", "Reference Source"],
        "pt": ["Cidade", "País", "Contexto de mobilidade aérea por helicópteros", "Fonte de referência"],
    },
    "cities.table.data": {
        "en": [
            ["**São Paulo**", "🇧🇷 Brazil",
             "Urban helicopter operations in a high-density environment, supported by specialized "
             "HELICONTROL air traffic management within the Congonhas operational area",
             "[**FAB** - Brazilian Air Force: HELICONTROL](https://www.fab.mil.br/noticias/imprime/42060/CONTROLE%20DO%20ESPA%C3%87O%20A%C3%89REO%20-%20HELICONTROL:%20Seguran%C3%A7a%20e%20fluidez%20no%20controle%20de%20helic%C3%B3pteros%20em%20S%C3%A3o%20Paulo)"],
            ["New York City", "🇺🇸 United States",
             "Public heliports, air taxi flights, general aviation, passenger transport, military "
             "operations, and regulated sightseeing flights",
             "[New York City Council — Helicopter Noise and Safety](https://council.nyc.gov/data/helicopter-noise-and-safety/)"],
            ["Tokyo", "🇯🇵 Japan",
             "Corporate, emergency, public safety, and specialized transport operations within the "
             "context of Japanese civil aviation",
             "[Japan Ministry of Land, Infrastructure, Transport and Tourism (MLIT)](https://www.mlit.go.jp/en/)"],
            ["Rio de Janeiro", "🇧🇷 Brazil",
             "Executive aviation, urban transport, and operations associated with offshore "
             "activities in the oil and gas sectors",
             "[National Civil Aviation Agency (ANAC)](https://www.gov.br/anac/pt-br)"],
            ["London", "🇬🇧 United Kingdom",
             "Urban heliport infrastructure serving executive operations, VIP services, landings, "
             "takeoffs, refueling, and charter flights",
             "[London Heliport](https://londonheliport.co.uk/)"],
            ["Belo Horizonte", "🇧🇷 Brazil",
             "Executive aviation, corporate operations, and helicopter use in specialized services",
             "[National Civil Aviation Agency (ANAC)](https://www.gov.br/anac/pt-br)"],
            ["Santiago", "🇨🇱 Chile",
             "Executive, corporate, and specialized operations under the regulations of the "
             "Chilean civil aviation authority",
             "[General Directorate of Civil Aeronautics of Chile (DGAC)](https://www.dgac.gob.cl/)"],
            ["Mexico City", "🇲🇽 Mexico",
             "Executive transport, government activities, public safety, and specialized aerial "
             "operations",
             "[Federal Civil Aviation Agency of Mexico (AFAC)](https://www.gob.mx/afac)"],
            ["Bogotá", "🇨🇴 Colombia",
             "Executive, emergency, and specialized air services under the regulations of the "
             "Colombian civil aviation authority",
             "[Aerocivil Colombia](https://www.aerocivil.gov.co/)"],
            ["Beijing", "🇨🇳 China",
             "Government, executive, and specialized air services within the context of Chinese "
             "civil aviation",
             "[**CAAC** - Civil Aviation Administration of China](http://www.caac.gov.cn/English/)"],
        ],
        "pt": [
            ["**São Paulo**", "🇧🇷 Brasil",
             "Operações urbanas de helicópteros em um ambiente de alta densidade, apoiadas pelo "
             "gerenciamento especializado do HELICONTROL na área operacional de Congonhas",
             "[**FAB** - Força Aérea Brasileira: HELICONTROL](https://www.fab.mil.br/noticias/imprime/42060/CONTROLE%20DO%20ESPA%C3%87O%20A%C3%89REO%20-%20HELICONTROL:%20Seguran%C3%A7a%20e%20fluidez%20no%20controle%20de%20helic%C3%B3pteros%20em%20S%C3%A3o%20Paulo)"],
            ["Nova York", "🇺🇸 Estados Unidos",
             "Heliportos públicos, voos de táxi aéreo, aviação geral, transporte de passageiros, "
             "operações militares e passeios turísticos regulamentados",
             "[New York City Council — Helicopter Noise and Safety](https://council.nyc.gov/data/helicopter-noise-and-safety/)"],
            ["Tóquio", "🇯🇵 Japão",
             "Operações corporativas, emergenciais, de segurança pública e de transporte "
             "especializado no contexto da aviação civil japonesa",
             "[Ministério da Terra, Infraestrutura, Transporte e Turismo do Japão (MLIT)](https://www.mlit.go.jp/en/)"],
            ["Rio de Janeiro", "🇧🇷 Brasil",
             "Aviação executiva, transporte urbano e operações associadas às atividades offshore "
             "dos setores de petróleo e gás",
             "[Agência Nacional de Aviação Civil (ANAC)](https://www.gov.br/anac/pt-br)"],
            ["Londres", "🇬🇧 Reino Unido",
             "Infraestrutura de heliporto urbano destinada a operações executivas, serviços VIP, "
             "pousos, decolagens, abastecimento e voos fretados",
             "[London Heliport](https://londonheliport.co.uk/)"],
            ["Belo Horizonte", "🇧🇷 Brasil",
             "Aviação executiva, operações corporativas e utilização de helicópteros em serviços "
             "especializados",
             "[Agência Nacional de Aviação Civil (ANAC)](https://www.gov.br/anac/pt-br)"],
            ["Santiago", "🇨🇱 Chile",
             "Operações executivas, corporativas e especializadas sob a regulamentação da "
             "autoridade de aviação civil chilena",
             "[Dirección General de Aeronáutica Civil de Chile (DGAC)](https://www.dgac.gob.cl/)"],
            ["Cidade do México", "🇲🇽 México",
             "Transporte executivo, atividades governamentais, segurança pública e operações "
             "aéreas especializadas",
             "[Agencia Federal de Aviación Civil do México (AFAC)](https://www.gob.mx/afac)"],
            ["Bogotá", "🇨🇴 Colômbia",
             "Operações executivas, emergenciais e serviços aéreos especializados sob a "
             "regulamentação da autoridade de aviação civil colombiana",
             "[Aerocivil Colômbia](https://www.aerocivil.gov.co/)"],
            ["Pequim", "🇨🇳 China",
             "Operações governamentais, executivas e serviços aéreos especializados no contexto "
             "da aviação civil chinesa",
             "[**CAAC** - Administração da Aviação Civil da China](http://www.caac.gov.cn/English/)"],
        ],
    },

    # ---- Main header ----
    "main.title": {"en": "🚁 Helipad Detector", "pt": "🚁 Helipad Detector"},
    "main.subtitle": {"en": "AI + Satellite Imagery • São Paulo", "pt": "IA + Imagens de Satélite • São Paulo"},
    "main.active_model": {"en": "Active model:", "pt": "Modelo ativo:"},
    "main.active_model.none": {"en": "_none yet — detection tabs disabled_", "pt": "_nenhum ainda — abas de detecção desabilitadas_"},

    
    # ---- Tab labels ----
    "tabs.metrics": {"en": "📊 Experiment Metrics", "pt": "📊 Métricas dos Experimentos"},
    "tabs.field": {"en": "🌍 Field Detections by Region", "pt": "🌍 Detecções de Campo por Região"},
    "tabs.map": {"en": "🗺️ Maps", "pt": "🗺️ Mapas"},
    # Promoted from a sub-tab nested inside "Map" to its own top-level tab so it
    # doesn't take an extra click to reach and so "Beta" is visible in the main
    # tab bar, not one level down.
    "tabs.flights": {"en": "🚁 Live Traffic · Beta", "pt": "🚁 Tráfego ao Vivo · Beta"},
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
    "upload.success": {"en": "✅ Possible helipad detected (visual detection only; human review required).", "pt": "✅ Possível heliponto detectado (apenas detecção visual; exige revisão humana)."},
    "upload.warning_none": {"en": "No helipad found.", "pt": "Nenhum heliponto encontrado."},

    # ---- Shared: mandatory scope-of-detection disclaimer (shown under any detection result) ----
    "detection.disclaimer": {
        "en": "Automated, image-based visual detection, subject to errors, and not equivalent to "
              "operational, legal, safety, or aeronautical validation.",
        "pt": "Detecção visual automatizada baseada em imagem, sujeita a erros e não equivalente a "
              "validação operacional, legal, de segurança ou aeronáutica.",
    },

    # ---- Tab 2: Search by Region ----
    "search.subheader": {"en": "🔎 Search for Helipads in a Region", "pt": "🔎 Buscar Helipontos em uma Região"},
    "search.preset_label": {"en": "Jump to a known corridor (optional)", "pt": "Ir direto para um corredor conhecido (opcional)"},
    "search.preset_custom": {"en": "Custom coordinates", "pt": "Coordenadas personalizadas"},
    "search.preset_help": {
        "en": "Small (~60-80 tile) boxes centered on the real bounding box of each field-validation region (Section 9, sp_neighborhoods_bbox.csv) — good for a quick live demo without triggering Streamlit's throttle.",
        "pt": "Caixas pequenas (~60-80 tiles) centradas na bounding box real de cada região da validação de campo (Seção 9, sp_neighborhoods_bbox.csv) — boas para uma demo ao vivo rápida, sem disparar o throttle do Streamlit.",
    },
    "search.preset_scope_note": {
        "en": "ℹ️ Each preset is a small, fixed window (~60-80 tiles) centered on that region — not a representative sample of it. "
              "The full field-validation numbers (hundreds to 1,000+ tiles per region, shown in Field Detections by Region) cover the "
              "entire mapped area; a preset here can legitimately find zero helipads even in a region with a high detection rate, simply "
              "because the helipads there sit outside this particular small window. That is expected behavior, not an error.",
        "pt": "ℹ️ Cada preset é uma janela pequena e fixa (~60-80 tiles) centrada naquela região — não é uma amostra representativa dela. "
              "Os números completos da validação de campo (centenas a 1.000+ tiles por região, na aba Field Detections by Region) cobrem "
              "a área mapeada inteira; um preset aqui pode legitimamente não encontrar nenhum heliponto mesmo numa região com taxa de "
              "detecção alta, simplesmente porque os helipontos de lá ficam fora dessa janela pequena específica. Isso é esperado, não é erro.",
    },
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
    "search.failed_downloads": {
        "en": "tile(s) could not be downloaded (network hiccup) and were skipped.",
        "pt": "tile(s) não puderam ser baixados (falha de rede) e foram ignorados.",
    },
    "search.blank_skipped": {
        "en": "blank/corrupted tile(s) skipped (partial ESRI download failure).",
        "pt": "tile(s) vazio(s)/corrompido(s) ignorados (falha parcial no download do ESRI).",
    },
    "search.download_all_zip": {"en": "⬇️ Download all as .zip", "pt": "⬇️ Baixar todos em .zip"},
    "search.found": {"en": "possible helipad detection(s) found", "pt": "possível(is) detecção(ões) de heliponto encontrada(s)"},
    "search.in_region": {"en": "in the region!", "pt": "na região!"},
    "search.download": {"en": "⬇️ Download", "pt": "⬇️ Baixar"},
    "search.download_individually": {
        "en": "Use the buttons above to download individually.",
        "pt": "Use os botões acima para baixar individualmente.",
    },
    "search.none_found": {"en": "No possible helipad detection in this region.", "pt": "Nenhuma possível detecção de heliponto nesta região."},

    
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
    "en": "🔴 **Training Areas (São Paulo)**: regional bounding boxes used to build and validate the training dataset. 🟢 **Discovery Dataset**: helipad candidates identified across other Brazilian states.",
    "pt": "🔴 **Áreas de Treinamento (São Paulo)**: regiões delimitadas por bounding boxes utilizadas na construção e validação do conjunto de treinamento. 🟢 **Dataset de Descoberta**: candidatos a helipontos identificados em outros estados brasileiros.",
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
    "en": "🟢 Field detection rate",
    "pt": "🟢 Taxa de detecção em campo",
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
    "en": "**{sp} training region(s)** 🔴 · **{other} discovered helipad(s)** 🟢",
    "pt": "**{sp} região(ões) de treinamento** 🔴 · **{other} heliponto(s) descoberto(s)** 🟢",
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

"map.flights_layer": {
    "en": "🚁 Live helicopter traffic",
    "pt": "🚁 Tráfego de helicópteros ao vivo",
},

"map.flights_caption": {
    "en": "Real-time aircraft positions over the São Paulo metro area, sourced live from **adsb.fi** "
          "(free, no-key public API). This is live radar-like telemetry, not a YOLO detection — it is "
          "unrelated to the satellite-image pipeline used elsewhere in this app.",
    "pt": "Posições de aeronaves em tempo real na região metropolitana de São Paulo, obtidas ao vivo do "
          "**adsb.fi** (API pública, gratuita, sem necessidade de chave). Isso é telemetria ao vivo, "
          "do tipo radar — não é uma detecção do YOLO, e não tem relação com o pipeline de imagens de satélite "
          "usado no restante do app.",
},

"map.flights_disclaimer": {
    "en": "⚠️ **Helicopter identification is best-effort, not guaranteed.** Most contacts report a real "
          "aircraft type code, which confirms a rotorcraft reliably (✈️ shown as \"Confirmed\" below); for "
          "the rest, this layer falls back to excluding known commercial-airline callsigns and shows "
          "everything else as an **unconfirmed** candidate (⚠️ badge on the map), which may include small "
          "fixed-wing aircraft, air taxis or executive jets, not only helicopters. Coverage is also partial: "
          "the feed only sees aircraft within range of a volunteer ADS-B receiver that are actively "
          "transmitting. An empty or sparse map means \"nothing detected/confirmed by this feed right now\", "
          "never \"no helicopters flying\".",
    "pt": "⚠️ **A identificação de helicóptero é um melhor esforço, não uma garantia.** A maioria dos "
          "contatos reporta um código real de tipo de aeronave, o que confirma um helicóptero de forma "
          "confiável (mostrado como \"confirmado\" abaixo); para o restante, esta camada cai para excluir "
          "callsigns de companhias aéreas conhecidas e mostra o restante como candidato **não confirmado** "
          "(badge ⚠️ no mapa), o que pode incluir aviões pequenos, táxi aéreo ou jatos executivos, não só "
          "helicópteros. A cobertura também é parcial: o feed só enxerga aeronaves dentro do alcance de um "
          "receptor ADS-B voluntário e que estejam de fato transmitindo. Um mapa vazio ou com poucos pontos "
          "significa \"nada detectado/confirmado por este feed agora\", nunca \"nenhum helicóptero voando\".",
},

"map.flights_confirmed": {
    "en": "Confirmed rotorcraft (aircraft type)",
    "pt": "Helicóptero confirmado (tipo da aeronave)",
},

"map.flights_unconfirmed": {
    "en": "Unconfirmed — small aircraft, not necessarily a helicopter",
    "pt": "Não confirmado — aeronave pequena, não necessariamente helicóptero",
},

"map.flights_trail_note": {
    "en": "Flight trails are built session-locally, point by point, from the moments this dashboard was open "
          "and refreshed — they are **not** the aircraft's full historical route (that requires a paid "
          "historical-data feed, out of scope here).",
    "pt": "Os rastros de voo são construídos localmente, nesta sessão, ponto a ponto, a partir dos momentos em "
          "que este dashboard esteve aberto e foi atualizado — **não** são o trajeto histórico completo da "
          "aeronave (isso exigiria um feed histórico pago, fora do escopo aqui).",
},

"demos.inf.expander_label": {
    "en": "🎥 Inference demos (exp1 – exp4)",
    "pt": "🎥 Demos de inferência (exp1 – exp4)",
},

"demos.inf.select_label": {
    "en": "Choose an experiment demo",
    "pt": "Escolha a demo do experimento",
},

"demos.inf.missing": {
    "en": "This demo video is not published yet. Drop the .mp4 in demo/ or add its URL to DEMO_VIDEO_URLS in app.py.",
    "pt": "O vídeo desta demo ainda não foi publicado. Coloque o .mp4 em demo/ ou adicione a URL em DEMO_VIDEO_URLS no app.py.",
},

"demos.inf.caption.exp1": {
    "en": "exp1 (60 epochs, YOLOv8n) — high Precision on the curated benchmark, but detects only ~half the real helipads in the field",
    "pt": "exp1 (60 épocas, YOLOv8n) — alta Precision no benchmark curado, mas detecta só ~metade dos helipontos reais em campo",
},

"demos.inf.caption.exp2": {
    "en": "exp2 (100 epochs, YOLOv8n) — the production model, best field generalization",
    "pt": "exp2 (100 épocas, YOLOv8n) — modelo em produção, melhor generalização em campo",
},

"demos.inf.caption.exp3": {
    "en": "exp3 (100 epochs, YOLOv8n, augmented dataset) — higher recall, mid-pack field result",
    "pt": "exp3 (100 épocas, YOLOv8n, dataset aumentado) — recall mais alto, resultado intermediário em campo",
},

"demos.inf.caption.exp4": {
    "en": "exp4 (100 epochs, YOLO11n) — same base as exp2, newer architecture; did not outperform exp2 in the field",
    "pt": "exp4 (100 épocas, YOLO11n) — mesma base do exp2, arquitetura mais nova; não superou o exp2 em campo",
},

"dl.presentations": {
    "en": "**🎞️ Presentations**",
    "pt": "**🎞️ Apresentações**",
},

"dl.pptx_en_button": {
    "en": "⬇️ Presentation (PPTX, English)",
    "pt": "⬇️ Apresentação (PPTX, inglês)",
},

"dl.pptx_pt_button": {
    "en": "⬇️ Presentation (PPTX, Portuguese)",
    "pt": "⬇️ Apresentação (PPTX, português)",
},

"dl.html_presentation_button": {
    "en": "🌐 Open the interactive HTML presentation",
    "pt": "🌐 Abrir a apresentação interativa em HTML",
},

"globe.entering": {
    "en": "Entering the map…",
    "pt": "Entrando no mapa…",
},

"globe.skip": {
    "en": "Skip ▸",
    "pt": "Pular ▸",
},

"globe.caption.main": {
    "en": "Helipad map",
    "pt": "Mapa de helipontos",
},

"globe.caption.density": {
    "en": "Density view",
    "pt": "Mapa de densidade",
},

"globe.caption.flights": {
    "en": "Live helicopter traffic (beta)",
    "pt": "Tráfego de helicópteros ao vivo (beta)",
},

"map.flights_refresh": {
    "en": "🔄 Refresh live positions",
    "pt": "🔄 Atualizar posições ao vivo",
},

"map.flights_last_update": {
    "en": "Last updated: {time} (auto-refreshes every 30s on interaction)",
    "pt": "Última atualização: {time} (atualiza sozinho a cada 30s, ao interagir com a página)",
},

"map.flights_count": {
    "en": "**{n} aircraft** currently shown (excluding known commercial airlines) — see the disclaimer above "
          "for what \"confirmed\" vs \"unconfirmed\" means.",
    "pt": "**{n} aeronave(s)** exibidas agora (excluindo companhias aéreas conhecidas) — veja o aviso acima "
          "sobre o que significa \"confirmado\" vs. \"não confirmado\".",
},

"map.flights_error": {
    "en": "Could not reach the live flight feed right now ({err}). This layer will retry on the next refresh.",
    "pt": "Não foi possível contatar o feed de voos ao vivo agora ({err}). Esta camada tenta de novo na próxima atualização.",
},

"map.flights_popup": {
    "en": "<b>{callsign}</b> — <i>{confidence}</i><br>Origin: {country}<br>Altitude: {alt}<br>Speed: {speed}<br>Heading: {heading}°",
    "pt": "<b>{callsign}</b> — <i>{confidence}</i><br>Origem: {country}<br>Altitude: {alt}<br>Velocidade: {speed}<br>Rumo: {heading}°",
},

# ---- Map sub-tabs (helipad map vs. live traffic) — added when the live-traffic
# layer was pulled out of the main Folium map into its own view, so a live ADS-B
# feed (unrelated to the YOLO pipeline) never visually blends with the helipad
# detection map. "Beta" in the tab label is a permanent, deliberate signal: this
# view depends on a third-party feed and a best-effort classification heuristic,
# not on this project's own model or dataset.
"map.subtab_helipads": {
    "en": "🗺️ Helipad Map",
    "pt": "🗺️ Mapa de Helipontos",
},

"map.subtab_flights": {
    "en": "🚁 Live Traffic · Beta",
    "pt": "🚁 Tráfego ao Vivo · Beta",
},

"map.flights_notice_short": {
    "en": "Live aircraft positions near São Paulo, from a third-party feed — helicopter identification is best-effort, not guaranteed. Details below.",
    "pt": "Posições de aeronaves ao vivo perto de São Paulo, vindas de um feed de terceiros — a identificação de helicóptero é um melhor esforço, não uma garantia. Detalhes abaixo.",
},

"map.flights_details_title": {
    "en": "ℹ️ How this works, and its limitations (technical details)",
    "pt": "ℹ️ Como isso funciona, e suas limitações (detalhes técnicos)",
},

"map.flights_legend_title": {
    "en": "Legend",
    "pt": "Legenda",
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
"pipeline.flowchart_header": {
    "en": "🗺️ AI/ML Ops Pipeline",
    "pt": "🗺️ Pipeline de AI/ML Ops",
},
"pipeline.diagram_missing_asset": {
    "en": "Diagram image not found at `assets/pipeline_diagram.svg` — the full flowchart is documented in README.md.",
    "pt": "Imagem do diagrama não encontrada em `assets/pipeline_diagram.svg` — o fluxograma completo está documentado no README.md.",
},
"pipeline.steps_header": {
    "en": "📋 Step-by-Step Breakdown",
    "pt": "📋 Detalhamento Passo a Passo",
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
        "- **Scope of a Detection:** A detected helipad is only a visual object-detection result. It must never be stated or implied to be safe, legally certified, operationally active, available for landing, approved for drone delivery, authorized by a building, suitable for package delivery, compliant with aviation regulations, or validated for weather and obstacles. *Automated, image-based visual detection, subject to errors, and not equivalent to operational, legal, safety, or aeronautical validation.*\n"
    ),
    "pt": (
        "- **Propósito e Escopo:** O modelo detecta apenas uma classe de objeto (heliponto) em imagens de satélite de domínio público. Ele não identifica, rastreia nem cria perfis de pessoas.\n"
        "- **Transparência:** Este dashboard apresenta os valores reais de Precision, Recall e mAP do modelo, além de seus principais padrões conhecidos de falsos positivos, como estruturas de telhado, piscinas e quadras esportivas semelhantes à marcação de um heliponto.\n"
        "- **Supervisão Humana:** As detecções servem como apoio à decisão e não substituem a análise humana. Todos os resultados devem ser revisados qualitativamente durante o processo de avaliação.\n"
        "- **Limitações Conhecidas:** O modelo foi treinado com um conjunto relativamente pequeno de dados (aproximadamente 150 imagens anotadas), proveniente de bairros específicos da cidade de São Paulo. Seu desempenho em outras cidades ou estilos arquitetônicos ainda não foi avaliado de forma sistemática.\n"
        "- **Escopo de uma Detecção:** Um heliponto detectado é apenas um resultado visual de detecção de objetos. Nunca deve ser afirmado ou sugerido que ele é seguro, legalmente certificado, operacionalmente ativo, disponível para pouso, aprovado para entrega por drone, autorizado pela edificação, apto para entrega de encomendas, compatível com regulamentação aeronáutica, ou validado quanto a condições climáticas e obstáculos. *Detecção visual automatizada baseada em imagem, sujeita a erros e não equivalente a validação operacional, legal, de segurança ou aeronáutica.*\n"
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

# Contribution Attribution for the Governance tab. Mirrors the "Contribution
# Attribution" section of README.md / README.pt_BR.md (keep the three in sync).
"gov.contributors": {
    "en": "🤝 Project Contributors",
    "pt": "🤝 Colaboradores do Projeto",
},
"gov.contributors.body": {
    "en": (
        "This project evolved from an initial foundation (dataset, first training run and a web "
        "prototype) into an end-to-end computer vision and geospatial intelligence platform. "
        "The two contributors took part at different stages and in different technical areas.\n\n"
        "**Pedro Vyctor Almeida** — established the initial foundation: the original annotated "
        "dataset, the initial web prototype (`Site.py`, a compact Streamlit app with image upload "
        "and regional satellite search) and the first training experiment, `exp1`.\n\n"
        "**Fabiana ⚡️ Campanari** — subsequent development, expansion, integration, evaluation and "
        "consolidation of the final platform:\n\n"
        "*Data & geospatial automation*\n"
        "- development and expansion of the geospatial scraping and geocoding automation (Selenium);\n"
        "- conversion of raw geographic coordinates into decimal coordinates and bounding boxes;\n"
        "- integration of satellite-imagery acquisition and geographic search workflows;\n\n"
        "*Experiments & evaluation*\n"
        "- execution of experiments `exp2`, `exp3` and `exp4` (`exp4` = YOLO11n, same base as `exp2`);\n"
        "- model benchmarking, comparative evaluation and performance analysis (Precision, Recall, "
        "mAP@50, mAP@50–95, training curves, confusion matrices);\n"
        "- comparison of all trained experiments on the same real-world field-validation dataset;\n"
        "- analysis of the gap between curated-benchmark performance and generalization on "
        "uncurated satellite imagery;\n"
        "- field validation across ten São Paulo regions with more than 7,900 real satellite tiles;\n\n"
        "*Dashboard & application*\n"
        "- expansion of the two-tab prototype into a substantially larger bilingual (PT/EN) Streamlit platform;\n"
        "- automatic model discovery and selectable experiment weights;\n"
        "- interactive maps, geographic layers, heatmaps, regional summaries, detection-rate "
        "visualizations and the live helicopter-traffic (beta) view;\n"
        "- the 3D globe → zoom → map intro on the three maps;\n"
        "- sample-image inference, upload inference, regional satellite search and downloadable results;\n"
        "- the inference-demo video selector (`exp1`–`exp4`) and the downloads area with the "
        "PPTX and interactive HTML presentations;\n"
        "- governance, transparency, Responsible AI, LGPD, limitations and human-oversight sections;\n"
        "- complete visual design, interface architecture, layout, styling and user experience;\n"
        "- Docker packaging prepared for future hosting;\n\n"
        "*Repository, documentation & presentation*\n"
        "- organization and consolidation of the complete final repository;\n"
        "- the interactive React/HTML executive presentation (with its 3D globe scene) and the "
        "PPTX versions in English and Portuguese;\n"
        "- the complete bilingual technical reports, guides, documentation, demo videos and supporting materials;\n"
        "- visual storytelling, interactive elements and soundtrack integration;\n"
        "- market research on helicopter presence and activity, including the international "
        "comparative ranking used to contextualize the project's practical relevance.\n\n"
        "Both contributors remain credited for their respective work. See the "
        "**Contribution Attribution** section of `README.md` for the same breakdown."
    ),
    "pt": (
        "Este projeto evoluiu de uma base inicial (dataset, primeiro treinamento e um protótipo "
        "web) para uma plataforma completa de visão computacional e inteligência geoespacial. "
        "Os dois colaboradores participaram em etapas e áreas técnicas diferentes.\n\n"
        "**Pedro Vyctor Almeida** — estabeleceu a base inicial: o dataset original anotado, o "
        "protótipo web inicial (`Site.py`, um app Streamlit compacto com upload de imagem e busca "
        "regional de imagens de satélite) e o primeiro experimento de treinamento, `exp1`.\n\n"
        "**Fabiana ⚡️ Campanari** — desenvolvimento subsequente, expansão, integração, avaliação e "
        "consolidação da plataforma final:\n\n"
        "*Dados e automação geoespacial*\n"
        "- desenvolvimento e expansão da automação de scraping e geocodificação geoespacial (Selenium);\n"
        "- conversão de coordenadas geográficas brutas em coordenadas decimais e bounding boxes;\n"
        "- integração dos fluxos de aquisição de imagens de satélite e de busca geográfica;\n\n"
        "*Experimentos e avaliação*\n"
        "- execução dos experimentos `exp2`, `exp3` e `exp4` (`exp4` = YOLO11n, mesma base do `exp2`);\n"
        "- benchmarking dos modelos, avaliação comparativa e análise de desempenho (Precision, "
        "Recall, mAP@50, mAP@50–95, curvas de treinamento, matrizes de confusão);\n"
        "- comparação de todos os experimentos treinados no mesmo dataset de validação em campo;\n"
        "- análise da diferença entre o desempenho no benchmark curado e a generalização em "
        "imagens de satélite não curadas;\n"
        "- validação em campo em dez regiões de São Paulo com mais de 7.900 tiles reais de satélite;\n\n"
        "*Dashboard e aplicação*\n"
        "- expansão do protótipo de duas abas para uma plataforma Streamlit bilíngue (PT/EN) substancialmente maior;\n"
        "- descoberta automática de modelos e seleção dos pesos de cada experimento;\n"
        "- mapas interativos, camadas geográficas, mapas de calor, resumos regionais, visualizações "
        "de taxa de detecção e a visão de tráfego de helicópteros ao vivo (beta);\n"
        "- a intro globo → zoom → mapa nos três mapas;\n"
        "- inferência em imagens de exemplo, inferência por upload, busca regional por satélite e resultados para download;\n"
        "- o seletor de vídeos de demo de inferência (`exp1`–`exp4`) e a área de downloads com as "
        "apresentações em PPTX e em HTML interativo;\n"
        "- seções de governança, transparência, IA Responsável, LGPD, limitações e supervisão humana;\n"
        "- design visual completo, arquitetura de interface, layout, estilo e experiência do usuário;\n"
        "- empacotamento em Docker preparado para hospedagem futura;\n\n"
        "*Repositório, documentação e apresentação*\n"
        "- organização e consolidação do repositório final completo;\n"
        "- a apresentação executiva interativa em React/HTML (com sua cena de globo 3D) e as "
        "versões em PPTX em inglês e português;\n"
        "- os relatórios técnicos, guias, documentação, vídeos de demonstração e materiais de apoio bilíngues completos;\n"
        "- storytelling visual, elementos interativos e integração da trilha sonora;\n"
        "- pesquisa de mercado sobre presença e atividade de helicópteros, incluindo o ranking "
        "comparativo internacional usado para contextualizar a relevância prática do projeto.\n\n"
        "Os dois colaboradores continuam creditados por suas respectivas contribuições. Veja a "
        "seção **Contribution Attribution** do `README.md` para o mesmo detalhamento."
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
"about.collaborators": {"en": "Collaborator", "pt": "Colaborador"},

# Demo videos. Split across two locations, each next to its relevant
# content: the scraping-bot demo sits in About (right below the credits),
# and the training-run demo sits in Experiment Metrics (right below the
# Confusion Matrix). No dashboard-demo video is embedded anywhere in the
# app itself — the running app *is* that demo; that video only appears in
# README.md / the presentation, where a live app isn't available.
"about.demos.muted_notice": {
    "en": "🔇 Starts muted — click the speaker icon on the player to enable audio.",
    "pt": "🔇 Começa mudo — clique no ícone de som do player para ativar o áudio.",
},
"about.demos.scraping.expander_label": {
    "en": "🎥 Demo — Automated Helipad Scraping",
    "pt": "🎥 Demo — Coleta Automatizada de Helipontos",
},
"about.credits.expander_label": {
    "en": "🎓 Institutional Credits",
    "pt": "🎓 Créditos Institucionais",
},
"about.demos.scraping.title_line": {
    "en": '🎥 <strong>DEMO:</strong> <strong>AUTOMATED HELIPAD SCRAPING</strong> ✦ <code>SELENIUM</code> ✦ <code>FLIGHTMARKET</code> ✦ <code>GEOCODING</code>',
    "pt": '🎥 <strong>DEMO:</strong> <strong>AUTOMATED HELIPAD SCRAPING</strong> ✦ <code>SELENIUM</code> ✦ <code>FLIGHTMARKET</code> ✦ <code>GEOCODING</code>',
},
"about.demos.scraping.credit_line": {
    "en": '🎼 <strong><em>Interstellar</em></strong> ✧ <strong><em>Hans Zimmer</em></strong> ✧ <em>Deep House Version</em> · Code · Sound · Creative Design · <strong><em>Fab</em></strong> ⚡️ <strong>𝄢 𝄫</strong>',
    "pt": '🎼 <strong><em>Interstellar</em></strong> ✧ <strong><em>Hans Zimmer</em></strong> ✧ <em>Deep House Version</em> · Código · Som · Direção Criativa · <strong><em>Fab</em></strong> ⚡️ <strong>𝄢 𝄫</strong>',
},
"about.demos.training.expander_label": {
    "en": "🎥 Demo — Model Training",
    "pt": "🎥 Demo — Treinamento do Modelo",
},
"about.demos.training.title_line": {
    "en": '🎥 <strong>DEMO:</strong> <strong>HELIPAD DETECTION</strong> ✧ <code>YOLO11</code> ✧ <code>MODEL TRAINING</code>',
    "pt": '🎥 <strong>DEMO:</strong> <strong>HELIPAD DETECTION</strong> ✧ <code>YOLO11</code> ✧ <code>MODEL TRAINING</code>',
},
"about.demos.training.credit_line": {
    "en": '🎶 <strong><em>Feel Good</em></strong> ✦ <strong><em>Nina Simone</em></strong> ✦ <em>Deep House Version</em> · Concept · Creative Design · <strong><em>Fab</em></strong> ⚡️ <strong>𝄢 𝄫</strong>',
    "pt": '🎶 <strong><em>Feel Good</em></strong> ✦ <strong><em>Nina Simone</em></strong> ✦ <em>Deep House Version</em> · Conceito · Direção Criativa · <strong><em>Fab</em></strong> ⚡️ <strong>𝄢 𝄫</strong>',
},

    
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
        "en": "**{exp}** scored higher than exp1 on mAP@50-95 ({delta}).",
        "pt": "**{exp}** teve resultado superior ao exp1 em mAP@50-95 ({delta}).",
    },
    "metrics.underperformed": {
        "en": "**{exp}** scored lower than exp1 on mAP@50-95 ({delta}).",
        "pt": "**{exp}** teve resultado inferior ao exp1 em mAP@50-95 ({delta}).",
    },
    "metrics.tied": {
        "en": "**{exp}** is essentially tied with exp1 (Δ {delta}).",
        "pt": "**{exp}** está essencialmente empatado com o exp1 (Δ {delta}).",
    },
    "metrics.not_controlled": {
        "en": "These experiments are not a controlled comparison: author, environment, Ultralytics version "
              "(exp1 8.4.75, exp2 8.4.98, exp3 8.4.98, exp4 8.4.163) and dataset version differ between runs. "
              "Small differences on a 226-image dataset are within expected noise and should not be attributed "
              "to a single factor such as the number of epochs.",
        "pt": "Estes experimentos não formam uma comparação controlada: autor, ambiente, versão do Ultralytics "
              "(exp1 8.4.75, exp2 8.4.98, exp3 8.4.98, exp4 8.4.163) e versão do dataset diferem entre as execuções. "
              "Diferenças pequenas em um dataset de 226 imagens estão dentro do ruído esperado e não devem ser "
              "atribuídas a um único fator, como o número de épocas.",
    },
    "lineage.expander": {"en": "Data lineage & limitations", "pt": "Linhagem dos dados e limitações"},
    "metrics.band.vs_exp1": {"en": "{exp} vs. exp1", "pt": "{exp} vs. exp1"},
    "metrics.band.caution": {"en": "Read with caution", "pt": "Leia com cautela"},
    "lineage.body": {
        "en": "- **Annotated dataset (version 2):** 226 images — 178 train / 34 validation / 14 test. Version 2 has no data augmentation; only the exp3 fork does.\n"
              "- **Labels:** mostly polygons (170 of 178 training label files and all validation/test files), converted to boxes for detection training. Three training label files mix polygons and boxes and are flagged by Ultralytics 8.4.163.\n"
              "- **Field run:** 7,943 tiles in the production run (10 neighborhoods); the comparison set has 7,767 region × tile pairs and 5,540 distinct tiles.\n"
              "- **Overlap:** 125 of the 225 annotated images with coordinates are copies of field tiles (2.3% of the 5,540 distinct tiles), so the field run is not fully independent of the annotated set. See [reports/lineage_audit/](https://github.com/Mindful-AI-Research/3-project-ai-ml-yolo-helipad_detector/blob/main/reports/lineage_audit/README.md).\n"
              "- **Detection rate is not precision or recall:** field detection rates have no ground-truth labels behind them.",
        "pt": "- **Dataset anotado (versão 2):** 226 imagens — 178 treino / 34 validação / 14 teste. A versão 2 não tem aumento de dados; só o fork do exp3 tem.\n"
              "- **Rótulos:** majoritariamente polígonos (170 dos 178 arquivos de treino e todos os de validação e teste), convertidos em caixas no treino de detecção. Três arquivos de rótulo do treino misturam polígono e caixa e são sinalizados pelo Ultralytics 8.4.163.\n"
              "- **Execução de campo:** 7.943 tiles na execução de produção (10 bairros); o conjunto de comparação tem 7.767 pares região × tile e 5.540 tiles distintos.\n"
              "- **Sobreposição:** 125 das 225 imagens anotadas com coordenadas são cópias de tiles de campo (2,3% dos 5.540 tiles distintos); portanto, a execução de campo não é totalmente independente do conjunto anotado. Ver [reports/lineage_audit/](https://github.com/Mindful-AI-Research/3-project-ai-ml-yolo-helipad_detector/blob/main/reports/lineage_audit/README.md).\n"
              "- **Taxa de detecção não é precisão nem recall:** as taxas de campo não têm rótulos de referência por trás.",
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
        "en": "🔬 Compare all {n} models on the same field validation",
        "pt": "🔬 Comparar os {n} modelos na mesma validação de campo",
    },
    "field.compare.table_title": {
        "en": "#### Detection Rate by Region and Experiment",
        "pt": "#### Taxa de Detecção por Região e Experimento",
    },
    "field.compare.body": {
        "en": "The same {tiles} tiles across the same 10 regions, run separately with each "
              "experiment's weights — shows whether the model that scored best on the curated "
              "validation set actually generalizes as well once it meets real, uncurated satellite "
              "coverage. (exp2 here uses a re-run on this exact tile set, not its original "
              "production run — see the Downloads tab for that number.)",
        "pt": "Os mesmos {tiles} tiles nas mesmas 10 regiões, rodados separadamente com os pesos de "
              "cada experimento — mostra se o modelo que teve a melhor nota no conjunto de "
              "validação curado realmente generaliza bem quando enfrenta cobertura de satélite "
              "real, sem curadoria prévia. (o exp2 aqui usa uma nova execução sobre esse mesmo "
              "conjunto de tiles, não a execução original de produção — veja a aba Downloads para "
              "esse número.)",
    },
    "field.compare.reality_check": {
        "en": "exp1 leads the curated validation set on Precision (1.000) — but across identical "
              "field conditions, it detects roughly half as many real helipads as exp2 (9.6% vs. "
              "21.0%) and noticeably fewer than exp3 (17.9%). A model that looks best on a small, "
              "curated benchmark is not automatically the model that generalizes best in "
              "unfiltered, real-world coverage — exactly the kind of gap field validation exists "
              "to catch.",
        "pt": "O exp1 lidera o conjunto de validação curado em Precision (1.000) — mas, nas mesmas "
              "condições de campo, detecta cerca de metade dos helipontos reais que o exp2 (9,6% "
              "vs. 21,0%) e sensivelmente menos que o exp3 (17,9%). Um modelo que parece melhor num "
              "benchmark pequeno e curado não é automaticamente o que generaliza melhor em "
              "cobertura real, sem filtragem — exatamente o tipo de lacuna que a validação de "
              "campo existe para capturar.",
    },
    "field.compare.reality_check_exp4": {
        "en": "On the curated benchmark, exp4 (YOLO11n) was roughly tied with exp3. In the field, "
              "exp4 does slightly better than exp3 ({exp4:.1%} vs. {exp3:.1%}) — but both stay "
              "well behind exp2 ({exp2:.1%}).",
        "pt": "No benchmark curado, o exp4 (YOLO11n) ficou praticamente empatado com o exp3. Em "
              "campo, o exp4 fica um pouco melhor que o exp3 ({exp4:.1%} vs. {exp3:.1%}) — mas os "
              "dois ficam bem atrás do exp2 ({exp2:.1%}).",
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
