# 🇧🇷 Manual — Geração dos Vídeos de Demo

**Helipad Detection · YOLOv8n / YOLO11n · São Paulo**

<br>

## 1. Objetivo

Este manual documenta o procedimento utilizado para gerar os vídeos de demonstração dos quatro experimentos de detecção de helipontos:

- `exp1` — YOLOv8n
- `exp2` — YOLOv8n
- `exp3` — YOLOv8n + dataset aumentado
- `exp4` — YOLO11n

Os vídeos apresentam a **inferência dos modelos sobre tiles reais de imagens de satélite**, permitindo visualizar o comportamento de cada modelo em imagens que não foram utilizadas durante seu treinamento.

> **Importante:** os vídeos representam **inferência**, não treinamento.

<br>

## 2. Metodologia Experimental

### 2.1 Amostragem controlada

O conjunto geoespacial contém aproximadamente **7.767–7.943 tiles**, dependendo da versão do dataset. Executar inferência sobre todos os tiles e convertê-los em vídeo produziria demonstrações excessivamente longas e aumentaria significativamente o custo computacional.

Para a demonstração, é utilizada uma **amostra fixa de tiles por região**.

Com a configuração padrão:

```text
10 regiões × 8 tiles por região = 80 tiles
```

A amostra é criada **uma única vez** e reutilizada nos quatro experimentos.

### 2.2 Comparabilidade

A utilização da mesma amostra garante que:

- os quatro modelos recebem as mesmas imagens;
- as regiões analisadas são as mesmas;
- a ordem de apresentação permanece consistente;
- a trilha sonora é a mesma;
- as diferenças observadas podem ser atribuídas ao comportamento dos modelos.

Em outras palavras:

> **Mesma cena, modelo diferente.**

Esse procedimento evita que a seleção das imagens introduza uma variável adicional na comparação visual dos experimentos.

<br>

## 3. Pré-requisitos

Antes de iniciar, confirme:

- repositório localizado em `3-project-ai-ml-yolo-helipad_detector`;
- `ffmpeg` instalado;
- ambiente Python configurado;
- pacote `ultralytics` disponível;
- pesos treinados disponíveis em:

```text
artifacts/runs/runs/detect/
├── exp1/weights/best.pt
├── exp2/weights/best.pt
├── exp3/weights/best.pt
└── exp4/weights/best.pt
```

- tiles das regiões disponíveis em:

```text
src/geospatial/mosaic_*/
```

### FFmpeg — macOS

Caso necessário:

```bash
brew install ffmpeg
```

<br>



## 4. Pipeline de Geração

O processo completo segue quatro etapas principais:

```text
Tiles reais
     │
     ▼
Amostra controlada
10 regiões
     │
     ▼
Inferência
exp1 · exp2 · exp3 · exp4
     │
     ▼
Frames anotados
     │
     ▼
Vídeos MP4
     │
     ▼
Trilha sonora comum
     │
     ▼
Demos finais
```

<br>



## 5. Etapa 1 — Construção da Amostra

Defina o número de tiles selecionados por região:

```bash
cd ~/Desktop/3-project-ai-ml-yolo-helipad_detector

N_PER_REGION=8
SRC=reports/demo_src

rm -rf "$SRC"
mkdir -p "$SRC" reports/demo_frames reports/demo_videos
```

Em seguida, monte a amostra:

```bash
i=0

for REGION in $(ls -d src/geospatial/mosaic_*/ | sort); do
  i=$((i+1))
  PREFIX=$(printf "%02d" $i)
  REGION_NAME=$(basename "$REGION")

  echo "[$PREFIX] $REGION_NAME"

  # Descompacta os tiles caso a região ainda contenha arquivos ZIP.
  unzip -n "$REGION"*.zip -d "$REGION" 2>/dev/null || true

  ls "$REGION"*.jpg | sort | head -$N_PER_REGION | while read -r TILE; do
    cp "$TILE" "$SRC/${PREFIX}_${REGION_NAME}_$(basename "$TILE")"
  done
done

echo "Total de tiles:"
ls "$SRC"/*.jpg | wc -l
```

Com `N_PER_REGION=8`, o resultado esperado é aproximadamente:

```text
80 tiles
```

Aumente `N_PER_REGION` caso seja necessária uma demonstração mais extensa:

```bash
N_PER_REGION=12
```

> **Não altere a amostra entre os experimentos.** A mesma pasta `reports/demo_src/` deve ser utilizada por `exp1`, `exp2`, `exp3` e `exp4`.

<br>



## 6. Etapa 2 — Inferência dos Quatro Experimentos

