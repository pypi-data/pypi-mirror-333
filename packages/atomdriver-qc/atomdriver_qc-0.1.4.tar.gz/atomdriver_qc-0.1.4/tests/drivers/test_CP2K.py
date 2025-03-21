#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import unittest
from os import environ
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
from conformer_core.records import RecordStatus
from numpy.testing import assert_allclose

from atomdriver.drivers.cp2k import CP2K, CP2KProc
from tests import AtomDriverTestCase
from tests._util import make_system
from tests.drivers.util import H2

INPUT_TEMPLATE = """\
&GLOBAL
  PROJECT {name}
  PRINT_LEVEL LOW
  RUN_TYPE ENERGY
&END GLOBAL

&FORCE_EVAL
  METHOD QS
  &DFT
    CHARGE {charge}
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME {static_path}/potential.pot
    &MGRID
        COMMENSURATE 
        CUTOFF 400
        NGRIDS 5
    &END MGRID
    &QS
      EPS_DEFAULT 1.0E-14
      EXTRAPOLATION ASPC
      EXTRAPOLATION_ORDER 3
    &END QS
    &SCF
      SCF_GUESS ATOMIC
      MAX_SCF 30
      EPS_SCF 1.0E-6
      &OT
        MINIMIZER DIIS
        PRECONDITIONER FULL_ALL
      &END OT
      &OUTER_SCF
          MAX_SCF 10
          EPS_SCF 1.0E-6
      &END OUTER_SCF
    &END SCF
    &XC
      &XC_FUNCTIONAL
        &PBE
          PARAMETRIZATION REVPBE
        &END PBE
      &END XC_FUNCTIONAL
      &vdW_POTENTIAL
        DISPERSION_FUNCTIONAL PAIR_POTENTIAL
        &PAIR_POTENTIAL
          TYPE DFTD3
          PARAMETER_FILE_NAME dftd3.dat
          REFERENCE_FUNCTIONAL revPBE
        &END
      &END vdW_POTENTIAL
    &END XC
    &POISSON
      POISSON_SOLVER WAVELET
      PERIODIC NONE
    &END POISSON
  &END DFT
  
  &SUBSYS
    &CELL
      ABC {cell_a} {cell_b} {cell_c}
      PERIODIC NONE
    &END CELL
    &TOPOLOGY
      COORD_FILE_NAME {geometry_file}
      COORD_FILE_FORMAT XYZ
      &CENTER_COORDINATES 
      &END CENTER_COORDINATES 
    &END TOPOLOGY
    &KIND O
      BASIS_SET DZVP-MOLOPT-GTH-q6
      POTENTIAL GTH-revPBE-q6
    &END KIND
    &KIND H
      BASIS_SET DZVP-MOLOPT-GTH-q1
      POTENTIAL GTH-revPBE-q1
    &END KIND
  &END SUBSYS
&END FORCE_EVAL
&END
"""

