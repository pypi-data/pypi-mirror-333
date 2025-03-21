#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
from copy import copy
from queue import Queue
from typing import (
    Callable,
    ClassVar,
    Dict,
    Iterable,
    List,
    Tuple,
)
from uuid import UUID

import ray
from conformer.db.models import DBSystemRecord
from conformer.records import RecordStatus, SystemRecord
from conformer.systems import System
from conformer_core.accessors import Accessor, CompositeAccessor, batched
from lru import LRU

from atomdriver.abstract_driver import Driver


class DriverAccessorLayer(Accessor[System, Tuple[System, SystemRecord | None]]):
    driver: Driver

    def __init__(self, driver: Driver) -> None:
        super().__init__()
        self.driver = driver

    def submit(self, system: System) -> None:
        # Override the generic submit because there are no kwargs
        self.num_submitted += 1
        self.in_queue.put(system)

    def update(self, records: Iterable[SystemRecord]) -> None:
        ...


class DictCacheLayer(DriverAccessorLayer):
    cache: LRU
    MAX_SIZE = 5000

    def __init__(self, driver: Driver) -> None:
        super().__init__(driver)
        self.cache = LRU(self.MAX_SIZE)

    def churn(self):
        """Moves data from then `in_queue` to the `out_queue`"""
        while not self.in_queue.empty():
            sys = self.in_queue.get()
            rec = self.cache.get(sys.fingerprint, None)
            self.out_queue.put((sys, rec.swap_system(sys) if rec is not None else rec))
            self.in_queue.task_done()

    def update(self, results: Iterable[SystemRecord]) -> None:
        # Update behavior for LRU cache is slightly different than dict
        for r in results:
            self.cache[r.system.fingerprint] = r
        # Normal dict usage
        # self.cache.update((r.system.fingerprint, r) for r in results))

    def clear_cache(self) -> None:
        self.cache.clear()


class DBLayer(DriverAccessorLayer):
    to_query: Dict[str, int]
    batch_size: ClassVar[int] = 100

    def __init__(self, driver: Driver) -> None:
        super().__init__(driver)
        self.to_query = {}

    def submit(self, system: System) -> None:
        # Account for duplicates. The DB code is really aggressive about deduplication
        self.num_submitted += 1
        try:
            self.to_query[system.fingerprint].append(system)
        except KeyError:
            self.to_query[system.fingerprint] = [system]
            self.in_queue.put(system)

        # Autocommit when enough jobs have been submitted
        if len(self.to_query) >= self.batch_size:
            self.churn()

    def churn(self) -> None:
        systems: Dict[str, System] = {}

        while not self.in_queue.empty():
            s = self.in_queue.get()
            systems[s.fingerprint] = s

            if len(systems) >= self.batch_size or self.in_queue.empty():
                hits = DBSystemRecord.get_system_records(self.driver, systems.values())

                for f, sys in systems.items():
                    try:
                        rec = hits[sys]
                        # TODO: Add options for `rerun failed` use case
                        if rec.status not in (
                            RecordStatus.COMPLETED,
                            RecordStatus.FAILED,
                        ):
                            rec = None
                    except KeyError:  # Missing system
                        rec = None

                    for real_sys in self.to_query.pop(f):
                        self.out_queue.put(
                            (
                                real_sys,
                                rec.swap_system(real_sys) if rec is not None else rec,
                            )
                        )
                    self.in_queue.task_done()

                # Reset for next batch
                systems.clear()

    def update(self, records: SystemRecord) -> None:
        for records in batched(records, self.batch_size):
            DBSystemRecord.add_or_update_system_record(list(records))


class LocalCalcLayer(DriverAccessorLayer):
    driver: Driver

    def churn(self):
        """Moves data from then `in_queue` to the `out_queue`"""
        count = 0
        while not self.in_queue.empty():
            sys = self.in_queue.get()
            self.out_queue.put((sys, self.driver(sys)))
            self.in_queue.task_done()

            # Return in batches (helps with progress bars)
            count += 1
            if count >= self.driver.opts.batch_size:
                break


