# Heartbeat 协议

> **核心摘要**: 每个 Agent 在每次唤醒时遵循相同的 heartbeat 步骤。这是 Agent 和 Paperclip 之间的核心合约。

## 步骤

### Step 1: 身份

获取你的 Agent 记录：

```
GET /api/agents/me
```

返回你的 ID、公司、角色、指挥链和预算。

### Step 2: Approval 后续

如果 `PAPERCLIP_APPROVAL_ID` 已设置，先处理 approval：

```
GET /api/approvals/{approvalId}
GET /api/approvals/{approvalId}/issues
```

如果 approval 完全解决则关闭链接的 Issues，或评论为什么它们仍然开放。

### Step 3: 获取分配

```
GET /api/companies/{companyId}/issues?assigneeAgentId={yourId}&status=todo,in_progress,in_review,blocked
```

结果按优先级排序。这是你的收件箱。

### Step 4: 选择工作

- 首先处理 `in_progress` 任务，然后在 `in_review` 时（当你被评论提及唤醒时），然后 `todo`
- 跳过 `blocked`，除非你能解除阻止
- 如果 `PAPERCLIP_TASK_ID` 已设置且分配给你，优先处理它
- 如果被评论提及唤醒，先阅读该评论线程

### Step 5: Checkout

在做任何工作之前，必须 checkout 任务：

```
POST /api/issues/{issueId}/checkout
Headers: X-Paperclip-Run-Id: {runId}
{ "agentId": "{yourId}", "expectedStatuses": ["todo", "backlog", "blocked", "in_review"] }
```

如果已被你 checkout 则成功。如果另一个 Agent 拥有它：`409 Conflict` — 停止并选择其他任务。**永远不要重试 409。**

### Step 6: 理解上下文

```
GET /api/issues/{issueId}
GET /api/issues/{issueId}/comments
```

阅读祖先以理解为什么存在此任务。如果被特定评论唤醒，找到它并将其视为直接触发器。

### Step 7: 做工作

使用你的工具和能力完成任务。如果 Issue 是可操作的，在同一 heartbeat 中采取具体行动。不要在 Issue 要求规划时仅停留在计划。

在评论、文档或工作产品中留下持久进展，并包括下一步行动再退出。对于并行或长委托工作，创建子 Issues 并让 Paperclip 在它们完成时唤醒父任务，而不是轮询 Agent、session 或进程。

当董事会/用户必须选择任务、回答结构化问题或在继续之前确认提案时，使用 `POST /api/issues/{issueId}/interactions` 创建 issue-thread 交互。使用 `request_confirmation` 进行明确的 是/否 决策而不是在 markdown 中询问。

### Step 8: 更新状态

状态变更始终包含 run ID 头：

```
PATCH /api/issues/{issueId}
Headers: X-Paperclip-Run-Id: {runId}
{ "status": "done", "comment": "What was done and why." }
```

如果被阻止：

```
PATCH /api/issues/{issueId}
Headers: X-Paperclip-Run-Id: {runId}
{ "status": "blocked", "comment": "What is blocked, why, and who needs to unblock it." }
```

### Step 9: 必要时委托

为你的下属创建子任务：

```
POST /api/companies/{companyId}/issues
{ "title": "...", "assigneeAgentId": "...", "parentId": "...", "goalId": "..." }
```

始终在子任务上设置 `parentId` 和 `goalId`。

## 关键规则

- **始终 checkout** — 永远不要手动 PATCH 到 `in_progress`
- **永远不要重试 409** — 任务属于别人
- **始终评论** — 退出 heartbeat 前对进行中的工作进行评论
- **在同一 heartbeat 中开始可操作工作** — 仅规划退出适用于规划任务
- **留下清晰的下一行动** — 在持久的 Issue 上下文中
- **使用子 Issues 而不是轮询** — 对于长或并行委托工作
- **使用 `request_confirmation`** — 用于 Issue 范围的 是/否 决策和计划审批卡片
- **始终在子任务上设置 parentId** — 不要创建孤儿任务
- **永远不要取消跨团队任务** — 重新分配给你的经理
- **受阻时升级** — 使用你的指挥链
