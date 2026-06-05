#!/usr/bin/env bash
set -euo pipefail

DATASET_ID="${DATASET_ID:-1}"
CONFIG="${CONFIG:-2d}"
FOLD="${FOLD:-0}"
DEVICE="${DEVICE:-cuda}"
TRAINER="${TRAINER:-nnUNetTrainer}"
export MPLCONFIGDIR="${MPLCONFIGDIR:-$(pwd)/.cache/matplotlib}"

if [[ -z "${nnUNet_raw:-}" || -z "${nnUNet_preprocessed:-}" || -z "${nnUNet_results:-}" ]]; then
  echo "Please set nnUNet_raw, nnUNet_preprocessed, and nnUNet_results."
  exit 1
fi

mkdir -p "${MPLCONFIGDIR}"

nnUNetv2_plan_and_preprocess -d "${DATASET_ID}" --verify_dataset_integrity
nnUNetv2_train "${DATASET_ID}" "${CONFIG}" "${FOLD}" -tr "${TRAINER}" -device "${DEVICE}"
