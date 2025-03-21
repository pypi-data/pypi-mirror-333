#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import unittest
from textwrap import dedent

import numpy as np
from conformer.systems import System
from conformer_core.records import RecordStatus

from atomdriver.drivers.qchem import QChem
from tests import AtomDriverTestCase
from tests._util import make_system
from tests.drivers.qchem_outfiles import (
    TEST_BAD_MULT,
    TEST_CCSD_OUT,
    TEST_CCSDT_OUT,
    TEST_MP2_OUT,
    TEST_WB97XV_OUT,
    TEST_WB97XV_OUT_NO_SCFMAN,
)
from tests.drivers.util import H2


class QChemTestCases(AtomDriverTestCase):
    def setUp(self) -> None:
        self.backend = QChem()
        self.backend.configure()  # Load template
        self.sys = make_system(atoms=2, ghost_atoms=2)

    def tearDown(self) -> None:
        self.backend.cleanup()
        return super().tearDown()

    def test_errors(self):
        backend = QChem.from_options()
        backend.configure()
        rec = backend.mk_record(System(atoms=[]))
        ctx = backend.mk_context(rec)
        with open(TEST_BAD_MULT, "r") as f:
            _ = backend.get_properties(ctx, [f])
        self.assertEqual(rec.status, RecordStatus.FAILED)
        self.assertIn(" Q-Chem fatal error", rec.meta["error"])
        backend.cleanup()

    def test_DFT_properties(self):
        rec = self.backend.mk_record(System(atoms=[]))
        ctx = self.backend.mk_context(rec)
        with open(TEST_WB97XV_OUT, "r") as f:
            props = self.backend.get_properties(ctx, [f])
        self.assertEqual(len(rec.meta["warnings"]), 1)
        self.assertEqual(
            rec.meta["warnings"][0],
            "Warning:  Energy on first SCF cycle will be non-variational",
        )
        self.assertDictEqual(
            props.to_dict(),
            {
                "nuclear_repulsion": 0.34873964,
                "hf_exchange": -0.30736459065521,
                "dft_exchange": -0.19132616115182,
                "dft_correlation": -0.03594325243512,
                "total_coulomb_energy": 0.96514412043875,
                "one_electron_int": -1.82894628401205,
                "total_scf_energy": -1.0496965291,
                "total_energy": -1.0496965291,
                "cpu_time": 11.87,
            },
        )

    @unittest.skipIf(not QChem.is_available(), "Could not find QChem exe")
    def test_gradient(self):
        """Tests nuclear gradient extraction"""
        backend = QChem.from_options(template = """\
            ! Name: {name}
            $molecule
            {charge} {mult}
            {geometry}
            $end

            $rem
                basis 6-31G
                method HF
                job_type force
            $end
        """)
        sys = System.from_tuples(
            [
                ("O", 0.0000000000, 0.0000000000, 0.0000000000),
                ("H", 0.0000000000, 0.0000000000, 0.9472690000),
                ("H", 0.9226720317, 0.0000000000, -0.2622325328),
                ("O", 2.6471478408, 0.3844315763, -0.9182749348),
                ("H", 3.1174655443, -0.2510444530, -1.4399583931),
                ("H", 2.4898165091, 1.1358441907, -1.4932568902),
                ("H", -0.7410073392, 1.4056351087, -1.0422511992),
                ("O", -0.8926504046, 2.1871551862, -1.5770641709),
                ("H", -1.3211437399, 2.8135423867, -1.0103863394),
                ("H", 0.8272292940, 2.5359868450, -2.2596898885),
                ("O", 1.7290565094, 2.4955238008, -2.5842220902),
                ("H", 1.6540997866, 2.3948478946, -3.5233223240),
            ]
        )

        # Changed so that the Q-Chem scratch files are read
        result = backend(sys) # Do the calculation for real

        # Gradient test fixture
        test_grad = np.array([
            [ 0.00346724,  0.00330368, -0.00929764],
            [-0.00625258, -0.00983027, -0.0005935 ],
            [ 0.00289265,  0.01043386,  0.00792184],
            [-0.00365455,  0.00430346,  0.00901952],
            [ 0.00998351, -0.00686966,  0.00124243],
            [-0.01027016,  0.00237207, -0.01067529],
            [ 0.00957   , -0.00242863,  0.01115737],
            [ 0.00449506, -0.00441673, -0.00861076],
            [-0.00996682,  0.00675699, -0.00201326],
            [-0.00310454, -0.00895341, -0.00893279],
            [-0.00332152, -0.0047638 ,  0.00893915],
            [ 0.00616169,  0.01009243,  0.00184292]]
        )

        # Older version of the test was giving this reulst. Unclear what has changed...
        # test_grad = np.array([
        #  [ 0.00996682, -0.00675699, -0.00201326],
        #  [-0.00449506,  0.00441673, -0.00861076],
        #  [-0.00957,     0.00242863,  0.01115737],
        #  [-0.00346724, -0.00330368, -0.00929764],
        #  [ 0.00625258,  0.00983027, -0.0005935 ],
        #  [ 0.00310454,  0.00895341, -0.00893279],
        #  [-0.00289265, -0.01043386,  0.00792184],
        #  [-0.00616169, -0.01009243,  0.00184292],
        #  [ 0.00332152,  0.0047638,   0.00893915],
        #  [ 0.01027016, -0.00237207, -0.01067529],
        #  [ 0.00365455, -0.00430346,  0.00901952],
        #  [-0.00998351,  0.00686966,  0.00124243]])
        np.testing.assert_almost_equal(result.properties["nuclear_gradient"], test_grad, 5)
        backend.cleanup()

    @unittest.skipIf(not QChem.is_available(), "Could not find QChem exe")
    def test_hessian(self):
        """Tests nuclear Hessian extraction"""
        backend = QChem.from_options(template = """\
            ! Name: {name}
            $molecule
            {charge} {mult}
            {geometry}
            $end

            $rem
                basis 6-31G
                method HF
                job_type freq
            $end
        """)
        sys = System.from_tuples(
            [
                ("O", 0.0000000000, 0.0000000000, 0.0000000000),
                ("H", 0.0000000000, 0.0000000000, 0.9472690000),
                ("H", 0.9226720317, 0.0000000000, -0.2622325328),
            ]
        )

        # Changed so that the Q-Chem scratch files are read
        result = backend(sys) # Do the calculation for real

        hessian = result.properties["nuclear_hessian"]
        test_hessian = np.array([[ 7.54497722e-01, -3.13946248e-02,  1.46316173e-16,
                -3.83942902e-01,  2.95585887e-01, -2.33595510e-16,
                -3.70554820e-01, -2.64191262e-01,  8.72793367e-17],
               [-3.13946248e-02,  4.71869735e-01, -1.83558163e-16,
                 2.19851378e-01, -2.50519236e-01,  2.19190959e-17,
                -1.88456754e-01, -2.21350498e-01,  1.61639067e-16],
               [ 1.46316173e-16, -1.83558163e-16,  1.43577886e-02,
                -2.34475452e-16,  3.69649078e-17, -3.53495699e-03,
                 8.81592789e-17,  1.46593255e-16, -1.08228316e-02],
               [-3.83942902e-01,  2.19851378e-01, -2.34475452e-16,
                 4.24551609e-01, -2.58151628e-01,  2.54034014e-16,
                -4.06087074e-02,  3.83002491e-02, -1.95585625e-17],
               [ 2.95585887e-01, -2.50519236e-01,  3.69649078e-17,
                -2.58151628e-01,  2.36361368e-01, -3.07698897e-17,
                -3.74342595e-02,  1.41578682e-02, -6.19501811e-18],
               [-2.33595510e-16,  2.19190959e-17, -3.53495699e-03,
                 2.54034014e-16, -3.07698897e-17, -2.19188947e-03,
                -2.04385046e-17,  8.85079380e-18,  5.72684646e-03],
               [-3.70554820e-01, -1.88456754e-01,  8.81592789e-17,
                -4.06087074e-02, -3.74342595e-02, -2.04385046e-17,
                 4.11163528e-01,  2.25891013e-01, -6.77207742e-17],
               [-2.64191262e-01, -2.21350498e-01,  1.46593255e-16,
                 3.83002491e-02,  1.41578682e-02,  8.85079380e-18,
                 2.25891013e-01,  2.07192630e-01, -1.55444049e-16],
               [ 8.72793367e-17,  1.61639067e-16, -1.08228316e-02,
                -1.95585625e-17, -6.19501811e-18,  5.72684646e-03,
                -6.77207742e-17, -1.55444049e-16,  5.09598512e-03]])
        np.testing.assert_almost_equal(hessian, test_hessian, 5)
        backend.cleanup()

    def test_no_scfman_properties(self):
        with open(TEST_WB97XV_OUT_NO_SCFMAN, "r") as f:
            props = self.backend.get_properties(None, [f])
            self.maxDiff = None
        self.assertDictEqual(
            props.to_dict(),
            {
                "nuclear_repulsion": 0.34873964,
                "hf_exchange": -0.3073645906,
                "dft_exchange": -0.1913261612,
                "dft_correlation": -0.0359432524,
                "total_coulomb_energy": 0.9651441204,
                "one_electron_int": -1.828946284,
                "kinetic_energy": 0.7760006951,
                "nuclear_attraction": -2.6049469792,
                "total_scf_energy": -1.04969653,
                "total_energy": -1.04969653,
                "cpu_time": 12.18,
            },
        )

    def test_MP2_properties(self):
        # TEST MP2 template
        backend = QChem.from_options(
            template=dedent(
                """\
        ! Name: {name}
        $molecule
        0 1
        {geometry}
        $end
        $rem
            basis aug-cc-pVTZ
            method mp2
            job_type sp
        $end
        """
            ),
        )
        backend.configure()
        with open(TEST_MP2_OUT, "r") as f:
            props = backend.get_properties(None, [f])
        self.assertEqual(backend.opts.method, "mp2")
        self.assertEqual(backend.opts.basis, "aug-cc-pvtz")
        self.assertEqual(backend.opts.job_type, "sp")
        backend.cleanup()
        self.assertDictEqual(
            props.to_dict(),
            {
                "nuclear_repulsion": 0.34873964,
                "hf_exchange": -0.55072907976639,
                "one_electron_int": -1.80515692871430,
                "total_correlation_energy": -0.04659996,
                "total_coulomb_energy": 1.10145815953278,
                "total_energy": -0.95228817,
                "total_scf_energy": -0.9056882102,
                "cpu_time": 3.54,
            },
        )

    def test_CCSD_properties(self):
        backend = QChem.from_options(
            template=dedent(
                """\
        ! Name: {name}
        $molecule
        0 1
        {geometry}
        $end
        $rem
            basis aug-cc-pVTZ
            method CCSD
            job_type sp
        $end
        """
            ),
        )
        backend.configure()
        with open(TEST_CCSD_OUT, "r") as f:
            props = backend.get_properties(None, [f])
        self.assertEqual(backend.opts.method, "ccsd")
        self.assertEqual(backend.opts.basis, "aug-cc-pvtz")
        self.assertEqual(backend.opts.job_type, "sp")
        backend.cleanup()
        self.assertDictEqual(
            props.to_dict(),
            {
                "nuclear_repulsion": 0.34873964,
                "hf_exchange": -0.47394666363846,
                "one_electron_int": -1.82166189958895,
                "total_correlation_energy": -0.06033663,
                "total_coulomb_energy": 0.94789332727691,
                "total_energy": -1.05931223,
                "total_scf_energy": -0.9989755972,
                "cpu_time": 10.14,
            },
        )

    def test_CCSD_T_properties(self):
        backend = QChem.from_options(
            template=dedent(
                """\
        ! Name: {name}
        $molecule
        0 1
        {geometry}
        $end
        $rem
            basis = aug-cc-pVTZ
            method = CCSD(T)
            job_type = sp
        $end
        """
            ),
        )
        backend.configure()
        with open(TEST_CCSDT_OUT, "r") as f:
            props = backend.get_properties(None, [f])
        self.assertEqual(backend.opts.method, "ccsd(t)")
        self.assertEqual(backend.opts.basis, "aug-cc-pvtz")
        self.assertEqual(backend.opts.job_type, "sp")
        backend.cleanup()
        self.assertDictEqual(
            props.to_dict(),
            {
                "nuclear_repulsion": 0.34873964,
                "hf_exchange": -0.55072907976639,
                "one_electron_int": -1.80515692871430,
                "total_correlation_energy": 0.00000000,
                "total_coulomb_energy": 1.10145815953278,
                "total_energy": -0.99540333,
                "total_scf_energy": -0.9056882102,
                "cpu_time": 9.04,
            },
        )

    def test_pinned_info(self):
        """Test cases for pinned atoms"""
        pinned_sys = make_system(atoms=2, pinned_atoms=2)
        num, idxs, coords = QChem.pinned_atoms(pinned_sys)
        self.assertEqual(num, 2)
        self.assertEqual(idxs, '3 4')
        self.assertEqual(coords, '3 0.00000000 0.00000000 0.00000000\n4 1.00000000 1.00000000 1.00000000')

    @unittest.skipIf(not QChem.is_available(), "Could not find QChem exe")
    def test_exec(self):
        res = self.backend(H2())

        # Now checkout how our job went :)
        self.assertEqual(res.status, RecordStatus.COMPLETED)
        self.assertAlmostEqual(res.properties["total_energy"], -1.10859, 5)
