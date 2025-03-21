#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import unittest
from io import StringIO
from textwrap import dedent

from conformer_core.records import RecordStatus

from atomdriver.drivers.xtb import xTB
from tests import AtomDriverTestCase
from tests._util import make_system
from tests.drivers.util import H2


class xTBTestCases(AtomDriverTestCase):
    def setUp(self) -> None:
        self.backend = xTB()
        self.backend.configure()
        self.sys = make_system(atoms=2, ghost_atoms=2)

    def tearDown(self) -> None:
        self.backend.cleanup()
        return super().tearDown()

    def test_template(self):
        ctx = self.backend.system_context(self.sys)
        out_templ = self.backend.ctx_to_str(ctx)
        self.assertEqual(
            out_templ,
            "4\nFragment sys-c9cd0a3a; Charge=0; Multiplicity=1\nH    0.0 0.0 0.0\nH    1.0 1.0 1.0\n",
        )

    def test_properties(self):
        props = self.backend.get_properties(
            None,
            [
                "output",
                StringIO(
                    dedent(
                        """\
         TOT                       37832.9366   215.6412   321.2541  1344.1271
            -------------------------------------------------
          | TOTAL ENERGY             -164.948939611365 Eh   |
          | TOTAL ENTHALPY           -164.055281977461 Eh   |
         total:
        * wall-time:     0 d,  0 h,  0 min, 42.992 sec
        *  cpu-time:     0 d,  0 h,  4 min, 56.617 sec
        """
                    )
                ),
            ],
        )
        self.assertDictEqual(
            props.to_dict(),
            {
                "total_energy": -164.948939611365,
                "cpu_time": 296.617,
                "total_entropy": 321.2541,
                "total_enthalpy": -164.055281977461,
            },
        )

    @unittest.skipIf(not xTB.is_available(), "Could not find xTB exe")
    def test_exec(self):
        res = self.backend(H2())

        # Now checkout how our job went :)
        self.assertEqual(res.status, RecordStatus.COMPLETED)
        self.assertAlmostEqual(res.properties["total_energy"], -0.97514, 5)
