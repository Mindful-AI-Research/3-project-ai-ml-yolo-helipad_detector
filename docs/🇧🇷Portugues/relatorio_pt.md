Helipad Detector --- Relatório Completo

> ![](media/image1.jpeg){width="6.526744313210848in"
> height="2.438332239720035in"}

![](media/image2.png){width="0.5in" height="0.5in"}

Helipad Detector

*Detecção de Helipontos em Imagens de Satélite de São Paulo com YOLO*

**Relatório Completo e Explica4vo do Projeto**

Pipeline técnico, metodologia, resultados e guia em linguagem simples

> **Pon49cia Universidade Católica de São Paulo (PUC-SP) --- FACEI**
>
> Graduação em Human Centered-AI & Data Science Machine Learning / Visão
> Computacional --- Projeto P2

**Professor:** Rooney Ribeiro Albuquerque Coelho

***Autor: Fabiana*** ![](media/image3.png){width="0.18055555555555555in"
height="0.18055555555555555in"}**Campanari**

> **São Paulo · 2026**
>
> Página 1 de 25
>
> Helipad Detector --- Relatório Completo
>
> **Sumário**
>
> Este relatório existe em duas camadas ao mesmo tempo. Para quem já
> trabalha com dados e inteligência arTﬁcial, ele é um relatório técnico
> completo: cobre o pipeline de doze etapas, os três experimentos de
> treinamento, as métricas de avaliação e a validação de campo em dez
> bairros de São Paulo. Para quem nunca ouviu falar de YOLO ou de mAP,
> cada seção também traz uma explicação em linguagem simples --- como se
> esTvéssemos conversando sobre o projeto, sem pressupor conhecimento
> prévio de Inteligência ArTﬁcial.
>
> **Índice**

-   1\. O que é o Helipad Detector, em uma frase

-   2\. Por que detectar helipontos --- e por que isso é di\\cil

-   3\. Como uma IA aprende a "ver" --- explicação para leigos

-   4\. Fonte de dados e escopo geográﬁco

-   5\. O pipeline técnico completo --- as 12 etapas

-   6\. Coleta de imagens e anotação

-   7\. Modelagem com YOLO --- os três experimentos

-   8\. Avaliação quanTtaTva --- o que os números signiﬁcam

-   9\. Validação de campo --- testando em dados reais, dez bairros

-   10\. Análise qualitaTva --- acertos, erros e por quê

-   11\. Aplicação web interaTva

-   12\. Pontos fortes, limitações e próximos passos

-   13\. ÉTca, LGPD e governança

-   14\. Conclusão

-   15\. Glossário de termos técnicos

> Página 2 de 25
>
> Helipad Detector --- Relatório Completo

# O que é o Helipad Detector, em uma frase

> Em uma frase: é um sistema de Inteligência ArTﬁcial que olha para
> imagens de satélite de São Paulo e aponta, sozinho, onde existem
> helipontos nos telhados dos prédios.
>
> Em termos um pouco mais técnicos: o Helipoint Detector é um pipeline
> completo de Detecção de Objetos que localiza helipontos em telhados na
> cidade de São Paulo, usando imagens aéreas/orbitais de alta resolução
> e modelos da família YOLOv8/YOLOv11. O projeto cobre todo o ciclo de
> vida de um sistema aplicado de visão computacional: coleta programáTca
> de imagens, automação geoespacial, criação e curadoria de um dataset
> próprio, anotação, pré-processamento, treinamento, avaliação
> quanTtaTva e qualitaTva, inferência em bairros não vistos durante o
> treino, uma etapa extra de validação de campo em dados reais em dez
> bairros, e uma aplicação web interaTva para demonstração.
>
> *Um ponto importante para quem não é da área: o projeto não usou
> nenhum banco de imagens pronto. Toda a base de dados --- as fotos de
> satélite e as marcações de onde ﬁcam os helipontos --- foi construída
> do zero pela equipe, etapa que costuma consumir a maior parte do
> esforço em qualquer projeto sério de Inteligência ArNﬁcial.*
>
> Página 3 de 25
>
> Helipad Detector --- Relatório Completo

# Por que detectar helipontos --- e por que isso é di9cil

> Helipontos foram escolhidos como alvo porque, vistos de cima, eles têm
> um desenho bem caracterísTco: um grande "H" pintado sobre uma área
> circular ou quadrada no telhado. Isso parece fácil de reconhecer ---
> mas na práTca não é, e é justamente essa diﬁculdade que torna o
> projeto interessante do ponto de vista educacional.
>
> Em imagens de satélite de uma cidade densa como São Paulo, o modelo
> pode se confundir com:

-   Piscinas de prédios, que têm formato e contraste parecidos com o
    "H";

-   Quadras esporTvas, com linhas e marcações geométricas semelhantes;

-   Estruturas de telhado, caixas d'água e equipamentos de
    ar-condicionado;

-   Super\\cies reﬂexivas, que mudam de aparência dependendo da luz do
    dia.

> Esse Tpo de confusão é chamado, na área, de falso posiTvo --- quando o
> modelo "vê" um heliponto onde não existe nenhum. Trabalhar com um alvo
> que gera falsos posiTvos plausíveis é o que torna esse projeto um bom
> exercício de visão computacional: obriga a equipe a pensar sobre
> qualidade de anotação, diversidade de exemplos e os limites reais do
> modelo, em vez de comemorar um número bonito sem entender o que está
> por trás dele.
>
> Página 4 de 25
>
> Helipad Detector --- Relatório Completo

