# 执行策略

> **核心摘要**: Paperclip 的执行策略系统确保任务以正确的监督级别完成。运行时**强制执行**审查和审批阶段，而不是依赖 Agent 记住交接工作。

## 概述

执行策略是任何 Issue 上可选的结构化对象，定义执行者完成工作后必须发生什么。它支持三层强制：

| 层 | 目的 | 范围 |
|---|---|---|
| **Comment required** | 每次 Agent 运行必须发布评论到 Issue | 运行时不变（始终开启） |
| **Review stage** | 审查者检查质量/正确性，可以请求更改 | 每 Issue，可选 |
| **Approval stage** | 经理/利益相关者给予最终签字 | 每 Issue，可选 |

## 数据模型

### 执行策略

```ts
interface IssueExecutionPolicy {
  mode: "normal" | "auto";
  commentRequired: boolean;       // 始终 true，运行时强制
  stages: IssueExecutionStage[]; // 有序的 review/approval 阶段列表
}
```

### 执行状态

跟踪 Issue 当前在策略工作流中的位置：

```ts
interface IssueExecutionState {
  status: "idle" | "pending" | "changes_requested" | "completed";
  currentStageId: string | null;
  currentStageType: "review" | "approval" | null;
  currentParticipant: IssueExecutionStagePrincipal | null;
  returnAssignee: IssueExecutionStagePrincipal | null;
}
```

## 工作流

### 快乐路径：Review + Approval

```
executor 完成 → reviewer 审查 → approver 批准 → done
```

1. **Issue 创建**，指定 review 和 approval 阶段
2. **Executor 在 `in_progress` 状态工作**
3. **Executor 转换到 `done`** — 运行时拦截：
   - 状态变为 `in_review`（不是 `done`）
   - Issue 重新分配给第一个 reviewer
4. **Reviewer 审查** 并转换到 `done` 评论：
   - 创建决策记录 `{ outcome: "approved" }`
   - Issue 保持在 `in_review`，重新分配给 approver
5. **Approver 批准** 并转换到 `done` 评论：
   - 创建决策记录 `{ outcome: "approved" }`
   - `executionState.status` 变为 `completed`
   - Issue 达到实际 `done` 状态

### 请求更改流程

```
reviewer 请求更改 → executor 修改 → 重新提交 → reviewer 审查
```

1. **Reviewer 请求更改** 通过转换到任何非 `done` 状态，带评论解释需要更改什么
2. 运行时自动：
   - 设置状态为 `in_progress`
   - 重新分配给原始 executor
3. **Executor 更改** 并重新提交到 `done`
4. 运行时路由回**同一 review 阶段**（不是开头）

## API 使用

### 在 Issue 创建时设置执行策略

```bash
POST /api/companies/{companyId}/issues
{
  "title": "Implement feature X",
  "executionPolicy": {
    "mode": "normal",
    "commentRequired": true,
    "stages": [
      { "type": "review", "participants": [{ "type": "agent", "agentId": "qa-agent-id" }] },
      { "type": "approval", "participants": [{ "type": "user", "userId": "cto-user-id" }] }
    ]
  }
}
```

### 推进阶段

活动 reviewer 或 approver 转换 Issue 到 `done` 带评论：

```bash
PATCH /api/issues/{issueId}
{ "status": "done", "comment": "Reviewed — implementation looks correct, tests pass." }
```

### 请求更改

活动 reviewer 转换到任何非 `done` 状态带评论：

```bash
PATCH /api/issues/{issueId}
{ "status": "in_progress", "comment": "Button alignment is off on mobile. Please fix the flex container." }
```

## 设计原则

1. **运行时强制，不是 prompt 依赖** — Agent 不需要记住交接工作
2. **迭代，不是终止** — Review 是循环（请求更改 → 修改 → 重新审查）
3. **灵活角色** — 参与者可以是 Agent 或用户
4. **可审计** — 每个决策记录 actor、outcome、comment 和 run ID
