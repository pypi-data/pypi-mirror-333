#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import subprocess
from typing import List, Tuple

from conformer_core.properties.extraction import calc_property

from atomdriver.abstract_driver import RunContext, ShellCommandDriver

DEFAULT_TEMPLATE = """\
# Name: {name}
! B3LYP SP 6-31G

*xyz {charge} {mult}
{geometry}
*
"""

class ORCA(ShellCommandDriver):
    class Options(ShellCommandDriver.Options):
        exe: str = "orca"
        template: str = DEFAULT_TEMPLATE

    ATOM_TEMPLATE = "{symbol}    {x} {y} {z}"
    GHOST_ATOM_TEMPLATE = "{symbol}:    {x} {y} {z}"
    STDOUT_FILE = "output"

    @classmethod
    def is_available(cls):
        # Don't simply run the ORCA command. We need to
        # discriminate between the QM code and the screen reader
        try:
            return (
                subprocess.run(
                    ["orca", "file_does_not_exits"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                ).returncode
                == 2
            )
        except FileNotFoundError:
            return False

    def get_run_cmd(self, ctx: RunContext) -> Tuple[str, List[str]]:
        return self.opts.exe, [str(ctx.files["input"])]

    @calc_property(
        source="re_file", patterns=[r"Total [eE]nergy\s*:\s+(-?\d+.\d+)\s*Eh"]
    )
    def prop_total_energy(self, ctx, m, _):
        return float(m[1])

    # Properties from frequency calcualtions
    @calc_property(
        source="re_file", patterns=[r"Total [eE]nthalpy\s+\.\.\.\s+(-?\d+.\d+)\s*Eh"]
    )
    def prop_total_enthalpy(self, ctx, m, _):
        return float(m[1])

    @calc_property(
        source="re_file", patterns=[r"Final entropy term \s+\.\.\.\s+(-?\d+.\d+)\s*Eh"]
    )
    def prop_total_entropy(self, ctx, m, _):
        return float(m[1])

    @calc_property(
        source="re_file",
        patterns=[r"Final Gibbs free energy \s+\.\.\.\s+(-?\d+.\d+)\s*Eh"],
    )
    def prop_total_gibbs(self, ctx, m, _):
        return float(m[1])

    @calc_property(
        source="re_file",
        patterns=[
            r"TOTAL RUN TIME: (\d+) days (\d+) hours (\d+) minutes (\d+) seconds (\d+) msec"
        ],
    )
    def prop_cpu_time(self, ctx, m, _):
        times = [
            float(m[1]) * 86400,
            float(m[2]) * 3600,
            float(m[3]) * 60,
            float(m[4]),
            float(m[5]) / 1000,
        ]
        return sum(times)
