# 🇧🇷 Manual — Gerar os Vídeos de Demo (exp1 a exp4, todas as 10 regiões)

<br><br>

## [Antes de Começar]()

<br>

Este manual gera, pra cada um dos 4 experimentos, um vídeo mostrando o modelo detectando helipontos em tiles reais de satélite — não é vídeo de treinamento, é inferência (o modelo já treinado rodando em imagens que ele nunca viu durante o treino).

**Sobre cobrir as 10 regiões:** rodar literalmente todos os ~7.767–7.943 tiles em vídeo ficaria longo demais (a 4 fps, mais de 30 minutos por experimento) e lento pra processar 4 vezes sem GPU. Em vez disso, este manual **amostra um número fixo de tiles de cada uma das 10 regiões** — assim o vídeo passa por todos os bairros, sem virar uma maratona. Os **mesmos tiles exatos** são usados nos 4 experimentos, então a comparação fica justa: mesma cena, modelo diferente.

<br>

### [***Pré-requisitos***]

<br>

- Terminal aberto na raiz do repositório (`3-MAINproject-ai-ml-yolo-helipad_detector`)
- `ffmpeg` instalado (`brew install ffmpeg` no Mac, se ainda não tiver)
- Os 4 pesos já treinados em `artifacts/runs/runs/detect/exp{1,2,3,4}/weights/best.pt`
- Os tiles das 10 regiões já baixados em `src/geospatial/mosaic_*/`

<br><br>

## [Passo 1 — Montar a Amostra (mesmos tiles pros 4 experimentos)]()

<br>

Esse bloco pega `N_PER_REGION` tiles de cada uma das 10 pastas `mosaic_*`, numera o nome do arquivo pela ordem da região (pra o vídeo final passear pelos bairros em sequência, não misturado), e junta tudo numa única pasta de origem.

```bash
cd ~/Desktop/3-MAINproject-ai-ml-yolo-helipad_detector

N_PER_REGION=8   # tiles por bairro — 10 bairros x 8 = 80 frames no vídeo final
SRC=reports/demo_src

rm -rf "$SRC" && mkdir -p "$SRC" reports/demo_frames reports/demo_videos

i=0
for REGION in $(ls -d src/geospatial/mosaic_*/ | sort); do
  i=$((i+1))
  PREFIX=$(printf "%02d" $i)
  REGION_NAME=$(basename "$REGION")
  echo "[$PREFIX] $REGION_NAME"

  # se a pasta só tiver o .zip, descompacta primeiro
  unzip -n "$REGION"*.zip -d "$REGION" 2>/dev/null || true

  ls "$REGION"*.jpg | sort | head -$N_PER_REGION | while read -r TILE; do
    cp "$TILE" "$SRC/${PREFIX}_${REGION_NAME}_$(basename "$TILE")"
  done
done

echo "Total de tiles na amostra:"
ls "$SRC"/*.jpg | wc -l   # deve dar ~80 (ou N_PER_REGION x número de regiões encontradas)
```

<br>

> Quer mais cobertura por bairro? Só aumentar `N_PER_REGION` — o vídeo fica mais longo, mas continua rodando a inferência uma vez só por experimento.

<br><br>

## [Passo 2 — Rodar Inferência nos 4 Experimentos (sobre a mesma amostra)]()

<br>

Como a amostra já está pronta e é pequena (~80 tiles), isso roda rápido mesmo sem GPU.

```bash
for EXP in exp1 exp2 exp3 exp4; do
  echo "=== Rodando $EXP ==="
  python -c "
from ultralytics import YOLO
model = YOLO('artifacts/runs/runs/detect/$EXP/weights/best.pt')
model.predict(source='reports/demo_src', conf=0.25, save=True,
               project='reports/demo_frames', name='$EXP', exist_ok=True)
"
  echo "$EXP: $(ls reports/demo_frames/$EXP/*.jpg | wc -l) frames gerados"
done
```

Confirma que os 4 geraram o mesmo número de frames (o mesmo da amostra do Passo 1) — se algum vier diferente, um dos pesos pode ter falhado ao carregar.

<br><br>

## [Passo 3 — Virar Vídeo (ffmpeg)]()

<br>

```bash
FPS=2   # tiles por segundo — com tiles de 10 bairros diferentes, mais lento ajuda a acompanhar

for EXP in exp1 exp2 exp3 exp4; do
  cd reports/demo_frames/$EXP
  ffmpeg -y -framerate $FPS -pattern_type glob -i '*.jpg' -pix_fmt yuv420p \
    ../../demo_videos/${EXP}_silent.mp4
  cd -
done
```

