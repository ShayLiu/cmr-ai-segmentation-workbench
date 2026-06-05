# Release Checklist

Use this checklist before publishing the repository or creating a GitHub release.

## Privacy

- Do not commit DICOM files, NIfTI images, model checkpoints, predictions, or raw nnU-Net workspaces.
- Do not commit source manifests that contain local file paths, names, dates, accession numbers, hospital identifiers, or patient identifiers.
- Search the repository for private paths before release:

```bash
rg -n "/Volumes|/Users|source_manifest|pah-shuntfree|\\.dcm|\\.nii\\.gz" README.md docs results scripts .github
```

Expected matches should be generic format examples or anonymized output paths only.

## Reproducibility

- Run script syntax checks:

```bash
python -m py_compile scripts/*.py
```

- Run the tiny dataset smoke test:

```bash
python scripts/create_tiny_nnunet_dataset.py \
  --output /tmp/nnunet_raw \
  --dataset-id 901 \
  --num-training 5
```

- Confirm `results/` files state hardware, dataset, and limitations clearly.

## Medical Claims

- Do not describe pseudo-label training as expert-labeled performance.
- Do not claim clinical diagnosis, treatment guidance, or regulatory readiness.
- State that private-data workflows require local ethics, privacy, and institutional approval.

## GitHub

- Check ignored files before first commit:

```bash
git status --ignored --short
```

- Confirm `.venv/`, `data/`, `nnunet_workspace/`, `*.nii.gz`, `*.dcm`, and `*.pth` are ignored.
