<br>

**[[🇧🇷 Português](README.pt_BR.md)] [**[🇺🇸 English](README.md)**]**

<br><br>



#  <p align="center"> 3- 🧠 [AI /ML - Project 2]() /  [Computer Vision]() - [Helipoint Detector]()

### <p align="center"> Automated Helipad Detection Using YOLO and Satellite Imagery of São Paulo, Brazil

</p>

<br>

<div align="center">

<a href="https://github.com/topics/satellite-imagery">Satellite Imagery</a> &nbsp;&nbsp;✦&nbsp;&nbsp;
<a href="https://github.com/topics/data-visualization">Urban Analytics</a> &nbsp;&nbsp;✦&nbsp;&nbsp;
<a href="https://github.com/topics/object-detection">Object Detection</a> &nbsp;&nbsp;✦&nbsp;&nbsp;
<a href="https://github.com/topics/yolo">YOLOv8 / YOLOv11</a> &nbsp;&nbsp;✦&nbsp;&nbsp;
<a href="https://github.com/topics/geospatial">Geospatial Intelligence</a>

</div>

<br>


#

#### <p align="center"> ✨ ***From Pixels to Geospatial Intelligence*** ✨


<!--
#### <p align="center"> Teaching YOLO to say: ***“Yup  !!! that's definitely an H !!*** 
##### <p align="center"> ***Finding Hidden H's in the Concrete Jungle...*** ⚡️ One Rooftop at a Time.
-->

<br><br>

<br><br>
<!-- ========= END REPO TITLE ========= -->

<!-- ========= START APP BADGE ========= -->
<p align="center" style="margin: 0;">
  <a href="https://github.com/Mindful-AI-Assistants/Helipoint-Detector" rel="noopener noreferrer">
    <img 
      src="https://img.shields.io/badge/GitHub%20Repository-Helipoint%20Detector-0f172a?style=for-the-badge&logo=github&logoColor=white" 
      alt="GitHub Repository Helipoint Detector"
      style="height: 38px; width: auto;"
    />
  </a>
</p>

<!-- ========= END APP BADGE ========= -->


<!-- ========= START NOTEBOOK BADGE ========= -->
<p align="center" style="margin: 0;">

  <a href="https://github.com/Mindful-AI-Assistants/Helipoint-Detector/blob/main/Analise.ipynb" rel="noopener noreferrer">
    <img 
      src="https://img.shields.io/badge/Jupyter-Training%20%26%20Evaluation%20Notebook-0f766e?style=for-the-badge&logo=jupyter&logoColor=white" 
      alt="Jupyter Training and Evaluation Notebook"
      style="height: 32px; width: auto; margin-right: 8px;"
    />
  </a>
  
<!-- =========End NOTEBOOK BADGE ========= -->

<!-- ========= START APP BADGE ========= -->
  <a href="https://github.com/Mindful-AI-Assistants/Helipoint-Detector/blob/main/Site.py" target="_blank" rel="noopener noreferrer">
    <img 
      src="https://img.shields.io/badge/Streamlit-Helipad%20Detection%20Interface-134e4a?style=for-the-badge&logo=streamlit&logoColor=white&labelColor=022c22" 
      alt="Streamlit Helipad Detection Interface"
      style="height: 32px; width: auto;"
    />
  </a>

</p>

<br><br>

#

<br><br>
<!-- ========= END APP BADGE ========= -->

<!-- ======================================= Start Institutional INFO ===========================================  -->
[**Institution:**]() Pontifical Catholic University of São Paulo (PUC-SP) • Humanistic AI & Data Science • 2026 <br>
[**School:**]() Faculty of Interdisciplinary Studies  <br>
[**Course Repo:**]() Integrated Project — Machine Learning  <br>
**Project:**  P2 — Object Detection in Satellite Images with YOLO  <br>
**Professor:**  [✨ Rooney Ribeiro Albuquerque Coelho](https://www.linkedin.com/in/rooney-coelho-320857182/)  <br>
**Authors:**  [Fabiana ⚡️ Campanari](https://linktr.ee/fabianacampanari) and Pedro Vyctor Almeida  <br>  <br>

<br><br>
<!-- ========= END Institutional INFO ========= -->








## [MLOps Pipeline Architecture]()

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

    A["FlightMarket / aviation website"] --> B["Selenium automation<br/>BOTHELIPONTO.py"]
    B --> C["Helipad records + metadata"]
    C --> D["Coordinates CSV<br/>cordenadasheli.csv"]
    D --> E["Coordinate conversion<br/>Transformarcordenadas.py"]
    E --> F["Geographic bounding boxes"]
    F --> G["ESRI World Imagery<br/>XYZ tile download"]
    G --> H["Image mosaics by region<br/>Imagens.ipynb"]
    H --> I["Manual visual triage"]
    I --> J["Selected images with helipads"]
    J --> K["Roboflow upload"]
    K --> L["Bounding box annotation<br/>single class: helipad"]
    L --> M["Preprocessing + augmentations<br/>resize 640x640"]
    M --> N["Dataset split<br/>train / valid / test"]
    N --> O["YOLO export<br/>data.yaml + labels"]
    O --> P["Google Colab training<br/>Ultralytics YOLOv8 / YOLOv11"]
    P --> Q["Runs, weights and metrics<br/>runs/detect/.../best.pt"]
    Q --> R["Quantitative evaluation<br/>mAP, Precision, Recall, confusion matrix"]
    Q --> S["Qualitative analysis<br/>hits, false positives, false negatives"]
    Q --> T["Inference on unseen neighborhood<br/>New Images/"]
    T --> U["Generalization assessment"]
    Q --> V["Optional web app<br/>Site.py"]

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
