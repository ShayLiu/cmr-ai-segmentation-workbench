# Tiny nnU-Net Smoke Test

Status: completed.

Date: 2026-06-05

## Purpose

This smoke test verifies that the local nnU-Net environment can:

- create a tiny synthetic NIfTI dataset,
- run nnU-Net dataset integrity checks,
- run fingerprint extraction and preprocessing,
- initialize training,
- complete a minimal training/validation cycle,
- write checkpoints and validation predictions.

This is not a meaningful medical model.

## Environment

- Machine: Apple Silicon Mac
- Device: CPU
- Python: 3.12
- nnU-Net: 2.7.0
- Dataset: `Dataset901_TinyCMR`
- Configuration: `2d`
- Trainer: `nnUNetTrainer_tiny_debug`
- Fold: 0

## Commands

```bash
python scripts/create_tiny_nnunet_dataset.py \
  --output "$nnUNet_raw" \
  --dataset-id 901 \
  --num-training 5

nnUNetv2_plan_and_preprocess \
  -d 901 \
  -c 2d \
  -npfp 1 \
  -np 1 \
  --verify_dataset_integrity \
  --clean

nnUNetv2_train 901 2d 0 \
  -tr nnUNetTrainer_tiny_debug \
  -device cpu
```

## Result

Training completed successfully.

Key log lines:

```text
Epoch 0
train_loss 1.168
val_loss 1.0705
Pseudo dice [0.0194]
Training done.
Validation complete
Mean Validation Dice: 0.006632277081798084
```

Generated outputs:

```text
nnunet_workspace/results/Dataset901_TinyCMR/nnUNetTrainer_tiny_debug__nnUNetPlans__2d/fold_0/checkpoint_best.pth
nnunet_workspace/results/Dataset901_TinyCMR/nnUNetTrainer_tiny_debug__nnUNetPlans__2d/fold_0/checkpoint_final.pth
nnunet_workspace/results/Dataset901_TinyCMR/nnUNetTrainer_tiny_debug__nnUNetPlans__2d/fold_0/progress.png
nnunet_workspace/results/Dataset901_TinyCMR/nnUNetTrainer_tiny_debug__nnUNetPlans__2d/fold_0/validation/summary.json
```

## Interpretation

The pipeline is functional. The low Dice score is expected because this debug trainer runs only two training iterations and one validation iteration.

For real experiments, train on a public cardiac MRI dataset such as ACDC with CUDA GPU acceleration.
