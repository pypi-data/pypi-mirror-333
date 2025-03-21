#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import time
from datetime import datetime
from functools import partial
from typing import Callable, Literal, Optional, Union

from conformer_core.properties.extraction import calc_property
from pydantic import BaseModel, Field

from atomdriver.abstract_driver import Driver, DriverOptions, RunContext
from atomdriver.exceptions import SCFConvergenceError

try:
    # Conditional import just in case
    import pyscf
except ImportError:
    pyscf = None

# Configure Logging because PySCF just won't stop emitting UserWarnings
import logging

logging.captureWarnings(True)


# Supported Methods
class ProcedureOptions(BaseModel):
    method: str
    basis: str
    conv_tol: float = 1e-9
    direct_scf_tol: float = 1e-14
    driver: Optional[str] = None
    use_newton: bool = False


# Hartree Fock Procedure
class HFOptions(ProcedureOptions):
    method: Literal["hf", "HF"] = "HF"
    driver: str = "HF"


def HF(mol, args: HFOptions):
    from pyscf import scf

    driver = scf.HF if args.driver is None else getattr(scf, args.driver)
    scf = driver(mol)
    if args.use_newton:
        scf = scf.newton()
    scf.run(conv_tol=args.conv_tol, direct_scf_tol=args.direct_scf_tol)

    if not scf.converged:
        raise SCFConvergenceError("HF SCF procedure didn't converge")
    return scf, dict(
        total_energy=scf.e_tot,
        total_scf_energy=scf.e_tot,
        one_electron_int=scf.scf_summary["e1"],
        two_electron_int=scf.scf_summary["e2"],
        nuclear_repulsion=scf.scf_summary["nuc"],
    )


# DFT Procedure
class KSOptions(ProcedureOptions):
    method: Literal["ks", "KS", "dft", "DFT"]
    xc: str
    driver: str = "KS"


def KS(mol, args: KSOptions):
    from pyscf import dft

    driver = dft.KS if args.driver is None else getattr(dft, args.driver)
    scf = driver(mol)
    if args.use_newton:
        scf = scf.newton()
    scf.xc = args.xc
    scf.run(conv_tol=args.conv_tol, direct_scf_tol=args.direct_scf_tol)

    if not scf.converged:
        raise SCFConvergenceError("KS SCF procedure didn't converge")

    return scf, dict(
        total_energy=scf.e_tot,
        total_scf_energy=scf.e_tot,
        one_electron_int=scf.scf_summary["e1"],
        dft_exchange=scf.scf_summary["exc"],
        total_coulomb_energy=scf.scf_summary["coul"],
        nuclear_repulsion=scf.scf_summary["nuc"],
    )


# MP2 Procedure
class MP2Options(HFOptions):
    method: Literal["mp2", "MP2"]
    mp2_driver: str = "MP2"
    driver: str = "HF"


def MP2(mol, args: MP2Options):
    from pyscf import mp

    scf, results = HF(mol, args)
    mp2_driver = mp.MP2 if args.driver is None else getattr(mp, args.mp2_driver)
    mp2 = mp2_driver(scf)
    mp2.conv_tol = args.conv_tol
    # mp2.direct_scf_tol = args.direct_scf_tol
    mp2.run()

    results.update(total_energy=mp2.e_tot, total_correlation_energy=mp2.e_corr)
    return (mp2, results)


# RIMP2/DFMP2 Procedures
class DFMP2Options(MP2Options):
    method: Literal["dfmp2", "DFMP2", "rimp2", "RIMP2"]
    auxbasis: Optional[str] = None
    driver: str = "HF"


def DFMP2(mol, args: DFMP2Options):
    from pyscf.mp import dfmp2_native

    scf, results = HF(mol, args)
    dfmp2_driver = (
        dfmp2_native.DFMP2
        if args.driver is None
        else getattr(dfmp2_native, args.mp2_driver)
    )

    if args.auxbasis:
        dfmp2 = dfmp2_driver(scf)
    else:
        dfmp2 = dfmp2_driver(scf, auxbasis=args.auxbasis)

    dfmp2.conv_tol = args.conv_tol
    dfmp2.direct_scf_tol = args.direct_scf_tol
    dfmp2.run()

    results.update(total_energy=dfmp2.e_tot, total_correlation_energy=dfmp2.e_corr)
    return (dfmp2, results)


# CCSD Procedure
class CCSDOptions(HFOptions):
    method: Literal["ccsd", "CCSD"]
    driver: str = "HF"


def CCSD(mol, args: CCSDOptions):
    from pyscf import cc

    scf, results = HF(mol, args)
    ccsd = cc.CCSD(scf)
    ccsd.run(conv_tol=args.conv_tol)
    results.update(
        total_energy=ccsd.e_tot,
        total_correlation_energy=ccsd.e_corr,
        CCSD_correlation=ccsd.e_corr,
        MP2_correlation=ccsd.emp2,
    )
    return (ccsd, results)


