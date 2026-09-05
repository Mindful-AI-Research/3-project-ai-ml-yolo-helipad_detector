
# Guia Execucao  - Descoberta de Helipontos, Conversão de Coordenadas e Atualização do Dataset

Este tutorial explica como executar o **Helipad Bot** para descobrir novos locais de helipontos, converter as coordenadas coletadas para o formato utilizado pela aplicação e adicionar os novos registros ao dataset existente.

<br><br>


### Fluxo do processo

<br>

```text
Helipad Bot
     │
     │ Descobre novos locais
     ▼
helipontos_resultado.csv
     │
     │ Converte as coordenadas
     ▼
helipontos_convertido.csv
     │
     │ Adiciona aos dados existentes
     ▼
Dataset atualizado
     │
     ▼
Mapa / Aplicação
```

<br>

> **Importante:** a etapa de descoberta pode levar bastante tempo. Deixe o processo rodando até que o bot termine.

<br><br>

## 1. Instale o Firefox e o GeckoDriver

**Essa etapa é necessária somente na primeira configuração.**

O bot utiliza o **Selenium** para controlar o navegador Firefox automaticamente.

### Instale o Firefox

```bash
brew install --cask firefox
```

### Instale o GeckoDriver

```bash
brew install geckodriver
```

<br><br>

## 2. Coloque o `helipad_bot.py` no local correto

O arquivo `helipad_bot.py` deve estar dentro da pasta:

```text
src/geospatial/
```

<br>

> junto aos demais arquivos relacionados ao processamento geoespacial.

Exemplo:

```text
src/geospatial/
├── helipad_bot.py
├── transform_coordinates.py
└── geospatial_image_collection.ipynb
```

<br><br>

## 3. Abra o Terminal na pasta do projeto

Execute:

```bash
cd "/Users/fabicampanari/Desktop/3-project-ai-ml-yolo-helipad_detector"
```

<br><br>

## 4. Ative o ambiente virtual

Execute:

```bash
source .venv/bin/activate
```

<br><br>
      
## 5. Instale as dependências

Execute:

```bash
pip install -r requirements.txt
```

<br>

> Esse comando instala as bibliotecas necessárias para executar o projeto, incluindo **Selenium** e **WebDriver Manager**.

<br><br>

## 6. Execute o Helipad Bot

Execute:

```bash
python src/geospatial/helipad_bot.py
```

O Terminal solicitará:

```text
Quantidade:
```

Digite, por exemplo:

```text
500
```

e pressione **Enter**.

<br>

> O bot iniciará o Firefox em **modo headless**, executando o navegador automaticamente em segundo plano.
> 
> Durante essa etapa, o bot navegará pelas páginas necessárias para **descobrir novos locais de helipontos e coletar suas informações**.


<br><br>


>  [!WARNING]
> **Importante:** essa etapa pode demorar bastante. Não encerre o Terminal enquanto o bot estiver executando.

<br><br>

Ao finalizar, será criado:

```text
helipontos_resultado.csv
```

<br>

> Esse arquivo contém os **novos resultados encontrados pelo bot**.

<br><br>

## 7. Converta as coordenadas

Os novos helipontos coletados possuem as coordenadas no formato de **graus, minutos e segundos (DMS)**.

Agora é necessário convertê-las para **graus decimais**, formato utilizado pelo mapa da aplicação.

Execute:

```bash
python src/geospatial/transform_coordinates.py helipontos_resultado.csv helipontos_convertido.csv
```

<br>

Será gerado:

```text
helipontos_convertido.csv
```

<br>

> Esse arquivo contém os novos helipontos com as coordenadas convertidas para o formato decimal.

<br><br>


## 8. Adicione os novos helipontos ao dataset existente

O arquivo `helipontos_convertido.csv` contém os **novos pontos encontrados**.

Para adicioná-los ao arquivo que já contém os helipontos existentes, sem duplicar o cabeçalho do CSV, execute:

```bash
tail -n +2 helipontos_convertido.csv >> src/geospatial/helipontos.csv
```

<br>

> O comando `tail -n +2` ignora a primeira linha do arquivo, que corresponde ao cabeçalho, e adiciona somente os novos registros ao final do dataset existente.


<br>

### Resultado

```text
Helipontos existentes
        +
Novos helipontos descobertos
        ↓
Dataset atualizado
        ↓
Mapa / Aplicação
```

<br><br>

## Resumo

O processo completo é:

**1. Descobrir novos helipontos**

→ **2. Gerar `helipontos_resultado.csv`**
→ **3. Converter as coordenadas**
→ **4. Gerar `helipontos_convertido.csv`**
→ **5. Adicionar os novos registros ao dataset existente**
→ **6. Utilizar os dados atualizados na aplicação.**


