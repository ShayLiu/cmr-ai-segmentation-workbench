# 30 / 60 / 90 Day Growth Plan

## Positioning

Build a practical cardiac MRI AI segmentation workbench for medical researchers.

The project should not be a simple clone of nnU-Net or MONAI. Its value is the complete research workflow: data formatting, training, prediction, evaluation, visualization, troubleshooting, and paper-ready reporting.

## Days 1-30: Reproducible Baseline

Main goal: run one public dataset from raw data to prediction.

Tasks:

- Choose the first dataset: ACDC cardiac MRI is recommended.
- Install nnU-Net v2 in a clean environment.
- Convert the dataset into nnU-Net v2 format.
- Train a 2D baseline model.
- Run prediction on validation or test cases.
- Save training logs and example predictions.
- Write a clear README with exact commands.
- Add medical data privacy warnings.

Deliverables:

- `scripts/prepare_acdc.py`
- `scripts/train_nnunet_acdc.sh`
- `scripts/predict_nnunet_acdc.sh`
- `results/acdc_nnunet_baseline.md`
- Example input, label, and prediction images.

Success criteria:

- A new user can reproduce the baseline by following the README.
- The repository has one visible result figure and one metrics table.

## Days 31-60: Research Utility

Main goal: make the repository useful for actual medical AI experiments.

Tasks:

- Add Dice and HD95 evaluation.
- Add visual overlays for segmentation masks.
- Add troubleshooting documentation.
- Add a guide for DICOM to NIfTI conversion.
- Add a MONAI baseline or MONAI preprocessing example.
- Add environment export files.
- Add GitHub issue templates.
- Publish `v0.1.0` release.

Deliverables:

- `scripts/evaluate_segmentation.py`
- `scripts/visualize_prediction.py`
- `docs/troubleshooting.md`
- `docs/dicom_to_nifti.md`
- `results/acdc_metrics.md`

Success criteria:

- Users can train, predict, evaluate, and visualize results.
- The repository looks like a serious open-source project, not a note dump.

## Days 61-90: Differentiation

Main goal: make the project distinct from generic nnU-Net tutorials.

Tasks:

- Add cardiac MRI-specific notes: LV, RV, myocardium labels.
- Add common clinical metrics: ventricular volume, ejection fraction if feasible.
- Add MedSAM adaptation or prompt-based segmentation example.
- Add Chinese documentation for medical researchers.
- Add a paper-style results template.
- Add model weight hosting instructions for Hugging Face or Zenodo.
- Write a public tutorial article.

Deliverables:

- `docs/cardiac_mri_labels.md`
- `scripts/compute_cardiac_metrics.py`
- `docs/zh_quickstart.md`
- `docs/paper_results_template.md`
- `results/v0.2_summary.md`

Success criteria:

- The repository has a clear niche: cardiac MRI segmentation research workflow.
- It can be shown to collaborators, supervisors, or open-source users.

