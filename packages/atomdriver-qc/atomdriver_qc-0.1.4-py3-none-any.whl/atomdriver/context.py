#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import os
import platform
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, Optional
from uuid import UUID

import psutil


@dataclass
class ResourceAllocation:
    # Default values
    cpus: int = 1
    gpus: int = 0  # 0 --> GPU disabled
    # None -> (total memory) * cpus / (total_cpus)
    memory: Optional[int] = None  # 0 --> No limit
    environ: Dict[str, str] = field(default_factory=lambda: os.environ.copy())
    basepath: Optional[Path] = None

    # Handle if the basepath is a tempdir for cleanup
    _tempdir: Optional[TemporaryDirectory] = None

    def __post_init__(self):
        if self.basepath is None:
            self._tempdir = TemporaryDirectory()
            self.basepath = Path(self._tempdir.name)

        # Default memory is 90% of the per-cpu memory
        machine = Machine()
        cpu_fraction = self.cpus / machine.cpus
        if self.memory is None:
            self.memory = int(machine.memory * cpu_fraction * 0.90)

        # Validate the allocation
        if cpu_fraction > 1.0:
            raise ValueError(
                f"More CPUs request ({self.cpus}) than available ({machine.cpus})"
            )
        if self.memory > machine.memory:
            raise ValueError(
                f"More CPUs request ({self.memory}) than available ({machine.memory})"
            )

    def cleanup(self):
        if self._tempdir is not None:
            self._tempdir.cleanup()

    def __del__(self):
        self.cleanup()


@dataclass
class Machine:
    """
    Accounting class for hardware
    """

    @staticmethod
    def get_info() -> int:
        return {
            "architecture": platform.architecture(),
            "machine": platform.machine(),
            "platform": platform.platform(),
            "processor": platform.processor(),
            "system": platform.system(),
        }

    cpus: int = field(default_factory=psutil.cpu_count)
    gpus: int = 0  # Not supported...
    memory: int = field(default_factory=lambda: psutil.virtual_memory().total >> 20)
    hostname: str = field(default_factory=platform.node)
    # See https://stackoverflow.com/questions/2461141/get-a-unique-computer-id-in-python-on-windows-and-linux
    hardware_id: UUID = field(default_factory=lambda: uuid.UUID(int=uuid.getnode()))
    info: Dict[str, str] = field(default_factory=get_info)
