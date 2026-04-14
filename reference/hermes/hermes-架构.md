# Hermes Agent 架构

## 整体架构

Hermes Agent 是一个模块化的 AI Agent 系统，由以下几个核心组件构成：

```
┌─────────────────────────────────────────────────────────────┐
│                        CLI / Gateway                         │
│                   (终端界面 / 消息网关)                       │
├─────────────────────────────────────────────────────────────┤
│                      AIAgent Core                           │
│                  (Agent 核心推理引擎)                        │
├──────────────────┬──────────────────┬────────────────────────┤
│   Tools System   │  Skills System   │   Memory System        │
│   (工具系统)     │   (技能系统)     │   (记忆系统)           │
├──────────────────┴──────────────────┴────────────────────────┤
│                     Providers Layer                         │
│              (LLM 提供商：OpenRouter, Anthropic...)          │
└─────────────────────────────────────────────────────────────┘
```

## 核心组件

### 1. AIAgent Core
Agent 的核心推理引擎，负责：
- 管理对话上下文
- 决策工具调用
- 处理用户输入/输出
- 协调各子系统

### 2. Tools System (工具系统)
扩展 Agent 能力的函数集合，按功能分组为工具集：

| 工具集 | 包含工具 |
|--------|----------|
| `terminal` | 文件操作、终端命令执行 |
| `web` | 网页搜索、内容提取 |
| `memory` | 记忆读写、用户画像 |
| `skills` | 技能安装、查看、搜索 |
| `delegation` | 子代理委托 |
| `code_execution` | Python RPC 执行 |
| `send_message` | 跨平台消息发送 |

### 3. Skills System (技能系统)
按需加载的知识文档，用于：
- 复杂任务的分步指导
- 外部工具/服务的使用说明
- 项目特定的上下文

### 4. Memory System (记忆系统)
持久化存储，包括：
- **MEMORY.md** - Agent 学到的知识
- **USER.md** - 用户画像和偏好
- **上下文文件** - `.hermes.md`, `AGENTS.md`, `.cursorrules`
- **外部提供者** - Honcho, Mem0, OpenViking

### 5. Providers Layer (提供商层)
支持多种 LLM 提供商：
- OpenRouter (多提供商路由)
- Anthropic (Claude 原生)
- OpenAI (GPT 系列)
- Nous Portal (订阅服务)
- GitHub Copilot
- 自定义端点 (Ollama, vLLM)

## 两种运行模式

### CLI 模式
```
hermes
```
完整的终端界面，支持：
- 多行输入
- Slash 命令
- 工具进度动画
- 会话恢复

### Gateway 模式
```
hermes gateway run
```
消息网关，连接多个平台：
- Telegram Bot
- Discord Bot
- Slack App
- WhatsApp
- Signal
- Email
- Home Assistant

## 配置管理

### 优先级 (高→低)
1. CLI 参数 (如 `--model anthropic/claude-4`)
2. `~/.hermes/config.yaml`
3. `~/.hermes/.env`
4. 内置默认值

### 目录结构
```
~/.hermes/
├── config.yaml         # 主配置
├── .env                 # 密钥
├── auth.json            # OAuth 凭证
├── SOUL.md              # Agent 身份
├── memories/
│   ├── MEMORY.md        # 知识记忆
│   └── USER.md          # 用户画像
├── skills/              # 技能目录
├── sessions/            # 会话历史
├── cron/                # 定时任务
├── hooks/               # 事件钩子
├── logs/
└── plugins/              # 插件
```

## 扩展机制

### MCP (Model Context Protocol)
连接外部工具服务器，无需编写原生工具：
```yaml
mcp_servers:
  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "***"
```

### Plugins
自定义工具、钩子和集成的插件系统：
```
~/.hermes/plugins/
└── my-plugin/
    ├── plugin.yaml
    └── src/
```

### Terminal Backends
命令执行的后端选择：

| 后端 | 隔离 | 用途 |
|------|------|------|
| `local` | 无 | 开发调试 |
| `docker` | 容器 | 生产安全 |
| `ssh` | 远程 | 强大硬件 |
| `modal` | 云沙箱 | 弹性计算 |
| `singularity` | 容器 | HPC 环境 |

## 关键设计原则

1. **安全优先** - 危险命令审批、MCP 凭证过滤、提示注入检测
2. **持久化** - 会话、记忆、技能跨会话保留
3. **模块化** - 工具集、技能、记忆系统均可插拔
4. **多平台** - 单一 Agent 连接所有消息平台
