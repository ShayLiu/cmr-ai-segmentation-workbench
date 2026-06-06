#!/usr/bin/env python3
"""Apply conservative anatomical cleanup to segmentation masks."""

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


def slice_largest_components(mask: np.ndarray) -> np.ndarray:
    output = np.zeros_like(mask, dtype=bool)
    for z_index in range(mask.shape[0]):
        output[z_index] = largest_component(mask[z_index])
    return output


def filter_small_slices(mask: np.ndarray, min_slice_area_fraction: float) -> np.ndarray:
    if min_slice_area_fraction <= 0 or not mask.any():
        return mask
    slice_areas = mask.reshape(mask.shape[0], -1).sum(axis=1)
    threshold = float(slice_areas.max()) * min_slice_area_fraction
    if threshold <= 0:
        return mask
    keep_slices = slice_areas >= threshold
    output = mask.copy()
    output[~keep_slices] = False
    return output


def cleanup(
    array: np.ndarray,
    labels: tuple[int, ...],
    min_voxels: int,
    per_slice_largest_component: bool,
    min_slice_area_fraction: float,
) -> np.ndarray:
    output = np.zeros_like(array, dtype=np.uint8)
    for label in labels:
        mask = array == label
        if int(mask.sum()) < min_voxels:
            continue
        kept = largest_component(mask)
        if per_slice_largest_component:
            kept = slice_largest_components(kept)
        kept = filter_small_slices(kept, min_slice_area_fraction)
        if int(kept.sum()) >= min_voxels:
            output[kept] = label
    return output


def process_file(
    path: Path,
    output_dir: Path,
    labels: tuple[int, ...],
    min_voxels: int,
    per_slice_largest_component: bool,
    min_slice_area_fraction: float,
) -> Path:
    image = sitk.ReadImage(str(path))
    array = sitk.GetArrayFromImage(image)
    cleaned = cleanup(array, labels, min_voxels, per_slice_largest_component, min_slice_area_fraction)
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
    parser.add_argument(
        "--per-slice-largest-component",
        action="store_true",
        help="After 3D component cleanup, keep only the largest component on each SAX slice.",
    )
    parser.add_argument(
        "--min-slice-area-fraction",
        default=0.0,
        type=float,
        help="Drop slices whose label area is below this fraction of the case-level peak slice area.",
    )
    args = parser.parse_args()
    if args.min_slice_area_fraction < 0 or args.min_slice_area_fraction > 1:
        raise ValueError("--min-slice-area-fraction must be between 0 and 1.")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    labels = tuple(args.labels)
    processed = 0
    for path in iter_masks(args.input_dir):
        process_file(
            path,
            args.output_dir,
            labels,
            args.min_voxels,
            args.per_slice_largest_component,
            args.min_slice_area_fraction,
        )
        processed += 1
    print(f"Postprocessed {processed} masks.")
    print(args.output_dir)


if __name__ == "__main__":
    main()
