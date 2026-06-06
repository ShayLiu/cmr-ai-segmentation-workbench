#!/usr/bin/env python3
"""Apply conservative connected-component cleanup to segmentation masks."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import SimpleITK as sitk
from scipy import ndimage


DEFAULT_LABELS = (1, 2, 3)


def iter_masks(input_dir: Path) -> list[Path]:
    return sorted(path for path in input_dir.glob("*.nii*") if path.is_file() and not path.name.startswith("._"))


def largest_component(mask: np.ndarray) -> np.ndarray:
    structure = ndimage.generate_binary_structure(mask.ndim, 1)
    components, count = ndimage.label(mask, structure=structure)
    if count <= 1:
        return mask
    sizes = np.bincount(components.ravel())
    sizes[0] = 0
    return components == int(np.argmax(sizes))


def cleanup(array: np.ndarray, labels: tuple[int, ...], min_voxels: int) -> np.ndarray:
    output = np.zeros_like(array, dtype=np.uint8)
    for label in labels:
        mask = array == label
        if int(mask.sum()) < min_voxels:
            continue
        kept = largest_component(mask)
        if int(kept.sum()) >= min_voxels:
            output[kept] = label
    return output


def process_file(path: Path, output_dir: Path, labels: tuple[int, ...], min_voxels: int) -> Path:
    image = sitk.ReadImage(str(path))
    array = sitk.GetArrayFromImage(image)
    cleaned = cleanup(array, labels, min_voxels)
    out_image = sitk.GetImageFromArray(cleaned)
    out_image.CopyInformation(image)
    output_path = output_dir / path.name
    sitk.WriteImage(out_image, str(output_path))
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean segmentation masks with connected-component filtering.")
    parser.add_argument("--input-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--labels", nargs="+", default=DEFAULT_LABELS, type=int)
    parser.add_argument("--min-voxels", default=64, type=int)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    labels = tuple(args.labels)
    processed = 0
    for path in iter_masks(args.input_dir):
        process_file(path, args.output_dir, labels, args.min_voxels)
        processed += 1
    print(f"Postprocessed {processed} masks.")
    print(args.output_dir)


if __name__ == "__main__":
    main()
