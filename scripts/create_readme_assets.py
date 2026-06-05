#!/usr/bin/env python3
"""Create privacy-safe README visuals for the project.

The overlay preview uses the public MSD Cardiac dataset when it is available
locally. It does not use private patient data.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
from scipy import ndimage
from scipy.interpolate import splprep, splev
from skimage import measure


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "assets"


def write_text(path: Path, text: str) -> None:
    path.write_text(text.strip() + "\n", encoding="utf-8")


def load_public_msd_slice() -> tuple[np.ndarray, np.ndarray]:
    image_path = ROOT / "data" / "msd-cardiac-hf" / "imagesTr" / "la_014.nii.gz"
    label_path = ROOT / "data" / "msd-cardiac-hf" / "labelsTr" / "la_014.nii.gz"
    if not image_path.exists() or not label_path.exists():
        raise FileNotFoundError("Public MSD Cardiac sample not found. Run the MSD preparation workflow first.")

    image_volume = nib.load(str(image_path)).get_fdata()
    label_volume = nib.load(str(label_path)).get_fdata()
    foreground_by_slice = (label_volume > 0).sum(axis=(0, 1))
    z_index = int(np.argmax(foreground_by_slice))

    image = normalize_image(image_volume[:, :, z_index])
    label = (label_volume[:, :, z_index] > 0).astype(np.uint8)
    image, label = crop_to_foreground(image, label, margin=58)
    return image.T, label.T


def image_to_data_uri(image: np.ndarray, label: np.ndarray) -> str:
    import base64
    from io import BytesIO

    image_hi, mask_hi, contour_field = prepare_display_masks(image, label)
    overlay = blend_overlay(image_hi, mask_hi)
    overlay = np.clip(overlay, 0, 1)
    fig, ax = plt.subplots(figsize=(3.4, 2.5), dpi=120)
    ax.imshow(overlay, cmap="gray", vmin=0, vmax=1)
    plot_smooth_contours(ax, contour_field, color="#fff0f2", linewidth=1.0, alpha=0.92)
    ax.set_axis_off()
    fig.subplots_adjust(0, 0, 1, 1)
    buf = BytesIO()
    fig.savefig(buf, format="png", transparent=False)
    plt.close(fig)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def create_banner(image: np.ndarray, label: np.ndarray) -> None:
    preview_uri = image_to_data_uri(image, label)
    write_text(
        ASSET_DIR / "cmr_workbench_banner.svg",
        f"""
<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="360" viewBox="0 0 1280 360" role="img" aria-label="CMR AI Segmentation Workbench banner">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#08111f"/>
      <stop offset="52%" stop-color="#13283a"/>
      <stop offset="100%" stop-color="#103b43"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#07111d" flood-opacity="0.36"/>
    </filter>
    <clipPath id="previewClip">
      <rect x="0" y="0" width="310" height="228" rx="18"/>
    </clipPath>
  </defs>
  <rect width="1280" height="360" fill="url(#bg)"/>
  <g opacity="0.18" stroke="#ffffff" stroke-width="1">
    <path d="M0 84 H1280"/>
    <path d="M0 180 H1280"/>
    <path d="M0 276 H1280"/>
    <path d="M180 0 V360"/>
    <path d="M420 0 V360"/>
    <path d="M660 0 V360"/>
    <path d="M900 0 V360"/>
    <path d="M1140 0 V360"/>
  </g>
  <g transform="translate(832 64)" filter="url(#softShadow)">
    <rect x="-16" y="-16" width="342" height="260" rx="24" fill="#07111d" stroke="#d6eef6" stroke-opacity="0.28"/>
    <image href="{preview_uri}" x="0" y="0" width="310" height="228" preserveAspectRatio="xMidYMid slice" clip-path="url(#previewClip)"/>
    <rect x="0" y="0" width="310" height="228" rx="18" fill="none" stroke="#d8f4ff" stroke-opacity="0.42"/>
    <text x="22" y="205" fill="#e4f7fb" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="700">Public MSD Cardiac preview</text>
  </g>
  <g transform="translate(84 78)">
    <text x="0" y="0" fill="#dff7ff" font-family="Inter, Arial, sans-serif" font-size="56" font-weight="700">CMR AI Segmentation Workbench</text>
    <text x="0" y="58" fill="#a8d5df" font-family="Inter, Arial, sans-serif" font-size="25">Reproducible cardiac MRI segmentation workflows for medical imaging AI research</text>
    <g transform="translate(0 104)" font-family="Inter, Arial, sans-serif" font-size="19" font-weight="600">
      <rect x="0" y="0" width="124" height="38" rx="19" fill="#1f6f78"/>
      <text x="24" y="25" fill="#ffffff">nnU-Net</text>
      <rect x="142" y="0" width="116" height="38" rx="19" fill="#315f8c"/>
      <text x="166" y="25" fill="#ffffff">MONAI</text>
      <rect x="276" y="0" width="120" height="38" rx="19" fill="#6a5c91"/>
      <text x="300" y="25" fill="#ffffff">MedSAM</text>
      <rect x="414" y="0" width="190" height="38" rx="19" fill="#33695c"/>
      <text x="438" y="25" fill="#ffffff">privacy first</text>
    </g>
  </g>
