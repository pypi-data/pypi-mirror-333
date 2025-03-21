#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import importlib
import time
from datetime import datetime
from os import environ
from types import ModuleType
from typing import Optional, Tuple

from conformer.records import RecordStatus
from conformer_core.properties.extraction import calc_property
from qcelemental import constants

from atomdriver.abstract_driver import Driver, DriverOptions, RunContext
from atomdriver.exceptions import BackendRunException, ConfigurationError

CONFIGURED = False
XTB_INTERFACE = None
XTB_LIB = None
XTB_THREADS = None


def load_xtb(cores: int) -> Tuple[ModuleType, ModuleType]:
    """
    Sets the relevent evirnment variables and loads xTB

    ..node:: Once loaded, the number of cores used by xtb cannot be changed
        even if we reload the module :(
    """
    global CONFIGURED
    global XTB_INTERFACE
    global XTB_LIB
    global XTB_THREADS

    if XTB_THREADS is not None and cores != XTB_THREADS:
        raise ConfigurationError(
            f"libxtb loaded with different number of cores ({cores} != {XTB_THREADS})!"
        )

    if not CONFIGURED:
        XTB_THREADS = cores
        environ["OMP_NUM_THREADS"] = str(XTB_THREADS) + ",1"
        environ["MKL_NUM_THREADS"] = str(XTB_THREADS)

        import xtb.interface as interface
        import xtb.libxtb as libxtb

        XTB_INTERFACE = interface
        XTB_LIB = libxtb
    return XTB_INTERFACE, XTB_LIB


class LibxTB(Driver):
    class Options(DriverOptions):
        method: str = "gfn2"
        accuracy: float = 0.01
        max_scf: int = 0
        save_output: bool = False
        calc_charges: bool = False
        calc_gradient: bool = False
        solvent: Optional[str] = None
        batch_size: int = 200

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._interface = None
        self._libxtb = None
        self._method = None
        self._solvent = None

    @classmethod
    def is_available(cls) -> bool:
        return importlib.util.find_spec("xtb") is not None

    def configure(self) -> None:
        super().configure()
        interface, libxtb = load_xtb(self.allocation.cpus)
        self._interface = interface
        self._libxtb = libxtb
        methods = {
            "gfn2": interface.Param.GFN2xTB,
            "gfn1": interface.Param.GFN1xTB,
            "gfn0": interface.Param.GFN0xTB,
            "ipea": interface.Param.IPEAxTB,
            "gfnff": interface.Param.GFNFF,
        }
        self._method = methods[self.opts.method.lower()]
        if self.opts.solvent:
            from xtb.utils import get_solvent

            self._solvent = get_solvent(self.opts.solvent)
        else:
            self._solvent = None

    def setup_calc(self, ctx: RunContext):
        super().setup_calc(ctx)
        if not self.is_configured:
            raise ConfigurationError(
                f"{self.__class__.__name__} backend is not configured!"
            )
        interface = self._interface
        libxtb = self._libxtb

        calc = interface.Calculator(
            self._method,
            ctx.record.system.Z_matrix,
            ctx.record.system.r_matrix / constants.bohr2angstroms,
            charge=ctx.record.system.charge,
        )
        calc.set_accuracy(self.opts.accuracy)
        calc.set_verbosity(libxtb.VERBOSITY_MUTED)
        # TODO: Setup external charges
        if self.opts.max_scf:
            calc.set_max_iterations(self.opts.max_scf)

        if self._solvent:
            calc.set_solvent(self._solvent)
        ctx.scratch["calculator"] = calc

    def cleanup(self):
        # Reset xtb-library settings
        self._interface = None
        self._libxtb = None
        self._method = None
        self._solvent = None
        return super().cleanup()

    def run_calc(self, ctx: RunContext):
        ctx.record.start_time = datetime.now()
        cpu0 = time.process_time()
        try:
            ctx.scratch["result"] = ctx.scratch["calculator"].singlepoint()
        except self._interface.XTBException as e:
            ctx.record.status = RecordStatus.FAILED
            ctx.record.meta["error"] = str(e)
            ctx.scratch["result"] = None
        ctx.scratch["cpu_time"] = time.process_time() - cpu0
        ctx.record.end_time = datetime.now()

    def determine_success(self, ctx: RunContext):
        if ctx.scratch["result"] is None:
            raise BackendRunException()

    @calc_property(source="context")
    def prop_total_energy(self, ctx: RunContext):
        res = ctx.scratch.get("result", None)
        if res:
            return res.get_energy()

    @calc_property(source="context")
    def prop_partial_charges(self, ctx: RunContext):
        if not self.opts.calc_charges:
            return
        res = ctx.scratch.get("result", None)
        if res:
            charges = res.get_charges()
            return charges.reshape(-1, 1)

    @calc_property(source="context")
    def prop_nuclear_gradient(self, ctx: RunContext):
        if not self.opts.calc_gradient:
            return
        res = ctx.scratch.get("result", None)
        if res:
            grad = res.get_gradient()
            return grad

    @calc_property(source="context")
    def prop_cpu_time(self, ctx: RunContext):
        return ctx.scratch.get("cpu_time", None)