# Como uma IA aprende a "ver" - explicação em linguagem simples

> Antes de entrar no pipeline técnico, vale explicar, em termos simples,
> o que está acontecendo por baixo do capô.

##### *O que é "Detecção de Objetos"?* {#o-que-é-detecção-de-objetos .unnumbered}

> É a tarefa de IA que responde a duas perguntas ao mesmo tempo, para
> cada imagem: "existe o objeto qu eu procuro aqui?" e "onde exatamente
> ele está?". A resposta da segunda pergunta vem na forma de uma caixa
> retangular ao redor do objeto --- chamada de bounding box (caixa
> delimitadora) --- desenhada sobre a imagem.

##### *O que é o YOLO?* {#o-que-é-o-yolo .unnumbered}

> YOLO é a sigla de "You Only Look Once" ("você só olha uma vez"), o
> nome de uma família de modelos de Inteligência ArTﬁcial muito usada
> para detecção de objetos em tempo real. Ele examina a imagem inteira
> de uma só vez e devolve, diretamente, a lista de objetos encontrados
> com suas respecTvas caixas e um grau de conﬁança (de 0 a 100%) para
> cada detecção. Este projeto usa a versão YOLOv8n (a letra "n" indica a
> variante "nano", mais leve e rápida de treinar) e também testa a
> variante mais recente YOLOv11n.

##### *Como o modelo "aprende"?* {#como-o-modelo-aprende .unnumbered}

> O processo se chama treinamento. A equipe mostra ao modelo centenas de
> imagens já marcadas manualmente --- "aqui tem um heliponto, e ele está
> exatamente nesta posição" --- e o modelo ajusta, aos poucos, seus
> parâmetros internos para acertar cada vez mais essas marcações. Cada
> "passada" completa por todas as imagens de treino é chamada de época
> (epoch). Neste projeto, os modelos foram treinados por 60 a 100
> épocas.

##### *Por que a qualidade dos dados importa mais do que o modelo em si?* {#por-que-a-qualidade-dos-dados-importa-mais-do-que-o-modelo-em-si .unnumbered}

> Essa é talvez a lição central do projeto: cerca de 80% do esforço em
> um projeto real de Inteligência ArTﬁcial está na construção e
> curadoria dos dados, não em ajustes ﬁnos de arquitetura do modelo. O
> YOLO usado por este grupo é essencialmente o mesmo YOLO que qualquer
> outra equipe usaria; o que diferencia o resultado ﬁnal é a qualidade
> das imagens coletadas, a consistência das marcações e a diversidade
> geográﬁca do dataset.
>
> Página 5 de 25
>
> Helipad Detector --- Relatório Completo

# Fonte de dados e escopo geográﬁco

> O escopo geográﬁco segue o brieﬁng acadêmico do curso: a cidade de São
> Paulo, com foco em bairros próximos a corredores corporaTvos densos,
> onde a presença de helipontos é mais comum --- Perdizes, Higienópolis,
> Pacaembu, Sumaré, Avenida Paulista, Itaim Bibi, Pinheiros, Faria Lima,
> Berrini, Vila Olímpia, Brooklin e Morumbi.

##### *De onde vêm as imagens?* {#de-onde-vêm-as-imagens .unnumbered}

-   ESRI World Imagery (Tles XYZ) --- fonte principal, com resolução
    sub-métrica e acesso HTTP programáTco (ou seja, pode ser baixada
    automaTcamente por código);

-   Google Earth Web --- fonte complementar, usada apenas para capturas
    pontuais de alvos especíﬁcos, nunca para coleta em massa;

-   GeoSampa --- mencionada como fonte alternaTva de alta resolução, um
    possível extra além do escopo básico.

> Sempre que uma imagem ou mosaico derivado do ESRI é reproduzido, o
> projeto inclui a atribuição obrigatória: "Source: Esri, Maxar,
> Earthstar Geographics, and the GIS User Community".
>
> Página 6 de 25
>
> Helipad Detector --- Relatório Completo

# O pipeline técnico completo --- as 12 etapas

> O pipeline completo, do zero à validação em campo, pode ser resumido
> em doze etapas. Cada uma delas está descrita abaixo com o nome técnico
> e uma explicação em linguagem simples do que ela signiﬁca na práTca.

##### *1 e 2 --- Descoberta e extração de registros de helipontos* {#e-2-descoberta-e-extração-de-registros-de-helipontos .unnumbered}

> Um robô de automação (Selenium, em src/geospaTal/helipad_bot.py)
> navega por um site público de aviação, procurando registros de
> helipontos e extraindo suas coordenadas geográﬁcas e metadados. Em
> linguagem simples: em vez de procurar manualmente, uma no navegador,
> "onde existem helipontos no Brasil", um programa faz essa busca
> sozinho, de forma sistemáTca.

##### *--- Organização das coordenadas*

> Os dados coletados são salvos e organizados em
> src/geospaTal/helipad_coordinates.csv, uma planilha simples com data,
> coordenadas e o bairro correspondente.

##### *--- Conversão em bounding boxes geográﬁcas*

> O script src/geospaTal/transform_coordinates.py converte cada
> coordenada de um heliponto (um ponto único) em uma pequena área
> retangular ao redor dele --- a bounding box geográﬁca ---, que será
> usada para decidir qual pedaço do mapa baixar.

##### *--- Download de imagens de satélite*

