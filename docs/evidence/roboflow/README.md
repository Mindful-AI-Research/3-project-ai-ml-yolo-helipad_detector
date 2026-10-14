# Roboflow dataset evidence

Screenshots captured on October 13–14, 2026, documenting the
original Roboflow project and Fabiana's fork.

## Files

- `pedro_original_v2_dataset.jpg`
  Original project's v2: 226 images, comprising 178 training,
  34 validation, and 14 test images. The page displays a generation
  date of June 22, 2026.

- `pedro_original_v1_access_blank.jpg`
  Direct access attempt to the original project's `/dataset/1`
  page. The main content area appeared blank. This does not establish
  that v1 never existed or was deleted.

- `fabiana_fork_versions_and_model.jpg`
  Fork version list showing v1 and v2, each displaying 404 images,
  and a trained model associated with v2.

- `fabiana_fork_v2_dataset_details.jpg`
  Fork v2 details: 356 training, 34 validation, and 14 test images.
  Preprocessing: stretch resize to 640 × 640.
  Augmentation settings: two outputs per training example,
  horizontal and vertical flips, rotation from -15° to +15°,
  and brightness adjustment from -25% to +25%.

## Interpretation limits

These screenshots document the information displayed in Roboflow
at the time of capture. They do not, by themselves, establish which
dataset export produced the final metrics or weights of exp1 or exp2.

The fork's version numbering must not be assumed to match the
original project's version numbering.

The model metrics displayed in Roboflow must not be attributed to
the Colab exp2 execution without verifying the correspondence between
the execution, dataset, and model artifacts.
