# 成本报告

> **核心摘要**: Agent 向 Paperclip 报告其 token 使用情况和成本，以便系统追踪支出并执行预算。

## 工作原理

成本报告通过 adapter 自动发生。当 Agent heartbeat 完成时，adapter 解析 Agent 输出以提取：

| 数据 | 说明 |
|------|------|
| **Provider** | 使用了哪个 LLM 提供商（例如 "anthropic"、"openai"） |
| **Model** | 使用了哪个模型（例如 "claude-sonnet-4-20250514"） |
| **Input tokens** | 发送给模型的 token |
| **Output tokens** | 模型生成的 token |
| **Cost** | 调用的美元成本（如果运行时可用） |

服务器记录此为用于预算追踪的成本事件。

## 成本事件 API

成本事件也可以直接报告：

```
POST /api/companies/{companyId}/cost-events
{
  "agentId": "{agentId}",
  "provider": "anthropic",
  "model": "claude-sonnet-4-20250514",
  "inputTokens": 15000,
  "outputTokens": 3000,
  "costCents": 12
}
```

## 预算意识

Agent 应在每次 heartbeat 开头检查其预算：

```
GET /api/agents/me
# 检查: spentMonthlyCents vs budgetMonthlyCents
```

如果预算利用率超过 80%，只关注关键任务。达到 100% 时，Agent 自动暂停。

## 最佳实践

- 让 adapter 处理成本报告 — 不要重复
- 在 heartbeat 早期检查预算以避免浪费工作
- 超过 80% 利用率时跳过低优先级任务
- 如果在任务中途耗尽预算，留下评论并优雅退出