> Para cada bounding box, o sistema baixa os "Tles" (pedaços quadrados
> de imagem de satélite) do ESRI World Imagery, no zoom 19 --- o nível
> de aproximação recomendado para alvos pequenos como helipontos.

##### *--- Construção de mosaicos*

> Os Tles baixados são unidos em mosaicos maiores, organizados por
> bairro e por zoom (notebook src/
> geospaTal/geospaTal_image_collecTon.ipynb), formando imagens conÄnuas
> prontas para inspeção visual.
>
> Página 7 de 25
>
> Helipad Detector --- Relatório Completo

##### *--- Triagem manual*

> Uma pessoa da equipe revisa os mosaicos e descarta os pedaços de
> imagem que claramente não contêm heliponto, mantendo apenas o material
> relevante para anotação --- evitando desperdiçar tempo anotando
> imagens vazias.

##### *e 9 --- Anotação e exportação do dataset*

> As imagens selecionadas sobem para o Roboﬂow, plataforma onde a equipe
> desenha as caixas delimitadoras ao redor de cada heliponto, usando uma
> única classe ("heliponto"). Em seguida, o Roboﬂow aplica
> pré-processamento (redimensionamento para 640×640 pixels), técnicas de
> aumento de dados (augmentaTons, como rotações e variações de brilho) e
> divide o conjunto em treino, validação e teste, exportando tudo em
> formato compaÄvel com o YOLO.

##### *--- Treinamento*

> Os modelos YOLOv8n são treinados no Google Colab, usando uma GPU T4
> gratuita, monitorando métricas e curvas de aprendizado ao longo das
> épocas.

##### *--- Inferência em bairro não visto*

> O modelo treinado é testado em um bairro que nunca apareceu durante o
> treinamento, para avaliar sua capacidade de generalização --- ou seja,
> se ele realmente "aprendeu" o padrão visual de um heliponto, e não
> apenas decorou as imagens de treino.

##### *--- Validação de campo em dez bairros*

> Além do teste padrão, o melhor modelo foi rodado contra 7.943 Tles
> reais de satélite, cobrindo dez bairros inteiros de São Paulo ---
> muito além do conjunto curado de treino/validação/teste, aproximando o
> projeto de um cenário real de uso.
>
> Página 8 de 25
>
> Helipad Detector --- Relatório Completo

# Coleta de imagens e anotação

### Coleta programá4ca

> A coleta segue o padrão de Tles XYZ do ESRI World Imagery: zoom 19
> para alvos pequenos como helipontos; bounding boxes deﬁnidas por
> bairro; conversão para índices de Tle por meio de uma função chamada
> deg2Tle; download com veriﬁcação do status HTTP e ﬁltragem de imagens
> "placeholder" (imagens em branco que indicam falha); e organização das
> imagens em pastas por bairro e nível de zoom.

### Curadoria e volume do dataset

-   Volume mínimo de 200 imagens com o objeto-alvo após a curadoria;

-   Diversidade geográﬁca: pelo menos 3 bairros diferentes no treino;

-   Reserva de pelo menos 1 bairro totalmente não visto para o teste
    ﬁnal de generalização;

-   Triagem manual dos Tles, descartando recortes sem heliponto.

### Anotação no Roboﬂow

> O Roboﬂow foi usado como plataforma central de anotação e gestão do
> dataset --- não como origem das imagens, apenas como ferramenta de
> marcação, versionamento, pré-processamento e exportação. As regras
> seguidas pela equipe foram:

-   Classe única: heliponto;

-   Caixas delimitadoras justas (bem ajustadas ao objeto, sem sobra de
    área);

-   Critérios escritos para casos ambíguos --- objetos parcialmente
    visíveis, sombras, reﬂexos;

-   Trabalho de anotação dividido entre os membros da equipe, para
    evitar viés de um único anotador.

### Pré-processamento e divisão do dataset

-   Redimensionamento para 640×640 pixels;

-   Aumentos de dados: rotações de 90°, espelhamentos
    horizontal/verTcal, pequenas variações de brilho e contraste;

-   Divisão padrão: 70% treino, 20% validação, 10% teste.

> Cada arquivo de anotação (.txt) contém, por linha, coordenadas
> normalizadas no formato (classe, x_centro, y_centro, largura, altura)
> --- o formato padrão esperado pelo YOLO.
>
> Página 9 de 25
>
> Helipad Detector --- Relatório Completo

# Modelagem com YOLO --- os três experimentos

> O treinamento foi feito com UltralyTcs YOLOv8n no Google Colab (GPU
> T4), usando Python, PyTorch e a biblioteca roboﬂow para integração
> direta do dataset. Seguindo o brieﬁng do curso, que pede pelo menos
> dois experimentos variando um hiperparâmetro por vez, a equipe rodou
> três:

-   exp1 --- dataset original, 60 épocas, imgsz 640, batch 16, seed 42.

-   exp2 --- dataset original, 100 épocas (mesmos demais parâmetros),
    para testar se treinar por mais tempo melhora o resultado ou causa
    overﬁÉng (quando o modelo "decora" o treino em vez de aprender o
    padrão geral).

-   exp3 --- versão aumentada (fork) do dataset, com rotação de ±15°,
    variação de brilho de 25% e espelhamento horizontal/verTcal, também
    por 100 épocas --- manTdo como um ponto de comparação separado por
    usar uma versão diferente do dataset.

### Um problema de integridade de dados --- encontrado e corrigido

