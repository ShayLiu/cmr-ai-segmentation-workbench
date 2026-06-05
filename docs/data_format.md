# Data Format

## Recommended First Dataset

Use a public cardiac MRI dataset such as ACDC for the first reproducible experiment.

Do not start with private patient data. Public data makes the repository easier to verify and safer to share.

## nnU-Net v2 Layout

nnU-Net v2 expects a dataset layout like this:

```text
nnUNet_raw/
└── Dataset001_ACDC/
    ├── imagesTr/
    │   ├── patient001_0000.nii.gz
    │   └── patient002_0000.nii.gz
    ├── labelsTr/
    │   ├── patient001.nii.gz
    │   └── patient002.nii.gz
    ├── imagesTs/
    │   └── patient101_0000.nii.gz
    └── dataset.json
```

For single-modality cardiac MRI, the image suffix is usually `_0000.nii.gz`.

ACDC files commonly use names like `patient001_frame01.nii.gz` and `patient001_frame01_gt.nii.gz`. Run `scripts/prepare_acdc.py` to copy them into nnU-Net naming:

```bash
python scripts/prepare_acdc.py \
  --source /absolute/path/to/acdc_raw \
  --output "$nnUNet_raw/Dataset001_ACDC"
```

## Example `dataset.json`

```json
{
  "channel_names": {
    "0": "cine_mri"
  },
  "labels": {
    "background": 0,
    "right_ventricle": 1,
    "myocardium": 2,
    "left_ventricle": 3
  },
  "numTraining": 100,
  "file_ending": ".nii.gz"
}
```

Label names and values must match the dataset annotation protocol.

## Privacy

Before using private data:

- Remove patient identifiers from DICOM metadata.
- Avoid uploading raw DICOM files.
- Avoid uploading dates, names, accession numbers, institution names, or IDs.
- Confirm local ethics and data sharing requirements.
