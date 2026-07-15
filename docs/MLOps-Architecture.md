## [Adjusted Mermaid Pipeline]()

```mermaid
%%{
  init: {
    "theme": "dark",
    "themeVariables": {
      "background": "#0b1220",
      "primaryColor": "#000000",
      "primaryTextColor": "#ffffff",
      "primaryBorderColor": "#000000",
      "lineColor": "#14b8a6",
      "secondaryColor": "#000000",
      "secondaryTextColor": "#ffffff",
      "secondaryBorderColor": "#000000",
      "tertiaryColor": "#000000",
      "tertiaryTextColor": "#ffffff",
      "tertiaryBorderColor": "#000000",
      "mainBkg": "#000000",
      "nodeBorder": "#000000",
      "clusterBkg": "#020617",
      "clusterBorder": "#000000",
      "titleColor": "#ffffff",
      "edgeLabelBackground": "#0b1220",
      "fontFamily": "Inter, Segoe UI, Arial, sans-serif"
    }
  }
}%%

flowchart TD

    A["FlightMarket / aviation website"] --> B["Selenium automation<br/>src/geospatial/helipad_bot.py"]
    B --> C["Helipad records + metadata"]
    C --> D["Coordinates CSV<br/>src/geospatial/helipad_coordinates.csv"]
    D --> E["Coordinate conversion<br/>src/geospatial/transform_coordinates.py"]
    E --> F["Geographic bounding boxes"]
    F --> G["ESRI World Imagery<br/>XYZ tile download"]
    G --> H["Image mosaics by region<br/>src/geospatial/geospatial_image_collection.ipynb"]
    H --> I["Manual visual triage"]
    I --> J["Selected images with helipads"]
    J --> K["Roboflow upload"]
    K --> L["Bounding box annotation<br/>single class: helipad"]
    L --> M["Preprocessing + augmentations<br/>resize 640x640"]
    M --> N["Dataset split<br/>train / valid / test"]
    N --> O["YOLO export<br/>configs/data.yaml + data/training/yolo_dataset/"]
    O --> P["Google Colab training<br/>Ultralytics YOLOv8 / YOLOv11 via src/training/yolo_training.ipynb"]
    P --> Q["Runs, weights and metrics<br/>artifacts/runs/runs/detect/.../weights/best.pt"]
    Q --> R["Quantitative evaluation<br/>mAP, Precision, Recall, confusion matrix"]
    Q --> S["Qualitative analysis<br/>analysis_yolo_results/Analysis.ipynb + analysis_yolo_results/Analysis_yolo_results.md"]
    Q --> T["Inference on unseen neighborhood<br/>data/tiles/ or another holdout folder"]
    T --> U["Generalization assessment"]
    Q --> V["Optional web app<br/>apps/streamlit_app/app.py"]

    subgraph G1["Geospatial Discovery"]
      A
      B
      C
      D
      E
      F
    end

    subgraph G2["Visual Acquisition"]
      G
      H
      I
      J
    end

    subgraph G3["Dataset Engineering"]
      K
      L
      M
      N
      O
    end

    subgraph G4["Modeling and Validation"]
      P
      Q
      R
      S
      T
      U
      V
    end
```

## [Updated Repository Tree]()

```text
.
├── README.md
├── README.pt-BR.md
├── .devcontainer/
│   └── devcontainer.json
├── analysis_yolo_results/
│   ├── Analysis.ipynb
│   └── Analysis_yolo_results.md
├── apps/
│   └── streamlit_app/
│       └── app.py
├── artifacts/
│   └── runs/
│       ├── runs/
│       └── runs_zipped.zip
├── briefing/
│   ├── 3315-264/
│   ├── briefing_assets/
│   └── notebooks/
├── configs/
│   └── data.yaml
├── data/
│   ├── raw/
│   ├── tiles/
│   └── training/
├── docs/
│   ├── MLOps-Architecture.md
│   └── governance/
├── notebooks/
│   └── model_analysis.ipynb
├── reports/
│   ├── executive_analysis/
│   ├── model_outputs/
│   └── yolo_results_analysis.md
├── src/
│   ├── data_preparation/
│   ├── geospatial/
│   └── training/
├── requirements.txt
└── packages.txt
```
