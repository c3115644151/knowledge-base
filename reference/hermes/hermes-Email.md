# Email 消息

通过标准 IMAP/SMTP 收发邮件，支持 Gmail、Outlook 等任何提供商。

## 架构

- **接收**：IMAP 轮询新邮件
- **发送**：SMTP 回复
- 无额外依赖（使用 Python 内置 `imaplib`、`smtplib`、`email`）

## 前置条件

- **专用邮箱账号**（建议不要用个人邮箱）
- **IMAP 已启用**
- **应用密码**（Gmail 需要）

### Gmail 设置
1. 启用两步验证
2. 进入 [App Passwords](https://myaccount.google.com/apppasswords)
3. 创建应用密码（选择 "Mail"）
4. 复制 16 位密码

### Outlook 设置
1. 进入 [Security Settings](https://account.microsoft.com/security)
2. 创建应用密码
3. IMAP：`outlook.office365.com`，SMTP：`smtp.office365.com`

## 配置

### 交互式设置
```bash
hermes gateway setup
# 选择 Email
```

### 手动配置

```bash
# ~/.hermes/.env

# 必需
EMAIL_ADDRESS=hermes@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx  # 应用密码
EMAIL_IMAP_HOST=imap.gmail.com
EMAIL_SMTP_HOST=smtp.gmail.com

# 安全（推荐）
EMAIL_ALLOWED_USERS=your@email.com,colleague@work.com

# 可选
EMAIL_IMAP_PORT=993                    # 默认 993
EMAIL_SMTP_PORT=587                    # 默认 587
EMAIL_POLL_INTERVAL=15                 # 轮询间隔（秒）
EMAIL_HOME_ADDRESS=your@email.com     # cron 默认投递
```

## 启动

```bash
hermes gateway
```

## 行为特性

### 接收邮件
- **主题行**作为上下文（如 `[Subject: Deploy to production]`）
- **回复邮件**（`Re:` 开头）自动保留线程
- **附件**缓存：
  - 图片 → 供 vision 工具使用
  - 文档（PDF、ZIP）→ 可文件访问
- **HTML 邮件**自动提取纯文本
- **自动化发送者**自动忽略（`noreply@`、`mailer-daemon@` 等）

### 发送回复
- 使用 `In-Reply-To` 和 `References` headers 保持线程
- 纯文本 UTF-8

### 附件处理
```yaml
# config.yaml - 跳过所有附件
platforms:
  email:
    skip_attachments: true
```

## 访问控制

| 配置 | 行为 |
|------|------|
| `EMAIL_ALLOWED_USERS` 已设置 | 仅白名单地址被处理 |
| 未设置 | 未知发送者收到配对码 |
| `EMAIL_ALLOW_ALL_USERS=true` | 任何人可发送（危险！） |

> ⚠️ **始终配置 `EMAIL_ALLOWED_USERS`**。代理有终端访问权限。

## 环境变量

| 变量 | 必需 | 默认 | 说明 |
|------|------|------|------|
| `EMAIL_ADDRESS` | ✅ | — | 邮箱地址 |
| `EMAIL_PASSWORD` | ✅ | — | 邮箱密码或应用密码 |
| `EMAIL_IMAP_HOST` | ✅ | — | IMAP 服务器 |
| `EMAIL_SMTP_HOST` | ✅ | — | SMTP 服务器 |
| `EMAIL_IMAP_PORT` | — | `993` | IMAP 端口 |
| `EMAIL_SMTP_PORT` | — | `587` | SMTP 端口 |
| `EMAIL_POLL_INTERVAL` | — | `15` | 轮询间隔（秒） |
| `EMAIL_ALLOWED_USERS` | — | — | 逗号分隔的允许地址 |
| `EMAIL_HOME_ADDRESS` | — | — | cron 默认投递地址 |

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| "IMAP connection failed" | 确认 IMAP 主机和端口，Gmail 需在设置中启用 IMAP |
| "SMTP connection failed" | 确认 SMTP 主机和端口，Gmail 必须用应用密码 |
| "Authentication failed" | Gmail 必须使用应用密码而非常规密码 |
| 消息未收到 | 检查 `EMAIL_ALLOWED_USERS`、检查垃圾邮件 |
| 响应慢 | 减少轮询间隔：`EMAIL_POLL_INTERVAL=5` |
