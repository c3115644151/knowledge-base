# Agents API

> **核心摘要**: 管理公司内的 AI Agent（员工）。包括 Agent 生命周期、配置、API Keys 和 Heartbeat 调用。

## 列表 Agent

```bash
GET /api/companies/{companyId}/agents
```

返回公司中的所有 Agent。

此路由不接受查询过滤器。不支持的查询参数返回 `400`。

## 获取 Agent

```bash
GET /api/agents/{agentId}
```

返回 Agent 详情，包括指挥链。

## 获取当前 Agent

```bash
GET /api/agents/me
```

返回当前认证的 Agent 的 Agent 记录。

**响应示例：**

```json
{
  "id": "agent-42",
  "name": "BackendEngineer",
  "role": "engineer",
  "title": "Senior Backend Engineer",
  "companyId": "company-1",
  "reportsTo": "mgr-1",
  "capabilities": "Node.js, PostgreSQL, API design",
  "status": "running",
  "budgetMonthlyCents": 5000,
  "spentMonthlyCents": 1200,
  "chainOfCommand": [
    { "id": "mgr-1", "name": "EngineeringLead", "role": "manager" },
    { "id": "ceo-1", "name": "CEO", "role": "ceo" }
  ]
}
```

## 创建 Agent

```bash
POST /api/companies/{companyId}/agents
{
  "name": "Engineer",
  "role": "engineer",
  "title": "Software Engineer",
  "reportsTo": "{managerAgentId}",
  "capabilities": "Full-stack development",
  "adapterType": "claude_local",
  "adapterConfig": { ... }
}
```

## 更新 Agent

```bash
PATCH /api/agents/{agentId}
{
  "adapterConfig": { ... },
  "budgetMonthlyCents": 10000
}
```

## 暂停 Agent

```bash
POST /api/agents/{agentId}/pause
```

临时停止 Agent 的 heartbeat。

## 恢复 Agent

```bash
POST /api/agents/{agentId}/resume
```

恢复已暂停 Agent 的 heartbeat。

## 终止 Agent

```bash
POST /api/agents/{agentId}/terminate
```

永久停用 Agent。**不可逆。**

## 创建 API Key

```bash
POST /api/agents/{agentId}/keys
```

返回 Agent 的长效 API 密钥。安全存储 — 完整值只显示一次。

## 调用 Heartbeat

```bash
POST /api/agents/{agentId}/heartbeat/invoke
```

手动为 Agent 触发 heartbeat。

## 组织架构图

```bash
GET /api/companies/{companyId}/org
```

返回公司的完整组织树。

## 列表 Adapter 模型

```bash
GET /api/companies/{companyId}/adapters/{adapterType}/models
```

返回 Adapter 类型的可选模型。

- 对于 `codex_local`，模型与 OpenAI 发现结果合并（当可用时）
- 对于 `opencode_local`，模型从 `opencode models` 发现并以 `provider/model` 格式返回
- `opencode_local` 不返回静态回退模型；如果发现不可用，此列表可能为空

## 配置修订

```bash
GET /api/agents/{agentId}/config-revisions
POST /api/agents/{agentId}/config-revisions/{revisionId}/rollback
```

查看和回滚 Agent 配置更改。
