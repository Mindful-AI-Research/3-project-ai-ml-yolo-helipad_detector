# 🚁 Helipad Detector — Manual Completo de Execução

Guia passo a passo pra rodar o projeto inteiro do zero: ambiente, automação de dados, treino, dashboard, deploy e Git. Escrito pra ser seguido copiando e colando os comandos, sem precisar adivinhar nada.

<br>

## 📋 Índice

1. [Pré-requisitos](#1-pré-requisitos)
2. [Configurar o ambiente pela primeira vez](#2-configurar-o-ambiente-pela-primeira-vez)
3. [Rotina do dia a dia (toda vez que for trabalhar)](#3-rotina-do-dia-a-dia)
4. [Automação de coleta de dados (scraping)](#4-automação-de-coleta-de-dados-scraping)
5. [Treinar os modelos (exp1, exp2, exp3)](#5-treinar-os-modelos)
6. [Rodar o dashboard localmente](#6-rodar-o-dashboard-localmente)
7. [Deploy no Streamlit Cloud](#7-deploy-no-streamlit-cloud)
8. [Git — subir mudanças pro GitHub](#8-git--subir-mudanças-pro-github)
9. [Erros comuns e como resolver](#9-erros-comuns-e-como-resolver)

<br><br>

## 1. Pré-requisitos

Antes de começar, você precisa ter instalado:

- **Python 3** (no Mac, geralmente já vem instalado)
- **Git** (geralmente já vem instalado no Mac)
- **Homebrew** (gerenciador de pacotes do Mac) — se não tiver:
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
- Uma conta no **GitHub** com acesso ao repositório
- Uma conta no **Roboflow** (pra baixar o dataset)
- Uma conta no **Google** (pra usar o Google Colab, treino com GPU)

<br><br>

## 2. Configurar o ambiente pela primeira vez

Só precisa fazer isso **uma vez** (ou de novo se apagar a pasta `.venv`).

### 2.1 Entrar na pasta do projeto

```bash
cd /Users/fabicampanari/Desktop/3-project-ai-ml-yolo-helipad_detector
```

> ⚠️ Se a pasta tiver outro nome no seu computador, ajusta o caminho acima.

### 2.2 Criar o ambiente virtual

```bash
python3 -m venv .venv
```

### 2.3 Ativar o ambiente virtual

```bash
source .venv/bin/activate
```

O início da linha do terminal deve mudar pra mostrar `(.venv)` na frente.

### 2.4 Instalar todas as dependências

```bash
python3 -m pip install -r requirements.txt
```

> ⚠️ **Nunca use só `pip install`** — sempre `python3 -m pip install`, senão pode instalar no lugar errado do computador e dar o erro `externally-managed-environment`.

<br><br>

## 3. Rotina do dia a dia

Toda vez que for trabalhar no projeto (depois da primeira configuração), só precisa disso:

```bash
cd /Users/fabicampanari/Desktop/3-project-ai-ml-yolo-helipad_detector
source .venv/bin/activate
```

Confirma que deu certo:
```bash
which python3
```
Deve mostrar um caminho **dentro** da pasta do projeto, terminando em `.venv/bin/python3`. Se aparecer `/opt/homebrew/bin/python3` ou parecido (sem `.venv` no meio), o ambiente virtual não ativou direito — repete o `source .venv/bin/activate`.

<br><br>

## 4. Automação de coleta de dados (scraping)

### 4.1 Rodar o pipeline completo

```bash
python3 src/geospatial/run_scraping_pipeline.py
```

Vai perguntar quantos helipontos coletar — digita um número (ex: `150`) e Enter.

> ⏳ Pode demorar bastante (o site é visitado devagar de propósito, uma página por vez, com pausa entre elas). Deixa rodando em segundo plano.

**Saída esperada:**
```
✅ Pipeline complete. Output ready at:
   src/geospatial/helipad_coordinates_bbox.csv
```

### 4.2 Separar São Paulo de outros estados (opcional)

```bash
python3 src/geospatial/geocode_states.py
```

Gera `helipad_coordinates_com_estado.csv` com uma coluna extra indicando o estado de cada heliponto. Demora ~1 segundo por linha (respeita o limite do serviço de geocodificação).

### 4.3 Coletar imagens de um bairro específico (ex: Faria Lima)

1. Coloca `geospatial_image_collection_faria_lima.ipynb` e `faria_lima_input.csv` na mesma pasta (`src/geospatial/`)
2. Abre o notebook e roda todas as células
3. Depois: faz a **triagem manual** dos tiles baixados (olha um por um, descarta os que não têm heliponto visível)
4. Sobe os selecionados pro Roboflow pra anotar

<br><br>

## 5. Treinar os modelos

Treino precisa de **GPU** — sempre no Google Colab, nunca local.

### 5.1 exp1 (60 épocas, dataset original)

Já foi rodado pelo Pedro. Não precisa rodar de novo, a menos que queira reproduzir.

### 5.2 exp2 (100 épocas, dataset original — o experimento oficial que falta)

1. Abre `src/training/yolo_training_exp2.ipynb` no Google Colab
2. Menu **Runtime → Change runtime type → T4 GPU**
3. Roda célula por célula, de cima pra baixo
4. Quando pedir a chave do Roboflow, cola a sua (não precisa ser a do Pedro — o dataset é público)
5. Se aparecer `AssertionError` na célula de download, **pare** e confira se o dataset baixado não é o fork por engano
6. No final, o notebook mostra os caminhos de tudo que foi salvo (pesos, ONNX, métricas)

**Depois de terminar:**
```bash
mkdir -p artifacts/runs/detect/exp2/weights
# copia best.pt e results.csv pra essa pasta
```

### 5.3 exp3 (100 épocas, dataset fork — já rodado, bônus)

Já concluído. Se quiser rodar de novo sem gastar GPU (reaproveitando o modelo já treinado):

1. Abre `src/training/yolo_training_exp3.ipynb`
2. Roda a célula **"💡 Already trained this before? Skip GPU entirely"** em vez da célula de treino
3. Segue direto pras seções de Export ONNX, Comparação e Kepler

<br><br>

## 6. Rodar o dashboard localmente

```bash
cd /Users/fabicampanari/Desktop/3-project-ai-ml-yolo-helipad_detector
source .venv/bin/activate
streamlit run apps/streamlit_app/app.py
```

Abre sozinho no navegador. Pra parar: `Ctrl+C` no terminal.

**O app funciona mesmo sem nenhum modelo treinado** — só as abas de detecção (Upload, Busca por Região, Amostras) ficam desativadas até existir um `best.pt`. O mapa, pipeline e downloads funcionam sempre.

<br><br>

## 7. Deploy no Streamlit Cloud

### 7.1 Primeiro, sobe tudo pro GitHub (ver Seção 8)

### 7.2 No navegador

1. Acessa **share.streamlit.io** e loga com GitHub
2. Clica **"New app"**
3. Preenche:
   - **Repository**: `Mindful-AI-Research/3-project-ai-ml-yolo-helipad_detector`
   - **Branch**: `main`
   - **Main file path**: `apps/streamlit_app/app.py`
4. Clica **"Deploy!"**
5. Espera 2-5 minutos o build terminar

<br><br>

## 8. Git — subir mudanças pro GitHub

### 8.1 Fluxo normal (sem conflito)

```bash
git status
```
Mostra o que mudou.

```bash
git add .
git commit -m "descreva o que você mudou aqui"
git push
```

### 8.2 Autenticação (primeira vez ou se pedir senha)

O GitHub **não aceita mais senha normal**. Use o GitHub CLI:

```bash
brew install gh
gh auth login
```

Responde:
- **GitHub.com**
- **HTTPS**
- **Yes** (autenticar Git com credenciais do GitHub)
- **Login with a web browser**

Copia o código mostrado, aperta Enter, confirma no navegador que abrir.

Depois disso, conecta o Git com o login:
```bash
gh auth setup-git
```

E confirma que o endereço remoto está certo:
```bash
git remote set-url origin https://github.com/Mindful-AI-Research/3-project-ai-ml-yolo-helipad_detector.git
```

### 8.3 ⚠️ Regra de ouro sobre `git push --force`

**Nunca use `--force` ou `--force-with-lease` sem ter certeza absoluta** de que:
- Não tem ninguém mais commitando direto no repositório sem passar pelo seu computador
- Você já rodou `git fetch` e olhou o que tem no remoto antes
- Você sabe exatamente o que está sobrescrevendo

Se editou algo direto no site do GitHub (navegador) recentemente, **puxa isso pro seu computador primeiro** (`git pull`) antes de fazer qualquer `push --force` — senão a edição do navegador pode sumir (like aconteceu com o README, mas recuperamos).

### 8.4 Editando direto no GitHub (navegador)

Se você mexe no README ou outro arquivo direto no site do GitHub, **sempre depois disso**, no seu computador:

```bash
git pull
```

Antes de continuar trabalhando — assim você nunca fica com uma versão desatualizada que depois entra em conflito.

<br><br>

## 9. Erros comuns e como resolver

| Erro | Causa | Solução |
|---|---|---|
| `zsh: command not found: python` | Mac usa `python3`, não `python` | Troca `python` por `python3` em todo comando |
| `zsh: command not found: pip` | Mesma coisa, mas com pip | Use `python3 -m pip install ...` |
| `error: externally-managed-environment` | Tentando instalar fora do ambiente virtual | Confirma que `(.venv)` aparece no terminal; se não, roda `source .venv/bin/activate` |
| `.venv` aponta pro Python errado mesmo com `(.venv)` ativo | Pasta foi renomeada depois que o `.venv` foi criado | Apaga e recria: `rm -rf .venv && python3 -m venv .venv && source .venv/bin/activate` |
| `Password authentication is not supported` | GitHub não aceita mais senha | Usa GitHub CLI (`gh auth login`), ver Seção 8.2 |
| `Personal access tokens (classic) are forbidden` | Organização bloqueia tokens antigos | Usa GitHub CLI (`gh auth login`) em vez de token manual |
| `fatal: not a git repository` | Terminal está na pasta errada (`~` em vez do projeto) | `cd` pra pasta certa do projeto primeiro |
| `KeyError: 'lat'` no dashboard | Falta o `sp_neighborhoods_bbox.csv` em `src/geospatial/` | Confirma que o arquivo está lá: `ls src/geospatial/sp_neighborhoods_bbox.csv` |
| "No model found" trava o app inteiro | Versão antiga do `app.py` sem o fix de tolerância | Usa a versão mais recente do `app.py` (já corrigida) |
| Link (`https://...`) dá erro `no such file or directory` no terminal | Colou um link do navegador no terminal por engano | Links são pra colar na **barra de endereço do navegador**, não no terminal. Ou usa `open "URL"` no Mac pra abrir automaticamente |
| Tela cheia de texto com `:` piscando no final, terminal não responde | Entrou no modo de visualização `less` (comum depois de `git log`, `git branch -r`, etc.) | Aperta **`q`** pra sair |

<br><br>

---

**Dica final:** sempre que um comando der erro, copia a mensagem completa (não só a última linha) — o erro geralmente já diz exatamente o que está errado, só precisa ler com calma.
