# 实践技巧

## 快速技巧

### 1. 使用 `@` 引用文件
在消息中使用 `@` 引用文件、文件夹、git diff、URL：
```
@/path/to/file.txt - 包含这段代码
@./src/ - 这个目录下的文件
@git diff main - 最近的更改
```

### 2. 预加载技能
```bash
hermes -s github-auth,kubernetes
```
启动时加载技能到上下文。

### 3. 并行后台任务
```bash
/background Research the latest AI developments
```
同时处理多个任务。

### 4. 命名会话
```
/title Project X Planning
```
便于后续恢复。

### 5. 快捷命令
在 `config.yaml` 定义：
```yaml
quick_commands:
  deploy:
    type: exec
    command: ./scripts/deploy.sh
  notify:
    type: message
    platform: telegram
    message: "Deployment complete!"
```

### 6. 切换人格
```
/personality pirate
```
内置：helpful, concise, technical, creative, kawaii, pirate 等。

### 7. 压缩长对话
```
/compress
```
节省 token，保留关键上下文。

### 8. 自定义终端后端
```bash
hermes config set terminal.backend docker
```
生产环境使用 Docker 隔离。

## 开发工作流

### 代码审查
1. 让 Agent 分析 PR
2. 委托审查任务到子代理
3. 收集反馈并汇总

### 并行开发
```bash
hermes -w -q "Fix issue #123"
```
使用 Git Worktrees 隔离更改。

### 调试
```bash
hermes --verbose -q "Debug this error"
```
详细输出便于诊断。

## 记忆管理

### 明确记忆
```
/remember API endpoint is https://api.example.com/v2
```

### 检索
```
/recall What was my last deployment date?
```

### 清理
```
/forget outdated information
```

## 技能使用

### 发现技能
```bash
hermes skills search <topic>
```

### 安装技能
```bash
hermes skills install openai/skills/k8s
```

### 加载技能
```
/skill my-awesome-skill
```

## MCP 集成

### 快速连接
```yaml
mcp_servers:
  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "***"
```

### 工具过滤
```yaml
mcp_servers:
  github:
    tools:
      include: [list_issues, create_issue]
```

## 定时任务

### 设置任务
```
"Every morning at 8am, summarize my emails and send to Telegram"
```

### 管理任务
```bash
hermes cron list
hermes cron pause <id>
hermes cron resume <id>
```

## 消息网关

### 设置白名单
```bash
TELEGRAM_ALLOWED_USERS=123456789
DISCORD_ALLOWED_USERS=111222333
```

### DM 配对
未知用户发送配对码，你审批：
```bash
hermes pairing approve telegram ABC12DEF
```

## 性能优化

### 选择合适的模型
- 简单任务：`gemini-flash`
- 复杂任务：`claude-sonnet-4`
- 代码任务：`gpt-4o`

### 配置委托模型
```yaml
delegation:
  model: "gemini-flash"
  provider: "openrouter"
```

### 合理使用工具集
```bash
hermes chat --toolsets "terminal,file"
```
禁用不需要的工具节省 token。

## 安全实践

### 使用 YOLO 模式
```bash
hermes --yolo
```
测试时绕过审批。

### 容器隔离
```yaml
terminal:
  backend: docker
```
生产环境推荐。

### 定期清理
- 旧会话
- 未使用的技能
- 过时记忆
