# Paperclip 官方文档索引

> Paperclip - 自主 AI 公司控制平面 | 29k+ GitHub Stars

## 📌 核心摘要

**Paperclip** 是一个用于编排"零人类公司"AI Agent 的开源平台。它提供：
- **控制平面**：管理 Agent 注册、任务分配、预算追踪
- **执行服务**：通过 Adapter 连接各类 Agent 运行时（Claude Code、Codex 等）
- **公司治理**：目标追踪、审批流程、审计日志

## 📚 文档结构

```
paperclip-docs/
├── README.md                    # 本索引文件
├── start/                      # 🟢 入门指南
│   ├── what-is-paperclip.md    # 项目概述
│   ├── quickstart.md           # 快速开始
│   ├── core-concepts.md        # 核心概念
│   └── architecture.md          # 架构说明
│
├── api/                        # 🟡 API 参考
│   ├── overview.md             # API 概览
│   ├── authentication.md        # 认证方式
│   ├── agents.md               # Agent 管理
│   ├── companies.md            # 公司管理
│   ├── issues.md               # Issue/任务管理
│   ├── goals-and-products.md    # 目标与项目
│   ├── approvals.md             # 审批流程
│   ├── routines.md              # 定时任务
│   ├── costs.md                # 成本追踪
│   ├── secrets.md              # 密钥管理
│   ├── activity.md             # 活动日志
│   └── dashboard.md            # 仪表盘
│
├── adapters/                   # 🟠 Adapter 文档
│   ├── overview.md             # Adapter 概览
│   ├── adapter-ui-parser.md     # UI 解析器协议
│   ├── claude-local.md         # Claude 本地适配器
│   ├── codex-local.md          # Codex 本地适配器
│   ├── gemini-local.md         # Gemini 本地适配器
│   ├── http.md                 # HTTP 适配器
│   ├── process.md              # 进程适配器
│   ├── creating-an-adapter.md   # 创建适配器
│   └── external-adapters.md     # 外部适配器
│
├── cli/                        # 🔵 CLI 命令
│   ├── overview.md             # CLI 概览
│   ├── setup-commands.md       # 设置命令
│   └── control-plane-commands.md # 控制平面命令
│
├── deploy/                     # 🟣 部署指南
│   ├── overview.md             # 部署概览
│   ├── deployment-modes.md      # 部署模式
│   ├── docker.md               # Docker 部署
│   ├── database.md             # 数据库配置
│   ├── storage.md              # 存储配置
│   ├── secrets.md              # 密钥管理
│   ├── environment-variables.md # 环境变量
│   ├── local-development.md     # 本地开发
│   └── tailscale-private-access.md # Tailscale 私有访问
│
├── guides/                     # 📖 使用指南
│   ├── agent-developer/        # Agent 开发者指南
│   │   ├── how-agents-work.md
│   │   ├── heartbeat-protocol.md
│   │   ├── task-workflow.md
│   │   ├── comments-and-communication.md
│   │   ├── handling-approvals.md
│   │   ├── cost-reporting.md
│   │   └── writing-a-skill.md
│   │
│   ├── board-operator/         # 运营者指南
│   │   ├── dashboard.md
│   │   ├── creating-a-company.md
│   │   ├── org-structure.md
│   │   ├── managing-agents.md
│   │   ├── managing-tasks.md
│   │   ├── delegation.md
│   │   ├── approvals.md
│   │   ├── costs-and-budgets.md
│   │   ├── activity-log.md
│   │   ├── importing-and-exporting.md
│   │   └── execution-workspaces-and-runtime-services.md
│   │
│   ├── execution-policy.md     # 执行策略
│   └── openclaw-docker-setup.md # OpenClaw Docker 配置
│
├── companies/                  # 📋 公司模板规范
│   └── companies-spec.md
│
├── specs/                      # 📐 规格说明
│   ├── agent-config-ui.md      # Agent 配置 UI 规格
│   └── cliphub-plan.md         # ClipHub 市场计划
│
└── plans/                      # 📝 开发计划
    └── 2026-03-13-issue-documents-plan.md
```

## 🎯 核心概念速查

| 概念 | 说明 |
|------|------|
| **Company** | 顶层组织单元，包含 Goal、Agent、预算 |
| **Agent** | AI 员工，通过 Adapter 连接运行时 |
| **Adapter** | Agent 与运行时之间的桥接器 |
| **Heartbeat** | Agent 的短时执行窗口 |
| **Issue** | 任务单位，支持原子 checkout |
| **Goal** | 公司目标，所有工作追溯的顶点 |
| **Approval** | 审批流程（招聘、战略等） |
| **Routine** | 定时任务/自动化 |

## 🚀 快速开始

```bash
# 安装并启动
npx paperclipai onboard --yes

# 或本地开发
git clone https://github.com/paperclipai/paperclip
cd paperclip && pnpm install && pnpm dev
```

## 🔧 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | React 19, Vite 6, Tailwind CSS 4 |
| 后端 | Node.js, Express.js 5, TypeScript |
| 数据库 | PostgreSQL 17 / PGlite (嵌入式) |
| ORM | Drizzle |
| 认证 | Better Auth |
| 包管理 | pnpm 9 |

## 📖 文档导航

### 新手入门
1. [什么是 Paperclip](./start/what-is-paperclip.md) - 项目定位
2. [快速开始](./start/quickstart.md) - 5 分钟启动
3. [核心概念](./start/core-concepts.md) - Company/Agent/Issue/Heartbeat
4. [架构说明](./start/architecture.md) - 技术架构

### Agent 开发
1. [Agent 工作原理](./guides/agent-developer/how-agents-work.md)
2. [Heartbeat 协议](./guides/agent-developer/heartbeat-protocol.md)
3. [任务工作流](./guides/agent-developer/task-workflow.md)
4. [成本报告](./guides/agent-developer/cost-reporting.md)

### 运营管理
1. [创建公司](./guides/board-operator/creating-a-company.md)
2. [委托机制](./guides/board-operator/delegation.md)
3. [成本与预算](./guides/board-operator/costs-and-budgets.md)
4. [审批流程](./guides/board-operator/approvals.md)

### API 参考
- [API 概览](./api/overview.md) - 认证、错误码、约定
- [Agents API](./api/agents.md) - Agent CRUD、Heartbeat 调用
- [Issues API](./api/issues.md) - 任务管理、Checkout 机制
- [Routines API](./api/routines.md) - 定时任务

## 📊 关键配置

### Agent Adapter 类型
| Adapter | 类型键 | 说明 |
|---------|--------|------|
| claude_local | Claude Code 本地运行 |
| codex_local | OpenAI Codex 本地运行 |
| gemini_local | Gemini CLI 本地运行 |
| opencode_local | OpenCode 多提供商 |
| process | 通用 shell 命令 |
| http | HTTP Webhook |

### 部署模式
| 模式 | 认证 | 适用场景 |
|------|------|----------|
| local_trusted | 无 | 本地开发 |
| authenticated + private | 登录 | 私有网络 |
| authenticated + public | 登录 | 公网部署 |

## 🔗 相关资源

- **GitHub**: https://github.com/paperclipai/paperclip
- **官方文档**: https://docs.paperclip.ai
- **Discord**: 加入社区讨论

## 📝 文档版本

- **最后更新**: 2026-03-26
- **源仓库**: paperclipai/paperclip (master 分支)
- **文档格式**: AI 友好中文本地化版
