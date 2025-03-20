# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Parse the pyproject.toml configuration."""

from __future__ import annotations

import dataclasses
import functools
import pathlib
import re
import tomllib
import typing

import mashumaro
from mashumaro import codecs as m_codecs
from mashumaro import config as m_config

from . import defs


if typing.TYPE_CHECKING:
    from typing import Any, Final


@dataclasses.dataclass
class ParseError(defs.Error):
    """An error that occurred while parsing the `pyproject.toml` configuration."""

    def __str__(self) -> str:
        """Provide a human-readable error message."""
        return f"Error parsing `pyproject.toml`: {self!r}"


@dataclasses.dataclass
class ProjMissingError(ParseError):
    """Missing values in the `pyproject.toml` file."""

    path: str
    """The missing value."""

    def __str__(self) -> str:
        """Provide a human-readable error message."""
        return f"Missing {self.path} in pyproject.toml"


@dataclasses.dataclass
class ProjWrongTypeError(ParseError):
    """Wrong type for a `pyproject.toml` value."""

    path: str
    """The wrong value."""

    exp_type: str
    """The expected type for the value."""

    def __str__(self) -> str:
        """Provide a human-readable error message."""
        return f"Expected the {self.path} pyproject.toml value to be a {self.exp_type}"


@dataclasses.dataclass
class ProjFormatVersionUnsupportedError(ParseError):
    """Unsupported format version in the `pyproject.toml` file."""

    major: int
    """The major version number from the file."""

    minor: int
    """The minor version number from the file."""

    def __str__(self) -> str:
        """Provide a human-readable error message."""
        return f"Unsupported uvoxen format version {self.major}.{self.minor} in pyproject.toml"


@dataclasses.dataclass
class ProjDeserializeError(ParseError):
    """Could not deserialize the `uvoxen` configuration in the `pyproject.toml` file."""

    err: Exception
    """The error that occurred."""

    def __str__(self) -> str:
        """Provide a human-readable error message."""
        return f"Could not parse the tool.uvoxen pyproject.toml section: {self.err}"


RE_LINE_VARS: Final = re.compile(
    r"""
        \{
            \[ (?P<section> [A-Za-z0-9_]+ ) \]
            (?P<name> [A-Za-z0-9_]+ )
        \}
    """,
    re.X,
)

RE_PY_SUPPORTED: Final = re.compile(
    r"""
        ^
        Programming \s Language \s :: \s Python \s :: \s
        (?P<version>
          3\.
          (?: 0 | [1-9][0-9]* )
        )
        $
    """,
    re.X,
)


@dataclasses.dataclass(frozen=True)
class PyDependencyGroupItem:
    """The base class for a single item in a dependency group."""


@dataclasses.dataclass(frozen=True)
class PyDependencyGroupItemReq(PyDependencyGroupItem):
    """A requirement specification within a dependency group."""

    req: str
    """The requirement string."""


@dataclasses.dataclass(frozen=True)
class PyDependencyGroupIncluded(PyDependencyGroupItem):
    """The name of another dependency group to be included herewith."""

    group: str
    """The name of the other dependency group."""


@dataclasses.dataclass(frozen=True)
class Environment(mashumaro.DataClassDictMixin):
    """A single test environment."""

    commands: list[str]
    """The commands to run for this test environment."""

    dependency_groups: list[str] = dataclasses.field(
        default_factory=list,
        metadata=mashumaro.field_options(alias="dependency-groups"),
    )
    """The list of Python package groups to install in this environment."""

    install_dependencies: bool = dataclasses.field(
        default=False,
        metadata=mashumaro.field_options(alias="install-dependencies"),
    )
    """Whether to install the project dependencies."""

    install_project: bool = dataclasses.field(
        default=False,
        metadata=mashumaro.field_options(alias="install-project"),
    )
    """Whether to install the project itself along with its dependencies."""

    allowlist_externals: list[str] | None = dataclasses.field(
        default=None,
        metadata=mashumaro.field_options(alias="allowlist-externals"),
    )
    """The external commands to allow Tox to run."""

    setenv: dict[str, str] = dataclasses.field(default_factory=dict)
    """Additional environment variables to set."""

    passenv: list[str] = dataclasses.field(default_factory=list)
    """Environment variables to pass from the parent process environment."""

    tags: list[str] | None = None
    """The tags for ordering the environments into stages."""

    class Config(m_config.BaseConfig):
        """Make sure the parser fails on extraneous keys."""

        forbid_extra_keys = True


