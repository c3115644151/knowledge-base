# Discord 集成

## 概述

Discord 支持文本频道、DM 和语音频道。Bot 可以加入语音频道进行实时对话。

## 设置

### 1. 创建 Application

1. 访问 [Discord Developer Portal](https://discord.com/developers/applications)
2. 点击 "New Application"
3. 输入名称

### 2. 创建 Bot

1. 进入 Application → "Bot"
2. 点击 "Add Bot"
3. 复制 Token

### 3. 配置权限

1. 进入 Application → "OAuth2" → "URL Generator"
2. 选择 scopes: `bot`, `applications.commands`
3. 选择 permissions:
   - **Text Permissions**: View Channels, Send Messages, Read Message History, Embed Links, Attach Files
   - **Voice Permissions**: Connect, Speak

### 4. 邀请 Bot

复制生成的 OAuth URL，浏览器打开并添加到服务器。

## 配置

```bash
# ~/.hermes/.env
DISCORD_BOT_TOKEN=xxx...
DISCORD_ALLOWED_USERS=111222333444555666
```

```yaml
# ~/.hermes/config.yaml
discord:
  bot_token: "${DISCORD_BOT_TOKEN}"
  allowed_users: []
  require_mention: true
```

## 语音频道设置

### 添加语音权限

在 Developer Portal → Bot → Permissions Integer 添加：
- 262656 (Text + Voice)

### 启用 Gateway Intents

在 Developer Portal → Bot → Privileged Gateway Intents：
- ✅ Presence Intent
- ✅ Server Members Intent
- ✅ Message Content Intent

### 系统依赖

```bash
# macOS
brew install opus

# Ubuntu/Debian
sudo apt install libopus0
```

## 使用

### DM
直接给 Bot 发消息，无需 @mention。

### 频道
在频道中 @Bot (需要 `require_mention: true`)

### 命令

| 命令 | 说明 |
|------|------|
| `/voice join` | Bot 加入你的语音频道 |
| `/voice leave` | Bot 离开语音频道 |
| `/voice status` | 查看语音状态 |

## 配置选项

| 选项 | 说明 | 默认 |
|------|------|------|
| `require_mention` | 频道中是否需要 @mention | `true` |
| `free_response_channels` | 无需 mention 的频道 ID | `[]` |
| `voice_activity_detection` | 检测用户说话 | `true` |
| `voice_auto_join` | 自动加入语音 | `false` |

## 语音频道工作原理

1. 用户在语音频道运行 `/voice join`
2. Bot 加入同一个语音频道
3. 用户说话 → 静音检测 → Whisper 转录
4. Agent 处理 → TTS 回复
5. 回复在频道播放并在文本频道显示

### 防回音
Bot 播放 TTS 时自动暂停监听。

## 安全

- 使用白名单
- 定期更新 Bot Token
- 监控未授权访问尝试
