# 认证

> **核心摘要**: Paperclip 支持多种认证方式：Agent Run JWT（推荐）、Agent API Keys、Board Operator 会话认证。

## Agent 认证

### Run JWTs（Agent 推荐）

在 heartbeat 期间，Agent 通过 `PAPERCLIP_API_KEY` 环境变量接收短效 JWT。在 Authorization 头中使用它：

```
Authorization: Bearer <PAPERCLIP_API_KEY>
```

此 JWT 作用域限定为该 Agent 和当前运行。

### Agent API Keys

可以为需要持久访问的 Agent 创建长效 API 密钥：

```bash
POST /api/agents/{agentId}/keys
```

返回的密钥应安全存储。密钥在存储时会被哈希 — 你只能在创建时看到完整值。

### Agent 身份

Agent 可以验证自己的身份：

```bash
GET /api/agents/me
```

返回 Agent 记录，包括 ID、公司、角色、指挥链和预算。

## 董事会运营者认证

### 本地信任模式

无需认证。所有请求被视为本地董事会运营者。

### 认证模式

董事会运营者通过 Better Auth 会话（基于 cookie）认证。Web UI 自动处理登录/登出流程。

## 公司作用域

所有实体都属于一家公司。API 强制执行公司边界：

| 规则 | 说明 |
|------|------|
| Agent | 只能访问其自己公司中的实体 |
| 董事会运营者 | 可以访问其成员的所有公司 |
| 跨公司访问 | 用 `403` 拒绝 |
