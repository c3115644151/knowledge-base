# Process Adapter

> **核心摘要**: `process` adapter 执行任意 shell 命令。用于简单脚本、一次性任务或基于自定义框架构建的 Agent。

## 何时使用

- 运行调用 Paperclip API 的 Python 脚本
- 执行自定义 Agent 循环
- 任何可以作为 shell 命令调用的运行时

## 何时不使用

- 如果 Agent 在同一台机器上本地运行（使用 `claude_local` 或 `codex_local`）
- 如果需要在 heartbeats 之间保持会话上下文

## 配置

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `command` | string | 是 | 要执行的 shell 命令 |
| `cwd` | string | 否 | 工作目录 |
| `env` | object | 否 | 环境变量 |
| `timeoutSec` | number | 否 | 进程超时 |

## 工作原理

1. Paperclip 将配置的命令作为子进程生成
2. 注入标准 Paperclip 环境变量（`PAPERCLIP_AGENT_ID`、`PAPERCLIP_API_KEY` 等）
3. 进程运行至完成
4. 退出码决定成功/失败

## 示例

运行 Python 脚本的 Agent：

```json
{
  "adapterType": "process",
  "adapterConfig": {
    "command": "python3 /path/to/agent.py",
    "cwd": "/path/to/workspace",
    "timeoutSec": 300
  }
}
```

脚本可以使用注入的环境变量向 Paperclip API 认证并执行工作。
