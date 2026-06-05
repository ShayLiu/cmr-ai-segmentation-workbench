#!/usr/bin/env python3
"""Prepare anonymized nnU-Net data from local CorSeg SAX pseudo-label outputs."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import numpy as np
import SimpleITK as sitk


def iter_summaries(root: Path):
    for path in sorted(root.rglob("segmentation_summary.json")):
        if "/._" in str(path) or path.name.startswith("._"):
            continue
        yield path


def load_summary(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def read_dicom_2d(path: Path) -> tuple[np.ndarray, sitk.Image]:
    image = sitk.ReadImage(str(path))
    array = sitk.GetArrayFromImage(image)
    if array.ndim == 3:
        array = array[0]
    return array.astype(np.float32), image


def read_mask_2d(path: Path) -> np.ndarray:
    image = sitk.ReadImage(str(path))
    array = sitk.GetArrayFromImage(image)
    if array.ndim == 3:
        array = array[0]
    return array.astype(np.uint8)


def write_volume(array: np.ndarray, reference: sitk.Image | None, path: Path, is_label: bool) -> None:
    image = sitk.GetImageFromArray(array)
    if reference is not None:
        spacing = reference.GetSpacing()
        if len(spacing) >= 2:
            image.SetSpacing((float(spacing[0]), float(spacing[1]), 1.0))
    if is_label:
        image = sitk.Cast(image, sitk.sitkUInt8)
    sitk.WriteImage(image, str(path))


def build_case(summary_path: Path, case_id: str, images_tr: Path, labels_tr: Path) -> dict | None:
    summary = load_summary(summary_path)
    if not summary:
        return None

    input_dir = Path(summary.get("input", ""))
    mask_dir = summary_path.parent / "masks"
    if not input_dir.exists() or not mask_dir.exists():
        return None

    dcm_files = sorted(input_dir.glob("*.dcm"))
    frames = []
    labels = []
    first_ref = None

    for dcm_path in dcm_files:
        stem = dcm_path.stem
        mask_path = mask_dir / f"{stem}.nii.gz"
        if not mask_path.exists():
            continue
        image_2d, ref = read_dicom_2d(dcm_path)
        label_2d = read_mask_2d(mask_path)
        if image_2d.shape != label_2d.shape:
            continue
        if first_ref is None:
            first_ref = ref
        frames.append(image_2d)
        labels.append(label_2d)

    if len(frames) < 5:
        return None

    image_volume = np.stack(frames, axis=0)
    label_volume = np.stack(labels, axis=0)
    if int((label_volume > 0).sum()) == 0:
        return None

    write_volume(image_volume, first_ref, images_tr / f"{case_id}_0000.nii.gz", is_label=False)
    write_volume(label_volume, first_ref, labels_tr / f"{case_id}.nii.gz", is_label=True)

    label_values = sorted(int(v) for v in np.unique(label_volume))
    return {
        "case_id": case_id,
        "num_frames": len(frames),
        "image_shape_zyx": list(image_volume.shape),
        "label_values": label_values,
        "foreground_voxels": int((label_volume > 0).sum()),
        "source_summary": str(summary_path),
        "source_input": str(input_dir),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--dataset-id", default=903, type=int)
    parser.add_argument("--max-cases", default=5, type=int)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()

    dataset_dir = args.output / f"Dataset{args.dataset_id:03d}_CorSegSAXPseudo"
    images_tr = dataset_dir / "imagesTr"
    labels_tr = dataset_dir / "labelsTr"
    if dataset_dir.exists():
        shutil.rmtree(dataset_dir)
    images_tr.mkdir(parents=True, exist_ok=True)
    labels_tr.mkdir(parents=True, exist_ok=True)
    (dataset_dir / "imagesTs").mkdir(parents=True, exist_ok=True)

    records = []
    for summary_path in iter_summaries(args.source_root):
        case_id = f"corseg_{len(records):04d}"
        record = build_case(summary_path, case_id, images_tr, labels_tr)
        if record is None:
            continue
        records.append(record)
        if len(records) >= args.max_cases:
            break

    if len(records) < 5:
        raise SystemExit(f"Need at least 5 usable cases for nnU-Net 5-fold split; found {len(records)}")

    dataset_json = {
        "channel_names": {"0": "cine_sax"},
        "labels": {
            "background": 0,
            "lv_myocardium": 1,
            "lv_blood_pool": 2,
            "rv_blood_pool": 3,
        },
        "numTraining": len(records),
        "file_ending": ".nii.gz",
    }
    (dataset_dir / "dataset.json").write_text(json.dumps(dataset_json, indent=2) + "\n", encoding="utf-8")

    manifest_path = args.manifest or dataset_dir / "source_manifest_private.json"
    manifest_path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(dataset_dir)
    print(f"cases={len(records)}")
    print(f"manifest={manifest_path}")


if __name__ == "__main__":
    main()
