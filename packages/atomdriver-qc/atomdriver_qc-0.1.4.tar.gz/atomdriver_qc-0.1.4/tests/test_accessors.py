#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import os
import platform
from tempfile import TemporaryDirectory

import numpy as np
from conformer.db.models import DBSystem, DBSystemRecord
from conformer.records import RecordStatus, SystemRecord

from atomdriver.accessors import (
    DBLayer,
    DictCacheLayer,
    Dispatcher,
    DriverAccessor,
    LocalCalcLayer,
    RayCalcLayer,
    clear_accessor_cache,
    get_accessor,
)
from atomdriver.drivers.libxtb import LibxTB
from tests import AtomDriverDBTestCase
from tests.drivers.util import H2


class SystemLayerTestCases(AtomDriverDBTestCase):
    def setUp(self) -> None:
        self.sys = H2()
        self.driver = LibxTB()
        self.record = SystemRecord(
            self.driver, system=self.sys, status=RecordStatus.COMPLETED
        )

    def tearDown(self) -> None:
        clear_accessor_cache()

    def test_dict_cache(self):
        cache = DictCacheLayer(self.driver)

        cache.submit(self.sys)
        self.assertEqual(cache.num_submitted, 1)

        completed = cache.get_completed()
        self.assertListEqual(completed, [(self.sys, None)])
        self.assertEqual(cache.num_completed, 1)

        cache.update([self.record])
        shifted_sys = self.sys.shift(np.array([1, 1, 1]))

        cache.submit(self.sys)
        cache.submit(shifted_sys)
        self.assertEqual(cache.num_submitted, 3)

        completed = cache.get_completed()
        self.assertEqual(cache.num_completed, 3)
        self.assertEqual(len(completed), 2)

        self.assertSetEqual({self.sys, shifted_sys}, {s[0] for s in completed})
        self.assertEqual(self.record, completed[0][1])
        self.assertEqual(self.record.swap_system(shifted_sys), completed[1][1])

    def test_db_layer(self):
        db = DBLayer(self.driver)
        RECORD_ID = self.record.id  # Will be checking this later...

        db.submit(self.sys)
        completed = db.get_completed()
        self.assertListEqual(completed, [(self.sys, None)])

        self.assertEqual(DBSystem.select().count(), 0)
        self.assertEqual(DBSystemRecord.select().count(), 0)

        # Try updating the record
        db.update([self.record])
        self.assertEqual(DBSystem.select().count(), 1)
        self.assertEqual(DBSystemRecord.select().count(), 1)

        # Check the database again
        db.submit(self.sys)
        db.submit(self.sys)
        completed = db.get_completed()

        # Dict Equal does not work for records dict
        self.assertEqual(len(completed), 2)
        self.assertEqual(completed[0], completed[1])
        self.assertListEqual(completed, [(self.sys, self.record)] * 2)

        self.assertEqual(DBSystem.select().count(), 1)
        self.assertEqual(DBSystemRecord.select().count(), 1)

        # Check double-updates
        record2 = SystemRecord(
            self.driver, system=self.sys, status=RecordStatus.COMPLETED
        )

        db.update([record2])
        db.submit(self.sys)
        completed = db.get_completed()

        self.assertEqual(DBSystem.select().count(), 1)
        self.assertEqual(DBSystemRecord.select().count(), 1)

        db_rec = completed[0][1]
        self.assertEqual(db_rec.id, RECORD_ID)
        self.assertEqual(db_rec._saved, 1)
        self.assertEqual(db_rec.status, RecordStatus.COMPLETED)

    def test_local_calc_layer(self):
        runner = LocalCalcLayer(self.driver)
        runner.submit(self.sys)
        rec = runner.get_completed()[0][1]
        self.assertEqual(rec.system, self.sys)

    def test_ray_calc_layer(self):
        import ray

        try:
            cwd = os.getcwd()
            tmp = TemporaryDirectory()

            # Kludge for https://github.com/ray-project/ray/issues/7724
            if platform.system() == "Darwin":
                _p_dir = None
                _t_dir = None
            else: # Helps it run in Docker containers
                _p_dir = tmp.name + "/p"
                _t_dir = tmp.name + "/t"
                os.mkdir(_p_dir)
                os.mkdir(_t_dir)
                os.chdir(tmp.name)

            ray.init(
                num_cpus=1,
                include_dashboard=False,
                logging_level="warn",
                _temp_dir=_t_dir,
                _plasma_directory=_p_dir
            )
            driver = RayCalcLayer(self.driver)

            # Submit twice. See if we get it twice
            driver.submit(self.sys)
            driver.submit(self.sys)
            results = list(driver.as_completed())
        finally:
            ray.shutdown()
            tmp.cleanup()
            os.chdir(cwd)

        # Check that job ran succesfully
        self.assertEqual(len(results), 2)

        # Should just return two of the same record
        self.assertEqual(results[0], results[1])

    def test_driver_accessor(self):
        accessor = DriverAccessor.get_accessor(
            self.driver, use_cache=True, use_database=True, use_ray=False
        )

        cache: DictCacheLayer = accessor.layers[0]
        db: DBLayer = accessor.layers[1]
        runner: LocalCalcLayer = accessor.layers[2]

        # Check the runner layer
        accessor.submit(self.sys)
        accessor.submit(self.sys)
        completed = accessor.get_completed()

        self.assertEqual(len(completed), 2)
        sys, rec = completed[0]
        self.assertEqual(self.sys, rec.system)

        self.assertEqual(accessor.num_completed, 2)
        self.assertEqual(cache.num_completed, 1)
        self.assertEqual(db.num_completed, 1)
        self.assertEqual(runner.num_completed, 1)  # Stops here

        # Test down to the DB layer
        cache.cache.clear()
        accessor.submit(self.sys)
        completed = accessor.get_completed()

        self.assertEqual(cache.num_completed, 2)
        self.assertEqual(db.num_completed, 2)  # Stopes Here
        self.assertEqual(runner.num_completed, 1)

        # Test down to the cache layer
        accessor.submit(self.sys)
        completed = accessor.get_completed()

        self.assertEqual(cache.num_completed, 3)  # Stops Here
        self.assertEqual(db.num_completed, 2)
        self.assertEqual(runner.num_completed, 1)

    def test_dispatcher(self):
        accessor = DriverAccessor.get_accessor(
            self.driver, use_cache=True, use_database=False, use_ray=False
        )
        dispatcher = Dispatcher(accessor)

        client1 = dispatcher.get_client()
        client1.submit(self.sys)

        self.assertEqual(client1.num_submitted, 1)
        self.assertEqual(client1.num_completed, 0)
        self.assertEqual(accessor.num_submitted, 1)
        self.assertEqual(accessor.num_completed, 0)

        client2 = dispatcher.get_client()
        client2.submit(self.sys)

        # Deduplication should happen at the dispatcher level
        self.assertEqual(client1.num_submitted, 1)
        self.assertEqual(client1.num_completed, 0)
        self.assertEqual(client2.num_submitted, 1)
        self.assertEqual(client2.num_completed, 0)
        self.assertEqual(accessor.num_submitted, 1)
        self.assertEqual(accessor.num_completed, 0)

        client3 = dispatcher.get_client()
        client3.submit(self.sys.recenter(np.array([1, 1, 1])))

        self.assertEqual(client1.num_submitted, 1)
        self.assertEqual(client1.num_completed, 0)
        self.assertEqual(client2.num_submitted, 1)
        self.assertEqual(client2.num_completed, 0)
        self.assertEqual(client3.num_submitted, 1)
        self.assertEqual(client3.num_completed, 0)
        self.assertEqual(accessor.num_submitted, 2)
        self.assertEqual(accessor.num_completed, 0)

        # One system per client
        self.assertEqual(len(client1.get_completed()), 1)
        self.assertEqual(len(client2.get_completed()), 1)
        self.assertEqual(len(client3.get_completed()), 1)

        # Check the accessor
        self.assertEqual(accessor.layers[0].num_submitted, 1)
        self.assertEqual(accessor.layers[1].num_submitted, 1)

        # Check that things are being flushed in the dispatcher
        self.assertDictEqual(dispatcher.out_queues, {})

    def test_client_realignment(self):
        client = get_accessor(
            self.driver, use_cache=True, use_database=False, use_ray=None
        )

        sys1 = H2()
        sys2 = sys1.shift(np.array([1, 1, 1]))
        sys3 = sys2.shift(np.array([1, 1, 1]))

        client.submit(sys1)
        sys, rep = client.get_completed()[0]
        np.testing.assert_allclose(
            sys.r_matrix - sys1.r_matrix, np.zeros((2, 3)), rtol=1e-6
        )

        client.submit(sys2)
        sys, rep = client.get_completed()[0]
        np.testing.assert_allclose(
            sys.r_matrix - sys2.r_matrix, np.zeros((2, 3)), rtol=1e-6
        )

        client.submit(sys3)
        sys, rep = client.get_completed()[0]
        np.testing.assert_allclose(
            sys.r_matrix - sys3.r_matrix, np.zeros((2, 3)), rtol=1e-6
        )
