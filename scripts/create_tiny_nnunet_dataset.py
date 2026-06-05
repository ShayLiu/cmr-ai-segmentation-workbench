#!/usr/bin/env python3
"""Create a tiny synthetic nnU-Net v2 dataset for installation smoke tests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import SimpleITK as sitk


def write_nifti(array: np.ndarray, path: Path) -> None:
    image = sitk.GetImageFromArray(array)
    image.SetSpacing((1.5, 1.5, 5.0))
    sitk.WriteImage(image, str(path))


def make_case(seed: int, shape: tuple[int, int, int]) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    z, y, x = np.indices(shape)
    center = np.array(shape)[:, None, None, None] / 2
    radius = min(shape) / 4
    distance = np.sqrt(((np.stack([z, y, x]) - center) ** 2).sum(axis=0))
    label = (distance < radius).astype(np.uint8)
    image = rng.normal(0, 0.05, shape).astype(np.float32) + label.astype(np.float32)
    return image, label


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--dataset-id", default=901, type=int)
    parser.add_argument("--num-training", default=4, type=int)
    parser.add_argument("--num-test", default=1, type=int)
    args = parser.parse_args()

    dataset_dir = args.output / f"Dataset{args.dataset_id:03d}_TinyCMR"
    images_tr = dataset_dir / "imagesTr"
    labels_tr = dataset_dir / "labelsTr"
    images_ts = dataset_dir / "imagesTs"
    for directory in [images_tr, labels_tr, images_ts]:
        directory.mkdir(parents=True, exist_ok=True)

    shape = (8, 32, 32)
    for idx in range(args.num_training):
        image, label = make_case(idx, shape)
        case = f"tiny_{idx:03d}"
        write_nifti(image, images_tr / f"{case}_0000.nii.gz")
        write_nifti(label, labels_tr / f"{case}.nii.gz")

    for idx in range(args.num_test):
        image, _ = make_case(100 + idx, shape)
        case = f"tiny_test_{idx:03d}"
        write_nifti(image, images_ts / f"{case}_0000.nii.gz")

    dataset = {
        "channel_names": {"0": "synthetic_cmr"},
        "labels": {"background": 0, "synthetic_structure": 1},
        "numTraining": args.num_training,
        "file_ending": ".nii.gz",
    }
    (dataset_dir / "dataset.json").write_text(json.dumps(dataset, indent=2) + "\n")
    print(dataset_dir)


if __name__ == "__main__":
    main()
