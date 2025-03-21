#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import os
from typing import Any, Dict, List, Tuple

from conformer_core.properties.extraction import calc_property
from conformer_core.records import RecordStatus
from pydantic import Field

from atomdriver.abstract_driver import (
    RunContext,
    ShellCommandMixin,
)


class GAMESSOptions(ShellCommandMixin.Options, extra='allow'):
    # Data will be added by the Driver
    # CONTRL will have ICHARG and MULT added by the Driver
    # Default basis 6-31G
    exe: str = "rungms"
    cpus: int = 1
    basis: Dict["str", Any] = Field(default={"GBASIS": "N31", "NGAUSS": 6})


class GAMESS(ShellCommandMixin):
    Options = GAMESSOptions
    opts: GAMESSOptions

    FILE_MANIFEST = {"input": ".inp", "output": ".out"}
    STDOUT_FILE: str = "output"
    STDERR_FILE: str = "output"

    @classmethod
    def is_available(cls):
        if "GAMESSHOME" in os.environ and os.path.exists(os.environ["GAMESSHOME"]):
            return True
        return False

    def get_run_cmd(self, ctx: RunContext) -> Tuple[str, List[str]]:
        return (
            self.opts.exe,
            [str(ctx.files["input"].name)],
        )  # This does not support multip-cpu GAMESS. I don't think the OSC version has that enabled

    def setup_calc(self, ctx: RunContext):
        # Skip the parent constructor
        super().setup_calc(ctx)
        # Driver.setup_calc(
        #     self, ctx
        # )  # TODO: This usecase might justify some refactoring for shell drivers in gernal
        opts: Dict[str, Any] = self.opts.model_dump().copy()

        # Pop unused values
        for n in ShellCommandMixin.Options.model_fields.keys():
            opts.pop(n)

        # Uppercase all key names:
        opts = {k.upper(): v for k, v in opts.items()}

        if "CONTRL" not in opts:
            opts["CONTRL"] = {}
        opts["CONTRL"]["ICHARG"] = ctx.working_system.charge
        opts["CONTRL"]["MULT"] = ctx.working_system.multiplicity

        DATA = [
            f"SYSTEM: {ctx.working_system.name}",
            "C1",
        ]  # disable symmetry
        for a in ctx.working_system:
            if a.is_physical:
                DATA.append("{}  {} {: .9f} {: .9f} {: .9f}".format(a.t, a.Z, *a.r))
            elif a.has_basis_fns:
                DATA.append("{} -{} {: .9f} {: .9f} {: .9f}".format(a.t, a.Z, *a.r))

            # TODO: Point charges?
        opts["DATA"] = DATA

        with ctx.files["input"].open("w") as f:
            _keys = sorted(opts.keys())
            for k in _keys:
                v = opts[k]
                print(" $" + k, file=f)
                if isinstance(v, dict):
                    for i, j in v.items():
                        print(f"    {i}={j}", file=f)
                elif isinstance(v, list):
                    for i in v:
                        print("    " + str(i), file=f)
                else:
                    print(v, file=f)
                print(" $END\n", file=f)

        # Get the run command
        ctx.scratch["_TMPDIR"] = os.environ.get("TMPDIR", None)
        os.environ["TMPDIR"] = str(ctx.workpath)  # TODO: Do this with Popen(envron=...)
        ctx.scratch["run_cmd"], ctx.scratch["run_args"] = self.get_run_cmd(ctx)

    def cleanup_calc(self, ctx: RunContext):
        super().cleanup_calc(ctx)

        # Restore the environment
        tmpdir = ctx.scratch.get("_TMPDIR", None)
        if tmpdir is not None:
            os.environ["TMPDIR"] = tmpdir
        return

    @calc_property(source="re_file", patterns=[r"TOTAL ENERGY = +(-?\d+.\d+)"])
    def prop_total_energy(self, ctx, m, _):
        return float(m[1])

    @calc_property(
        source="re_file",
        patterns=[r"ONE ELECTRON ENERGY = +(-?\d+.\d+)"],
    )
    def prop_one_electron_int(self, ctx: RunContext, m, _):
        return float(m[1])

    @calc_property(
        source="re_file",
        patterns=[r"TWO ELECTRON ENERGY = +(-?\d+.\d+)"],
    )
    def prop_hf_exchange(self, ctx: RunContext, m, _):
        return float(m[1])

    @calc_property(
        source="re_file",
        patterns=[r"TOTAL POTENTIAL ENERGY = +(-?\d+.\d+)"],
    )
    def prop_total_coulomb_energy(self, ctx: RunContext, m, _):
        return float(m[1])

    @calc_property(
        source="re_file",
        patterns=[r"TOTAL KINETIC ENERGY = +(-?\d+.\d+)"],
    )
    def prop_kinetic_energy(self, ctx: RunContext, m, _):
        return float(m[1])

    @calc_property(
        source="re_file",
        patterns=[r"NUCLEUS-NUCLEUS POTENTIAL ENERGY = +(-?\d+.\d+)"],
    )
    def prop_nuclear_repulsion(self, ctx: RunContext, m, _):
        return float(m[1])

    @calc_property(
        source="re_file", patterns=[r"NUCLEUS-ELECTRON POTENTIAL ENERGY = +(-?\d+.\d+)"]
    )
    def prop_nuclear_attraction(self, ctx: RunContext, m, _):
        return float(m[1])

    @calc_property(source="re_file", patterns=[r"\*+ ERROR"])
    def error(self, ctx: RunContext, m, stream):
        ctx.record.status = RecordStatus.FAILED
        ctx.record.meta["error"] = m.string + "\n" + stream.read()
