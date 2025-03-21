#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import subprocess
from typing import List, Tuple

import qcelemental as qcel
from conformer_core.properties.extraction import calc_property

from atomdriver.abstract_driver import RunContext, ShellCommandDriver

DEFAULT_TEMPLATE = """\
PM7 XYZ PRECISE NOSYM NOREOR GEO-OK


{geometry}
"""

class MOPAC(ShellCommandDriver):
    class Options(ShellCommandDriver.Options):
        exe: str = "mopac"
        template: str = DEFAULT_TEMPLATE

    ATOM_TEMPLATE = "{symbol}    {x} {y} {z}"
    GHOST_ATOM_TEMPLATE = None

    STDOUT_FILE = "output"
    FILE_MANIFEST = {"input": "molecule.mop", "output": "molecule.out"}

    @classmethod
    def is_available(cls):
        try:
            return (
                subprocess.run(
                    "mopac",
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    input=b"\n",
                ).returncode
                == 0
            )
        except FileNotFoundError:
            return False

    def get_run_cmd(self, ctx: RunContext) -> Tuple[str, List[str]]:
        return self.opts.exe, [ctx.files["input"]]

    @calc_property(source="re_file", patterns=[
        r"TOTAL ENERGY\s+=\s+(-?\d+\.\d+)\sEV",
        r"FINAL HEAT OF FORMATION = .*=\s+(-?\d+\.\d+)\sKJ/MOL"
    ])
    def prop_total_energy(self, ctx, m, _):
        """It's unclear what should be done here"""
        if m[0].endswith("EV"):
            return float(m[1]) / qcel.constants.hartree2ev
        if m[0].endswith("KJ/MOL"):
            return float(m[1]) / qcel.constants.hartree2kJmol

    @calc_property(
        source="re_file", patterns=[r"COMPUTATION TIME\s+=\s+(-?\d+\.\d+)\sSECONDS"]
    )
    def prop_cpu_time(self, ctx, m, _):
        return float(m[1])