@dataclasses.dataclass(frozen=True)
class ToxSettings(mashumaro.DataClassDictMixin):
    """Tox-specific settings."""

    envlist_append: list[str] | None = dataclasses.field(
        default=None,
        metadata=mashumaro.field_options(alias="envlist-append"),
    )
    """Additional entries to add to `tox.envlist`."""

    env_order: list[str] | None = dataclasses.field(
        default=None,
        metadata=mashumaro.field_options(alias="env-order"),
    )
    """The order in which the environments should appear in the Tox configuration."""

    footer: str = ""
    """Text to place at the bottom of the file."""

    header: str = ""
    """Text to place at the top of the file."""

    class Config(m_config.BaseConfig):
        """Make sure the parser fails on extraneous keys."""

        forbid_extra_keys = True


@dataclasses.dataclass(frozen=True)
class ReqSettings(mashumaro.DataClassDictMixin):
    """Requirements-specific settings."""

    footer: str = ""
    """Text to place at the bottom of the file."""

    header: str = ""
    """Text to place at the top of the file."""

    class Config(m_config.BaseConfig):
        """Make sure the parser fails on extraneous keys."""

        forbid_extra_keys = True


@dataclasses.dataclass(frozen=True)
class ProjectParsed(mashumaro.DataClassDictMixin):
    """A set of test environments and definitions."""

    env: dict[str, Environment]
    """The actual test environments defined."""

    envlist: list[str]
    """The list of environments to run by default."""

    build_project: bool = dataclasses.field(
        default=True,
        metadata=mashumaro.field_options(alias="build-project"),
    )
    """Whether to build the Python project at all, or merely run tests."""

    defs: dict[str, str | list[str]] = dataclasses.field(default_factory=dict)
    """The variables to expand within the commands and the test configuration."""

    req: ReqSettings | None = None
    """Requirements-specific settings, if any."""

    tox: ToxSettings | None = None
    """Tox-specific settings, if any."""

    class Config(m_config.BaseConfig):
        """Make sure the parser fails on extraneous keys."""

        forbid_extra_keys = True


@dataclasses.dataclass(frozen=True)
class ProjectParsedV0dot1(mashumaro.DataClassDictMixin):
    """A set of test environments and definitions."""

    env: dict[str, Environment]
    """The actual test environments defined."""

    envlist: list[str]
    """The list of environments to run by default."""

    defs: dict[str, str | list[str]] = dataclasses.field(default_factory=dict)
    """The variables to expand within the commands and the test configuration."""

    req: ReqSettings | None = None
    """Requirements-specific settings, if any."""

    tox: ToxSettings | None = None
    """Tox-specific settings, if any."""

    class Config(m_config.BaseConfig):
        """Make sure the parser fails on extraneous keys."""

        forbid_extra_keys = True

    def upgrade_to_latest(self) -> ProjectParsed:
        """Upgrade the parsed configuration to the latest format."""
        return ProjectParsed(
            env=self.env,
            envlist=self.envlist,
            build_project=True,
            defs=self.defs,
            req=self.req,
            tox=self.tox,
        )


@dataclasses.dataclass(frozen=True)
class Project:
    """A set of test environments and definitions."""

    build_project: bool
    """Whether to build the Python project at all, or merely run tests."""

    defs: dict[str, str | list[str]]
    """The variables to expand within the commands and the test configuration."""

    env: dict[str, Environment]
    """The actual test environments defined."""

    envlist: list[str]
    """The list of environments to run by default."""

    python_dependency_groups: dict[str, list[PyDependencyGroupItem]]
    """The `dependency-groups` section of the `pyproject.toml` file."""

    python_supported: list[str]
    """The list of supported Python versions as declared in `pyproject.toml` trove classifiers."""

    req: ReqSettings | None = None
    """Requirements-specific settings, if any."""

    tox: ToxSettings | None = None
    """Tox-specific settings, if any."""


