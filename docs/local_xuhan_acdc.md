# Local Xuhan ACDC Setup

This machine can keep large benchmark data outside Git at:

```text
/Volumes/Xuhan/cmr-ai-segmentation-workbench-data
```

Expected ACDC source folder:

```text
/Volumes/Xuhan/cmr-ai-segmentation-workbench-data/datasets/acdc_raw
```

Place the downloaded and extracted ACDC files there. The converter expects files like:

```text
patient001_frame01.nii.gz
patient001_frame01_gt.nii.gz
```

Set paths:

```bash
source configs/local_xuhan_env.sh
```

Convert ACDC:

```bash
python scripts/prepare_acdc.py \
  --source "$CMR_WORKBENCH_DATA/datasets/acdc_raw" \
  --output "$nnUNet_raw/Dataset001_ACDC"
```

Train:

```bash
DATASET_ID=1 CONFIG=2d FOLD=0 DEVICE=cuda bash scripts/train_nnunet_acdc.sh
```

Evaluate and visualize after prediction:

```bash
python scripts/evaluate_segmentation.py \
  --pred-dir "$CMR_WORKBENCH_DATA/predictions/acdc_nnunet_2d_fold0" \
  --label-dir "$nnUNet_raw/Dataset001_ACDC/labelsTr" \
  --out-csv results/acdc_metrics.csv \
  --out-md results/acdc_metrics.md
```
