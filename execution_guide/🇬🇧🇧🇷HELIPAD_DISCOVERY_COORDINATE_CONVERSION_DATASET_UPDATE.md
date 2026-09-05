
# Execution Guide — Helipad Discovery, Coordinate Conversion & Dataset Update

This tutorial explains how to run the **Helipad Bot** to discover new helipad locations, convert the collected coordinates into the format used by the application, and add the new records to the existing dataset.

<br><br>

### Process Flow

<br>

```text
Helipad Bot
     │
     │ Discovers new locations
     ▼
helipontos_resultado.csv
     │
     │ Converts the coordinates
     ▼
helipontos_convertido.csv
     │
     │ Adds to the existing data
     ▼
Updated Dataset
     │
     ▼
Map / Application
```

<br>

> **Important:** the discovery stage may take a considerable amount of time. Leave the process running until the bot finishes.

<br><br>

## 1. Install Firefox and GeckoDriver

**This step is only required during the initial setup.**

The bot uses **Selenium** to automatically control the Firefox browser.

### Install Firefox

```bash
brew install --cask firefox
```

### Install GeckoDriver

```bash
brew install geckodriver
```

<br><br>

## 2. Place `helipad_bot.py` in the Correct Location

The `helipad_bot.py` file must be located inside:

```text
src/geospatial/
```

<br>

> alongside the other files related to geospatial processing.

Example:

```text
src/geospatial/
├── helipad_bot.py
├── transform_coordinates.py
└── geospatial_image_collection.ipynb
```

<br><br>

## 3. Open the Terminal in the Project Directory

Run:

```bash
cd "/Users/fabicampanari/Desktop/3-project-ai-ml-yolo-helipad_detector"
```

<br><br>

## 4. Activate the Virtual Environment

Run:

```bash
source .venv/bin/activate
```

<br><br>

## 5. Install the Dependencies

Run:

```bash
pip install -r requirements.txt
```

<br>

> This command installs the libraries required to run the project, including **Selenium** and **WebDriver Manager**.

<br><br>

## 6. Run the Helipad Bot

Run:

```bash
python src/geospatial/helipad_bot.py
```

The Terminal will prompt:

```text
Quantidade:
```

Enter, for example:

```text
500
```

and press **Enter**.

<br>

> The bot will launch Firefox in **headless mode**, running the browser automatically in the background.
>
> During this stage, the bot will navigate through the required pages to **discover new helipad locations and collect their information**.

<br><br>

> [!WARNING]
> **Important:** this stage may take a considerable amount of time. Do not close the Terminal while the bot is running.

<br><br>

When the process is complete, the following file will be created:

```text
helipontos_resultado.csv
```

<br>

> This file contains the **new results discovered by the bot**.

<br><br>

## 7. Convert the Coordinates

The newly discovered helipads contain coordinates in **degrees, minutes, and seconds (DMS)** format.

They must now be converted to **decimal degrees**, the format used by the application's map.

Run:

```bash
python src/geospatial/transform_coordinates.py helipontos_resultado.csv helipontos_convertido.csv
```

<br>

The following file will be generated:

```text
helipontos_convertido.csv
```

<br>

> This file contains the newly discovered helipads with their coordinates converted to decimal format.

<br><br>

## 8. Add the New Helipads to the Existing Dataset

The `helipontos_convertido.csv` file contains the **newly discovered locations**.

To add them to the file that already contains the existing helipads, without duplicating the CSV header, run:

```bash
tail -n +2 helipontos_convertido.csv >> src/geospatial/helipontos.csv
```

<br>

> The `tail -n +2` command skips the first line of the file, which contains the header, and appends only the new records to the end of the existing dataset.

<br>

### Result

```text
Existing Helipads
        +
Newly Discovered Helipads
        ↓
Updated Dataset
        ↓
Map / Application
```

<br><br>

## Summary

The complete process is:

**1. Discover new helipads**

→ **2. Generate `helipontos_resultado.csv`**
→ **3. Convert the coordinates**
→ **4. Generate `helipontos_convertido.csv`**
→ **5. Add the new records to the existing dataset**
→ **6. Use the updated data in the application.**
