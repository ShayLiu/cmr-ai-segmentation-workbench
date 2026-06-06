#!/usr/bin/env python3
"""Install the tiny debug nnU-Net trainer into the active Python environment."""

from __future__ import annotations

import importlib.util
from pathlib import Path


TRAINER_SOURCE = '''import os

import torch

from nnunetv2.training.nnUNetTrainer.nnUNetTrainer import nnUNetTrainer


class nnUNetTrainer_tiny_debug(nnUNetTrainer):
    def __init__(self, plans: dict, configuration: str, fold: int, dataset_json: dict,
                 device: torch.device = torch.device("cuda")):
        os.environ.setdefault("nnUNet_n_proc_DA", "0")
        plans["configurations"][configuration]["batch_size"] = min(
            int(plans["configurations"][configuration]["batch_size"]),
            2,
        )
        super().__init__(plans, configuration, fold, dataset_json, device)
        self.num_epochs = 1
        self.num_iterations_per_epoch = 1
        self.num_val_iterations_per_epoch = 1

    def perform_actual_validation(self, save_probabilities: bool = False):
        if self.device.type == "cpu":
            self.print_to_log_file("Skipping full validation export in tiny CPU debug trainer.")
            return
        return super().perform_actual_validation(save_probabilities)
'''

CPU_DEBUG_5EPOCHS_SOURCE = '''import os

import torch

from nnunetv2.training.nnUNetTrainer.nnUNetTrainer import nnUNetTrainer


class nnUNetTrainer_cpu_debug_5epochs(nnUNetTrainer):
    def __init__(self, plans: dict, configuration: str, fold: int, dataset_json: dict,
                 device: torch.device = torch.device("cuda")):
        os.environ.setdefault("nnUNet_n_proc_DA", "0")
        plans["configurations"][configuration]["batch_size"] = min(
            int(plans["configurations"][configuration]["batch_size"]),
            2,
        )
        super().__init__(plans, configuration, fold, dataset_json, device)
        self.num_epochs = 5
        self.num_iterations_per_epoch = 5
        self.num_val_iterations_per_epoch = 2

    def perform_actual_validation(self, save_probabilities: bool = False):
        if self.device.type == "cpu":
            self.print_to_log_file("Skipping full validation export in CPU debug trainer.")
            return
        return super().perform_actual_validation(save_probabilities)
'''

CPU_DEBUG_25EPOCHS_SOURCE = '''import os

import torch

from nnunetv2.training.nnUNetTrainer.nnUNetTrainer import nnUNetTrainer


class nnUNetTrainer_cpu_debug_25epochs(nnUNetTrainer):
    def __init__(self, plans: dict, configuration: str, fold: int, dataset_json: dict,
                 device: torch.device = torch.device("cuda")):
        os.environ.setdefault("nnUNet_n_proc_DA", "0")
        plans["configurations"][configuration]["batch_size"] = min(
            int(plans["configurations"][configuration]["batch_size"]),
            2,
        )
        super().__init__(plans, configuration, fold, dataset_json, device)
        self.num_epochs = 25
        self.num_iterations_per_epoch = 10
        self.num_val_iterations_per_epoch = 3

    def perform_actual_validation(self, save_probabilities: bool = False):
        if self.device.type == "cpu":
            self.print_to_log_file("Skipping full validation export in CPU debug trainer.")
            return
        return super().perform_actual_validation(save_probabilities)
'''


def main() -> None:
    spec = importlib.util.find_spec("nnunetv2")
    if spec is None or spec.submodule_search_locations is None:
        raise SystemExit("nnunetv2 is not installed in the active environment.")

    package_root = Path(next(iter(spec.submodule_search_locations)))
    target = (
        package_root
        / "training"
        / "nnUNetTrainer"
        / "variants"
        / "training_length"
        / "nnUNetTrainer_tiny_debug.py"
    )
    target.write_text(TRAINER_SOURCE, encoding="utf-8")
    print(f"Installed tiny debug trainer: {target}")

    cpu_debug_target = target.with_name("nnUNetTrainer_cpu_debug_5epochs.py")
    cpu_debug_target.write_text(CPU_DEBUG_5EPOCHS_SOURCE, encoding="utf-8")
    print(f"Installed CPU debug trainer: {cpu_debug_target}")

    cpu_debug_25_target = target.with_name("nnUNetTrainer_cpu_debug_25epochs.py")
    cpu_debug_25_target.write_text(CPU_DEBUG_25EPOCHS_SOURCE, encoding="utf-8")
    print(f"Installed CPU debug trainer: {cpu_debug_25_target}")


if __name__ == "__main__":
    main()
