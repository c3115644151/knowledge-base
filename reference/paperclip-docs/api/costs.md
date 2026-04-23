# Costs API

> **核心摘要**: 追踪跨 Agent、项目和公司的 token 使用情况和支出。包括成本事件报告和预算管理。

## 报告成本事件

```bash
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

通常由 Adapter 在每次 heartbeat 后自动报告。

## 公司成本摘要

```bash
GET /api/companies/{companyId}/costs/summary
```

返回当前月份的总支出、预算和利用率。

## 按 Agent 成本

```bash
GET /api/companies/{companyId}/costs/by-agent
```

返回当前月份按 Agent 的成本明细。

## 按项目成本

```bash
GET /api/companies/{companyId}/costs/by-project
```

返回当前月份按项目的成本明细。

## 预算管理

### 设置公司预算

```bash
PATCH /api/companies/{companyId}
{ "budgetMonthlyCents": 100000 }
```

### 设置 Agent 预算

```bash
PATCH /api/agents/{agentId}
{ "budgetMonthlyCents": 5000 }
```

## 预算执行

| 阈值 | 效果 |
|------|------|
| 80% | 软警报 — Agent 应专注于关键任务 |
| 100% | 硬停止 — Agent 自动暂停 |

预算窗口在每月第一天（UTC）重置。