> Durante o desenvolvimento, a equipe idenTﬁcou um problema importante:
> uma execução inicial do notebook havia baixado silenciosamente o
> dataset com fork (o dataset aumentado), mas salvado os resultados sob
> o nome "exp2", o que gerou documentação incorreta sobre qual dataset
> havia sido realmente usado naquele experimento.
>
> *Esse Npo de erro é conhecido como um problema de integridade de
> dados: o código rodou sem travar, os números pareciam plausíveis, mas
> a atribuição do experimento estava errada. Em qualquer projeto real de
> IA, esse é exatamente o Npo de falha silenciosa mais perigosa ---
> porque não gera um erro visível, apenas uma conclusão falsa.*
>
> A correção foi em duas partes: renomear a execução equivocada para
> exp3 (já que, na práTca, era o experimento com o dataset aumentado) e
> re-rodar o exp2 corretamente, contra o workspace do dataset original.
> Como salvaguarda contra recorrência, foi adicionado um guard de assert
> no notebook de treino
>
> --- uma veriﬁcação automáTca que interrompe a execução caso o dataset
> carregado não seja o esperado para aquele experimento.
>
> Página 10 de 25
>
> Helipad Detector --- Relatório Completo

# Avaliação quan4ta4va --- o que os números signiﬁcam

> Antes das tabelas, um pequeno glossário das quatro métricas usadas
> para avaliar o modelo, explicadas em linguagem simples:

-   Precision (Precisão): de todas as vezes que o modelo disse "achei um
    heliponto", quantas dessas vezes ele estava certo? Precisão alta
    signiﬁca poucos alarmes falsos.

-   Recall (Revocação): de todos os helipontos que realmente existem nas
    imagens, quantos o modelo conseguiu encontrar? Recall alto signiﬁca
    que o modelo raramente deixa passar um heliponto real.

-   mAP@50: uma nota única que resume a qualidade geral das detecções,
    considerando um critério "razoável" de sobreposição entre a caixa
    prevista e a caixa real (50% de sobreposição mínima).

-   mAP@50-95: a mesma ideia, mas com um critério muito mais rigoroso,
    exigindo sobreposição quase perfeita em vários níveis --- o padrão
    usado em benchmarks internacionais como o COCO.

### Resultados dos três experimentos

> Os três experimentos são descobertos automaTcamente e comparados ao
> vivo na aba "Experiment Metrics" do dashboard Streamlit do projeto.
> Estes são os resultados na melhor época de cada execução:

  ---------------------------------------------------------------------------------------------
  **Experimento**          **Melhor   **Precision**   **Recall**   **mAP@50**   **mAP@50-95**
                           Época**                                              
  ------------------------ ---------- --------------- ------------ ------------ ---------------
  exp1 (60 ép., dataset    54         1,000           0,963        0,994        0,881
  original)                                                                     

  exp2 (100 ép., dataset   81         0,982           0,971        0,993        0,888
  original)                                                                     

  exp3 (100 ép., fork      78         0,943           1,000        0,993        0,885
  aumentado)                                                                    
  ---------------------------------------------------------------------------------------------

> Leitura em linguagem simples desses resultados: o exp2 supera
> levemente o exp1 em mAP@50-95 (uma diferença de +0,0065) ao treinar
> por mais tempo (100 em vez de 60 épocas), enquanto o exp1 permanece
> marginalmente à frente em Precision na sua melhor época. Essas
> diferenças são pequenas o suﬁciente para estarem dentro da margem de
> ruído esperada, dado que o dataset é pequeno (cerca de 150 imagens ao
> todo) --- ou seja, treinar mais não trouxe um ganho dramáTco, mas
> também não piorou o modelo.
>
> Um sinal importante de saúde do treinamento: as curvas de loss (a
> "taxa de erro" do modelo durante o aprendizado) não mostram overﬁÉng
> em nenhuma das três execuções --- a loss de validação acompanha de
> perto a loss de treino ao longo de todas as épocas, em vez de se
> distanciar dela. Isso indica que o modelo está aprendendo um padrão
> genuíno de "o que é um heliponto", e não apenas memorizando as imagens
> de treino.
>
> Página 11 de 25
>
> Helipad Detector --- Relatório Completo

### Gráﬁcos de treinamento --- exp1 (60 épocas, dataset original)

> Estes gráﬁcos foram gerados diretamente a parTr do results.csv real do
> exp1, o experimento-base do projeto

![](media/image4.jpeg){width="5.6981441382327205in"
height="1.6674989063867016in"}

> *Figura 1 --- Evolução das losses (Box, Cls, DFL) por época, treino
> vs. validação. Sem sinal evidente de overﬁZng nas 60 épocas;
> val/cls_loss oscila nas primeiras 20 épocas e estabiliza a parNr da
> 30.*

![](media/image5.jpeg){width="5.742465004374453in" height="2.2475in"}

> *Figura 2 --- Precision e Recall ao longo do treino. Precision
> estabiliza acima de 0,95 a parNr da época 30; Recall alcança 0,97+ nas
> épocas ﬁnais, após uma queda acentuada por volta da época 5.*
>
> Página 12 de 25
>
> Helipad Detector --- Relatório Completo

![](media/image6.jpeg){width="5.834733158355205in" height="2.755in"}

*Figura 3 --- mAP@50 e mAP@50-95. Pico na melhor época (54), após o qual
as métricas ﬂutuam levemente.*

### Gráﬁcos de treinamento --- exp2 (100 épocas, dataset original)

