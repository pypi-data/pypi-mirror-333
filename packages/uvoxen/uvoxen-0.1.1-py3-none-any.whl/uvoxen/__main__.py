# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Generate test configuration files, run tests."""

from __future__ import annotations

import dataclasses
import sys
import typing

import click

from . import defs
from . import parse
from . import util
from .run import base
from .run import req
from .run import tox
from .run import uv


if typing.TYPE_CHECKING:
    from typing import Final


PY_SUPPORTED: Final = "supported"
"""The magic Python version meaning "run for all supported Python versions"."""


@dataclasses.dataclass
class ConfigHolder:
    """Hold a `Config` object."""

    cfg: defs.Config | None = None
    """The `Config` object stashed by the main function."""


def extract_cfg(ctx: click.Context) -> defs.Config:
    """Extract the `Config` object that the main function built."""
    cfg_hold: Final = ctx.find_object(ConfigHolder)
    if cfg_hold is None:
        sys.exit("Internal error: no click config holder object")

    cfg: Final = cfg_hold.cfg
    if cfg is None:
        sys.exit("Internal error: no config in the click config holder")

    return cfg


def arg_features(_ctx: click.Context, _self: click.Parameter, value: bool) -> bool:  # noqa: FBT001
    """Display program features information and exit."""
    if not value:
        return value

    print("Features: " + " ".join(f"{name}={value}" for name, value in defs.FEATURES.items()))
    sys.exit(0)


@click.command(name="envs")
@click.pass_context
def cmd_list_envs(ctx: click.Context) -> None:
    """List the defined test environments."""
    try:
        cfg: Final = extract_cfg(ctx)
        proj: Final = parse.pyproject(cfg)
        print("\n".join(name for name in sorted(proj.env)))
    except defs.Error as err:
        sys.exit(f"Could not list the test environments: {err}")


@click.command(name="pythons")
@click.pass_context
def cmd_list_pythons(ctx: click.Context) -> None:
    """List the supported Python versions."""
    try:
        cfg: Final = extract_cfg(ctx)
        proj: Final = parse.pyproject(cfg)
        print("\n".join(proj.python_supported))
    except defs.Error as err:
        sys.exit(f"Could not list the supported Python versions: {err}")


@click.command(name="reqs")
@click.pass_context
def cmd_list_reqs(ctx: click.Context) -> None:
    """List the defined dependency groups."""
    try:
        cfg: Final = extract_cfg(ctx)
        proj: Final = parse.pyproject(cfg)
        print("\n".join(sorted(proj.python_dependency_groups)))
    except defs.Error as err:
        sys.exit(f"Could not list the project dependency groups: {err}")


@click.group(name="list")
@click.pass_context
def cmd_list(ctx: click.Context) -> None:
    """List various configuration settings."""


cmd_list.add_command(cmd_list_envs)
cmd_list.add_command(cmd_list_pythons)
cmd_list.add_command(cmd_list_reqs)


@click.command(name="generate")
@click.option("--check", is_flag=True, help="check whether the file is up to date")
@click.option(
    "--group",
    "-g",
    type=str,
    required=True,
    help="the dependency group to generate the requirements file for",
)
@click.option("--diff", is_flag=True, help="in check mode, display a diff")
@click.option("--force", "-f", is_flag=True, help="only write the file out if it has changed")
@click.option("--noop", "-N", is_flag=True, help="no-operation mode; display what would be done")
@click.option(
    "--output",
    "-o",
    type=str,
    help="the name of the file to write to, or '-' for standard output",
)
@click.pass_context
def cmd_req_generate(  # noqa: PLR0913  # this function does many things
    ctx: click.Context,
    *,
    check: bool,
    diff: bool,
    force: bool,
    group: str,
    noop: bool,
    output: str | None,
) -> None:
    """Generate the `requirements/groupname.txt` file."""
    try:
        cfg: Final = extract_cfg(ctx)
        proj: Final = parse.pyproject(cfg)

        runner = req.ReqRunner(cfg=cfg, proj=proj, posargs=[], group=group)
        runner.generate(check=check, diff=diff, force=force, noop=noop, output=output)
    except base.NeedsRegeneratingError as err:
        sys.exit(str(err))
    except defs.Error as err:
        sys.exit(f"Could not generate the requirements file: {err}")


@click.group(name="req")
@click.pass_context
def cmd_req(ctx: click.Context) -> None:
    """Export dependency groups as requirement text files."""


cmd_req.add_command(cmd_req_generate)


@click.command(name="generate")
@click.option("--check", is_flag=True, help="check whether the file is up to date")
@click.option("--diff", is_flag=True, help="in check mode, display a diff")
@click.option("--force", "-f", is_flag=True, help="only write the file out if it has changed")
@click.option("--noop", "-N", is_flag=True, help="no-operation mode; display what would be done")
@click.option(
    "--output",
    "-o",
    type=str,
    default="tox.ini",
    help="the name of the file to write to, or '-' for standard output",
)
@click.pass_context
def cmd_tox_generate(  # noqa: PLR0913  # this function does many things
    ctx: click.Context,
    *,
    check: bool,
    diff: bool,
    force: bool,
    noop: bool,
    output: str,
) -> None:
    """Generate the `tox.ini` file."""
    try:
        cfg: Final = extract_cfg(ctx)
        proj: Final = parse.pyproject(cfg)

        if cfg.python is None:
            cfg.log.info("Generating tox.ini using the default Python version")
        else:
            cfg.log.info("Generating tox.ini using  Python %(pyver)s", {"pyver": cfg.python})

        runner = tox.ToxRunner(cfg=cfg, proj=proj, posargs=[])
        runner.generate(check=check, diff=diff, force=force, noop=noop, output=output)
    except base.NeedsRegeneratingError as err:
        sys.exit(str(err))
    except defs.Error as err:
        sys.exit(f"Could not generate the Tox configuration: {err}")


