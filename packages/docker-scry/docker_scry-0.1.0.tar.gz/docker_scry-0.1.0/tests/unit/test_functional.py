# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Make sure that `docker-scry run` starts up at least."""

from __future__ import annotations

import functools
import os
import os.path
import pathlib
import subprocess  # noqa: S404
import sys
import tempfile
import typing

import utf8_locale


if typing.TYPE_CHECKING:
    from typing import Final


TEST_DATA: Final = pathlib.Path(__file__).resolve().parent.parent.parent / "test-data"
"""The path to the directory containing the test data files."""

CID: Final = "ff4ad37638dc"
"""The container ID to use for the tests."""

PID_MAIN: Final = 6502
"""The process ID of the main container process."""

PID_CHILD: Final = "6800"
"""The process ID of the child process within the container."""


@functools.lru_cache
def utf8_env() -> dict[str, str]:
    """Prepare a UTF-8-capable environment."""
    return utf8_locale.UTF8Detect().detect().env


def test_ps_help() -> None:
    """Make sure that `docker-scry ps --help` works."""
    output_help: Final = subprocess.check_output(  # noqa: S603
        [sys.executable, "-m", "docker_scry", "pgrep", "--help"],
        encoding="UTF-8",
    )
    assert "CONTAINER_ID" in output_help


def test_pgrep() -> None:
    """Make sure that `docker-scry ps` runs the right external commands."""
    with tempfile.TemporaryDirectory(prefix="test-docker-scry-ps.") as tempd_obj:
        tempd: Final = pathlib.Path(tempd_obj)

        docker_data: Final = tempd / "docker-data"
        docker_data.mkdir(mode=0o755)

        env: Final = dict(utf8_env()) | {
            "DOCKER_SCRY_TEST_DATA": str(docker_data),
        }
        env["PATH"] = os.path.pathsep.join([str(TEST_DATA / "bin"), env["PATH"]])

        cid: Final = CID
        pid_main: Final = PID_MAIN
        pid_child: Final = PID_CHILD

        path_inspect: Final = docker_data / f"docker-inspect-{cid}.json"
        data_inspect: Final = (
            (TEST_DATA / "docker-data" / "docker-inspect-cid.json")
            .read_text(encoding="UTF-8")
            .replace("{{ CID }}", cid)
            .replace("{{ PID_MAIN }}", str(pid_main))
            .replace("{{ PID_CHILD }}", str(pid_child))
        )
        path_inspect.write_text(data_inspect, encoding="UTF-8")

        path_pgrep: Final = docker_data / f"pgrep-{pid_main}.txt"
        data_pgrep: Final = (
            (TEST_DATA / "docker-data" / "pgrep-pid.txt")
            .read_text(encoding="UTF-8")
            .replace("{{ CID }}", cid)
            .replace("{{ PID_MAIN }}", str(pid_main))
            .replace("{{ PID_CHILD }}", str(pid_child))
        )
        path_pgrep.write_text(data_pgrep, encoding="UTF-8")

        output: Final = subprocess.check_output(  # noqa: S603
            [sys.executable, "-m", "docker_scry", "pgrep", "-c", cid, "-f"],
            encoding="UTF-8",
            env=env,
        )
        assert output == data_pgrep