> O exp2 é a ablação oﬁcial exigida pelo brieﬁng: mesmo dataset do exp1,
> variando apenas a duração do treino (60 → 100 épocas).

![](media/image7.jpeg){width="6.013888888888889in"
height="3.2247036307961503in"}![](media/image8.png){width="6.458333333333333in"
height="3.7108147419072615in"}

*Visão geral --- losses, mAP@50-95, Precision e Recall ao longo de 100
épocas (exp2).*

> Página 13 de 25
>
> Helipad Detector --- Relatório Completo

![](media/image9.png){width="4.332061461067367in"
height="3.2490463692038496in"}![](media/image10.png){width="4.776505905511811in"
height="3.7351574803149608in"}

> *Matriz de confusão (validação, exp2): 34 acertos, 3 falsos posiNvos
> de fundo confundido com heliponto.*

![](media/image11.png){width="4.453047900262467in"
height="3.7147801837270342in"}![](media/image12.png){width="4.897492344706912in"
height="4.200891294838145in"}

> *Correlação entre as losses de treino e as métricas de validação
> (exp2).*
>
> Página 14 de 25
>
> Helipad Detector --- Relatório Completo

### Gráﬁcos de treinamento --- exp3 (100 épocas, dataset com fork/augmenta4on)

> O exp3 usa uma versão diferente do dataset (fork com augmentaTon
> extra), por isso funciona como ponto de referência adicional, e não
> como comparação direta de ablação --- essa comparação é a exp1 vs.
> exp2, acima.

![](media/image13.jpeg){width="4.945910979877516in"
height="3.2766655730533683in"}

> *Visão geral --- losses, mAP@50-95, Precision e Recall ao longo de 100
> épocas (exp3). Mesmo padrão de leve queda entre a melhor época e a
> ﬁnal observado no exp1.*

![](media/image14.png){width="3.924856736657918in"
height="3.4807283464566927in"}

> *Correlação entre as losses de treino e as métricas de validação
> (exp3): cls_loss é a mais fortemente (anN)correlacionada com mAP@50-95
> (-0,84).*
>
> Página 15 de 25
>
> Helipad Detector --- Relatório Completo

# Validação de campo --- testando em dados reais, dez bairros

> Um diferencial deste projeto em relação ao mínimo exigido pelo brieﬁng
> é a etapa de validação de campo: em vez de avaliar o modelo apenas no
> conjunto de teste curado (imagens já selecionadas manualmente), o
> melhor modelo (exp2) foi rodado contra 7.943 Tles reais de satélite,
> sem nenhuma curadoria prévia, cobrindo dez bairros inteiros de São
> Paulo --- incluindo corredores corporaTvos densos como Itaim Bibi,
> Avenida Paulista, Vila Olímpia, Pinheiros, Brooklin e Faria Lima.
>
> Em termos simples: em vez de mostrar ao modelo só as "melhores fotos",
> a equipe o soltou para trabalhar em um bairro inteiro, Tle por Tle,
> exatamente como ele funcionaria em um uso real.
>
> Os Tles e bounding boxes por região vêm de
> src/geospaTal/sp_neighborhoods_bbox.csv; o download de Tles e a
> inferência são automaTzados pelos scripts
> src/geospaTal/download_all_regions.py e auto_triage_regions.py, ambos
> retomáveis --- ou seja, o processo pode ser pausado e retomado depois
> sem reprocessar o que já foi feito, algo essencial ao lidar com
> milhares de imagens.

  --------------------------------------------------------------------------
  **Bairro**                   **Detectados**   **Total de       **Taxa**
                                                Tiles**          
  ---------------------------- ---------------- ---------------- -----------
  Inter-Zone Corridor          133              480              27,7%

  Itaim Bibi                   191              750              25,5%

  Brooklin                     231              1.014            22,8%

  Vila Olímpia                 158              660              23,9%

  Av. Paulista (Trecho 1)      179              840              21,3%

  Faria Lima                   170              840              20,2%

  Av. Paulista (Trecho 2)      157              780              20,1%

  Pinheiros                    244              1.232            19,8%

  Vila Nova Conceição          109              572              19,1%

  Alphaville Industrial        105              775              13,6%
  --------------------------------------------------------------------------

  ------------------------------------------------------------------------
  **TOTAL**                    **1.677**      **7.943**        **21,1%**
  ---------------------------- -------------- ---------------- -----------

  ------------------------------------------------------------------------

> Interpretação dos resultados: Inter-Zone Corridor e Itaim Bibi
> apresentam as maiores taxas de detecção, o que é coerente com serem
> corredores corporaTvos densos --- regiões com muitos prédios
> comerciais e, portanto, mais chances reais de haver helipontos.
> Alphaville Industrial, com perﬁl mais industrial e menos torres
> corporaTvas, apresenta a menor taxa, alinhada ao esperado para esse
> Tpo de uso do solo. Esse Tpo de coerência entre o resultado do modelo
> e o conhecimento urbano da cidade é um bom sinal de que o modelo está
> captando um padrão real, e não gerando detecções aleatórias.
>
> Página 16 de 25
>
> Helipad Detector --- Relatório Completo

## Comparando exp1, exp2 e exp3 na mesma validação de campo

