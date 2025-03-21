#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import inspect
import logging
import os
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from shutil import rmtree
from typing import Any, ClassVar, Dict, List, Optional, TextIO, Tuple

from conformer.records import Property, SystemRecord
from conformer.systems import BoundAtom, System
from conformer_core.properties.core import add_property
from conformer_core.properties.extraction import PropertyExtractorMixin, calc_property
from conformer_core.records import RecordStatus
from conformer_core.stages import Stage, StageOptions
from pydantic import Field, field_validator

import atomdriver.properties as ad_properties  # import to initilize all properties
from atomdriver.context import Machine, ResourceAllocation
from atomdriver.exceptions import (
    BackendRunException,
    ConfigurationError,
    NoOutputFile,
    ProcessFailed,
)

# Adds all properties to the MASTER_PROPERTY_LIST.
# TODO: Replace this with registry code
for name, val in inspect.getmembers(ad_properties):
    if isinstance(val, Property):
        add_property(val)

log = logging.getLogger(__name__)


@dataclass(unsafe_hash=True)
class RunContext:
    """Transient information needed to handle a claculation including files and
    scratch data
    """

    working_system: System  # The working copy of the system
    record: SystemRecord
    workpath: Optional[Path] = None
    scratch: Dict[Any, Any] = field(
        default_factory=dict
    )  # Scratch space for running the calc
    files: Dict[str, Path] = field(default_factory=dict)
    _open_files: Dict[str, TextIO] = field(default_factory=dict)

    def open_file(self, tag: str, mode="r") -> TextIO:
        if tag in self._open_files:
            return self._open_files[tag]
        self._open_files[tag] = self.files[tag].open(mode)
        return self._open_files[tag]

    def close_file(self, tag: str) -> None:
        f = self._open_files.get(tag, None)
        if f is None:
            return
        f.close()
        del self._open_files[tag]

    def close_files(self) -> None:
        for f in self._open_files.values():
            f.close()
        self._open_files = dict()

    def sanitize(self) -> None:
        self.scratch = {}
        self.close_files()

# These types are all valid input for a driver
Runnable = System | SystemRecord | RunContext

class DriverOptions(StageOptions):
    cpus: int = 1  # Max number of CPUs
    memory: Optional[int] = None  # Max memory in MB
    batch_size: int = 5  # How many calculations to run concurrently
    environment: Dict["str", "str"] = Field(default_factory=dict)

    # Options for use with DriverAccessors
    use_database: bool = True
    use_cache: bool = True
    run_calculations: bool = True


