
<!--START  🇧🇷Portuguese LANGUAGE BUTTON  -->
\[**[🇧🇷 Português](README.pt_BR.md)**\] \[[🇬🇧 English](README.md)\]
<!--END 🇧🇷 Portuguese LANGUAGE BUTTON  -->


<br><br>



<!-- ========= START HEADRE ========= -->
# <p align="center"> 🚁  [Helipad Detector]()

### <p align="center"> Plataforma de Inteligência Artificial End-to-End para Detecção Automatizada de Helipontos e Inteligência Geoespacial a partir de Imagens de Satélite

<br>

<div align="center">

<a href="https://github.com/topics/satellite-imagery">Imagens de Satélite</a>
  ✦   <a href="https://github.com/topics/data-visualization">Análise Urbana</a>
  ✦   <a href="https://github.com/topics/object-detection">Detecção de Objetos</a>
  ✦   <a href="https://github.com/topics/yolo">YOLO (v8 / v11)</a>
  ✦   <a href="https://github.com/topics/geospatial">Inteligência Geoespacial</a>

</div>

<br><br>

<!-- ========= START TEASER ========= -->
###### <p align="center"> <i>Teaching YOLO to spot the city's most exclusive landing spots.</i> ✨</p> 

###### <p align="center"> 🚁 ***Finding hidden H’s in the concrete jungle*** <br>

###### <p align="center">One rooftop at a time. <br> 

#### <p align="center"> ⚡️


<br>

#

<br><br>
<!-- ========= END TEASER ========= -->


<!-- ========= START SPONSOR BADGE ========= -->
<p align="center">

  <a href="https://github.com/sponsors/Mindful-AI-Research">
    <img
      src="https://img.shields.io/badge/Sponsor-%E0%A5%90%20%E2%8B%86%20Mindful%20AI%20%E2%8B%86%20Research%20%26%20Consulting%20%F0%96%A4%90%20%E2%8B%86-3A424C?style=for-the-badge&logo=githubsponsors&logoColor=white&labelColor=07111F"
      alt="Sponsor ॐ ⋆ Mindful AI ⋆ Research & Consulting 𖤐 ⋆"
      height="36"
    >
  </a>

  
<br><br>
<!-- ========= END SPONSOR BADGE ========= -->


<!-- ========= START PUC GIF ========= -->
<p align="center">
   <img src="https://github.com/user-attachments/assets/791a69e2-d09a-429f-9257-f6667fff5c04 ">
 </p>

 <br>
<!-- ========= END PUC GIF ========= -->


<!-- ========= START 🇧🇷 Top CommtributorsE ========= 
<p align="center">
  <a href="https://user-badge.committers.top/brazil/FabianaCampanari">
    <img
      src="https://img.shields.io/badge/%F0%9F%87%A7%F0%9F%87%B7%20TOP%20CONTRIBUTORS-07111F?style=for-the-badge&labelColor=07111F&logoColor=white"
      alt="🇧🇷 TOP CONTRIBUTORS"
      height="36"
    >
    <img
      src="https://img.shields.io/badge/·····%20BRAZIL-3A424C?style=for-the-badge&labelColor=3A424C&logoColor=white"
      alt="Brazil"
      height="36"
    >
  </a>
</p>

</p>

<br><br><br>
========= END 🇧🇷 Top CommtributorsE  ========= -->


