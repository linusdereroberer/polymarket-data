#!/usr/bin/env bash
set -euo pipefail
script="${BASH_SOURCE[0]}"
here="$(cd -- "${script%/*}" && pwd)"
destination="${1:-restored-data}"
if (( $# )); then shift; fi
exec python3 "$here/restore.py" --manifest "$here/MANIFEST.json" --destination "$destination" "$@"