</svg>
""",
    )


def create_workflow() -> None:
    write_text(
        ASSET_DIR / "workflow_overview.svg",
        """
<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="360" viewBox="0 0 1180 360" role="img" aria-label="Workflow overview">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#35556b"/>
    </marker>
  </defs>
  <rect width="1180" height="360" rx="18" fill="#f7fbfc"/>
  <text x="42" y="54" fill="#163244" font-family="Inter, Arial, sans-serif" font-size="30" font-weight="700">Reproducible CMR Segmentation Workflow</text>
  <g font-family="Inter, Arial, sans-serif" font-size="17" fill="#1d3446">
    <g transform="translate(48 105)">
      <rect width="160" height="132" rx="14" fill="#e7f0f2" stroke="#aec6cf"/>
      <text x="22" y="40" font-weight="700">Input data</text>
      <text x="22" y="72">Public CMR</text>
      <text x="22" y="98">Local pseudo-labels</text>
    </g>
    <g transform="translate(268 105)">
      <rect width="160" height="132" rx="14" fill="#edf4ea" stroke="#b6ccb1"/>
      <text x="22" y="40" font-weight="700">Anonymize</text>
      <text x="22" y="72">No PHI in Git</text>
      <text x="22" y="98">Private manifest</text>
    </g>
    <g transform="translate(488 105)">
      <rect width="160" height="132" rx="14" fill="#eef1fb" stroke="#bac3e2"/>
      <text x="22" y="40" font-weight="700">nnU-Net format</text>
      <text x="22" y="72">imagesTr</text>
      <text x="22" y="98">labelsTr</text>
    </g>
    <g transform="translate(708 105)">
      <rect width="160" height="132" rx="14" fill="#fbf2e6" stroke="#dec6a3"/>
      <text x="22" y="40" font-weight="700">Train/debug</text>
      <text x="22" y="72">tiny smoke test</text>
      <text x="22" y="98">public baseline</text>
    </g>
    <g transform="translate(928 105)">
      <rect width="160" height="132" rx="14" fill="#f7eaf0" stroke="#d7b5c5"/>
      <text x="22" y="40" font-weight="700">Report</text>
      <text x="22" y="72">metrics</text>
      <text x="22" y="98">limits + artifacts</text>
    </g>
  </g>
  <g stroke="#35556b" stroke-width="3" marker-end="url(#arrow)">
    <line x1="214" y1="171" x2="258" y2="171"/>
    <line x1="434" y1="171" x2="478" y2="171"/>
    <line x1="654" y1="171" x2="698" y2="171"/>
    <line x1="874" y1="171" x2="918" y2="171"/>
  </g>
  <text x="48" y="303" fill="#5b6c76" font-family="Inter, Arial, sans-serif" font-size="16">No private DICOM, NIfTI, checkpoints, or patient-level source manifests are distributed.</text>
</svg>
""",
    )


def create_results_summary() -> None:
    write_text(
        ASSET_DIR / "debug_runs_summary.svg",
        """
<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="300" viewBox="0 0 1120 300" role="img" aria-label="Completed debug runs summary">
  <rect width="1120" height="300" rx="18" fill="#fbfcfd"/>
  <text x="42" y="54" fill="#163244" font-family="Inter, Arial, sans-serif" font-size="28" font-weight="700">Completed Debug Runs</text>
  <g font-family="Inter, Arial, sans-serif">
    <g transform="translate(52 96)">
      <rect width="300" height="140" rx="14" fill="#eaf3f5" stroke="#b6ccd4"/>
      <text x="24" y="38" fill="#173244" font-size="22" font-weight="700">Tiny smoke test</text>
      <text x="24" y="72" fill="#526570" font-size="17">Synthetic data</text>
      <text x="24" y="106" fill="#1f7a62" font-size="17" font-weight="700">Training completed</text>
    </g>
    <g transform="translate(410 96)">
      <rect width="300" height="140" rx="14" fill="#eef1fb" stroke="#bac3e2"/>
      <text x="24" y="38" fill="#173244" font-size="22" font-weight="700">MSD Cardiac</text>
      <text x="24" y="72" fill="#526570" font-size="17">Public real medical data</text>
      <text x="24" y="106" fill="#1f7a62" font-size="17" font-weight="700">Debug training completed</text>
    </g>
    <g transform="translate(768 96)">
      <rect width="300" height="140" rx="14" fill="#fbf2e8" stroke="#dec6a3"/>
      <text x="24" y="38" fill="#173244" font-size="22" font-weight="700">CorSeg SAX</text>
      <text x="24" y="72" fill="#526570" font-size="17">Local pseudo-label workflow</text>
      <text x="24" y="106" fill="#a06418" font-size="17" font-weight="700">Workflow validation only</text>
    </g>
  </g>
