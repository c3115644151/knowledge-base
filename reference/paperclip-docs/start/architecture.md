# 架构说明

> **核心摘要**: Paperclip 是一个 monorepo，包含四层：React UI、Express.js API、PostgreSQL 数据库、Adapter 执行层。控制平面编排 Agent，但不运行 Agent。

## 技术栈概览

```
┌─────────────────────────────────────┐
│  React UI (Vite)                    │
│  Dashboard, org management, tasks   │
├─────────────────────────────────────┤
│  Express.js REST API (Node.js)      │
│  Routes, services, auth, adapters   │
├─────────────────────────────────────┤
│  PostgreSQL (Drizzle ORM)           │
│  Schema, migrations, embedded mode  │
├─────────────────────────────────────┤
│  Adapters                           │
│  Claude Local, Codex Local,         │
│  Process, HTTP                      │
└─────────────────────────────────────┘
```

## 技术栈详情

| 层级 | 技术 |
|------|------|
| 前端 | React 19, Vite 6, React Router 7, Radix UI, Tailwind CSS 4, TanStack Query |
| 后端 | Node.js 20+, Express.js 5, TypeScript |
| 数据库 | PostgreSQL 17 (或嵌入式 PGlite), Drizzle ORM |
| 认证 | Better Auth (sessions + API keys) |
| Adapter | Claude Code CLI, Codex CLI, shell process, HTTP webhook |
| 包管理 | pnpm 9 with workspaces |

## 仓库结构

```
paperclip/
├── ui/                          # React 前端
│   ├── src/pages/              # 路由页面
│   ├── src/components/         # React 组件
│   ├── src/api/                # API 客户端
│   └── src/context/            # React context providers
│
├── server/                      # Express.js API
│   ├── src/routes/             # REST 端点
│   ├── src/services/           # 业务逻辑
│   ├── src/adapters/           # Agent 执行 adapter
│   └── src/middleware/         # 认证、日志中间件
│
├── packages/
│   ├── db/                      # Drizzle schema + migrations
│   ├── shared/                  # API 类型、常量、验证器
│   ├── adapter-utils/           # Adapter 接口和辅助函数
│   └── adapters/
│       ├── claude-local/        # Claude Code adapter
│       └── codex-local/         # OpenAI Codex adapter
│
├── skills/                      # Agent skills
│   └── paperclip/               # 核心 Paperclip skill (heartbeat 协议)
│
├── cli/                         # CLI 客户端
│   └── src/                     # 设置和控制平面命令
│
└── doc/                         # 内部文档
```

## 请求流程

当 heartbeat 触发时：

1. **Trigger** — Scheduler、manual invoke、或事件（assignment、mention）触发 heartbeat
2. **Adapter Invocation** — Server 调用配置好的 adapter 的 `execute()` 函数
3. **Agent Process** — Adapter 启动 Agent（例如 Claude Code CLI），传入 Paperclip 环境变量和 prompt
4. **Agent Work** — Agent 调用 Paperclip 的 REST API 检查分配、checkout 任务、执行工作、更新状态
5. **Result Capture** — Adapter 捕获 stdout、解析 usage/cost 数据、提取 session 状态
6. **Run Record** — Server 记录运行结果、成本、以及下次 heartbeat 的 session 状态

## Adapter 模型

Adapter 是 Paperclip 和 Agent 运行时之间的桥接器。每个 Adapter 是一个包含三个模块的包：

| 模块 | 说明 |
|------|------|
| **Server Module** | `execute()` 函数，生成/调用 Agent，加上环境诊断 |
| **UI Module** | stdout 解析器用于运行查看器、用于 Agent 创建的配置表单字段 |
| **CLI Module** | 用于 `paperclipai run --watch` 的终端格式化器 |

内置 Adapter：`claude_local`、`codex_local`、`process`、`http`。你也可以为任何运行时创建自定义 Adapter。

## 关键设计决策

| 决策 | 说明 |
|------|------|
| **控制平面，而非执行平面** | Paperclip 编排 Agent；它不运行 Agent |
| **公司作用域** | 所有实体都属于唯一一家公司；严格的数据边界 |
| **单一 assignee 任务** | 原子 checkout 防止同一任务上的并发工作 |
| **Adapter 无关** | 任何能调用 HTTP API 的运行时都可以作为 Agent |
| **默认嵌入式** | 零配置本地模式，使用嵌入式 PostgreSQL |
