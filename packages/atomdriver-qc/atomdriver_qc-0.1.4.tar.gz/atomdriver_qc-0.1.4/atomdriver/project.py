#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
from typing import Any, Generator

import ray
from conformer.project import Project
from conformer.records import SystemRecord
from conformer.systems import System

from atomdriver.abstract_driver import Driver
from atomdriver.accessors import DispatcherClient, DriverAccessor, get_accessor


def run_system_calc(
    accessor: DriverAccessor, system: System
) -> Generator[None, None, SystemRecord]:
    accessor.submit(system)
    record = None
    try:
        while True:  # Oooh. Infinite loop ;)
            completed = accessor.get_completed()
            if not completed:
                yield
            else:
                _sys, record = completed[0]
                break
    finally:
        if record is None:
            record = SystemRecord(stage=accessor.driver)
    return record


class AtomDriverProject(Project):
    DEFAULT_CONFIG = "atomdriver"
    USE_RAY: bool
    RAY_INITED: bool

    def __init__(self, *args, use_ray: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.USE_RAY = use_ray
        self.RAY_INITED = False
        self.init_ray()

    def init_ray(self) -> None:
        if self.RAY_INITED:
            return
        self.RAY_INITED = True

        if self.USE_RAY:
            ray.init()  # TODO: Specify numcpus

    def get_driver(
        self,
        driver: str | Driver,
        use_cache: bool = True,
        use_database: bool | None = None,
        run_calculations: bool = True,
    ) -> DispatcherClient:
        if isinstance(driver, str):
            driver = self.get_stage(driver)
            assert isinstance(driver, Driver)
        return get_accessor(
            driver,
            use_cache=use_cache,
            run_calculatons=run_calculations,
            use_database=use_database,
        )

    def call_stage(self, in_value, stage, args) -> Generator[None, None, Any]:
        # Handle driver calls
        if isinstance(in_value, System) and isinstance(stage, Driver):
            accessor = self.get_driver(stage)
            return run_system_calc(accessor, in_value)  # There aren't any args for this
        return super().call_stage(in_value, stage, args)
