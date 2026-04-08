#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="${OPENCLAW_WORKSPACE_DIR:-$HOME/.openclaw/workspace-main}"
MP_BIN_DIR="${OPENCLAW_MP_BIN_DIR:-$HOME/.local/bin}"
PY_SITE_BIN="$HOME/Library/Python/3.9/bin"

mkdir -p "$WORKSPACE_DIR/scripts" "$WORKSPACE_DIR/.learnings" "$MP_BIN_DIR" "$HOME/.mempalace/palace"

echo "==> Installing Python dependency: mempalace"
python3 -m pip install --user mempalace

echo "==> Installing mp wrapper"
cp "$REPO_DIR/bin/mp.py" "$WORKSPACE_DIR/scripts/mp.py"
chmod +x "$WORKSPACE_DIR/scripts/mp.py"
ln -sf "$WORKSPACE_DIR/scripts/mp.py" "$MP_BIN_DIR/mp"

if [ -d "$PY_SITE_BIN" ] && [[ ":$PATH:" != *":$PY_SITE_BIN:"* ]]; then
  echo "==> Note: add this to your shell profile if needed:"
  echo "export PATH=\"$MP_BIN_DIR:$PY_SITE_BIN:\$PATH\""
fi

echo "==> Writing MemPalace config"
cat > "$HOME/.mempalace/config.json" <<EOF
{
  "palace_path": "$HOME/.mempalace/palace",
  "collection_name": "mempalace_drawers",
  "people_map": {}
}
EOF

cat > "$HOME/.mempalace/identity.txt" <<EOF
OpenClaw Memory Palace
- Local-first memory system for OpenClaw
- Powered by MemPalace + ChromaDB + SQLite knowledge graph
EOF

if [ ! -f "$HOME/.mempalace/wing_config.json" ]; then
cat > "$HOME/.mempalace/wing_config.json" <<EOF
{
  "default_wing": "wing_general",
  "wings": {
    "wing_openclaw": {
      "type": "project",
      "keywords": ["openclaw", "agent", "assistant", "memory"]
    },
    "wing_library": {
      "type": "project",
      "keywords": ["library", "article", "tweet", "video", "podcast"]
    }
  }
}
EOF
fi

touch "$WORKSPACE_DIR/.learnings/LEARNINGS.md" "$WORKSPACE_DIR/.learnings/ERRORS.md" "$WORKSPACE_DIR/.learnings/FEATURE_REQUESTS.md"

echo "==> Done"
echo
echo "Next steps:"
echo "  1. export PATH=\"$MP_BIN_DIR:$PY_SITE_BIN:\$PATH\""
echo "  2. mp status"
echo "  3. mp graph enrich"
echo "  4. mp save https://example.com/article"
