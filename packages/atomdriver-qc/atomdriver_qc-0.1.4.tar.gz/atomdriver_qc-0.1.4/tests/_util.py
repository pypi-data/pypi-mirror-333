#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List

import numpy as np
from conformer.common import GHOST_ATOM, PHYSICAL_ATOM, PINNED_ATOM, AtomRole
from conformer.systems import Atom, BoundAtom, System


class TempDirTestCase(unittest.TestCase):
    def run(self, *args, **kwargs):
        # Construct the supporting structure
        self.tmpdir = TemporaryDirectory()
        self.tmppath = Path(self.tmpdir.name)
        with self.tmpdir as _:
            return super().run(*args, **kwargs)


def make_atoms(n, role: AtomRole) -> List[BoundAtom]:
    if n == 0:
        return []

    atoms = [
        BoundAtom(Atom("H", np.array([float(i), float(i), float(i)])), role=role)
        for i in range(n)
    ]
    return atoms


def make_system(
    atoms=0,
    ghost_atoms=0,
    pinned_atoms=0,
) -> System:
    _atoms = make_atoms(atoms, PHYSICAL_ATOM)
    _ghost_atoms = make_atoms(ghost_atoms, GHOST_ATOM)
    _pinned_atoms = make_atoms(pinned_atoms, PINNED_ATOM)
    sys = System(
        atoms=_atoms + _ghost_atoms + _pinned_atoms,
    )
    return sys
