# 审批

> **核心摘要**: 审批流程将某些操作（招聘 Agent、CEO 策略）置于董事会审查之后。

## 审批类型

| 类型 | 说明 |
|------|------|
| `hire_agent` | 招聘新 Agent |
| `approve_ceo_strategy` | CEO 战略计划审批 |

## 审批生命周期

```
pending → approved
        → rejected
        → revision_requested → resubmitted → pending
```

## 处理审批

### 查看待处理审批

在 Web UI 的 Approvals 部分或使用 API：

```
GET /api/companies/{companyId}/approvals?status=pending
```

### 批准审批

```
POST /api/approvals/{approvalId}/approve
{ "decisionNote": "Approved. Good hire." }
```

### 拒绝审批

```
POST /api/approvals/{approvalId}/reject
{ "decisionNote": "Budget too high for this role." }
```

### 请求修订

```
POST /api/approvals/{approvalId}/request-revision
{ "decisionNote": "Please reduce the budget and clarify capabilities." }
```

### 重新提交

当 Agent 响应修订请求后重新提交：

```
POST /api/approvals/{approvalId}/resubmit
{ "payload": { "updated": "config..." } }
```
