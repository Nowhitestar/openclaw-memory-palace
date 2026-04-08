<div align="center">

# OpenClaw Memory Palace

### An OpenClaw-enhanced MemPalace: unified conversation memory + link library + knowledge graph — local-first.

[![Release](https://img.shields.io/github/v/release/Nowhitestar/openclaw-memory-palace?style=flat-square)](https://github.com/Nowhitestar/openclaw-memory-palace/releases)
[![License](https://img.shields.io/github/license/Nowhitestar/openclaw-memory-palace?style=flat-square)](./LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-integration-blue?style=flat-square)](https://github.com/openclaw/openclaw)
[![MemPalace](https://img.shields.io/badge/Built%20on-MemPalace-black?style=flat-square)](https://github.com/milla-jovovich/mempalace)

<br>

[Quick Start](#quick-start) · [What You Get](#what-you-get) · [How You Actually Use It](#how-you-actually-use-it) · [Architecture](#architecture) · [FAQ](docs/FAQ.md)

</div>

---

Every agent conversation contains decisions, tradeoffs, and debugging context.
But most setups either:
- store it as flat markdown you can’t semantically navigate, or
- split “saved links” into a separate system, disconnected from your real work.

**OpenClaw Memory Palace** is a practical “MemPalace for OpenClaw” integration:
- full-text link archiving into your OpenClaw `library/`
- chunked semantic indexing into MemPalace / ChromaDB
- a lightweight knowledge graph that can be enriched from saved content
- a single command surface: `mp`

This repo ships the reusable system only — **your actual memory data stays local**.


## Quick Start

### Option A (recommended): clone & run

```bash
git clone https://github.com/Nowhitestar/openclaw-memory-palace.git
cd openclaw-memory-palace
bash install.sh

mp status
mp graph enrich
mp save https://github.com/milla-jovovich/mempalace --title "MemPalace GitHub"
mp find "memory system"
mp search "why did we choose X"
```

### Option B: one-liner (review before you run)

```bash
curl -fsSL https://raw.githubusercontent.com/Nowhitestar/openclaw-memory-palace/main/install.sh | bash
```

If `mp` is not found afterwards, add this to your shell profile:

```bash
export PATH="$HOME/.local/bin:$(python3 -m site --user-base)/bin:$PATH"
```


## What You Get

### 1) One unified memory surface
- **Conversation memory** (mined from your OpenClaw `memory/` logs)
- **Saved link library** (your OpenClaw `library/`)
- **Knowledge graph** for entity relations

Everything is retrievable through one CLI:
- `mp search …` (all wings)
- `mp find …` (library-only)
- `mp graph query …`

### 2) Full original text stays readable
`mp save` writes a markdown file with:
- full original content
- auto-generated summary
- heuristic tags
- related entries (semantic)

### 3) Retrieval is optimized
The same document is indexed into MemPalace as **chunks**, so semantic search works well on long articles.


## How You Actually Use It

You don’t “manage a database”. You do normal work, and the memory system follows.

### Save links (the Link Library becomes a MemPalace wing)
```bash
mp save https://example.com/article
mp save https://x.com/user/status/123
mp save https://mp.weixin.qq.com/s/xxx
```

### Search
```bash
mp search "auth decision"
mp find "agent workflow"
```

### Knowledge graph
```bash
mp graph enrich
mp graph stats
mp graph query OpenClaw
```

### Browse
```bash
mp list
mp list articles
mp list tweets
```


## Architecture

**Source of truth (files):**
- Full text is stored in: `~/.openclaw/workspace-main/library/`

**Semantic index (vectors):**
- ChromaDB lives in: `~/.mempalace/palace`
- Documents are indexed as **overlapping chunks** for better recall.

**Knowledge graph (SQLite):**
- `~/.mempalace/knowledge_graph.sqlite3`

### What’s different from vanilla MemPalace?

MemPalace is the engine.
This repo is the OpenClaw-focused “product layer”:

- ✅ Adds a **Link Library workflow** (`mp save`) that writes OpenClaw library files and indexes them in chunks
- ✅ Adds **OpenClaw-friendly commands** (`mp find`, `mp list`)
- ✅ Adds **graph enrichment** from saved library metadata (`mp graph enrich`)
- ✅ Keeps everything **local-first** and **human-readable**


## Repo contents

```text
bin/mp.py
install.sh
upgrade.sh
uninstall.sh
README.md
README.zh-CN.md
docs/FAQ.md
docs/RELEASE_NOTES_v0.1.0.md
examples/quickstart.md
examples/demo-output.txt
```


## Safety / Privacy

- This repo does **not** upload your personal memory.
- It ships only reusable code + scripts.
- Your local data remains on your machine.


## Upgrade / Uninstall

```bash
bash upgrade.sh
bash uninstall.sh
```


## Credits

Built on top of MemPalace by Milla Jovovich & Ben Sigman.


## License

MIT
