
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

[**Helipad Detector**]() é uma plataforma de Inteligência Artificial e Visão Computacional de ponta a ponta, desenvolvida para detectar e mapear automaticamente **possíveis helipontos em coberturas de edifícios** a partir de imagens de satélite. O projeto transforma imagens geoespaciais em informações estruturadas, permitindo identificar padrões visuais compatíveis com áreas de pouso de helicópteros e representá-los em um mapa interativo.

O foco do projeto é [**São Paulo, Brasil**](https://www.prefeitura.sp.gov.br/), um ambiente urbano particularmente relevante para esse tipo de aplicação. A cidade é amplamente reconhecida por concentrar uma das maiores frotas urbanas de helicópteros do mundo. Dados divulgados por fontes do setor indicam mais de **400 helicópteros registrados**, além de uma rede com mais de **260 helipontos**; as estimativas de operação variam conforme o período e o recorte geográfico, chegando a cerca de **2.200 pousos e decolagens por dia** na região metropolitana. [São Paulo: a cidade dos helicópteros — Folha de S.Paulo](https://www1.folha.uol.com.br/tv/2026/04/sao-paulo-a-cidade-dos-helicopteros.shtml) · [São Paulo tem a maior frota de helicópteros do mundo — Exame](https://exame.com/casual/sao-paulo-tem-a-maior-frota-de-helicopteros-do-mundo-e-a-segunda-em-jatos/) · [Dados sobre a frota de helicópteros em São Paulo — Avantto](https://www.avantto.com.br/blog/business/parabens-sao-paulo/)

Para lidar com esse ambiente aéreo de alta complexidade, a cidade conta com o [**HELICONTROL**](https://www.fab.mil.br/noticias/imprime/42060/CONTROLE%20DO%20ESPA%C3%87O%20A%C3%89REO%20-%20HELICONTROL:%20Seguran%C3%A7a%20e%20fluidez%20no%20controle%20de%20helic%C3%B3pteros%20em%20S%C3%A3o%20Paulo), serviço desenvolvido pela [**Força Aérea Brasileira (FAB)**](https://www.fab.mil.br/) por meio do [**Departamento de Controle do Espaço Aéreo (DECEA)**](https://www.decea.mil.br/). Operado no contexto da Torre de Controle de Congonhas, o sistema coordena o fluxo de helicópteros e contribui para a convivência segura entre as operações dessas aeronaves e o tráfego regular de aviões. [DECEA atua no controle de tráfego aéreo de helicópteros — FAB](https://www.fab.mil.br/noticias/imprime/42044/SEGURAN%C3%87A%20DE%20VOO%20-%20DECEA%20atua%20no%20Controle%20de%20Tr%C3%A1fego%20A%C3%A9reo%20de%20Helic%C3%B3pteros%20do%20Brasil) · [CRCEA-SE — DECEA](https://www.decea.mil.br/?i=unidades&p=crcea-se)

Essas condições tornam São Paulo um cenário real e desafiador para aplicações de inteligência geoespacial baseada em IA. O **Helipad Detector não realiza controle de tráfego aéreo** e não substitui sistemas operacionais como o HELICONTROL. Seu objetivo é apoiar o mapeamento de infraestrutura, identificando, a partir de imagens de satélite, locais com características visuais compatíveis com helipontos e organizando essas informações como dados geográficos para análise urbana, pesquisa acadêmica e futuras aplicações de Smart Cities.

A plataforma implementa um fluxo completo de IA, incluindo coleta de dados públicos, geocodificação, aquisição de imagens de satélite, anotação manual com [**Roboflow**](https://roboflow.com/), treinamento de modelos [**Ultralytics YOLOv8**](https://docs.ultralytics.com/models/yolov8/) e [**Ultralytics YOLO11**](https://docs.ultralytics.com/models/yolo11/), além de validação em condições reais em mais de **7.900 tiles de satélite**. Seu dashboard interativo disponibiliza informações sobre o pipeline, os datasets, os resultados de desempenho e as limitações identificadas, reforçando princípios de reprodutibilidade, explicabilidade e Inteligência Artificial Responsável.

<br><br>

## [Contexto Global do Tráfego de Helicópteros — Por que São Paulo?]()

A escolha de São Paulo não é incidental. Grandes metrópoles como Nova York, Tóquio, Rio de Janeiro, Londres, Cidade do México e Bogotá utilizam helicópteros em diferentes combinações de transporte executivo, turismo, emergência médica, segurança pública, serviços governamentais e operações especializadas.

São Paulo, contudo, destaca-se pela combinação de uma frota urbana de grande porte, elevada densidade de edifícios, presença expressiva de helipontos em coberturas e um volume diário de operações que exige gerenciamento especializado. A existência do **HELICONTROL** evidencia a complexidade prática dessa mobilidade aérea e reforça a pertinência de utilizar a cidade como estudo de caso para a detecção automatizada de possíveis helipontos.

<br>

| Cidade | País | Contexto de mobilidade aérea por helicópteros | Fonte de referência |
|---|---|---|---|
| [**São Paulo**](https://www.fab.mil.br/noticias/imprime/42060/CONTROLE%20DO%20ESPA%C3%87O%20A%C3%89REO%20-%20HELICONTROL:%20Seguran%C3%A7a%20e%20fluidez%20no%20controle%20de%20helic%C3%B3pteros%20em%20S%C3%A3o%20Paulo) | 🇧🇷 Brasil | Operações urbanas de helicópteros em ambiente de alta densidade, apoiadas pelo gerenciamento dedicado do HELICONTROL na área operacional de Congonhas | [(FAB) - Força Aérea Brasileira  - HELICONTROL](https://www.fab.mil.br/noticias/imprime/42060/CONTROLE%20DO%20ESPA%C3%87O%20A%C3%89REO%20-%20HELICONTROL:%20Seguran%C3%A7a%20e%20fluidez%20no%20controle%20de%20helic%C3%B3pteros%20em%20S%C3%A3o%20Paulo) |
| [Nova York](https://council.nyc.gov/data/helicopter-noise-and-safety/) | 🇺🇸 Estados Unidos | Heliportos públicos, voos de táxi aéreo, aviação geral, deslocamentos de passageiros, operações militares e passeios turísticos regulamentados | [New York City Council — Helicopter Noise and Safety](https://council.nyc.gov/data/helicopter-noise-and-safety/) |
| [Tóquio](https://www.mlit.go.jp/en/) | 🇯🇵 Japão | Operações corporativas, de emergência, segurança pública e transporte especializado dentro do sistema nacional de aviação civil | [Ministério da Terra, Infraestrutura, Transporte e Turismo do Japão (MLIT)](https://www.mlit.go.jp/en/) |
| [Rio de Janeiro](https://www.gov.br/anac/pt-br) | 🇧🇷 Brasil | Aviação executiva, transporte urbano e operações relacionadas às atividades offshore de petróleo e gás | [Agência Nacional de Aviação Civil (ANAC)](https://www.gov.br/anac/pt-br) |
| [Londres](https://londonheliport.co.uk/) | 🇬🇧 Reino Unido | Infraestrutura de heliporto urbano voltada a operações executivas, serviços VIP, pousos, decolagens, abastecimento e fretamento | [London Heliport](https://londonheliport.co.uk/) |
| [Belo Horizonte](https://www.gov.br/anac/pt-br) | 🇧🇷 Brasil | Aviação executiva, operações corporativas e uso de helicópteros em serviços especializados | [Agência Nacional de Aviação Civil (ANAC)](https://www.gov.br/anac/pt-br) |
| [Santiago](https://www.dgac.gob.cl/) | 🇨🇱 Chile | Operações executivas, corporativas e especializadas reguladas pela autoridade de aviação civil chilena | [Dirección General de Aeronáutica Civil de Chile (DGAC)](https://www.dgac.gob.cl/) |
| [Cidade do México](https://www.gob.mx/afac) | 🇲🇽 México | Transporte executivo, atividades governamentais, segurança pública e operações aéreas especializadas | [Agencia Federal de Aviación Civil do México (AFAC)](https://www.gob.mx/afac) |
| [Bogotá](https://www.aerocivil.gov.co/) | 🇨🇴 Colômbia | Operações executivas, emergenciais e serviços aéreos especializados sob regulação da aviação civil colombiana | [Aerocivil Colômbia](https://www.aerocivil.gov.co/) |
| [Pequim](http://www.caac.gov.cn/English/) | 🇨🇳 China | Operações governamentais, executivas e serviços aéreos especializados no contexto da aviação civil chinesa | [Administração da Aviação Civil da China (CAAC) — site oficial em inglês](http://www.caac.gov.cn/English/) |


| [Pequim](http://www.caac.gov.cn/English/) | 🇨🇳 China | Operações governamentais, executivas e de serviços especializados | [Administração da Aviação Civil da China (CAAC) — site oficial em inglês](http://www.caac.gov.cn/English/) |

<br><br>

> [!TIP]
> São Paulo é o foco do **Helipad Detector** pela combinação de alta densidade urbana, grande concentração de edifícios, infraestrutura de helipontos em coberturas e tráfego intenso de helicópteros. O projeto utiliza esse contexto para demonstrar como a Visão Computacional e os dados de satélite podem apoiar o mapeamento automatizado de infraestrutura urbana. As detecções do modelo representam **candidatos visuais** e não constituem confirmação regulatória, operacional ou aeronáutica da existência de um heliponto.

<br><br>
<!-- ========= END Overview ========= -->



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
