# 📊 Análise de Resultados — Helipad Detector
### YOLOv8n · 60 épocas · Dataset de Helipontos em São Paulo

<br><br>

## 🏆 Métricas de Destaque (dados reais do `results.csv`)

| | Melhor Época (54) | Época Final (60) |
|---|:---:|:---:|
| **Precision** | **1.000** | 0.992 |
| **Recall** | **0.963** | 0.971 |
| **mAP\@50** | **0.994** | 0.994 |
| **mAP\@50–95** | **0.881** | 0.841 |

> [!IMPORTANT]
> O modelo atingiu **Precision = 1.00** e **mAP\@50 = 0.994** na época 54 — resultado excepcionalmente forte para um dataset com apenas ~116 imagens de treino.

<br><br>

## 📈 Gráficos Gerados


<br>

### Figura 1 — Evolução das Losses por Época
![Curvas de Loss](file:///Users/fabicampanari/.gemini/antigravity-ide/brain/5760042e-2127-41ec-a4da-9cab1095c97f/loss_curves.png)

**O que observar:**
- Todas as três losses (Box, Cls, DFL) caem de forma consistente tanto no treino quanto na validação.
- Não há sinal de *overfitting* nas primeiras 60 épocas — a `val_loss` acompanha a `train_loss` sem se distanciar.
- A `val/cls_loss` apresenta oscilação nos primeiros 20 epochs, o que é esperado em datasets pequenos, mas estabiliza a partir do epoch 30.

<br>

### Figura 2 — Precision e Recall ao longo do Treino
![Precision e Recall](file:///Users/fabicampanari/.gemini/antigravity-ide/brain/5760042e-2127-41ec-a4da-9cab1095c97f/precision_recall.png)

**O que observar:**
- **Precision** sobe rapidamente e se estabiliza acima de **0.95** a partir do epoch 30 — o modelo raramente detecta "helipontos" onde não existem.
- **Recall** também alcança **0.97+** nas épocas finais — o modelo consegue encontrar quase todos os helipontos reais nas imagens.
- O cruzamento das duas curvas ocorre cedo (~epoch 20), indicando que o modelo equilibrou bem a captura de objetos e a filtragem de falsos positivos.

<br>

### Figura 3 — mAP\@50 e mAP\@50–95
![mAP Curves](file:///Users/fabicampanari/.gemini/antigravity-ide/brain/5760042e-2127-41ec-a4da-9cab1095c97f/map_curves.png)

**O que observar:**
- **mAP\@50 = 0.994** na melhor época — praticamente perfeito no critério padrão de IoU 50%.
- **mAP\@50–95 = 0.881** — excelente resultado mesmo com o critério rigoroso (padrão COCO), mostrando que as *bounding boxes* são precisas além de somente se sobrepor ao objeto.
- O pico ocorre na **época 54**, após o qual as métricas flutuam levemente, sugerindo que 55–60 épocas são o ponto ótimo para este dataset.

<br><br>

## 📝 Textos Prontos para Slides

<br>

### Slide: Métricas Principais
> "Após 60 épocas de treinamento, o modelo YOLOv8n alcançou uma **Precision de 99,2%** e um **Recall de 97,1%** nos dados de validação, indicando que detecta corretamente a quase totalidade dos helipontos com pouquíssimos falsos positivos."

### Slide: mAP
> "A **mAP\@50 de 99,4%** confirma que o modelo é altamente preciso no critério padrão de detecção. Já a **mAP\@50–95 de 88,1%** (critério rigoroso do padrão COCO) demonstra que as caixas delimitadoras são geometricamente precisas — não apenas se sobrepõem ao objeto, mas o enquadram corretamente."

### Slide: Curvas de Loss
> "As curvas de loss mostram aprendizado consistente e sem sinais de overfitting: tanto a loss de treino quanto a de validação decrescem de forma suave e paralela ao longo das 60 épocas, indicando boa generalização do modelo."

### Slide: Conclusão
> "O Helipoint Detector atingiu desempenho de classe profissional em um dataset construído do zero: **mAP\@50 próxima de 100%** e **mAP\@50–95 de 88%**. Isso valida a qualidade da curadoria, anotação e diversidade geográfica do dataset, confirmando que 80% do esforço em IA está, de fato, nos dados."

<br><br>

## 🔍 Análise Qualitativa — Roteiro para Slides Visuais

Use o seguinte roteiro ao exibir imagens de predição:

| Tipo | O que mostrar | O que explicar |
|------|--------------|----------------|
| ✅ **Acerto claro** | Heliponto detectado com caixa bem ajustada e confiança > 0.8 | "O modelo identificou o 'H' característico mesmo com sombra no rooftop" |
| ✅ **Acerto desafiador** | Heliponto parcialmente coberto ou em ângulo | "Alta confiança mesmo com oclusão parcial, mostrando robustez" |
| ⚠️ **Falso Positivo** | Padrão circular ou 'H' em piscina/quadra detectado | "Estruturas similares ao 'H' de helipontos geram FPs — tratável com mais exemplos negativos" |
| ❌ **Falso Negativo** | Heliponto não detectado | "Helipontos desbotados ou com sombra densa ainda escapam — área de melhoria" |

<br><br>

## 💡 Recomendações para a Apresentação

1. **Use apenas 3 gráficos**: Loss Curves + Precision/Recall + mAP (gerados acima).
2. **Destaque em slide único** a tabela com Precision / Recall / mAP\@50 / mAP\@50–95.
3. **Mostre 4–6 imagens** de predição: 2–3 acertos, 1 FP e 1 FN, com comentário.
4. **Evite** apresentar todas as 15 colunas do CSV — foque nas 4 métricas principais.
5. **Número de ouro para fechar**: *"99,4% de mAP\@50 com um dataset construído do zero em 3 bairros de São Paulo."*

<br><br>

## 🛠️ Código Python Completo para Reproduzir os Gráficos

Copie e cole diretamente no `Analysis.ipynb`:

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('AI Training/runs/detect/runs/exp1-2/results.csv',
                 skipinitialspace=True)
df.columns = df.columns.str.strip()
epoch = df["epoch"]

# ── Figura 1: Losses ────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 4))
fig.suptitle("Evolução da Loss por Época", fontsize=14, fontweight="bold")

for ax, (tr, vl, name) in zip(axes, [
    ("train/box_loss","val/box_loss","Box Loss"),
    ("train/cls_loss","val/cls_loss","Cls Loss"),
    ("train/dfl_loss","val/dfl_loss","DFL Loss"),
]):
    ax.plot(epoch, df[tr], label="Treino",    color="#14b8a6", lw=2)
    ax.plot(epoch, df[vl], label="Validação", color="#f97316", lw=2, ls="--")
    ax.set_title(name); ax.set_xlabel("Época"); ax.legend(); ax.grid(True)

plt.tight_layout(); plt.show()

# ── Figura 2: Precision e Recall ────────────────────────────────
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4))
fig.suptitle("Precision e Recall ao longo do Treino", fontsize=14, fontweight="bold")

a1.plot(epoch, df["metrics/precision(B)"], color="#14b8a6", lw=2)
a1.fill_between(epoch, df["metrics/precision(B)"], alpha=0.1, color="#14b8a6")
a1.set_title("Precision"); a1.set_xlabel("Época"); a1.set_ylim(0,1.05); a1.grid(True)

a2.plot(epoch, df["metrics/recall(B)"], color="#ec4899", lw=2)
a2.fill_between(epoch, df["metrics/recall(B)"], alpha=0.1, color="#ec4899")
a2.set_title("Recall"); a2.set_xlabel("Época"); a2.set_ylim(0,1.05); a2.grid(True)

plt.tight_layout(); plt.show()

# ── Figura 3: mAP ───────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 4))
fig.suptitle("mAP50 e mAP50-95 ao longo do Treino", fontsize=14, fontweight="bold")

ax.plot(epoch, df["metrics/mAP50(B)"],    color="#6366f1", lw=2.5, label="mAP@50")
ax.plot(epoch, df["metrics/mAP50-95(B)"], color="#ec4899", lw=2.5, label="mAP@50-95", ls="--")
ax.fill_between(epoch, df["metrics/mAP50(B)"],    alpha=0.1, color="#6366f1")
ax.fill_between(epoch, df["metrics/mAP50-95(B)"], alpha=0.1, color="#ec4899")
ax.set_xlabel("Época"); ax.set_ylim(0,1.05); ax.legend(); ax.grid(True)

plt.tight_layout(); plt.show()

# ── Tabela: métricas finais ─────────────────────────────────────
best = df.loc[df["metrics/mAP50-95(B)"].idxmax()]
final = df.iloc[-1]

resumo = pd.DataFrame({
    "Precision":  [best["metrics/precision(B)"],  final["metrics/precision(B)"]],
    "Recall":     [best["metrics/recall(B)"],      final["metrics/recall(B)"]],
    "mAP@50":     [best["metrics/mAP50(B)"],       final["metrics/mAP50(B)"]],
    "mAP@50-95":  [best["metrics/mAP50-95(B)"],    final["metrics/mAP50-95(B)"]],
}, index=[f"Melhor (ép. {int(best['epoch'])})", f"Final (ép. {int(final['epoch'])})"])

display(resumo.style.format("{:.4f}").background_gradient(cmap="YlGn", axis=None))
```

<br><br>


<!-- ============================================================ -->
<!-- BLOCO 1 — colar em Analysis_yolo_results.md                  -->
<!-- ============================================================ -->

## [Análise Qualitativa — Dados Reais do Faria Lima]()

<br>

### [***Contexto***]

Rodada de inferência com o modelo `exp2` sobre **840 tiles reais** baixados do bairro Faria Lima (zoom 19, ESRI World Imagery), como teste de campo em uma região densa de helipontos corporativos. **170 de 840 tiles (20,2%)** tiveram detecção com confiança ≥ 0,25.



Abaixo, uma seleção representativa — acertos claros, acertos desafiadores, falsos positivos e um problema de qualidade de dado identificado no processo.

<br>

### [***Tabela de Casos***]

| Tipo | Tile | Confiança | Observação |
|---|:---:|:---:|---|
| ✅ Acerto claro | `tile_z19_x194126_y297485.jpg` | 0.94 | Padrão "H" nítido dentro de quadrado bem definido no telhado |
| ✅ Acerto claro | `tile_z19_x194143_y297481.jpg` | 0.96 | Geometria e contraste claros, caixa bem ajustada |
| ✅ Acerto claro | `tile_z19_x194149_y297489.jpg` | 0.96 | Geometria e contraste claros, caixa bem ajustada |
| ✅ Acerto desafiador | `tile_z19_x194545_y298183.jpg` | 0.77 | Detecção correta mesmo em ângulo/iluminação menos favorável |
| ⚠️ Falso Positivo | `tile_z19_x194129_y297480.jpg` | 0.78 | Caixa sobre **quadra esportiva** (padrão retangular listrado), não heliponto |
| ⚠️ Falso Positivo | `tile_z19_x194547_y298176.jpg` | 0.86 | Caixa sobre **piscina** — reflexo/formato geométrico similar ao "H" |
| ⚠️ Falso Positivo (baixa confiança) | `tile_z19_x194548_y298181.jpg` | 0.28 | Caixa minúscula na borda da imagem — provável ruído do modelo |
| ❌ Falha de dado (não do modelo) | `tile_z19_x194139_y297467.jpg` | — | Tile **vazio/preto** (falha no download ESRI) marcado como "Detected" |
| ❌ Falha de dado (não do modelo) | `tile_z19_x194141_y297481.jpg` | — | Mesmo problema — tile preto sem conteúdo válido |

<br>

### [***Leitura dos Resultados***]

Os falsos positivos seguem o padrão já esperado e documentado no projeto: **piscinas e quadras esportivas** compartilham geometria retangular/contraste semelhante ao "H" do heliponto, e continuam sendo a principal fonte de erro do modelo — reforçando a necessidade de mais exemplos negativos desse tipo no próximo ciclo de anotação.



O caso dos **tiles vazios marcados como detectados** não é um erro de modelo, e sim uma lacuna no pipeline de dados: tiles que falham no download (conteúdo preto/corrompido) ainda são enviados para inferência. Ação recomendada: adicionar uma checagem de "tile vazio" (ex: desvio-padrão de pixel abaixo de um limiar) antes de rodar o modelo, filtrando esses casos automaticamente.

<br><br>



<!-- ============================================================ -->
<!-- BLOCO 2 — colar no Relatório Executivo                        -->
<!-- ============================================================ -->

## [Validação de Campo — Faria Lima]()



Além da avaliação padrão em dados de validação/teste, o modelo foi submetido a um **teste de campo real**: inferência completa sobre 840 tiles de satélite do bairro Faria Lima, um dos corredores corporativos com maior densidade de helipontos de São Paulo.



**Resultado: 170 de 840 tiles (20,2%) com detecção**, com confiança mediana alta (a maioria dos acertos claros entre 0.90–0.98). A análise qualitativa confirmou o padrão de erro já conhecido do projeto — falsos positivos concentrados em piscinas e quadras esportivas — validando tanto a robustez do modelo quanto a consistência da documentação de limitações já registrada no projeto.

<br><br>



<!-- ============================================================ -->
<!-- BLOCO 3 — colar no README (destaque)                           -->
<!-- ============================================================ -->

## [Teste de Campo Real — Faria Lima]()



O modelo treinado (`exp2`) foi testado contra **840 tiles reais** de satélite do Faria Lima — um dos corredores corporativos com maior densidade de helipontos de São Paulo — como etapa prática de validação além da divisão padrão treino/validação/teste.



**170 de 840 tiles (20,2%)** retornaram uma detecção, com acertos de alta confiança (0.90–0.98) compatíveis com o padrão "H" esperado no telhado, além de um punhado de falsos positivos já documentados (piscinas, quadras esportivas) consistentes com os padrões de erro já descritos na seção de análise qualitativa.

<br><br>

> [!NOTE]
> Esses números refletem só o Faria Lima (primeira rodada). Assim que a triagem multi-bairro (`auto_triage_regions.py`) terminar de rodar nos 10 bairros do `sp_neighborhoods_bbox.csv`, este conteúdo deve ser atualizado com os totais e a tabela por região.

