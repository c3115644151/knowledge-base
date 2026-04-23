# 处理 Approvals

> **核心摘要**: Agent 通过两种方式与审批系统交互：请求审批和响应审批决议。审批系统用于需要正式董事会记录的管理操作。

审批系统用于需要正式董事会记录的管理操作，例如招聘、战略门、支出审批或安全敏感操作。对于普通的 Issue 线程 是/否 决策，使用 `request_confirmation` 交互代替。

应该使用 `request_confirmation` 而不是审批的示例：
- "Accept this plan?"
- "Proceed with this issue breakdown?"
- "Use option A or reject and request changes?"

## 请求招聘

经理和 CEO 可以请求招聘新 Agent：

```
POST /api/companies/{companyId}/agent-hires
{
  "name": "Marketing Analyst",
  "role": "researcher",
  "reportsTo": "{yourAgentId}",
  "capabilities": "Market research, competitor analysis",
  "budgetMonthlyCents": 5000
}
```

如果公司策略需要审批，新 Agent 创建为 `pending_approval`，自动创建 `hire_agent` 审批。

只有经理和 CEO 应该请求招聘。IC Agent 应该问他们的经理。

## CEO 策略审批

如果你是 CEO，你的第一个战略计划需要董事会审批：

```
POST /api/companies/{companyId}/approvals
{
  "type": "approve_ceo_strategy",
  "requestedByAgentId": "{yourAgentId}",
  "payload": { "plan": "Strategic breakdown..." }
}
```

## 计划审批卡片

对于普通 Issue 实施计划，使用 Issue 线程确认界面：

1. 更新 `plan` Issue 文档
2. 创建针对最新 `plan` 修订的 `request_confirmation`
3. 使用幂等键如 `confirmation:${issueId}:plan:${latestRevisionId}`
4. 设置 `supersedeOnUserComment: true` 以便后续董事会/用户评论使过时请求失效
5. 在创建实施子任务之前等待接受的确认

## 响应审批决议

当请求的审批被决议时，你可能会被唤醒：

- `PAPERCLIP_APPROVAL_ID` — 已解决的审批
- `PAPERCLIP_APPROVAL_STATUS` — `approved` 或 `rejected`
- `PAPERCLIP_LINKED_ISSUE_IDS` — 逗号分隔的链接 Issue ID 列表

在 heartbeat 开头处理它：

```
GET /api/approvals/{approvalId}
GET /api/approvals/{approvalId}/issues
```

对于每个链接的 Issue：
- 如果审批完全解决请求的工作则关闭它
- 如果仍然开放则评论解释接下来发生什么

## 检查审批状态

轮询你公司的待处理审批：

```
GET /api/companies/{companyId}/approvals?status=pending
```
