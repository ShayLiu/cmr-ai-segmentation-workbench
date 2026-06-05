#!/usr/bin/env python3
"""Create privacy-safe README visuals for the project.

The README should not present weak pseudo-labels as a polished segmentation
result. These assets emphasize workflow, quality control, and benchmark status
until an expert-labeled SAX baseline is available.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "assets"


def write_text(path: Path, text: str) -> None:
    path.write_text(text.strip() + "\n", encoding="utf-8")


def create_banner() -> None:
    write_text(
        ASSET_DIR / "cmr_workbench_banner.svg",
        """
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
    <text x="18" y="26" fill="#e4f7fb" font-family="Inter, Arial, sans-serif" font-size="18" font-weight="700">Quality gate before claims</text>
    <g font-family="Inter, Arial, sans-serif" font-size="13" fill="#d4e9ef">
      <g transform="translate(18 58)">
        <rect width="274" height="38" rx="10" fill="#12283a" stroke="#42677a"/>
        <text x="16" y="25">1. Public SAX benchmark baseline</text>
      </g>
      <g transform="translate(18 112)">
        <rect width="274" height="38" rx="10" fill="#143044" stroke="#4e7586"/>
        <text x="16" y="25">2. Expert-label QC + failure modes</text>
      </g>
      <g transform="translate(18 166)">
        <rect width="274" height="38" rx="10" fill="#163b3f" stroke="#5a8584"/>
        <text x="16" y="25">3. Dice / HD95 before visual claims</text>
      </g>
    </g>
  </g>
  <g transform="translate(84 78)">
    <text x="0" y="0" fill="#dff7ff" font-family="Inter, Arial, sans-serif" font-size="56" font-weight="700">CMR AI Segmentation Workbench</text>
    <text x="0" y="58" fill="#a8d5df" font-family="Inter, Arial, sans-serif" font-size="25">Reproducible cardiac MRI segmentation workflows with benchmark-first validation</text>
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


def create_qc_gate() -> None:
    write_text(
        ASSET_DIR / "segmentation_qc_gate.svg",
        """
<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="420" viewBox="0 0 1180 420" role="img" aria-label="SAX segmentation quality gate">
  <rect width="1180" height="420" rx="18" fill="#fbfcfd"/>
  <text x="42" y="54" fill="#163244" font-family="Inter, Arial, sans-serif" font-size="30" font-weight="700">SAX Segmentation Quality Gate</text>
  <text x="42" y="86" fill="#526570" font-family="Inter, Arial, sans-serif" font-size="17">Pseudo-labels can validate the pipeline, but expert-labeled SAX benchmarks are required before claiming segmentation quality.</text>
  <g font-family="Inter, Arial, sans-serif">
    <g transform="translate(52 126)">
      <rect width="250" height="170" rx="14" fill="#eaf3f5" stroke="#b6ccd4"/>
      <text x="22" y="38" fill="#173244" font-size="21" font-weight="700">Current</text>
      <text x="22" y="76" fill="#526570" font-size="16">Workflow runs end to end</text>
      <text x="22" y="106" fill="#526570" font-size="16">Pseudo-label debug only</text>
      <text x="22" y="136" fill="#9a5d18" font-size="16" font-weight="700">Not a performance claim</text>
    </g>
    <g transform="translate(354 126)">
      <rect width="250" height="170" rx="14" fill="#fff5e8" stroke="#dec6a3"/>
      <text x="22" y="38" fill="#173244" font-size="21" font-weight="700">Reject</text>
      <text x="22" y="76" fill="#526570" font-size="16">Poor boundary adherence</text>
      <text x="22" y="106" fill="#526570" font-size="16">Unreviewed RV contours</text>
      <text x="22" y="136" fill="#a94442" font-size="16" font-weight="700">No homepage showcase</text>
    </g>
    <g transform="translate(656 126)">
      <rect width="250" height="170" rx="14" fill="#edf4ea" stroke="#b6ccb1"/>
      <text x="22" y="38" fill="#173244" font-size="21" font-weight="700">Required</text>
      <text x="22" y="76" fill="#526570" font-size="16">ACDC / expert SAX labels</text>
      <text x="22" y="106" fill="#526570" font-size="16">Dice + HD95 by structure</text>
      <text x="22" y="136" fill="#1f7a62" font-size="16" font-weight="700">Then publish visuals</text>
    </g>
    <g transform="translate(958 126)">
      <rect width="170" height="170" rx="14" fill="#eef1fb" stroke="#bac3e2"/>
      <text x="22" y="38" fill="#173244" font-size="21" font-weight="700">Labels</text>
      <circle cx="32" cy="75" r="7" fill="#3b8ff0"/>
      <text x="50" y="81" fill="#526570" font-size="15">RV</text>
      <circle cx="32" cy="106" r="7" fill="#f3b43f"/>
      <text x="50" y="112" fill="#526570" font-size="15">LV blood</text>
      <circle cx="32" cy="137" r="7" fill="#e94a54"/>
      <text x="50" y="143" fill="#526570" font-size="15">Myo</text>
    </g>
  </g>
  <text x="52" y="358" fill="#5b6c76" font-family="Inter, Arial, sans-serif" font-size="16">Publication-grade claim threshold: expert-reviewed contours, held-out validation, structure-wise metrics, and representative success/failure examples.</text>
</svg>
""",
    )


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    create_banner()
    create_workflow()
    create_results_summary()
    create_qc_gate()
    print(ASSET_DIR)


if __name__ == "__main__":
    main()
