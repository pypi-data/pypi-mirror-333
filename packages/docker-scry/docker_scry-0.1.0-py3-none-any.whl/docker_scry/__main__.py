# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Examine Docker containers using the host's tools."""

from __future__ import annotations

import dataclasses
import json
import shlex
import sys
import typing

import click
import utf8_locale

from . import defs
from . import scry
from . import util


if typing.TYPE_CHECKING:
    from typing import Final


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

    print(  # noqa: T201
        "Features: " + " ".join(f"{name}={value}" for name, value in defs.FEATURES.items()),
    )
    sys.exit(0)


@click.command(name="docker-cli-plugin-metadata", hidden=True)
def cmd_docker_cli_plugin_metadata() -> None:
    """Return the JSON description of this Docker plugin."""
    print(  # noqa: T201  # this is the whole point
        json.dumps(
            {
                "SchemaVersion": "0.1.0",
                "Vendor": "Ringlet",
                "Version": defs.VERSION,
                "ShortDescription": "Examine containers using host tools",
            },
            indent=2,
        ),
    )


@click.command(name="pgrep")
@click.option(
    "-c",
    "--container-id",
    type=str,
    required=True,
    metavar="CONTAINER_ID",
    help="the container to examine",
)
@click.option("-f", "--force", is_flag=True, help="skip the /proc/.../ns/pid access rights check")
@click.option("--ps", type=str, help="run `ps` with the specified arguments on the `pgrep` output")
@click.argument("pgrep-args", type=str, nargs=-1)
@click.pass_context
def cmd_pgrep(
    ctx: click.Context,
    *,
    container_id: str,
    force: bool,
    ps: str | None = None,
    pgrep_args: list[str],
) -> None:
    """Do the actual work, or something."""
    cfg: Final = extract_cfg(ctx)
    pcfg: Final = defs.PGrepConfig(
        **dataclasses.asdict(cfg),
        cid=container_id,
        force=force,
        pgrep_args=pgrep_args,
    )

    try:
        cont: Final = scry.inspect(pcfg)
        pids, lines = scry.pgrep(pcfg, cont)

        if ps is None:
            print("\n".join(lines))  # noqa: T201  # this is the whole point
        else:
            scry.run_ps(pcfg, cont, pids, ps_args=shlex.split(ps))
    except defs.NoMatchError as err:
        print(f"docker-scry: {err}", file=sys.stderr)  # noqa: T201
        sys.exit(1)
    except defs.Error as err:
        print(f"docker-scry: {err}", file=sys.stderr)  # noqa: T201
        sys.exit(3)
    except Exception as err:  # noqa: BLE001  # we want to exit with code 3
        print(f"docker-scry: unexpected error: {err}", file=sys.stderr)  # noqa: T201
        sys.exit(3)


@click.group(name="docker-scry", hidden=True)
@click.option(
    "--features",
    is_flag=True,
    is_eager=True,
    callback=arg_features,
    help="display program features information and exit",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="quiet operation; only display warning and error messages",
)
@click.option("--verbose", "-v", is_flag=True, help="verbose operation; display diagnostic output")
@click.pass_context
def main(ctx: click.Context, *, features: bool, quiet: bool, verbose: bool) -> None:
    """Examine Docker containers using the host's tools."""
    if features:
        sys.exit("Internal error: how did we get to main() with features=True?")

    ctx.ensure_object(ConfigHolder)
    ctx.obj.cfg = defs.Config(
        log=util.build_logger(quiet=quiet, verbose=verbose),
        utf8_env=utf8_locale.UTF8Detect().detect().env,
        verbose=verbose,
    )


main.add_command(cmd_docker_cli_plugin_metadata)
main.add_command(cmd_pgrep)

# This is... weird, but it is how Docker invokes CLI plugins -
# apparently it doesn't trust them to know how to examine argv[0].
main.add_command(main, name="scry")


if __name__ == "__main__":
    main()
