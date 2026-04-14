# MCP (Model Context Protocol) 集成

## 概述

MCP 允许 Hermes Agent 连接外部工具服务器，无需编写原生工具即可访问 GitHub、数据库、文件系统、内部 API 等。

## 快速开始

### 1. 安装 MCP 支持
```bash
cd ~/.hermes/hermes-agent
uv pip install -e ".[mcp]"
```

### 2. 配置 MCP 服务器
```yaml
# ~/.hermes/config.yaml
mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]
```

### 3. 使用
```bash
hermes chat
# 然后问: "List the files in /home/user/projects"
```

## 服务器类型

### Stdio 服务器 (本地)
```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "***"
```

### HTTP 服务器 (远程)
```yaml
mcp_servers:
  remote_api:
    url: "https://mcp.example.com/mcp"
    headers:
      Authorization: "Bearer ***"
```

## 工具注册

MCP 工具以 `mcp_<server>_<tool>` 前缀注册：

| 服务器 | MCP 工具 | 注册名称 |
|--------|----------|----------|
| `filesystem` | `read_file` | `mcp_filesystem_read_file` |
| `github` | `create-issue` | `mcp_github_create_issue` |
| `my-api` | `query.data` | `mcp_my_api_query_data` |

## 工具过滤

### 白名单
```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "***"
    tools:
      include: [create_issue, list_issues]
```

### 黑名单
```yaml
mcp_servers:
  stripe:
    url: "https://mcp.stripe.com"
    tools:
      exclude: [delete_customer]
```

### 禁用工具
```yaml
mcp_servers:
  docs:
    url: "https://mcp.docs.example.com"
    tools:
      prompts: false      # 禁用 list_prompts, get_prompt
      resources: false    # 禁用 list_resources, read_resource
```

## 配置参考

| 键 | 类型 | 说明 |
|-----|------|------|
| `command` | string | Stdio 服务器命令 |
| `args` | list | 命令参数 |
| `env` | mapping | 环境变量 |
| `url` | string | HTTP 端点 |
| `headers` | mapping | HTTP 头 |
| `timeout` | number | 工具调用超时 |
| `connect_timeout` | number | 连接超时 |
| `enabled` | bool | 是否启用 |
| `tools` | mapping | 工具过滤 |

## MCP 采样支持

MCP 服务器可以请求 Hermes 执行 LLM 推理：

```yaml
mcp_servers:
  my_server:
    command: "my-mcp-server"
    sampling:
      enabled: true
      model: "openai/gpt-4o"
      max_tokens_cap: 4096
      timeout: 30
      max_rpm: 10
      max_tool_rounds: 5
      allowed_models: []
      log_level: "info"
```

## 运行时行为

### 启动发现
MCP 服务器在启动时发现，工具注册到正常工具注册表。

### 动态工具发现
服务器发送 `notifications/tools/list_changed` 时自动刷新。

### 重新加载
```bash
/reload-mcp    # 重新加载 MCP 配置
```

## 安全模型

### Stdio 环境过滤
Hermes 不会盲目传递完整 shell 环境，只传递显式配置的 `env` 和安全基线。

### 凭证处理
错误消息中的凭证自动编辑为 `[REDACTED]`。

## 使用示例

### GitHub 最小权限
```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "***"
    tools:
      include: [list_issues, create_issue, update_issue]
      prompts: false
      resources: false
```

### Stripe 禁用危险操作
```yaml
mcp_servers:
  stripe:
    url: "https://mcp.stripe.com"
    headers:
      Authorization: "Bearer ***"
    tools:
      exclude: [delete_customer, refund_payment]
```

## Hermes 作为 MCP 服务器

Hermes 也可以作为 MCP 服务器运行：

```bash
hermes mcp serve
```

### 可用工具
| 工具 | 说明 |
|------|------|
| `conversations_list` | 列出活动对话 |
| `conversation_get` | 获取对话详情 |
| `messages_read` | 读取消息历史 |
| `attachments_fetch` | 获取附件 |
| `events_poll` | 轮询新事件 |
| `events_wait` | 等待下一个事件 |
| `messages_send` | 发送消息 |
| `channels_list` | 列出可用频道 |
| `permissions_list_open` | 列出待批准请求 |
| `permissions_respond` | 响应批准请求 |

### Claude Code 配置
```json
{
  "mcpServers": {
    "hermes": {
      "command": "hermes",
      "args": ["mcp", "serve"]
    }
  }
}
```