Nesse ponto você tem 4 vídeos mudos em `reports/demo_videos/`, cada um passeando pelas 10 regiões.

<br><br>

## [Passo 4 — Adicionar a Trilha (Interstellar)]()

<br>

Todos os 4 vídeos de detecção usam a mesma trilha de propósito — como são comparados lado a lado, trocar a música junto com o experimento criaria uma variável confundindo a comparação.

```bash
AUDIO="assets/audio/Interstellar - Deep House Remix.m4a"   # confira o nome exato na sua pasta assets/audio/

for EXP in exp1 exp2 exp3 exp4; do
  ffmpeg -y -i reports/demo_videos/${EXP}_silent.mp4 -i "$AUDIO" \
    -c:v copy -c:a aac -shortest \
    reports/demo_videos/${EXP}_with_audio.mp4
done
```

<br><br>

## [Passo 5 — Renomear pros Nomes Finais]()

<br>

```bash
mkdir -p demo
cp reports/demo_videos/exp1_with_audio.mp4 "demo/Helipad-Detection-exp1-YOLOv8n-Deteccao-em-Tiles-Reais.mp4"
cp reports/demo_videos/exp2_with_audio.mp4 "demo/Helipad-Detection-exp2-YOLOv8n-Deteccao-em-Tiles-Reais.mp4"
cp reports/demo_videos/exp3_with_audio.mp4 "demo/Helipad-Detection-exp3-YOLOv8n-Deteccao-em-Tiles-Reais.mp4"
cp reports/demo_videos/exp4_with_audio.mp4 "demo/Helipad-Detection-exp4-YOLO11n-Deteccao-em-Tiles-Reais.mp4"

ls -la demo/*.mp4
```

<br>

### [***Opcional — limpar arquivos intermediários***]

<br>

Os frames (`reports/demo_frames/`) e a amostra de origem (`reports/demo_src/`) ocupam espaço em disco e não precisam ser versionados. Depois de conferir os vídeos finais:

```bash
rm -rf reports/demo_frames reports/demo_src reports/demo_videos/*_silent.mp4
```

<br><br>

## [Legendas Sugeridas (uma linha por vídeo)]()

<br>

| Vídeo | Legenda |
|---|---|
| exp1 | exp1 (60 épocas, YOLOv8n) — alta Precision no benchmark curado, mas detecta só ~metade dos helipontos reais em campo |
| exp2 | exp2 (100 épocas, YOLOv8n) — modelo em produção, melhor generalização em campo |
| exp3 | exp3 (100 épocas, YOLOv8n, dataset aumentado) — recall mais alto, resultado intermediário em campo |
| exp4 | exp4 (100 épocas, YOLO11n) — mesma base do exp2, arquitetura mais nova; não superou o exp2 em campo |

<br><br>

---

<br><br>

# 🇬🇧 Manual — Generate the Demo Videos (exp1 to exp4, all 10 regions)

<br><br>

## [Before You Start]()

<br>

This manual generates, for each of the 4 experiments, a video showing the model detecting helipads on real satellite tiles — this is not a training video, it's inference (the already-trained model running on images it never saw during training).

**About covering all 10 regions:** running literally every ~7,767–7,943 tiles into video would be far too long (at 4 fps, over 30 minutes per experiment) and slow to process 4 times without a GPU. Instead, this manual **samples a fixed number of tiles from each of the 10 regions** — so the video tours every neighborhood without becoming a marathon. The **exact same tiles** are used across all 4 experiments, keeping the comparison fair: same scene, different model.

<br>

### [***Prerequisites***]

<br>

