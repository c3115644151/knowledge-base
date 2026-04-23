# Auggie MCP 配置 - 配置协议

## 前置条件检查清单

- [ ] Node.js 和 npm 已安装
- [ ] Claude Code / Codex 已安装
- [ ] 拥有 Auggie API Token
- [ ] Auggie CLI 已安装 (`@augmentcode/auggie@prerelease`)
- [ ] 目标项目路径存在且可访问

## 配置步骤（IF-THEN）

### 步骤 1：安装 Auggie CLI

```
IF Auggie CLI 未安装
THEN 执行安装命令
```

```bash
npm install -g @augmentcode/auggie@prerelease
```

### 步骤 2：用户认证

```
IF 尚未登录 Auggie
THEN 执行登录（交互式或 Token 方式）
```

```bash
# 方式一：交互式登录
auggie login

# 方式二：使用 Token（适用于 CI/CD）
export AUGMENT_API_TOKEN="your-token"
export AUGMENT_API_URL="https://i0.api.augmentcode.com/"
```

### 步骤 3：配置 Claude Code MCP

```
IF 需要在 Claude Code 中使用 Auggie MCP
THEN 添加 MCP 服务器配置
```

```bash
# 全局配置（所有项目可用）
claude mcp add-json auggie-mcp --scope user '{
  "type": "stdio",
  "command": "auggie",
  "args": ["--mcp"],
  "env": {
    "AUGMENT_API_TOKEN": "your-token",
    "AUGMENT_API_URL": "https://i0.api.augmentcode.com/"
  }
}'

# 项目配置（仅当前项目可用）
claude mcp add-json auggie-mcp --scope project '{
  "type": "stdio",
  "command": "auggie",
  "args": ["-w", "/path/to/project", "--mcp"],
  "env": {
    "AUGMENT_API_TOKEN": "your-token",
    "AUGMENT_API_URL": "https://i0.api.augmentcode.com/"
  }
}'
```

### 步骤 4：配置 Codex MCP

```
IF 使用 Codex 作为 AI 工具
THEN 编辑配置文件
```

```bash
# 编辑 ~/.codex/config.toml
[mcp_servers."auggie-mcp"]
command = "auggie"
args = ["-w", "/path/to/project", "--mcp"]
startup_timeout_ms = 20000
```

### 步骤 5：创建环境配置文件（可选）

```
IF 需要持久化配置
THEN 创建配置文件
```

```bash
mkdir -p ~/.augment
cat > ~/.augment/config << 'EOF'
{
  "apiToken": "your-token",
  "apiUrl": "https://i0.api.augmentcode.com/",
  "defaultModel": "gpt-4",
  "workspaceRoot": "/path/to/project"
}
EOF
```

## 验证检查点

- [ ] `auggie token print` 显示有效 Token
- [ ] `claude mcp list` 显示 `auggie-mcp: auggie --mcp - ✓ Connected`
- [ ] `auggie -w /path/to/project --mcp` 执行无错误
- [ ] Claude Code 中能正常使用 `codebase-retrieval` 等工具

## 高级配置

| 配置项 | 环境变量 | 说明 |
|--------|----------|------|
| 自定义缓存 | `AUGMENT_CACHE_DIR` | 缓存目录路径 |
| 重试超时 | `AUGMENT_RETRY_TIMEOUT` | 超时秒数（默认30） |
| 禁用确认 | `--allow-indexing` | 跳过确认提示 |

```bash
# 高级配置示例
export AUGMENT_CACHE_DIR="/custom/cache/path"
export AUGMENT_RETRY_TIMEOUT=30
auggie --allow-indexing --mcp
```

## 常见故障

| 问题 | 解决方案 |
|------|----------|
| 连接失败 | 检查 Token：`auggie token print`，重新登录 |
| 路径错误 | 使用绝对路径 `auggie -w $(pwd) --mcp` |
| 权限问题 | 检查 `ls -la ~/.augment/`，修复权限 `chmod 600 ~/.augment/session.json` |
| MCP 未识别 | 确认 Claude Code 版本支持 MCP，重新加载配置 |