<!-- ========= START Institutional INFO ========= -->
[**Instituição:**]() Pontifícia Universidade Católica de São Paulo (PUC-SP) <br>
[**Escola:**]() FACEI — Departamento de Ciência da Computação <br>
[**Curso:**]() Bacharelado em Human-Centered AI & Data Science  <br>
[**Disciplina:**]() Machine Learning / Visão Computacional — YOLO <br>
[**Projeto:**]() Detecção de Objetos em Imagens de Satélite com YOLO <br>
**Autora:** [Fabiana ⚡️ Campanari](https://linktr.ee/fabianacampanari) <br>
**Colaboradores:** [Carlos Antonio dos Santos Roth Gorham]() · [Pedro Vyctor Almeida](https://github.com/ppvyctor/Helipoint-Detector) 

# <br>
<!-- ========= END Institutional INFO ========= -->


<!-- ======================================= Start Institutional  Atribuição de Contribuições / subm tidd ======== -->
### [Atribuição de Contribuições]()

Este projeto evoluiu de uma base inicial envolvendo desenvolvimento de dataset, treinamento de modelos e um protótipo web para uma plataforma integrada de visão computacional e inteligência geoespacial. Os três colaboradores creditados participaram em diferentes etapas do projeto, com contribuições abrangendo distintas áreas técnicas e responsabilidades. <br><br>

* [Pedro Vyctor Almeida](https://github.com/ppvyctor/Helipoint-Detector) estabeleceu a base inicial do projeto, incluindo o dataset originalmente anotado, o protótipo inicial da aplicação web (`Site.py`) e o primeiro experimento de treinamento (`exp1`). Seu protótipo consistia em uma aplicação compacta em Streamlit, com duas funções principais: upload de imagens e busca de imagens de satélite por região. O trabalho original está documentado em seu [repositório Helipoint Detector](https://github.com/ppvyctor/Helipoint-Detector). <br><br>

* [**Carlos Antonio dos Santos Roth Gorham**]() propôs o conceito de automação geoespacial para a descoberta de helipontos e contribuiu para o início dessa direção de implementação. <br><br>

* [Fabiana ⚡️ Campanari](https://linktr.ee/fabianacampanari) contribuiu para o desenvolvimento, expansão, integração, avaliação e consolidação subsequentes da plataforma final **Helipad Detector**. Seu trabalho incluiu: <br><br>

  * desenvolvimento e expansão da automação de scraping geoespacial e geocodificação;
  * conversão de coordenadas geográficas brutas para coordenadas decimais e bounding boxes;
  * integração da aquisição de imagens de satélite e dos fluxos de busca geográfica;
  * execução dos experimentos `exp2` e `exp3`;
  * benchmarking dos modelos, avaliação comparativa e análise de desempenho;
  * comparação dos modelos treinados utilizando Precision, Recall, mAP@50, mAP@50–95, curvas de treinamento e matrizes de confusão;
  * avaliação comparativa dos três experimentos utilizando o mesmo dataset de validação em condições reais de campo;
  * análise da diferença entre o desempenho em benchmarks com dados curados e a generalização em imagens de satélite não curadas;
  * validação em campo em dez regiões de São Paulo, utilizando mais de 7.900 tiles de imagens de satélite reais;
  * expansão do protótipo inicial de duas abas para uma plataforma Streamlit bilíngue substancialmente mais ampla;
  * implementação de descoberta automática de modelos e seleção dos pesos dos experimentos;
  * desenvolvimento de mapas interativos, camadas geográficas, heatmaps, resumos regionais e visualizações das taxas de detecção;
  * implementação de inferência com imagens de amostra, inferência por upload, busca regional de imagens de satélite e resultados de detecção para download;
  * desenvolvimento das seções de governança, transparência, Responsible AI, LGPD, limitações e supervisão humana;
  * implementação do suporte à interface bilíngue PT/EN;
  * desenvolvimento completo do design visual, arquitetura da interface, layout, estilização, design de interação e experiência do usuário do dashboard;
  * organização e consolidação do repositório final completo;
  * criação da apresentação executiva interativa em React/HTML;
  * preparação dos relatórios técnicos bilíngues completos, guias, documentação, demonstrações e materiais de apoio;
  * desenvolvimento da camada de apresentação do projeto, narrativa visual, elementos interativos e integração da trilha sonora;
  * pesquisa de mercado e análise comparativa de indicadores de presença e atividade de helicópteros, incluindo o ranking comparativo internacional utilizado para contextualizar a relevância prática do projeto. <br><br>

O repositório final representa a evolução do projeto a partir de seu protótipo inicial para uma plataforma integrada de visão computacional e inteligência geoespacial, abrangendo descoberta de dados, automação geoespacial, experimentação, benchmarking de modelos, avaliação comparativa, validação em campo, visualização, governança, documentação, apresentação e pesquisa contextual aplicada.

**Os três colaboradores permanecem creditados por suas respectivas contribuições. Esta atribuição tem como objetivo documentar de forma transparente o histórico de desenvolvimento do projeto, a evolução de sua implementação e as áreas técnicas para as quais cada participante contribuiu.**


<br>

#

<br><br><br>
<!-- ======================================= END Institutional / mestr/ SUBMISSION =========================================== --> 


<!-- ========= START Streamlit BADGE ========= -->
<p align="center" style="margin: 0;">
  <a href="https://helipad-detector-sp.streamlit.app/" rel="noopener noreferrer">
    <img 
      src="https://img.shields.io/badge/Streamlit%20Repository-Helipad%20Detector-0f172a?style=for-the-badge&logo=streamlit&logoColor=white" 
      alt="Streamlit Repository Helipad Detector"
      style="height: 38px; width: auto;"
    />
  </a>
</p>
<!-- ========= END Streamlit BADGE ========= -->


<!-- ========= START React Presentation BADGE ========= -->
<p align="center" style="margin: 0;">

  <a href="https://mellow-salamander-f81315.netlify.app/" target="_blank" rel="noopener noreferrer">
    <img
      src="https://img.shields.io/badge/React%20Presentation-Slides%20and%20Overview-0f766e?style=for-the-badge&logo=react&logoColor=white"
      alt="React Presentation Slides and Overview"
      style="height: 32px; width: auto; margin-right: 8px;"
    />
  </a> 
<!-- =========End REeact Presentation BADGE ========= -->

<!-- ========= START Helipad Detector Relatório Completo. BADGE ========= -->
 <a href="https://github.com/Mindful-AI-Research/3-project-ai-ml-yolo-helipad_detector/blob/34e0c885443ab622df84a65a666995ee8ef118b1/reports/helipad_detector_full_report/%F0%9F%87%A7%F0%9F%87%B7Helipad_Detector_Relatorio_Completo.pdf" target="_blank" rel="noopener noreferrer">
    <img 
      src="https://img.shields.io/badge/Helipad%20Detector-Relat%C3%B3rio%20Completo-134e4a?style=for-the-badge&logo=github&logoColor=white&labelColor=022c22" 
      alt="Helipad Detector — Relatório Completo"
      style="height: 32px; width: auto;"
    />
  </a>

</p>
<!-- ========= END Helipad Detector Relatório Completo. BADGE ========= -->

<br><br>

#

<br><br>
<!-- =========  BADGES END Helipad Detector -------  ALL  PORESENBTATIONS  BADGES     ========= -->

<!-- 🚧<!-- ========= START 🎥 **DEMO** ========= 
### 🎥 **DEMO: RESTful API & Dashboard Deployment** ✧ ` * Geocoding: Nominatim (OpenStreetMap)` ✧ ` MapLibre GL JS` ✧ `Streamlit`

## Dashboard Preview

###### <p align="center"> 🎬 **Creative Direction, Music Curation & Editing by Fab⚡️**
###### <p align="center"> 🎶 **Soundtrack:** *"Canon in D"* — Johann Pachelbel

<br>

#

<br><br>
=========🚧 END 🎥 **DEMO** =========  -->



<!-- ========= START TECH STACK / PIPELINE BADGES ========= -->
<p align="center">
  <img src="https://img.shields.io/badge/Python-Core%20Language-0f172a?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PyTorch-Deep%20Learning%20Framework-101f2f?style=for-the-badge&logo=pytorch&logoColor=white" />
  <img src="https://img.shields.io/badge/YOLO-Ultralytics%20Object%20Detection-112a3a?style=for-the-badge&logo=ultralytics&logoColor=white" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Roboflow-Dataset%20%26%20Annotation-134a4a?style=for-the-badge&logo=roboflow&logoColor=white" />
  <img src="https://img.shields.io/badge/Geospatial-Satellite%20Imagery-124050?style=for-the-badge&logo=googleearth&logoColor=white" />
  <img src="https://img.shields.io/badge/Computer%20Vision-Object%20Detection-0f2a2a?style=for-the-badge&logo=opencv&logoColor=white" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Google%20Colab-GPU%20Training-134e4a?style=for-the-badge&logo=googlecolab&logoColor=white" />
  <img src="https://img.shields.io/badge/Evaluation-mAP%20%2F%20Precision%20Metrics-0f172a?style=for-the-badge&logo=githubactions&logoColor=white" />
</p>


<br><br>

#

<br><br>
<!-- =========END TECH STACK / PIPELINE BADGES========= -->


<!-- ========= START NOTE ========= -->
> [!WARNING]
>
> ⚠️ Os projetos podem ser compartilhados publicamente quando permitido.  
> O foco está no aprendizado aplicado e prático, utilizando datasets reais em contextos de governança e segurança de IA.  
> Todo conteúdo sensível permanece protegido em repositórios privados quando necessário.
>

<br><br>

#

<br><br>
<!-- ========= END NOTE ========= -->

<!-- =========START MAIN REPO =Projects REFERENCES ========= -->
> [!TIP]
>
> Este repositório faz parte do ecossistema principal:
>
> ## 🧠 IA/ML ✦ Redes Neurais ✦ Hub ✦
>
> Explore a coleção completa de projetos, notebooks, materiais de pesquisa, análises e aplicações interativas disponível no repositório central:
>
> 🔗 **[IA/ML ✦ Redes Neurais ✦ Hub](https://github.com/Mindful-AI-Research/1-ai-ml_neural-networks_hub)**
>
> #
>
> ### Projeto Relacionado nesta Série:
>
> 🔗 **[Projeto IA/ML 1 · Visão Computacional · EMNIST Vision Intelligence](https://github.com/Mindful-AI-Assistants/2-project-ai-ml-emnist-vision-intelligence)**
>
> Um sistema de deep learning para reconhecimento de caracteres manuscritos utilizando PyTorch e Streamlit.
>
>
<br><br><br><br>
<!-- =========END MAIN REPO =Projects REFERENCES ========= -->


<!-- ========= START Overview ========= -->
## [Visão Geral]()

[**Helipad Detector**]() é uma plataforma de Inteligência Artificial e Visão Computacional de ponta a ponta, desenvolvida para detectar e mapear automaticamente helipontos em coberturas de edifícios a partir de imagens de satélite. O projeto concentra-se em São Paulo, Brasil, um ambiente urbano singular, reconhecido por possuir uma das maiores frotas de helicópteros do mundo, com aproximadamente **2.200 pousos e decolagens por dia** e picos operacionais que chegam a **um movimento a cada 45 segundos**. A cidade também conta com o [**HELICONTROL**](), um sistema dedicado de controle de tráfego aéreo de helicópteros, desenvolvido para gerenciar esse ambiente excepcionalmente denso de mobilidade aérea urbana.

Essas características tornam São Paulo um cenário real particularmente relevante para aplicações de inteligência geoespacial baseada em IA. Ao transformar imagens de satélite em informações espaciais estruturadas, o projeto demonstra como a Visão Computacional pode apoiar o mapeamento automatizado de infraestrutura, a análise urbana e a tomada de decisões orientada por dados em futuras aplicações de Smart Cities.

A plataforma implementa um fluxo completo de IA de ponta a ponta, incluindo coleta de dados públicos, geocodificação, aquisição de imagens de satélite, anotação manual com Roboflow, treinamento de modelos YOLOv8n / YOLO11n e validação em condições reais em mais de **7.900 tiles de satélite**. Seu dashboard interativo oferece acesso transparente ao pipeline, aos datasets, ao desempenho dos modelos e às limitações documentadas, reforçando os princípios de reprodutibilidade, explicabilidade e Inteligência Artificial Responsável.

<br><br>


## [Contexto Global do Tráfego de Helicópteros — Por que São Paulo?]()


A escolha de São Paulo como cenário real do projeto não é incidental. A tabela abaixo posiciona a atividade de helicópteros em helipontos localizados em coberturas de edifícios da cidade em relação a outros grandes centros mundiais de aviação de helicópteros, utilizando um índice relativo de tamanho da frota e densidade operacional:

<br>

| [Posição]() | [Cidade]()  | [País]()  | [Principal Indicador]()  | [Índice]() <sub>(Índice Relativo)</sub> | [Frota Estimada]() <sub>(Helicópteros)</sub> | [Destaque]()  |
|:---:|---|---|---|:---:|:---:|---|
| [**1º**]()  | **São Paulo** | 🇧🇷 Brasil | Maior frota | **27,7%** | 400+ | ~2.200 pousos/decolagens diários na região metropolitana |
| [**2º**]()  | **Nova York** | 🇺🇸 EUA | Frota + tráfego urbano intenso | **25,5%** | — | Forte uso executivo, turístico e de transporte |
| [**3º**]()  | **Tóquio** | 🇯🇵 Japão | Frota expressiva | **23,9%** | — | Operações corporativas, emergenciais e de transporte |
| [**4º**]()  | **Rio de Janeiro** | 🇧🇷 Brasil | Frota + operações offshore | **22,8%** | — | Atividade significativa relacionada a petróleo e gás |
| [**5º**]()  | **Londres** | 🇬🇧 Reino Unido | Tráfego executivo | **21,3%** | — | Forte mercado corporativo e heliportos urbanos |
| [**6º**]()  | **Belo Horizonte** | 🇧🇷 Brasil | Frota expressiva | **20,2%** | — | Aviação executiva e corporativa relevante |
| [**7º**]()  | **Santiago** | 🇨🇱 Chile | Frota expressiva | **20,1%** | — | Aviação executiva e operações especiais |
| [**8º**]()  | **Cidade do México** | 🇲🇽 México | Frota expressiva | **19,8%** | — | Transporte executivo e operações governamentais |
| [**9º**]()  | **Bogotá** | 🇨🇴 Colômbia | Frota expressiva | **19,1%** | — | Operações executivas, emergenciais e especiais |
| [**10º**]()  | **Pequim** | 🇨🇳 China | Frota expressiva | **13,6%** | — | Operações executivas, governamentais e especiais |

<br><br>

> [!TIP]
> **Índice** representa uma medida relativa de presença/tráfego de helicópteros, combinando tamanho da frota e densidade operacional. A frota estimada de **400+ helicópteros** e os **~2.200 pousos/decolagens diários** de São Paulo — mencionados no Overview acima — colocam a cidade no topo deste ranking global, razão central pela qual o projeto se concentra especificamente em São Paulo, em vez de uma cidade com infraestrutura de helipontos menos densa ou já amplamente mapeada.


<br><br>


## [Principais Recursos]()

[-]() Pipeline de Inteligência Artificial e Visão Computacional de ponta a ponta <br>

[-]() Aquisição e pré-processamento automatizados de imagens de satélite <br>

[-]() Fluxo de trabalho de inteligência geoespacial e processamento de dados espaciais <br>

[-]() Detecção de objetos com YOLOv8n / YOLO11n <br>

[-]() Fluxo de anotação de imagens e preparação de datasets com Roboflow <br>

[-]() Mapas geoespaciais interativos com MapLibre GL JS + OpenStreetMap <br>

[-]() Geocodificação automatizada com Nominatim (OpenStreetMap) <br>

[-]() Validação em condições reais em mais de 7.900 tiles de satélite de 10 bairros de São Paulo <br>

[-]() Aplicação web e dashboard interativo desenvolvidos com Streamlit <br>

[-]() Repositório de pesquisa totalmente reprodutível <br>

[-]() Datasets, notebooks e artefatos gerados disponíveis para download


<br>

#

<br><br>
<!-- ========= END Overview ========= -->

 
<!-- ========= START 🎥 **DEMO** ========= -->
###### <p align="center">  🎥 **DEMO:** **HELIPAD DETECTION** ✧ `YOLO11` ✧ `MODEL TRAINING`  

https://github.com/user-attachments/assets/5b7d581c-ab5e-416e-8471-d91136b2ada0

###### <p align="center"> 🎶 *Feel Good* by Nina Simone - Deep House  Remix  ✧ *Creation by Fabi* ⚡️

<br><br>

#

<br><br>
<!-- ========= END  🎥 **DEMO** ========= -->


<!-- ========= START 🎥 **DEMO** `AUTOMATED HELIPAD SCRAPING` ========= -->
###### <p align="center"> 🎥 **DEMO:** **AUTOMATED HELIPAD SCRAPING** ✧ `SELENIUM` ✧ `FLIGHTMARKET` ✧ `GEOCODING` ✧ *Creation by Fabi* ⚡️

https://github.com/user-attachments/assets/eab6e951-6b66-4c6c-a2c6-23ee2f902c5f

<br><br><br><br><br>
<!-- ========= END  🎥 **DEMO** ========= -->


<!-- ========= START ToC-->
##  Índice

- [Global Helicopter Traffic Context — Why São Paulo?](#global-helicopter-traffic-context--why-são-paulo)
- [Project Definition](#project-definition)
- [Objective](#objective)
- [Why Helipads?](#why-helipads)
- [Data Source](#data-source)
- [Project Context](#project-context)
- [Business and Research Problem](#business-and-research-problem)
- [Extra Automation Contribution](#extra-automation-contribution)
- [Geospatial Visualization (Kepler.gl)](#geospatial-visualization-keplergl)
- [Overall Flow Architecture](#overall-flow-architecture)
- [AI/ML Ops Pipeline](#aiml-ops-pipeline)
- [Repository Structure](#repository-structure)
- [What is `data/raw/helipad_dataset.rar`?](#what-is-datarawhelipad_datasetrar)
- [What is Roboflow in This Project?](#what-is-roboflow-in-this-project)
- [Methodology](#methodology)
- [Full Technical Pipeline](#full-technical-pipeline)
- [Image Collection and Generation](#image-collection-and-generation)
- [Annotation and Roboflow](#annotation-and-roboflow)
- [Modeling with YOLO](#modeling-with-yolo)
- [Evaluation](#evaluation)
- [Inference and Generalization](#inference-and-generalization)
- [Web Application (Optional Layer)](#web-application-optional-layer)
- [Gains from the Extra Resource](#gains-from-the-extra-resource)
- [Educational Value](#educational-value)
- [Image and Text Sources](#image-and-text-sources)
- [Technologies Used](#technologies-used)
- [How to Run](#how-to-run)
- [Deliverables Covered](#deliverables-covered)
- [Results Analysis](#results-analysis)
- [Field Validation — Real-World Detection Across 10 São Paulo Neighborhoods](#field-validation--real-world-detection-across-10-são-paulo-neighborhoods)
- [Strengths, Limitations and Future Improvements](#strengths-limitations-and-future-improvements)
- [Ethics, LGPD and Governance](#ethics-lgpd-and-governance)
- [Image Attribution](#image-attribution)
- [References](#references)
- [Acknowledgements](#acknowledgements)
- [Final Statement](#final-statement)
<br><br>
