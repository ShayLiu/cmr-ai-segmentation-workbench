# Launch Plan

This plan is for introducing CMR AI Segmentation Workbench to research and open-source communities without overstating clinical or model-performance claims.

## Positioning

Primary message:

> A reproducible cardiac MRI SAX segmentation workflow with public ACDC validation, Dice/HD95 reporting, QC overlays, and failure-mode analysis.

Do not position the project as a clinical model, diagnostic tool, or SOTA segmentation system.

## Audience

| Audience | What they care about | Best message |
|---|---|---|
| Medical imaging AI researchers | Reproducibility, benchmarks, evaluation | Public ACDC validation plus transparent workflow and failure analysis |
| Cardiac MRI researchers | SAX stacks, LV/RV/myocardium labels, CMR workflow | A bridge between CMR data and AI segmentation pipelines |
| Clinical researchers learning AI | Practical steps, privacy, documentation | A teachable nnU-Net-based starting point |
| Open-source engineers | Clean scripts, issues, roadmap | A focused medical imaging project with clear contribution boundaries |

## Launch Sequence

### Day 1: GitHub Ready

- Confirm README first screen is clear.
- Confirm repository description and topics are set.
- Confirm no private data, DICOM, NIfTI, checkpoints, or manifests are tracked.
- Confirm ACDC metrics, QC overlay, and failure analysis are visible from the README.
- Keep release language conservative: workflow milestone, not model-performance release.

### Day 2: Chinese Research Network

Post the short Chinese text from `docs/promotion_kit.md` to:

- WeChat Moments
- research group chat
- imaging/AI student groups
- Zhihu or Xiaohongshu only if the post remains educational and non-hype

Main goal: collect early feedback from people who know CMR and medical imaging. Ask them whether the failure cases, evaluation metrics, and next baseline are convincing.

### Day 3: English Research Network

Post the short English text to:

- LinkedIn
- X
- personal website or lab page if available

Main goal: reach imaging AI researchers and engineers. Use the ACDC mean Dice/HD95 as an evidence snapshot, but explicitly state that it is a CPU debug workflow milestone.

### Day 4-7: Community Feedback

Open or share selectively in:

- MONAI community channels
- medical imaging AI groups
- Reddit `r/MachineLearning` as a `[P]` project post after one more stronger baseline

Ask for feedback on reproducibility, metrics, and visualization needs.

## Suggested First GitHub Issues

Create these issues to show the project is alive and contribution-friendly:

1. Run full GPU nnU-Net 2D ACDC baseline
2. Add 3D full-resolution nnU-Net ACDC baseline
3. Add ED vs ES stratified validation metrics
4. Add MONAI baseline
5. Add documentation for common CMR DICOM pitfalls

## Success Metrics

Early success is not stars alone. Track:

- useful issues from real users
- forks from medical imaging researchers
- reproducibility feedback
- requests for datasets or visualization
- one public benchmark baseline completed

## Next Credibility Milestone

The next scientifically meaningful milestone is a full GPU ACDC baseline with:

- dataset version/source
- preprocessing command
- training configuration
- validation split
- Dice and HD95
- prediction overlay examples
- failure cases

That milestone is much more valuable than another private pseudo-label debug run or a purely visual README improvement.
