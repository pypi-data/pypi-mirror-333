<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

# docker scry - examine Docker containers using host tools

## Synopsis

```
docker scry [-qv] pgrep [-f] [--ps PS_OPTIONS] -c container-id [pgrep arguments]

docker scry [-h | --help | -V | --version]
```

## Description

The `docker scry` tool uses the host's tools to examine processes running in
a Docker container.
Currently a single subcommand, `pgrep`, is implemented to show the list of
processes running within the container.

The `docker scry` tool accepts the following command-line options:

- `--features`: display program features information and exit
- `--help` (`-h`): display program usage information and exit
- `--quiet` (`-q`): quiet operation; only display warning and error messages
- `--verbose` (`-v`): verbose operation; display diagnostic output
- `--version` (`-V`): display program version information and exit

### The pgrep subcommand

The `docker scry pgrep` subcommand uses the host's `pgrep` and `ps` utilities to
display information about processes running within a Docker container.
It first runs `docker inspect`, and then uses the Linux-specific namespace
parameters to `pgrep` to find the other processes running in
the same PID namespace as the container's main process.
The `docker scry pgrep` subcommand accepts the following command-line options:

- `--container-id` (`-c`): required: specifiy the container to examine
- `--force` (`-f`): skip the `/proc/.../ns/pid` access rights check
- `--help` (`-h`): display subcommand usage information and exit
- `--ps`: instead of displaying `pgrep` output, run `ps` with
  the specified options on the processes reported by `pgrep`

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
