# Telegram 集成

## 概述

Telegram 是最简单易用的消息平台，支持语音消息和文件。

## 设置

### 1. 创建 Bot

1. 在 Telegram 搜索 **@BotFather**
2. 发送 `/newbot`
3. 输入 Bot 名称和用户名
4. 复制 Bot Token

### 2. 配置

```bash
# ~/.hermes/.env
TELEGRAM_BOT_TOKEN=123456789:ABCDEFGHIJKLMN...
```

### 3. 授权用户

```bash
TELEGRAM_ALLOWED_USERS=123456789,987654321
```

获取你的 Telegram User ID：
1. 搜索 **@userinfobot**
2. 发送任意消息
3. 复制 `Id` 字段

### 4. 启动

```bash
hermes gateway start
```

## 配置选项

```yaml
# ~/.hermes/config.yaml
telegram:
  bot_token: "${TELEGRAM_BOT_TOKEN}"
  allowed_users: []
  require_mention: false
```

| 选项 | 说明 |
|------|------|
| `bot_token` | Bot Token |
| `allowed_users` | 允许的用户 ID 列表 |
| `require_mention` | 是否需要在群组中 @Bot |

## 使用

### DM (推荐)
直接给 Bot 发消息，无需 @mention。

### 群组
- 在群组中添加 Bot
- 配置 `require_mention: true` (需要 @Bot)
- 或 `require_mention: false` (回复所有消息)

## 命令

| 命令 | 说明 |
|------|------|
| `/voice` | 切换语音模式 |
| `/voice tts` | TTS 回复 |
| `/status` | 状态 |

## 语音支持

Bot 可以发送语音消息回复：

```yaml
tts:
  provider: "edge"    # 免费，无需 API 密钥
```

## 安全

- 始终使用白名单
- 不使用 `GATEWAY_ALLOW_ALL_USERS`
- 定期检查日志
