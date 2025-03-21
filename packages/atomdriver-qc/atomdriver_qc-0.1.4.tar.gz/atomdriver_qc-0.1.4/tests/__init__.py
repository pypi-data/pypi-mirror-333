#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
from conformer_core.testing import DBTestCase


class AtomDriverTestCase(DBTestCase, enable_tmpdir=False, enable_db=False):
    CONFIG = "atomdriver"

    @classmethod
    def setUpClass(cls):
        # Start it once for the entire test suite/module
        pass

    @classmethod
    def tearDownClass(cls):
        # ray.shutdown()
        pass


class AtomDriverDBTestCase(DBTestCase, enable_tmpdir=False, enable_db=True):
    CONFIG = "atomdriver"
