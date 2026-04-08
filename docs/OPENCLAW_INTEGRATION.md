# OpenClaw Integration Notes

This project is intentionally OpenClaw-shaped.

## Default paths

- OpenClaw workspace: `~/.openclaw/workspace-main`
- Library archive: `~/.openclaw/workspace-main/library/`
- MemPalace palace: `~/.mempalace/palace`
- Knowledge graph: `~/.mempalace/knowledge_graph.sqlite3`

## Recommended workflow

- Use OpenClaw normally.
- When a link is worth keeping: `mp save <url>`.
- When you need recall: `mp search <query>` or `mp find <query>`.
- Periodically: `mp graph enrich` to expand relationships.

## Environment variables (optional)

- `OPENCLAW_WORKSPACE_DIR` — override workspace path
- `OPENCLAW_MP_BIN_DIR` — where the `mp` symlink is created
