#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import pickle
import unittest

import numpy as np
from conformer_core.records import RecordStatus

from atomdriver.drivers.pyscf import (
    CCSD_TOptions,
    CCSDOptions,
    DFMP2Options,
    HFOptions,
    KSOptions,
    MP2Options,
    PySCF,
)
from tests import AtomDriverTestCase
from tests._util import make_system
from tests.drivers.util import H2

ATOM_FIXTURE = [
    ("H", np.array([0.0, 0.0, 0.0])),
    ("H", np.array([1.0, 1.0, 1.0])),
    ("ghost:H", np.array([0.0, 0.0, 0.0])),
    ("ghost:H", np.array([1.0, 1.0, 1.0])),
]


class PySCFTestCases(AtomDriverTestCase):
    @unittest.skipIf(not PySCF.is_available(), "Could not find PySCF exe")
    def test_setup(self) -> None:
        backend = PySCF.from_options(procedure=HFOptions(method="HF", basis="STO-3G"))
        backend.configure()
        ctx = backend.system_context(make_system(atoms=2, ghost_atoms=2))
        backend.setup_calc(ctx)
        backend.cleanup()
        mol = ctx.scratch["mol"]
        self.assertEqual(mol.basis, "STO-3G")
        self.assertEqual(mol.charge, 0)
        self.assertEqual(mol.spin, 0)
        for a, a_ref in zip(ctx.scratch["mol"].atom, ATOM_FIXTURE):
            self.assertEqual(a[0], a_ref[0])
            np.testing.assert_allclose(a[1], a_ref[1])

    @unittest.skipIf(not PySCF.is_available(), "Could not find PySCF exe")
    def test_exec_HF(self):
        backend = PySCF.from_options(procedure=HFOptions(method="HF", basis="STO-3G"))
        res = backend(H2())
        backend.cleanup()

        # Now checkout how our job went :)
        self.assertEqual(res.status, RecordStatus.COMPLETED)
        self.assertTrue("cpu_time" in res.properties)
        self.assertTrue("wall_time" in res.properties)

        PROPERTIES = {
            "nuclear_repulsion": 1.0869565217391304,
            "one_electron_int": -2.839560964360053,
            "total_energy": -1.0305550699899921,
            "total_scf_energy": -1.0305550699899921,
            "two_electron_int": 0.7220493726309302,
        }

        for p, v in PROPERTIES.items():
            self.assertAlmostEqual(res.properties[p], v, 5)

    @unittest.skipIf(not PySCF.is_available(), "Could not find PySCF exe")
    def test_exec_KS(self):
        backend = PySCF.from_options(
            procedure=KSOptions(method="KS", basis="STO-3G", xc="b3lyp")
        )
        res = backend(H2())
        backend.cleanup()

        # Now checkout how our job went :)
        self.assertEqual(res.status, RecordStatus.COMPLETED)
        self.assertTrue("cpu_time" in res.properties)
        self.assertTrue("wall_time" in res.properties)

        PROPERTIES = {
            "dft_exchange": -0.7652628454127979,
            "nuclear_repulsion": 1.0869565217391304,
            "one_electron_int": -2.8395609643600523,
            "total_coulomb_energy": 1.4440987452618606,
            "total_energy": -1.0737685427718593,
            "total_scf_energy": -1.0737685427718593,
        }

        for p, v in PROPERTIES.items():
            self.assertAlmostEqual(res.properties[p], v, 5)

    @unittest.skipIf(not PySCF.is_available(), "Could not find PySCF exe")
    def test_exec_MP(self):
        backend = PySCF.from_options(
            procedure=MP2Options(method="MP2", basis="STO-3G", xc="b3lyp"),
        )
        res = backend(H2())
        backend.cleanup()

        # Now checkout how our job went :)
        self.assertEqual(res.status, RecordStatus.COMPLETED)
        self.assertTrue("cpu_time" in res.properties)
        self.assertTrue("wall_time" in res.properties)

        PROPERTIES = {
            "nuclear_repulsion": 1.0869565217391304,
            "one_electron_int": -2.839560964360053,
            "total_correlation_energy": -0.008286823260946544,
            "total_energy": -1.0388418932509387,
            "total_scf_energy": -1.0305550699899921,
            "two_electron_int": 0.7220493726309302,
        }

        for p, v in PROPERTIES.items():
            self.assertAlmostEqual(res.properties[p], v, 5)

    @unittest.skipIf(not PySCF.is_available(), "Could not find PySCF exe")
    def test_exec_DFMP(self):
        backend = PySCF.from_options(
            procedure=DFMP2Options(method="RIMP2", basis="cc-pVDZ"),
        )
        res = backend(H2())
        backend.cleanup()

        # Now checkout how our job went :)
        self.assertEqual(res.status, RecordStatus.COMPLETED)
        self.assertTrue("cpu_time" in res.properties)
        self.assertTrue("wall_time" in res.properties)

        PROPERTIES = {
            "nuclear_repulsion": 1.0869565217391304,
            "one_electron_int": -2.8814480362747235,
            "total_correlation_energy": -0.0238001845258694,
            "total_energy": -1.0604796952414164,
            "total_scf_energy": -1.036679510715547,
            "two_electron_int": 0.757812003820046,
        }

        for p, v in PROPERTIES.items():
            self.assertAlmostEqual(res.properties[p], v, 5)

    @unittest.skipIf(not PySCF.is_available(), "Could not find PySCF exe")
    def test_exec_CCSD(self):
        backend = PySCF.from_options(
            "pyscf_CCSD", procedure=CCSDOptions(method="CCSD", basis="STO-3G")
        )
        res = backend(H2())
        backend.cleanup()

        # Now checkout how our job went :)
        self.assertEqual(res.status, RecordStatus.COMPLETED)
        self.assertTrue("cpu_time" in res.properties)
        self.assertTrue("wall_time" in res.properties)

        PROPERTIES = {
            "total_energy": -1.0423720957128741,
            "CCSD_correlation": -0.011817025722882075,
            "MP2_correlation": -0.008286823260946546,
            "total_correlation_energy": -0.011817025722882075,
            "nuclear_repulsion": 1.0869565217391304,
            "total_scf_energy": -1.0305550699899921,
            "one_electron_int": -2.839560964360053,
            "two_electron_int": 0.7220493726309302,
        }

        for p, v in PROPERTIES.items():
            self.assertAlmostEqual(res.properties[p], v, 5)

    @unittest.skipIf(not PySCF.is_available(), "Could not find PySCF exe")
    def test_exec_CCSD_T(self):
        backend = PySCF.from_options(
            procedure=CCSD_TOptions(method="CCSD(T)", basis="STO-3G")
        )
        res = backend(H2())
        backend.cleanup()

        # Now checkout how our job went :)
        self.assertEqual(res.status, RecordStatus.COMPLETED)
        self.assertTrue("cpu_time" in res.properties)
        self.assertTrue("wall_time" in res.properties)

        PROPERTIES = {
            "total_energy": -1.0423720957128741,
            "total_scf_energy": -1.0305550699899921,
            "MP2_correlation": -0.008286823260946546,
            "CCSD_correlation": -0.011817025722882075,
            "CC_T_correlation": -1.9014596366096455e-47,
            "total_correlation_energy": -0.011817025722882075,
            "nuclear_repulsion": 1.0869565217391304,
            "one_electron_int": -2.839560964360053,
            "two_electron_int": 0.7220493726309302,
        }

        for p, v in PROPERTIES.items():
            self.assertAlmostEqual(res.properties[p], v, 5)

    @unittest.skipIf(not PySCF.is_available(), "Could not find PySCF exe")
    def test_pickle(self):
        driver = PySCF.from_options(procedure=HFOptions(method="HF", basis="STO-3G"))
        _ = driver(H2())
        driver.cleanup()
        loaded_driver = pickle.loads(pickle.dumps(driver))
        _ = loaded_driver(H2())  # Test that it runs
        loaded_driver.cleanup()
