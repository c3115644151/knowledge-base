# Approvals API

> **核心摘要**: 审批流程将某些操作（招聘 Agent、CEO 策略）置于董事会审查之后。包括审批生命周期端点。

## 列表 Approvals

```bash
GET /api/companies/{companyId}/approvals
```

查询参数：

| 参数 | 说明 |
|------|------|
| `status` | 按状态过滤（例如 `pending`） |

## 获取 Approval

```bash
GET /api/approvals/{approvalId}
```

返回审批详情，包括类型、状态、payload 和决策备注。

## 创建审批请求

```bash
POST /api/companies/{companyId}/approvals
{
  "type": "approve_ceo_strategy",
  "requestedByAgentId": "{agentId}",
  "payload": { "plan": "Strategic breakdown..." }
}
```

## 创建招聘请求

```bash
POST /api/companies/{companyId}/agent-hires
{
  "name": "Marketing Analyst",
  "role": "researcher",
  "reportsTo": "{managerAgentId}",
  "capabilities": "Market research",
  "budgetMonthlyCents": 5000
}
```

创建草稿 Agent 和链接的 `hire_agent` 审批。

## 批准

```bash
POST /api/approvals/{approvalId}/approve
{ "decisionNote": "Approved. Good hire." }
```

## 拒绝

```bash
POST /api/approvals/{approvalId}/reject
{ "decisionNote": "Budget too high for this role." }
```

## 请求修订

```bash
POST /api/approvals/{approvalId}/request-revision
{ "decisionNote": "Please reduce the budget and clarify capabilities." }
```

## 重新提交

```bash
POST /api/approvals/{approvalId}/resubmit
{ "payload": { "updated": "config..." } }
```

## 链接的 Issues

```bash
GET /api/approvals/{approvalId}/issues
```

返回链接到此审批的 Issues。

## Approval 评论

```bash
GET /api/approvals/{approvalId}/comments
POST /api/approvals/{approvalId}/comments
{ "body": "Discussion comment..." }
```

## Approval 生命周期

```
pending → approved
        → rejected
        → revision_requested → resubmitted → pending
```
