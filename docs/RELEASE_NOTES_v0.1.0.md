# OpenClaw Memory Palace — v0.1.0

The first public release of an **OpenClaw-enhanced MemPalace**.

This release is best understood as an **OpenClaw-native memory layer** built on top of MemPalace:
- users primarily interact with **OpenClaw**
- `mp` acts as the **integration / operator layer** underneath
- full source text is preserved as readable markdown
- long content is indexed as overlapping chunks for retrieval
- relationships can be enriched into a local SQLite knowledge graph

## Highlights

- One-command install (`install.sh`)
- Upgrade / uninstall scripts
- Unified internal command surface: `mp`
- OpenClaw link archiving into `library/`
- Chunked semantic indexing into MemPalace / ChromaDB
- Graph enrichment from saved content metadata
- English + Chinese documentation
- Banner, architecture notes, and user-flow docs

## End-user mental model

A normal user should mostly:
- chat with OpenClaw
- share links
- ask about past decisions or saved material

OpenClaw should handle the memory layer behind the scenes.

## Operator / debugging commands

```bash
mp status
mp search "why did we choose X"
mp find "agent workflow"
mp save <url>
mp graph enrich
mp graph query <entity>
mp list
```

## Local-first storage

- Full text archive: `~/.openclaw/workspace-main/library/`
- Vector index: `~/.mempalace/palace`
- Knowledge graph: `~/.mempalace/knowledge_graph.sqlite3`

## Privacy

This release ships reusable scripts and code only.
Your private memory data stays on your machine.
