#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import re
from os import environ, path
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
from conformer_core.properties.extraction import calc_property
from conformer_core.records import RecordStatus
from pydantic import Field

from atomdriver.abstract_driver import RunContext, ShellCommandDriver

# Feature search expressions
METHOD_SEARCH_RE = r"^\s*method[ \t]*=?[ \t]*([^\s]*)"  # Cannot pre-compile
BASIS_SEARCH_RE = r"^\s*basis[ \t]*=?[ \t]*([^\s]*)"  # Cannot pre-compile
JOB_TYPE_RE = r"^\s*job_type[ \t]*=?[ \t]*([^\s]*)"  # Cannot pre-compile
HARM_OPT_SEARCH_RE = r"^\s*harm_opt[ \t=]+(true|1)"
FROZEN_OPT_SEARCH_RE = r"^\s*frzn_opt[ \t=]+(true|1)"

# Regex's for searching for the final energy
ENERGY_EXPRESSIONS = {
    "mp2": re.compile(r"MP2[ \t]+[tT]otal [eE]nergy =[ \t]+(-?\d+.\d+)"),
    "rimp2": re.compile(r"RIMP2[ \t]+[tT]otal [eE]nergy =[ \t]+(-?\d+.\d+)"),
    "ccsd": re.compile(r"CCSD [tT]otal [eE]nergy[ \t]+=[ \t]+(-?\d+.\d+)"),
    "ccsd(t)": re.compile(r"CCSD\(T\) [tT]otal [eE]nergy[ \t]+=[ \t]+(-?\d+.\d+)"),
    "default": re.compile(
        r"Total energy (?:in the final basis set )?=[ \t]+(-?\d+.\d+)"
    ),
}
CORRELATION_EXPRESSION = {
    "mp2": re.compile(r"MP2[ \t]+correlation energy =[ \t]+(-?\d+.\d+)"),
    "rimp2": re.compile(r"RIMP2[ \t]+correlation energy =[ \t]+(-?\d+.\d+)"),
    "ccsd": re.compile(r"CCSD correlation energy[ \t]+=[ \t]+(-?\d+.\d+)"),
    "ccsd(t)": re.compile(r"CCSD\(T\) correlation energy[ \t]+=[ \t]+(-?\d+.\d+)"),
}
DEFAULT_ENERGY_EXPRESSION = ENERGY_EXPRESSIONS["default"]
ZERO = 1e-9

# List of available scratch files. See fileman.h in the Q-Chem source for more
DATA_FILES = {
    "DENSITY_BASIS": 47,
    "MO_COEFS": 53,
    "DENSITY_MATRIX": 54,
    "FOCK_MATRIX": 58,
    "NUCLEAR_GRADIENT": 131,
    "NUCLEAR_HESSIAN": 132,
}

# Default template. User should be advised to update this.
DEFAULT_TEMPLATE = """\
! Name: {name}
$molecule
{charge} {mult}
{geometry}
$end

$rem
    basis           {basis}
    method          {method}
    job_type        {job_type}
    thresh          14
    scf_convergence 8
    sym_ignore      true

    mem_total       {total_memory}
    mem_static      {static_memory}

    ! User provided rems:
    {rem_extra}
$end

! Extra input sections
{input_extra}
"""


