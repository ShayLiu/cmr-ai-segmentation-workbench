# Promotion Kit

Use these posts to introduce the project accurately. The safest framing is: reproducible research workflow, not clinical model.

Project URL: https://github.com/ShayLiu/cmr-ai-segmentation-workbench

## One-Line Description

CMR AI Segmentation Workbench is an open, privacy-conscious, reproducible workflow for cardiac MRI segmentation research.

## Short English Post

I just open-sourced CMR AI Segmentation Workbench, a reproducible research workflow for cardiac MRI segmentation.

The repository focuses on practical medical imaging AI workflows:

- nnU-Net v2 dataset formatting and debug training
- synthetic smoke tests
- public MSD Cardiac debug runs
- privacy-preserving local pseudo-label workflows
- documentation for DICOM/NIfTI, reproducibility, and medical data boundaries

This is not a clinical model and does not include private patient data. The goal is to help medical imaging researchers build transparent and reproducible CMR segmentation pipelines.

GitHub: https://github.com/ShayLiu/cmr-ai-segmentation-workbench

Suggested tags: #MedicalImaging #CardiacMRI #DeepLearning #OpenSource #nnUNet #MONAI #MedicalAI

## Long English Post

I have started an open-source project called CMR AI Segmentation Workbench:

https://github.com/ShayLiu/cmr-ai-segmentation-workbench

The goal is to make cardiac MRI segmentation workflows easier to reproduce, audit, and teach. Instead of presenting a black-box clinical model, the project focuses on the research workflow around medical imaging AI:

- converting data into nnU-Net-compatible structure
- documenting DICOM/NIfTI formatting assumptions
- running synthetic smoke tests
- running public MSD Cardiac debug training
- supporting privacy-preserving local pseudo-label experiments
- recording training outputs, limitations, and failure modes

The repository does not distribute private DICOM/NIfTI files, trained checkpoints, or patient-level source manifests. Pseudo-label experiments are explicitly documented as workflow validation rather than expert-labeled model performance.

I am especially interested in feedback from cardiac MRI, medical imaging AI, and reproducibility communities on evaluation metrics, visualization examples, and how to make the workflow more useful for clinical researchers.

## Reddit Project Post

Title:

```text
[P] CMR AI Segmentation Workbench: reproducible cardiac MRI segmentation workflows with nnU-Net
```

Body:

```text
Hi everyone,

I’m building an open-source research workbench for cardiac MRI segmentation:

https://github.com/ShayLiu/cmr-ai-segmentation-workbench

The goal is not to claim SOTA performance, but to make cardiac MRI segmentation workflows easier to reproduce and audit.

Current features:
- nnU-Net v2 workflow scaffolding
- synthetic smoke test dataset
- public MSD Cardiac debug run
- local pseudo-label workflow for CorSeg SAX outputs
- DICOM/NIfTI formatting notes
- privacy checklist for medical imaging data
- result logs documenting hardware, limitations, and failure modes

The project does not include private DICOM/NIfTI files or trained checkpoints. Pseudo-label results are clearly separated from expert-labeled validation.

I’d appreciate feedback on:
1. reproducibility structure,
2. medical imaging data-format handling,
3. evaluation metrics to prioritize next,
4. how to make this more useful for CMR researchers.
```

## 中文短文案

我开源了一个心脏磁共振 CMR 分割研究工作台：

CMR AI Segmentation Workbench  
https://github.com/ShayLiu/cmr-ai-segmentation-workbench

这个项目不是临床诊断模型，也不包含任何私有患者数据。它的目标是帮助医学影像/心血管影像研究者更快搭建可复现的 AI 分割流程，包括：

- nnU-Net v2 数据格式整理
- DICOM/NIfTI 处理说明
- synthetic smoke test
- 公开 MSD Cardiac debug run
- 本地 pseudo-label workflow
- 医学数据隐私与发布检查清单
- 训练结果和失败问题记录模板

我想把它慢慢做成一个面向 CMR AI 研究者的开源工作台：既能帮助临床研究者入门，也能作为后续 MONAI、MedSAM、ACDC baseline、可视化和论文复现实验的基础。

欢迎感兴趣的同学、医生、影像研究者和工程师提 issue 或建议。

## 中文长文案

最近我把一个心脏磁共振 CMR 分割相关的研究工作流整理成了开源项目：

CMR AI Segmentation Workbench  
https://github.com/ShayLiu/cmr-ai-segmentation-workbench

做医学影像 AI 的时候，最难的往往不只是模型本身，而是前面的数据格式、DICOM/NIfTI 转换、nnU-Net 目录结构、训练参数、结果记录、隐私边界和复现流程。这个项目想解决的正是这些“科研中真正消耗时间”的问题。

目前项目已经包含：

- synthetic smoke test，用来快速验证环境和数据结构
- public MSD Cardiac debug run，用公开数据跑通真实医学影像训练流程
- local pseudo-label workflow，用于在不上传私有数据的前提下测试本地 CMR 分割流程
- DICOM/NIfTI 和 nnU-Net 数据格式说明
- 医学数据隐私和发布前检查清单
- 训练结果、失败模式和限制的记录模板

我不会把它包装成临床可用模型。当前阶段更准确的定位是：一个开放、可复现、隐私友好的 CMR segmentation research workflow。后续计划继续补 ACDC baseline、Dice/HD95 评估、可视化 overlay、MONAI baseline 和 MedSAM adaptation。

如果你也在做医学影像 AI、心血管影像、CMR 或者想学习 nnU-Net workflow，欢迎看看这个仓库，也欢迎给建议。

## Recommended Communities

- GitHub topics and README
- LinkedIn or X for English research audience
- Reddit `r/MachineLearning` with `[P]` project tag
- MONAI community discussions for workflow feedback
- Zhihu, WeChat, Xiaohongshu, or research group chat for Chinese medical imaging researchers

## Do Not Claim

- Do not claim clinical diagnosis or treatment use.
- Do not claim SOTA performance.
- Do not claim expert-level validation from pseudo-label experiments.
- Do not imply private data are included in the repository.