@click.command(name="run")
@click.option("--env", "-e", type=str, help="the environments to run commands for")
@click.option("--force", "-f", is_flag=True, help="always write the tox.ini file out")
@click.option("--noop", "-N", is_flag=True, help="no-operation mode; display what would be done")
@click.argument("posargs", type=str, required=False, nargs=-1)
@click.pass_context
def cmd_tox_run(
    ctx: click.Context,
    *,
    env: str,
    force: bool,
    noop: bool,
    posargs: tuple[str],
) -> None:
    """Run test environments using Tox."""
    try:
        cfg: Final = extract_cfg(ctx)
        proj: Final = parse.pyproject(cfg)
        posargs_list: Final = list(posargs)

        py_versions: Final = [cfg.python] if cfg.python != PY_SUPPORTED else proj.python_supported
        for pyver in py_versions:
            if pyver is None:
                cfg.log.info("Running the tests for the default Python version")
            else:
                cfg.log.info("Running the tests for Python %(pyver)s", {"pyver": pyver})

            runner = tox.ToxRunner(
                cfg=dataclasses.replace(cfg, python=pyver),
                proj=proj,
                posargs=posargs_list,
            )
            runner.generate(check=False, diff=False, force=force, noop=noop)
            runner.run(envs=env.split(",") if env is not None else [], noop=noop)
    except defs.Error as err:
        sys.exit(f"Could not run the tests using Tox: {err}")


@click.group(name="tox")
@click.pass_context
def cmd_tox(ctx: click.Context) -> None:
    """Generate the `tox.ini` file and run tests using Tox."""


cmd_tox.add_command(cmd_tox_generate)
cmd_tox.add_command(cmd_tox_run)


@click.command(name="run")
@click.option("--env", "-e", type=str, help="the environments to run commands for")
@click.option("--force", "-f", is_flag=True, help="unused for `uv`")
@click.option("--noop", "-N", is_flag=True, help="no-operation mode; display what would be done")
@click.option("--resolution", type=str, help="the resolution mode to pass to `uv sync`")
@click.argument("posargs", type=str, required=False, nargs=-1)
@click.pass_context
def cmd_uv_run(  # noqa: PLR0913  # this function does many things
    ctx: click.Context,
    *,
    env: str,
    force: bool,
    noop: bool,
    resolution: str | None,
    posargs: tuple[str],
) -> None:
    """Run tests using the uv tool."""
    try:
        cfg: Final = extract_cfg(ctx)
        proj: Final = parse.pyproject(cfg)
        posargs_list: Final = list(posargs)

        py_versions: Final = [cfg.python] if cfg.python != PY_SUPPORTED else proj.python_supported
        for pyver in py_versions:
            if pyver is None:
                cfg.log.info("Running the tests for the default Python version")
            else:
                cfg.log.info("Running the tests for Python %(pyver)s", {"pyver": pyver})

            runner = uv.UvRunner(
                cfg=dataclasses.replace(cfg, python=pyver),
                proj=proj,
                posargs=posargs_list,
                resolution=resolution,
            )
            runner.generate(check=False, diff=False, force=force, noop=noop)
            runner.run(envs=env.split(",") if env is not None else proj.envlist, noop=noop)
    except defs.Error as err:
        sys.exit(f"Could not run the tests using uv: {err}")


@click.group(name="uv")
@click.pass_context
def cmd_uv(ctx: click.Context) -> None:
    """Run tests using the uv tool."""


cmd_uv.add_command(cmd_uv_run)


@click.group(name="uvoxen")
@click.option(
    "--features",
    is_flag=True,
    is_eager=True,
    callback=arg_features,
    help="display program features information and exit",
)
@click.option(
    "--python",
    "-p",
    type=str,
    help=f"the Python version to use, or '{PY_SUPPORTED}' for all",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="quiet operation; only display warning and error messages",
)
@click.option("--verbose", "-v", is_flag=True, help="verbose operation; display diagnostic output")
@click.pass_context
def main(
    ctx: click.Context,
    *,
    features: bool,
    python: str | None,
    quiet: bool,
    verbose: bool,
) -> None:
    """Generate test configuration files and run tests."""
    if features:
        sys.exit("Internal error: how did we get to main() with features=True?")

    ctx.ensure_object(ConfigHolder)
    ctx.obj.cfg = defs.Config(
        log=util.build_logger(quiet=quiet, verbose=verbose),
        python=python,
        verbose=verbose,
    )


main.add_command(cmd_list)
main.add_command(cmd_req)
main.add_command(cmd_tox)
main.add_command(cmd_uv)


if __name__ == "__main__":
    main()
