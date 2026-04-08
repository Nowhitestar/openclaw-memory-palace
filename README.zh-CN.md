# OpenClaw Memory Palace

[![Release](https://img.shields.io/github/v/release/Nowhitestar/openclaw-memory-palace?style=flat-square)](https://github.com/Nowhitestar/openclaw-memory-palace/releases)
[![License](https://img.shields.io/github/license/Nowhitestar/openclaw-memory-palace?style=flat-square)](./LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-memory%20upgrade-blue?style=flat-square)](https://github.com/Nowhitestar/openclaw-memory-palace)

把 OpenClaw 从“会翻笔记的助手”升级成“有持续记忆的搭档”。

**OpenClaw Memory Palace** 是我们这次整理出来的可安装记忆系统，核心基于：
- [MemPalace](https://github.com/milla-jovovich/mempalace)
- ChromaDB 语义检索
- SQLite 知识图谱
- 面向 OpenClaw 的 `mp` 包装命令

## 适合谁 / 不适合谁

**适合：**
- 想让 OpenClaw 具备更强语义记忆的人
- 想把对话记忆和链接资料统一起来的人
- 想要本地优先、可控、可扩展记忆系统的人
- 想在不依赖云服务的前提下获得知识图谱能力的人

**不太适合：**
- 想要纯 SaaS 托管方案的人
- 想要完全图形化、零命令行体验的人
- 不打算本地存储数据的人

## 为什么要做它

OpenClaw 本身已经有文件、日志、memory notes，但常见问题是：
- 结构偏扁平
- 信息散落在多个位置
- 语义搜索不够顺手
- 保存的网页资料和对话记忆是分开的

这个项目就是把这些能力统一成一个本地优先的记忆系统。

## 改造前 vs 改造后

### 改造前
- 扁平 markdown 记忆
- Link Library 是独立系统
- 检索更像关键词匹配 / 翻文件
- 实体关系记忆较弱

### 改造后
- 对话记忆 + 链接资料统一搜索
- `library` 成为 MemPalace 的一个 wing
- 有知识图谱能力（`mp graph query` / `mp graph enrich`）
- `mp save` 支持原文保存 + chunk 索引
- 自动生成摘要 / tags / related

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

完整示例见：[`examples/demo-output.txt`](examples/demo-output.txt)

## 你能做什么

- `mp status` — 查看当前记忆状态
- `mp search` — 全局语义搜索
- `mp find` — 只搜索已保存链接
- `mp save <url>` — 保存链接原文并索引进 MemPalace
- `mp graph query <entity>` — 查询知识图谱
- `mp graph enrich` — 从资料里扩充知识图谱
- `mp list` — 浏览已保存资料

## 安装

```bash
git clone https://github.com/Nowhitestar/openclaw-memory-palace.git
cd openclaw-memory-palace
bash install.sh
```

如果执行后找不到 `mp`，把下面这行加进 shell 配置：

```bash
export PATH="$HOME/.local/bin:$HOME/Library/Python/3.9/bin:$PATH"
```

## 快速开始

```bash
mp status
mp graph enrich
mp save https://github.com/milla-jovovich/mempalace
mp find "记忆系统"
mp search "之前为什么这么决定"
```

更多示例见：[`examples/quickstart.md`](examples/quickstart.md)

## 存储方式

### 1. 原文存档
`mp save` 会把完整原文保存到：

```text
~/.openclaw/workspace-main/library/
```

### 2. 语义索引
同一份内容会被切 chunk 后写入 MemPalace / ChromaDB，用于召回和搜索。

### 3. 知识图谱
实体和关系保存在：

```text
~/.mempalace/knowledge_graph.sqlite3
```

## 仓库内容

```text
bin/mp.py              # OpenClaw 记忆命令封装
install.sh             # 一键安装脚本
upgrade.sh             # 升级脚本
uninstall.sh           # 卸载脚本
README.md              # English 文档
README.zh-CN.md        # 中文文档
docs/FAQ.md            # 常见问题
docs/RELEASE_NOTES_v0.1.0.md
examples/quickstart.md # 使用示例
examples/demo-output.txt
```

## 隐私说明

- 这个仓库**不会**上传你的私人记忆文件。
- 上传的是可复用的系统和安装脚本。
- 你的实际记忆、资料、知识图谱仍然保留在本地。

## 升级

```bash
bash upgrade.sh
```

## 卸载

```bash
bash uninstall.sh
```

注意：卸载只移除包装层，不会删除你的本地记忆数据。

## FAQ

见 [`docs/FAQ.md`](docs/FAQ.md)

## 致谢

底层能力基于 Milla Jovovich / Ben Sigman 的 MemPalace。

## License

MIT
