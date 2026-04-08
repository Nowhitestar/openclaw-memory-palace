<div align="center">

<img src="assets/banner.svg" alt="OpenClaw Memory Palace" width="100%">

# OpenClaw Memory Palace

### OpenClaw 增强版 MemPalace：对话记忆 + 链接知识库 + 知识图谱，统一成一个本地优先的系统。

[![Release](https://img.shields.io/github/v/release/Nowhitestar/openclaw-memory-palace?style=flat-square)](https://github.com/Nowhitestar/openclaw-memory-palace/releases)
[![License](https://img.shields.io/github/license/Nowhitestar/openclaw-memory-palace?style=flat-square)](./LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-%E9%9B%86%E6%88%90-blue?style=flat-square)](https://github.com/openclaw/openclaw)
[![MemPalace](https://img.shields.io/badge/%E5%9F%BA%E4%BA%8E-MemPalace-black?style=flat-square)](https://github.com/milla-jovovich/mempalace)

<br>

[快速开始](#快速开始) · [为什么做它](#为什么做它) · [用户实际感知到什么](#用户实际感知到什么) · [架构](#架构) · [FAQ](docs/FAQ.md)

</div>

---

真正有价值的 agent 工作流，都会持续产生记忆：
- 为什么当时这么决策
- 哪篇链接后来真的有用
- 某次 debug 里排除了什么路径
- 某个项目 / 人 / 主题后来发生了什么变化

但大多数系统里，这些记忆是割裂的：
- 对话日志在一处
- 保存的链接在另一处
- 长文检索弱
- 实体关系没有被显式组织起来

**OpenClaw Memory Palace** 做的，是把 MemPalace 变成一个 **OpenClaw 原生记忆层**。
它统一承接：
- 对话记忆
- 链接存档 / 阅读资料库
- 长文本语义检索
- 轻量知识图谱增强

最重要的一点：**普通用户主要应该和 OpenClaw 交互，而不是直接操作 `mp`。**
`mp` 更像底层集成层。


## 快速开始

### 方式 A（推荐）：clone 安装

```bash
git clone https://github.com/Nowhitestar/openclaw-memory-palace.git
cd openclaw-memory-palace
bash install.sh
```

### 方式 B：一行命令（建议先看脚本再跑）

```bash
curl -fsSL https://raw.githubusercontent.com/Nowhitestar/openclaw-memory-palace/main/install.sh | bash
```

如果执行后找不到 `mp`，把下面这行加进 shell 配置：

```bash
export PATH="$HOME/.local/bin:$(python3 -m site --user-base)/bin:$PATH"
```

### 安装验证

```bash
mp status
```

这一步主要用于安装验证 / 运维检查。正常使用时，OpenClaw 应该在后台调用记忆层，用户不需要天天手打这些命令。


## 为什么做它

MemPalace 是很强的记忆引擎。
但 OpenClaw 需要的不只是引擎，还需要一层真正可用的“产品层”：

- 要有地方保存**完整原文**
- 要有从真实对话里触发的**链接保存工作流**
- 要能处理**长文章 / 长线程**的检索
- 要更贴近 **agent 实际工作方式**

这就是这个项目的意义。

它不是“MemPalace + 一个壳”。
它是一个建立在 MemPalace 之上的、面向 OpenClaw 的记忆系统。


## 用户实际感知到什么

理想状态下，用户体验应该是：

1. 你照常跟 OpenClaw 聊天。
2. 你发一篇链接、让它记住一件事，或者之后再问“我们之前怎么决定的？”
3. OpenClaw 在后台自动存储 / 检索记忆。
4. 你获得更强的上下文连续性，而不是手动管理存储系统。

典型的用户表述会是：
- “帮我总结这篇，顺便存一下。”
- “把我之前存的那篇 agent memory 文章找出来。”
- “我们为什么后来换方案了？”
- “上个月关于 auth 是怎么定的？”

另见：[`examples/user-flow.md`](examples/user-flow.md)


## 你能得到什么

### 1) 一个统一的记忆面
- OpenClaw 对话记忆
- OpenClaw `library/` 里的链接知识库
- 实体关系知识图谱

### 2) 原文仍然可读、可编辑
保存的链接会以 markdown 形式落盘，并带上：
- 完整原文
- 摘要
- tags
- related 条目

### 3) 更适合 agent 的检索方式
长文会被切成 overlap chunks 索引进 MemPalace / ChromaDB，召回更稳。

### 4) 默认本地优先
- 文件在本地
- 向量库在本地
- 图谱在本地


## 高级 / 运维命令

这些命令更多是给安装、调试、运维、power user 用的。
普通用户日常不应该依赖它们。

```bash
mp status
mp search "之前为什么这么决定"
mp find "agent workflow"
mp save <url>
mp graph enrich
mp graph query <entity>
mp list
```


## 架构

```text
User
  │
  │ 正常聊天 / 分享链接 / 追问过去发生过什么
  ▼
OpenClaw agent
  │
  ├─ 需要时召回记忆
  ├─ 合适时保存链接
  └─ 查询相关实体 / 决策
  ▼
mp（内部集成层）
  │
  ├─ library 文件（source of truth）
  ├─ MemPalace / ChromaDB（语义检索）
  └─ SQLite knowledge graph（实体 + 关系）
```

更详细见：[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

### 存储布局

**原文真源（files）：**
- `~/.openclaw/workspace-main/library/`

**语义索引（vectors）：**
- `~/.mempalace/palace`
- 文档按 overlapping chunks 入库

**知识图谱（SQLite）：**
- `~/.mempalace/knowledge_graph.sqlite3`


## 相比原生 MemPalace，多了什么？

MemPalace 是引擎。
这个仓库是在它之上做的 OpenClaw 记忆产品层。

- ✅ 把原来的 Link Library 思路变成 MemPalace-backed 工作流
- ✅ 完整原文落在 OpenClaw `library/`
- ✅ 长内容按 chunk 索引，提高检索可用性
- ✅ 从 library 元信息生成图谱增强
- ✅ 保持本地优先 + 人类可读


## 仓库内容

```text
assets/banner.svg
bin/mp.py
install.sh
upgrade.sh
uninstall.sh
README.md
README.zh-CN.md
docs/ARCHITECTURE.md
docs/FAQ.md
docs/OPENCLAW_INTEGRATION.md
docs/RELEASE_NOTES_v0.1.0.md
examples/quickstart.md
examples/demo-output.txt
examples/user-flow.md
```


## 隐私说明

- 本仓库不会上传你的私人记忆
- 只发布可复用代码和脚本
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
