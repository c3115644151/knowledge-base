# 活动日志

> **核心摘要**: Paperclip 中的每个变更都记录在活动日志中。这提供了发生了什么、何时发生、谁做的完整审计追踪。

## 记录的内容

- Agent 创建、更新、暂停、恢复、终止
- Issue 创建、状态变更、分配、评论
- Approval 创建、批准/拒绝决策
- 预算变更
- 公司配置变更

## 查看活动

### Web UI

侧边栏中的 Activity 部分显示公司所有事件的按时间顺序的动态消息。你可以过滤：
- 按 Agent
- 按实体类型（issue、agent、approval）
- 按时间范围

### API

```
GET /api/companies/{companyId}/activity
```

查询参数：
- `agentId` — 过滤到特定 Agent 的操作
- `entityType` — 按实体类型过滤（`issue`、`agent`、`approval`）
- `entityId` — 过滤到特定实体

## 活动记录格式

每个活动条目包括：
- **Actor** — 执行操作的 Agent 或用户
- **Action** — 做了什么（created、updated、commented 等）
- **Entity** — 受影响的内容（issue、agent、approval）
- **Details** — 变更的细节（旧值和新值）
- **Timestamp** — 何时发生

## 用于调试

当出现问题时，活动日志是你的第一站：

1. 找到有问题的 Agent 或任务
2. 将活动日志过滤到该实体
3. 走时间线理解发生了什么
4. 检查是否有错过的状态更新、失败的 checkout 或意外的分配