class Driver(Stage, PropertyExtractorMixin):
    Options = DriverOptions

    opts: DriverOptions

    # Machine-specific settings
    allocation: ResourceAllocation
    machine: Machine

    # Working status
    is_configured: bool = False
    is_provisioned: bool = False

    @classmethod
    def is_available(cls) -> bool:
        """
        Returns true if this backend be used pending system configuration
        """
        return True


    def __init__(self, *args, **kwargs):
        """Start without an allocation"""
        super().__init__(*args, **kwargs)
        self.allocation = None
        self.machine = None

    def provision(
        self,
        allocation: ResourceAllocation = None,
        cpus: Optional[int] = None,
        memory: Optional[int] = None,
        basepath: Optional[Path] = None,
        machine: Optional[Machine] = None,
        force=False,
    ):
        """
        Gets resource limitations and requirements for the driver

        This information is reused for each calculation run
        """

        if self.allocation and not force:
            return

        self.is_provisioned = True
        self.machine = machine if machine else Machine()

        # We are given an allocation
        if allocation is not None and any([cpus, memory]):
            raise ValueError("Cannot specify both `allocation` and `cpus`/`memory`")
        else:  # We are told what the allocation should be
            if cpus is None:
                cpus = self.opts.cpus
            if memory is None:
                memory = self.opts.memory
            allocation = ResourceAllocation(cpus=cpus, memory=memory, basepath=basepath)

        # Overwrite env variables
        allocation.environ.update(**self.opts.environment)

        self.allocation = allocation

    def configure(self) -> None:
        """Configures backend to work the amount of cores and memory provided by `worker`"""
        if not self.is_provisioned:
            # Set the basepath to one that never will be used
            self.provision(basepath=Path("NULL"))  # Do default provisioning
        self.is_configured = True


    def cleanup(self):
        """Cleanup driver working directory."""
        if self.is_provisioned:
            self.allocation.cleanup()
        self.is_provisioned = False
        self.is_configured = False


    def __del__(self):
        if self.is_configured:
            # TODO: Use proper logging
            # print(f"Warning: Driver \"{self.name}\" ({self.__class__.__name__}) was never called `cleanup`.")
            ...
        self.cleanup()


    def __call__(self, system: Runnable):
        """Run the calculation. If the driver is not yet provision, do so now!"""
        if not self.is_configured:
            self.configure()

        # Convert `system` to RunContext
        if isinstance(system, System):
            rec = self.mk_record(system)
            ctx = self.mk_context(rec)
        elif isinstance(system, SystemRecord):
            ctx = self.mk_context(system)
        elif isinstance(system, RunContext):
            ctx = system
        else:
            raise ValueError(f"Cannot run object of type `{type(system)}`")

        return self.run_ctx(ctx)


    def get_run_env(self, ctx: RunContext) -> Dict[str, str]:
        """Method returns OS environment for subprocess execution"""
        env = self.allocation.environ.copy()
        env.update(**self.opts.environment)
        return env


    def mk_record(self, system: System) -> SystemRecord:
        """Creates a record object for this driver"""
        return SystemRecord(system=system, stage=self)


    def mk_context(self, record: SystemRecord) -> RunContext:
        """Creates a run context for this driver"""
        return RunContext(
            working_system=record.system.canonize(),
            record=record,
            workpath=None,
        )

    def system_context(self, system: System) -> RunContext:
        """Returns a context object for the system"""
        if not self.is_configured:
            self.configure()
        rec = self.mk_record(system)
        return self.mk_context(rec)

    def run_ctx(self, ctx: RunContext) -> SystemRecord:
        """
        Run calculation given a run context
        """

        rec = ctx.record

        try:
            self.setup_calc(ctx)
            self.run_calc(ctx)
            self.gather_results(ctx)
        except Exception as e:
            # Is this the best option? this will be funneled into the DB...
            # Let's let this fail. This is Fragment issue, not a backend subprocess issue
            
            rec.status = RecordStatus.FAILED
            rec.meta["error"] = str(e)
            raise e
        finally:
            self.cleanup_calc(ctx)

        return rec

    def setup_calc(self, ctx: RunContext):
        """
        Ensure that the environment is setup to run the calculation
        """
        ...

    def run_calc(self, ctx: RunContext):
        """Execute the QM backend"""
        raise NotImplementedError(
            f"Please implement `{self.__class__.__name__}.run_calc`"
        )

    def determine_success(self, ctx: RunContext) -> bool:
        return True

    def sources_from_ctx(self, ctx: RunContext) -> List[Any]:
        sources = [ctx]
        return sources

    def gather_results(self, ctx: RunContext) -> RunContext:
        try:
            self.determine_success(ctx)
        except BackendRunException:
            ctx.record.status = RecordStatus.FAILED
        else:
            ctx.record.status = RecordStatus.COMPLETED

        try:
            ctx.record.properties = self.get_properties(ctx, self.sources_from_ctx(ctx))
            return ctx
        finally:
            ctx.close_files()

    def cleanup_calc(self, ctx: RunContext):
        ...

    @calc_property(source="context")
    def prop_wall_time(self, ctx: RunContext):
        if ctx.record.start_time is None or ctx.record.end_time is None:
            return None
        return (ctx.record.end_time - ctx.record.start_time).total_seconds()

####################################################################################
#         SHELL MIXIN
####################################################################################
class FilesPolicy(str, Enum):
    NEVER = "never"
    ON_FAIL = "on_fail"
    ALWAYS = "always"

