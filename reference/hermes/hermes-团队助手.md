# 团队 Telegram 助手教程

设置团队共享的 Telegram Bot。

## 构建内容

- **授权团队成员**可以 DM 获取帮助
- **运行在服务器**上，拥有完整工具访问
- **Per-user 会话**：每人独立对话上下文
- **安全默认**：授权用户才可交互
- **定时任务**：每日 standup、health check 等

## 前置条件

- 服务器/VPS 上安装 Hermes Agent
- Telegram 账号
- LLM Provider 已配置

## 步骤一：创建 Telegram Bot

1. 在 Telegram 搜索 **@BotFather**
2. 发送 `/newbot`
3. 输入显示名称（如 `Team Hermes Assistant`）
4. 输入用户名（必须以 `bot` 结尾，如 `myteam_hermes_bot`）
5. **复制 Bot Token**

## 步骤二：配置 Gateway

### 交互式设置
```bash
hermes gateway setup
# 选择 Telegram，粘贴 bot token，输入你的 User ID
```

### 手动配置
```bash
# ~/.hermes/.env
TELEGRAM_BOT_TOKEN=7123456789:AAH1bGciOiJSUzI1NiIsInR5cCI6Ikp...
TELEGRAM_ALLOWED_USERS=123456789
```

### 查找 User ID
1. 在 Telegram 给 [@userinfobot](https://t.me/userinfobot) 发消息
2. 它会回复你的数字 User ID

## 步骤三：启动 Gateway

### 快速测试
```bash
hermes gateway
```

### 生产环境：安装为服务
```bash
hermes gateway install
sudo hermes gateway install --system  # Linux 服务器
```

### 管理服务
```bash
# Linux
hermes gateway start
hermes gateway stop
hermes gateway status
journalctl --user -u hermes-gateway -f

# macOS
hermes gateway start
tail -f ~/.hermes/logs/gateway.log
```

## 步骤四：设置团队访问

### 方式一：静态白名单
```bash
# ~/.hermes/.env
TELEGRAM_ALLOWED_USERS=123456789,987654321,555555555
```

### 方式二：DM 配对（推荐）
1. 队员给 Bot 发消息 → 收到配对码 `XKGH5N7P`
2. 队员把配对码发给你
3. 批准：
```bash
hermes pairing approve telegram XKGH5N7P
```

**管理配对**：
```bash
hermes pairing list          # 查看所有配对
hermes pairing revoke telegram 987654321  # 撤销
hermes pairing clear-pending # 清除过期
```

## 步骤五：配置 Bot

### 设置 Home Channel
```bash
# ~/.hermes/.env
TELEGRAM_HOME_CHANNEL=-1001234567890
TELEGRAM_HOME_CHANNEL_NAME="Team Updates"
```

### 设置 SOUL.md 个性
```markdown
# ~/.hermes/SOUL.md

You are a helpful team assistant. Be concise and technical.
Use code blocks for any code. Skip pleasantries.
When debugging, always ask for error logs before guessing.
```

## 步骤六：设置定时任务

### 每日 Standup
```
Every weekday at 9am, check the GitHub repository at
github.com/myorg/myproject for:
1. Pull requests opened/merged in the last 24 hours
2. Issues created or closed
3. Any CI/CD failures on the main branch

Format as a brief standup-style summary.
```

### 服务器健康检查
```
Every 6 hours, check disk usage with 'df -h', memory with 'free -h',
and Docker container status with 'docker ps'. Report anything unusual —
partitions above 80%, containers that have restarted, or high memory usage.
```

## 生产提示

### 使用 Docker 隔离
```bash
# ~/.hermes/.env
TERMINAL_BACKEND=docker
TERMINAL_DOCKER_IMAGE=nikolaik/python-nodejs:python3.11-nodejs20
```

或 `config.yaml`：
```yaml
terminal:
  backend: docker
  container_cpu: 1
  container_memory: 5120
  container_persistent: true
```

### 监控
```bash
hermes gateway status
journalctl --user -u hermes-gateway -f  # Linux
```

### 更新
```
在 Telegram 发送 /update
# 或
hermes update
```

## 日志位置

| 内容 | 位置 |
|------|------|
| Gateway 日志 | `journalctl --user -u hermes-gateway` (Linux) 或 `~/.hermes/logs/gateway.log` (macOS) |
| Cron 输出 | `~/.hermes/cron/output/{job_id}/{timestamp}.md` |
| Cron 定义 | `~/.hermes/cron/jobs.json` |
| 配对数据 | `~/.hermes/pairing/` |
| 会话历史 | `~/.hermes/sessions/` |
