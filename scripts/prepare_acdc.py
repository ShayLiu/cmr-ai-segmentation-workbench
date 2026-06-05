#!/usr/bin/env python3
"""
Prepare ACDC-style cardiac MRI data for nnU-Net v2.

This is a placeholder scaffold. The exact conversion depends on how the ACDC
files are downloaded and unpacked locally.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


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
    (output_dir / "dataset.json").write_text(
        json.dumps(dataset, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--num-training", default=100, type=int)
    args = parser.parse_args()

    dataset_dir = args.output
    for name in ["imagesTr", "labelsTr", "imagesTs"]:
        (dataset_dir / name).mkdir(parents=True, exist_ok=True)

    write_dataset_json(dataset_dir, args.num_training)

    print(f"Created nnU-Net dataset scaffold: {dataset_dir}")
    print("Next step: copy or convert ACDC NIfTI files into imagesTr/labelsTr/imagesTs.")
    print(f"Source path recorded for reference: {args.source}")


if __name__ == "__main__":
    main()

