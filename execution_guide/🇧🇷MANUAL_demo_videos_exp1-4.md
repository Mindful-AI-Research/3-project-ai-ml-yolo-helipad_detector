# 🇧🇷 Manual — Geração dos Vídeos de Demonstração

**Detecção de Helipads · YOLOv8n / YOLO11n · São Paulo**

\<br>

## Índice

\<br>

- [1. Objective](https://chatgpt.com/c/6ac2eb7f-1ef0-83e8-ba59-beda6da05236#1-objective)
- [2. Experimental Methodology](https://chatgpt.com/c/6ac2eb7f-1ef0-83e8-ba59-beda6da05236#2-experimental-methodology)
  - [2.1 Controlled Sampling](https://chatgpt.com/c/6ac2eb7f-1ef0-83e8-ba59-beda6da05236#21-controlled-sampling)
  - [2.2 Comparability](https://chatgpt.com/c/6ac2eb7f-1ef0-83e8-ba59-beda6da05236#22-comparability)
- [3. Prerequisites](https://chatgpt.com/c/6ac2eb7f-1ef0-83e8-ba59-beda6da05236#3-prerequisites)
  - [FFmpeg — macOS](https://chatgpt.com/c/6ac2eb7f-1ef0-83e8-ba59-beda6da05236#ffmpeg--macos)
- [4. Generation Pipeline](https://chatgpt.com/c/6ac2eb7f-1ef0-83e8-ba59-beda6da05236#4-generation-pipeline)
- [5. Step 1 — Build the Tile Sample](https://chatgpt.com/c/6ac2eb7f-1ef0-83e8-ba59-beda6da05236#5-step-1--build-the-tile-sample)
- [6. Step 2 — Run Inference for the Four Experiments](https://chatgpt.com/c/6ac2eb7f-1ef0-83e8-ba59-beda6da05236#6-step-2--run-inference-for-the-four-experiments)
  - [Consistency Check](https://chatgpt.com/c/6ac2eb7f-1ef0-83e8-ba59-beda6da05236#consistency-check)
- [7. Step 3 — Convert Frames to Video](https://chatgpt.com/c/6ac2eb7f-1ef0-83e8-ba59-beda6da05236#7-step-3--convert-frames-to-video)
- [8. Step 4 — Add the Soundtrack](https://chatgpt.com/c/6ac2eb7f-1ef0-83e8-ba59-beda6da05236#8-step-4--add-the-soundtrack)
- [9. Step 5 — Create the Final Demo Videos](https://chatgpt.com/c/6ac2eb7f-1ef0-83e8-ba59-beda6da05236#9-step-5--create-the-final-demo-videos)
- [10. Experiment Captions](https://chatgpt.com/c/6ac2eb7f-1ef0-83e8-ba59-beda6da05236#10-experiment-captions)
- [11. Demo 5 — Automated Helipad Scraping](https://chatgpt.com/c/6ac2eb7f-1ef0-83e8-ba59-beda6da05236#11-demo-5--automated-helipad-scraping)
- [12. Clean Up Intermediate Files](https://chatgpt.com/c/6ac2eb7f-1ef0-83e8-ba59-beda6da05236#12-clean-up-intermediate-files)
- [13. Final Output](https://chatgpt.com/c/6ac2eb7f-1ef0-83e8-ba59-beda6da05236#13-final-output)
  - [Comparability Criterion](https://chatgpt.com/c/6ac2eb7f-1ef0-83e8-ba59-beda6da05236#comparability-criterion)

\<br>\<br>

## 1. Objetivo

Este manual documenta o procedimento utilizado para gerar os vídeos de demonstração dos quatro experimentos de detecção de helipads:

- `exp1` — YOLOv8n
- `exp2` — YOLOv8n
- `exp3` — YOLOv8n + augmented dataset
- `exp4` — YOLO11n

Os vídeos apresentam a **inferência dos modelos sobre tiles reais de imagens de satélite**, permitindo inspecionar visualmente o comportamento de cada modelo treinado em imagens que não foram utilizadas durante o treinamento.

> **Importante:** estes vídeos representam **inferência**, e não treinamento.

Os quatro vídeos de detecção são apresentados como:

- **🎥 Demo 1** — `exp1`
- **🎥 Demo 2** — `exp2`
- **🎥 Demo 3** — `exp3`
- **🎥 Demo 4** — `exp4`

Uma quinta demonstração apresenta o processo automatizado de coleta de dados geoespaciais:

- **🎥 Demo 5** — Automated Helipad Scraping

\<br>

---

## 2. Metodologia Experimental

### 2.1 Amostragem Controlada

O conjunto de dados geoespaciais contém aproximadamente **7.767–7.943 tiles**, dependendo da versão do dataset. Executar a inferência em todos os tiles e converter o conjunto completo em vídeo produziria demonstrações excessivamente longas e aumentaria significativamente o tempo de processamento.

Para as demonstrações, um **número fixo de tiles é amostrado de cada uma das 10 regiões**.

With the default configuration:

```
10 regions × 8 tiles per region = 80 tiles
```

A amostra é criada **uma única vez** e reutilizada nos quatro experimentos de detecção.

### 2.2 Comparabilidade

Usar a mesma amostra garante que:

- all four models receive the same images;
- the analyzed regions are identical;
- the presentation order remains consistent;
- the soundtrack is identical;
- observed differences can be attributed to model behavior.

Em outras palavras:

> **Mesma cena. Modelo diferente.**

Isso impede que a seleção das imagens se torne uma variável adicional na comparação visual.

\<br>

---

## 3. Pré-requisitos

Antes de começar, confirme que:

- the repository is located at `3-MAINproject-ai-ml-yolo-helipad_detector`;
- `ffmpeg` is installed;
- the Python environment is configured;
- the `ultralytics` package is available;
- the four trained weights are available at:

```
artifacts/runs/runs/detect/
├── exp1/weights/best.pt
├── exp2/weights/best.pt
├── exp3/weights/best.pt
└── exp4/weights/best.pt
```

- the regional satellite tiles are available under:

```
src/geospatial/mosaic_*/
```

- the required audio files are available under:

```
assets/audio/
```

### FFmpeg — macOS

Se necessário:

```
brew install ffmpeg
```

\<br>

---

## 4. Pipeline de Geração

O fluxo de trabalho completo é:

```
Real Satellite Tiles
        │
        ▼
Controlled Sample
10 Regions
        │
        ▼
Inference
exp1 · exp2 · exp3 · exp4
        │
        ▼
Annotated Frames
        │
        ▼
Silent MP4 Videos
        │
        ▼
Common Soundtrack
        │
        ▼
Demo 1 · Demo 2 · Demo 3 · Demo 4
```

A demonstração de scraping segue um fluxo separado:

```
Automated Data Collection
        │
        ▼
Selenium / helipad_bot.py
        │
        ▼
Helipad Coordinates
        │
        ▼
Demo 5
        │
        ▼
Soundtrack
```

> **Demo 1–4** demonstram a inferência dos modelos.
> **Demo 5** demonstra a coleta automatizada de dados de helipads.

\<br>

---

## 5. Etapa 1 — Criar a Amostra de Tiles

Defina o número de tiles selecionados de cada região:

```
cd ~/Desktop/3-MAINproject-ai-ml-yolo-helipad_detector

N_PER_REGION=8
SRC=reports/demo_src

rm -rf "$SRC"
rm -rf reports/demo_frames
mkdir -p "$SRC" reports/demo_frames reports/demo_videos
```

> A remoção de `reports/demo_frames` antes da inferência é intencional. Isso impede que frames de uma execução anterior sejam misturados à amostra atual.

Build the controlled sample:

```
i=0

for REGION in $(ls -d src/geospatial/mosaic_*/ | sort); do
  i=$((i+1))
  PREFIX=$(printf "%02d" $i)
  REGION_NAME=$(basename "$REGION")

  echo "[$PREFIX] $REGION_NAME"

  # Extract tiles if the region still contains ZIP archives.
  unzip -n "$REGION"*.zip -d "$REGION" 2>/dev/null || true

  ls "$REGION"*.jpg | sort | head -$N_PER_REGION | while read -r TILE; do
    cp "$TILE" "$SRC/${PREFIX}_${REGION_NAME}_$(basename "$TILE")"
  done
done

echo "Total tiles:"
ls "$SRC"/*.jpg | wc -l
```

Com `N_PER_REGION=8`, o tamanho esperado da amostra é:

```
80 tiles
```

Para criar uma demonstração mais longa, aumente o valor:

```
N_PER_REGION=12
```

> **Não altere a amostra entre os experimentos.** O mesmo diretório `reports/demo_src/` deve ser utilizado para `exp1`, `exp2`, `exp3` e `exp4`.

\<br>

---

## 6. Etapa 2 — Executar a Inferência para os Quatro Experimentos

Execute a inferência sobre a mesma amostra:

```
for EXP in exp1 exp2 exp3 exp4; do
  echo "=== Running $EXP ==="

  python -c "
from ultralytics import YOLO

model = YOLO(
    'artifacts/runs/runs/detect/$EXP/weights/best.pt'
)

model.predict(
    source='reports/demo_src',
    conf=0.25,
    save=True,
    project='reports/demo_frames',
    name='$EXP',
    exist_ok=True
)
"

  echo "$EXP: $(ls reports/demo_frames/$EXP/*.jpg | wc -l) frames"
done
```

A estrutura resultante será:

```
reports/demo_frames/
├── exp1/
├── exp2/
├── exp3/
└── exp4/
```

Cada diretório contém os frames anotados gerados pelo respectivo modelo.

### Verificação de Consistência

Os quatro experimentos devem gerar o mesmo número de frames.

Para uma amostra de 80 tiles:

```
exp1 → 80 frames
exp2 → 80 frames
exp3 → 80 frames
exp4 → 80 frames
```

Se as quantidades de frames forem diferentes, pare e investigue antes de prosseguir para a geração dos vídeos.

\<br>

---

## 7. Etapa 3 — Converter Frames em Vídeo

Converta os frames anotados em vídeos MP4 usando `ffmpeg`.

Recomenda-se uma taxa de **2 FPS** para que as detecções permaneçam visíveis por tempo suficiente para inspeção visual.

```
FPS=2

for EXP in exp1 exp2 exp3 exp4; do
  cd reports/demo_frames/$EXP

  ffmpeg -y \
    -framerate $FPS \
    -pattern_type glob \
    -i '*.jpg' \
    -pix_fmt yuv420p \
    ../../demo_videos/${EXP}_silent.mp4

  cd -
done
```

Os vídeos intermediários serão criados em:

```
reports/demo_videos/
├── exp1_silent.mp4
├── exp2_silent.mp4
├── exp3_silent.mp4
└── exp4_silent.mp4
```

\<br>

---

## 8. Etapa 4 — Adicionar a Trilha Sonora

Os quatro vídeos de inferência utilizam a **mesma trilha sonora**.

Isso é intencional: como os vídeos são utilizados para comparar visualmente os quatro modelos, a trilha sonora deve permanecer constante e não deve introduzir uma variável experimental adicional.

```
AUDIO="assets/audio/Interstellar - Deep House Remix.m4a"

for EXP in exp1 exp2 exp3 exp4; do
  ffmpeg -y \
    -i reports/demo_videos/${EXP}_silent.mp4 \
    -i "$AUDIO" \
    -c:v copy \
    -c:a aac \
    -shortest \
    reports/demo_videos/${EXP}_with_audio.mp4
done
```

> Confirme o nome exato do arquivo em `assets/audio/` antes de executar o comando.

Os arquivos resultantes são:

```
reports/demo_videos/
├── exp1_with_audio.mp4
├── exp2_with_audio.mp4
├── exp3_with_audio.mp4
└── exp4_with_audio.mp4
```

\<br>

---

## 9. Etapa 5 — Criar os Vídeos Finais de Demonstração

Crie o diretório `demo/`:

```
mkdir -p demo
```

Copie os vídeos finais utilizando nomes de arquivo descritivos.

Os nomes dos arquivos incluem intencionalmente o **número da Demo**, a **finalidade da inferência**, o **experimento**, o **modelo** e a configuração relevante. Como o GitHub exibe o nome do arquivo do vídeo acima do player incorporado, essa convenção de nomenclatura também funciona como o título visual de cada demonstração.

```
cp reports/demo_videos/exp1_with_audio.mp4 \
  "demo/🎥 Demo 1 — Inference — Helipad Detection · exp1 · YOLOv8n · 60 epochs.mp4"

cp reports/demo_videos/exp2_with_audio.mp4 \
  "demo/🎥 Demo 2 — Inference — Helipad Detection · exp2 · YOLOv8n · 100 epochs.mp4"

cp reports/demo_videos/exp3_with_audio.mp4 \
  "demo/🎥 Demo 3 — Inference — Helipad Detection · exp3 · YOLOv8n · 100 epochs · Augmented Dataset.mp4"

cp reports/demo_videos/exp4_with_audio.mp4 \
  "demo/🎥 Demo 4 — Inference — Helipad Detection · exp4 · YOLO11n · 100 epochs.mp4"
```

Verifique os arquivos finais:

```
ls -lh demo/*.mp4
```

Os quatro arquivos agora devem ser:

```
demo/
├── 🎥 Demo 1 — Inference — Helipad Detection · exp1 · YOLOv8n · 60 epochs.mp4
├── 🎥 Demo 2 — Inference — Helipad Detection · exp2 · YOLOv8n · 100 epochs.mp4
├── 🎥 Demo 3 — Inference — Helipad Detection · exp3 · YOLOv8n · 100 epochs · Augmented Dataset.mp4
└── 🎥 Demo 4 — Inference — Helipad Detection · exp4 · YOLO11n · 100 epochs.mp4
```

<br><br>



## 10. Legendas dos Experimentos

| Demo       | Experimento | Descrição                                                                                                                                             |
| ---------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Demo 1** | `exp1`     | **YOLOv8n · 60 epochs** — alta precisão no benchmark curado, mas menor cobertura dos helipads observados em condições de campo.                       |
| **Demo 2** | `exp2`     | **YOLOv8n · 100 epochs** — modelo de referência, com a melhor generalização observada em condições de campo.                                         |
| **Demo 3** | `exp3`     | **YOLOv8n · 100 epochs · Augmented Dataset** — maior recall, com desempenho intermediário em campo.                                                  |
| **Demo 4** | `exp4`     | **YOLO11n · 100 epochs** — mesma base experimental de `exp2`, utilizando uma arquitetura mais recente, mas sem superar `exp2` na avaliação de campo. |


<br>


> Mantenha estas descrições consistentes com os resultados apresentados na análise experimental final do projeto.

<br><br>

## 11. Demo 5 — Scraping Automatizado de Helipads

A **Demo 5** é independente das quatro demonstrações de inferência dos modelos.

Ela apresenta a **coleta automatizada de coordenadas de helipads** utilizando Selenium e `helipad_bot.py`.

Portanto, ela **não** utiliza o pipeline de inferência descrito nas Etapas 5–9.

O objetivo da Demo 5 é documentar a etapa de aquisição de dados geoespaciais do projeto.

### Adicionar a Trilha Sonora

```
cd ~/Desktop/3-MAINproject-ai-ml-yolo-helipad_detector

SCRAPING_VIDEO="demo/🚁Automated Helipad Scraping Demo.mp4"
SCRAPING_AUDIO="assets/audio/feel-good_nina-simone_house remix.mp3"

ffmpeg -y \
  -i "$SCRAPING_VIDEO" \
  -i "$SCRAPING_AUDIO" \
  -c:v copy \
  -c:a aac \
  -shortest \
  "demo/🎥 Demo 5 — Automated Helipad Scraping · Selenium · Coordinate Collection.mp4"
```

Isso cria uma nova versão do vídeo, preservando a demonstração original de scraping.

O diretório final, portanto, conterá:

```
demo/
├── 🎥 Demo 1 — Inference — Helipad Detection · exp1 · YOLOv8n · 60 epochs.mp4
├── 🎥 Demo 2 — Inference — Helipad Detection · exp2 · YOLOv8n · 100 epochs.mp4
├── 🎥 Demo 3 — Inference — Helipad Detection · exp3 · YOLOv8n · 100 epochs · Augmented Dataset.mp4
├── 🎥 Demo 4 — Inference — Helipad Detection · exp4 · YOLO11n · 100 epochs.mp4
└── 🎥 Demo 5 — Automated Helipad Scraping · Selenium · Coordinate Collection.mp4
```

> [!TIP]
> Se o vídeo original de scraping já contiver narração ou outra faixa de áudio, o comando acima substituirá o áudio existente. Para preservar e mixar ambas as fontes de áudio, use `amix`.

<br>



## 12. Limpar Arquivos Intermediários

Após verificar os cinco vídeos finais, os arquivos intermediários podem ser removidos:

```
rm -rf reports/demo_frames
rm -rf reports/demo_src
rm -f reports/demo_videos/*_silent.mp4
```

Os vídeos finais em `demo/` são preservados.

> **Não execute esta limpeza antes de verificar os vídeos finais.**

<br>


## 13. Saída Final

Após concluir todo o fluxo de trabalho, o diretório `demo/` deverá conter exatamente cinco demonstrações finais:

```
demo/
├── 🎥 Demo 1 — Inference — Helipad Detection · exp1 · YOLOv8n · 60 epochs.mp4
├── 🎥 Demo 2 — Inference — Helipad Detection · exp2 · YOLOv8n · 100 epochs.mp4
├── 🎥 Demo 3 — Inference — Helipad Detection · exp3 · YOLOv8n · 100 epochs · Augmented Dataset.mp4
├── 🎥 Demo 4 — Inference — Helipad Detection · exp4 · YOLO11n · 100 epochs.mp4
└── 🎥 Demo 5 — Automated Helipad Scraping · Selenium · Coordinate Collection.mp4
```

### Critério de Comparabilidade

Para as **Demo 1–4**, a validade da comparação visual depende da manutenção de três elementos constantes:

**mesmas imagens de entrada · mesma ordem · mesma trilha sonora**

A variável experimental que muda entre as quatro demonstrações de inferência é o **modelo utilizado para a inferência**.

> **Mesma cena. Modelo diferente.**

**Demo 5 is intentionally excluded from this model comparison**, because it documents automated data collection rather than model inference.
