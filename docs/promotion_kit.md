# Promotion Kit

Use these posts to introduce the project accurately. The safest framing is: reproducible research workflow, not clinical model.

Project URL: https://github.com/ShayLiu/cmr-ai-segmentation-workbench

## One-Line Description

CMR AI Segmentation Workbench is a reproducible cardiac MRI SAX segmentation workflow with public ACDC validation, Dice/HD95 reporting, QC overlays, and failure-mode analysis.

## Current Evidence Snapshot

- Public benchmark: ACDC fold 0 validation
- Model: nnU-Net v2, 2D CPU debug run, 300 shortened epochs
- Postprocessing: conservative anatomical cleanup
- Metrics: mean Dice `0.8740`, mean HD95 `5.31`
- Boundary: reproducible research workflow, not a clinical model or SOTA claim

## Short English Post

I’m building CMR AI Segmentation Workbench, an open-source workflow for reproducible cardiac MRI SAX segmentation research.

Current public benchmark snapshot:

- ACDC fold 0 validation
- nnU-Net v2 2D CPU debug run
- Dice/HD95 by RV, myocardium, and LV
- Mean Dice: 0.8740; mean HD95: 5.31
- QC overlays and representative failure cases

The goal is not to claim SOTA performance, but to make the full medical imaging AI workflow easier to reproduce: data conversion, nnU-Net formatting, prediction, postprocessing, evaluation, visualization, privacy boundaries, and failure analysis.

No private patient data, DICOM/NIfTI files, or checkpoints are included.

GitHub: https://github.com/ShayLiu/cmr-ai-segmentation-workbench

Suggested tags: #MedicalImaging #CardiacMRI #CMR #DeepLearning #OpenSource #nnUNet #MedicalAI

## Long English Post

I’m building an open-source project called CMR AI Segmentation Workbench:

https://github.com/ShayLiu/cmr-ai-segmentation-workbench

The goal is to make cardiac MRI SAX segmentation workflows easier to reproduce, audit, and teach. Instead of presenting a black-box clinical model, the repository focuses on the practical research workflow around medical imaging AI:

- converting cardiac MRI data into nnU-Net-compatible format
- training and predicting with nnU-Net v2
- computing structure-wise Dice and HD95
- generating QC overlays for expert labels and predictions
- documenting postprocessing choices
- reporting representative failure cases instead of hiding them
- keeping private data, checkpoints, DICOM files, and NIfTI files out of Git

Current public benchmark snapshot:

- ACDC fold 0 validation
- nnU-Net v2 2D CPU debug run, 300 shortened epochs
- RV Dice 0.8579, myocardium Dice 0.8547, LV Dice 0.9093
- Mean Dice 0.8740; mean HD95 5.31

This is not a clinical model and not a state-of-the-art claim. The current contribution is a transparent, reproducible research workflow with metrics, QC figures, and failure analysis. I would especially appreciate feedback from cardiac MRI, medical imaging AI, and reproducibility communities on evaluation protocol, visualization, and the next baseline to prioritize.

## Reddit Project Post

Title:

```text
[P] CMR AI Segmentation Workbench: reproducible cardiac MRI segmentation workflows with nnU-Net
```

Body:

```text
Hi everyone,

I’m building an open-source research workbench for cardiac MRI SAX segmentation:

https://github.com/ShayLiu/cmr-ai-segmentation-workbench

The goal is not to claim SOTA performance, but to make cardiac MRI segmentation workflows easier to reproduce, audit, and teach.

Current features:
- nnU-Net v2 workflow scaffolding
- synthetic smoke test dataset
- public ACDC fold 0 validation with Dice/HD95
- prediction and expert-label QC overlays
- postprocessing ablation
- representative failure-case analysis
- privacy checklist and medical data release boundaries

Current ACDC CPU debug result:
- RV Dice 0.8579
- Myocardium Dice 0.8547
- LV Dice 0.9093
- Mean Dice 0.8740

The project does not include private DICOM/NIfTI files or trained checkpoints.

I’d appreciate feedback on:
1. reproducibility structure,
2. medical imaging data-format handling,
3. evaluation metrics to prioritize next,
4. how to make this more useful for CMR researchers.
```

## 中文短文案

我在做一个开源的心脏磁共振 CMR SAX 分割研究工作台：

CMR AI Segmentation Workbench  
https://github.com/ShayLiu/cmr-ai-segmentation-workbench

这个项目不是临床诊断模型，也不包装成 SOTA。它的目标是帮助医学影像/心血管影像研究者更快搭建可复现的 AI 分割流程。

目前已经补上公开 ACDC fold 0 验证：

- RV Dice 0.8579
- Myocardium Dice 0.8547
- LV Dice 0.9093
- Mean Dice 0.8740
- Mean HD95 5.31

仓库包含 nnU-Net v2 数据准备、训练、预测、后处理、Dice/HD95 评估、真实 QC overlay 和 failure-case analysis。不包含任何私有患者数据、DICOM/NIfTI 文件或模型 checkpoint。

我想把它慢慢做成一个面向 CMR AI 研究者的开源工作台：既能帮助临床研究者入门，也能作为后续 full GPU nnU-Net、MONAI、MedSAM、可视化和论文复现实验的基础。

欢迎感兴趣的同学、医生、影像研究者和工程师提 issue 或建议。

## 中文长文案

最近我把一个心脏磁共振 CMR SAX 分割相关的研究工作流整理成了开源项目：

CMR AI Segmentation Workbench  
https://github.com/ShayLiu/cmr-ai-segmentation-workbench

做医学影像 AI 的时候，最难的往往不只是模型本身，而是前面的数据格式、DICOM/NIfTI 转换、nnU-Net 目录结构、训练参数、结果记录、隐私边界和复现流程。这个项目想解决的正是这些“科研中真正消耗时间”的问题。

目前项目已经包含：

- ACDC 公开数据 fold 0 验证
- nnU-Net v2 训练、预测和后处理流程
- RV / myocardium / LV 的 Dice 和 HD95
- 真实 expert-label / prediction QC overlay
- postprocessing ablation
- failure-case analysis
- 医学数据隐私和发布前检查清单

当前 ACDC CPU debug 结果是：RV Dice 0.8579，myocardium Dice 0.8547，LV Dice 0.9093，mean Dice 0.8740，mean HD95 5.31。

我不会把它包装成临床可用模型，也不说它是 SOTA。当前阶段更准确的定位是：一个开放、可复现、隐私友好的 CMR segmentation research workflow。后续计划继续补 full GPU nnU-Net baseline、3D training、MONAI baseline 和 MedSAM adaptation。

如果你也在做医学影像 AI、心血管影像、CMR 或者想学习 nnU-Net workflow，欢迎看看这个仓库，也欢迎给建议。

## Recommended Communities

1. GitHub README and topics
2. WeChat/research group chats for trusted early feedback
3. LinkedIn for medical imaging AI and CMR researchers
4. X for open-source AI engineers and imaging researchers
5. MONAI discussion forum for workflow feedback
6. Reddit `r/MachineLearning` with `[P]` project tag after one more full GPU baseline
7. Zhihu/Xiaohongshu only if the post stays educational rather than hype-driven

## Do Not Claim

- Do not claim clinical diagnosis or treatment use.
- Do not claim SOTA performance.
- Do not claim expert-level validation from pseudo-label experiments.
- Do not imply private data are included in the repository.
