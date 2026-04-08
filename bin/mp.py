#!/usr/bin/env python3
"""
mp - MemPalace + Link Library for OpenClaw
===========================================
合并 MemPalace 记忆宫殿 + Link Library 知识库于一体。

用法:
  # Palace 核心
  mp status                          # 宫殿概览
  mp search "query"                  # 语义搜索（全部 wings）
  mp find "query"                    # 搜索 library wing（已保存内容）
  mp wake                            # L0+L1 唤醒上下文
  mp add "content"                   # 添加记忆
  
  # 保存链接
  mp save <url>                      # 保存 URL 到 library
  
  # 知识图谱
  mp graph query <entity>            # 查询实体
  mp graph add <S> <P> <O>           # 添加三元组
  
  # 列表
  mp list [articles|tweets|videos]   # 列出已保存内容
"""

import sys
import os
import json
import argparse
import re
import subprocess
from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path

# Ensure mempalace is importable
sys.path.insert(0, os.path.expanduser("~/Library/Python/3.9/lib/python/site-packages"))

from mempalace.config import MempalaceConfig
from mempalace.searcher import search_memories
from mempalace.knowledge_graph import KnowledgeGraph
import chromadb


# === Configuration ===
_config = MempalaceConfig()
_kg = KnowledgeGraph(db_path=os.path.expanduser("~/.mempalace/knowledge_graph.sqlite3"))

LIBRARY_ROOT = os.path.expanduser("~/.openclaw/workspace-main/library")
LIBRARY_WING = "library"

# URL type detection
URL_PATTERNS = {
    "wechat": [r"mp\.weixin\.qq\.com"],
    "tweet": [r"(twitter|x)\.com/.*status/"],
    "youtube": [r"youtube\.com|youtu\.be"],
    "bilibili": [r"bilibili\.com|b23\.tv"],
    "podcast": [r"podcasts\.apple\.com|spotify\.com/episode"],
    "paper": [r"arxiv\.org"],
}


def _get_collection(create=False):
    try:
        client = chromadb.PersistentClient(path=_config.palace_path)
        if create:
            return client.get_or_create_collection(_config.collection_name)
        return client.get_collection(_config.collection_name)
    except Exception:
        return None


def detect_url_type(url: str) -> str:
    """Detect content type from URL."""
    url_lower = url.lower()
    for content_type, patterns in URL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, url_lower, re.IGNORECASE):
                return content_type
    return "article"


def infer_title_from_url(url: str) -> str:
    """Best-effort title fallback from URL path/domain."""
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if parsed.netloc.endswith("github.com") and path:
        return path.replace("/", " - ")
    if path:
        last = path.split("/")[-1]
        last = re.sub(r'[-_]+', ' ', last)
        if last:
            return last[:80]
    return parsed.netloc or "Untitled"


def extract_title_from_content(content: str) -> str:
    """Try to extract a meaningful title from fetched content."""
    if not content:
        return ""
    lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
    for line in lines[:20]:
        if len(line) < 5:
            continue
        if line.startswith('#'):
            line = line.lstrip('#').strip()
        if line.lower().startswith(('url source', 'markdown content', 'warning', 'http')):
            continue
        if len(line) <= 120:
            return line
    return ""


