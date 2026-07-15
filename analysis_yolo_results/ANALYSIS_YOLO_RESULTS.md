# 📊 Análise de Resultados — Helipoint Detector
### YOLOv8n · 60 épocas · Dataset de Helipontos em São Paulo

<br><br>

## 🏆 Métricas de Destaque (dados reais do `results.csv`)

| | Melhor Época (54) | Época Final (60) |
|---|:---:|:---:|
| **Precision** | **1.000** | 0.992 |
| **Recall** | **0.963** | 0.971 |
| **mAP\@50** | **0.994** | 0.994 |
| **mAP\@50–95** | **0.881** | 0.841 |

<br>

> [!IMPORTANT]
> O modelo atingiu **Precision = 1.00** e **mAP\@50 = 0.994** na época 54 — resultado excepcionalmente forte para um dataset com apenas ~116 imagens de treino.

<br><br>

## 📈 Gráficos Gerados

### Figura 1 — Evolução das Losses por Época

<br><br>


<img width="2384" height="696" alt="Image" src="https://github.com/user-attachments/assets/908d3f06-f9f9-4d4c-aa91-aefdf11ba6f3" />

<br><br>


**O que observar:**

- Todas as três losses (Box, Cls, DFL) caem de forma consistente tanto no treino quanto na validação.
- Não há sinal de *overfitting* nas primeiras 60 épocas — a `val_loss` acompanha a `train_loss` sem se distanciar.
- A `val/cls_loss` apresenta oscilação nos primeiros 20 epochs, o que é esperado em datasets pequenos, mas estabiliza a partir do epoch 30.

<br><br>

### Figura 2 — Precision e Recall ao longo do Treino

<br><br>

!<img width="1784" height="696" alt="Image" src="https://github.com/user-attachments/assets/aa55ed18-4704-456a-93eb-660a3f14115c" />

<br><br>


**O que observar:**

- **Precision** sobe rapidamente e se estabiliza acima de **0.95** a partir do epoch 30 — o modelo raramente detecta "helipontos" onde não existem.
- **Recall** também alcança **0.97+** nas épocas finais — o modelo consegue encontrar quase todos os helipontos reais nas imagens.
- O cruzamento das duas curvas ocorre cedo (~epoch 20), indicando que o modelo equilibrou bem a captura de objetos e a filtragem de falsos positivos.

<br><br>

### Figura 3 — mAP\@50 e mAP\@50–95


<br><br>


<img width="1484" height="696" alt="Image" src="https://github.com/user-attachments/assets/ca3521c6-7027-4969-aa09-530d47c5a83b" />


<br><br>


**O que observar:**
- **mAP\@50 = 0.994** na melhor época — praticamente perfeito no critério padrão de IoU 50%.
- **mAP\@50–95 = 0.881** — excelente resultado mesmo com o critério rigoroso (padrão COCO), mostrando que as *bounding boxes* são precisas além de somente se sobrepor ao objeto.
- O pico ocorre na **época 54**, após o qual as métricas flutuam levemente, sugerindo que 55–60 épocas são o ponto ótimo para este dataset.

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
