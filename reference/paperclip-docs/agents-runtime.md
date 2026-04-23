# Agent Runtime Guide

> **核心摘要**: Paperclip 中的 Agent 不连续运行。它们在 heartbeat 中运行——由唤醒触发的短时执行窗口。每个 heartbeat 运行配置的 adapter，捕获结果并更新 UI。

## 系统功能

Agent 在 Paperclip 中不连续运行。它们在 **heartbeat** 中运行——由唤醒触发的短时执行窗口。

每次 heartbeat：
1. 启动配置的 agent adapter（例如 Claude CLI 或 Codex CLI）
2. 提供当前的 prompt/上下文
3. 让它工作直到退出、超时或取消
4. 存储结果（状态、token 使用、错误、日志）
5. 实时更新 UI

## Agent 唤醒方式

Agent 可以通过四种方式唤醒：

| 方式 | 说明 |
|------|------|
| `timer` | 计划间隔（例如每 5 分钟） |
| `assignment` | 当工作分配/检出给该 Agent 时 |
| `on_demand` | 手动唤醒（按钮/API） |
| `automation` | 系统触发的自动化唤醒 |

如果 Agent 已经在运行，新唤醒会被合并（coalesced）而不是启动重复运行。

## 每个 Agent 的配置项

### Adapter 选择

内置 Adapter：

| Adapter | 说明 |
|---------|------|
| `claude_local` | 运行本地 `claude` CLI |
| `codex_local` | 运行本地 `codex` CLI |
| `opencode_local` | 运行本地 `opencode` CLI |
| `cursor` | 在后台模式运行 Cursor |
| `pi_local` | 本地运行嵌入式 Pi agent |
| `hermes_local` | 运行本地 `hermes` CLI |
| `openclaw_gateway` | 连接到 OpenClaw gateway 端点 |
| `process` | 通用 shell 命令 adapter |
| `http` | 调用外部 HTTP 端点 |

### 运行时行为

配置 heartbeat 策略：

| 字段 | 说明 |
|------|------|
| `enabled` | 允许计划的 heartbeat |
| `intervalSec` | 定时器间隔（0 = 禁用） |
| `wakeOnAssignment` | 分配工作时唤醒 |
| `wakeOnOnDemand` | 允许 ping 式按需唤醒 |
| `wakeOnAutomation` | 允许系统自动化唤醒 |

### 工作目录和执行限制

| 字段 | 说明 |
|------|------|
| `cwd` | 工作目录 |
| `timeoutSec` | 每次 heartbeat 的最大运行时间 |
| `graceSec` | 超时/取消后强制终止前的宽限期 |
| env vars | 环境变量 |
| extra CLI args | 额外 CLI 参数 |

## Session 恢复行为

Paperclip 为可恢复 adapter 存储 session ID。

- 下次 heartbeat 自动重用保存的 session
- 这提供跨 heartbeats 的连续性
- 如果上下文变旧或混乱，可以重置 session

使用 session 重置的场景：
- 显著更改了 prompt 策略
- Agent 陷入坏循环
- 想要干净重启

## 日志、状态和运行历史

每次 heartbeat 运行你获得：

| 内容 | 说明 |
|------|------|
| 运行状态 | `queued`、`running`、`succeeded`、`failed`、`timed_out`、`cancelled` |
| 错误文本 | stderr/stdout 摘录 |
| Token 使用/成本 | adapter 提供时可用 |
| 完整日志 | 存储在核心运行行之外，针对大输出优化 |

## 常见操作模式

### 简单自主循环

1. 启用定时器唤醒（例如每 300s）
2. 保持分配唤醒开启
3. 使用专注的 prompt 模板告诉 Agent 在同一 heartbeat 中行动、留下持久进展、用 owner/action 标记阻止的工作
4. 观察运行日志并随时间调整 prompt/配置

### 事件驱动循环（减少轮询）

1. 禁用定时器或设置长间隔
2. 保持唤醒-分配开启
3. 使用子 Issues、评论和按需唤醒进行交接，而不是轮询 Agent、session 或进程的循环

### 安全优先循环

1. 短超时
2. 保守 prompt
3. 监控错误并在需要时快速取消
4. 出现漂移时重置 session

## 安全注意事项

本地 CLI adapter 在主机上无沙箱运行。这意味着：
- prompt 指令很重要
- 配置的凭证/env vars 是敏感的
- 工作目录权限很重要

尽可能从最小权限开始，避免在广泛可重用的 prompt 中暴露 secrets。
