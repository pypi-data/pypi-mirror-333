#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#

# # # # # # # # # # # # # # # # # # # # # # # # # #
#  Definitions for globally available properties  #
# # # # # # # # # # # # # # # # # # # # # # # # # #

import numpy as np
from conformer.records import Property, SystemMatrixProperty

# Add master list of properties
CPUTime = Property(
    name="cpu_time",
    type=float,
    use_coef=False,
    help="CPU time for a calculation in seconds.",
    unit="s",
    readable_name="CPU Time",
)


WallTime = Property(
    name="wall_time",
    type=float,
    use_coef=False,
    help="Wall time for a calculation in seconds.",
    unit="s",
    readable_name="Wall Time",
)


BasisFunctions = Property(
    name="basis_functions",
    type=int,
    use_coef=False,
    help="Number of basis functions in calculation",
    unit="functions",
    readable_name="# Basis Functions",
)


TotalEnergy = Property(
    name="total_energy",
    type=float,
    use_coef=True,
    help="Total energy of QM system in Hartree",
    unit="Eh",
    readable_name="Total Energy",
)


SCFEnergy = Property(
    name="total_scf_energy",
    type=float,
    use_coef=True,
    help="Total SCF energy before the addition of correlation corrections Hartree",
    unit="Eh",
    readable_name="SCF Energy",
)


DFTExchange = Property(
    name="dft_exchange",
    type=float,
    use_coef=True,
    help="DFT exchange energy in Hartree",
    unit="Eh",
    readable_name="DFT Energy",
)


DFTCorrelation = Property(
    name="dft_correlation",
    type=float,
    use_coef=True,
    help="DFT correlation contribution to total energy Hartree",
    unit="Eh",
    readable_name="DFT Cor.",
)


MP2Correlation = Property(
    name="MP2_correlation",
    type=float,
    use_coef=True,
    help="Couple cluster triples correlation correlation contribution to total energy Hartree",
    unit="Eh",
    readable_name="MP2 Cor.",
)


CCSDCorrelation = Property(
    name="CCSD_correlation",
    type=float,
    use_coef=True,
    help="Couple cluster singles and doubles correlation contribution to total energy Hartree",
    unit="Eh",
    readable_name="CCSD Cor.",
)


CCTCorrelation = Property(
    name="CC_T_correlation",
    type=float,
    use_coef=True,
    help="Couple cluster triples correlation correlation contribution to total energy Hartree",
    unit="Eh",
    readable_name="CC_T Energy",
)


HFExchange = Property(
    name="hf_exchange",
    type=float,
    use_coef=True,
    help="Total Hartree Fock exchange energy in Hartree",
    unit="Eh",
    readable_name="HF Exchange",
)


CorrelationEnergy = Property(
    name="total_correlation_energy",
    type=float,
    use_coef=True,
    help="Hartree Fock exchange energy in Hartree",
    unit="Eh",
    readable_name="Total Cor.",
)


KineticEnergy = Property(
    name="kinetic_energy",
    type=float,
    use_coef=True,
    help="Kinetic energy in Hartree",
    unit="Eh",
    readable_name="Kinetic Energy",
)


CoulombEnergy = Property(
    name="total_coulomb_energy",
    type=float,
    use_coef=True,
    help="Coulomb energy in Hartree",
    unit="Eh",
    readable_name="Coulomb Energy",
)


NuclearAttraction = Property(
    name="nuclear_attraction",
    type=float,
    use_coef=True,
    help="Nuclear attraction Energy in Hartree",
    unit="Eh",
    readable_name="Nuclear Attr. Energy",
)


NuclearRepulsion = Property(
    name="nuclear_repulsion",
    type=float,
    use_coef=True,
    help="Nuclear attraction energy in Hartree",
    unit="Eh",
    readable_name="Nuclear Rep. Energy",
)


OneElectronIntegrals = Property(
    name="one_electron_int",
    type=float,
    use_coef=True,
    help="Sum of one-electron integrals in Hartree",
    unit="Eh",
    readable_name="One Electron Int.",
)


TwoElectronIntegrals = Property(
    name="two_electron_int",
    type=float,
    use_coef=True,
    help="Sum of one-electron integrals in Hartree",
    unit="Eh",
    readable_name="Two Electron Int.",
)


Enthalpy = Property(
    name="total_enthalpy",
    type=float,
    use_coef=True,
    help="Total enthalpy of QM system in kcal/mol",
    unit="kcal/mol",
    readable_name="Enthalpy",
)


Entropy = Property(
    name="total_entropy",
    type=float,
    use_coef=True,
    help="Total entropy of QM system kcal/mol/K",
    unit="kcal/mol",
    readable_name="Entropy",
)


GibbsFreeEnergy = Property(
    name="total_gibbs",
    type=float,
    use_coef=True,
    help="Total Gibbs free energy of QM system in kcal/mol",
    unit="kcal/mol",
    readable_name="Gibbs Free Energy",
)

NumImaginaryFreq = Property(
    name="num_imaginary_freq",
    type=int,
    use_coef=False,
    help="Number of imaginary frequencies",
    unit="",
    readable_name="Imaginary Frequencies",
)

ZeroPointEnergy = Property(
    name="zero_point_energy",
    type=float,
    use_coef=True,
    help="Zero point vibrational energy in kcal/mol",
    unit="kcal/mol",
    readable_name="Zero Point Energy",
)

NuclearGradient = SystemMatrixProperty(
    name="nuclear_gradient",
    type=np.float64,
    use_coef=True,
    help="Cartesian gradient of the electronic energy",
    unit="??",
    readable_name="Nuclear Gradient",
    window=(1, 3),
    extensive=(True, False),
    dim_labels=("atom", "dof"),
)


NuclearHessian = SystemMatrixProperty(
    name="nuclear_hessian",
    type=np.float64,
    use_coef=True,
    help="Nuclear Hessian",
    unit="TODO: What is this?",
    readable_name="Nuclear Hessian",
    window=(3, 3),
    extensive=(True, True),
    dim_labels=("dof", "dof"),
)


PartialCharges = SystemMatrixProperty(
    name="partial_charges",
    type=np.float64,
    use_coef=True,
    help="Partial charges for each nuclie",
    unit="e-",
    readable_name="Partial Charges",
    window=(1, 1),
    extensive=(True, False),
    dim_labels=("atom", "charge"),
)
