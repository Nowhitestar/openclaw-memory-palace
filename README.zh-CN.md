# OpenClaw Memory Palace

给 OpenClaw 用的一键记忆升级包。

这个项目把我们这次改造出来的记忆系统整理成了可安装版本，核心基于：
- [MemPalace](https://github.com/milla-jovovich/mempalace)
- ChromaDB 语义检索
- SQLite 知识图谱
- 面向 OpenClaw 的 `mp` 包装命令

## 它解决了什么问题

改造前：
- 记忆主要是扁平 markdown
- Link Library 是独立系统
- 检索更像关键词匹配 / 翻文件

改造后：
- 对话记忆 + 链接资料统一进一个系统
- `library` 成为 MemPalace 的一个 wing
- 有知识图谱能力
- `mp save` 会保存原文、分块索引、生成摘要 / tags / related

## 主要能力

- `mp status` — 查看当前记忆状态
- `mp search` — 全局语义搜索
- `mp find` — 只搜索已保存链接
- `mp save <url>` — 保存链接原文并索引进 MemPalace
- `mp graph query <entity>` — 查询知识图谱
- `mp graph enrich` — 从资料中扩充知识图谱
- `mp list` — 浏览已保存资料

## 安装

```bash
git clone https://github.com/Nowhitestar/openclaw-memory-palace.git
cd openclaw-memory-palace
bash install.sh
```

如果命令找不到，再把下面这行加进 shell 配置：

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

## 存储方式

### 原文存档
`mp save` 会把完整原文保存到：

```text
~/.openclaw/workspace-main/library/
```

### 语义索引
同一份内容会被切 chunk 后写入 MemPalace / ChromaDB，用来做召回检索。

### 知识图谱
实体和关系会存到：

```text
~/.mempalace/knowledge_graph.sqlite3
```

## 仓库内容

```text
bin/mp.py          # OpenClaw 记忆命令封装
install.sh         # 一键安装脚本
README.md          # English 说明
README.zh-CN.md    # 中文说明
```

## 说明

- 这个仓库**不会**上传你的私人记忆文件。
- 上传的只是可复用的系统和安装脚本。
- 你的实际记忆、资料、知识图谱仍然保留在本地。

## 致谢

底层能力基于 Milla Jovovich / Ben Sigman 的 MemPalace。

## License

MIT
