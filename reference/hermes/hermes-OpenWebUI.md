# Open WebUI + API Server

使用 Open WebUI 作为 Hermes Agent 的前端界面。

## 架构

```
Open WebUI (浏览器)
    ↓ POST /v1/chat/completions
Hermes Agent API Server (port 8642)
    ↓
完整工具集（终端、文件、搜索、记忆等）
```

## 快速配置

### 1. 启用 API Server

```bash
# ~/.hermes/.env
API_SERVER_ENABLED=true
API_SERVER_KEY=your-secret-key
```

### 2. 启动 Gateway

```bash
hermes gateway
# 输出: [API Server] API server listening on http://127.0.0.1:8642
```

### 3. 启动 Open WebUI

```bash
docker run -d -p 3000:8080 \
  -e OPENAI_API_BASE_URL=http://host.docker.internal:8642/v1 \
  -e OPENAI_API_KEY=your-secret-key \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

### 4. 打开 UI

访问 http://localhost:3000 ，创建管理员账号。

## Docker Compose 配置

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    volumes:
      - open-webui:/app/backend/data
    environment:
      - OPENAI_API_BASE_URL=http://host.docker.internal:8642/v1
      - OPENAI_API_KEY=your-secret-key
    extra_hosts:
      - "host.docker.internal:host-gateway"
    restart: always
volumes:
  open-webui:
```

## 通过管理界面配置

1. 登录 http://localhost:3000
2. 头像 → Admin Settings → Connections
3. OpenAI API → Manage → + Add New Connection
4. 输入：
   - **URL**: `http://host.docker.internal:8642/v1`
   - **API Key**: 任意非空值

> 环境变量仅在 Open WebUI **首次启动** 时生效。

## 多用户配置（Profiles）

为每个用户运行独立 Hermes 实例：

### 1. 创建 profiles
```bash
hermes profile create alice
hermes -p alice config set API_SERVER_ENABLED true
hermes -p alice config set API_SERVER_PORT 8643
hermes -p alice config set API_SERVER_KEY alice-secret

hermes profile create bob
hermes -p bob config set API_SERVER_ENABLED true
hermes -p bob config set API_SERVER_PORT 8644
hermes -p bob config set API_SERVER_KEY bob-secret
```

### 2. 启动 gateways
```bash
hermes -p alice gateway &
hermes -p bob gateway &
```

### 3. 在 Open WebUI 添加连接

| 连接 | URL | API Key |
|------|-----|---------|
| Alice | `http://host.docker.internal:8643/v1` | `alice-secret` |
| Bob | `http://host.docker.internal:8644/v1` | `bob-secret` |

模型下拉菜单会显示 `alice` 和 `bob`。

## 环境变量

### Hermes Agent (API Server)

| 变量 | 默认 | 说明 |
|------|------|------|
| `API_SERVER_ENABLED` | false | 启用 API Server |
| `API_SERVER_PORT` | 8642 | HTTP 端口 |
| `API_SERVER_HOST` | 127.0.0.1 | 绑定地址 |
| `API_SERVER_KEY` | 必需 | Bearer token |

### Open WebUI

| 变量 | 说明 |
|------|------|
| `OPENAI_API_BASE_URL` | Hermes API URL（包含 `/v1`） |
| `OPENAI_API_KEY` | 任意非空值，需匹配 |

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 模型下拉为空 | 检查 URL 包含 `/v1` 后缀 |
| 连接测试通过但无模型 | 几乎总是缺少 `/v1` |
| Invalid API key | 确认两侧 API_KEY 匹配 |
