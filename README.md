# OpenClaw Memory Palace

A one-command memory upgrade for OpenClaw.

This project packages the memory system we built on top of:
- [MemPalace](https://github.com/milla-jovovich/mempalace)
- ChromaDB for semantic retrieval
- SQLite knowledge graph for entity relations
- a custom `mp` wrapper for OpenClaw workflows

## What it gives you

Before:
- flat markdown notes
- separate link library
- mostly keyword/file-based recall

After:
- semantic memory across conversations + saved links
- unified `library` wing inside MemPalace
- knowledge graph (`mp graph query`, `mp graph enrich`)
- full-text link archiving with chunked indexing
- auto summary / tags / related links on `mp save`

## Features

- `mp status` — inspect memory state
- `mp search` — semantic search across all wings
- `mp find` — search saved links only
- `mp save <url>` — save full original content to `library/` and index it into MemPalace
- `mp graph query <entity>` — inspect knowledge graph
- `mp graph enrich` — derive extra triples from saved content
- `mp list` — browse archived content

## Install

```bash
git clone https://github.com/Nowhitestar/openclaw-memory-palace.git
cd openclaw-memory-palace
bash install.sh
```

Then add to shell profile if needed:

```bash
export PATH="$HOME/.local/bin:$HOME/Library/Python/3.9/bin:$PATH"
```

## Quick start

```bash
mp status
mp graph enrich
mp save https://github.com/milla-jovovich/mempalace
mp find "memory system"
mp search "auth decision"
```

## How storage works

### Full original text
`mp save` stores the full original content in:

```text
~/.openclaw/workspace-main/library/
```

### Semantic index
The same document is chunked and indexed into MemPalace/ChromaDB for retrieval.

### Knowledge graph
Important entities and relations live in:

```text
~/.mempalace/knowledge_graph.sqlite3
```

## Repository structure

```text
bin/mp.py          # OpenClaw wrapper
install.sh         # one-click installer
README.md          # English docs
README.zh-CN.md    # 中文文档
```

## Notes

- This repo does **not** upload your personal memory files.
- It only ships the reusable memory system and installer.
- Your actual saved memories stay local.

## Credits

Built on top of MemPalace by Milla Jovovich & Ben Sigman.

## License

MIT
