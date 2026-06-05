# Launch Plan

This plan is for introducing CMR AI Segmentation Workbench to research and open-source communities without overstating clinical or model-performance claims.

## Positioning

Primary message:

> An open, privacy-conscious, reproducible workflow for cardiac MRI segmentation research.

Do not position the project as a clinical model, diagnostic tool, or SOTA segmentation system.

## Audience

| Audience | What they care about | Best message |
|---|---|---|
| Medical imaging AI researchers | Reproducibility, benchmarks, evaluation | A reusable CMR segmentation workflow scaffold |
| Cardiac MRI researchers | DICOM/NIfTI, LV/RV structures, CMR workflow | A bridge between CMR data and AI segmentation pipelines |
| Clinical researchers learning AI | Practical steps, privacy, documentation | A teachable nnU-Net-based starting point |
| Open-source engineers | Clean scripts, issues, roadmap | A focused medical imaging project with clear contribution boundaries |

## Launch Sequence

### Day 1: GitHub Ready

- Confirm README first screen is clear.
- Confirm repository description and topics are set.
- Confirm no private data, DICOM, NIfTI, checkpoints, or manifests are tracked.
- Create a v0.1.0 GitHub release.

### Day 2: Chinese Research Network

Post the short Chinese text from `docs/promotion_kit.md` to:

- WeChat Moments
- research group chat
- imaging/AI student groups
- Zhihu or Xiaohongshu if appropriate

Main goal: collect early feedback from people who know CMR and medical imaging.

### Day 3: English Research Network

Post the short English text to:

- LinkedIn
- X
- personal website or lab page if available

Main goal: reach imaging AI researchers and engineers.

### Day 4-7: Community Feedback

Open or share selectively in:

- MONAI community channels
- Reddit `r/MachineLearning` as a `[P]` project post
- medical imaging AI groups

Ask for feedback on reproducibility, metrics, and visualization needs.

## Suggested First GitHub Issues

Create these issues to show the project is alive and contribution-friendly:

1. Add ACDC dataset preparation and baseline result
2. Add Dice and HD95 evaluation script
3. Add prediction overlay visualization
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

The next scientifically meaningful milestone is a public ACDC baseline with:

- dataset version/source
- preprocessing command
- training configuration
- validation split
- Dice and HD95
- prediction overlay examples
- failure cases

That milestone is much more valuable than another private pseudo-label debug run.
