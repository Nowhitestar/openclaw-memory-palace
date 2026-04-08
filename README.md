# OpenClaw Memory Palace

Turn OpenClaw from a note-searching assistant into a memory-backed partner.

**OpenClaw Memory Palace** packages the memory system we built on top of:
- [MemPalace](https://github.com/milla-jovovich/mempalace)
- ChromaDB for semantic retrieval
- SQLite knowledge graph for entity relations
- a custom `mp` wrapper for OpenClaw workflows

## Why this exists

OpenClaw already has files, notes, and memory logs. But those are usually:
- flat
- split across multiple places
- awkward to search semantically
- disconnected from saved web content

This project unifies them into one local-first memory system.

## Before vs After

### Before
- flat markdown notes
- separate link library
- mostly keyword/file-based recall
- weak entity relationship memory

### After
- semantic memory across conversations + saved links
- unified `library` wing inside MemPalace
- knowledge graph (`mp graph query`, `mp graph enrich`)
- full-text link archiving with chunked indexing
- auto summary / tags / related links on `mp save`

## What you can do

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

If `mp` is not found afterwards, add this to your shell profile:

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

More examples: [`examples/quickstart.md`](examples/quickstart.md)

## How storage works

### 1. Full original text
`mp save` stores the full original content in:

```text
~/.openclaw/workspace-main/library/
```

### 2. Semantic index
The same document is chunked and indexed into MemPalace / ChromaDB for retrieval.

### 3. Knowledge graph
Important entities and relations live in:

```text
~/.mempalace/knowledge_graph.sqlite3
```

## Repo contents

```text
bin/mp.py              # OpenClaw wrapper
install.sh             # one-click installer
upgrade.sh             # upgrade wrapper + dependency
uninstall.sh           # remove wrapper files
README.md              # English docs
README.zh-CN.md        # 中文文档
docs/FAQ.md            # FAQ
examples/quickstart.md # command examples
```

## Safety / privacy

- This repo does **not** upload your personal memory files.
- It only ships the reusable memory system and installer.
- Your actual saved memories stay local.

## Upgrade

```bash
bash upgrade.sh
```

## Uninstall

```bash
bash uninstall.sh
```

Note: uninstall removes the wrapper, not your local data.

## FAQ

See [`docs/FAQ.md`](docs/FAQ.md).

## Credits

Built on top of MemPalace by Milla Jovovich & Ben Sigman.

## License

MIT
