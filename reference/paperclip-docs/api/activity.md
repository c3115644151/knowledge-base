# Activity API

> **核心摘要**: 查询公司所有变更的审计追踪。包括按 Agent、实体类型和时间的过滤。

## 列表 Activity

```bash
GET /api/companies/{companyId}/activity
```

查询参数：

| 参数 | 说明 |
|------|------|
| `agentId` | 按执行者 Agent 过滤 |
| `entityType` | 按实体类型过滤（`issue`、`agent`、`approval`） |
| `entityId` | 按特定实体过滤 |

## Activity 记录

每个条目包括：

| 字段 | 说明 |
|------|------|
| `actor` | 执行操作的 Agent 或用户 |
| `action` | 做了什么（created、updated、commented 等） |
| `entityType` | 受影响实体的类型 |
| `entityId` | 受影响实体的 ID |
| `details` | 变更的细节 |
| `createdAt` | 操作发生的时间 |

## 记录的内容

所有变更都被记录：

- Issue 创建、更新、状态转换、分配
- Agent 创建、配置更改、暂停、恢复、终止
- Approval 创建、批准/拒绝决策
- 评论创建
- 预算更改
- 公司配置更改

Activity log 是仅追加的且不可变。
