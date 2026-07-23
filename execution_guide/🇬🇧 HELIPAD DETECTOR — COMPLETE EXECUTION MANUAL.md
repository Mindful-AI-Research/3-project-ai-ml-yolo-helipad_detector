

# 🚁 Helipad Detector — Complete Execution Manual

A step-by-step guide to run the entire project from scratch: environment setup, data automation, training, dashboard, deployment, and Git. Written to be followed by copying and pasting the commands, with no guesswork needed.[^1][^2]

<br><br>

## 📋 Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Set up the environment for the first time](#2-set-up-the-environment-for-the-first-time)
3. [Daily routine (every time you work)](#3-daily-routine-every-time-you-work)
4. [Data collection automation (scraping)](#4-data-collection-automation-scraping)
5. [Train the models (exp1, exp2, exp3)](#5-train-the-models)
6. [Run the dashboard locally](#6-run-the-dashboard-locally)
7. [Deploy to Streamlit Cloud](#7-deploy-to-streamlit-cloud)
8. [Git — push changes to GitHub](#8-git--push-changes-to-github)
9. [Common errors and how to fix them](#9-common-errors-and-how-to-fix-them)

<br><br>

## 1. Prerequisites

Before you start, you need to have the following installed:

- **Python 3** (on Mac, it is usually already installed)
- **Git** (usually already installed on Mac)
- **Homebrew** (Mac package manager) — if you do not have it:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

- A **GitHub** account with access to the repository
- A **Roboflow** account (to download the dataset)
- A **Google** account (to use Google Colab for GPU training)

<br><br>

## 2. Set up the environment for the first time

You only need to do this **once** (or again if you delete the `.venv` folder).

<br>

### 2.1 Go into the project folder

```bash
cd /Users/fabicampanari/Desktop/3-project-ai-ml-yolo-helipad_detector
```
<br>

> ⚠️ If the folder has a different name on your computer, adjust the path above.

<br>

### 2.2 Create the virtual environment

<br>

```bash
python3 -m venv .venv
```
<br>

### 2.3 Activate the virtual environment

```bash
source .venv/bin/activate
```
<br>

> The beginning of the terminal line should change to show `(.venv)` in front.

<br>

### 2.4 Install all dependencies

<br>

```bash
python3 -m pip install -r requirements.txt
```

<br>

> ⚠️ **Never use only `pip install`** — always use `python3 -m pip install`, otherwise it may install in the wrong place on your computer and trigger the `externally-managed-environment` error.

<br><br>

## 3. Daily routine

Every time you work on the project (after the initial setup), this is all you need:

<br>

```bash
cd /Users/fabicampanari/Desktop/3-project-ai-ml-yolo-helipad_detector
source .venv/bin/activate
```
<br>

Confirm that it worked:

```bash
which python3
```
<br>

It should show a path **inside** the project folder, ending in `.venv/bin/python3`. If it shows `/opt/homebrew/bin/python3` or something similar (without `.venv` in the middle), the virtual environment was not activated correctly — run `source .venv/bin/activate` again.

<br><br>

## 4. Data collection automation (scraping)

### 4.1 Run the full pipeline

<br>

```bash
python3 src/geospatial/run_scraping_pipeline.py
```

<br>

It will ask how many helipads to collect — type a number (for example, `150`) and press Enter.

<br>

> ⏳ This may take quite a while (the site is visited slowly on purpose, one page at a time, with pauses in between). Let it run in the background.


<br>

**Expected output:**

<br>

```
✅ Pipeline complete. Output ready at:
   src/geospatial/helipad_coordinates_bbox.csv
```

<br>

### 4.2 Separate São Paulo from other states (optional)

<br>

```bash
python3 src/geospatial/geocode_states.py
```
<br>

This generates `helipad_coordinates_com_estado.csv` with an extra column indicating the state of each helipad. It takes about 1 second per row (to respect the geocoding service rate limit).

<br>

### 4.3 Collect images from a specific neighborhood (example: Faria Lima)

<br>

1. Put `geospatial_image_collection_faria_lima.ipynb` and `faria_lima_input.csv` in the same folder (`src/geospatial/`)
2. Open the notebook and run all cells
3. Then do the **manual triage** of the downloaded tiles (check them one by one, discard the ones without a visible helipad)
4. Upload the selected ones to Roboflow for annotation

<br><br>

## 5. Train the models

Training requires a **GPU** — always use Google Colab, never run it locally.

<br>

### 5.1 exp1 (60 epochs, original dataset)

This has already been run by Pedro. You do not need to run it again unless you want to reproduce it.

<br>

### 5.2 exp2 (100 epochs, original dataset — the missing official experiment)

<br>

1. Open `src/training/yolo_training_exp2.ipynb` in Google Colab
2. Go to **Runtime → Change runtime type → T4 GPU**
3. Run the notebook cell by cell, from top to bottom
4. When it asks for the Roboflow key, paste yours (it does not need to be Pedro’s — the dataset is public)
5. If `AssertionError` appears in the download cell, **stop** and check whether the downloaded dataset is the fork by mistake
6. At the end, the notebook shows the paths for everything that was saved (weights, ONNX, metrics)

<br>

**After it finishes:**

<br>

```bash
mkdir -p artifacts/runs/detect/exp2/weights
# copy best.pt and results.csv into this folder
```

<br>


### 5.3 exp3 (100 epochs, forked dataset — already run, bonus)

Already completed. If you want to run it again without spending GPU time (reusing the already trained model):

<br>

1. Open `src/training/yolo_training_exp3.ipynb`
2. Run the cell **"💡 Already trained this before? Skip GPU entirely"** instead of the training cell
3. Go straight to the ONNX Export, Comparison, and Kepler sections

<br><br>

## 6. Run the dashboard locally

<br>

```bash
cd /Users/fabicampanari/Desktop/3-project-ai-ml-yolo-helipad_detector
source .venv/bin/activate
streamlit run apps/streamlit_app/app.py
```

<br>

It opens automatically in the browser. To stop it: press `Ctrl+C` in the terminal.

<br>

**The app works even without any trained model** — only the detection tabs (Upload, Region Search, Samples) stay disabled until a `best.pt` file exists. The map, pipeline, and downloads always work.[^3]

<br><br>

## 7. Deploy to Streamlit Cloud

<br>

### 7.1 First, push everything to GitHub (see Section 8)ß

<br>

### 7.2 In the browser

<br>

1. Go to **share.streamlit.io** and sign in with GitHub
2. Click **"New app"**
3. Fill in:
    - **Repository**: `Mindful-AI-Research/3-project-ai-ml-yolo-helipad_detector`
    - **Branch**: `main`
    - **Main file path**: `apps/streamlit_app/app.py`
4. Click **"Deploy!"**
5. Wait 2 to 5 minutes for the build to finish

<br><br>

## 8. Git — push changes to GitHub

### 8.1 Normal flow (no conflicts)

<br>

```bash
git status
```
<br>

Shows what changed.

<br>

```bash
git add .
git commit -m "describe what you changed here"
git push
```
<br>

### 8.2 Authentication (first time or if it asks for a password)

GitHub **no longer accepts regular passwords**. Use GitHub CLI:

<br>

```bash
brew install gh
gh auth login
```
<br>

Answer:

- **GitHub.com**
- **HTTPS**
- **Yes** (authenticate Git with GitHub credentials)
- **Login with a web browser**

Copy the code shown, press Enter, and confirm in the browser that opens.

After that, connect Git to the login:

<br>

```bash
gh auth setup-git
```
<br>

And confirm that the remote URL is correct:

<br>

```bash
git remote set-url origin https://github.com/Mindful-AI-Research/3-project-ai-ml-yolo-helipad_detector.git
```
<br>

### 8.3 ⚠️ Golden rule about `git push --force`

**Never use `--force` or `--force-with-lease` unless you are absolutely sure** that:

- Nobody else is committing directly to the repository without going through your computer
- You already ran `git fetch` and checked what is on the remote before doing it
- You know exactly what you are overwriting

If you edited something directly on the GitHub website (in the browser) recently, **pull it to your computer first** (`git pull`) before doing any `push --force` — otherwise the browser edit may disappear (like what happened with the README, but we recovered it).

<br>

### 8.4 Editing directly on GitHub (browser)

If you edit the README or another file directly on the GitHub website, **always do this afterward** on your computer:

<br>

```bash
git pull
```
<br>

Before continuing to work — that way you never stay with an outdated version that later causes conflicts.

<br><br>

## 9. Common errors and how to fix them

| Error | Cause | Solution |
| :-- | :-- | :-- |
| `zsh: command not found: python` | Mac uses `python3`, not `python` | Replace `python` with `python3` in every command |
| `zsh: command not found: pip` | Same thing, but for pip | Use `python3 -m pip install ...` |
| `error: externally-managed-environment` | Trying to install outside the virtual environment | Make sure `(.venv)` appears in the terminal; if not, run `source .venv/bin/activate` |
| `.venv` points to the wrong Python even with `(.venv)` active | The folder was renamed after `.venv` was created | Delete and recreate it: `rm -rf .venv && python3 -m venv .venv && source .venv/bin/activate` |
| `Password authentication is not supported` | GitHub no longer accepts passwords | Use GitHub CLI (`gh auth login`), see Section 8.2 |
| `Personal access tokens (classic) are forbidden` | The organization blocks old tokens | Use GitHub CLI (`gh auth login`) instead of a manual token |
| `fatal: not a git repository` | The terminal is in the wrong folder (`~` instead of the project) | `cd` into the correct project folder first |
| `KeyError: 'lat'` in the dashboard | Missing `sp_neighborhoods_bbox.csv` in `src/geospatial/` | Confirm that the file is there: `ls src/geospatial/sp_neighborhoods_bbox.csv` |
| `"No model found"` freezes the whole app | Old version of `app.py` without the tolerance fix | Use the latest version of `app.py` (already fixed) |
| A link (`https://...`) throws `no such file or directory` in the terminal | You pasted a browser link into the terminal by mistake | Links go into the **browser address bar**, not the terminal. Or use `open "URL"` on Mac to open it automatically |
| Full screen of text with `:` blinking at the end, terminal does not respond | You entered `less` viewer mode (common after `git log`, `git branch -r`, etc.) | Press **`q`** to exit |

<br><br>


**Final tip:** whenever a command fails, copy the full error message (not just the last line) — the error usually tells you exactly what is wrong, you just need to read it carefully.


