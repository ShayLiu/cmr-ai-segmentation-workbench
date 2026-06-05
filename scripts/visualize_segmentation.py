#!/usr/bin/env python3
"""Create a privacy-safe segmentation overlay PNG from NIfTI files."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import SimpleITK as sitk
from skimage import measure


LABEL_COLORS = {
    1: "#3b8ff0",
    2: "#e94a54",
    3: "#f3b43f",
}


def read_array(path: Path) -> np.ndarray:
    return sitk.GetArrayFromImage(sitk.ReadImage(str(path)))


def normalize(image: np.ndarray) -> np.ndarray:
    lo, hi = np.percentile(image, [1, 99])
    image = np.clip(image, lo, hi)
    return (image - lo) / max(float(hi - lo), 1e-6)


def choose_slice(label: np.ndarray | None, prediction: np.ndarray | None, image: np.ndarray) -> int:
    reference = None
    if label is not None:
        reference = label > 0
    if prediction is not None:
        pred_mask = prediction > 0
        reference = pred_mask if reference is None else np.logical_or(reference, pred_mask)
    if reference is None or not reference.any():
        return image.shape[0] // 2
    return int(np.argmax(reference.sum(axis=(1, 2))))


def draw_contours(ax, mask: np.ndarray, linewidth: float, alpha: float = 1.0) -> None:
    for value, color in LABEL_COLORS.items():
        binary = mask == value
        for contour in measure.find_contours(binary.astype(float), level=0.5):
            if len(contour) > 8:
                ax.plot(contour[:, 1], contour[:, 0], color=color, linewidth=linewidth, alpha=alpha)


def overlay_rgb(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    rgb = np.dstack([image, image, image])
    for value, color in LABEL_COLORS.items():
        hex_color = color.lstrip("#")
        color_rgb = np.array([int(hex_color[i : i + 2], 16) for i in (0, 2, 4)], dtype=float) / 255.0
        rgb[mask == value] = rgb[mask == value] * 0.76 + color_rgb * 0.24
    return np.clip(rgb, 0, 1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render CMR segmentation overlays for QC.")
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument("--label", default=None, type=Path)
    parser.add_argument("--prediction", default=None, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--slice", default=None, type=int)
    args = parser.parse_args()

    image = normalize(read_array(args.image).astype(float))
    label = read_array(args.label).astype(np.uint8) if args.label else None
    prediction = read_array(args.prediction).astype(np.uint8) if args.prediction else None
    z_index = args.slice if args.slice is not None else choose_slice(label, prediction, image)

    panels = [("Image", image[z_index], None)]
    if label is not None:
        panels.append(("Expert label", image[z_index], label[z_index]))
    if prediction is not None:
        panels.append(("Prediction", image[z_index], prediction[z_index]))

    fig, axes = plt.subplots(1, len(panels), figsize=(4.2 * len(panels), 4.2), dpi=180)
    if len(panels) == 1:
        axes = [axes]
    fig.patch.set_facecolor("#0b1521")
    for ax, (title, panel_image, mask) in zip(axes, panels):
        ax.set_facecolor("#0b1521")
        ax.imshow(panel_image, cmap="gray", vmin=0, vmax=1)
        if mask is not None:
            ax.imshow(overlay_rgb(panel_image, mask))
            draw_contours(ax, mask, linewidth=1.1)
        ax.text(
            0.04,
            0.92,
            title,
            transform=ax.transAxes,
            color="#edf8fb",
            fontsize=12,
            fontweight="bold",
            va="top",
            bbox={"facecolor": "#07111d", "alpha": 0.72, "edgecolor": "none", "boxstyle": "round,pad=0.3"},
        )
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    fig.text(0.5, 0.035, f"SAX segmentation QC overlay | slice {z_index}", color="#b8cbd3", ha="center", fontsize=10)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.10, wspace=0.035)
    fig.savefig(args.output, bbox_inches="tight")
    plt.close(fig)
    print(args.output)


if __name__ == "__main__":
    main()
