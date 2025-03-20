# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Examine the container."""

from __future__ import annotations

import dataclasses
import json
import pathlib
import shlex
import subprocess  # noqa: S404
import typing

from . import defs


if typing.TYPE_CHECKING:
    from typing import Final


@dataclasses.dataclass
class ScryError(defs.Error):
    """An error that occurred while scrying."""

    cid: str
    """The container ID that we tried to scry."""

    def __str__(self) -> str:
        """Provide a human-readable description of the error."""
        return f"Could not scry into the {self.cid} container: {self!r}"


@dataclasses.dataclass
class ContainerNoMatchError(ScryError, defs.NoMatchError):
    """The `docker inspect` invocation failed, probably because of no container."""

    def __str__(self) -> str:
        """Provide a human-readable description of the error."""
        return f"The `docker inspect` invocation for `{self.cid}` failed; no such container?"


@dataclasses.dataclass
class ProcessNoMatchError(ScryError, defs.NoMatchError):
    """No matching process was reported by `pgrep`."""

    pgrep_args: list[str]
    """The additional arguments passed to `pgrep`."""

    def __str__(self) -> str:
        """Provide a human-readable description of the error."""
        return (
            f"No process could be found matching `{shlex.join(self.pgrep_args)}` "
            f"in the {self.cid} container"
        )


@dataclasses.dataclass
class CommandRunError(ScryError):
    """An error that occurred while running a command."""

    cmd: list[str]
    """The command to run."""

    err: OSError | subprocess.CalledProcessError
    """The error that occurred."""

    @property
    def cmdstr(self) -> str:
        """A shell-quoted representation of the command."""
        return shlex.join(self.cmd)

    def __str__(self) -> str:
        """Provide a human-readable description of the error."""
        return f"Could not run the `{self.cmdstr}` command: {self.err}"


def inspect(cfg: defs.PGrepConfig) -> defs.Container:
    """Grab some of the data that `docker-inspect` will output."""
    cfg.log.info("Inspecting the %(cid)s container", {"cid": cfg.cid})
    cmd: Final = ["docker", "inspect", "-f", "json", "--", cfg.cid]
    cfg.log.debug("- running %(cmdstr)s", {"cmdstr": shlex.join(cmd)})
    try:
        raw: Final = subprocess.check_output(cmd, encoding="UTF-8", env=cfg.utf8_env)  # noqa: S603
    except OSError as err:
        raise CommandRunError(cfg.cid, cmd, err) from err
    except subprocess.CalledProcessError as err:
        raise ContainerNoMatchError(cfg.cid) from err
    cfg.log.debug("- got %(count)d characters of JSON output", {"count": len(raw)})
    try:
        insp: Final = json.loads(raw)
    except ValueError as err:
        raise RuntimeError(repr((cfg.cid, err))) from err
    cfg.log.debug("- got info about %(count)d containers", {"count": len(insp)})

    try:
        pid: Final = insp[0]["State"]["Pid"]
    except (KeyError, IndexError, TypeError, AttributeError) as err:
        raise RuntimeError(repr((cfg.cid, err))) from err
    cfg.log.debug("- got pid %(pid)d", {"pid": pid})

    return defs.Container(cid=cfg.cid, pid=pid)


def proc_ns_pid_path(pid: int) -> pathlib.Path:
    """Determine the path to examine for permissions to access a pid namespace."""
    return pathlib.Path("/proc") / str(pid) / "ns" / "pid"


def check_proc_ns_pid(cfg: defs.PGrepConfig, cont: defs.Container) -> None:
    """Check whether we can access /proc/.../ns/pid before we run `pgrep`."""
    proc_path: Final = proc_ns_pid_path(cont.pid)
    cfg.log.info("Checking whether we can access the %(proc)s link", {"proc": proc_path})
    try:
        proc_path.stat()
    except (PermissionError, FileNotFoundError) as err:
        raise RuntimeError(repr((proc_path, err))) from err


def pgrep(
    cfg: defs.PGrepConfig,
    cont: defs.Container,
) -> tuple[list[tuple[int, str]], list[str]]:
    """Run `pgrep`, parse the output."""
    if not cfg.force:
        check_proc_ns_pid(cfg, cont)

    cfg.log.info("Looking for processes in the same namespace as %(pid)d", {"pid": cont.pid})
    cmd: Final = [
        "pgrep",
        "--ns",
        str(cont.pid),
        "-a",
        *cfg.pgrep_args,
    ]
    cfg.log.debug("- running %(cmdstr)s", {"cmdstr": shlex.join(cmd)})
    try:
        lines: Final = subprocess.check_output(  # noqa: S603
            cmd,
            encoding="UTF-8",
            env=cfg.utf8_env,
        ).splitlines()
    except OSError as err:
        raise CommandRunError(cont.cid, cmd, err) from err
    except subprocess.CalledProcessError as err:
        if err.args[0] == 1:
            # pgrep could not find the process
            raise ProcessNoMatchError(cont.cid, cfg.pgrep_args) from err

        raise CommandRunError(cont.cid, cmd, err) from err
    cfg.log.debug("- got %(count)d lines of output", {"count": len(lines)})

    def single(line: str) -> tuple[int, str]:
        """Split a single line into a process ID and a command string."""
        first, rest = line.split(" ", maxsplit=1)
        cfg.log.debug(
            "- examining a line: first %(first)r rest %(rest)r",
            {"first": first, "rest": rest},
        )
        try:
            pid: Final = int(first)
        except ValueError as err:
            raise RuntimeError(repr((line, err))) from err
        cfg.log.debug("- extracted pid %(pid)d", {"pid": pid})

        return pid, rest

    res: Final = [single(line) for line in lines]
    cfg.log.debug("- parsed info about %(count)d processes", {"count": len(res)})
    if (not cfg.pgrep_args) and res and res[0][0] != cont.pid:
        raise RuntimeError(repr((lines, res, cont.pid)))

    seen: Final = {pair[0] for pair in res}
    if len(seen) != len(res):
        raise RuntimeError(repr((lines, res, sorted(seen))))

    return res, lines


def run_ps(
    cfg: defs.Config,
    cont: defs.Container,
    pids: list[tuple[int, str]],
    *,
    ps_args: list[str],
) -> None:
    """Run `ps` on the returned process IDs."""
    cmd: Final = ["ps", *ps_args]
    cfg.log.debug("Running `%(cmdstr)s` on the selected processes", {"cmdstr": shlex.join(cmd)})
    try:
        subprocess.check_call([*cmd, *(str(tup[0]) for tup in pids)])  # noqa: S603
    except (OSError, subprocess.CalledProcessError) as err:
        raise CommandRunError(cont.cid, cmd, err) from err