class FileMixinOptions(DriverOptions):
    remove_files: bool = True
    save_files_policy: FilesPolicy = FilesPolicy.ON_FAIL


class FileMixin(Driver):
    Options = FileMixinOptions

    # Working copy of the environment
    EXTRACTABLE_FILES: ClassVar[List[str]]
    FILE_MANIFEST: ClassVar[Dict[str, str]]

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        # Create defaults. Don't allow these structures to be shared
        #   between classes and their subclasses
        if not hasattr(cls, "EXTRACTABLE_FILES"):
            cls.EXTRACTABLE_FILES = list()
        if not hasattr(cls, "FILE_MANIFEST"):
            cls.FILE_MANIFEST = dict()

    def configure(self) -> None:
        """
        Redefinition of `configure` but allow the resource allocation
        to make a temporary base path
        """
        if not self.is_provisioned:
            self.provision()  # Do default provisioning
        self.is_configured = True

    def mk_context(self, record: SystemRecord) -> RunContext:
        """Add a work path to the run context

        Method assumes we have an allocation
        """
        ctx = super().mk_context(record)
        ctx.workpath = self.allocation.basepath / str(record.id)
        return ctx

    def setup_calc(self, ctx: RunContext):
        """Create the working directory and cache in context"""
        super().setup_calc(ctx)

        # NOTE: It's possible to have an empty FILE_MANIFEST and still be
        #       FILELESS due to non-saved scratch files
        if ctx.workpath is None:
            raise ConfigurationError(f"Driver {self.__class__} needs a workpath")
        if not ctx.workpath.is_absolute():
            raise ConfigurationError(
                "Context has a relative workpath: " + str(ctx.workpath)
            )

        ctx.scratch["old_path"] = os.getcwd()
        ctx.workpath.mkdir(parents=True, exist_ok=True)
        os.chdir(ctx.workpath)

        # Create Path objects for each file in FILE_MANIFEST
        for k, ext in self.FILE_MANIFEST.items():
            if ext.startswith("."):
                ctx.files[k] = ctx.workpath / f"{k}{ext}"
            else:
                ctx.files[k] = ctx.workpath / ext

    def cleanup_calc(self, ctx: RunContext):
        """Remove the work path if required"""
        super().cleanup_calc(ctx)

        if ctx.scratch.get("old_path", None):
            os.chdir(ctx.scratch["old_path"])

        # Start from a clean slate in case the driver is sloppy
        ctx.close_files()

        # Handle file storage
        policy = self.opts.save_files_policy
        if policy == FilesPolicy.NEVER:
            ...
        elif policy == FilesPolicy.ON_FAIL and ctx.record.status != RecordStatus.FAILED:
            ...
        else: # Always or failed calculations
            ctx.record.meta["files"] = {}
            for f, p in ctx.files.items():
                if not p.exists():
                    continue
                with p.open("r") as file:
                    ctx.record.meta["files"][f] = file.read()

        # Remove the work path
        if self.opts.remove_files:
            rmtree(ctx.workpath)
        else:
            ctx.record.meta["work_path"] = str(ctx.workpath.absolute())

    def sources_from_ctx(self, ctx: RunContext) -> List[Any]:
        """Adds open files to the run context"""
        sources = super().sources_from_ctx(ctx)
        ctx.close_files()  # Start from a clean slate

        # Open the run context and add it's file to list of sources
        for tag in self.EXTRACTABLE_FILES:
            if ctx.files[tag].exists():
                sources.append(ctx.open_file(tag))
        return sources

####################################################################################
#         TEMPLATE FILE MIXIN
####################################################################################

DEFAULT_TEMPLATE = """\
{name}: n_atoms={num_atoms}

{charge} {mult}
{geometry}
"""

