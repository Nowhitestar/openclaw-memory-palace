# FAQ

## Does this upload my private memory to GitHub?
No. This repository only contains the reusable installer and wrapper. Your actual memory stays local.

## Where is the full original text stored?
In `~/.openclaw/workspace-main/library/`.

## Where is the semantic index stored?
In MemPalace / ChromaDB under `~/.mempalace/palace`.

## Where is the knowledge graph stored?
In `~/.mempalace/knowledge_graph.sqlite3`.

## Why store files and vectors separately?
Because files are the source of truth, while vectors are optimized for retrieval.

## Can I re-index after editing a saved file?
Yes. Re-run `mp save <url>` for the same URL, or use MemPalace mining commands on your library.

## Does `mp save` keep the full original content?
Yes. Full original text is written to the markdown file. MemPalace indexes chunked copies for search.

## What if a platform fetch fails?
The wrapper still saves a stub entry so you can edit/fill it later.
