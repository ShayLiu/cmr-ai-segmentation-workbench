# Quickstart

This quickstart is for the first reproducible baseline: ACDC cardiac MRI segmentation with nnU-Net v2.

## 1. Create Environment

```bash
conda create -n cmr-nnunet python=3.10 -y
conda activate cmr-nnunet
pip install nnunetv2
```

Install PyTorch according to your CUDA version before training on GPU.

For this repository's minimal environment:

```bash
pip install -r requirements.txt
python scripts/install_tiny_debug_trainer.py
```

## 2. Set nnU-Net Paths

```bash
export nnUNet_raw=/absolute/path/to/nnUNet_raw
export nnUNet_preprocessed=/absolute/path/to/nnUNet_preprocessed
export nnUNet_results=/absolute/path/to/nnUNet_results
```

## 3. Convert ACDC to nnU-Net

```bash
python scripts/prepare_acdc.py \
  --source /absolute/path/to/acdc_raw \
  --output "$nnUNet_raw/Dataset001_ACDC"
```

The converter looks for ACDC-style files such as `patient001_frame01.nii.gz` and `patient001_frame01_gt.nii.gz`, then writes `imagesTr`, `labelsTr`, `imagesTs`, and `dataset.json`.

## 4. Train

```bash
DATASET_ID=1 CONFIG=2d FOLD=0 bash scripts/train_nnunet_acdc.sh
```

## 5. Predict

```bash
DATASET_ID=1 CONFIG=2d FOLD=0 bash scripts/predict_nnunet_acdc.sh
```

## 6. Evaluate

After prediction on a labeled validation folder, compute Dice and HD95:

```bash
python scripts/evaluate_segmentation.py \
  --pred-dir predictions/acdc_nnunet_2d_fold0 \
  --label-dir "$nnUNet_raw/Dataset001_ACDC/labelsTr" \
  --out-csv results/acdc_metrics.csv \
  --out-md results/acdc_metrics.md
```

## 7. Visual QC

Create a representative overlay for expert review:

```bash
python scripts/visualize_segmentation.py \
  --image "$nnUNet_raw/Dataset001_ACDC/imagesTr/patient001_frame01_0000.nii.gz" \
  --label "$nnUNet_raw/Dataset001_ACDC/labelsTr/patient001_frame01.nii.gz" \
  --prediction predictions/acdc_nnunet_2d_fold0/patient001_frame01.nii.gz \
  --output results/figures/acdc_patient001_frame01_overlay.png
```

## 8. Record Results

Update:

```text
results/acdc_nnunet_baseline.md
```

Add metrics, representative success/failure screenshots, hardware, training time, and problems encountered.

## Public MSD Cardiac Debug Run

This repository also includes a real public cardiac MRI debug workflow using the MSD Heart dataset hosted on Hugging Face:

```bash
python scripts/prepare_msd_cardiac.py \
  --output "$nnUNet_raw" \
  --dataset-id 902 \
  --max-cases 5

nnUNetv2_plan_and_preprocess \
  -d 902 \
  -c 2d \
  -npfp 1 \
  -np 1 \
  --verify_dataset_integrity \
  --clean

nnUNetv2_train 902 2d 0 \
  -tr nnUNetTrainer_tiny_debug \
  -device cpu
```

See `results/msd_cardiac_debug.md` for the completed debug result.

## Local CorSeg SAX Pseudo-Label Debug Run

For private local CMR data with existing CorSeg outputs, create an anonymized nnU-Net dataset without publishing source paths:

```bash
python scripts/prepare_corseg_sax_pseudolabels.py \
  --source-root /path/to/local/corseg_outputs \
  --output "$nnUNet_raw" \
  --dataset-id 903 \
  --max-cases 5
```

Then preprocess and run the tiny CPU debug trainer as above. See `results/corseg_sax_pseudolabel_debug.md`.
