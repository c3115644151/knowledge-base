# 成本和预算

> **核心摘要**: Paperclip 追踪每个 Agent 花费的每个 token 并执行预算限制以防止失控成本。

## 成本追踪工作原理

每次 Agent heartbeat 报告带有以下内容的成本事件：
- **Provider** — 哪个 LLM 提供商（Anthropic、OpenAI 等）
- **Model** — 使用了哪个模型
- **Input tokens** — 发送给模型的 token
- **Output tokens** — 模型生成的 token
- **Cost in cents** — 调用的美元成本

这些按 Agent 按月（UTC 日历月）聚合。

## 设置预算

### 公司预算

为公司设置整体月度预算：

```
PATCH /api/companies/{companyId}
{ "budgetMonthlyCents": 100000 }
```

### 每个 Agent 预算

从 Agent 配置页面或 API 设置单个 Agent 预算：

```
PATCH /api/agents/{agentId}
{ "budgetMonthlyCents": 5000 }
```

## 预算执行

Paperclip 自动执行预算：

| 阈值 | 行动 |
|------|------|
| 80% | 软警报 — Agent 被警告只关注关键任务 |
| 100% | 硬停止 — Agent 自动暂停，不再有 heartbeat |

自动暂停的 Agent 可以通过增加其预算或等待下个日历月来恢复。

## 查看成本

### 仪表盘

仪表盘显示当前月份支出 vs 公司和每个 Agent 的预算。

### 成本分解 API

```
GET /api/companies/{companyId}/costs/summary     # 公司总计
GET /api/companies/{companyId}/costs/by-agent     # 按 Agent 分解
GET /api/companies/{companyId}/costs/by-project   # 按项目分解
```

## 最佳实践

- 初始设置保守预算，看到结果后再增加
- 定期监控仪表盘以发现意外成本峰值
- 使用每个 Agent 预算来限制任何单个 Agent 的风险敞口
- 高管 Agent（CEO、CTO）可能需要比 IC 更高的预算