def fetch_content(url: str, content_type: str) -> dict:
    """Fetch content from URL based on type."""
    result = {"title": "", "content": "", "author": "", "date": "", "success": False, "error": ""}
    
    try:
        if content_type == "wechat":
            # Use wechat-article-for-ai
            tool_path = os.path.expanduser("~/.agent-reach/tools/wechat-article-for-ai")
            proc = subprocess.run(
                ["python3", "main.py", url],
                capture_output=True, text=True, timeout=60, cwd=tool_path
            )
            if proc.returncode == 0:
                result["content"] = proc.stdout
                result["title"] = extract_title_from_content(proc.stdout)
                result["success"] = True
            else:
                result["error"] = f"wechat fetch failed: {proc.stderr[:200]}"
                
        elif content_type == "tweet":
            # Try xreach, fallback to jina
            proc = subprocess.run(
                ["xreach", "tweet", url, "--json"],
                capture_output=True, text=True, timeout=30
            )
            if proc.returncode == 0:
                data = json.loads(proc.stdout)
                result["content"] = data.get("full_text", "")
                result["author"] = data.get("user", {}).get("screen_name", "")
                result["date"] = data.get("created_at", "")
                result["title"] = f"Tweet by @{result['author']}"
                result["success"] = True
            else:
                # Fallback to jina.ai
                jina_url = f"https://r.jina.ai/{url}"
                proc2 = subprocess.run(["curl", "-sL", "--max-time", "30", jina_url], 
                                       capture_output=True, text=True, timeout=35)
                if proc2.returncode == 0 and len(proc2.stdout) > 50:
                    result["content"] = proc2.stdout
                    result["title"] = extract_title_from_content(proc2.stdout) or infer_title_from_url(url)
                    result["success"] = True
                else:
                    result["error"] = "xreach and jina both failed"
                    
        elif content_type in ["youtube", "bilibili"]:
            proc = subprocess.run(
                ["yt-dlp", "--dump-json", "--no-download", url],
                capture_output=True, text=True, timeout=30
            )
            if proc.returncode == 0:
                data = json.loads(proc.stdout)
                result["title"] = data.get("title", "")
                result["author"] = data.get("uploader", "")
                result["content"] = f"Video Description:\n{data.get('description', '')}"
                result["success"] = True
            else:
                result["error"] = f"yt-dlp failed: {proc.stderr[:200]}"
                
        else:
            # Default: jina.ai reader
            jina_url = f"https://r.jina.ai/{url}"
            proc = subprocess.run(
                ["curl", "-sL", "--max-time", "30", jina_url],
                capture_output=True, text=True, timeout=35
            )
            if proc.returncode == 0 and len(proc.stdout) > 100:
                result["content"] = proc.stdout
                result["title"] = extract_title_from_content(proc.stdout) or infer_title_from_url(url)
                result["success"] = True
            else:
                result["error"] = f"jina fetch failed: {len(proc.stdout)} chars"
                
    except Exception as e:
        result["error"] = str(e)
        
    if not result.get("title"):
        result["title"] = infer_title_from_url(url)
    return result


def generate_slug(title: str, date: datetime) -> str:
    """Generate filename slug."""
    date_str = date.strftime("%Y-%m-%d")
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[\s]+', '-', slug)[:50].rstrip('-')
    return f"{slug}-{date_str}"


def determine_library_path(content_type: str) -> str:
    """Determine which subdirectory to save to."""
    type_to_dir = {
        "wechat": "articles", "tweet": "tweets", "youtube": "videos",
        "bilibili": "videos", "podcast": "podcasts", "paper": "papers",
    }
    return os.path.join(LIBRARY_ROOT, type_to_dir.get(content_type, "articles"))


def split_into_chunks(text: str, chunk_size: int = 1800, overlap: int = 250) -> list:
    """Split long text into overlapping chunks for vector indexing."""
    text = (text or "").strip()
    if not text:
        return []
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(n, start + chunk_size)
        chunks.append(text[start:end])
        if end >= n:
            break
        start = max(end - overlap, start + 1)
    return chunks


def summarize_text(text: str, title: str = "") -> str:
    """Simple extractive summary without calling an external LLM."""
    text = (text or "").strip()
    if not text:
        return ""
    paras = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    summary_parts = []
    if title:
        summary_parts.append(f"这篇内容主要围绕《{title}》。")
    for p in paras[:2]:
        p = re.sub(r'\s+', ' ', p)
        if len(p) > 220:
            p = p[:220].rstrip() + "..."
        summary_parts.append(p)
    return "\n\n".join(summary_parts[:3])


def extract_tags(text: str, title: str, content_type: str, url: str = "") -> list:
    """Heuristic tags from title/content/url."""
    base = f"{title}\n{text[:3000]}\n{url}".lower()
    tag_rules = {
        "ai": [" ai ", "llm", "agent", "gpt", "claude", "gemini", "reasoning"],
        "openclaw": ["openclaw", "claw"],
        "startup": ["startup", "founder", "yc", "创业"],
        "security": ["security", "安全", "secure", "auth"],
        "memory": ["memory", "记忆", "retrieval", "mempalace"],
        "web3": ["web3", "crypto", "blockchain", "chainbase", "链上"],
        "workflow": ["workflow", "pipeline", "orchestration", "协作"],
        "twitter": ["twitter", "x.com", "tweet"],
        "video": ["youtube", "bilibili", "video"],
    }
    tags = [content_type]
    for tag, needles in tag_rules.items():
        if any(n in base for n in needles):
            tags.append(tag)
    host = urlparse(url).netloc.replace('www.', '') if url else ''
    if host:
        tags.append(host.split(':')[0])
    # de-dup preserve order
    out = []
    seen = set()
    for t in tags:
        if t and t not in seen:
            out.append(t)
            seen.add(t)
    return out[:8]


