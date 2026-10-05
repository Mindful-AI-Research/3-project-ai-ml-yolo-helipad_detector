# 🇧🇷 Manual — Gerar os Vídeos de Demo (exp1 a exp4, todas as 10 regiões)

<br><br>

## [Antes de Começar]()

<br>

Este manual gera, pra cada um dos 4 experimentos, um vídeo mostrando o modelo detectando helipontos em tiles reais de satélite — não é vídeo de treinamento, é inferência (o modelo já treinado rodando em imagens que ele nunca viu durante o treino).

**Sobre cobrir as 10 regiões:** rodar literalmente todos os ~7.767–7.943 tiles em vídeo ficaria longo demais (a 4 fps, mais de 30 minutos por experimento) e lento pra processar 4 vezes sem GPU. Em vez disso, este manual **amostra um número fixo de tiles de cada uma das 10 regiões** — assim o vídeo passa por todos os bairros, sem virar uma maratona. Os **mesmos tiles exatos** são usados nos 4 experimentos, então a comparação fica justa: mesma cena, modelo diferente.

<br>

### [***Pré-requisitos***]

<br>

- Terminal aberto na raiz do repositório (`3-project-ai-ml-yolo-helipad_detector`)
- `ffmpeg` instalado (`brew install ffmpeg` no Mac, se ainda não tiver)
- Os 4 pesos já treinados em `artifacts/runs/runs/detect/exp{1,2,3,4}/weights/best.pt`
- Os tiles das 10 regiões já baixados em `src/geospatial/mosaic_*/`

<br><br>

## [Passo 1 — Montar a Amostra (mesmos tiles pros 4 experimentos)]()

<br>

Esse bloco pega `N_PER_REGION` tiles de cada uma das 10 pastas `mosaic_*`, numera o nome do arquivo pela ordem da região (pra o vídeo final passear pelos bairros em sequência, não misturado), e junta tudo numa única pasta de origem.

```bash
cd ~/Desktop/3-project-ai-ml-yolo-helipad_detector

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

### [***Opcional — limpar arquivos intermediários***]()

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

## [Passo 6 — Trilha no Vídeo de Scraping (Automated Helipad Scraping Demo)]()

<br>

Esse vídeo é sobre a raspagem de coordenadas (Selenium / `helipad_bot.py`), não é inferência de modelo — não passa pelos passos 1 a 5 acima. É só adicionar a trilha.

```bash
cd ~/Desktop/3-project-ai-ml-yolo-helipad_detector

SCRAPING_VIDEO="demo/🚁Automated Helipad Scraping Demo.mp4"   # ajuste o caminho se o arquivo estiver em outra pasta
SCRAPING_AUDIO="assets/audio/feel-good_nina-simone_house remix.mp3"   # confira o nome exato na sua pasta assets/audio/

ffmpeg -y -i "$SCRAPING_VIDEO" -i "$SCRAPING_AUDIO" \
  -c:v copy -c:a aac -shortest \
  "demo/🚁Automated-Helipad-Scraping-Demo-com-trilha.mp4"
```

<br>

Isso gera uma cópia nova do vídeo, já com áudio, sem sobrescrever o arquivo mudo original. Confere o resultado antes de apagar o antigo.

<br>

> [!TIP]
> Se o vídeo original já tiver algum áudio (narração, etc.), o comando acima substituirá o áudio inteiro pela trilha. Se quiser **misturar** a trilha por baixo de um áudio já existente, o comando muda (precisa de `amix` em vez de `-shortest` direto).