POTENTIAL_FILE = """\
#
H GTH-revPBE-q1
	1	0	0	0
	0.20016995890943	2	-4.17620500156816	0.72331890028322
	0
#
N GTH-revPBE-q5
	2	3	0	0
	0.28170297703800	2 -12.44749931239895	1.88552287889776
	1
	0.25546700814149	1	13.57047242882571
#
C GTH-revPBE-q4
	2	2	0	0
	0.33844318955221	2	-8.72754824830209	1.34292529706254
	1
	0.30251428183120	1	9.61143874244521
#
O GTH-revPBE-q6
	2	4	0	0
	0.23926594896015	2 -16.93098298728737	2.52854372456023
	1
	0.22052348957419	1	18.42348732424916
#
K GTH-revPBE-q9
	3	6	0	0
	0.39250464514581	2	-3.36355185931784	-1.05652974706380
	2
	0.30531773770277	2	17.85062322518532	-5.62264869939036
	7.26130826238767
	0.31656802191361	2	7.33378021694260	-2.46094504966893
	2.91120443661679
#
Al GTH-revPBE-q3
	2	1	0	0
	0.43522493716126	2	-8.27253615740789	0.12340152465836
	2
	0.48743074481381	2	6.92421170398871	-1.88883583255700
	2.44150480767714
	0.56259598095577	1	1.86709197536867
#
Si GTH-revPBE-q4
	2	2	0	0
	0.43224079969648	1	-6.26928834981876
	2
	0.43563382750146	2	8.90861648065539	-2.70627081846166
	3.50378060414596
	0.49794218773404	1	2.43127674242674
#
Cl GTH-revPBE-q7
	2	5	0	0
	0.412034522378	2	-6.387383124731	-0.009021846686
	2
	0.339499063755	2	15.221166054129	-4.941683697911
	6.377370338332
	0.378779796494	1	4.341201779417
#
Zn GTH-revPBE-q12
	2	0	10	0
	0.51000000228344	0
	3
	0.40031643972938	3	11.53004133325909	-8.79189815087765	3.14508644050535
	16.46577517823516	-8.12057826991473
	6.44550918109619
	0.54318233049508	2	2.59719511863852	-0.59426275777150
	0.70314116434215
	0.25095883990735	1 -14.46695794737136
#
Zn GTH-revPBE-q20
	4	6	10	0
	0.34729494527940	2	0.55188457612508	1.24394371538092
	3
	0.24394891392819	2	-1.34762692127901	12.79313122006917
	-16.51586127796785
	0.23975357983051	2	-9.72145778524195	8.07114354774031
	-9.54990573621412
	0.20855197150871	1 -14.19380886456333
#
Li GTH-revPBE-q3
	3	0	0	0
	0.40000000000000	4 -14.08115455000000	9.62621962000000	-1.78361605000000	0.08515207000000
	0
#
I GTH-revPBE-q7
	2	5	0	0
	0.56097542412968	1	8.30696737704382
	3
	0.53192813005532	3	2.30814580951754	1.00390933198339	-0.95915606171248
	-2.85610798585839	2.47653030126803
	-1.96568497424122
	0.58918243972806	2	0.90648219018486	0.42507060006662
	-0.50295032038699
	0.74085157566198	1	0.47919458163563
#
Be GTH-revPBE-q4
	4	0	0	0
	0.32499880271667	4 -24.07750832805718	17.29795124769334	-3.34457120268635	0.16592706571054
	0
#
Ca GTH-revPBE-q10
	4	6	0	0
	0.37678047893891	2	-4.18920270368861	-1.58269419211563
	3
	0.28959658426544	2	20.60271759134962	-7.12978577970040
	9.20451388087920
	0.32798190506635	2	5.80560515445721	-0.42875335998725
	0.50730783345657
	0.66395554334508	1	0.05806812816398
#
Mg GTH-revPBE-q10
	4	6	0	0
	0.19368897937368	2 -20.57355447707430	3.03432071800105
	2
	0.14135522938540	1	41.04812203589492
	0.10309633839049	1	-9.99181442015447
#
F GTH-revPBE-q7
	2	5	0	0
	0.21567445455070	2 -21.48683351622989	3.21178110848798
	1
	0.19458888073306	1	23.75455185056465
#
Pb GTH-revPBE-q4
	2	2	0	0
	0.62653984021894	1	4.80942462908873
	3
	0.62239090790603	3	0.91062966105019	2.08114783414933	-1.43125709514796
	-5.01469015497042	3.69548993848729
	-2.93320024763669
	0.82127204767750	2	0.15775036263689	0.47889785159446
	-0.56326396709903
	1.02293599354606	1	0.35389806040014
#
Pb GTH-revPBE-q14
	2	2	10	0
	0.52999999956377	1	12.57214280289374
	3
	0.49588591819966	2	8.41124414880275	-3.44005610001354
	4.48109332262415
	0.56934785269083	2	4.92900648134337	-2.89639919972065
	3.42706575600028
	0.40422412959527	2	-6.81491261568961	1.83782672991795
	-2.08389963461851
#
Na GTH-revPBE-q9
	3	6	0	0
	0.273005790125	2	0.338497427794	-0.626328732556
	2
	0.125922383347	1	34.093580226825
	0.147350171683	1 -14.234385268353
"""

LJ_INPUT = """
&GLOBAL                  ! section to select the kind of calculation
   RUN_TYPE ENERGY       ! select type of calculation. In this case: ENERGY (=Single point calculation)
&END GLOBAL
&FORCE_EVAL              ! section with parameters and system description
  METHOD FIST            ! Molecular Mechanics method
  &MM                    ! specification of MM parameters 
    &FORCEFIELD          ! parameters needed to describe the potential 
    &SPLINE
    EMAX_SPLINE 10000    ! numeric parameter to ensure calculation stability. Should not be changed
    &END
        &NONBONDED       ! parameters for the non bonded interactions
          &LENNARD-JONES ! Lennard-Jones parameters
          atoms Kr Kr
          EPSILON    [K_e] 164.56
          SIGMA [angstrom]   3.601
          RCUT  [angstrom]  25.0
        &END LENNARD-JONES
      &END NONBONDED
      &CHARGE
        ATOM Kr
        CHARGE 0.0
      &END CHARGE
    &END FORCEFIELD
    &POISSON              ! solver for non periodic calculations
     PERIODIC NONE
      &EWALD
        EWALD_TYPE none
      &END EWALD
    &END POISSON
  &END MM
  &SUBSYS                 ! system description 
    &CELL
     ABC [angstrom] 10 10 10  
     PERIODIC NONE
    &END CELL
    &COORD                
      UNIT angstrom
      Kr  0 0 0
      Kr  4 0 0
    &END COORD
   &END SUBSYS
&END FORCE_EVAL
"""


