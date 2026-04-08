#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_DIR="${OPENCLAW_WORKSPACE_DIR:-$HOME/.openclaw/workspace-main}"
MP_BIN_DIR="${OPENCLAW_MP_BIN_DIR:-$HOME/.local/bin}"

rm -f "$MP_BIN_DIR/mp"
rm -f "$WORKSPACE_DIR/scripts/mp.py"

echo "Uninstalled wrapper files."
echo "Note: local memory data under ~/.mempalace and ~/ .openclaw/workspace-main/library was NOT deleted."
