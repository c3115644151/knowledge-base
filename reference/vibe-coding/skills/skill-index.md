# 技能能力映射 (Skill Capability Map)

> **文档类型**：技能详细能力映射
> **格式**：技能名 → 核心能力 → 使用场景 → 关键命令

---

## 一、元技能

### skills-skills

| 属性 | 内容 |
|:---|:---|
| **核心能力** | 生成针对特定领域的 Skill |
| **使用场景** | 需要创建自定义 AI 能力封装 |
| **输入** | 领域资料（文档、代码、规范） |
| **输出** | 专用 SKILL.md 文件 |

### sop-generator

| 属性 | 内容 |
|:---|:---|
| **核心能力** | 生成和规范化 SOP（标准操作流程） |
| **使用场景** | 需要建立可复用操作流程 |

---

## 二、AI 工具

### canvas-dev

| 属性 | 内容 |
|:---|:---|
| **核心能力** | Canvas 白板驱动开发，AI 架构总师 |
| **使用场景** | 复杂架构设计、多人协作 |
| **关键概念** | 图形是第一公民，代码是白板序列化 |

### headless-cli

| 属性 | 内容 |
|:---|:---|
| **核心能力** | 无头模式 AI CLI 调用（Gemini/Claude/Codex） |
| **使用场景** | 批量任务、自动化流程 |
| **支持模型** | Gemini、Claude、Codex |

### claude-code-guide

| 属性 | 内容 |
|:---|:---|
| **核心能力** | Claude Code CLI 使用指南 |
| **关键命令** | /init, /rewind, /clear, /compact |
| **使用场景** | 本地开发、深度代码交互 |

### tmux-autopilot

| 属性 | 内容 |
|:---|:---|
| **核心能力** | tmux 自动化操控（AI蜂群协作） |
| **关键命令** | capture-pane, send-keys |
| **使用场景** | 多 AI 并行任务、互相监控 |

---

## 三、数据库

### postgresql

| 属性 | 内容 |
|:---|:---|
| **核心能力** | PostgreSQL 完整专家技能 |
| **使用场景** | 数据库设计、查询优化、PL/pgSQL |
| **关键能力** | SQL 编写、索引优化、事务管理 |

---

## 四、加密货币/量化交易

### ccxt

| 属性 | 内容 |
|:---|:---|
| **核心能力** | 加密货币交易所统一 API |
| **支持交易所** | Binance, OKX, Bybit 等 100+ |
| **使用场景** | 跨交易所交易机器人 |

### polymarket

| 属性 | 内容 |
|:---|:---|
| **核心能力** | 预测市场 API |
| **使用场景** | 市场预测、数据分析 |

---

## 五、开发工具

### telegram-dev

| 属性 | 内容 |
|:---|:---|
| **核心能力** | Telegram Bot 开发 |
| **使用场景** | 消息推送、自动化交互 |

### twscrape

| 属性 | 内容 |
|:---|:---|
| **核心能力** | Twitter/X 数据抓取 |
| **使用场景** | 社交媒体数据分析 |

---

## 六、技能选择决策树

```
FUNCTION select_skill(任务需求)
  │
  ├─► IF 架构设计需求
  │     └─► canvas-dev
  │
  ├─► IF 批量 AI 任务
  │     └─► headless-cli + tmux-autopilot
  │
  ├─► IF 数据库相关
  │     └─► postgresql
  │
  ├─► IF 加密货币相关
  │     ├─► 交易所交易 → ccxt
  │     └─► 预测市场 → polymarket
  │
  ├─► IF 消息通知
  │     └─► telegram-dev
  │
  └─► IF 社交媒体数据
        └─► twscrape

END FUNCTION
```

---

## 七、技能组合推荐

| 场景 | 推荐技能组合 |
|:---|:---|
| 加密货币量化交易 | ccxt + postgresql + telegram-dev |
| 社交媒体监控 | twscrape + telegram-dev + postgresql |
| 复杂 AI 协作 | canvas-dev + headless-cli + tmux-autopilot |
| 数据采集服务 | postgresql + 相关 API 技能 |

---

**映射版本**：v1.0
**来源**：tukuaiai/vibe-coding-cn