# CCSD(T) Procedure
class CCSD_TOptions(CCSDOptions):
    method: Literal["ccsd(t)", "CCSD(T)", "ccsd_t", "CCSD_T"]
    driver: str = "HF"


def CCSD_T(mol, args: CCSD_TOptions):
    ccsd, results = CCSD(mol, args)
    et = ccsd.ccsd_t()

    results["total_energy"] += et
    results["total_correlation_energy"] += et
    results["CC_T_correlation"] = et
    return (ccsd, results)


PROCEDURES = {
    "HF": HF,
    "KS": KS,
    "DFT": KS,
    "MP2": MP2,
    "DFMP2": DFMP2,
    "RIMP2": DFMP2,
    "CCSD": CCSD,
    "CCSD(T)": CCSD_T,
}

PROC_LIST = Union[
    HFOptions, KSOptions, MP2Options, DFMP2Options, CCSDOptions, CCSD_TOptions
]


class PySCF(Driver):
    class Options(DriverOptions):
        procedure: PROC_LIST = Field(default_factory=HFOptions)
        verbose: int = 0

    procedure_args: ProcedureOptions
    procedure: Callable

    @classmethod
    def is_available(cls) -> bool:
        return pyscf is not None

    def setup_calc(self, ctx: RunContext):
        super().setup_calc(ctx)

        sys = ctx.record.system
        physical = [(a.t, a.r) for a in sys if a.is_physical]
        ghost = [("ghost:" + a.t, a.r) for a in sys if a.has_basis_fns]
        ctx.scratch["mol"] = pyscf.M(
            atom=physical + ghost,
            basis=self.procedure_args.basis,
            charge=sys.charge,
            spin=(sys.multiplicity - 1),
            unit="AU",
            symmetry=False,
            verbose=self.opts.verbose,
            max_memory=self.allocation.memory,
        )

    def _run_calc(self, ctx: RunContext) -> None:
        ctx.record.start_time = datetime.now()
        cpu0 = time.process_time()
        _, res = self.procedure(ctx.scratch["mol"])
        ctx.scratch["cpu_time"] = time.process_time() - cpu0
        ctx.record.end_time = datetime.now()
        ctx.scratch.update(**res)

    def run_calc(self, ctx: RunContext) -> None:
        cpus = self.allocation.cpus
        if cpus == 1:
            self._run_calc(ctx)
        else:
            with pyscf.lib.misc.with_omp_threads(cpus):
                self._run_calc(ctx)

    def configure(self) -> None:
        super().configure()
        self.procedure_args = self.opts.procedure
        self.procedure = partial(
            PROCEDURES[self.procedure_args.method.upper()],
            args=self.procedure_args,
        )

    def cleanup(self) -> None:
        self.procedure_args = None
        self.procedure = None
        super().cleanup()

    @calc_property(source="context")
    def prop_cpu_time(self, ctx: RunContext):
        return ctx.scratch.get("cpu_time", None)

    @calc_property(source="context")
    def prop_total_energy(self, ctx: RunContext):
        return ctx.scratch.get("total_energy", None)

    @calc_property(source="context")
    def prop_total_scf_energy(self, ctx: RunContext):
        return ctx.scratch.get("total_scf_energy", None)

    @calc_property(source="context")
    def prop_CCSD_correlation(self, ctx: RunContext):
        return ctx.scratch.get("CCSD_correlation", None)

    @calc_property(source="context")
    def prop_CC_T_correlation(self, ctx: RunContext):
        return ctx.scratch.get("CC_T_correlation", None)

    @calc_property(source="context")
    def prop_MP2_correlation(self, ctx: RunContext):
        return ctx.scratch.get("MP2_correlation", None)

    @calc_property(source="context")
    def prop_total_correlation_energy(self, ctx: RunContext):
        return ctx.scratch.get("total_correlation_energy", None)

    @calc_property(source="context")
    def prop_one_electron_int(self, ctx: RunContext):
        return ctx.scratch.get("one_electron_int", None)

    @calc_property(source="context")
    def prop_two_electron_int(self, ctx: RunContext):
        return ctx.scratch.get("two_electron_int", None)

    @calc_property(source="context")
    def prop_dft_exchange(self, ctx: RunContext):
        return ctx.scratch.get("dft_exchange", None)

    @calc_property(source="context")
    def prop_total_coulomb_energy(self, ctx: RunContext):
        return ctx.scratch.get("total_coulomb_energy", None)

    @calc_property(source="context")
    def prop_nuclear_repulsion(self, ctx: RunContext):
        # Returns an integer for lone atoms so must be cast to float
        return float(ctx.scratch.get("nuclear_repulsion", None))
