# Local Smoke Test

This repository includes a tiny synthetic nnU-Net dataset generator.

The smoke test is only for verifying installation, nnU-Net paths, and command wiring. It is not a meaningful medical model.

## Verified Locally

On the current Apple Silicon Codex environment:

- Python virtual environment creation works.
- `nnunetv2==2.7.0` installs successfully.
- PyTorch imports successfully.
- CUDA is not available.
- MPS is not available in this environment.
- Tiny NIfTI dataset generation works.
- `nnUNetv2_plan_and_preprocess` succeeds on `Dataset901_TinyCMR`.

Training reaches nnU-Net dataloader creation, but the Codex sandbox blocks PyTorch shared memory manager startup:

```text
RuntimeError: torch_shm_manager ... Operation not permitted
```

This is an execution sandbox limitation, not a dataset-format problem. Run training from a normal local terminal or a GPU workstation/cloud instance.

When run outside the restricted sandbox with `nnUNetTrainer_tiny_debug`, the tiny CPU training completes successfully.

Install the debug trainer into the active environment before using it:

```bash
python scripts/install_tiny_debug_trainer.py
```

## Create Tiny Dataset

```bash
python scripts/create_tiny_nnunet_dataset.py \
  --output "$nnUNet_raw" \
  --dataset-id 901 \
  --num-training 5
```

## Preprocess

```bash

nnUNetv2_plan_and_preprocess \
  -d 901 \
  -c 2d \
  -npfp 1 \
  -np 1 \
  --verify_dataset_integrity \
  --clean
```

## Optional 1-Epoch CPU Training

Use this short debug trainer on a normal terminal:

```bash
nnUNetv2_train 901 2d 0 \
  -tr nnUNetTrainer_tiny_debug \
  -device cpu
```

On machines without CUDA, full training is not recommended. Use this local test to verify preprocessing, then move real training to a GPU workstation or cloud instance.
