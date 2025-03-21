#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import unittest
from io import StringIO
from textwrap import dedent

from conformer.common import GHOST_ATOM
from conformer_core.records import RecordStatus

from atomdriver.drivers.gamess import GAMESS
from tests import AtomDriverTestCase
from tests._util import make_system
from tests.drivers.util import H2

INPUT_FILE_FIXTURE = " $BASIS\n    GBASIS=N31\n    NGAUSS=6\n $END\n\n $CONTRL\n    ICHARG=0\n    MULT=2\n $END\n\n $DATA\n    SYSTEM: sys-247e8933\n    C1\n    H -1  0.920000000  0.000000000  0.000000000\n    H  1  0.000000000  0.000000000  0.000000000\n $END\n\n"


class GAMESSTestCases(AtomDriverTestCase):
    def setUp(self) -> None:
        self.backend = GAMESS()
        self.backend.configure()
        self.sys = make_system(atoms=2, ghost_atoms=2)

    def tearDown(self) -> None:
        self.backend.cleanup()
        return super().tearDown()

    def test_template(self):
        sys = H2()
        sys.update_atoms([1], role=GHOST_ATOM)
        ctx = self.backend.system_context(sys)
        try:
            self.backend.setup_calc(ctx)
            self.assertEqual(ctx.open_file("input", "r").read(), INPUT_FILE_FIXTURE)
        finally:
            self.backend.cleanup_calc(ctx)
        ctx.close_files()

    def test_properties(self):
        props = self.backend.get_properties(
            None,
            [
                StringIO(
                    dedent(
                        """\
                    -----------------
                    ENERGY COMPONENTS
                    -----------------

                            WAVEFUNCTION NORMALIZATION =       1.0000000000

                                    ONE ELECTRON ENERGY =     -65.2165958005
                                    TWO ELECTRON ENERGY =      19.4136026367
                            NUCLEAR REPULSION ENERGY =       6.9836967914
                                                        ------------------
                                        TOTAL ENERGY =     -38.8192963723

                    ELECTRON-ELECTRON POTENTIAL ENERGY =      19.4136026367
                    NUCLEUS-ELECTRON POTENTIAL ENERGY =    -104.5921160835
                    NUCLEUS-NUCLEUS POTENTIAL ENERGY =       6.9836967914
                                                        ------------------
                                TOTAL POTENTIAL ENERGY =     -78.1948166554
                                TOTAL KINETIC ENERGY =      39.3755202831
                                    VIRIAL RATIO (V/T) =       1.9858738651
                    """
                    )
                )
            ],
        )
        self.assertDictEqual(
            props.to_dict(),
            {
                "hf_exchange": 19.4136026367,
                "kinetic_energy": 39.3755202831,
                "nuclear_attraction": -104.5921160835,
                "nuclear_repulsion": 6.9836967914,
                "one_electron_int": -65.2165958005,
                "total_coulomb_energy": -78.1948166554,
                "total_energy": -38.8192963723,
            },
        )

    @unittest.skipIf(not GAMESS.is_available(), "Could not find GAMESS exe")
    def test_exec(self):
        res = self.backend(H2())

        # Now checkout how our job went :)
        self.assertEqual(res.status, RecordStatus.COMPLETED)
        self.assertAlmostEqual(res.properties["total_energy"], -1.108592, 4)
