#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
"""Test the generic driver packages"""

from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from conformer.common import GHOST_ATOM
from conformer.systems import System
from conformer_core.records import RecordStatus

from atomdriver.abstract_driver import (
    Driver,
    FileMixin,
    RunContext,
    ShellCommandMixin,
    StaticFileMixin,
    TemplateMixin,
)
from tests import AtomDriverTestCase

H2O_STR = """\
 H  0.00000000  0.53835160 -0.78303660
 O -0.00000000 -0.01840410  0.00000000
 H -0.00000000  0.53835160  0.78303660
"""

GHOSTED_H2O_STR = """\
@H  0.00000000  0.53835160 -0.78303660
 O -0.00000000 -0.01840410  0.00000000
 H -0.00000000  0.53835160  0.78303660
"""


class TestDriver(Driver):
    def run_calc(self, ctx: RunContext):
        ctx.record.start_time = datetime.now()
        ctx.record.end_time = datetime.now()


class FileDriver(FileMixin):
    def run_calc(self, ctx: RunContext):
        ctx.record.start_time = datetime.now()
        ctx.record.end_time = datetime.now()


class TemplateDriver(TemplateMixin):
    def run_calc(self, ctx: RunContext):
        ctx.record.start_time = datetime.now()
        ctx.record.end_time = datetime.now()


class StaticFileDriver(StaticFileMixin, TemplateMixin):
    def run_calc(self, ctx: RunContext):
        ctx.record.start_time = datetime.now()
        ctx.record.end_time = datetime.now()


class ShellDriver(ShellCommandMixin):
    FILE_MANIFEST = {"input": ".inp", "output": ".out"}

    def setup_calc(self, ctx: RunContext):
        super().setup_calc(ctx)
        with ctx.files["input"].open("w") as f:
            f.write("DATA\n")

    def get_run_cmd(self, ctx: RunContext) -> Tuple[str | List[str]]:
        # No-op command that should run on most systems.
        # tests might not pass on Windows
        return "cp", [
            ctx.files["input"],
            ctx.files["output"],
        ]


class DriverTestCases(AtomDriverTestCase):
    def setUp(self) -> None:
        self.H2O = System.from_string(H2O_STR)

    def test_BaseDriver(self) -> None:
        """Should not create a workpath"""
        driver = TestDriver.from_options()
        self.assertFalse(driver.is_configured)
        self.assertFalse(driver.is_provisioned)
        driver.configure()
        ctx = driver.system_context(self.H2O)
        self.assertIsNone(ctx.workpath)

        self.assertTrue(driver.is_configured)
        self.assertTrue(driver.is_provisioned)

        # Check that the basepath is null
        self.assertEqual(driver.allocation.basepath.name, "NULL")

        # Test that it runs
        res = driver(self.H2O)
        self.assertIsInstance(res.start_time, datetime)
        self.assertIsInstance(res.end_time, datetime)
        self.assertTrue("wall_time" in res.properties)

    def test_FileDriver(self):
        """Driver should create a workpath"""
        driver = FileDriver.from_options()

        driver.configure()
        ctx = driver.system_context(self.H2O)

        # Should create a temporary file
        basepath = driver.allocation.basepath
        self.assertTrue(basepath.exists())
        self.assertEqual(ctx.workpath, basepath / str(ctx.record.id))

        # Should clean up
        driver(self.H2O)
        driver.cleanup()
        self.assertFalse(basepath.exists())

        # Test keeping files
        driver = FileDriver.from_options(remove_files=False)
        driver.configure()
        rec = driver(self.H2O)
        self.assertTrue(Path(rec.meta["work_path"]).exists())
        driver.cleanup()

    def test_TemplateDriver(self):
        """Driver should automatically write the system to the input.inp file"""
        driver = TemplateDriver.from_options()
        self.H2O.update_atoms([0], role=GHOST_ATOM)
        ctx = driver.system_context(self.H2O)

        # Trigger the template write.
        driver.setup_calc(ctx)
        with ctx.files["input"].open("r") as f:
            self.assertEqual(
                f.read(), "sys-355ee5f5: n_atoms=3\n\n" + "0 2\n" + GHOSTED_H2O_STR
            )
        driver.cleanup()

    def test_StaticDriver(self):
        """Driver should create a STATIC folder containing a data.txt file"""
        driver = StaticFileDriver.from_options(static_files={"data.txt": "STATIC DATA"})
        driver.configure()
        self.assertTrue((driver.allocation.basepath / "STATIC" / "data.txt").exists())

        # The TemplateMixin interacts with the static mixin. Check that line of code
        ctx = driver.system_context(self.H2O)
        self.assertIn("static_path", driver.get_template_tags(ctx))
        driver.cleanup()

    def test_ShellDriver(self):
        """Writes and the copies the input file to the output file"""
        driver = ShellDriver.from_options()
        ctx = driver.system_context(self.H2O)

        # Do steps manually to prevent cleanup
        driver.setup_calc(ctx)
        driver.run_calc(ctx)
        driver.gather_results(ctx)

        self.assertEqual(ctx.record.status, RecordStatus.COMPLETED)
        with ctx.files["input"].open("r") as f_input:
            with ctx.files["output"].open("r") as f_output:
                # This driver copies the file
                self.assertEqual(f_input.read(), f_output.read())

        # Clean up
        driver.cleanup_calc(ctx)

        # Do it again to test file retention policy
        ctx = driver.system_context(self.H2O)
        driver.setup_calc(ctx)
        driver.run_calc(ctx)
        driver.gather_results(ctx)

        # Force failure
        ctx.record.status = RecordStatus.FAILED

        driver.cleanup_calc(ctx)
        self.assertDictEqual(
            ctx.record.meta["files"], {"input": "DATA\n", "output": "DATA\n", "log": ""}
        )
        driver.cleanup()
