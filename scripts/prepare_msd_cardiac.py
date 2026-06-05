#!/usr/bin/env python3
"""Prepare MSD Cardiac data from Hugging Face for nnU-Net v2."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def maybe_download(repo_id: str, target: Path) -> Path:
    from huggingface_hub import snapshot_download

    return Path(
        snapshot_download(
            repo_id=repo_id,
            repo_type="dataset",
            local_dir=target,
            local_dir_use_symlinks=False,
        )
    )


def find_task_dir(source: Path) -> Path:
    if (source / "imagesTr").exists() and (source / "labelsTr").exists():
        return source
    candidates = list(source.rglob("Task02_Heart"))
    if not candidates:
        raise FileNotFoundError(f"Could not find Task02_Heart under {source}")
    return candidates[0]


def prepare_dataset(source: Path, output: Path, dataset_id: int, max_cases: int | None) -> Path:
    task_dir = find_task_dir(source)
    src_images = task_dir / "imagesTr"
    src_labels = task_dir / "labelsTr"
    if not src_images.exists() or not src_labels.exists():
        raise FileNotFoundError(f"Expected imagesTr and labelsTr under {task_dir}")

    dataset_dir = output / f"Dataset{dataset_id:03d}_MSDHeart"
    dst_images = dataset_dir / "imagesTr"
    dst_labels = dataset_dir / "labelsTr"
    dst_test = dataset_dir / "imagesTs"
    for directory in [dst_images, dst_labels, dst_test]:
        directory.mkdir(parents=True, exist_ok=True)

    cases = sorted(src_labels.glob("*.nii.gz"))
    if max_cases is not None:
        cases = cases[:max_cases]
    if len(cases) < 5:
        raise ValueError("nnU-Net 5-fold training needs at least 5 training cases.")

    for label_path in cases:
        case_id = label_path.name.removesuffix(".nii.gz")
        image_path = src_images / label_path.name
        if not image_path.exists():
            raise FileNotFoundError(f"Missing image for label: {label_path}")
        shutil.copy2(image_path, dst_images / f"{case_id}_0000.nii.gz")
        shutil.copy2(label_path, dst_labels / f"{case_id}.nii.gz")

    dataset = {
        "channel_names": {"0": "MRI"},
        "labels": {"background": 0, "left_atrium": 1},
        "numTraining": len(cases),
        "file_ending": ".nii.gz",
    }
    (dataset_dir / "dataset.json").write_text(json.dumps(dataset, indent=2) + "\n")
    return dataset_dir


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, help="Existing downloaded dataset directory.")
    parser.add_argument("--download-dir", type=Path, default=Path("data/msd-cardiac-hf"))
    parser.add_argument("--repo-id", default="Angelou0516/msd-cardiac")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--dataset-id", default=902, type=int)
    parser.add_argument("--max-cases", default=5, type=int)
    args = parser.parse_args()

    source = args.source if args.source else maybe_download(args.repo_id, args.download_dir)
    dataset_dir = prepare_dataset(source, args.output, args.dataset_id, args.max_cases)
    print(dataset_dir)


if __name__ == "__main__":
    main()
