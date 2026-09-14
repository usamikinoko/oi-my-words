#!/usr/bin/env bash
# oi-my-words — installer (bash counterpart of install.ps1).
#
# Deploys every skill bundle in skills/ (one directory = one bundle, must
# contain SKILL.md) into a DSH user skill root. The DSH watcher hot-reloads the
# newly installed skills; no restart is needed.

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: bash install.sh [options]

  -t, --target DIR   skill root to install into (default: ~/.dsh/skills)
  -n, --dry-run      show what would be copied, write nothing
  -h, --help         show this help
EOF
}

TARGET="${HOME}/.dsh/skills"
DRY_RUN=0

while [ $# -gt 0 ]; do
  case "$1" in
    -t|--target)
      [ $# -ge 2 ] || { echo "install.sh: $1 needs an argument" >&2; exit 2; }
      TARGET="$2"; shift 2 ;;
    -n|--dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "install.sh: unknown argument: $1" >&2; exit 2 ;;
  esac
done

# Locate the repo next to this script. BASH_SOURCE is unset when bash is invoked
# from stdin (curl | bash); fall back to the current working directory.
here="$(cd "$(dirname "${BASH_SOURCE[0]:-}")" 2>/dev/null && pwd)" || here="$PWD"
src="${here}/skills"
if [ ! -d "$src" ]; then
  echo "install.sh: skills/ not found next to install.sh (looked in ${here})" >&2
  exit 1
fi

mkdir -p "$TARGET"

installed=0
for bundle in "$src"/*/; do
  [ -d "$bundle" ] || continue
  bundle="${bundle%/}"
  name="$(basename "$bundle")"
  if [ ! -f "${bundle}/SKILL.md" ]; then
    echo "install.sh: skip ${name}: no SKILL.md" >&2
    continue
  fi
  dest="${TARGET}/${name}"
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "would install: ${name} -> ${dest}"
    continue
  fi
  # Clean-replace: cp -R nests the source inside an existing destination.
  rm -rf "$dest"
  cp -R "$bundle" "$dest"
  installed=$((installed + 1))
  echo "installed: ${name}"
done

if [ "$DRY_RUN" -eq 1 ]; then
  echo "dry run: no files written"
else
  echo "done: ${installed} skills -> ${TARGET}"
fi
