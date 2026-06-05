# Changelog

## v0.1.0 - 2026-06-06

Initial public release of CMR AI Segmentation Workbench.

### Added

- nnU-Net v2 workflow scaffold for cardiac MRI segmentation research
- Tiny synthetic nnU-Net smoke test
- Public MSD Cardiac debug workflow and result note
- Local CorSeg SAX pseudo-label preparation workflow and result note
- ACDC preparation, training, and prediction script scaffold
- Python 3.12 distutils compatibility wrapper for nnU-Net preprocessing
- CPU-friendly tiny debug trainer installer
- DICOM/NIfTI and nnU-Net data format documentation
- Medical data disclaimer, model/data statement, and release checklist
- Promotion kit and launch plan for research outreach

### Privacy

- No private DICOM files, NIfTI files, model checkpoints, predictions, or source manifests are included.
- Private-data workflows are documented as local-only and privacy-preserving.

### Limitations

- The project is a research workflow, not a clinical model.
- Pseudo-label results are workflow validation, not expert-labeled performance.
- Public benchmark baseline training on ACDC is planned but not yet completed.
