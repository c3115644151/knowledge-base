# SMS (Twilio)

通过 Twilio API 连接短信服务。

## 架构

- 用户发短信到 Twilio 号码
- Twilio 发送 webhook 到 Hermes
- Hermes 处理并回复

## 前置条件

- **Twilio 账号** - [注册](https://www.twilio.com/try-twilio)
- **Twilio 电话号码**（带 SMS 功能）
- **公开可访问的服务器** - Twilio 需要回调
- **aiohttp** - `pip install 'hermes-agent[sms]'`

## 配置步骤

### 1. 获取 Twilio 凭证

1. 进入 [Twilio Console](https://console.twilio.com/)
2. 复制 **Account SID** 和 **Auth Token**
3. 记下电话号码（E.164 格式，如 `+15551234567`）

### 2. 配置 Hermes

**交互式设置**：
```bash
hermes gateway setup
# 选择 SMS (Twilio)
```

**手动配置**（`~/.hermes/.env`）：
```bash
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+15551234567

# 安全（推荐）
SMS_ALLOWED_USERS=+15559876543,+15551112222

# 可选
SMS_HOME_CHANNEL=+15559876543
```

### 3. 配置 Twilio Webhook

1. 进入 [Twilio Console](https://console.twilio.com/)
2. Phone Numbers → Manage → Active Numbers
3. 点击号码
4. Messaging → A MESSAGE COMES IN：
   - **Webhook**：`https://your-server:8080/webhooks/twilio`
   - **HTTP Method**：`POST`

**本地开发**：使用 tunnel 暴露 webhook
```bash
cloudflared tunnel --url http://localhost:8080
# 或
ngrok http 8080
```

### 4. 设置 Webhook URL

```bash
# 必须与 Twilio Console 中配置的 URL 一致
SMS_WEBHOOK_URL=https://your-server:8080/webhooks/twilio
SMS_WEBHOOK_PORT=3000  # 自定义端口
```

## 行为特性

- **纯文本**：自动去除 Markdown
- **1600 字符限制**：超长响应分段发送
- **回声防止**：忽略来自自己 Twilio 号码的消息
- **电话号码脱敏**：日志中脱敏

## 安全

### Webhook 签名验证

Hermes 验证 `X-Twilio-Signature` header（HMAC-SHA1）：
- **必须设置 `SMS_WEBHOOK_URL`**
- 本地开发可禁用：`SMS_INSECURE_NO_SIGNATURE=true`（不推荐生产环境）

### 用户白名单
```bash
# 推荐：限制特定号码
SMS_ALLOWED_USERS=+15559876543,+15551112222

# 或允许所有人（不推荐）
SMS_ALLOW_ALL_USERS=true
```

> ⚠️ SMS 无内置加密，敏感操作请使用 Signal 或 Telegram。

## 环境变量

| 变量 | 必需 | 说明 |
|------|------|------|
| `TWILIO_ACCOUNT_SID` | ✅ | Twilio Account SID（以 `AC` 开头） |
| `TWILIO_AUTH_TOKEN` | ✅ | Twilio Auth Token |
| `TWILIO_PHONE_NUMBER` | ✅ | Twilio 电话号（E.164 格式） |
| `SMS_WEBHOOK_URL` | ✅ | 公开 webhook URL |
| `SMS_WEBHOOK_PORT` | — | Webhook 监听端口（默认 8080） |
| `SMS_ALLOWED_USERS` | — | 逗号分隔的 E.164 电话号 |
| `SMS_HOME_CHANNEL` | — | cron 通知投递目标 |

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 消息未收到 | 检查 webhook URL 可访问、凭证正确、号码在白名单中 |
| 回复未发送 | 确认 `TWILIO_PHONE_NUMBER` 正确且有 SMS 功能 |
| Webhook 端口冲突 | 更改：`SMS_WEBHOOK_PORT=3001` 并更新 Twilio Console |
