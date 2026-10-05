# 🇧🇷 [Manual — Geração de Vídeos de Demonstração](#-manual--geração-de-vídeos-de-demonstração)

**[Detecção de Helipontos · YOLOv8n / YOLO11n · São Paulo](#1-objetivo)**

<br>

##  [Sumário](#-sumário)

<br>

- [1. Objetivo](#1-objetivo)
- [2. Metodologia Experimental](#2-metodologia-experimental)
  - [2.1 Amostragem Controlada](#21-amostragem-controlada)
  - [2.2 Comparabilidade](#22-comparabilidade)
- [3. Pré-requisitos](#3-pré-requisitos)
  - [FFmpeg — macOS](#ffmpeg--macos)
- [4. Pipeline de Geração](#4-pipeline-de-geração)
- [5. Etapa 1 — Construir a Amostra de Tiles](#5-etapa-1--construir-a-amostra-de-tiles)
- [6. Etapa 2 — Executar a Inferência para os Quatro Experimentos](#6-etapa-2--executar-a-inferência-para-os-quatro-experimentos)
  - [Verificação de Consistência](#verificação-de-consistência)
- [7. Etapa 3 — Converter Frames em Vídeo](#7-etapa-3--converter-frames-em-vídeo)
- [8. Etapa 4 — Adicionar a Trilha Sonora](#8-etapa-4--adicionar-a-trilha-sonora)
- [9. Etapa 5 — Criar os Arquivos Finais](#9-etapa-5--criar-os-arquivos-finais)
- [10. Legendas dos Experimentos](#10-legendas-dos-experimentos)
- [11. Demonstração Adicional — Scraping Automatizado de Helipontos](#11-demonstração-adicional--scraping-automatizado-de-helipontos)
- [12. Limpeza dos Arquivos Intermediários](#12-limpeza-dos-arquivos-intermediários)
- [13. Resultado Final](#13-resultado-final)
  - [Critério de Comparabilidade](#critério-de-comparabilidade)

<br><br>

## [1. Objetivo](#1-objetivo)

<br>

Este manual documenta o procedimento usado para gerar vídeos de demonstração dos quatro experimentos de detecção de helipontos:

<br>

- `exp1` — YOLOv8n
- `exp2` — YOLOv8n
- `exp3` — YOLOv8n + conjunto de dados aumentado
- `exp4` — YOLO11n

<br>

Os vídeos apresentam a **inferência do modelo em tiles reais de imagens de satélite**, permitindo que o comportamento de cada modelo seja inspecionado visualmente em imagens que não foram utilizadas durante o treinamento.

<br>

> **Importante:** estes vídeos representam a **inferência**, e não o treinamento.

<br><br>

## [2. Metodologia Experimental](#2-metodologia-experimental)

<br>

### [2.1 Amostragem Controlada](#21-amostragem-controlada)

<br>

O conjunto de dados geoespaciais contém aproximadamente **7.767–7.943 tiles**, dependendo da versão do conjunto de dados. Executar a inferência em todos os tiles e converter o conjunto completo em vídeo produziria demonstrações excessivamente longas e aumentaria significativamente o custo computacional.

<br>

Para a demonstração, é utilizada uma **amostra fixa de tiles por região**.

<br>

Com a configuração padrão:

<br>

```text
10 regiões × 8 tiles por região = 80 tiles
```

<br>

A amostra é criada **uma única vez** e reutilizada nos quatro experimentos.

<br>

### [2.2 Comparabilidade](#22-comparabilidade)

<br>

O uso da mesma amostra garante que:

<br>

- os quatro modelos recebam as mesmas imagens;
- as regiões analisadas sejam idênticas;
- a ordem de apresentação permaneça consistente;
- a trilha sonora seja a mesma;
- as diferenças observadas possam ser atribuídas ao comportamento do modelo.

<br>

Em outras palavras:

<br>

> **Mesma cena, modelo diferente.**

<br>

Esse procedimento impede que a seleção das imagens se torne uma variável adicional na comparação visual dos experimentos.

<br><br>

## [3. Pré-requisitos](#3-pré-requisitos)

<br>

Antes de começar, confirme que:

<br>

- o repositório está localizado em `3-project-ai-ml-yolo-helipad_detector`;
- o `ffmpeg` está instalado;
- o ambiente Python está configurado;
- o pacote `ultralytics` está disponível;
- os pesos treinados estão disponíveis em:

<br>

```text
artifacts/runs/runs/detect/
├── exp1/weights/best.pt
├── exp2/weights/best.pt
├── exp3/weights/best.pt
└── exp4/weights/best.pt
```

<br>

- os tiles regionais estão disponíveis em:

<br>

```text
src/geospatial/mosaic_*/
```

<br>

### [FFmpeg — macOS](#ffmpeg--macos)

<br>

Se necessário:

<br>

```bash
brew install ffmpeg
```

<br><br>

## [4. Pipeline de Geração](#4-pipeline-de-geração)

<br>

O processo completo segue quatro etapas principais:

<br>

```text
Tiles Reais de Satélite
        │
        ▼
Amostra Controlada
10 Regiões
        │
        ▼
Inferência
exp1 · exp2 · exp3 · exp4
        │
        ▼
Frames Anotados
        │
        ▼
Vídeos MP4
        │
        ▼
Trilha Sonora Comum
        │
        ▼
Demonstrações Finais
```

<br><br>

## [5. Etapa 1 — Construir a Amostra de Tiles](#5-etapa-1--construir-a-amostra-de-tiles)

<br>

Defina o número de tiles selecionados de cada região:

<br>

```bash
cd ~/Desktop/3-project-ai-ml-yolo-helipad_detector

N_PER_REGION=8
SRC=reports/demo_src

rm -rf "$SRC"
mkdir -p "$SRC" reports/demo_frames reports/demo_videos
```

<br>

Em seguida, construa a amostra:

<br>

```bash
i=0

for REGION in $(ls -d src/geospatial/mosaic_*/ | sort); do
  i=$((i+1))
  PREFIX=$(printf "%02d" $i)
  REGION_NAME=$(basename "$REGION")

  echo "[$PREFIX] $REGION_NAME"

  # Extrai os tiles caso a região ainda contenha arquivos ZIP.
  unzip -n "$REGION"*.zip -d "$REGION" 2>/dev/null || true

  ls "$REGION"*.jpg | sort | head -$N_PER_REGION | while read -r TILE; do
    cp "$TILE" "$SRC/${PREFIX}_${REGION_NAME}_$(basename "$TILE")"
  done
done

echo "Total de tiles:"
ls "$SRC"/*.jpg | wc -l
```

<br>

Com `N_PER_REGION=8`, o resultado esperado é aproximadamente:

<br>

```text
80 tiles
```

<br>

Aumente `N_PER_REGION` caso seja necessária uma demonstração mais longa:

<br>

```bash
N_PER_REGION=12
```

<br>

> **Não altere a amostra entre os experimentos.** O mesmo diretório `reports/demo_src/` deve ser usado por `exp1`, `exp2`, `exp3` e `exp4`.

<br><br>

## [6. Etapa 2 — Executar a Inferência para os Quatro Experimentos](#6-etapa-2--executar-a-inferência-para-os-quatro-experimentos)

<br>

Execute a inferência na mesma amostra:

<br>

```bash
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

<br>

A estrutura resultante será:

<br>

```text
reports/demo_frames/
├── exp1/
├── exp2/
├── exp3/
└── exp4/
```

<br>

Cada diretório contém os frames anotados gerados pelo modelo correspondente.

<br>

### [Verificação de Consistência](#verificação-de-consistência)

<br>

Os quatro experimentos devem gerar a mesma quantidade de frames.

<br>

Para uma amostra de 80 tiles:

<br>

```text
exp1 → 80 frames
exp2 → 80 frames
exp3 → 80 frames
exp4 → 80 frames
```

<br>

Uma diferença na quantidade de frames indica que a execução deve ser verificada antes de gerar os vídeos.

<br><br>

## [7. Etapa 3 — Converter Frames em Vídeo](#7-etapa-3--converter-frames-em-vídeo)

<br>

Use o `ffmpeg` para converter os frames anotados em vídeos MP4.

<br>

Uma taxa de **2 FPS** é recomendada para que as detecções permaneçam claramente visíveis.

<br>

```bash
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

<br>

Os vídeos intermediários serão criados em:

<br>

```text
reports/demo_videos/
├── exp1_silent.mp4
├── exp2_silent.mp4
├── exp3_silent.mp4
└── exp4_silent.mp4
```

<br><br>

## [8. Etapa 4 — Adicionar a Trilha Sonora](#8-etapa-4--adicionar-a-trilha-sonora)

<br>

Todos os quatro vídeos utilizam a **mesma trilha sonora**.

<br>

Essa padronização é intencional: como o objetivo é comparar visualmente o comportamento dos modelos, a trilha sonora não deve introduzir uma variável adicional entre os experimentos.

<br>

```bash
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

<br>

> Confirme o nome exato do arquivo em `assets/audio/` antes de executar o comando.

<br><br>

<br>

## [9. Etapa 5 — Criar os Arquivos Finais](#9-etapa-5--criar-os-arquivos-finais)

<br>

Crie o diretório de demonstração:

<br>

```bash
mkdir -p demo
```

<br>

Copie os vídeos finais:

<br>

```bash
cp reports/demo_videos/exp1_with_audio.mp4 \
  "demo/Helipad-Detection-exp1-YOLOv8n-Deteccao-em-Tiles-Reais.mp4"

cp reports/demo_videos/exp2_with_audio.mp4 \
  "demo/Helipad-Detection-exp2-YOLOv8n-Deteccao-em-Tiles-Reais.mp4"

cp reports/demo_videos/exp3_with_audio.mp4 \
  "demo/Helipad-Detection-exp3-YOLOv8n-Deteccao-em-Tiles-Reais.mp4"

cp reports/demo_videos/exp4_with_audio.mp4 \
  "demo/Helipad-Detection-exp4-YOLO11n-Deteccao-em-Tiles-Reais.mp4"
```

<br>

Verifique os arquivos:

<br>

```bash
ls -lh demo/*.mp4
```

<br><br>

## [10. Legendas dos Experimentos](#10-legendas-dos-experimentos)

<br>

| Experimento | Descrição |
|---|---|
| **exp1** | **60 épocas · YOLOv8n** — alta precisão no benchmark curado, mas menor cobertura de helipontos observada em condições de campo. |
| **exp2** | **100 épocas · YOLOv8n** — modelo de referência, com a melhor generalização observada em condições de campo. |
| **exp3** | **100 épocas · YOLOv8n + conjunto de dados aumentado** — maior recall, com desempenho intermediário em campo. |
| **exp4** | **100 épocas · YOLO11n** — mesma base experimental do `exp2`, utilizando uma arquitetura mais recente, mas sem superar o `exp2` na avaliação de campo. |

<br>

> As descrições devem permanecer consistentes com os resultados relatados na análise experimental final do projeto.

<br><br>

## [11. Demonstração Adicional — Scraping Automatizado de Helipontos](#11-demonstração-adicional--scraping-automatizado-de-helipontos)

<br>

A **Demonstração de Scraping Automatizado de Helipontos** possui um propósito diferente dos quatro vídeos de detecção.

<br>

Ela demonstra a **coleta automatizada de coordenadas de helipontos**, realizada usando Selenium e `helipad_bot.py`.

<br>

Portanto, ela **não utiliza o pipeline de inferência descrito nas Etapas 5–9**.

<br>

Para adicionar a trilha sonora:

<br>

```bash
cd ~/Desktop/3-project-ai-ml-yolo-helipad_detector

SCRAPING_VIDEO="demo/🚁Automated Helipad Scraping Demo.mp4"
SCRAPING_AUDIO="assets/audio/feel-good_nina-simone_house remix.mp3"

ffmpeg -y \
  -i "$SCRAPING_VIDEO" \
  -i "$SCRAPING_AUDIO" \
  -c:v copy \
  -c:a aac \
  -shortest \
  "demo/🚁Automated-Helipad-Scraping-Demo-com-trilha.mp4"
```

<br>

Este procedimento cria uma nova versão do vídeo enquanto preserva o arquivo original.

<br>

> [!TIP]
> Se o vídeo original já contiver narração ou outra faixa de áudio, o comando acima irá substituí-la. Para preservar e combinar as duas fontes de áudio, use `amix`.

<br><br>

## [12. Limpeza dos Arquivos Intermediários](#12-limpeza-dos-arquivos-intermediários)

<br>

Após validar os vídeos finais, os arquivos intermediários podem ser removidos:

<br>

```bash
rm -rf reports/demo_frames
rm -rf reports/demo_src
rm -f reports/demo_videos/*_silent.mp4
```

<br>

Os arquivos finais em `demo/` permanecem preservados.

<br><br>

## [13. Resultado Final](#13-resultado-final)

<br>

Ao final do processo, o diretório `demo/` deve conter os quatro vídeos dos experimentos:

<br>

```text
demo/
├── Helipad-Detection-exp1-YOLOv8n-Deteccao-em-Tiles-Reais.mp4
├── Helipad-Detection-exp2-YOLOv8n-Deteccao-em-Tiles-Reais.mp4
├── Helipad-Detection-exp3-YOLOv8n-Deteccao-em-Tiles-Reais.mp4
├── Helipad-Detection-exp4-YOLO11n-Deteccao-em-Tiles-Reais.mp4
└── 🚁Automated-Helipad-Scraping-Demo-com-trilha.mp4
```

<br>

### [Critério de Comparabilidade](#critério-de-comparabilidade)

<br>

A validade da demonstração visual depende de três elementos permanecerem constantes:

<br>

**mesmas imagens de entrada · mesma ordem · mesma trilha sonora**

<br>

A única variável experimental alterada entre os quatro vídeos de detecção é o **modelo usado para a inferência**.

<br>

>  [!TIP]
> **Mesma cena. Modelo diferente.**