- Terminal open at the repository root (`3-MAINproject-ai-ml-yolo-helipad_detector`)
- `ffmpeg` installed (`brew install ffmpeg` on Mac, if you don't have it yet)
- All 4 trained weights at `artifacts/runs/runs/detect/exp{1,2,3,4}/weights/best.pt`
- Tiles for all 10 regions already downloaded at `src/geospatial/mosaic_*/`

<br><br>

## [Step 1 — Build the Sample (same tiles for all 4 experiments)]()

<br>

This block grabs `N_PER_REGION` tiles from each of the 10 `mosaic_*` folders, numbers the filename by region order (so the final video tours the neighborhoods in sequence, not shuffled), and collects everything into one source folder.

```bash
cd ~/Desktop/3-MAINproject-ai-ml-yolo-helipad_detector

N_PER_REGION=8   # tiles per neighborhood — 10 neighborhoods x 8 = 80 frames in the final video
SRC=reports/demo_src

rm -rf "$SRC" && mkdir -p "$SRC" reports/demo_frames reports/demo_videos

i=0
for REGION in $(ls -d src/geospatial/mosaic_*/ | sort); do
  i=$((i+1))
  PREFIX=$(printf "%02d" $i)
  REGION_NAME=$(basename "$REGION")
  echo "[$PREFIX] $REGION_NAME"

  # if the folder only has the .zip, unpack it first
  unzip -n "$REGION"*.zip -d "$REGION" 2>/dev/null || true

  ls "$REGION"*.jpg | sort | head -$N_PER_REGION | while read -r TILE; do
    cp "$TILE" "$SRC/${PREFIX}_${REGION_NAME}_$(basename "$TILE")"
  done
done

echo "Total tiles in the sample:"
ls "$SRC"/*.jpg | wc -l   # should be ~80 (or N_PER_REGION x number of regions found)
```

<br>

> Want more coverage per neighborhood? Just increase `N_PER_REGION` — the video gets longer, but inference still runs only once per experiment.

<br><br>

## [Step 2 — Run Inference on All 4 Experiments (over the same sample)]()

<br>

Since the sample is already built and small (~80 tiles), this runs fast even without a GPU.

```bash
for EXP in exp1 exp2 exp3 exp4; do
  echo "=== Running $EXP ==="
  python -c "
from ultralytics import YOLO
model = YOLO('artifacts/runs/runs/detect/$EXP/weights/best.pt')
model.predict(source='reports/demo_src', conf=0.25, save=True,
               project='reports/demo_frames', name='$EXP', exist_ok=True)
"
  echo "$EXP: $(ls reports/demo_frames/$EXP/*.jpg | wc -l) frames generated"
done
```

Confirm all 4 generated the same frame count (matching Step 1's sample) — if one comes out different, one of the weight files may have failed to load.

<br><br>

## [Step 3 — Turn Into Video (ffmpeg)]()

<br>

```bash
FPS=2   # tiles per second — with tiles from 10 different neighborhoods, slower helps viewers follow along

for EXP in exp1 exp2 exp3 exp4; do
  cd reports/demo_frames/$EXP
  ffmpeg -y -framerate $FPS -pattern_type glob -i '*.jpg' -pix_fmt yuv420p \
    ../../demo_videos/${EXP}_silent.mp4
  cd -
done
```

At this point you have 4 silent videos in `reports/demo_videos/`, each touring all 10 regions.

<br><br>

## [Step 4 — Add the Soundtrack (Interstellar)]()

<br>

All 4 detection videos deliberately share the same track — since they're compared side by side, changing the music along with the experiment would introduce a variable that confounds the comparison.

```bash
AUDIO="assets/audio/Interstellar - Deep House Remix.m4a"   # check the exact filename in your assets/audio/ folder

for EXP in exp1 exp2 exp3 exp4; do
  ffmpeg -y -i reports/demo_videos/${EXP}_silent.mp4 -i "$AUDIO" \
    -c:v copy -c:a aac -shortest \
    reports/demo_videos/${EXP}_with_audio.mp4
done
```

<br><br>

## [Step 5 — Rename to Final Filenames]()

<br>

```bash
mkdir -p demo
cp reports/demo_videos/exp1_with_audio.mp4 "demo/Helipad-Detection-exp1-YOLOv8n-Deteccao-em-Tiles-Reais.mp4"
cp reports/demo_videos/exp2_with_audio.mp4 "demo/Helipad-Detection-exp2-YOLOv8n-Deteccao-em-Tiles-Reais.mp4"
cp reports/demo_videos/exp3_with_audio.mp4 "demo/Helipad-Detection-exp3-YOLOv8n-Deteccao-em-Tiles-Reais.mp4"
cp reports/demo_videos/exp4_with_audio.mp4 "demo/Helipad-Detection-exp4-YOLO11n-Deteccao-em-Tiles-Reais.mp4"

ls -la demo/*.mp4
```

<br>

### [***Optional — clean up intermediate files***]

<br>

The frames (`reports/demo_frames/`) and source sample (`reports/demo_src/`) take up disk space and don't need to be version-controlled. Once you've checked the final videos:

```bash
rm -rf reports/demo_frames reports/demo_src reports/demo_videos/*_silent.mp4
```

<br><br>

## [Suggested Captions (one line per video)]()

<br>

| Video | Caption |
|---|---|
| exp1 | exp1 (60 epochs, YOLOv8n) — high Precision on the curated benchmark, but detects only ~half the real helipads in the field |
| exp2 | exp2 (100 epochs, YOLOv8n) — the production model, best field generalization |
| exp3 | exp3 (100 epochs, YOLOv8n, augmented dataset) — higher recall, mid-pack field result |
| exp4 | exp4 (100 epochs, YOLO11n) — same base as exp2, newer architecture; did not outperform exp2 in the field |
