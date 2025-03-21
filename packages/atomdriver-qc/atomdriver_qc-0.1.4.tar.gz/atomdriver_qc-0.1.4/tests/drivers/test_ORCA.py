#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import unittest
from io import StringIO
from textwrap import dedent

from conformer_core.records import RecordStatus

from atomdriver.drivers.orca import ORCA
from tests import AtomDriverTestCase
from tests._util import make_system
from tests.drivers.util import H2


class OrcaTestCases(AtomDriverTestCase):
    def setUp(self) -> None:
        self.backend = ORCA()
        self.backend.configure()
        self.sys = make_system(atoms=2, ghost_atoms=2)

    def tearDown(self) -> None:
        self.backend.cleanup()
        return super().tearDown()

    def test_atom(self):
        atom = self.sys[0]
        self.assertEqual(self.backend.atom_to_str(atom), "H    0.0 0.0 0.0")

    def test_ghost_atom(self):
        atom = self.sys[2]
        self.assertEqual(
            self.backend.atom_to_str(atom), "H:    0.0 0.0 0.0"
        )

    def test_template(self):
        ctx = self.backend.system_context(self.sys)
        out_templ = self.backend.ctx_to_str(ctx)
        self.assertEqual(
            out_templ,
            "# Name: sys-c9cd0a3a\n! B3LYP SP 6-31G\n\n*xyz 0 1\nH    0.0 0.0 0.0\nH    1.0 1.0 1.0\nH:    0.0 0.0 0.0\nH:    1.0 1.0 1.0\n*\n",
        )

    def test_properties(self):
        props = self.backend.get_properties(
            None,
            [
                StringIO(
                    dedent(
                        """\
        Total Energy       :         -496.88645078 Eh          -13520.96772 eV
        TOTAL RUN TIME: 0 days 0 hours 1 minutes 11 seconds 2 msec
        Total Enthalpy                    ...   -157.06107433 Eh
        Final entropy term                ...      0.03354941 Eh     21.05 kcal/mol
        Final Gibbs free energy         ...   -157.09462374 Eh
        """
                    )
                )
            ],
        )
        self.assertDictEqual(
            props.to_dict(),
            {
                "total_energy": -496.88645078,
                "cpu_time": 71.002,
                "total_entropy": 0.03354941,
                "total_enthalpy": -157.06107433,
                "total_gibbs": -157.09462374,
            },
        )

    @unittest.skipIf(not ORCA.is_available(), "Could not find ORCA exe")
    def test_exec(self):
        res = self.backend(H2())

        # Now checkout how our job went :)
        self.assertEqual(res.status, RecordStatus.COMPLETED)
        self.assertAlmostEqual(res.properties["total_energy"], -1.153897, 4)
