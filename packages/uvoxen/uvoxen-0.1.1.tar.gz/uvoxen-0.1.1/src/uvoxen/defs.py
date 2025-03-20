# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Common definitions for the uvoxen library."""

from __future__ import annotations

import dataclasses
import typing


if typing.TYPE_CHECKING:
    import logging
    from typing import Final


VERSION: Final = "0.1.1"
"""The uvoxen library version, semver-like."""


FEATURES: Final = {
    "uvoxen": VERSION,
    "format-min": "0.1",
    "format-current": "0.2",
    "req-generate": "0.1",
    "tox-expand-vars": "0.1",
    "tox-generate": "0.2",
    "tox-run": "0.1",
    "uv-generate": "0.1",
    "uv-run": "0.2",
}
"""The list of features supported by the uvoxen library."""


@dataclasses.dataclass
class Error(Exception):
    """An error that occurred while processing the test settings."""

    def __str__(self) -> str:
        """Provide a human-readable error message."""
        return f"uvoxen error: {self!r}"


@dataclasses.dataclass(frozen=True)
class Config:
    """Runtime configuration for the uvoxen library."""

    log: logging.Logger
    """The logger to send diagnostic, informational, and error messages to."""

    python: str | None
    """The Python version to use."""

    verbose: bool
    """Verbose operation; display diagnostic output."""
