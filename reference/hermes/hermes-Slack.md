# Slack 集成

## 概述

Slack 集成支持企业工作空间。

## 设置

### 1. 创建 Slack App

1. 访问 [api.slack.com/apps](https://api.slack.com/apps)
2. 点击 "Create New App" → "From scratch"
3. 输入名称，选择工作空间

### 2. 配置权限

进入 "OAuth & Permissions"：

**User Token Scopes:**
- `chat:write`
- `channels:history`
- `channels:read`
- `groups:history`
- `groups:read`
- `im:history`
- `im:read`
- `im:write`
- `mpim:history`
- `mpim:read`
- `mpim:write`

**Bot Token Scopes:**
- `chat:write`
- `channels:history`
- `channels:read`
- `channels:write`
- `groups:history`
- `groups:read`
- `groups:write`
- `im:history`
- `im:read`
- `im:write`
- `mpim:history`
- `mpim:read`
- `mpim:write`
- `app_mentions:read`
- `reactions:read`
- `reactions:write`

### 3. 启用 Socket Mode

进入 "Socket Mode" → Enable Socket Mode

### 4. 安装到工作空间

"Install App" → "Install to Workspace"

## 配置

```bash
# ~/.hermes/.env
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
SLACK_ALLOWED_USERS=U01ABC123,U02DEF456
```

```yaml
# ~/.hermes/config.yaml
slack:
  bot_token: "${SLACK_BOT_TOKEN}"
  app_token: "${SLACK_APP_TOKEN}"
  allowed_users: []
  require_mention: true
```

## 功能

- DM 直接消息
- 频道消息 (需要 @App)
- 线程回复
- 表情反应
- 文件上传

## 配置选项

| 选项 | 说明 |
|------|------|
| `require_mention` | 是否需要 @App |
| `allowed_users` | 允许的用户 ID |
| `auto_reply_threads` | 自动回复线程 |
