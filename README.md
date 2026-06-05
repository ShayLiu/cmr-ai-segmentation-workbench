# CMR AI Segmentation Workbench

![CMR AI Segmentation Workbench banner](docs/assets/cmr_workbench_banner.svg)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](requirements.txt)
[![nnU-Net](https://img.shields.io/badge/nnU--Net-v2-informational.svg)](https://github.com/MIC-DKFZ/nnUNet)
[![Medical Data](https://img.shields.io/badge/private%20data-not%20included-critical.svg)](docs/model_and_data_statement.md)

An open, privacy-conscious, reproducible workbench for cardiac MRI segmentation research.

This project is designed for medical researchers, students, and engineers who want to train, evaluate, and document cardiac MRI segmentation models with reproducible workflows.

The first milestones use nnU-Net v2 for synthetic smoke tests, public cardiac MRI debug runs, and local pseudo-label workflows. Later milestones add ACDC baselines, MONAI, MedSAM, visualization, metrics, and paper-ready outputs.

![Workflow overview](docs/assets/workflow_overview.svg)

## Why This Exists

Cardiac MRI AI projects often spend more time on data formatting, DICOM/NIfTI conversion, nnU-Net folder structure, privacy checks, and result documentation than on the model itself.

This repository aims to make that workflow explicit, teachable, and reusable.

## What You Can Do in 5 Minutes

Create a tiny privacy-safe nnU-Net-style dataset and verify the project structure:

```bash
pip install -r requirements.txt
python scripts/create_tiny_nnunet_dataset.py \
  --output /tmp/nnunet_raw \
  --dataset-id 901 \
  --num-training 5
```

This does not require private medical data.

## Current Status

| Workflow | Dataset type | Status | Notes |
|---|---|---|---|
| Tiny smoke test | Synthetic | Done | Verifies environment and nnU-Net formatting |
| MSD Cardiac debug run | Public dataset | Done | Real public medical image debug training |
| CorSeg SAX pseudo-label run | Private local workflow | Done | Privacy-preserving pseudo-label pipeline validation |
| ACDC baseline | Public benchmark | Planned | Next major reproducibility milestone |

The project is not a clinical model and does not include private patient data, trained checkpoints, DICOM files, or NIfTI files.

![Completed debug runs](docs/assets/debug_runs_summary.svg)

## SAX Segmentation QC

The local CorSeg SAX pseudo-label run proves that the data conversion and nnU-Net workflow can run end to end, but its boundaries are not accurate enough to present as a segmentation result. This repository therefore treats pseudo-label output as a quality-control and workflow-validation artifact only.

![SAX segmentation quality gate](docs/assets/segmentation_qc_gate.svg)

Publication-grade SAX LV/RV figures should come from expert-labeled data or a public benchmark such as ACDC, with structure-wise Dice and HD95 reported before any visual showcase.

## Goals

- Reproduce a strong cardiac MRI segmentation baseline with nnU-Net v2.
- Provide clean scripts for data preparation, training, prediction, and evaluation.
- Make medical imaging AI workflows easier for clinical researchers to understand and repeat.
- Document common problems in DICOM/NIfTI conversion, dataset formatting, GPU setup, and segmentation evaluation.

## Quick Links

- [Quickstart](docs/quickstart.md)
- [Data format guide](docs/data_format.md)
- [Model and data statement](docs/model_and_data_statement.md)
- [Release checklist](docs/release_checklist.md)
- [Promotion kit](docs/promotion_kit.md)
- [Launch plan](docs/launch_plan.md)
- [Starter issues](docs/starter_issues.md)
- [Changelog](CHANGELOG.md)
- [Completed debug results](results/)

## Roadmap

| Stage | Goal | Status |
|---|---|---|
| 0 | Project scaffold and documentation | In progress |
| 1 | Local tiny nnU-Net smoke test | Done |
| 2 | Public MSD Cardiac debug training | Done |
| 3 | Local CorSeg SAX pseudo-label debug training | Done |
| 4 | nnU-Net v2 ACDC baseline training | Planned |
| 5 | Dice / HD95 evaluation script | Script ready |
| 6 | Prediction visualization examples | Script ready |
| 7 | MONAI baseline | Planned |
| 8 | MedSAM adaptation example | Planned |
| 9 | CMR research template for papers | Planned |

## Recommended First Experiment

Use ACDC cardiac MRI data with nnU-Net v2.

```bash
conda create -n cmr-nnunet python=3.10 -y
conda activate cmr-nnunet
pip install nnunetv2
```

Set nnU-Net paths:

```bash
export nnUNet_raw=/path/to/nnUNet_raw
export nnUNet_preprocessed=/path/to/nnUNet_preprocessed
export nnUNet_results=/path/to/nnUNet_results
```

Prepare and train:

```bash
python scripts/prepare_acdc.py \
  --source /path/to/acdc_raw \
  --output "$nnUNet_raw/Dataset001_ACDC"

DATASET_ID=1 CONFIG=2d FOLD=0 DEVICE=cuda bash scripts/train_nnunet_acdc.sh
```

Predict:

```bash
bash scripts/predict_nnunet_acdc.sh
```

Evaluate and create a QC overlay:

```bash
python scripts/evaluate_segmentation.py \
  --pred-dir predictions/acdc_nnunet_2d_fold0 \
  --label-dir "$nnUNet_raw/Dataset001_ACDC/labelsTr" \
  --out-csv results/acdc_metrics.csv \
  --out-md results/acdc_metrics.md

python scripts/visualize_segmentation.py \
  --image "$nnUNet_raw/Dataset001_ACDC/imagesTr/patient001_frame01_0000.nii.gz" \
  --label "$nnUNet_raw/Dataset001_ACDC/labelsTr/patient001_frame01.nii.gz" \
  --prediction predictions/acdc_nnunet_2d_fold0/patient001_frame01.nii.gz \
  --output results/figures/acdc_patient001_frame01_overlay.png
```

## Repository Structure

```text
cmr-ai-segmentation-workbench/
├── README.md
├── configs/
├── docs/
│   ├── data_format.md
│   ├── medical_disclaimer.md
│   └── roadmap_30_60_90.md
├── examples/
├── results/
└── scripts/
    ├── prepare_acdc.py
    ├── evaluate_segmentation.py
    ├── visualize_segmentation.py
    ├── train_nnunet_acdc.sh
    └── predict_nnunet_acdc.sh
```

## Important Notes

- Do not upload identifiable patient DICOM files or private clinical data.
- Use public datasets for reproducible examples.
- If private data is used, remove patient identifiers and follow institutional rules.
- This project is for research and education only, not clinical diagnosis.
- For real training, use a CUDA GPU workstation or cloud instance. The local Codex sandbox can verify preprocessing, but it may block PyTorch shared-memory training.
- Before publishing, run the privacy and reproducibility checks in [docs/release_checklist.md](docs/release_checklist.md).
- For accurate community posts and project descriptions, see [docs/promotion_kit.md](docs/promotion_kit.md).

## Local Verification

The project includes a tiny synthetic dataset smoke test:

```bash
python scripts/create_tiny_nnunet_dataset.py --output "$nnUNet_raw" --dataset-id 901 --num-training 5
nnUNetv2_plan_and_preprocess -d 901 -c 2d -npfp 1 -np 1 --verify_dataset_integrity --clean
```

See [docs/local_smoke_test.md](docs/local_smoke_test.md).

Completed debug runs are documented in:

- [results/tiny_smoke_test.md](results/tiny_smoke_test.md)
- [results/msd_cardiac_debug.md](results/msd_cardiac_debug.md)
- [results/corseg_sax_pseudolabel_debug.md](results/corseg_sax_pseudolabel_debug.md)

## Acknowledgements

This workbench builds around excellent open-source medical AI projects:

- nnU-Net: https://github.com/MIC-DKFZ/nnUNet
- MONAI: https://github.com/Project-MONAI/MONAI
- MedSAM: https://github.com/bowang-lab/MedSAM
- TorchIO: https://github.com/TorchIO-project/torchio

The local SAX pseudo-label workflow is included to test conversion, preprocessing, training, and privacy boundaries. It should not be cited as evidence of model performance until expert-labeled validation is added.