@ray.remote
def remote_calcs(driver: Driver, systems: Tuple[System]) -> List[SystemRecord]:
    # Get a new remote file path...
    if driver.allocation:
        cpus = driver.allocation.cpus
    else:
        cpus = driver.opts.cpus
    driver.provision(cpus=cpus, force=True)
    if not driver.allocation.basepath.exists():
        raise Exception("BASEPATH DOES NOT EXIST!")

    driver.configure()
    results: List[SystemRecord] = []
    for system in systems:
        try:
            result = driver(system)
            results.append(result)
        except Exception as e:  # Should be robust to other failsure
            result = SystemRecord(
                stage=driver, status=RecordStatus.FAILED, meta={"error": str(e)}
            )
            results.append(result)
    driver.cleanup()
    return results


class RayCalcLayer(DriverAccessorLayer):
    NUM_RETURNS = 100
    TIMEOUT = 0.05

    running_systems: Dict[str, int]
    tasks: List[ray.ObjectRef]
    driver_ref = ray.ObjectRef

    def __init__(self, driver: Driver) -> None:
        # Use a copy of the driver
        driver_copy = copy(driver)
        driver_copy.cleanup()  # Put a clean version the driver into Ray (maybe copy first?)

        super().__init__(driver_copy)
        self.running_systems = {}
        self.tasks = []

        self.driver_ref = ray.put(driver_copy)

        self.sub_fn = remote_calcs.options(num_cpus=driver.opts.cpus).remote

    def submit(self, system: System) -> None:
        super().submit(system)

        if self.in_queue.qsize() >= self.driver.opts.batch_size:
            self.sub_calcs()

    def sub_calcs(self):
        systems = []
        while not self.in_queue.empty():
            s = self.in_queue.get()
            try:
                self.running_systems[s.fingerprint].append(s)
            except KeyError:
                self.running_systems[s.fingerprint] = [s]
                systems.append(s)

        for batch in batched(systems, self.driver.opts.batch_size):
            self.tasks.append(self.sub_fn(self.driver_ref, batch))

    def check_calcs(self) -> None:
        if not self.tasks:
            return  # Don't wait on an empty check
        done, self.tasks = ray.wait(
            self.tasks,
            num_returns=min(len(self.tasks), self.NUM_RETURNS),
            fetch_local=True,
            timeout=self.TIMEOUT,
        )
        for records in ray.get(done):
            for r in records:
                r: SystemRecord

                # Report duplicates
                for real_sys in self.running_systems.pop(r.system.fingerprint):
                    self.out_queue.put((real_sys, r.swap_system(real_sys)))
                    self.in_queue.task_done()

    def churn(self):
        self.sub_calcs()
        self.check_calcs()

    def __del__(self) -> None:
        # Cancel all running tasks
        if ray.is_initialized():  # Check if it's running
            for t in self.tasks:
                ray.cancel(t)


