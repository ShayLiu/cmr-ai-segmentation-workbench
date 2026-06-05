# ACDC nnU-Net Baseline

Status: ACDC conversion, evaluation, and visualization scripts are implemented; ACDC training not run yet.

## Experiment

- Dataset: ACDC cardiac MRI
- Model: nnU-Net v2
- Configuration: 2D baseline first, then 3D full resolution
- Fold: 0

## Metrics

| Structure | Dice | HD95 |
|---|---:|---:|
| Right ventricle | TBD | TBD |
| Myocardium | TBD | TBD |
| Left ventricle | TBD | TBD |
| Mean | TBD | TBD |

## Notes

Local environment verification:

- `nnunetv2==2.7.0` installed in `.venv`.
- Tiny synthetic NIfTI dataset was generated as `Dataset901_TinyCMR`.
- `nnUNetv2_plan_and_preprocess -d 901 -c 2d -npfp 1 -np 1 --verify_dataset_integrity --clean` completed successfully.
- CPU training with `nnUNetTrainer_tiny_debug` completed successfully after running outside the restricted sandbox.
- Tiny smoke-test mean validation Dice was `0.006632277081798084`, expectedly low because it only ran two training iterations.

Record GPU, CUDA, PyTorch, nnU-Net version, training time, and common errors here after running on a normal terminal or GPU machine.

## Available Scripts

```bash
python scripts/prepare_acdc.py \
  --source /path/to/acdc_raw \
  --output "$nnUNet_raw/Dataset001_ACDC"

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

The next publishable milestone is to train on ACDC and replace this placeholder table with held-out Dice and HD95 by structure.
