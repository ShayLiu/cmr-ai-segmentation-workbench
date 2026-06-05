# Model and Data Statement

This repository is a research workbench for cardiac MRI segmentation workflows.

## Data

The repository does not distribute private clinical data, DICOM files, NIfTI files, trained checkpoints, or prediction files.

Public examples should use public datasets with clear redistribution and citation terms. Private-data workflows should keep all raw images, annotations, source manifests, and model artifacts outside Git.

README preview images may use derived visualizations from public datasets when the source license permits reuse and the dataset is cited. They should never use private clinical images.

## Pseudo-Labels

Some workflows can prepare nnU-Net datasets from locally generated pseudo-labels, such as CorSeg segmentation outputs. These pseudo-labels are useful for pipeline development and weak-supervision experiments, but they are not equivalent to manual expert annotations.

Results from pseudo-label runs should not be presented as clinical model performance.

## Intended Use

- Reproducible cardiac MRI segmentation experiments
- Dataset formatting and preprocessing examples
- Debug training runs for research workflows
- Documentation templates for medical imaging AI projects

## Out of Scope

- Clinical diagnosis or treatment decisions
- Regulatory or deployment claims
- Redistribution of private patient data
- Performance claims without appropriate validation

## Recommended Validation

Before making scientific claims, evaluate on expert-labeled data with a prespecified protocol. Report dataset source, cohort definition, labels, hardware, preprocessing, model configuration, cross-validation strategy, Dice, HD95 or related metrics, and failure modes.