class QChem(ShellCommandDriver):
    class Options(ShellCommandDriver.Options):
        exe: str = "qchem"
        template: str = DEFAULT_TEMPLATE

        # Quick reference options
        basis: str = "6-31G"
        method: str = "HF"
        job_type: str = "SP"
        rem_extra: Dict[str, Any] = Field(default_factory=dict)
        input_extra: str = ""

        # Enable the expirmental version
        _qcprog_direct: bool = True

    opts: Options

    # Working variables
    use_pinned_atoms: bool
    rem_extra: str

    @classmethod
    def is_available(cls):
        QC = environ.get("QC", None)
        QCAUX = environ.get("QCAUX", None)
        if not (QC and path.exists(QC)):
            return False
        if not (QCAUX and path.exists(QCAUX)):
            return False
        return True

    def __init_stage__(self):
        super().__init_stage__()

        # Direct program writes to stdout
        if self.opts._qcprog_direct:
            self.STDOUT_FILE = "output"

        # The template might contain formation about the method and basis
        # so let's scrape that and save for latter
        # Doing this in __init_stage__ instead of configure to make sure this is
        # save to the database
        template = self.opts.template.lower()

        # Method search
        m = re.search(METHOD_SEARCH_RE, template, re.MULTILINE)
        if m and m[1] != "{method}":
            self.opts.method = m[1]
        self.set_energy_regex(self.opts.method)

        # Basis search
        m = re.search(BASIS_SEARCH_RE, template, re.MULTILINE)
        if m and m[1] != "{basis}":
            self.opts.basis = m[1]

        # Job type search
        m = re.search(JOB_TYPE_RE, template, re.MULTILINE)
        if m and m[1] != "{job_type}":
            self.opts.job_type = m[1]

        # Check for harmonic confiner
        self.use_pinned_atoms = False
        m = re.search(HARM_OPT_SEARCH_RE, template, re.MULTILINE)
        if m:
            self.use_pinned_atoms = True

        # Check for frozen atoms
        m = re.search(FROZEN_OPT_SEARCH_RE, template, re.MULTILINE)
        if m:
            self.use_pinned_atoms = True

        # While we are here, compile the rem_extra extra section
        self.rem_extra = "\n    ".join(
            (a + "    " + str(b) for a, b in self.opts.rem_extra.items())
        )

    def set_energy_regex(self, method: str):
        """Q-Chem used different strings for reporting energy
        depending on the method. This method chooses the correct RE
        """
        method = method.lower()
        self.prop_total_energy.patterns = [
            ENERGY_EXPRESSIONS.get(method, DEFAULT_ENERGY_EXPRESSION)
        ]
        if method in CORRELATION_EXPRESSION:
            self.prop_total_correlation_energy.patterns = [
                CORRELATION_EXPRESSION[method]
            ]

    def get_run_cmd(self, ctx: RunContext) -> Tuple[str, List[str]]:
        if self.opts._qcprog_direct:
            QC = Path(self.allocation.environ["QC"])
            QCPROG = QC / "exe" / "qcprog.exe"
            assert QCPROG.exists()
            return QCPROG, [ctx.files['input'], ctx.workpath / "scratch"]

        return self.opts.exe, [
            "-nt",
            str(self.allocation.cpus),
            "-save",  # The driver will clean up the scratch files
            ctx.files["input"],
            ctx.files["output"],
            "scratch",  # Save datafiles to scratch
        ]


    def get_template_tags(self, ctx: RunContext) -> Dict[str, str]:
        tags = super().get_template_tags(ctx)

        # Update standard q-chem tags
        tags.update(
            static_memory=min([int(self.allocation.memory * 0.20), 2000]),
            method=self.opts.method,
            basis=self.opts.basis,
            job_type=self.opts.job_type,
            rem_extra=self.rem_extra,  # The pre-compiled version
            input_extra=self.opts.input_extra,
        )

        # Harmonic confiner stuff here
        if self.use_pinned_atoms:
            p_num, p_idx, p_coords = self.pinned_atoms(ctx.record.system)
            tags.update(
                pinned_num=p_num,
                pinned_idxs=p_idx,
                pinned_coords=p_coords,
            )
        return tags

    def get_run_env(self, ctx: RunContext) -> Dict[str, str]:
        """Changes the location of QCSCRATCH to the working directory.
        This choice assumes that the temporary directory will not be on
        a network drive
        """
        env = super().get_run_env(ctx)

        if self.opts._qcprog_direct:
            # Looks like we are running qcprog.exe directly
            scratch = ctx.workpath / "scratch" 
            scratch.mkdir()

            env.update(
                QCSCRATCH=str(scratch),
                QCOUTFILE=str(ctx.files["output"]),
                GFORTRAN_UNBUFFERED_PRECONNECTED="y",
                QCTHREADS=str(self.allocation.cpus),
                OMP_NUM_THREADS=str(self.allocation.cpus),
                MKL_NUM_THREADS="1",
                KMP_NUM_THREADS="1",
                OPENBLAS_NUM_THREADS="1",
                HDF5_USE_FILE_LOCKING="FALSE",
            )
            return env

        env["QCSCRATCH"] = str(ctx.workpath)
        return env

    @staticmethod
    def pinned_atoms(sys) -> Tuple[int, str, str]:
        """Returns information needed to use frozen or harmonically confined atoms

        Use this with a input sections like

            $rem
            ...
            hoatoms {pinned_num}
            ...
            $end

            $harmonic_opt
                {pinned_atoms} ! indices of the confined atoms
            $end

            $coords !coordinates of confined atoms
                {pinned_coords}
            $end

        Returns:
            number of pinned atoms, space delimited list atom idx, coords
        """
        num_pinned = 0
        idxs = []
        coords = []
        for i, a in enumerate(sys, 1):
            if a.role.is_pinned:
                num_pinned += 1
                idxs.append(str(i))
                coords.append("{:n} {:.8f} {:.8f} {:.8f}".format(i, *a.r))
        return num_pinned, " ".join(idxs), "\n".join(coords)

    def read_scratch_file(
        self, ctx: RunContext, file: str | int, dims: Tuple[int, ...], dtype="float64"
    ) -> np.ndarray:
        """Reads a Q-Chem scratch file (see fileman.h for available files)"""
        if isinstance(file, str):
            filenum = DATA_FILES[file]
        else:
            filenum = file

        # This might not work for multi-part files. Do we support this?
        scratch_path = ctx.workpath / "scratch" / (str(filenum) + ".0")
        return np.fromfile(scratch_path, dtype=dtype).reshape(dims)

    @calc_property(source="re_file")  # Patterns configured at runtime
    def prop_total_energy(self, ctx: RunContext, m, _):
        return float(m[1])

    @calc_property(
        source="re_file", patterns=[r"Total [eE]nthalpy\s*:\s+(-?\d+.\d+)\s*"]
    )
    def prop_total_enthalpy(self, ctx: RunContext, m, _):
        """
        Properties from frequency calcualtions
        Enthalphy reported in kcal/mol
        """
        return float(m[1])

    @calc_property(
        source="re_file",
        patterns=[r"SCF +energy in the final basis set = +(-?\d+.\d+)"],
    )
    def prop_total_scf_energy(self, ctx: RunContext, m, _):
        return float(m[1])

    @calc_property(
        source="re_file",
        patterns=[r"DFT +Exchange +Energy = +(-?\d+.\d+)"],
    )
    def prop_dft_exchange(self, ctx: RunContext, m, _):
        res = float(m[1])
        if abs(res) > ZERO:
            return res

    @calc_property(
        source="re_file",
        patterns=[r"DFT +Correlation +Energy = +(-?\d+.\d+)"],
    )
    def prop_dft_correlation(self, ctx: RunContext, m, _):
        res = float(m[1])
        if abs(res) > ZERO:
            return res

    @calc_property(
        source="re_file",
        patterns=[r"Total +Coulomb +Energy = +(-?\d+.\d+)"],
    )
    def prop_total_coulomb_energy(self, ctx: RunContext, m, _):
        res = float(m[1])
        if abs(res) > ZERO:
            return res

    @calc_property(
        source="re_file",
        patterns=[
            r"HF +Exchange +Energy = +(-?\d+.\d+)",
            r"Alpha +Exchange +Energy = +(-?\d+.\d+)",
        ],
    )
    def prop_hf_exchange(self, ctx: RunContext, m, stream):
        if m[0].startswith("HF"):
            return float(m[1])
        if m[0].startswith("Alph"):
            alpha = float(m[1])
            beta_str = stream.readline()
            m2 = re.match(r" Beta +Exchange +Energy = +(-?\d+.\d+)", beta_str)
            if m2:
                return alpha + float(m2[1])

    @calc_property(source="re_file")
    def prop_total_correlation_energy(self, ctx: RunContext, m, _):
        return float(m[1])

    @calc_property(
        source="re_file",
        patterns=[r"Kinetic + Energy = +(-?\d+.\d+)"],
    )
    def prop_kinetic_energy(self, ctx: RunContext, m, _):
        res = float(m[1])
        if abs(res) > ZERO:
            return res

    @calc_property(
        source="re_file",
        patterns=[r"Nuclear Repulsion Energy = +(-?\d+.\d+)"],
    )
    def prop_nuclear_repulsion(self, ctx: RunContext, m, _):
        return float(m[1])

    @calc_property(
        source="re_file", patterns=[r"Nuclear Attr(actions|\.) + Energy = +(-?\d+.\d+)"]
    )
    def prop_nuclear_attraction(self, ctx: RunContext, m, _):
        res = float(m[2])
        if abs(res) > ZERO:
            return float(m[2])

    @calc_property(source="ctx")
    def prop_nuclear_gradient(self, ctx: RunContext):
        try:
            return self.read_scratch_file(ctx, "NUCLEAR_GRADIENT", (-1, 3))
        except FileNotFoundError:
            pass

    @calc_property(source="ctx")
    def prop_nuclear_hessian(self, ctx: RunContext):
        na = sum((1 for a in ctx.working_system if a.role.is_physical))
        try:
            return self.read_scratch_file(ctx, "NUCLEAR_HESSIAN", (3 * na, 3 * na))
        except FileNotFoundError:
            pass

    # @calc_property(
    #     source="re_file",
    #     patterns=[r"Gradient of SCF Energy"],
    # )
    # def prop_nuclear_gradient(self, ctx: RunContext, line: re.Match, stream: TextIO):
    #     """Text-base gradient parser. This is depricated and we not parse scratch files"""
    #     # TODO: This will likely be spun off into it's own helper function
    #     atom_map = []
    #     atom_type_map = []
    #     for i, a in enumerate(ctx.record.system):
    #         if a.is_physical:
    #             atom_map.append(i)
    #             if a.is_proxy:
    #                 atom_type_map.append(1)  # Proxies will take back seat
    #             else:
    #                 atom_type_map.append(0)  # Real atom

    #     grad = np.zeros((len(atom_map), 3), dtype=NuclearGradient.type)

    #     # TODO: Do some math to pre-allocate our matrix
    #     uncollected = len(atom_map)
    #     while True:
    #         if uncollected <= 0:  # Break when we are done
    #             break
    #         idxs = [int(i) - 1 for i in stream.readline().split()]
    #         xs = [float(i) for i in stream.readline().split()[1:]]
    #         ys = [float(i) for i in stream.readline().split()[1:]]
    #         zs = [float(i) for i in stream.readline().split()[1:]]

    #         grad[idxs, 0] += xs
    #         grad[idxs, 1] += ys
    #         grad[idxs, 2] += zs

    #         uncollected -= len(idxs)

    #     return grad

    @calc_property(
        source="re_file",
        patterns=[r"One-Electron +Energy = +(-?\d+.\d+)"],
    )
    def prop_one_electron_int(self, ctx: RunContext, m, _):
        return float(m[1])

    @calc_property(
        source="re_file", patterns=[r"Total [eE]ntropy\s*:\s+(-?\d+.\d+)\s*"]
    )
    def prop_total_entropy(self, ctx: RunContext, m, _):
        return float(m[1])

    @calc_property(source="re_file", patterns=[r"(\d+\.\d+)s\(cpu\)"])
    def prop_cpu_time(self, ctx: RunContext, m, _):
        return float(m[1])

    @calc_property(source="re_file", patterns=[r"Q-Chem fatal error occurred *"])
    def error(self, ctx: RunContext, m, stream):
        ctx.record.status = RecordStatus.FAILED
        # Back up. QChem is bad about printing full error
        stream.seek(stream.tell() - 300)
        ctx.record.meta["error"] = "..." + stream.read()

    @calc_property(source="re_file", patterns=[r"[Ww]arning:"])
    def warnings(self, ctx: RunContext, m, _):
        if ctx is None:  # This really only happens in testing
            return None
        warning = m.string.strip()
        try:
            ctx.record.meta["warnings"].append(warning)
        except KeyError:
            ctx.record.meta["warnings"] = [warning]

    @calc_property(
        source="re_file",
        patterns=[r"This [mM]olecule [hH]as\s+(\d+)\s+[iI]maginary [fF]requencies"],
    )
    def prop_num_imaginary_freq(self, ctx: RunContext, m, _):
        return int(m[1])

    @calc_property(
        source="re_file",
        patterns=[r"Zero [pP]oint [vV]ibrational [eE]nergy\s*:\s+(-?\d+.\d+)\s*"],
    )
    def prop_zero_point_energy(self, ctx: RunContext, m, _):
        return float(m[1])
