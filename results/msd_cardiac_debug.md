# MSD Cardiac Debug Training

Status: completed.

Date: 2026-06-05

## Dataset

- Source: Hugging Face dataset `Angelou0516/msd-cardiac`
- Original task: Medical Segmentation Decathlon Task02 Heart
- Modality: MRI
- Target: left atrium
- Local nnU-Net dataset: `Dataset902_MSDHeart`
- Debug subset: first 5 training cases

## Planned Commands

```bash
python scripts/prepare_msd_cardiac.py \
  --output "$nnUNet_raw" \
  --dataset-id 902 \
  --max-cases 5

python scripts/install_tiny_debug_trainer.py

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

## Result

Training and validation completed on CPU.

Key log lines:

```text
Epoch 0
train_loss 0.7734
val_loss 0.7245
Pseudo dice [0.0315]
Epoch time: 37.26 s
Training done.
Validation complete
Mean Validation Dice: 0.041143866306299855
```

Generated outputs:

```text
nnunet_workspace/results/Dataset902_MSDHeart/nnUNetTrainer_tiny_debug__nnUNetPlans__2d/fold_0/checkpoint_best.pth
nnunet_workspace/results/Dataset902_MSDHeart/nnUNetTrainer_tiny_debug__nnUNetPlans__2d/fold_0/checkpoint_final.pth
nnunet_workspace/results/Dataset902_MSDHeart/nnUNetTrainer_tiny_debug__nnUNetPlans__2d/fold_0/progress.png
nnunet_workspace/results/Dataset902_MSDHeart/nnUNetTrainer_tiny_debug__nnUNetPlans__2d/fold_0/validation/summary.json
nnunet_workspace/results/Dataset902_MSDHeart/nnUNetTrainer_tiny_debug__nnUNetPlans__2d/fold_0/validation/la_003.nii.gz
```

Storage used locally:

```text
249M data/msd-cardiac-hf
65M  nnunet_workspace/raw/Dataset902_MSDHeart
123M nnunet_workspace/preprocessed/Dataset902_MSDHeart
512M nnunet_workspace/results/Dataset902_MSDHeart
```

## Interpretation

This debug run is intended to prove the real medical data workflow. It is not expected to produce useful segmentation performance because it only runs a minimal number of training iterations.

The low Dice score is expected. The important result is that a real cardiac MRI dataset was downloaded, converted, preprocessed, trained, and validated end to end.
