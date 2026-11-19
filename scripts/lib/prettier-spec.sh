#!/usr/bin/env bash
# prettier-spec.sh — print the one prettier this repository runs, as
# `prettier@X.Y.Z`.
#
# This file is the pin. The hooks and `make init-hooks` hand the spec to npx so
# every host formats with the same prettier instead of whatever `npx prettier`
# resolves that day. prettier 3.10 rewrites a `---` line inside fenced markdown
# examples to `***`, which breaks the documented hook-file shape and a negative
# skill fixture; an unpinned gate turned the same tree red overnight.
set -euo pipefail

printf 'prettier@%s\n' "3.9.0"
