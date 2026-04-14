# API 服务器

API 服务器将 Hermes Agent 暴露为 OpenAI 兼容的 HTTP 端点。任何支持 OpenAI 格式的前端（Open WebUI、LobeChat、LibreChat 等）都可连接。

## 快速开始

### 1. 启用 API 服务器

在 `~/.hermes/.env` 添加：
```bash
API_SERVER_ENABLED=true
API_SERVER_KEY=change-me-local-dev
```

### 2. 启动网关

```bash
hermes gateway
```

输出：
```
[API Server] API server listening on http://127.0.0.1:8642
```

### 3. 连接前端

将任何 OpenAI 兼容客户端指向 `http://localhost:8642/v1`：

```bash
curl http://localhost:8642/v1/chat/completions \
  -H "Authorization: Bearer change-me-local-dev" \
  -H "Content-Type: application/json" \
  -d '{"model": "hermes-agent", "messages": [{"role": "user", "content": "Hello!"}]}'
```

## 端点

### POST /v1/chat/completions

标准 OpenAI Chat Completions 格式。无状态。

**请求：**
```json
{
  "model": "hermes-agent",
  "messages": [
    {"role": "system", "content": "You are a Python expert."},
    {"role": "user", "content": "Write a fibonacci function"}
  ],
  "stream": false
}
```

**流式传输** (`"stream": true`)：返回 SSE，逐 token 输出响应。

### POST /v1/responses

OpenAI Responses API 格式。支持通过 `previous_response_id` 服务端保存对话状态。

```json
{
  "model": "hermes-agent",
  "input": "What files are in my project?",
  "instructions": "You are a helpful coding assistant.",
  "store": true
}
```

### GET /v1/models

列出可用模型。广告模型名默认为 profile 名。

### GET /health

健康检查。返回 `{"status": "ok"}`。

## 认证

Bearer token 认证：
```
Authorization: Bearer <API_SERVER_KEY>
```

## 配置

| 变量 | 默认 | 描述 |
|------|------|------|
| `API_SERVER_ENABLED` | `false` | 启用 API 服务器 |
| `API_SERVER_PORT` | `8642` | HTTP 服务器端口 |
| `API_SERVER_HOST` | `127.0.0.1` | 绑定地址（默认仅本地） |
| `API_SERVER_KEY` | — | Bearer token 认证 |
| `API_SERVER_CORS_ORIGINS` | — | 逗号分隔的允许浏览器来源 |

## 兼容前端

| 前端 | Stars | 连接 |
|------|-------|------|
| Open WebUI | 126k | 完整指南可用 |
| LobeChat | 73k | 自定义提供商端点 |
| LibreChat | 34k | 自定义端点 |
| AnythingLLM | 56k | 通用 OpenAI 提供商 |
| NextChat | 87k | BASE_URL 环境变量 |
| ChatBox | 39k | API Host 设置 |

## 多用户设置（使用 Profiles）

```bash
# 每个用户创建 profile
hermes profile create alice
hermes profile create bob

# 配置每个 profile 的 API 服务器在不同端口
hermes -p alice config set API_SERVER_ENABLED true
hermes -p alice config set API_SERVER_PORT 8643
hermes -p alice config set API_SERVER_KEY alice-secret

# 启动每个 profile 的网关
hermes -p alice gateway &
hermes -p bob gateway &
```

## 限制

- **响应存储** — 存储的响应持久化在 SQLite 中，最多 100 个（LRU 驱逐）
- **无文件上传** — 通过 API 上传的图像/文档分析尚未支持
- **模型字段是装饰性的** — 请求中的 `model` 字段接受但实际 LLM 在服务器端配置
