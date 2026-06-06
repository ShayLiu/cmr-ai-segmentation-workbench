#!/usr/bin/env python3
"""Convert ACDC cardiac MRI files to nnU-Net v2 format.

Expected ACDC layout:

  source/
    training/patient001/patient001_frame01.nii.gz
    training/patient001/patient001_frame01_gt.nii.gz
    training/patient001/patient001_frame12.nii.gz
    training/patient001/patient001_frame12_gt.nii.gz
    testing/patient101/patient101_frame01.nii.gz

Hugging Face mirrors may instead use:

  source/
    train/patient001/patient001_sax_ed.nii.gz
    train/patient001/patient001_sax_ed_gt.nii.gz
    train/patient001/patient001_sax_es.nii.gz
    train/patient001/patient001_sax_es_gt.nii.gz

The script copies labeled frames to imagesTr/labelsTr and unlabeled frames to
imagesTs. It does not modify image geometry or label values.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

import SimpleITK as sitk


FRAME_RE = re.compile(r"^(patient\d+_(?:frame\d+|sax_(?:ed|es)))\.nii(?:\.gz)?$")


@dataclass(frozen=True)
class AcdcCase:
    case_id: str
    image_path: Path
    label_path: Path | None


def find_acdc_cases(source: Path) -> list[AcdcCase]:
    cases: list[AcdcCase] = []
    for image_path in sorted(source.rglob("patient*.nii*")):
        if image_path.name.startswith("._"):
            continue
        if image_path.name.endswith("_gt.nii") or image_path.name.endswith("_gt.nii.gz"):
            continue
        match = FRAME_RE.match(image_path.name)
        if not match:
            continue
        case_id = match.group(1)
        label_name = label_name_for(image_path)
        label_path = image_path.with_name(label_name)
        cases.append(AcdcCase(case_id=case_id, image_path=image_path, label_path=label_path if label_path.exists() else None))
    return cases


def write_dataset_json(output_dir: Path, num_training: int) -> None:
    dataset = {
        "channel_names": {"0": "cine_mri"},
        "labels": {
            "background": 0,
            "right_ventricle": 1,
            "myocardium": 2,
            "left_ventricle": 3,
        },
        "numTraining": num_training,
        "file_ending": ".nii.gz",
    }
    (output_dir / "dataset.json").write_text(json.dumps(dataset, indent=2) + "\n", encoding="utf-8")


def copy_case(case: AcdcCase, images_dir: Path, labels_dir: Path | None) -> None:
    copy_nifti(case.image_path, images_dir / f"{case.case_id}_0000.nii.gz")
    if labels_dir is not None and case.label_path is not None:
        copy_nifti(case.label_path, labels_dir / f"{case.case_id}.nii.gz")


def copy_nifti(source: Path, destination: Path) -> None:
    if source.name.endswith(".nii.gz"):
        shutil.copy2(source, destination)
        return
    image = sitk.ReadImage(str(source))
    sitk.WriteImage(image, str(destination))


def label_name_for(image_path: Path) -> str:
    if image_path.name.endswith(".nii.gz"):
        return image_path.name.removesuffix(".nii.gz") + "_gt.nii.gz"
    if image_path.name.endswith(".nii"):
        return image_path.name.removesuffix(".nii") + "_gt.nii"
    raise ValueError(f"Unsupported ACDC image suffix: {image_path.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare ACDC NIfTI files for nnU-Net v2.")
    parser.add_argument("--source", required=True, type=Path, help="ACDC root containing patient folders or training/testing folders.")
    parser.add_argument("--output", required=True, type=Path, help="Output directory, e.g. $nnUNet_raw/Dataset001_ACDC.")
    parser.add_argument("--max-training", default=None, type=int, help="Optional limit for quick local smoke tests.")
    parser.add_argument("--max-test", default=None, type=int, help="Optional limit for copied unlabeled test images.")
    args = parser.parse_args()

    cases = find_acdc_cases(args.source)
    if not cases:
        raise SystemExit("No ACDC frame files found. Expected files like patient001_frame01.nii.gz.")

    training_cases = [case for case in cases if case.label_path is not None]
    test_cases = [case for case in cases if case.label_path is None]
    if args.max_training is not None:
        training_cases = training_cases[: args.max_training]
    if args.max_test is not None:
        test_cases = test_cases[: args.max_test]
    if not training_cases:
        raise SystemExit("No labeled ACDC frames found. Expected paired *_gt.nii.gz files for training.")

    images_tr = args.output / "imagesTr"
    labels_tr = args.output / "labelsTr"
    images_ts = args.output / "imagesTs"
    for directory in [images_tr, labels_tr, images_ts]:
        directory.mkdir(parents=True, exist_ok=True)

    for case in training_cases:
        copy_case(case, images_tr, labels_tr)
    for case in test_cases:
        copy_case(case, images_ts, None)

    write_dataset_json(args.output, len(training_cases))
    print(f"Prepared {len(training_cases)} labeled ACDC frames and {len(test_cases)} unlabeled test frames.")
    print(args.output)


if __name__ == "__main__":
    main()
