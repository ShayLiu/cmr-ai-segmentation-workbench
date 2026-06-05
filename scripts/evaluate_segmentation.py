#!/usr/bin/env python3
"""Evaluate multi-label medical image segmentations with Dice and HD95."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
import SimpleITK as sitk
from scipy import ndimage


DEFAULT_LABELS = {
    1: "right_ventricle",
    2: "myocardium",
    3: "left_ventricle",
}


def load_labels(value: str | None) -> dict[int, str]:
    if value is None:
        return DEFAULT_LABELS
    parsed = json.loads(value)
    return {int(key): str(name) for key, name in parsed.items()}


def read_mask(path: Path) -> tuple[np.ndarray, tuple[float, ...]]:
    image = sitk.ReadImage(str(path))
    array = sitk.GetArrayFromImage(image)
    spacing = tuple(reversed(image.GetSpacing()))
    return array, spacing


def dice_score(pred: np.ndarray, truth: np.ndarray) -> float:
    pred_sum = int(pred.sum())
    truth_sum = int(truth.sum())
    if pred_sum == 0 and truth_sum == 0:
        return 1.0
    if pred_sum == 0 or truth_sum == 0:
        return 0.0
    return float(2.0 * np.logical_and(pred, truth).sum() / (pred_sum + truth_sum))


def surface(mask: np.ndarray) -> np.ndarray:
    if not mask.any():
        return mask.astype(bool)
    structure = ndimage.generate_binary_structure(mask.ndim, 1)
    eroded = ndimage.binary_erosion(mask, structure=structure, border_value=0)
    return np.logical_and(mask, np.logical_not(eroded))


def hd95(pred: np.ndarray, truth: np.ndarray, spacing: tuple[float, ...]) -> float:
    if not pred.any() and not truth.any():
        return 0.0
    if not pred.any() or not truth.any():
        return float("nan")

    pred_surface = surface(pred)
    truth_surface = surface(truth)
    pred_to_truth = ndimage.distance_transform_edt(~truth_surface, sampling=spacing)[pred_surface]
    truth_to_pred = ndimage.distance_transform_edt(~pred_surface, sampling=spacing)[truth_surface]
    distances = np.concatenate([pred_to_truth, truth_to_pred])
    return float(np.percentile(distances, 95))


def find_label_path(label_dir: Path, pred_path: Path) -> Path | None:
    candidates = [
        label_dir / pred_path.name,
        label_dir / pred_path.name.replace("_0000.nii.gz", ".nii.gz"),
        label_dir / pred_path.name.replace("_0000.nii", ".nii"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def iter_prediction_files(pred_dir: Path) -> list[Path]:
    return sorted(path for path in pred_dir.glob("*.nii*") if path.is_file())


def summarize(rows: list[dict[str, object]], labels: dict[int, str]) -> list[dict[str, object]]:
    summary = []
    for label_value, label_name in labels.items():
        label_rows = [row for row in rows if row["label_value"] == label_value]
        dice_values = np.array([row["dice"] for row in label_rows], dtype=float)
        hd95_values = np.array([row["hd95"] for row in label_rows], dtype=float)
        summary.append(
            {
                "case": "mean",
                "label_value": label_value,
                "label_name": label_name,
                "dice": float(np.nanmean(dice_values)) if dice_values.size else float("nan"),
                "hd95": float(np.nanmean(hd95_values)) if hd95_values.size else float("nan"),
            }
        )
    return summary


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["case", "label_value", "label_name", "dice", "hd95"])
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, object]], summary_rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Segmentation Evaluation",
        "",
        "## Mean Metrics",
        "",
        "| Structure | Dice | HD95 |",
        "|---|---:|---:|",
    ]
    for row in summary_rows:
        lines.append(f"| {row['label_name']} | {row['dice']:.4f} | {row['hd95']:.2f} |")
    lines.extend(["", "## Per-Case Metrics", "", "| Case | Structure | Dice | HD95 |", "|---|---|---:|---:|"])
    for row in rows:
        lines.append(f"| {row['case']} | {row['label_name']} | {row['dice']:.4f} | {row['hd95']:.2f} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute Dice and HD95 for NIfTI segmentation predictions.")
    parser.add_argument("--pred-dir", required=True, type=Path)
    parser.add_argument("--label-dir", required=True, type=Path)
    parser.add_argument("--labels", default=None, help='JSON mapping, e.g. \'{"1":"rv","2":"myo","3":"lv"}\'.')
    parser.add_argument("--out-csv", default=Path("results/segmentation_metrics.csv"), type=Path)
    parser.add_argument("--out-md", default=None, type=Path)
    args = parser.parse_args()

    labels = load_labels(args.labels)
    rows: list[dict[str, object]] = []
    for pred_path in iter_prediction_files(args.pred_dir):
        label_path = find_label_path(args.label_dir, pred_path)
        if label_path is None:
            print(f"Skipping {pred_path.name}: no matching label found.")
            continue

        pred_array, pred_spacing = read_mask(pred_path)
        truth_array, _ = read_mask(label_path)
        if pred_array.shape != truth_array.shape:
            raise ValueError(f"Shape mismatch for {pred_path.name}: {pred_array.shape} vs {truth_array.shape}")

        case_name = pred_path.name.replace(".nii.gz", "").replace(".nii", "")
        for label_value, label_name in labels.items():
            pred_binary = pred_array == label_value
            truth_binary = truth_array == label_value
            rows.append(
                {
                    "case": case_name,
                    "label_value": label_value,
                    "label_name": label_name,
                    "dice": dice_score(pred_binary, truth_binary),
                    "hd95": hd95(pred_binary, truth_binary, pred_spacing),
                }
            )

    if not rows:
        raise SystemExit("No matched prediction/label pairs were evaluated.")

    summary_rows = summarize(rows, labels)
    write_csv(args.out_csv, rows + summary_rows)
    if args.out_md is not None:
        write_markdown(args.out_md, rows, summary_rows)
    print(f"Evaluated {len({row['case'] for row in rows})} cases.")
    print(args.out_csv)


if __name__ == "__main__":
    main()
