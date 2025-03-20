# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Common definitions for the docker-scry library."""

from __future__ import annotations

import dataclasses
import typing


if typing.TYPE_CHECKING:
    import logging
    from typing import Final


VERSION: Final = "0.1.0"
"""The docker-scry library version, semver-like."""


FEATURES: Final = {
    "docker-scry": VERSION,
    "pgrep": "0.1",
}
"""The list of features supported by the docker-scry library."""


@dataclasses.dataclass(frozen=True)
class Config:
    """Runtime configuration for the docker-scry library."""

    log: logging.Logger
    """The logger to send diagnostic, informational, and error messages to."""

    utf8_env: dict[str, str]
    """The UTF-8-capable environment to run child processes in."""

    verbose: bool
    """Verbose operation; display diagnostic output."""


@dataclasses.dataclass(frozen=True)
class PGrepConfig(Config):
    """Runtime configuration for the `docker-scry pgrep` subcommand."""

    cid: str
    """The container to examine."""

    force: bool
    """Skip the /proc/.../ns/pid access rights check."""

    pgrep_args: list[str]
    """Additional arguments to pass to `pgrep`, if any."""


@dataclasses.dataclass(frozen=True)
class Container:
    """The attributes of a Docker container that we care about."""

    cid: str
    """The container ID."""

    pid: int
    """The main process's ID."""


@dataclasses.dataclass
class Error(Exception):
    """Base class for an error that occurred during the program's operation."""

    def __str__(self) -> str:
        """Provide a human-readable description of the error."""
        return f"Could not examine the container or its processes: {self!r}"


@dataclasses.dataclass
class NoMatchError(Error):
    """Base class for "no such container", "no such process", etc. errors."""

    def __str__(self) -> str:
        """Provide a human-readable description of the error."""
        return f"Could not find the specified object: {self!r}"
