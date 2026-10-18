## [Lineage audit: where the files came from]()

<br><br>

> Automated image-based visual detection, subject to errors and not equivalent to operational, legal, safety or aeronautical validation. This folder concerns data lineage, not the validation of sites.

<br><br>

## [Origin of the files]()

<br>

### [***Field inventory***]()

`field_tiles_inventory.csv` and `field_tiles_inventory_raw.csv` were **reconstructed from the zip archives** `src/geospatial/mosaic_*/mosaic_*.zip` (`main` branch, revision `9e767ec1f8d711b4e09f920aadf802c3855acb9a`). The main inventory has 7,767 rows (region × tile pairs, equal to the historical set) and 5,540 distinct tile identifiers; the `raw` file keeps the 8,083 raw zip entries.

<br>

### [***Annotated images***]()

`train_valid_test_tiles_overlap.csv` covers the 226 images in `data/training/exp1` (revision `bc5a0ad953e4ffc8433d3e3f68d245068ebddc5a`), whose content is identical to `data/training/exp2` and to the `My-First-Project-2` folder in Pedro Vyctor Almeida's repository (dataset version 2: 178 train, 34 validation, 14 test).

<br>

### [***Summary and criteria***]()

`overlap_summary.json` gathers the criteria, denominators and totals used in `docs/evidence/relatorio_evidencias_exp1_exp2.docx`.

<br><br>

## [Main columns]()

<br>

### [***field_tiles_inventory.csv***]()

`tile_id`, `original_name`, `region_folder`, `z`, `x`, `y`, `path_in_zip`, `zip_files`, `n_copies_in_zips`, `copies_identical_crc`, `size_bytes`, `crc32`, `n_regions_with_tile`.

<br>

### [***train_valid_test_tiles_overlap.csv***]()

`split`, `original_name`, `name_tile_id`, `name_id_shared_by_n_images`, `pixel_best_field_tile`, `pixel_mae256`, `pixel_match_le5`, `resolved_tile_id`, `resolved_by`, `z`, `x`, `y`, `in_field_exact`, `field_regions`, `min_chebyshev_to_field`, `field_within_1/2/3/5`, `train_same_tile_id`, `train_min_chebyshev`.

<br><br>

## [Criteria]()

<br>

### [***How to read the numbers***]()

- **Pixel copy:** mean absolute error (0–255) of 5 or less between the annotated image and the most similar field tile (32×32 pre-filter, measured at 256×256). All matches are at 1.56 or below; no other image falls below 16.9.
- **Identifier from the file name:** z/x/y read from the file name; unreliable when several images share the same tile name (23 Itaim Bibi images).
- **Neighbourhood:** Chebyshev distance in z19 tiles (about 70 m, approximation). A neighbour is not confirmed leakage.

<br><br>

## [Limitations and open items]()

<br>

### [***What is not covered***]()

- Rotated, cropped, rescaled or different-date copies are not detected by the pixel criterion.
- There are no per-tile detections in the materials, so the effect of the overlap on field rates was not computed.
- 176 Faria Lima tiles are missing from the inventory (840 in the history versus 664 distinct in the zips), and the Av. Paulista split shifts 5 tiles.
- The scripts that generated these files are not yet versioned: **Unknown in the materials provided.** Without them the numbers cannot be reproduced by third parties; version them under `src/geospatial/` before citing the numbers as reproducible.