class TemplateMixinOptions(FileMixinOptions):
    """TemplateOptionsMixin

    Options for template-base QM codes. If `tempalte_file` is specified, it overrides
    the template option. The template file is not saved to the database

    By the end of the validation process, only ref:`template` should be set.

    This code will check the `template_file` followed by the `default_template`.
    After initialization, the default template will be set to None
    """
    template: str = DEFAULT_TEMPLATE

    @field_validator('template')
    @classmethod
    def name_must_contain_space(cls, template: str | None) -> str:
        # Make assumptions about the max file path length
        if len(template) > 150:
            return template

        template_path = Path(template)
        if template_path.exists():
            with template_path.open("r") as f:
                return f.read()

        return template

class TemplateMixin(FileMixin):
    Options = TemplateMixinOptions

    ATOM_TEMPLATE = " {symbol} {x: .8f} {y: .8f} {z: .8f}"
    GHOST_ATOM_TEMPLATE = "@{symbol} {x: .8f} {y: .8f} {z: .8f}"

    # Automatically write the template tho this file
    AUTOWRITE_FILE = "input"

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        # Make sure the autowrite file is in the file manifest
        if cls.AUTOWRITE_FILE not in cls.FILE_MANIFEST:
            cls.FILE_MANIFEST[cls.AUTOWRITE_FILE] = ".inp"


    def get_template_tags(self, ctx: RunContext) -> Dict[str, str]:
        """Creates dictionary of template tags for system"""
        system = ctx.record.system
        tags = {
            # General info
            "time": datetime.now().isoformat(),
            "driver_name": self.name,

            # System information
            "name": system.name,
            "system_id": system._saved,
            "charge": int(system.charge),
            "mult": system.multiplicity,
            "num_atoms": system.size,
            "geometry": self.system_to_str(ctx),

            # Allocation information
            "cpus": self.allocation.cpus,
            "total_memory": self.allocation.memory,
            "memory_per_cpu": int(self.allocation.memory / self.allocation.cpus),
        }

        # Handle periodic systems
        if system.unit_cell is not None:
            tags.update(
                cell_a = system.unit_cell[0],
                cell_b = system.unit_cell[1],
                cell_c = system.unit_cell[2],
            )

        # No good way to do this with the mixin model
        # Do this for the static mixin
        if hasattr(self, "static_path"):
            tags["static_path"] = self.static_path
        return tags


    def setup_calc(self, ctx: RunContext) -> None:
        """Write template to input file if requested"""
        super().setup_calc(ctx)
        if self.AUTOWRITE_FILE is not None:
            self.write_template(ctx, self.AUTOWRITE_FILE)


    def write_template(self, ctx: RunContext, file: str, template: str | None = None) -> None:
        """Write the template to the given context file"""
        with ctx.files[file].open("w") as f:
            f.write(self.ctx_to_str(ctx, template=template))


    def ctx_to_str(self, ctx: RunContext, template: str | None = None) -> str:
        """Return string for a given template. Helpful for testing"""
        # Allow user-defined template
        if template is None:
            template  = self.opts.template
        return template.format(**self.get_template_tags(ctx))


    def system_to_str(self, ctx: RunContext) -> str:
        """Creates a template string for the system"""
        system = ctx.record.system
        atom_strs = [self.atom_to_str(a) for a in system]
        return "\n".join(atom_s for atom_s in atom_strs if atom_s is not None)


    def atom_to_str(self, a: BoundAtom) -> str | None:
        """Converts atoms to string while templating"""
        if a.is_physical:
            template = self.ATOM_TEMPLATE
        else:
            template = self.GHOST_ATOM_TEMPLATE
        if template is None:
            return
        return template.format(symbol=a.t, x=a.r[0], y=a.r[1], z=a.r[2])

