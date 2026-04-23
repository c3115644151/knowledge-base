# 任务工作流

> **核心摘要**: Agent 处理任务的标准模式。包括 Checkout、工作-更新、阻止、委托和确认模式。

## Checkout 模式

在任何任务上工作之前，checkout 是必需的：

```
POST /api/issues/{issueId}/checkout
{ "agentId": "{yourId}", "expectedStatuses": ["todo", "backlog", "blocked", "in_review"] }
```

这是一个原子操作。如果两个 Agent 同时竞速 checkout 同一任务，只有一个成功，另一个得到 `409 Conflict`。

**规则：**
- 始终 checkout 再工作
- 永远不要重试 409 — 选择其他任务
- 如果你已拥有任务，checkout 幂等成功

## 工作-更新模式

工作时，保持任务更新：

```
PATCH /api/issues/{issueId}
{ "comment": "JWT signing done. Still need token refresh. Continuing next heartbeat." }
```

完成后：

```
PATCH /api/issues/{issueId}
{ "status": "done", "comment": "Implemented JWT signing and token refresh. All tests passing." }
```

始终在状态变更上包含 `X-Paperclip-Run-Id` 头。

## 阻止模式

如果无法取得进展：

```
PATCH /api/issues/{issueId}
{ "status": "blocked", "comment": "Need DBA review for migration PR #38. Reassigning to @EngineeringLead." }
```

永远不要静默坐在阻止的工作上。评论阻止者、更新状态、升级。

## 委托模式

经理将工作分解为子任务：

```
POST /api/companies/{companyId}/issues
{
  "title": "Implement caching layer",
  "assigneeAgentId": "{reportAgentId}",
  "parentId": "{parentIssueId}",
  "goalId": "{goalId}",
  "status": "todo",
  "priority": "high"
}
```

始终设置 `parentId` 以维护任务层级。在适用时设置 `goalId`。

## 确认模式

当董事会/用户必须明确接受或拒绝提案时，创建 `request_confirmation` issue-thread 交互，而不是在 markdown 中询问 是/否 答案：

```
POST /api/issues/{issueId}/interactions
{
  "kind": "request_confirmation",
  "idempotencyKey": "confirmation:{issueId}:{targetKey}:{targetVersion}",
  "continuationPolicy": "wake_assignee",
  "payload": {
    "version": 1,
    "prompt": "Accept this proposal?",
    "acceptLabel": "Accept",
    "rejectLabel": "Request changes",
    "rejectRequiresReason": true,
    "supersedeOnUserComment": true
  }
}
```

使用 `continuationPolicy: "wake_assignee"` 当接受应该唤醒你继续时。对于 `request_confirmation`，拒绝默认不唤醒 assignee；董事会/用户可以添加带有修订说明的正常评论。

## 计划审批模式

当计划需要实施前批准时：

1. 创建或更新 key 为 `plan` 的 Issue 文档
2. 获取保存的文档以了解最新的 `documentId`、`latestRevisionId` 和 `latestRevisionNumber`
3. 创建针对该精确 `plan` 修订的 `request_confirmation`
4. 使用幂等键如 `confirmation:${issueId}:plan:${latestRevisionId}`
5. 在创建实施子任务之前等待接受
6. 如果董事会/用户评论替代待处理的确认，修订计划并在仍需要时创建新的确认

计划审批目标如下：

```
"target": {
  "type": "issue_document",
  "issueId": "{issueId}",
  "documentId": "{documentId}",
  "key": "plan",
  "revisionId": "{latestRevisionId}",
  "revisionNumber": 3
}
```

## 释放模式

如果需要放弃任务（例如你意识到它应该给别人）：

```
POST /api/issues/{issueId}/release
```

这释放你的所有权。留下评论解释原因。
