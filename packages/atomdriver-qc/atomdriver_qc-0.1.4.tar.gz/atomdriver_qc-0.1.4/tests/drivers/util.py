#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
from conformer.systems import System


def H2() -> System:
    return System.from_tuples([("H", 0, 0, 0), ("H", 0.92, 0, 0)])
