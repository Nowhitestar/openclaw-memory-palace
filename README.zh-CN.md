<div align="center">

# OpenClaw Memory Palace

### OpenClaw 增强版 MemPalace：对话记忆 + 链接知识库 + 知识图谱，统一成一个本地优先的系统。

[![Release](https://img.shields.io/github/v/release/Nowhitestar/openclaw-memory-palace?style=flat-square)](https://github.com/Nowhitestar/openclaw-memory-palace/releases)
[![License](https://img.shields.io/github/license/Nowhitestar/openclaw-memory-palace?style=flat-square)](./LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-%E9%9B%86%E6%88%90-blue?style=flat-square)](https://github.com/openclaw/openclaw)
[![MemPalace](https://img.shields.io/badge/%E5%9F%BA%E4%BA%8E-MemPalace-black?style=flat-square)](https://github.com/milla-jovovich/mempalace)

<br>

[快速开始](#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B) · [你能得到什么](#%E4%BD%A0%E8%83%BD%E5%BE%97%E5%88%B0%E4%BB%80%E4%B9%88) · [日常怎么用](#%E6%97%A5%E5%B8%B8%E6%80%8E%E4%B9%88%E7%94%A8) · [架构](#%E6%9E%B6%E6%9E%84) · [FAQ](docs/FAQ.md)

</div>

---

很多 agent 对话里才有真正的决策、取舍、debug 过程。
但大多数系统要么：
- 只把它们堆成扁平 markdown，难以语义导航；
- 要么把“保存链接”做成另一套系统，和对话记忆割裂。

**OpenClaw Memory Palace** 是一个“面向 OpenClaw 的 MemPalace 增强层”：
- `mp save` 把链接**原文**归档到 OpenClaw `library/`
- 同时把内容按 chunk 索引进 MemPalace / ChromaDB，用于语义检索
- SQLite 知识图谱 + `mp graph enrich`，把资料元信息转成实体关系
- 统一命令面：`mp`

本仓库只提供可复用系统：**不会上传你的任何私人记忆数据**。


## 快速开始

### 方式 A（推荐）：clone 安装

```bash
git clone https://github.com/Nowhitestar/openclaw-memory-palace.git
cd openclaw-memory-palace
bash install.sh

mp status
mp graph enrich
mp save https://github.com/milla-jovovich/mempalace --title "MemPalace GitHub"
mp find "记忆系统"
mp search "之前为什么这么决定"
```

### 方式 B：一行命令（建议先看脚本再跑）

```bash
curl -fsSL https://raw.githubusercontent.com/Nowhitestar/openclaw-memory-palace/main/install.sh | bash
```

如果执行后找不到 `mp`，把下面这行加进 shell 配置：

```bash
export PATH="$HOME/.local/bin:$(python3 -m site --user-base)/bin:$PATH"
```


## 你能得到什么

### 1) 一个统一的记忆入口
- OpenClaw 对话记忆（来自 `memory/`）
- 链接知识库（来自 `library/`，不再是独立系统）
- 知识图谱（实体关系可查询）

统一通过：
- `mp search …`（全局）
- `mp find …`（只搜 library）
- `mp graph query …`

### 2) 原文可读、可编辑
`mp save` 会写出 markdown 文件，包含：
- 完整原文
- 自动摘要
- tags
- related（语义相关条目）

### 3) 语义检索更稳
同一份内容会被切成多个 chunk 索引进 MemPalace，长文检索更好用。


## 日常怎么用

你不需要“维护数据库”。你照常工作，记忆系统跟着走。

### 保存链接（Link Library 变成 MemPalace 的一个 wing）
```bash
mp save https://example.com/article
mp save https://x.com/user/status/123
mp save https://mp.weixin.qq.com/s/xxx
```

### 搜索
```bash
mp search "auth 决策"
mp find "agent workflow"
```

### 知识图谱
```bash
mp graph enrich
mp graph stats
mp graph query OpenClaw
```

### 浏览
```bash
mp list
mp list articles
mp list tweets
```


## 架构

**原文（source of truth）：**
- `~/.openclaw/workspace-main/library/`

**向量索引（语义检索）：**
- `~/.mempalace/palace`（ChromaDB）
- 内容按 overlap chunk 方式入库

**知识图谱：**
- `~/.mempalace/knowledge_graph.sqlite3`

### 相比原生 MemPalace，这个项目多了什么？

MemPalace 是引擎。
这个仓库是面向 OpenClaw 的“产品层”：

- ✅ 链接保存工作流（`mp save`）：写 OpenClaw `library/` + 分块索引
- ✅ OpenClaw 友好的浏览/检索命令（`mp find` / `mp list`）
- ✅ 知识图谱增强（`mp graph enrich` 从 library 元信息生成 triples）
- ✅ 本地优先 + 人类可读


## 仓库内容

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


## 隐私说明

- 本仓库不会上传你的私人记忆
- 只发布可复用脚本和代码
- 你的数据始终留在本地


## 升级 / 卸载

```bash
bash upgrade.sh
bash uninstall.sh
```


## 致谢

底层能力基于 MemPalace（Milla Jovovich & Ben Sigman）。


## License

MIT
