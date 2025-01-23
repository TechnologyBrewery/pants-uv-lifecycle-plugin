from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Iterator, List
from pathlib import Path
from pants.engine.env_vars import EnvironmentVars, EnvironmentVarsRequest
from pants.engine.target import Target, AllTargets, SourcesField
from pants.engine.rules import collect_rules, Get, rule
from pants.core.util_rules.source_files import SourceFilesRequest, SourceFiles
import logging

logger = logging.getLogger("rule_utils_logger")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")


@dataclass(frozen=True)
class PathEnvVariableRequest:
    """A request class to retrieve the PATH environment variable."""


@rule
async def get_path_env_variable(_: PathEnvVariableRequest) -> EnvironmentVars:
    return await Get(EnvironmentVars, EnvironmentVarsRequest(["PATH"]))


@dataclass(frozen=True)
class PyprojectTomlFileTargets:
    """A wrapper type to return a collection of targets from a rule."""

    targets: Tuple[Target, ...]

    def __iter__(self) -> Iterator[Target]:
        return iter(self.targets)


@rule
async def get_pyproject_file_targets(
    all_targets: AllTargets,
) -> PyprojectTomlFileTargets:
    pyproject_toml_targets = [
        target
        for target in all_targets
        if target.address.target_name == "pyproject_toml_files"
    ]
    return PyprojectTomlFileTargets(tuple(pyproject_toml_targets))


@dataclass(frozen=True)
class PyprojectTomlFilepaths:
    """A wrapper type to return a collection of filepaths from a rule."""

    paths: Tuple[str, ...]

    def __iter__(self) -> Iterator[str]:
        return iter(self.paths)


@rule
async def get_pyproject_toml_filepaths(
    py_targets: PyprojectTomlFileTargets,
) -> PyprojectTomlFilepaths:
    pyproject_toml_filepaths: List[str] = []

    for target in py_targets:
        sources_field = target[SourcesField]
        source_files = await Get(SourceFiles, SourceFilesRequest([sources_field]))

        # Request the Snapshot of the source files for this target
        snapshot = source_files.snapshot

        # snapshot.files is a tuple of the full file paths
        pyproject_toml_filepaths.extend(snapshot.files)

    return PyprojectTomlFilepaths(paths=tuple(pyproject_toml_filepaths))


@dataclass(frozen=True)
class PyprojectTomlDirs:
    """A wrapper type to return a collection of directories from a rule."""

    paths: Tuple[str, ...]

    def __iter__(self) -> Iterator[str]:
        return iter(self.paths)


@rule
async def get_pyproject_toml_dirs(
    py_targets: PyprojectTomlFileTargets,
) -> PyprojectTomlDirs:
    pyproject_toml_dirs: List[str] = []

    for target in py_targets:
        sources_field = target[SourcesField]
        source_files = await Get(SourceFiles, SourceFilesRequest([sources_field]))
        snapshot = source_files.snapshot

        for filepath in snapshot.files:
            pyproject_toml_dirs.append(str(Path(filepath).parent))

    return PyprojectTomlDirs(paths=tuple(pyproject_toml_dirs))


### behave feature files
@dataclass(frozen=True)
class FeatureFileTargets:
    """A wrapper type to return a collection of targets from a rule."""

    targets: Tuple[Target, ...]

    def __iter__(self) -> Iterator[Target]:
        return iter(self.targets)


@rule
async def get_feature_file_targets(
    all_targets: AllTargets,
) -> FeatureFileTargets:
    feature_file_targets = [
        target
        for target in all_targets
        if target.address.target_name == "feature_files"
    ]
    return FeatureFileTargets(tuple(feature_file_targets))


@dataclass(frozen=True)
class FeatureFilepaths:
    """A wrapper type to return a collection of filepaths from a rule."""

    paths: Tuple[str, ...]

    def __iter__(self) -> Iterator[str]:
        return iter(self.paths)


@rule
async def get_feature_filepaths(
    feature_file_targets: FeatureFileTargets,
) -> FeatureFilepaths:
    feature_filepaths: List[str] = []

    for target in feature_file_targets:
        sources_field = target[SourcesField]
        source_files = await Get(SourceFiles, SourceFilesRequest([sources_field]))

        # Request the Snapshot of the source files for this target
        snapshot = source_files.snapshot

        # snapshot.files is a tuple of the full file paths
        feature_filepaths.extend(snapshot.files)

    return FeatureFilepaths(paths=tuple(feature_filepaths))


def rules():
    return collect_rules()