class DriverAccessor(CompositeAccessor[System, Tuple[System, SystemRecord]]):
    driver: Driver
    running_systems: Dict[str, int]

    def __init__(self, driver: Driver, layers: List[DriverAccessorLayer]) -> None:
        super().__init__(layers)
        self.driver = driver
        self.running_systems = {}

    @classmethod
    def get_accessor(
        cls,
        driver: Driver,
        use_cache=True,
        use_database=True,
        run_calculators=True,
        use_ray=True,
    ) -> "DriverAccessor":
        """Returns an accessor matching the configuration"""
        layers = []

        if use_cache:
            layers.append(DictCacheLayer(driver))
        if use_database:
            layers.append(DBLayer(driver))
        if run_calculators:
            if use_ray:
                layers.append(RayCalcLayer(driver))
            else:
                layers.append(LocalCalcLayer(driver))
        return cls(driver, layers)

    def submit(self, system: System) -> None:
        # Override the generic submit because there are no kwargs
        self.num_submitted += 1
        self.in_queue.put(system)

    def back_propogate(self, layer_idx: int, records: Iterable) -> None:
        for layer in self.layers[0:layer_idx]:
            layer.update(records)

    def churn(self) -> None:
        # Deduplicate systems and process input queue
        new_systems: List[System] = []
        completed: List[SystemRecord] = []
        while not self.in_queue.empty():
            s = self.in_queue.get()
            try:
                self.running_systems[s.fingerprint].append(s)
            except KeyError:
                self.running_systems[s.fingerprint] = [s]
                new_systems.append(s)

        # Go through layers and propogate
        for i, layer in enumerate(self.layers):
            # Add system to the layer
            for s in new_systems:
                layer.submit(s)

            new_systems.clear()
            completed.clear()

            for res in layer.get_completed():
                if res[1] is None:  # Check if the record is None
                    new_systems.append(res[0])
                    continue

                # Process for returning
                s, r = res
                completed.append(r)  # For updating previous layers

                real_systems = self.running_systems.pop(s.fingerprint)
                for real_sys in real_systems:  # Repeat as needed
                    assert not isinstance(r, System)
                    self.out_queue.put((real_sys, r.swap_system(real_sys)))
                    self.in_queue.task_done()

            # Update ALL the layers!
            self.back_propogate(i, completed)

        # Drivers should ALWAYS return a result
        if new_systems:
            for s in new_systems:
                self.out_queue.put((s, None))
                self.in_queue.task_done()
            raise Exception("All jobs should complete")


class Dispatcher:
    """
    .. note:: This is not actually an accessor
    """

    accessor: DriverAccessor
    out_queues: Dict[str, List[Queue]]

    def __init__(self, accessor: DriverAccessor) -> None:
        self.out_queues = {}
        self.accessor = accessor

    def submit(self, sys: System, out_fn: Callable) -> None:
        if sys in self.out_queues:
            self.out_queues[sys].append(out_fn)
        else:
            self.out_queues[sys] = [out_fn]
            self.accessor.submit(sys)  # Deduplication handled at DriverAccessor layer

    def gather_completed(self):
        for sys, rec in self.accessor.get_completed():
            out_qs = self.out_queues.pop(sys)
            for out in out_qs:
                out.put((sys, rec))

    def get_client(self) -> "DispatcherClient":
        return DispatcherClient(self)


class DispatcherClient(Accessor[System, Tuple[System, SystemRecord]]):
    driver: Driver
    dispatcher: Dispatcher

    def __init__(self, dispatcher: Dispatcher) -> None:
        super().__init__()
        self.dispatcher = dispatcher
        self.driver = dispatcher.accessor.driver

    def submit(self, sys: System) -> None:
        self.num_submitted += 1
        self.dispatcher.submit(sys, self.out_queue)

    def get_completed(self) -> List[Tuple[System, SystemRecord]]:
        self.dispatcher.gather_completed()
        return super().get_completed()

    def churn(self) -> None:
        self.dispatcher.accessor.churn()

    @property
    def total_active(self):
        return self.dispatcher.accessor.num_active


ACCESSOR_CACHE: Dict[Tuple[UUID, bool, bool, bool, bool], Dispatcher] = {}


def clear_accessor_cache():
    global ACCESSOR_CACHE
    ACCESSOR_CACHE.clear()


def get_accessor(
    driver: Driver,
    use_cache=None,
    run_calculatons=None,
    use_database=None,
    use_ray=None,
) -> DispatcherClient:
    global ACCESSOR_CACHE

    if use_ray is None:
        use_ray = ray.is_initialized()
    if use_cache is None:
        use_cache = driver.opts.use_cache
    if use_database is None:
        use_database = driver.opts.use_database
    if run_calculatons is None:
        run_calculatons = driver.opts.run_calculations
    k = (driver.id, use_cache, run_calculatons, use_database, use_ray)

    if k not in ACCESSOR_CACHE:
        accessor = DriverAccessor.get_accessor(
            driver,
            use_cache=use_cache,
            use_database=use_database,
            run_calculators=run_calculatons,
            use_ray=use_ray,
        )
        ACCESSOR_CACHE[k] = Dispatcher(accessor)

    return ACCESSOR_CACHE[k].get_client()