####################################################################################
#         STATIC FILE MIXIN
####################################################################################
class StaticFileMixinOptions(FileMixinOptions):
    """Creates static files which can be shared between all calculations done with
    this driver.

    This mixin should be used if the driver need basis, potential, or other supporting
    file.
    """
    static_files: Dict[str, str] = Field(default_factory=dict)

    @field_validator('static_files')
    @classmethod
    def files_validator(cls, static_files: List[str] | Dict[str, str]) -> Dict[str, str]:
        """Reads and converts static files into dictionaries"""
        if isinstance(static_files, dict):
            return static_files

        static_files_dict = {}
        for fp in static_files:
            fp = Path(fp)
            with fp.open("r") as f:
                static_files_dict[fp.name] = f.read()
        return static_files_dict


class StaticFileMixin(FileMixin):
    """Adds a static folder to the basepath of the driver's ResourceAllocation

    Note that static files are added to `STATIC_FILE/file_name`. Nested structures are
    not allowed
    """
    Options = StaticFileMixinOptions

    static_path: Path

    def configure(self) -> None:
        super().configure()

        # Make static files!
        static_files = self.opts.static_files
        self.static_path = self.allocation.basepath / "STATIC"
        self.static_path.mkdir()
        for fname, fdata in static_files.items():
            with (self.static_path / fname).open("w") as f:
                f.write(fdata)

    # Cleanup is taken care of with ResourceAllocation.cleanup

####################################################################################
#         SHELL FILE MIXIN
####################################################################################

class ShellCommandDriverOptions(FileMixinOptions):
    exe: str = "" # Absolute executable path


class ShellCommandMixin(FileMixin):
    Options = ShellCommandDriverOptions

    FILE_MANIFEST = {"input": ".inp", "output": ".out", "log": ".log"}
    EXTRACTABLE_FILES = ("output",)
    STDOUT_FILE: str = "log"
    STDERR_FILE: str = "log"
    AVAILABLE_RETURN_CODE: ClassVar[int] = 0

    @classmethod
    def is_available(cls):
        result = subprocess.run(["which", cls.Options.exe], text=True, capture_output=True)
        return result.returncode == cls.AVAILABLE_RETURN_CODE

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if "log" not in cls.FILE_MANIFEST:
            if cls.STDOUT_FILE == "log" or cls.STDERR_FILE == "log":
                cls.FILE_MANIFEST["log"] = ".log"

        # Error check that the output files are in the manifest
        for f in cls.EXTRACTABLE_FILES:
            if f not in cls.FILE_MANIFEST:
                raise ConfigurationError(
                    f"The extractible file {f} is not in the FILE_MANIFEST"
                )


    def get_run_cmd(self, ctx: RunContext) -> Tuple[str, List[str]]:
        """
        Returns the command-line program required to run an external
        """
        raise NotImplementedError("The backend should implement this function")

    def run_calc(self, ctx: RunContext):
        """Execute the shell command"""
        cmd, args = self.get_run_cmd(ctx)

        ctx.record.start_time = datetime.now()
        proc = subprocess.Popen(
            [cmd] + args,
            stdout=ctx.open_file(self.STDOUT_FILE, "w"),
            stderr=ctx.open_file(self.STDERR_FILE, "w"),
            env=self.get_run_env(ctx)
        )
        ctx.scratch["proc"] = proc
        proc.wait()
        ctx.record.end_time = datetime.now()
        ctx.close_files()

    def determine_success(self, ctx: RunContext):
        """
        Raise exception if the QM Job failed
        """
        try:
            proc: subprocess.Popen = ctx.scratch["proc"]
        except KeyError:
            raise BackendRunException("The executable was never called.")
        if proc.returncode is None:
            raise BackendRunException("Calculation is still running")
        if proc.returncode != 0:
            raise ProcessFailed("Process returned a non-zero exit code")

        # Check that the output files exist
        for f in self.EXTRACTABLE_FILES:
            if not ctx.files[f].exists():
                raise NoOutputFile(f"Missing the '{f}' output file")

        super().determine_success(ctx)

# Alias for backwards compatibility
class ShellCommandDriver(ShellCommandMixin, TemplateMixin):
    """Compatibility class for older drivers.

    .. WARNING ::
        This class is depricated
    """

    class Options(ShellCommandDriverOptions, TemplateMixinOptions):
        ...
