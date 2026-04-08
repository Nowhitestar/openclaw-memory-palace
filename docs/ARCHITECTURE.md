# Architecture

```text
User
  │
  │ normal conversation / sharing links / asking about the past
  ▼
OpenClaw agent
  │
  ├─ recalls memory when needed
  ├─ saves interesting links when appropriate
  └─ queries related entities / decisions
  ▼
mp (internal integration layer)
  │
  ├─ library files (source of truth)
  ├─ MemPalace / ChromaDB (semantic retrieval)
  └─ SQLite knowledge graph (entities + relations)
```

## Layers

### 1. User-facing layer
The user talks to OpenClaw normally. In the ideal workflow, the user does **not** need to manually run `mp` commands.

### 2. Integration layer
`mp` is the glue layer between OpenClaw and the underlying memory engines. It handles:
- link capture
- indexing
- graph enrichment
- retrieval helpers

### 3. Storage layer
- `~/.openclaw/workspace-main/library/` → full text / markdown source of truth
- `~/.mempalace/palace` → semantic chunks in ChromaDB
- `~/.mempalace/knowledge_graph.sqlite3` → entity graph
