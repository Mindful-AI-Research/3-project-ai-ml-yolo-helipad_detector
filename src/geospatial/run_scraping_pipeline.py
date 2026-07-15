#!/usr/bin/env python3
"""
run_scraping_pipeline.py — Orchestrates the two automated geospatial discovery
steps into a single command, instead of running each script separately.

    1) helipad_scraper.py        -> src/geospatial/helipad_coordinates_raw.csv
    2) transform_coordinates.py  -> src/geospatial/helipad_coordinates_bbox.csv

The third step (satellite tile download + visual triage, in
geospatial_image_collection.ipynb) stays manual on purpose — it involves
reviewing mosaics visually before sending images to Roboflow, which is not
something that should be fully automated.

USAGE
-----
    python src/geospatial/run_scraping_pipeline.py

This just calls the two existing scripts in order, in the same process space
they already expect (relative paths, same folder), so neither script needs
to be modified.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_SCRAPER_CANDIDATES = ["helipad_scraper.py", "helipad_bot.py", "BOTHELIPONTO.py"]
SCRAPER = next((HERE / name for name in _SCRAPER_CANDIDATES if (HERE / name).exists()), HERE / _SCRAPER_CANDIDATES[0])
TRANSFORMER = HERE / "transform_coordinates.py"
RAW_CSV = HERE / "helipad_coordinates_raw.csv"
BBOX_CSV = HERE / "helipad_coordinates_bbox.csv"


def run_step(title: str, script: Path, extra_args: list[str] | None = None) -> None:
    print(f"\n{'='*60}")
    print(f"  STEP: {title}")
    print(f"{'='*60}\n")
    if not script.exists():
        sys.exit(f"[ERROR] Script not found: {script}")
    cmd = [sys.executable, str(script)] + (extra_args or [])
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(f"[ERROR] '{script.name}' exited with code {result.returncode}. Stopping pipeline.")


def main() -> None:
    print("Helipad discovery pipeline — scraping + coordinate conversion")
    print(f"Working directory: {HERE}")
    print(f"Using scraper script: {SCRAPER.name}")

    # Step 1: scraping (interactive — will ask how many helipads to collect).
    # --output is passed explicitly: the scraper's own default
    # ("helipontos_resultado.csv") doesn't match RAW_CSV below, and relying
    # on it silently breaks the existence check after this step.
    run_step("1/2 — Scraping helipad records (Selenium)", SCRAPER, ["--output", str(RAW_CSV)])

    if not RAW_CSV.exists():
        sys.exit(
            f"[ERROR] Expected output not found: {RAW_CSV}\n"
            "The scraper may have been interrupted before saving any results."
        )

    # Step 2: coordinate conversion (non-interactive). Positional args passed
    # explicitly for the same reason — transform_coordinates.py's own no-arg
    # defaults ("helipontos_resultado.csv" -> "cordenadasheli.csv") don't
    # match this pipeline's filenames.
    run_step("2/2 — Converting coordinates to bounding boxes", TRANSFORMER, [str(RAW_CSV), str(BBOX_CSV)])

    if BBOX_CSV.exists():
        print(f"\n✅ Pipeline complete. Output ready at:\n   {BBOX_CSV}")
        print(
            "\nNext manual step: open geospatial_image_collection.ipynb to download "
            "satellite tiles and build mosaics for visual triage."
        )
    else:
        sys.exit(f"[ERROR] Expected output not found: {BBOX_CSV}")


if __name__ == "__main__":
    main()
