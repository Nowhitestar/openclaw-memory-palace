#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="${OPENCLAW_WORKSPACE_DIR:-$HOME/.openclaw/workspace-main}"
MP_BIN_DIR="${OPENCLAW_MP_BIN_DIR:-$HOME/.local/bin}"

python3 -m pip install --user --upgrade mempalace
cp "$REPO_DIR/bin/mp.py" "$WORKSPACE_DIR/scripts/mp.py"
chmod +x "$WORKSPACE_DIR/scripts/mp.py"
mkdir -p "$MP_BIN_DIR"
ln -sf "$WORKSPACE_DIR/scripts/mp.py" "$MP_BIN_DIR/mp"

echo "Upgrade complete."
python3 "$WORKSPACE_DIR/scripts/mp.py" status || true