Execute a inferência sobre a mesma amostra:

```bash
for EXP in exp1 exp2 exp3 exp4; do
  echo "=== Rodando $EXP ==="

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

```text
reports/demo_frames/
├── exp1/
├── exp2/
├── exp3/
└── exp4/
```

Cada pasta contém os frames anotados produzidos pelo respectivo modelo.

### Verificação de consistência

Os quatro experimentos devem gerar a mesma quantidade de frames.

Para uma amostra de 80 tiles:

```text
exp1 → 80 frames
exp2 → 80 frames
exp3 → 80 frames
exp4 → 80 frames
```

Uma diferença na quantidade de frames indica que a execução deve ser verificada antes da geração dos vídeos.

<br>



## 7. Etapa 3 — Conversão dos Frames em Vídeo

Utilize `ffmpeg` para converter os frames anotados em MP4.

A configuração recomendada é de **2 FPS**, permitindo observar as detecções com maior clareza.

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

Os vídeos intermediários serão criados em:

```text
reports/demo_videos/
├── exp1_silent.mp4
├── exp2_silent.mp4
├── exp3_silent.mp4
└── exp4_silent.mp4
```

<br>



## 8. Etapa 4 — Adição da Trilha Sonora

Os quatro vídeos utilizam a **mesma trilha sonora**.

Essa padronização é intencional: como o objetivo é comparar visualmente os modelos, a trilha não deve funcionar como uma variável adicional entre os experimentos.

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

> Confirme o nome exato do arquivo em `assets/audio/` antes da execução.

<br>


## 9. Etapa 5 — Arquivos Finais

Crie a pasta de demonstração:

```bash
mkdir -p demo
```

Copie os vídeos finais:

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

Verifique os arquivos:

```bash
ls -lh demo/*.mp4
```

<br>



## 10. Legendas dos Experimentos

| Experimento | Descrição |
|---|---|
| **exp1** | **60 épocas · YOLOv8n** — alta precisão no benchmark curado, mas menor cobertura dos helipontos observados em campo. |
| **exp2** | **100 épocas · YOLOv8n** — modelo de referência, com melhor generalização observada em campo. |
| **exp3** | **100 épocas · YOLOv8n + dataset aumentado** — maior recall, com desempenho intermediário em campo. |
| **exp4** | **100 épocas · YOLO11n** — mesma base experimental do `exp2`, utilizando uma arquitetura mais recente, mas sem superar o `exp2` na avaliação em campo. |

> As descrições devem permanecer consistentes com os resultados apresentados no relatório experimental.

<br>



## 11. Demo Adicional — Automated Helipad Scraping

O vídeo **Automated Helipad Scraping Demo** possui uma finalidade diferente dos vídeos de detecção.

Ele demonstra o processo de **coleta automatizada de coordenadas de helipontos**, realizado por meio de Selenium e `helipad_bot.py`.

Portanto, ele **não utiliza o pipeline de inferência dos Passos 5–9**.

Para adicionar a trilha sonora:

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

Esse procedimento cria uma nova versão do vídeo e preserva o arquivo original.

> [!TIP]
> Se o vídeo original já possuir narração ou outro áudio, o comando acima substituirá a faixa existente. Para preservar e combinar os dois áudios, utilize `amix`.

<br>



## 12. Limpeza dos Arquivos Intermediários

Após validar os vídeos finais, os arquivos intermediários podem ser removidos:

```bash
rm -rf reports/demo_frames
rm -rf reports/demo_src
rm -f reports/demo_videos/*_silent.mp4
```

Os arquivos finais em `demo/` permanecem preservados.

<br>


## 13. Resultado Final

Ao final do processo, a pasta `demo/` deverá conter os vídeos de demonstração dos quatro experimentos:

```text
demo/
├── Helipad-Detection-exp1-YOLOv8n-Deteccao-em-Tiles-Reais.mp4
├── Helipad-Detection-exp2-YOLOv8n-Deteccao-em-Tiles-Reais.mp4
├── Helipad-Detection-exp3-YOLOv8n-Deteccao-em-Tiles-Reais.mp4
├── Helipad-Detection-exp4-YOLO11n-Deteccao-em-Tiles-Reais.mp4
└── 🚁Automated-Helipad-Scraping-Demo-com-trilha.mp4
```

### Critério de Comparabilidade

A validade da demonstração visual depende de três elementos permanecerem constantes:

**mesmas imagens de entrada · mesma ordem · mesma trilha sonora**

A única variável experimental alterada entre os quatro vídeos é o **modelo utilizado na inferência**.

> **Same scene. Different model.**
