
# 🚁 Helipad Detector — Manual Completo de Execução

Guia passo a passo para rodar o projeto inteiro do zero: ambiente, automação de dados, treino, dashboard, deploy e Git. Escrito para ser seguido copiando e colando os comandos, sem precisar adivinhar nada.[^1][^2]

<br><br>

## 📋 Índice

1. [Pré-requisitos](#1-pr%C3%A9-requisitos)
2. [Configurar o ambiente pela primeira vez](#2-configurar-o-ambiente-pela-primeira-vez)
3. [Rotina do dia a dia (toda vez que for trabalhar)](#3-rotina-do-dia-a-dia-toda-vez-que-for-trabalhar)
4. [Automação de coleta de dados (scraping)](#4-automa%C3%A7%C3%A3o-de-coleta-de-dados-scraping)
5. [Treinar os modelos (exp1, exp2, exp3)](#5-treinar-os-modelos-exp1-exp2-exp3)
6. [Rodar o dashboard localmente](#6-rodar-o-dashboard-localmente)
7. [Deploy no Streamlit Cloud](#7-deploy-no-streamlit-cloud)
8. [Git — subir mudanças para o GitHub](#8-git--subir-mudan%C3%A7as-para-o-github)
9. [Erros comuns e como resolver](#9-erros-comuns-e-como-resolver)

<br><br>

## 1. Pré-requisitos

Antes de começar, você precisa ter instalado:

<br>

- **Python 3** (no Mac, geralmente já vem instalado)
- **Git** (geralmente já vem instalado no Mac)
- **Homebrew** (gerenciador de pacotes do Mac) — se não tiver:

<br>

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

- Uma conta no **GitHub** com acesso ao repositório
- Uma conta no **Roboflow** (para baixar o dataset)
- Uma conta no **Google** (para usar o Google Colab para treino com GPU)

<br><br>

## 2. Configurar o ambiente pela primeira vez

Só precisa fazer isso **uma vez** (ou de novo se apagar a pasta `.venv`).

<br>

### 2.1 Entrar na pasta do projeto

<br>

```bash
cd /Users/fabicampanari/Desktop/3-project-ai-ml-yolo-helipad_detector
```

<br>

> ⚠️ Se a pasta tiver outro nome no seu computador, ajuste o caminho acima.

<br>

### 2.2 Criar o ambiente virtual

<br>

```bash
python3 -m venv .venv
```

<br>

### 2.3 Ativar o ambiente virtual

<br>

```bash
source .venv/bin/activate
```

<br>

> O início da linha do terminal deve mudar para mostrar `(.venv)` na frente.

<br>

### 2.4 Instalar todas as dependências

<br>

```bash
python3 -m pip install -r requirements.txt
```

<br>

> ⚠️ **Nunca use só `pip install`** — sempre use `python3 -m pip install`, senão pode instalar no lugar errado do computador e gerar o erro `externally-managed-environment`.

<br><br>

## 3. Rotina do dia a dia

Toda vez que for trabalhar no projeto (depois da configuração inicial), só precisa disso:

<br>

```bash
cd /Users/fabicampanari/Desktop/3-project-ai-ml-yolo-helipad_detector
source .venv/bin/activate
```

<br>

Confirme que deu certo:

<br>

```bash
which python3
```

<br>

Deve mostrar um caminho **dentro** da pasta do projeto, terminando em `.venv/bin/python3`. Se aparecer `/opt/homebrew/bin/python3` ou algo parecido (sem `.venv` no meio), o ambiente virtual não foi ativado corretamente — rode `source .venv/bin/activate` de novo.

<br><br>

## 4. Automação de coleta de dados (scraping)

### 4.1 Rodar o pipeline completo

<br>

```bash
python3 src/geospatial/run_scraping_pipeline.py
```

<br>

Vai perguntar quantos helipontos coletar — digite um número (por exemplo, `150`) e aperte Enter.

<br>

> ⏳ Isso pode demorar bastante (o site é visitado devagar de propósito, uma página por vez, com pausas entre elas). Deixe rodando em segundo plano.

<br>

**Saída esperada:**

<br>

```
✅ Pipeline complete. Output ready at:
   src/geospatial/helipad_coordinates_bbox.csv
```

<br>

### 4.2 Separar São Paulo de outros estados (opcional)

<br>

```bash
python3 src/geospatial/geocode_states.py
```

<br>

Isso gera `helipad_coordinates_com_estado.csv` com uma coluna extra indicando o estado de cada heliponto. Demora cerca de 1 segundo por linha (para respeitar o limite do serviço de geocodificação).

<br>

### 4.3 Coletar imagens de um bairro específico (exemplo: Faria Lima)

<br>

1. Coloque `geospatial_image_collection_faria_lima.ipynb` e `faria_lima_input.csv` na mesma pasta (`src/geospatial/`)
2. Abra o notebook e rode todas as células
3. Depois, faça a **triagem manual** dos tiles baixados (olhe um por um, descarte os que não têm heliponto visível)
4. Suba os selecionados para o Roboflow para anotação

<br><br>

## 5. Treinar os modelos

Treino exige **GPU** — sempre use Google Colab, nunca rode localmente.

<br>

### 5.1 exp1 (60 épocas, dataset original)

Isso já foi rodado pelo Pedro. Você não precisa rodar de novo, a menos que queira reproduzir.

<br>

### 5.2 exp2 (100 épocas, dataset original — o experimento oficial que falta)

<br>

1. Abra `src/training/yolo_training_exp2.ipynb` no Google Colab
2. Vá em **Runtime → Change runtime type → T4 GPU**
3. Rode o notebook célula por célula, de cima para baixo
4. Quando pedir a chave do Roboflow, cole a sua (não precisa ser a do Pedro — o dataset é público)
5. Se aparecer `AssertionError` na célula de download, **pare** e confira se o dataset baixado não é o fork por engano
6. No final, o notebook mostra os caminhos de tudo que foi salvo (pesos, ONNX, métricas)

<br>

**Depois de terminar:**

<br>

```bash
mkdir -p artifacts/runs/detect/exp2/weights
# copie best.pt e results.csv para esta pasta
```

<br>

### 5.3 exp3 (100 épocas, dataset forkado — já rodado, bônus)

Já está concluído. Se quiser rodar de novo sem gastar GPU (reaproveitando o modelo já treinado):

<br>

1. Abra `src/training/yolo_training_exp3.ipynb`
2. Rode a célula **"💡 Already trained this before? Skip GPU entirely"** em vez da célula de treino
3. Vá direto para as seções de Export ONNX, Comparison e Kepler

<br><br>

## 6. Rodar o dashboard localmente

<br>

```bash
cd /Users/fabicampanari/Desktop/3-project-ai-ml-yolo-helipad_detector
source .venv/bin/activate
streamlit run apps/streamlit_app/app.py
```

<br>

Ele abre automaticamente no navegador. Para parar: aperte `Ctrl+C` no terminal.

<br>

**O app funciona mesmo sem nenhum modelo treinado** — só as abas de detecção (Upload, Busca por Região, Amostras) ficam desativadas até existir um arquivo `best.pt`. O mapa, o pipeline e os downloads funcionam sempre.[^3]

<br><br>

## 7. Deploy no Streamlit Cloud

<br>

### 7.1 Primeiro, suba tudo para o GitHub (veja a Seção 8)ß

<br>

### 7.2 No navegador

<br>

1. Acesse **share.streamlit.io** e faça login com GitHub
2. Clique em **"New app"**
3. Preencha:
    - **Repository**: `Mindful-AI-Research/3-project-ai-ml-yolo-helipad_detector`
    - **Branch**: `main`
    - **Main file path**: `apps/streamlit_app/app.py`
4. Clique em **"Deploy!"**
5. Espere de 2 a 5 minutos o build terminar

<br><br>

## 8. Git — subir mudanças para o GitHub

### 8.1 Fluxo normal (sem conflitos)

<br>

```bash
git status
```

<br>

Mostra o que mudou.

<br>

```bash
git add .
git commit -m "descreva aqui o que você mudou"
git push
```

<br>

### 8.2 Autenticação (primeira vez ou se pedir senha)

O GitHub **não aceita mais senhas normais**. Use o GitHub CLI:

<br>

```bash
brew install gh
gh auth login
```

<br>

Responda:

- **GitHub.com**
- **HTTPS**
- **Yes** (autenticar o Git com as credenciais do GitHub)
- **Login with a web browser**

Copie o código mostrado, aperte Enter e confirme no navegador que abrir.

Depois disso, conecte o Git ao login:

<br>

```bash
gh auth setup-git
```

<br>

E confirme que a URL remota está correta:

<br>

```bash
git remote set-url origin https://github.com/Mindful-AI-Research/3-project-ai-ml-yolo-helipad_detector.git
```

<br>

### 8.3 ⚠️ Regra de ouro sobre `git push --force`

**Nunca use `--force` ou `--force-with-lease` sem ter certeza absoluta** de que:

- Ninguém mais está commitando direto no repositório sem passar pelo seu computador
- Você já rodou `git fetch` e olhou o que está no remoto antes de fazer isso
- Você sabe exatamente o que está sobrescrevendo

Se você editou algo direto no site do GitHub (no navegador) recentemente, **puxe isso para o seu computador primeiro** (`git pull`) antes de fazer qualquer `push --force` — senão a edição feita no navegador pode sumir (como aconteceu com o README, mas nós recuperamos).

<br>

### 8.4 Editando direto no GitHub (navegador)

Se você editar o README ou outro arquivo direto no site do GitHub, **sempre faça isso depois** no seu computador:

<br>

```bash
git pull
```

<br>

Antes de continuar trabalhando — assim você nunca fica com uma versão desatualizada que depois causa conflitos.

<br><br>

## 9. Erros comuns e como resolver

<br>

| Erro | Causa | Solução |
| :-- | :-- | :-- |
| `zsh: command not found: python` | Mac usa `python3`, não `python` | Troque `python` por `python3` em todos os comandos |
| `zsh: command not found: pip` | A mesma coisa, mas com pip | Use `python3 -m pip install ...` |
| `error: externally-managed-environment` | Tentando instalar fora do ambiente virtual | Confirme que `(.venv)` aparece no terminal; se não aparecer, rode `source .venv/bin/activate` |
| `.venv` aponta para o Python errado mesmo com `(.venv)` ativo | A pasta foi renomeada depois que o `.venv` foi criado | Apague e recrie: `rm -rf .venv && python3 -m venv .venv && source .venv/bin/activate` |
| `Password authentication is not supported` | GitHub não aceita mais senhas | Use GitHub CLI (`gh auth login`), veja a Seção 8.2 |
| `Personal access tokens (classic) are forbidden` | A organização bloqueia tokens antigos | Use GitHub CLI (`gh auth login`) em vez de token manual |
| `fatal: not a git repository` | O terminal está na pasta errada (`~` em vez do projeto) | Faça `cd` para a pasta correta do projeto primeiro |
| `KeyError: 'lat'` no dashboard | Falta o `sp_neighborhoods_bbox.csv` em `src/geospatial/` | Confirme que o arquivo está lá: `ls src/geospatial/sp_neighborhoods_bbox.csv` |
| `"No model found"` trava o app inteiro | Versão antiga do `app.py` sem o fix de tolerância | Use a versão mais recente do `app.py` (já corrigida) |
| Um link (`https://...`) dá `no such file or directory` no terminal | Você colou um link do navegador no terminal por engano | Links vão na **barra de endereço do navegador**, não no terminal. Ou use `open "URL"` no Mac para abrir automaticamente |
| Tela cheia de texto com `:` piscando no final, o terminal não responde | Você entrou no modo de visualização `less` (comum depois de `git log`, `git branch -r` etc.) | Aperte **`q`** para sair |

<br>

**Dica final:** sempre que um comando der erro, copie a mensagem completa (não só a última linha) — o erro geralmente já diz exatamente o que está errado, só precisa ler com calma.