</svg>
""",
    )


def normalize_image(image: np.ndarray) -> np.ndarray:
    lo, hi = np.percentile(image, [1, 99])
    image = np.clip(image, lo, hi)
    return (image - lo) / max(hi - lo, 1e-6)


def crop_to_foreground(image: np.ndarray, label: np.ndarray, margin: int = 44) -> tuple[np.ndarray, np.ndarray]:
    coords = np.argwhere(label > 0)
    if coords.size == 0:
        return image, label
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0) + 1
    y0 = max(int(y0) - margin, 0)
    x0 = max(int(x0) - margin, 0)
    y1 = min(int(y1) + margin, image.shape[0])
    x1 = min(int(x1) + margin, image.shape[1])
    return image[y0:y1, x0:x1], label[y0:y1, x0:x1]


def prepare_display_masks(image: np.ndarray, label: np.ndarray, scale: int = 4) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    image_hi = ndimage.zoom(image, scale, order=3)
    label_float = ndimage.zoom(label.astype(float), scale, order=1)
    label_smooth = ndimage.gaussian_filter(label_float, sigma=1.15)
    label_hi = label_float >= 0.5
    contour_field = label_smooth
    return image_hi, label_hi, contour_field


def blend_overlay(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    overlay = np.dstack([image, image, image])
    color = np.array([0.98, 0.33, 0.38])
    overlay[mask] = overlay[mask] * 0.82 + color * 0.18
    return np.clip(overlay, 0, 1)


def smooth_contour(contour: np.ndarray, points: int = 500) -> np.ndarray:
    if len(contour) < 8:
        return contour
    closed = np.vstack([contour, contour[0]])
    # splprep expects x/y order. The smoothing is for display only.
    try:
        tck, _ = splprep([closed[:, 1], closed[:, 0]], s=len(closed) * 0.85, per=True)
        u_new = np.linspace(0, 1, points)
        x_new, y_new = splev(u_new, tck)
        return np.column_stack([y_new, x_new])
    except ValueError:
        smoothed = ndimage.gaussian_filter1d(closed, sigma=1.8, axis=0, mode="wrap")
        return smoothed


def plot_smooth_contours(ax, contour_field: np.ndarray, **kwargs) -> None:
    contours = measure.find_contours(contour_field, level=0.5)
    contours = sorted(contours, key=len, reverse=True)
    for contour in contours[:2]:
        smooth = smooth_contour(contour)
        ax.plot(smooth[:, 1], smooth[:, 0], **kwargs)


def create_overlay() -> None:
    image, label = load_public_msd_slice()
    image_hi, mask_hi, contour_field = prepare_display_masks(image, label)
    overlay = blend_overlay(image_hi, mask_hi)

    fig, axes = plt.subplots(1, 3, figsize=(12.8, 4.0), dpi=190)
    fig.patch.set_facecolor("#0b1521")
    titles = ["MRI", "Boundary", "Subtle overlay"]
    for ax in axes:
        ax.set_facecolor("#0b1521")
        ax.imshow(image_hi, cmap="gray", vmin=0, vmax=1)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    plot_smooth_contours(axes[1], contour_field, color="#ff4f5f", linewidth=2.7, solid_capstyle="round")
    plot_smooth_contours(axes[2], contour_field, color="#fff0f2", linewidth=1.9, alpha=0.98, solid_capstyle="round")
    axes[2].imshow(overlay)

    for ax, title in zip(axes, titles):
        ax.text(
            0.04,
            0.92,
            title,
            transform=ax.transAxes,
            color="#edf8fb",
            fontsize=13,
            fontweight="bold",
            ha="left",
            va="top",
            bbox={"facecolor": "#07111d", "alpha": 0.72, "edgecolor": "none", "boxstyle": "round,pad=0.35"},
        )

    fig.text(
        0.5,
        0.035,
        "Public MSD Cardiac sample | smoothed boundary for visualization only | no private patient data",
        color="#b8cbd3",
        ha="center",
        fontsize=10,
    )
    plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.12, wspace=0.035)
    fig.savefig(ASSET_DIR / "msd_cardiac_overlay_example.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    image, label = load_public_msd_slice()
    create_banner(image, label)
    create_workflow()
    create_results_summary()
    create_overlay()
    print(ASSET_DIR)


if __name__ == "__main__":
    main()
