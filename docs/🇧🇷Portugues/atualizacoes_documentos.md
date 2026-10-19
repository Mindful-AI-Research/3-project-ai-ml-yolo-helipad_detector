## [Atualizações necessárias nos documentos do projeto]()

<br><br>

> Detecção visual automatizada baseada em imagem, sujeita a erros e não equivalente a validação operacional, legal, de segurança ou aeronáutica.

<br><br>

## [Como usar esta lista]()

Cada linha traz o trecho atual (lido nos arquivos do projeto), o motivo e o texto sugerido. Só substitui o que os achados de linhagem tornaram impreciso; o que não aparece aqui não precisa mudar. O `app.py` do painel não foi lido nesta rodada; a seção 5 é uma sugestão, não um diff.

<br><br>

## [1. README (README.pt_BR.md e README.md)]()

| Trecho atual | Problema | Texto sugerido |
|---|---|---|
| “exp1 vs. exp2 (confirmado): … mesmo dataset original … variando apenas as épocas” | exp1 e exp2 têm dados de mesmo conteúdo (v2, 178/34/14), mas outro autor, ambiente e versão do Ultralytics (8.4.75 e 8.4.98) | “exp1 e exp2 usam o mesmo conteúdo de dados (versão 2 do conjunto de Pedro). Diferem também em autor, ambiente e versão do Ultralytics, então não formam uma ablação controlada de épocas. O vínculo do exp1 com a v2 é indício forte (args.yaml e pesos), sem registro de contagem.” |
| “~150 imagens” | A v2 tem 226 imagens (178 treino, 34 validação, 14 teste); 116/33 era a v1 | “226 imagens (v2: 178/34/14)” |
| “augmentations como rotações de 90°, flips…” e “70/20/10” | A v2 não tem aumento de dados (só pré-processamento de orientação); só o fork (exp3) tem aumento | “A v2 não usa aumento; o exp3 usa um fork com aumento (rotação ±15°, brilho ±25%, inversões).” |
| “anotação com bounding boxes bem definidas” | 170 dos 178 arquivos de rótulo do treino e todos os de validação e teste são polígonos; o treino de detecção os converte em caixas | “Rótulos majoritariamente em polígono, convertidos em caixas no treino de detecção.” |
| Seção do exp4 | Falta explicar o “3 corrupt” | “Três arquivos de rótulo do treino misturam polígono e caixa e são sinalizados pelo Ultralytics 8.4.163 (o exp2 usou 8.4.98, sem sinalização).” |
| Seção de validação em campo | Falta a sobreposição | “125 das 225 imagens anotadas são cópias de *tiles* de campo (2,3% dos 5.540 *tiles* distintos). Ver `reports/lineage_audit/`.” |
| Autoria “Campanari” | Sobrenome atual: Campaner (mantenha os links e *slugs* como estão) | Trocar só o texto de autoria. |

<br><br>

## [2. HTML da apresentação (helipad-detector-presentation.html)]()

| Trecho atual | Problema | Texto sugerido |
|---|---|---|
| `Autor/Autora: Fabiana ⚡️ Campanari` (PT e EN) | Sobrenome | `Fabiana ⚡️ Campaner` |
| “Regime de poucos dados (~150 imagens)” e nota dos resultados “(~150 imagens)” | Contagem desatualizada | “226 imagens” |
| Etapa “Dividir: 70/20/10 treino/validação/teste” | A v2 é 178/34/14 (cerca de 79/15/6) | “178/34/14” |
| Diagrama “Field validation on unseen regions” e slide “Proven beyond the training set” | O campo não é, em parte, região não vista: 125 imagens anotadas são *tiles* de campo | “Validação em campo (inclui 125 *tiles* também presentes nas imagens anotadas; ver relatório de evidências)” |
| “7.943 tiles reais validados em campo” | O conjunto comparado entre experimentos tem 7.767 pares e 5.540 *tiles* distintos | “7.943 (produção) / 7.767 pares comparados; 5.540 *tiles* distintos” |
| Slide de comparação exp1 × exp2 | Mesma ressalva do README | “Não é comparação controlada (autor, ambiente e versão do Ultralytics diferem).” |

<br><br>

## [3. Relatório completo (Helipad_Detector_Full_Report)]()

| Trecho atual | Problema | Texto sugerido |
|---|---|---|
| Capa: “Autor: Fabiana Campanari”; rodapé “Helipod Detector” | Sobrenome e erro de digitação | “Fabiana Campaner”; “Helipad Detector” |
| “about 150 images total” (seção 8) | Contagem desatualizada | “226 imagens (v2)” |
| Seção 6: “Data augmentation: rotações de 90°, flips… Standard split: 70/20/10” | A v2 não tem aumento e a divisão é 178/34/14 | Descrever a v2 e restringir o aumento ao exp3 |
| Seção 7, exp1 | Falta a origem da execução | “exp1: execução de Pedro Vyctor Almeida (pasta exp1-2), versão 2; vínculo por evidência documental.” |
| Seção 7.1, incidente exp2/exp3 | Pode ser documentado com registros | “O registro do exp3 conta 356/34 (fork); o do exp2 refeito, 178/34 (original).” |
| Seção 9, campo | Falta a sobreposição e a duplicidade entre regiões | Acrescentar os números das seções 5 e 6 do relatório de evidências |
| Seção 4 e 6, “bounding boxes” | Rótulos são polígonos | Mesma frase do README |

<br><br>

## [4. Observação sobre prazos]()

Estas mudanças não afetam o pré-projeto, que já está atualizado. Pode ser feito depois de 16/10 sem prejuízo.

<br><br>

## [5. Painel Streamlit (apps/streamlit_app/app.py)]()

Sugestão, sem leitura do arquivo: na aba Governança, um quadro “Linhagem e limitações” com as contagens acima; na aba de métricas, uma nota de que os experimentos não são comparação controlada; na aba de campo, 7.943 (produção) e 7.767 (comparação), com 5.540 *tiles* distintos.
