# HTTP Adapter

> **核心摘要**: `http` adapter 向外部 Agent 服务发送 webhook 请求。Agent 在外部运行，Paperclip 只触发它。

## 何时使用

- Agent 作为外部服务运行（云函数、专用服务器）
- 即发即忘调用模式
- 与第三方 Agent 平台集成

## 何时不使用

- 如果 Agent 在同一台机器上本地运行（使用 `process`、`claude_local` 或 `codex_local`）
- 如果需要 stdout 捕获和实时运行查看

## 配置

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `url` | string | 是 | 要 POST 的 Webhook URL |
| `headers` | object | 否 | 额外的 HTTP 头 |
| `timeoutSec` | number | 否 | 请求超时 |

## 工作原理

1. Paperclip 向配置的 URL 发送 POST 请求
2. 请求体包括执行上下文（Agent ID、任务信息、唤醒原因）
3. 外部 Agent 处理请求并回调 Paperclip API
4. Webhook 的响应被捕获为运行结果

## 请求体

Webhook 接收包含以下内容的 JSON payload：

```json
{
  "runId": "...",
  "agentId": "...",
  "companyId": "...",
  "context": {
    "taskId": "...",
    "wakeReason": "...",
    "commentId": "..."
  }
}
```

外部 Agent 使用 `PAPERCLIP_API_URL` 和 API 密钥回调 Paperclip。
