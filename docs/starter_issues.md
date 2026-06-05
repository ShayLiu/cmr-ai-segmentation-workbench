# Starter Issues

These are good first issues for turning the workbench into a more useful research project.

## 1. Add ACDC Baseline

Goal: provide a public benchmark result that others can reproduce.

Acceptance criteria:

- ACDC preparation instructions are complete.
- Training command is documented.
- Dataset source and split are described.
- Dice and HD95 are reported.
- At least one prediction overlay is shown.

## 2. Add Evaluation Metrics

Goal: compute segmentation metrics from prediction and label folders.

Acceptance criteria:

- Dice is reported per label and averaged.
- HD95 is reported when spacing is available.
- Output can be saved as CSV and Markdown.
- Example command is documented.

## 3. Add Prediction Overlay Visualization

Goal: make results easier to inspect and share.

Acceptance criteria:

- Input image, label, and prediction can be overlaid.
- Output is saved as PNG.
- Works with single case NIfTI files.
- Includes an example in `docs/`.

## 4. Add MONAI Baseline

Goal: provide a second implementation path beyond nnU-Net.

Acceptance criteria:

- Minimal MONAI training script is added.
- Dataset format expectations are documented.
- Tiny smoke test is supported.

## 5. Document CMR DICOM Pitfalls

Goal: help clinical researchers avoid common conversion mistakes.

Acceptance criteria:

- Covers slice/time ordering.
- Covers cine SAX frame handling.
- Covers spacing and orientation.
- Covers privacy metadata concerns.
