# 记忆提供者

Hermes Agent 附带 8 个外部记忆提供者插件，提供持久化、跨会话知识。**一次只能激活一个**外部提供者——内置记忆始终与它一起工作。

## 快速开始

```bash
hermes memory setup  # 交互式选择器 + 配置
hermes memory status  # 检查活动提供者
hermes memory off     # 禁用外部提供者
```

或在 `~/.hermes/config.yaml` 手动设置：
```yaml
memory:
  provider: openviking  # 或 honcho, mem0, hindsight, holographic, retaindb, byterover, supermemory
```

## 可用提供者

### Honcho

AI 原生跨会话用户建模，辩证问答、语义搜索、持久结论。

| 最佳用途 | 多代理系统跨会话上下文、用户代理对齐 |
|----------|--------------------------------------|
| 需求 | `pip install honcho-ai` + API 密钥 |
| 存储 | Honcho Cloud 或自托管 |
| 成本 | 按量计费（云）/ 免费（自托管） |

**工具**：`honcho_profile`、`honcho_search`、`honcho_context`、`honcho_conclude`

### OpenViking

字节跳动火山引擎上下文数据库，文件系统风格知识层级、分层检索、6 类自动记忆提取。

| 最佳用途 | 自托管知识管理、结构化浏览 |
|----------|---------------------------|
| 需求 | `pip install openviking` + 运行服务器 |
| 存储 | 自托管（本地或云） |
| 成本 | 免费（开源，AGPL-3.0） |

**工具**：`viking_search`、`viking_read`、`viking_browse`、`viking_remember`、`viking_add_resource`

### Mem0

服务器端 LLM 事实提取，语义搜索、重排序、自动去重。

| 最佳用途 | 放手记忆管理 — Mem0 自动处理提取 |
|----------|----------------------------------|
| 需求 | `pip install mem0ai` + API 密钥 |
| 存储 | Mem0 Cloud |
| 成本 | Mem0 定价 |

**工具**：`mem0_profile`、`mem0_search`、`mem0_conclude`

### Hindsight

长期记忆，知识图谱、实体解析、多策略检索。`hindsight_reflect` 工具提供跨记忆综合。

| 最佳用途 | 基于知识图谱的召回与实体关系 |
|----------|---------------------------|
| 需求 | 云：API 密钥。本地：LLM API 密钥 |
| 存储 | Hindsight Cloud 或本地嵌入式 PostgreSQL |
| 成本 | 按量计费（云）/ 免费（本地） |

**工具**：`hindsight_retain`、`hindsight_recall`、`hindsight_reflect`

### Holographic

本地 SQLite 事实存储，FTS5 全文搜索、信任评分、HRR（全息归约表示）代数查询。

| 最佳用途 | 仅本地记忆、高级检索、无外部依赖 |
|----------|---------------------------|
| 需求 | 无（SQLite 始终可用）。NumPy 可选用于 HRR |
| 存储 | 本地 SQLite |
| 成本 | 免费 |

**工具**：`fact_store`（9 种操作）、`fact_feedback`

### RetainDB

云记忆 API，混合搜索（Vector + BM25 + Reranking）、7 种记忆类型、增量压缩。

| 最佳用途 | 已使用 RetainDB 基础设施的团队 |
|----------|---------------------------|
| 需求 | RetainDB 账户 + API 密钥 |
| 存储 | RetainDB Cloud |
| 成本 | $20/月 |

**工具**：`retaindb_profile`、`retaindb_search`、`retaindb_context`、`retaindb_remember`、`retaindb_forget`

### ByteRover

通过 `brv` CLI 的持久记忆——分层知识树、分层检索。本地优先，可选云同步。

| 最佳用途 | 需要便携、本地优先记忆和 CLI 的开发者 |
|----------|---------------------------|
| 需求 | ByteRover CLI |
| 存储 | 本地（默认）或 ByteRover Cloud |
| 成本 | 免费（本地）/ 按量计费（云） |

**工具**：`brv_query`、`brv_curate`、`brv_status`

### Supermemory

语义长期记忆，画像召回、语义搜索、显式记忆工具，通过 Supermemory 图 API 的会话结束对话提取。

| 最佳用途 | 用户画像和会话级图构建的语义召回 |
|----------|---------------------------|
| 需求 | `pip install supermemory` + API 密钥 |
| 存储 | Supermemory Cloud |
| 成本 | Supermemory 定价 |

**工具**：`supermemory_store`、`supermemory_search`、`supermemory_forget`、`supermemory_profile`

## 提供者比较

| 提供者 | 存储 | 成本 | 工具数 | 依赖 | 独特功能 |
|--------|------|------|--------|------|----------|
| **Honcho** | 云 | 付费 | 4 | `honcho-ai` | 辩证用户建模 |
| **OpenViking** | 自托管 | 免费 | 5 | `openviking` + 服务器 | 文件系统层级 + 分层加载 |
| **Mem0** | 云 | 付费 | 3 | `mem0ai` | 服务器端 LLM 提取 |
| **Hindsight** | 云/本地 | 免费/付费 | 3 | `hindsight-client` | 知识图谱 + 反思综合 |
| **Holographic** | 本地 | 免费 | 2 | 无 | HRR 代数 + 信任评分 |
| **RetainDB** | 云 | $20/月 | 5 | `requests` | 增量压缩 |
| **ByteRover** | 本地/云 | 免费/付费 | 3 | `brv` CLI | 预压缩提取 |
| **Supermemory** | 云 | 付费 | 4 | `supermemory` | 上下文围栏 + 会话图提取 + 多容器 |
