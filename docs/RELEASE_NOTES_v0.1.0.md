# OpenClaw Memory Palace — v0.1.0

The first public release of an **OpenClaw-enhanced MemPalace**.

This is not “just a wrapper”. It is a practical product layer for OpenClaw that:
- unifies **conversation memory** + **saved link library** into one semantic system
- preserves **full original text** as readable markdown files
- indexes long documents as **overlapping chunks** for better retrieval
- provides a lightweight **SQLite knowledge graph** with enrichment

## Highlights

- **One-command install** (`install.sh`) + upgrade/uninstall scripts
- Unified command surface: `mp`
- `mp save <url>`
  - writes full original content into OpenClaw `library/`
  - auto summary / tags / related
  - chunked indexing into MemPalace / ChromaDB
- `mp search` (global) and `mp find` (library-only)
- Knowledge graph:
  - `mp graph query` / `mp graph stats`
  - `mp graph enrich` (derive extra triples from saved content)

## Main commands

```bash
mp status
mp search "why did we choose X"
mp find "agent workflow"
mp save <url>
mp graph enrich
mp graph query <entity>
mp list
```

## Data locations (local-first)

- Full text archive: `~/.openclaw/workspace-main/library/`
- Vector index: `~/.mempalace/palace` (ChromaDB)
- Knowledge graph: `~/.mempalace/knowledge_graph.sqlite3`

## Privacy

This release ships reusable scripts and code only.
Your private memory data stays on your machine.
