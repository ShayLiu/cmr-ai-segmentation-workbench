#!/usr/bin/env python3
"""Run an nnU-Net console entrypoint with a Python 3.12 distutils shim."""

from __future__ import annotations

import importlib
import sys
import types


def install_distutils_shim() -> None:
    try:
        import distutils.file_util  # noqa: F401
        return
    except ModuleNotFoundError:
        pass

    file_util = importlib.import_module("setuptools._distutils.file_util")
    distutils_module = types.ModuleType("distutils")
    distutils_module.file_util = file_util
    sys.modules["distutils"] = distutils_module
    sys.modules["distutils.file_util"] = file_util


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: run_nnunet_with_distutils.py <plan|train|predict> [args...]")

    install_distutils_shim()

    command = sys.argv[1]
    sys.argv = [f"nnUNetv2_{command}", *sys.argv[2:]]

    if command == "plan_and_preprocess":
        from nnunetv2.experiment_planning.plan_and_preprocess_entrypoints import plan_and_preprocess_entry

        raise SystemExit(plan_and_preprocess_entry())
    if command == "train":
        from nnunetv2.run.run_training import run_training_entry

        raise SystemExit(run_training_entry())
    if command == "predict":
        from nnunetv2.inference.predict_from_raw_data import predict_entry_point

        raise SystemExit(predict_entry_point())

    raise SystemExit(f"Unsupported command: {command}")


if __name__ == "__main__":
    main()
