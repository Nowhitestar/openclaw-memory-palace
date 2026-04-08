# OpenClaw Memory Palace

[![Release](https://img.shields.io/github/v/release/Nowhitestar/openclaw-memory-palace?style=flat-square)](https://github.com/Nowhitestar/openclaw-memory-palace/releases)
[![License](https://img.shields.io/github/license/Nowhitestar/openclaw-memory-palace?style=flat-square)](./LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-memory%20upgrade-blue?style=flat-square)](https://github.com/Nowhitestar/openclaw-memory-palace)

Turn OpenClaw from a note-searching assistant into a memory-backed partner.

**OpenClaw Memory Palace** packages the memory system we built on top of:
- [MemPalace](https://github.com/milla-jovovich/mempalace)
- ChromaDB for semantic retrieval
- SQLite knowledge graph for entity relations
- a custom `mp` wrapper for OpenClaw workflows

## Who this is for

**Good fit if you want:**
- semantic recall across conversation memory and saved links
- a local-first memory system for OpenClaw
- full-text link archiving plus vector retrieval
- a lightweight knowledge graph without cloud lock-in

**Not ideal if you want:**
- a hosted SaaS memory product
- a pure GUI workflow
- a non-local / cloud-only setup

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

## Demo

```bash
$ mp status
📦 MemPalace — 108 drawers

$ mp save https://github.com/milla-jovovich/mempalace --title "MemPalace GitHub"
✅ Saved to: ~/.openclaw/workspace-main/library/articles/mempalace-github-2026-04-08.md
✅ Indexed full text to MemPalace (33 chunks)
🏷️ Tags: article, ai, startup, security, memory, workflow, github.com

$ mp graph stats
🧠 Knowledge Graph Stats
  Triples: 28
  Entities: 31
```

Full sample: [`examples/demo-output.txt`](examples/demo-output.txt)

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
docs/RELEASE_NOTES_v0.1.0.md
examples/quickstart.md # command examples
examples/demo-output.txt
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
