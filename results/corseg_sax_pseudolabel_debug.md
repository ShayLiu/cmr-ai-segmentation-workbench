# CorSeg SAX Pseudo-Label Debug Training

Status: completed with manual stop during post-training validation export.

## Dataset

- Source: local CorSeg output directory, supplied by the user and kept outside the repository
- Original images: local DICOM series referenced by CorSeg `segmentation_summary.json`
- Labels: CorSeg-generated pseudo-label masks
- Structures:
  - 1: LV myocardium
  - 2: LV blood pool
  - 3: RV blood pool
- Local nnU-Net dataset: `Dataset903_CorSegSAXPseudo`
- Training cases: 5 anonymized cases
- Fold 0 split: 4 training cases, 1 validation case

## Privacy

The nnU-Net dataset uses anonymized case IDs such as `corseg_0000`.

The private manifest containing original local source paths is excluded from GitHub by `.gitignore` and should not be published.

## Commands

```bash
python scripts/prepare_corseg_sax_pseudolabels.py \
  --source-root /path/to/local/corseg_outputs \
  --output "$nnUNet_raw" \
  --dataset-id 903 \
  --max-cases 5

python scripts/run_nnunet_with_distutils.py plan_and_preprocess \
  -d 903 \
  -c 2d \
  -npfp 1 \
  -np 1 \
  --verify_dataset_integrity \
  --clean

nnUNetv2_train 903 2d 0 \
  -tr nnUNetTrainer_tiny_debug \
  -device cpu
```

## Result

Dataset integrity verification and 2D preprocessing completed successfully.

Tiny CPU training completed for one epoch with `nnUNetTrainer_tiny_debug`.

- `train_loss`: 1.7274
- `val_loss`: 1.6448
- Pseudo Dice by label: 0.0445, 0.0573, 0.0498
- Mean pseudo Dice: 0.0505
- Epoch time: 143.64 s

Generated outputs:

```text
nnunet_workspace/results/Dataset903_CorSegSAXPseudo/nnUNetTrainer_tiny_debug__nnUNetPlans__2d/fold_0/checkpoint_best.pth
nnunet_workspace/results/Dataset903_CorSegSAXPseudo/nnUNetTrainer_tiny_debug__nnUNetPlans__2d/fold_0/checkpoint_final.pth
nnunet_workspace/results/Dataset903_CorSegSAXPseudo/nnUNetTrainer_tiny_debug__nnUNetPlans__2d/fold_0/progress.png
nnunet_workspace/results/Dataset903_CorSegSAXPseudo/nnUNetTrainer_tiny_debug__nnUNetPlans__2d/fold_0/validation/corseg_0000.nii.gz
```

No `validation/summary.json` was produced in this run. Training had already finished, but the full validation export spawned too many CPU worker processes for the local environment and was manually stopped after the validation prediction file was written.

Local disk footprint:

```text
137M nnunet_workspace/raw/Dataset903_CorSegSAXPseudo
213M nnunet_workspace/preprocessed/Dataset903_CorSegSAXPseudo
318M nnunet_workspace/results/Dataset903_CorSegSAXPseudo
```

## Interpretation

This is a pseudo-label workflow. It validates the end-to-end local pipeline from real CMR DICOM-derived inputs to nnU-Net training artifacts, but it does not represent clinical model performance and does not replace manual expert annotation.

The debug trainer has been updated to be more CPU-friendly for future smoke tests: it caps batch size, uses one training iteration, sets `nnUNet_n_proc_DA=0`, and skips full validation export on CPU.
