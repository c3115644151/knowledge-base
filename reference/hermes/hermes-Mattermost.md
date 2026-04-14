# Mattermost 集成

作为 Bot 接入 Mattermost（自托管 Slack 替代品）。

## 前置条件

- Mattermost 服务器（自托管）
- **启用 Bot 账号**（需要 System Admin）
- Bot Token
- 你的 Mattermost User ID

## 启用 Bot 账号

1. 以 System Admin 登录
2. System Console → Integrations → Bot Accounts
3. 启用 **Enable Bot Account Creation**

## 创建 Bot 账号

1. Integrations → Bot Accounts → Add Bot Account
2. 填写：Username（如 `hermes`）、Display Name
3. 点击 **Create Bot Account**
4. **立即复制 Token**（只显示一次）

## 配置

### 交互式设置
```bash
hermes gateway setup
# 选择 Mattermost
```

### 手动配置

```bash
# ~/.hermes/.env

# 必需
MATTERMOST_URL=https://mm.example.com
MATTERMOST_TOKEN=xxx
MATTERMOST_ALLOWED_USERS=user-id-26chars

# 可选
MATTERMOST_REPLY_MODE=thread  # 回复模式（thread 或 off）
MATTERMOST_REQUIRE_MENTION=true  # 是否需要 @mention
```

### 配置项

| 变量 | 默认 | 说明 |
|------|------|------|
| `MATTERMOST_URL` | 必需 | Mattermost 服务器 URL |
| `MATTERMOST_TOKEN` | 必需 | Bot Token |
| `MATTERMOST_ALLOWED_USERS` | 必需 | 你的 User ID（26位字母数字） |
| `MATTERMOST_REPLY_MODE` | off | `thread` 或 `off` |
| `MATTERMOST_REQUIRE_MENTION` | true | 群聊是否需要 @mention |
| `MATTERMOST_HOME_CHANNEL` | — | 频道 ID，cron 结果投递目标 |

### 会话模型

```yaml
group_sessions_per_user: true  # 默认：每个用户会话隔离
```

## 行为特性

| 场景 | 行为 |
|------|------|
| **私信** | 无需 @mention，每条私信独立会话 |
| **公开/私有频道** | 需要 @mention 才响应 |
| **线程** | 如果 `MATTERMOST_REPLY_MODE=thread`，回复在线程下 |
| **共享频道多人** | 默认按用户隔离会话 |

## 查找 User ID

1. 点击头像 → Profile
2. 在 Profile 对话框中复制 User ID

> 注意：User ID 不是 @username，是26位字母数字字符串。

## 故障排除

| 问题 | 原因 |
|------|------|
| Bot 不响应 | 未加入频道，或 User ID 不在白名单 |
| 403 Forbidden | Token 无效或无权限发布 |
| WebSocket 断开 | 检查反向代理的 WebSocket 配置 |

### Nginx WebSocket 配置
```nginx
location /api/v4/websocket {
    proxy_pass http://mattermost-backend;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 600s;
}
```