> A validação de campo da Seção 9 usa o **exp2**, o modelo escolhido
> para o deploy --- mas a mesma rodada (7.943 tiles, dez bairros) foi
> repetida com os pesos do **exp1** e do **exp3**, para verificar se o
> modelo líder no benchmark curado também generaliza melhor em campo.

  -----------------------------------------------------------------------
  **Bairro**                 **exp1**       **exp2**       **exp3**
  -------------------------- -------------- -------------- --------------
  Alphaville Industrial      6,1%           13,6%          13,3%

  Av. Paulista (Trecho 1)    9,8%           **21,3%**      26,8%

  Av. Paulista (Trecho 2)    9,3%           20,1%          23,8%

  Brooklin                   9,7%           **22,8%**      14,2%

  Faria Lima                 9,0%           **20,2%**      17,2%

  Inter-Zone Corridor        14,2%          **27,7%**      20,8%

  Itaim Bibi                 11,9%          **25,5%**      17,9%

  Pinheiros                  8,2%           **19,8%**      16,6%

  Vila Olímpia               12,9%          **23,9%**      16,5%

  Vila Nova Conceição        8,0%           19,1%          12,1%

  **TOTAL (taxa geral de     **9,6%**       **21,1%**      **17,9%**
  detecção)**                                              
  -----------------------------------------------------------------------

#### *Achado principal:* {#achado-principal .unnumbered}

> *o exp1 lidera o conjunto de validação curado em Precision (1,000, ver
> Seção 8.1) mas, nas mesmas condições de campo, detecta aproximadamente
> **metade** dos helipontos reais que o exp2 detecta (9,6% vs. 21,1% de
> taxa geral) e sensivelmente menos que o exp3 (17,9%). O modelo com a
> melhor nota num benchmark pequeno e curado não é automaticamente o que
> generaliza melhor em cobertura real de satélite sem filtragem prévia;
> exatamente o tipo de lacuna que a validação de campo em larga escala,
> além do split padrão de treino/validação/teste, existe para capturar.*
>
> *Esse resultado também reforça a decisão de usar o exp2 em produção,
> em vez do exp1 (que tinha a Precision mais alta no papel).*
>
> *\\*
>
> Página 17 de 25
>
> Helipad Detector --- Relatório Completo

# Análise qualita4va --- acertos, erros e por quê

> Números resumidos, como Precision ou mAP, contam apenas parte da
> história. Por isso, tanto as imagens curadas de teste quanto a rodada
> de validação de campo do Faria Lima foram revisadas caso a caso,
> olhando manualmente para o que o modelo acertou e o que ele errou:

  ---------------------------------------------------------------------------------
  **Tipo**       **Tile de Exemplo**           **Conﬁança**   **Observação**
  -------------- ----------------------------- -------------- ---------------------
  Acerto claro   Tle_z19_x194126_y297485.jpg   0,94           Padrão "H" níTdo em
                                                              quadrado bem deﬁnido
                                                              no telhado

  Acerto claro   Tle_z19_x194143_y297481.jpg   0,96           Geometria e contraste
                                                              claros, caixa bem
                                                              ajustada

  Acerto         Tle_z19_x194545_y298183.jpg   0,77           Detecção correta
  desaﬁador                                                   mesmo com
                                                              ângulo/iluminação
                                                              menos favorável

  Falso PosiTvo  Tle_z19_x194129_y297480.jpg   0,78           Caixa sobre quadra
                                                              esporTva, não
                                                              heliponto

  Falso PosiTvo  Tle_z19_x194547_y298176.jpg   0,86           Caixa sobre piscina,
                                                              geometricamente
                                                              parecida com o "H"

  Falha de dado  Tle_z19_x194139_y297467.jpg   ---            Tile vazio/preto
                                                              (falha de download do
                                                              ESRI) marcado como
                                                              "Detected"
  ---------------------------------------------------------------------------------

> Dois padrões de erro merecem destaque, porque ambos são explicáveis
> --- e explicáveis é uma palavra-chave em avaliação de IA responsável:
> um erro que a equipe entende e consegue jusTﬁcar é muito mais tratável
> do que um erro opaco.

-   Falsos posiTvos previsíveis: piscinas e quadras esporTvas
    comparTlham geometria e contraste retangular semelhantes ao "H" do
    heliponto --- esse é um erro de confusão visual, tratável
    adicionando mais exemplos negaTvos (imagens de piscinas e quadras
    marcadas como "não é heliponto") em treinos futuros.

-   Tiles vazios marcados como detecção: esse não é um erro do modelo, e
    sim uma falha do pipeline de dados --- quando o download de um Tle
    falha parcialmente, ele pode ﬁcar preto ou vazio, e o modelo às
    vezes reage a esse ruído. A correção recomendada, já documentada
    para a próxima iteração do projeto, é checar o desvio-padrão de
    pixel da imagem antes de rodar a inferência, descartando
    automaTcamente Tles vazios.

> Página 18 de 25
>
> Helipad Detector --- Relatório Completo

### Exemplos reais de detecção (conjunto de teste curado, exp1)

> Abaixo, recortes reais gerados pelo próprio modelo (exp1), extraídos
> de reports/model_outputs/detect/ predict/, mostrando a caixa prevista
> e o grau de conﬁança da detecção --- o mesmo Tpo de saída que aparece
> na aplicação web.

##### *Acertos claros (alta conﬁança)* {#acertos-claros-alta-conﬁança .unnumbered}

![](media/image15.jpeg){width="2.08in" height="2.08in"}

> *heliponto --- conﬁança 0,95. Padrão "H" níNdo, caixa bem ajustada ao
> contorno do heliponto.*

