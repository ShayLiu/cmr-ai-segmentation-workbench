#!/usr/bin/env bash
set -euo pipefail

DATASET_ID="${DATASET_ID:-1}"
CONFIG="${CONFIG:-2d}"
FOLD="${FOLD:-0}"
INPUT_DIR="${INPUT_DIR:-${nnUNet_raw}/Dataset001_ACDC/imagesTs}"
OUTPUT_DIR="${OUTPUT_DIR:-predictions/acdc_nnunet_${CONFIG}_fold${FOLD}}"
export MPLCONFIGDIR="${MPLCONFIGDIR:-$(pwd)/.cache/matplotlib}"

if [[ -z "${nnUNet_raw:-}" || -z "${nnUNet_results:-}" ]]; then
  echo "Please set nnUNet_raw and nnUNet_results."
  exit 1
fi

mkdir -p "${OUTPUT_DIR}" "${MPLCONFIGDIR}"

nnUNetv2_predict \
  -i "${INPUT_DIR}" \
  -o "${OUTPUT_DIR}" \
  -d "${DATASET_ID}" \
  -c "${CONFIG}" \
  -f "${FOLD}"
