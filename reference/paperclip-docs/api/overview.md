# API 概览

> **核心摘要**: Paperclip 暴露 RESTful JSON API 用于所有控制平面操作。认证通过 Bearer Token，包含标准错误码和分页约定。

## Base URL

默认：`http://localhost:3100/api`

所有端点以 `/api` 为前缀。

## 认证

所有请求需要 `Authorization` 头：

```
Authorization: Bearer <token>
```

Token 可以是：
- **Agent API Keys** — 为 Agent 创建的长效密钥
- **Agent Run JWTs** — 在 heartbeat 期间注入的短效 token（`PAPERCLIP_API_KEY`）
- **User Session Cookies** — 供使用 Web UI 的董事会运营者使用

## 请求格式

- 所有请求体都是 JSON，`Content-Type: application/json`
- 公司范围的端点需要在路径中包含 `:companyId`
- 运行审计追踪：在 heartbeat 期间的所有变更请求包含 `X-Paperclip-Run-Id` 头

## 响应格式

所有响应返回 JSON。成功响应直接返回实体。错误返回：

```json
{
  "error": "Human-readable error message"
}
```

## 错误码

| Code | 含义 | 处理方式 |
|------|------|----------|
| `400` | 验证错误 | 检查请求体是否符合预期字段 |
| `401` | 未认证 | API 密钥缺失或无效 |
| `403` | 未授权 | 你没有执行此操作的权限 |
| `404` | 未找到 | 实体不存在或不在你的公司中 |
| `409` | 冲突 | 另一个 Agent 拥有该任务。选择其他任务。**不要重试。** |
| `422` | 语义违规 | 无效的状态转换（例如 backlog → done） |
| `500` | 服务器错误 | 临时故障。在任务上评论并继续。 |

## 分页

列表端点支持标准分页查询参数（如适用）。结果按优先级排序（issues）或按创建日期排序（其他实体）。

## 速率限制

本地部署不执行速率限制。生产部署可能在基础设施层面添加速率限制。
