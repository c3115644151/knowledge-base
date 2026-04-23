# Routines API

> **核心摘要**: Routine 是定时任务，根据 schedule、webhook 或 API 调用触发，并为分配的 Agent 创建 heartbeat 运行。

## 列表 Routines

```bash
GET /api/companies/{companyId}/routines
```

返回公司中的所有 Routines。

## 获取 Routine

```bash
GET /api/routines/{routineId}
```

返回 Routine 详情，包括 triggers。

## 创建 Routine

```bash
POST /api/companies/{companyId}/routines
{
  "title": "Weekly CEO briefing",
  "description": "Compile status report and email Founder",
  "assigneeAgentId": "{agentId}",
  "projectId": "{projectId}",
  "goalId": "{goalId}",
  "priority": "medium",
  "status": "active",
  "concurrencyPolicy": "coalesce_if_active",
  "catchUpPolicy": "skip_missed"
}
```

**Agent 只能创建分配给自己的 Routine。** 董事会运营者可以分配给任何 Agent。

### 字段说明

| 字段 | 必需 | 说明 |
|------|------|------|
| `title` | 是 | Routine 名称 |
| `description` | 否 | Routine 的人类可读描述 |
| `assigneeAgentId` | 是 | 接收每次运行的 Agent |
| `projectId` | 是 | 此 Routine 所属的项目 |
| `goalId` | 否 | 要链接的目标 |
| `parentIssueId` | 否 | 创建的运行 Issue 的父 Issue |
| `priority` | 否 | `critical`、`high`、`medium`（默认）、`low` |
| `status` | 否 | `active`（默认）、`paused`、`archived` |
| `concurrencyPolicy` | 否 | 当运行触发但前一个仍在活跃时的行为 |
| `catchUpPolicy` | 否 | 错过的计划运行的行为 |

### 并发策略

| 值 | 行为 |
|----|------|
| `coalesce_if_active`（默认） | 传入运行立即完成为 `coalesced` 并链接到活跃运行 — 不创建新 Issue |
| `skip_if_active` | 传入运行立即完成为 `skipped` 并链接到活跃运行 — 不创建新 Issue |
| `always_enqueue` | 始终创建新运行，无论活跃运行如何 |

### 补偿策略

| 值 | 行为 |
|----|------|
| `skip_missed`（默认） | 错过的计划运行被丢弃 |
| `enqueue_missed_with_cap` | 错过的运行排队，最多达到内部上限 |

## 更新 Routine

```bash
PATCH /api/routines/{routineId}
{
  "status": "paused"
}
```

所有创建字段都可更新。**Agent 只能更新分配给自己的 Routine，不能将 Routine 重新分配给其他 Agent。**

## 添加 Trigger

```bash
POST /api/routines/{routineId}/triggers
```

三种 trigger 类型：

### Schedule — 按 cron 表达式触发

```json
{
  "kind": "schedule",
  "cronExpression": "0 9 * * 1",
  "timezone": "Europe/Amsterdam"
}
```

### Webhook — 按入站 HTTP POST 到生成的 URL 触发

```json
{
  "kind": "webhook",
  "signingMode": "hmac_sha256",
  "replayWindowSec": 300
}
```

签名模式：`bearer`（默认）、`hmac_sha256`。重放窗口范围：30–86400 秒（默认 300）。

### API — 仅在通过手动运行显式调用时触发

```json
{
  "kind": "api"
}
```

Routine 可以有多种不同类型的 triggers。

## 更新 Trigger

```bash
PATCH /api/routine-triggers/{triggerId}
{
  "enabled": false,
  "cronExpression": "0 10 * * 1"
}
```

## 删除 Trigger

```bash
DELETE /api/routine-triggers/{triggerId}
```

## 轮换 Trigger Secret

```bash
POST /api/routine-triggers/{triggerId}/rotate-secret
```

为 webhook trigger 生成新签名密钥。之前的密钥立即失效。

## 手动运行

```bash
POST /api/routines/{routineId}/run
{
  "source": "manual",
  "triggerId": "{triggerId}",
  "payload": { "context": "..." },
  "idempotencyKey": "my-unique-key"
}
```

立即触发运行，绕过 schedule。并发策略仍然适用。

`triggerId` 是可选的。当提供时，服务器验证 trigger 属于此 Routine（`403`）并已启用（`409`），然后记录运行针对该 trigger 并更新其 `lastFiredAt`。为没有 trigger 归属的通用手动运行省略它。

## 触发公开 Trigger

```bash
POST /api/routine-triggers/public/{publicId}/fire
```

从外部系统触发 webhook trigger。需要有效的 `Authorization` 或 `X-Paperclip-Signature` + `X-Paperclip-Timestamp` 头对匹配 trigger 的签名模式。

## 列表运行

```bash
GET /api/routines/{routineId}/runs?limit=50
```

返回 Routine 的最近运行历史。默认为 50 个最近运行。

## Agent 访问规则

Agent 可以读取其公司中的所有 Routine，但只能创建和管理分配给自己的 Routine：

| 操作 | Agent | 董事会 |
|------|-------|--------|
| 列表/获取 | ✅ 任何 Routine | ✅ |
| 创建 | ✅ 仅自己的 | ✅ |
| 更新/激活 | ✅ 仅自己的 | ✅ |
| 添加/更新/删除 triggers | ✅ 仅自己的 | ✅ |
| 轮换 trigger secret | ✅ 仅自己的 | ✅ |
| 手动运行 | ✅ 仅自己的 | ✅ |
| 重新分配给其他 Agent | ❌ | ✅ |

## Routine 生命周期

```
active → paused → active
       → archived
```

归档的 Routine 不会触发，也不能重新激活。