![](media/image16.jpeg){width="2.08in" height="2.08in"}

> *heliponto --- conﬁança 0,86. Marcação clara idenNﬁcada mesmo com
> vegetação e sombra próximas ao telhado.*

##### *Acerto desaﬁador* {#acerto-desaﬁador .unnumbered}

![](media/image17.jpeg){width="2.08in" height="2.08in"}

> *heliponto --- conﬁança 0,64. Conﬁança moderada; a estrutura do
> heliponto é menos evidente visualmente nesta captura.*
>
> Página 19 de 25
>
> Helipad Detector --- Relatório Completo

##### *Falsos posi\\vos* {#falsos-posivos .unnumbered}

![](media/image18.jpeg){width="2.08in" height="2.08in"}

> *heliponto --- conﬁança 0,28. Marcação de solo/via confundida com
> padrão de heliponto --- conﬁança baixa, coerente com um falso
> posiNvo.*

![](media/image19.jpeg){width="2.08in" height="2.08in"}

> *heliponto --- conﬁança 0,28. Outro caso de via/pavimento gerando
> falso posiNvo, novamente com conﬁança baixa.*
>
> Nota metodológica: nenhum exemplo de falso negaTvo conﬁrmado foi
> incluído nesta versão do relatório --- os Tles sem detecção
> disponíveis não têm anotação de referência (ground truth) que conﬁrme
> a presença real de um heliponto não detectado. Adicionar isso exige
> cruzar com o rótulo original do dataset antes de publicar a alegação,
> para não arriscar uma aﬁrmação incorreta.
>
> Página 20 de 25
>
> Helipad Detector --- Relatório Completo

# Aplicação web intera4va

> O arquivo apps/streamlit_app/app.py implementa um dashboard Streamlit
> completo com nove abas, indo bem além do requisito opcional do brieﬁng
> de uma simples interface de demonstração:

  -----------------------------------------------------------------------
  **Aba**             **Finalidade**
  ------------------- ---------------------------------------------------
  Experiment Metrics  Descobre automaTcamente cada experimento treinado,
                      comparando Precision/ Recall/mAP ao vivo

  Field DetecTons by  Cards, gráﬁco de barras e tabela da validação de
  Region              campo em 10 bairros

  Map                 Mapa Folium em modo escuro com 3 camadas
                      alternáveis, incluindo uma camada de taxa de
                      detecção em escala de azul

  Search by Region    Busca ao vivo por bounding box: baixa Tles e roda
                      inferência sob demanda

  Sample Images       Detecções reais pré-selecionadas para demonstração
                      instantânea

  Upload Image        Upload de qualquer imagem aérea/satélite para
                      detecção anotada

  Pipeline            Passo a passo visual do pipeline completo de 12
                      etapas

  Governance          Declarações de jusTça, LGPD e limitações conhecidas

  Downloads           Relatórios, dataset, métricas e artefatos da
                      validação de campo
  -----------------------------------------------------------------------

> Em linguagem simples: essa aplicação é a "vitrine" do projeto ---
> permite que qualquer pessoa, mesmo sem saber programar, faça upload de
> uma foto de satélite, busque uma região do mapa, ou simplesmente veja
> os resultados já processados, sem precisar rodar nenhum código.
>
> Página 21 de 25
>
> Helipad Detector --- Relatório Completo

# Pontos fortes, limitações e próximos passos

### Pontos fortes

-   Cobertura de ponta a ponta do ciclo de vida de um projeto de visão
    computacional --- da coleta bruta de dados até uma aplicação
    demonstrável;

-   Foco explícito em engenharia de dados, e não apenas em ajustar o
    modelo;

-   Automação geoespacial que aumenta escala e reproduTbilidade da
    coleta;

-   Uma etapa de validação de campo em dados reais, além dos benchmarks
    curados --- algo incomum em projetos acadêmicos deste porte;

-   Uma camada de aplicação interaTva completa, com nove abas
    funcionais.

### Limitações observadas

-   Confusão visual com piscinas e quadras esporTvas conTnua sendo a
    principal fonte de falsos posiTvos;

-   Os resultados dependem da consistência de anotação entre os membros
    da equipe;

-   A capacidade de generalização é limitada pela diversidade de padrões
    de telhado vistos durante o treino;

-   Falhas de download de Tles (Tles vazios) podem gerar detecções
    espúrias na validação de campo.

### Melhorias futuras sugeridas

-   Adicionar mais exemplos negaTvos (piscinas, quadras esporTvas) para
    reduzir falsos posiTvos;

-   Adicionar um ﬁltro automáTco de Tle vazio antes da inferência no
    pipeline de validação de campo;

-   Estender a validação de campo para outros bairros e para a região
    totalmente não vista da Baixada SanTsta;

-   Comparar sistemaTcamente YOLOv8n vs. YOLOv11n nos mesmos splits de
    dataset;

-   Incorporar ciclos de acTve learning, re-anotando os exemplos mais
    di\\ceis idenTﬁcados na validação de campo.

> Página 22 de 25
>
> Helipad Detector --- Relatório Completo

1.  **É4ca, LGPD e governança**

> O projeto segue práTcas-chave de IA responsável, resumidas aqui tanto
> para o leitor técnico quanto para quem está avaliando o projeto do
> ponto de vista de conformidade:

-   Uso exclusivo de imagens de satélite de área pública;

-   Nenhuma anotação de pessoas, placas de veículos ou outros
    idenTﬁcadores pessoais;