@unittest.skipIf(not CP2K.is_available(), "Could not find cp2k exe")
class CP2KShellInterfaceTestCases(unittest.TestCase):
    def test_shell(self):
        with TemporaryDirectory() as f_name:
            work_path = Path(f_name)
            input_file = work_path / "lj.inp"
            with input_file.open("w") as inp:
                inp.write(LJ_INPUT)
            proc = CP2KProc([environ.get("CP2K_EXEC", "cp2k"), "--shell"], work_path)
            proc.startup()
            self.assertTrue(proc.VERSION().startswith("CP2K Shell Version: "))
            self.assertTrue(proc.INFO())  # Don't check this in detail
            self.assertEqual(  # Can't do direct comparison (symbolic links)
                proc.PWD().split("/")[-1], f_name.split("/")[-1]
            )
            self.assertEqual(proc.UNITS(), "au")
            proc.UNITS_EV_A()
            self.assertEqual(proc.UNITS(), "eV_A")
            proc.UNITS_AU()  # Switch back
            self.assertEqual(proc.UNITS(), "au")

            env = proc.load_file("lj.inp", "lj.out")
            self.assertEqual(proc.LAST_ENV_ID(), 1)

            self.assertEqual(env.natom, 2)
            assert_allclose(env.positions, np.array([[0, 0, 0], [4, 0, 0]]))
            assert_allclose(env.cell, np.array([[10, 0, 0], [0, 10, 0], [0, 0, 10]]))

            # Check that we can change the cell
            env.cell = np.array([[5, 0, 0], [0, 5, 0], [0, 0, 5]])
            assert_allclose(env.cell, np.array([[5, 0, 0], [0, 5, 0], [0, 0, 5]]))
            self.assertAlmostEqual(env.get_energy(), 0.0)
            self.assertAlmostEqual(env.calc_energy(), -0.00051894)

            energy, grad = env.calc_force_energy()
            self.assertAlmostEqual(energy, -0.00051894)
            assert_allclose(
                grad, np.array([[-5.710054e-5, 0, 0], [5.710054e-5, 0, 0]]), atol=1e-5
            )

            self.assertAlmostEqual(env.get_energy(), -0.00051894)
            assert_allclose(
                env.get_forces(),
                np.array([[-5.710054e-5, 0, 0], [5.710054e-5, 0, 0]]),
                atol=1e-5,
            )

            env.positions = np.array([[0, 0, 0], [2, 0, 0]])
            assert_allclose(env.positions, np.array([[0, 0, 0], [2, 0, 0]]))

            proc.shutdown()


@unittest.skipIf(not CP2K.is_available(), "Could not find cp2k exe")
class CP2KTestCases(AtomDriverTestCase):
    def setUp(self) -> None:
        self.backend = CP2K.from_options(template=LJ_INPUT)
        self.backend.configure()
        self.sys = make_system(atoms=2)

    def tearDown(self) -> None:
        self.backend.cleanup()

    def test_atom(self):
        atom = self.sys[0]
        self.assertEqual(
            self.backend.atom_to_str(atom),
            " H  0.00000000  0.00000000  0.00000000"
        )

    @unittest.skip("Not implemented yet")
    def test_ghost_atom(self):
        """CP2K uses a custom kinds command which isn't yet implemented"""
        ...

    def test_template(self):
        ctx = self.backend.system_context(self.sys)

        self.backend.setup_calc(ctx)
        out_templ = self.backend.ctx_to_str(ctx)
        self.backend.cleanup_calc(ctx)

        self.assertTrue(out_templ.startswith("\n&GLOBAL"))

    @unittest.skipIf(not CP2K.is_available(), "Could not find cp2k exe")
    def test_exec(self):
        backend = CP2K.from_options(
            template=INPUT_TEMPLATE,
            static_files={"potential.pot": POTENTIAL_FILE},
            calc_gradient=True,
        )
        H2_periodic = H2()
        H2_periodic.unit_cell = np.array([5.0, 5.0, 5.0])
        res = backend(H2_periodic)

        # Now checkout how our job went :)
        self.assertEqual(res.status, RecordStatus.COMPLETED)
        self.assertAlmostEqual(res.properties["total_energy"], -1.16302222, 5)
        assert_allclose(
            res.properties["nuclear_gradient"].data,
            np.array(
                [
                    [-7.083475e-02, -2.122029e-08, -2.122029e-08],
                    [7.083544e-02, -2.238672e-08, -2.238672e-08],
                ]
            ),
            atol=1e-5,
        )
