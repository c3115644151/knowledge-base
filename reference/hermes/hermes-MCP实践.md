# MCP 实践指南

Model Context Protocol 使用指南。

## 何时使用 MCP

### 适合使用 MCP
- 工具已以 MCP 形式存在
- 想通过 RPC 层操作本地/远程系统
- 需要精细的 per-server 暴露控制
- 连接内部 API、数据库或公司系统

### 不适合使用 MCP
- 内置 Hermes 工具已能很好解决
- MCP server 暴露大量危险工具面
- 只需要一个非常窄的集成

## 快速开始

### 1. 安装 MCP 支持
```bash
cd ~/.hermes/hermes-agent
uv pip install -e ".[mcp]"
```

### 2. 添加第一个 server

```yaml
# config.yaml
mcp_servers:
  project_fs:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/my-project"]
```

### 3. 验证加载
```bash
hermes chat
# 询问: Tell me which MCP-backed tools are available right now.
```

### 4. 立即开始过滤

**白名单模式**：
```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxx"
    tools:
      include: [list_issues, create_issue, search_code]
```

**黑名单模式**：
```yaml
mcp_servers:
  stripe:
    url: "https://mcp.stripe.com"
    headers:
      Authorization: "Bearer ***"
    tools:
      exclude: [delete_customer, refund_payment]
```

**禁用工具包装器**：
```yaml
mcp_servers:
  docs:
    url: "https://mcp.docs.example.com"
    tools:
      prompts: false
      resources: false
```

## 常用模式

### 模式一：本地项目助手
```yaml
mcp_servers:
  fs:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/project"]
  git:
    command: "uvx"
    args: ["mcp-server-git", "--repository", "/home/user/project"]
```

### 模式二：GitHub 分诊助手
```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxx"
    tools:
      include: [list_issues, create_issue, update_issue, search_code]
      prompts: false
      resources: false
```

### 模式三：内部 API 助手
```yaml
mcp_servers:
  internal_api:
    url: "https://mcp.internal.example.com"
    headers:
      Authorization: "Bearer ***"
    tools:
      include: [list_customers, get_customer, list_invoices]
      resources: false
      prompts: false
```

## 配置变更后重载

```bash
/reload-mcp
```

## 过滤控制

| 过滤方式 | 控制 |
|----------|------|
| `tools.include` | 白名单 MCP 原生工具 |
| `tools.exclude` | 黑名单 MCP 原生工具 |
| `tools.resources` | 控制资源包装器 |
| `tools.prompts` | 控制提示包装器 |

## 安全建议

1. **危险系统优先使用白名单**
2. **禁用未使用的工具**
3. **保持 server 范围窄**：
   - 文件系统 server 限制到项目目录
   - git server 指向单一仓库
4. **变更后重载**

## 推荐的第一个 MCP 配置

**推荐**：
- filesystem
- git
- GitHub
- fetch/documentation servers
- 一个窄的内部 API

**不推荐**：
- 有大量破坏性操作的大型业务系统
- 不理解的系统
