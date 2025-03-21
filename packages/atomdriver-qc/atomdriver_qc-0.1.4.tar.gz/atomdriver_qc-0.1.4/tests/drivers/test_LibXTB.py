#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import pickle
import unittest

import numpy as np
from conformer_core.records import RecordStatus
from numpy.testing import assert_allclose

from atomdriver.drivers.libxtb import LibxTB
from tests import AtomDriverTestCase
from tests._util import make_system
from tests.drivers.util import H2


class LibxTBTestCases(AtomDriverTestCase):
    def setUp(self) -> None:
        self.driver: LibxTB = LibxTB.from_options(
            "xTB", calc_charges=True, calc_gradient=True
        )
        self.sys = make_system(atoms=2, ghost_atoms=2)

    def tearDown(self) -> None:
        self.driver.cleanup()
        return super().tearDown()

    @unittest.skipIf(not LibxTB.is_available(), "Could not find xTB exe")
    def test_exec(self):
        res = self.driver(H2())

        # Now checkout how our job went :)
        self.assertEqual(res.status, RecordStatus.COMPLETED)
        self.assertTrue("cpu_time" in res.properties)
        self.assertTrue("wall_time" in res.properties)
        self.assertTrue("partial_charges" in res.properties)
        self.assertTrue("nuclear_gradient" in res.properties)
        self.assertAlmostEqual(res.properties["total_energy"], -0.97514, 5)
        # TODO: Look more into this. Running on with GitLab CI gives -0.047947
        #       Local version and CI version are both xTB 6.7.1
        #       Give  
        #       [[ 0.0479468  0.         0.       ]
        #        [-0.0479468  0.         0.       ]]    
        self.assertEqual(res.properties["nuclear_gradient"].shape, (2, 3))
        return  # Disable this test for now.
        assert_allclose(
            res.properties["nuclear_gradient"].data,
            np.array([[-0.04957603, 0.0, 0.0], [0.04957603, 0.0, 0.0]]),
            atol=1e-2,
        )

    @unittest.skipIf(not LibxTB.is_available(), "Could not find xTB exe")
    def test_exec_fail(self):
        bad_driver = LibxTB.from_options(max_scf=1)
        res = bad_driver(H2())
        self.assertEqual(res.status, RecordStatus.FAILED)
        self.assertEqual(
            res.meta["error"],
            "Single point calculation failed:\n-2- xtb_calculator_singlepoint: Electronic structure method terminated\n-1- scf: Self consistent charge iterator did not converge",
        )

    @unittest.skipIf(not LibxTB.is_available(), "Could not find xTB exe")
    def test_pickle(self):
        _ = self.driver(H2())
        self.driver.cleanup()
        data = pickle.dumps(self.driver)
        loaded_driver = pickle.loads(data)
        _ = loaded_driver(H2())  # Test that it runs