-   IA generaTva usada apenas como ferramenta de apoio, com uso
    documentado no relatório;

-   Foco acadêmico e de pesquisa, sem qualquer intenção de vigilância
    individual.

> Na perspecTva da LGPD (Lei Geral de Proteção de Dados), o projeto
> minimiza dados pessoais idenTﬁcáveis, documenta claramente as fontes
> de imagem e sua atribuição obrigatória (Esri, Maxar, Earthstar
> Geographics e a GIS User Community), e restringe o uso dos resultados
> a ﬁns acadêmicos e de pesquisa.

### Incidente de segurança iden4ﬁcado e corrigido

> Durante o desenvolvimento, a equipe idenTﬁcou e corrigiu um problema
> real de segurança: uma chave de API do Roboﬂow estava hardcoded
> (escrita diretamente em texto puro) nos notebooks de treino. A chave
> foi removida do código-fonte, subsTtuída por leitura via variável de
> ambiente / Colab Secrets, e marcada para revogação.
>
> *Em linguagem simples: uma "senha" de acesso ao Roboﬂow estava visível
> para qualquer pessoa que abrisse o notebook --- inclusive em um
> repositório público no GitHub. Isso é um risco real, porque quem visse
> essa chave poderia usá-la para acessar o workspace do projeto. A
> equipe corrigiu o problema movendo a chave para fora do código, um
> exemplo concreto de por que boas práNcas de gestão de segredos
> (secrets management) importam mesmo em projetos acadêmicos, e não só
> em produtos comerciais.*
>
> Como práTca de governança de IA, o repositório prioriza: fontes de
> dados controladas, critérios de anotação claros e documentados,
> reproduTbilidade dos experimentos via notebooks e seeds ﬁxas,
> avaliação de erros estruturada (a análise qualitaTva da Seção 10) e
> documentação explícita das decisões de design tomadas ao longo do
> pipeline --- incluindo o próprio erro de integridade de dados descrito
> na Seção 7.1, manTdo no relatório de forma transparente em vez de
> omiTdo.
>
> Página 23 de 25
>
> Helipad Detector --- Relatório Completo

# Conclusão

> O Helipad Detector aTnge métricas de nível proﬁssional --- mAP@50 de
> aproximadamente 99% e mAP@50-95 de aproximadamente 88% --- em um
> dataset construído inteiramente do zero pela equipe. A etapa de
> validação de campo conﬁrma que esses resultados se sustentam também em
> cobertura real de satélite, sem curadoria prévia, em dez bairros de
> São Paulo, com padrões de erro documentados e explicáveis, em vez de
> falhas opacas.
>
> Isso valida tanto o modelo em si quanto a ênfase mais ampla do
> projeto: qualidade de dado, governança de anotação, reproduTbilidade e
> documentação honesta e baseada em evidências --- inclusive quando
> essas evidências mostram um erro comeTdo e corrigido pela própria
> equipe, como aconteceu na atribuição inicial do exp2/exp3.
>
> Para quem chega até aqui sem experiência técnica em IA, a mensagem
> central deste relatório pode ser resumida assim: construir um bom
> sistema de Inteligência ArTﬁcial não é, na maior parte do tempo, um
> problema de algoritmo --- é um problema de dados bem coletados, bem
> anotados, bem testados e bem documentados. Este projeto é, acima de
> tudo, um exemplo práTco e transparente desse princípio.
>
> Página 24 de 25
>
> Helipad Detector --- Relatório Completo

# Glossário de termos técnicos

> Referência rápida dos termos técnicos usados ao longo deste relatório,
> para consulta a qualquer momento.

  -----------------------------------------------------------------------
  **Termo**           **Signiﬁcado em linguagem simples**
  ------------------- ---------------------------------------------------
  Bounding box        Caixa retangular desenhada ao redor de um objeto em
                      uma imagem, indicando onde ele está.

  Dataset             Conjunto de dados (aqui, imagens + marcações) usado
                      para treinar e testar o modelo.

  Época (epoch)       Uma passagem completa do modelo por todas as
                      imagens de treino.

  Falso NegaTvo (FN)  Quando existe um heliponto real na imagem, mas o
                      modelo não o detecta.

  Falso PosiTvo (FP)  Quando o modelo detecta um heliponto onde, na
                      verdade, não existe nenhum.

  Generalização       Capacidade do modelo de funcionar bem em imagens
                      novas, nunca vistas durante o treino.

  IoU (IntersecTon    Medida de quanto a caixa prevista pelo modelo se
  over Union)         sobrepõe à caixa real do objeto.

  mAP (mean Average   Nota única que resume a qualidade geral das
  Precision)          detecções do modelo, considerando vários limiares
                      de sobreposição.

  OverﬁÉng            Quando o modelo "decora" os exemplos de treino em
                      vez de aprender o padrão geral, funcionando mal em
                      dados novos.

  Precision           De todas as detecções feitas, quantas estavam
  (Precisão)          corretas.

  Recall (Revocação)  De todos os objetos reais existentes, quantos o
                      modelo conseguiu encontrar.

  Tile                Pedaço quadrado e padronizado de uma imagem de
                      mapa/satélite, usado para montar mosaicos maiores.

  YOLO                "You Only Look Once" --- família de modelos de IA
                      para detecção de objetos em tempo real.
  -----------------------------------------------------------------------

*Helipad Detector · PUC-SP · Machine Learning / Visão Computacional ·*

> Página 25 de 25