def _parse_dep_group(name: str, items: Any) -> list[PyDependencyGroupItem]:  # noqa: ANN401
    """Parse the list of items within a `pyproject.toml` dependency group."""
    if not isinstance(items, list):
        raise ProjWrongTypeError(f"dependency-groups.{name}", "table")  # noqa: EM102

    def single(item: Any) -> PyDependencyGroupItem:  # noqa: ANN401
        """Parse a single item within a dependency group."""
        match item:
            case str(item_req):
                return PyDependencyGroupItemReq(item_req)

            case dict(item_dict):
                included: Final = item_dict.get("include-group")
                match included:
                    case None:
                        raise ProjMissingError(
                            f"dependency-groups.{name}.{{include-group}}",  # noqa: EM102
                        )

                    case str(included_group):
                        return PyDependencyGroupIncluded(included_group)

                    case _:
                        raise ProjWrongTypeError(
                            f"dependency-group.{name}.{{item}}",  # noqa: EM102
                            "include-group",
                        )

            case _:
                raise ProjWrongTypeError(
                    f"dependency-group.{name}.item",  # noqa: EM102
                    "string or table",
                )

    return [single(item) for item in items]


@functools.lru_cache
def _pyproject_loader() -> m_codecs.BasicDecoder[ProjectParsed]:
    """Instantiate a typed loader that will parse the `tool.uvoxen` pyproject section."""
    return m_codecs.BasicDecoder(ProjectParsed)


@functools.lru_cache
def _pyproject_loader_v0dot1() -> m_codecs.BasicDecoder[ProjectParsedV0dot1]:
    """Instantiate a typed loader that will parse the `tool.uvoxen` pyproject section."""
    return m_codecs.BasicDecoder(ProjectParsedV0dot1)


def _pyproject_load(proj_tool: dict[str, Any]) -> ProjectParsed:
    """Parse the [tool.uvoxen] section according to its .format.version field."""
    try:
        ver_major: Final = proj_tool["format"]["version"]["major"]
        ver_minor: Final = proj_tool["format"]["version"]["minor"]
    except (KeyError, TypeError) as err:
        raise ProjMissingError("tool.uvoxen.version.{major,minor}") from err  # noqa: EM101
    if not isinstance(ver_major, int) or not isinstance(ver_minor, int):
        raise ProjWrongTypeError("tool.uvoxen.version.{major,minor}", "integer")  # noqa: EM101

    del proj_tool["format"]
    try:
        match ver_major, ver_minor:
            case 0, 1:
                return _pyproject_loader_v0dot1().decode(proj_tool).upgrade_to_latest()

            case 0, _:
                return _pyproject_loader().decode(proj_tool)

            case _:
                raise ProjFormatVersionUnsupportedError(ver_major, ver_minor)
    except ValueError as err:
        raise ProjDeserializeError(err) from err


def pyproject(cfg: defs.Config) -> Project:
    """Parse the pyproject.toml configuration."""
    cfg.log.debug("Parsing the pyproject.toml file")
    with pathlib.Path("pyproject.toml").open(mode="rb") as proj_file:
        proj: Final = tomllib.load(proj_file)
    try:
        proj_tool: Final = proj["tool"]["uvoxen"]
    except (KeyError, TypeError) as err:
        raise ProjMissingError("tool.uvoxen") from err  # noqa: EM101

    parsed: Final = _pyproject_load(proj_tool)

    try:
        classifiers: Final = proj["project"]["classifiers"]
    except (KeyError, TypeError) as err:
        raise ProjMissingError("project.classifiers") from err  # noqa: EM101
    if not isinstance(classifiers, list):
        raise ProjWrongTypeError("project.classifiers", "list")  # noqa: EM101
    python_supported: Final = [
        found.group("version")
        for found in (RE_PY_SUPPORTED.match(line) for line in classifiers)
        if found
    ]

    dep_groups: Final = proj.get("dependency-groups")
    match dep_groups:
        case None:
            python_dependency_groups = {}

        case dict(groups):
            python_dependency_groups = {
                name: _parse_dep_group(name, dep_group) for (name, dep_group) in groups.items()
            }

        case _:
            raise ProjWrongTypeError("dependency-groups", "table")  # noqa: EM101

    return Project(
        build_project=parsed.build_project,
        defs=parsed.defs,
        env=parsed.env,
        envlist=parsed.envlist,
        python_dependency_groups=python_dependency_groups,
        python_supported=python_supported,
        req=parsed.req,
        tox=parsed.tox,
    )