def find_related_entries(query: str, limit: int = 3, exclude_source: str = "") -> list:
    """Find related items already stored in library wing."""
    result = search_memories(query, palace_path=_config.palace_path, wing=LIBRARY_WING, n_results=limit + 8)
    rows = result.get("results", []) if isinstance(result, dict) else []
    existing = {p.name for p in Path(LIBRARY_ROOT).rglob('*.md')}
    related = []
    seen = set()
    for r in rows:
        source = r.get("source_file", "")
        if not source or source == exclude_source or source in seen or source not in existing:
            continue
        seen.add(source)
        related.append(source)
        if len(related) >= limit:
            break
    return related


def create_entry_file(url: str, content_type: str, data: dict, summary: str = "", tags: list = None, related: list = None) -> str:
    """Create a library entry file with full original content preserved."""
    now = datetime.now()
    title = data.get("title") or "Untitled"
    filename = generate_slug(title, now) + ".md"
    
    save_dir = determine_library_path(content_type)
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, filename)
    
    if os.path.exists(filepath):
        base, ext = os.path.splitext(filepath)
        counter = 1
        while os.path.exists(filepath):
            filepath = f"{base}-{counter}{ext}"
            counter += 1
    
    frontmatter = {
        "title": title,
        "source": content_type,
        "url": url,
        "author": data.get("author", ""),
        "date_published": data.get("date", ""),
        "date_saved": now.strftime("%Y-%m-%d"),
        "last_updated": now.strftime("%Y-%m-%d"),
        "type": content_type,
        "tags": tags or [],
        "status": "unread",
        "priority": "normal",
        "related": related or [],
    }

    key_points = [f"- {t}" for t in (tags or [])[:4]] or ["- "]
    related_lines = [f"- [[library/{item}]]" for item in (related or [])]
    content = f"""---
{json.dumps(frontmatter, indent=2, ensure_ascii=False)}
---

# {title}

## Summary

{summary}

## Key Points

{chr(10).join(key_points)}

## Original Content

{data.get("content", "*Content fetch failed or empty*")}

## Notes

## Related

{chr(10).join(related_lines)}
"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def index_full_document(col, filepath: str, title: str, content: str, content_type: str, url: str = "", tags: list = None):
    """Index full document in chunks into MemPalace using upsert."""
    chunks = split_into_chunks(content)
    if not chunks:
        chunks = [title]
    stem = Path(filepath).name
    ids = [f"library::{stem}::{i}" for i in range(len(chunks))]
    docs = [f"{title}\n\n{chunk}" for chunk in chunks]
    metas = []
    for i, chunk in enumerate(chunks):
        metas.append({
            "wing": LIBRARY_WING,
            "room": content_type,
            "hall": "facts",
            "source_file": stem,
            "source_path": filepath,
            "source_url": url,
            "title": title,
            "chunk_index": i,
            "chunk_count": len(chunks),
            "tags": ",".join(tags or []),
            "filed_at": datetime.now().isoformat(),
            "agent": "shandian",
        })
    col.upsert(documents=docs, metadatas=metas, ids=ids)
    return len(chunks)


def remove_existing_url_entries(url: str):
    """Remove existing library markdown files for same URL to avoid duplicates during re-save."""
    removed = []
    if not os.path.exists(LIBRARY_ROOT):
        return removed
    for md in Path(LIBRARY_ROOT).rglob('*.md'):
        try:
            txt = md.read_text(encoding='utf-8', errors='ignore')
            if f'"url": "{url}"' in txt:
                removed.append(str(md))
                md.unlink()
        except Exception:
            pass
    return removed


def remove_existing_url_index(url: str):
    """Delete previously indexed chunks for the same URL from ChromaDB."""
    col = _get_collection(create=True)
    if not col:
        return 0
    try:
        rows = col.get(where={"source_url": url}, include=[])
        ids = rows.get("ids", []) if isinstance(rows, dict) else []
        if ids:
            col.delete(ids=ids)
            return len(ids)
    except Exception:
        pass
    return 0


# ===== COMMANDS =====

def cmd_status(args):
    """宫殿状态概览"""
    col = _get_collection()
    if not col:
        print("❌ No palace found. Run: mempalace init && mempalace mine")
        return
    count = col.count()
    wings = {}
    rooms = {}
    all_meta = col.get(include=["metadatas"])["metadatas"]
    for m in all_meta:
        w = m.get("wing", "unknown")
        r = m.get("room", "unknown")
        wings[w] = wings.get(w, 0) + 1
        rooms[r] = rooms.get(r, 0) + 1

    print(f"📦 MemPalace — {count} drawers")
    print(f"   Palace: {_config.palace_path}")
    print()
    print("  Wings:")
    for w, c in sorted(wings.items(), key=lambda x: -x[1]):
        print(f"    {w}: {c} drawers")
    print()
    print("  Rooms:")
    for r, c in sorted(rooms.items(), key=lambda x: -x[1])[:10]:
        print(f"    {r}: {c} drawers")


def cmd_search(args):
    """语义搜索（全部 wings）"""
    query = " ".join(args.query)
    result = search_memories(
        query, palace_path=_config.palace_path,
        wing=args.wing, room=args.room, n_results=args.limit or 5,
    )
    results = result.get("results", []) if isinstance(result, dict) else []

    if not results:
        print(f"🔍 No results for: {query}")
        return

    print(f"🔍 Results for: \"{query}\"")
    print()
    for i, r in enumerate(results, 1):
        wing = r.get("wing", "?")
        room = r.get("room", "?")
        source = r.get("source_file", "?")
        doc = r.get("text", "")[:400]
        print(f"  [{i}] {wing}/{room} | {source}")
        print(f"      {doc}...")
        print()


def cmd_find(args):
    """搜索 library wing（已保存内容）"""
    query = " ".join(args.query)
    result = search_memories(
        query, palace_path=_config.palace_path,
        wing=LIBRARY_WING, n_results=args.limit or 5,
    )
    results = result.get("results", []) if isinstance(result, dict) else []

    if not results:
        print(f"📚 No library results for: {query}")
        return

    print(f"📚 Library results for: \"{query}\"")
    print()
    for i, r in enumerate(results, 1):
        room = r.get("room", "?")
        source = r.get("source_file", "?")
        doc = r.get("text", "")[:300]
        print(f"  [{i}] {room} | {source}")
        print(f"      {doc}...")
        print()


def cmd_save(args):
    """保存 URL 到 library，并完整索引原文。"""
    url = args.url
    content_type = args.type or detect_url_type(url)
    
    print(f"📎 URL detected as: {content_type}")
    print("   Fetching content...")
    data = fetch_content(url, content_type)
    if args.title:
        data["title"] = args.title
    
    if not data["success"]:
        print(f"⚠️  Fetch warning: {data.get('error', 'unknown')}")
        print("   Saving anyway (you can edit the file later)")
    
    try:
        removed = remove_existing_url_entries(url)
        removed_chunks = remove_existing_url_index(url)
        title = data.get("title", "Untitled")
        full_content = data.get("content", "")
        summary = summarize_text(full_content, title)
        tags = extract_tags(full_content, title, content_type, url)
        related = find_related_entries(f"{title}\n{summary}", exclude_source="")
        filepath = create_entry_file(url, content_type, data, summary=summary, tags=tags, related=related)
        print(f"✅ Saved to: {filepath}")
        
        col = _get_collection(create=True)
        if col:
            chunk_count = index_full_document(col, filepath, title, full_content, content_type, url=url, tags=tags)
            print(f"✅ Indexed full text to MemPalace ({chunk_count} chunks)")
        if removed or removed_chunks:
            print(f"♻️ Replaced {len(removed)} old file(s), removed {removed_chunks} old chunk(s)")
        print(f"🏷️ Tags: {', '.join(tags)}")
        if related:
            print(f"🔗 Related: {', '.join(related[:3])}")
    except Exception as e:
        print(f"❌ Error saving: {e}")


def cmd_add(args):
    """添加记忆到 Palace"""
    col = _get_collection(create=True)
    if not col:
        print("❌ Failed to open palace")
        return

    content = " ".join(args.content)
    now = datetime.now().isoformat()
    doc_id = f"manual_{now}_{hash(content) % 10000}"

    metadata = {
        "wing": args.wing or "general", "room": args.room or "general",
        "hall": getattr(args, 'hall', None) or "facts", "source_file": "manual_entry",
        "filed_at": now, "agent": "shandian",
    }

    col.add(documents=[content], metadatas=[metadata], ids=[doc_id])
    print(f"✅ Added to {metadata['wing']}/{metadata['room']}")
    print(f"   ID: {doc_id}")


def cmd_list(args):
    """列出 library 内容"""
    if not os.path.exists(LIBRARY_ROOT):
        print("📚 Library is empty")
        return
    
    content_type = getattr(args, 'type', None)
    
    if content_type:
        target_dir = os.path.join(LIBRARY_ROOT, content_type)
        if os.path.exists(target_dir):
            files = sorted([f for f in os.listdir(target_dir) if f.endswith('.md')])
            print(f"📚 {content_type}: {len(files)} entries")
            for f in files[:20]:
                print(f"  - {f}")
            if len(files) > 20:
                print(f"  ... and {len(files) - 20} more")
        else:
            print(f"📚 No entries for: {content_type}")
    else:
        total = 0
        for subdir in sorted(os.listdir(LIBRARY_ROOT)):
            subdir_path = os.path.join(LIBRARY_ROOT, subdir)
            if os.path.isdir(subdir_path):
                files = [f for f in os.listdir(subdir_path) if f.endswith('.md')]
                total += len(files)
                print(f"📁 {subdir}: {len(files)} entries")
        print(f"\n📚 Total: {total} entries")


def cmd_graph(args):
    """知识图谱操作"""
    if args.graph_cmd == "query":
        entity = " ".join(args.entity)
        results = _kg.query_entity(entity, as_of=getattr(args, 'as_of', None))
        if not results:
            print(f"🧠 No graph entries for: {entity}")
            return
        print(f"🧠 Knowledge Graph — {entity}")
        for r in results:
            status = "✅" if not r.get("valid_until") else f"❌ ({r['valid_until']})"
            print(f"  {status} {r['subject']} → {r['predicate']} → {r['object']}")

    elif args.graph_cmd == "add":
        _kg.add_triple(args.subject, args.predicate, args.object,
                       valid_from=getattr(args, 'valid_from', None) or datetime.now().strftime("%Y-%m-%d"))
        print(f"✅ Added: {args.subject} → {args.predicate} → {args.object}")

    elif args.graph_cmd == "invalidate":
        _kg.invalidate(args.subject, args.predicate, args.object,
                       ended=getattr(args, 'ended', None) or datetime.now().strftime("%Y-%m-%d"))
        print(f"❌ Invalidated: {args.subject} → {args.predicate} → {args.object}")

    elif args.graph_cmd == "timeline":
        entity = " ".join(args.entity)
        timeline = _kg.timeline(entity)
        if not timeline:
            print(f"📅 No timeline for: {entity}")
            return
        print(f"📅 Timeline — {entity}")
        for t in timeline:
            print(f"  [{t.get('valid_from', '?')}] {t['subject']} → {t['predicate']} → {t['object']}")

    elif args.graph_cmd == "stats":
        stats = _kg.stats()
        print("🧠 Knowledge Graph Stats")
        print(f"  Triples: {stats.get('triples', 0)}")
        print(f"  Entities: {stats.get('entities', 0)}")
        print(f"  Current facts: {stats.get('current_facts', 0)}")
        print(f"  Expired facts: {stats.get('expired_facts', 0)}")
        rel = stats.get('relationship_types', [])
        print(f"  Relationship types: {len(rel)}")

    elif args.graph_cmd == "enrich":
        added = 0
        # core workspace facts
        core = [
            ("King", "prefers", "direct_communication"),
            ("King", "prefers", "concise_responses"),
            ("King", "works_in", "Web3"),
            ("Shandian", "uses_memory", "MemPalace"),
            ("MemPalace", "stores", "full_text_in_library_files"),
            ("MemPalace", "indexes", "chunked_text_in_chromadb"),
            ("library", "is_part_of", "MemPalace"),
        ]
        for s,p,o in core:
            try:
                _kg.add_triple(s,p,o, valid_from=datetime.now().strftime("%Y-%m-%d"))
                added += 1
            except Exception:
                pass
        # enrich from library entries
        for md in Path(LIBRARY_ROOT).rglob('*.md'):
            try:
                txt = md.read_text(encoding='utf-8', errors='ignore')
                if not txt.startswith('---\n{'):
                    continue
                end = txt.find('\n---', 4)
                if end == -1:
                    continue
                meta = json.loads(txt[4:end])
                title = meta.get('title') or md.stem
                source = meta.get('source') or 'article'
                author = meta.get('author')
                url = meta.get('url')
                _kg.add_triple(title, 'content_type', str(meta.get('type', source)), valid_from=meta.get('date_saved') or datetime.now().strftime('%Y-%m-%d'))
                added += 1
                if author:
                    _kg.add_triple(title, 'author', author, valid_from=meta.get('date_saved') or datetime.now().strftime('%Y-%m-%d'))
                    added += 1
                if url:
                    host = urlparse(url).netloc.replace('www.', '')
                    if host:
                        _kg.add_triple(title, 'source_domain', host, valid_from=meta.get('date_saved') or datetime.now().strftime('%Y-%m-%d'))
                        added += 1
            except Exception:
                pass
        print(f"✅ Enriched knowledge graph with ~{added} triples")


def cmd_wake(args):
    """加载 L0+L1 唤醒上下文"""
    os.system("mempalace wake-up" + (f" --wing {args.wing}" if getattr(args, 'wing', None) else ""))


def cmd_mine(args):
    """挖矿"""
    cmd = f"mempalace mine {args.dir}"
    if getattr(args, 'mode', None): cmd += f" --mode {args.mode}"
    if getattr(args, 'wing', None): cmd += f" --wing {args.wing}"
    os.system(cmd)


def main():
    parser = argparse.ArgumentParser(description="mp — MemPalace + Link Library")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="Palace overview")
    
    p_search = sub.add_parser("search", help="Semantic search all wings")
    p_search.add_argument("query", nargs="+")
    p_search.add_argument("--wing", "-w")
    p_search.add_argument("--room", "-r")
    p_search.add_argument("--limit", "-n", type=int, default=5)
    
    p_find = sub.add_parser("find", help="Search library wing")
    p_find.add_argument("query", nargs="+")
    p_find.add_argument("--limit", "-n", type=int, default=5)
    
    p_save = sub.add_parser("save", help="Save URL to library")
    p_save.add_argument("url")
    p_save.add_argument("--type", "-t", choices=["article", "tweet", "video", "podcast", "paper", "wechat", "youtube", "bilibili"])
    p_save.add_argument("--title")
    
    p_add = sub.add_parser("add", help="Add memory")
    p_add.add_argument("content", nargs="+")
    p_add.add_argument("--wing", "-w", default="general")
    p_add.add_argument("--room", "-r", default="general")
    p_add.add_argument("--hall", "-l", default="facts")
    
    p_list = sub.add_parser("list", help="List library contents")
    p_list.add_argument("type", nargs="?", choices=["articles", "tweets", "videos", "podcasts", "papers", "images", "misc"])
    
    p_wake = sub.add_parser("wake", help="Load L0+L1 context")
    p_wake.add_argument("--wing", "-w")
    
    # graph
    p_graph = sub.add_parser("graph", help="Knowledge graph")
    graph_sub = p_graph.add_subparsers(dest="graph_cmd")
    
    g_query = graph_sub.add_parser("query", help="Query entity")
    g_query.add_argument("entity", nargs="+")
    g_query.add_argument("--as-of")
    
    g_add = graph_sub.add_parser("add", help="Add triple")
    g_add.add_argument("subject")
    g_add.add_argument("predicate")
    g_add.add_argument("object")
    g_add.add_argument("--valid-from")
    
    g_inv = graph_sub.add_parser("invalidate", help="Invalidate triple")
    g_inv.add_argument("subject")
    g_inv.add_argument("predicate")
    g_inv.add_argument("object")
    g_inv.add_argument("--ended")
    
    g_timeline = graph_sub.add_parser("timeline", help="Entity timeline")
    g_timeline.add_argument("entity", nargs="+")
    
    graph_sub.add_parser("stats", help="Knowledge graph stats")
    graph_sub.add_parser("enrich", help="Enrich graph from library/workspace")
    
    p_mine = sub.add_parser("mine", help="Mine files")
    p_mine.add_argument("dir")
    p_mine.add_argument("--mode", choices=["projects", "convos"])
    p_mine.add_argument("--wing")

    args = parser.parse_args()
    
    cmds = {
        "status": cmd_status, "search": cmd_search, "find": cmd_find,
        "save": cmd_save, "add": cmd_add, "list": cmd_list,
        "graph": cmd_graph, "wake": cmd_wake, "mine": cmd_mine,
    }

    if args.command in cmds:
        cmds[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
