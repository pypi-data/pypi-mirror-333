<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

# docker-scry - examine Docker containers using host tools

\[[Home][ringlet-home] | [Download][ringlet-download] | [GitLab][gitlab] | [PyPI][pypi] | [ReadTheDocs][readthedocs]\]

## Overview

The `docker-scry` tool uses the host's `pgrep` and `ps` utilities to
display information about processes running within a Docker container.
It first runs `docker inspect`, and then uses the Linux-specific namespace
parameters to `pgrep` to find the other processes running in
the same PID namespace as the container's main process.

## Needs to be run as root

Because of the way `pgrep` works, `docker-scry` only runs reliably if
invoked from the root account; otherwise `pgrep` will list all of
the processes running on the system as being in the same namespace as
the container's main process.

The `docker-scry` tool will refuse to run `pgrep` if it is unable to
examine the `/proc/<main-process-id>/ns/pid` filesystem entry; that will
happen if it is not run as root.
If there is a reason to believe that `pgrep` will not fall back to
listing all the system processes, this check may be disabled by
the `--force` (`-f`) option to `docker-scry pgrep`.

## Installation

### Install the docker-scry tool itself

#### Install into a virtual environment using uv

One of the fastest ways to get a virtual environment up and running is to
use [the uv tool][astral-uv]:

``` sh
uv venv /path/to/venv
(set -e; . /path/to/venv/bin/activate; uv pip install docker-scry)
/path/to/venv/bin/docker-scry --help
```

#### Let uvx handle the virtual environment

The `uv` tool's `uvx` command will automatically handle the installation of
Python libraries into virtual environments that it keeps in per-user cache and
temporary directories:

``` sh
uvx docker-scry --help
```

#### Install into a virtual environment using venv

Most distributions of Python will already have a `venv` module installed or
ready to be installed by the package manager (e.g. `apt install python3-venv`):

``` sh
python3 -m venv /path/to/venv
/path/to/venv/bin/python3 -m pip install docker-scry
/path/to/venv/bin/docker-scry --help
```

### Let docker know about the scry subcommand

Once there is a way to run `docker-scry` itself, `docker` must be told about
the new `scry` subcommand.
This is done by placing a `docker-scry` symlink into one of the directories that
`docker` searches for its CLI plugins: either a system-wide one (usually
`/usr/lib/docker/cli-plugins/` or `/usr/libexec/docker/cli-plugins`), or
a per-user one:

```
mkdir -p -- "$HOME/.docker/cli-plugins"
ln -s /path/to/venv/bin/docker-scry "$HOME/.docker/cli-plugins/"
docker --help | grep -Fe scry
docker scry --help
```

If `docker-scry` is started using `uvx`, then a small shell program should be
placed into the `cli-plugins` directory under the `docker-scry` name:

```
#!/bin/sh

exec uvx -- docker-scry "$@"
```

Once that file exists (and is made executable), Docker should be able to
detect it and run it as the `scry` subcommand.

## Examples

Show the list of processes running within a container:

``` sh
docker scry pgrep -c sweet_banzai
```

Same, but display more diagnostic information about the commands run:

``` sh
docker scry -v pgrep -c sweet_banzai
```

Do not display even the informational messages; any output on
the standard error stream will indicate actual warnings or errors:

``` sh
docker scry -q pgrep -c sweet_banzai
```

Only show processes that have `python` in their command name:

``` sh
docker scry pgrep -c sweet_banzai -- python
```

Only show processes that have `python` anywhere on their command line:

``` sh
docker scry pgrep -c sweet_banzai -- -f python
```

Same, but run `ps uww` on the processes to show more information:

``` sh
docker scry pgrep -c sweet_banzai --ps uww -- -f python
```

Pass more command-line arguments to `ps`:

``` sh
docker scry -q pgrep -c sweet_banzai --ps '-h -o pid,ppid,cmd' -- -f python
```

## Exit status

The `docker scry pgrep` subcommand attempts to imitate the exit status of
the `pgrep` utility:

- 0 on success
- 1 if the container was not found or no processes were matched within it
- 3 on another fatal error

## Contact

The `docker-scry` library was written by [Peter Pentchev][roam].
It is developed in [a GitLab repository][gitlab].
This documentation is hosted at [Ringlet][ringlet-home] with a copy at [ReadTheDocs][readthedocs].

[roam]: mailto:roam@ringlet.net "Peter Pentchev"
[gitlab]: https://gitlab.com/ppentchev/docker-scry "The docker-scry GitLab repository"
[pypi]: https://pypi.org/project/docker-scry/ "The docker-scry Python Package Index page"
[readthedocs]: https://docker-scry.readthedocs.io/ "The docker-scry ReadTheDocs page"
[ringlet-download]: https://devel.ringlet.net/sysutils/docker-scry/download/ "The Ringlet docker-scry download page"
[ringlet-home]: https://devel.ringlet.net/sysutils/docker-scry/ "The Ringlet docker-scry homepage"

[astral-uv]: https://astral.sh/uv "uv - an extremely fast Python package and project manager"
