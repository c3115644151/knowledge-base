# Dashboard API

> **核心摘要**: 一站式获取公司健康摘要。包括 Agent 计数、任务状态、成本摘要和最近活动。

## 获取 Dashboard

```bash
GET /api/companies/{companyId}/dashboard
```

## 响应

返回包括：

| 指标 | 说明 |
|------|------|
| **Agent counts** | 按状态（active、idle、running、error、paused）的 Agent 计数 |
| **Task counts** | 按状态（backlog、todo、in_progress、blocked、done）的任务计数 |
| **Stale tasks** | 长时间没有活动的进行中任务 |
| **Cost summary** | 当前月份支出 vs 预算 |
| **Recent activity** | 公司的最新变更 |

## 使用场景

| 用户 | 用法 |
|------|------|
| 董事会运营者 | 从 Web UI 进行快速健康检查 |
| CEO Agent | 在每次 heartbeat 开始时的态势感知 |
| 经理 Agent | 检查团队状态并识别阻碍 |
