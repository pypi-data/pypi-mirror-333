#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
from pkg_resources import resource_filename

# EXAMPLE H2 OUTPUT FILES
TEST_WB97XV_OUT = resource_filename(__name__, "test_wb97xv.out")
TEST_WB97XV_OUT_NO_SCFMAN = resource_filename(__name__, "test_wb97xv_no_scfman.out")
TEST_GRAD_OUT = resource_filename(__name__, "test_GRAD.out")
TEST_MP2_OUT = resource_filename(__name__, "test_MP2.out")
TEST_RIMP2_OUT = resource_filename(__name__, "test_RIMP2.out")
TEST_CCSD_OUT = resource_filename(__name__, "test_CCSD.out")
TEST_CCSDT_OUT = resource_filename(__name__, "test_CCSDT.out")
TEST_CISD_OUT = resource_filename(__name__, "test_CISD.out")
TEST_BAD_MULT = resource_filename(__name__, "test_bad_mult.out")
