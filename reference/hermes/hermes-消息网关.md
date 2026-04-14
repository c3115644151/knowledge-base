# 消息网关 (Messaging Gateway)

## 概述

消息网关让 Hermes Agent 通过多个平台与用户交互：Telegram、Discord、Slack、WhatsApp、Signal、Email 等。

## 快速开始

```bash
hermes gateway setup    # 交互式设置向导
hermes gateway start     # 启动网关
```

## 支持的平台

### 即时消息平台

| 平台 | 文档 | 说明 |
|------|------|------|
| Telegram | [telegram](hermes-Telegram.md) | 即时消息 Bot |
| Discord | [discord](hermes-Discord.md) | 服务器 + 语音频道 |
| Slack | [slack](hermes-Slack.md) | 工作空间集成 |
| WhatsApp | [whatsapp](hermes-WhatsApp.md) | 移动端消息 |
| Signal | [signal](signal.md) | 隐私优先 |
| SMS | [sms](sms.md) | 手机短信 |
| Email | [email](email.md) | 邮件收发 |
| Mattermost | [mattermost](mattermost.md) | 自托管团队聊天 |
| Matrix | [matrix](matrix.md) | 去中心化聊天 |
| DingTalk | [dingtalk](dingtalk.md) | 钉钉 |
| 飞书/Lark | [feishu](feishu.md) | 企业协作 |
| 企业微信 | [wecom](wecom.md) | 企业微信 |
| Open WebUI | [open-webui](open-webui.md) | 自托管 Web UI |
| Home Assistant | [homeassistant](homeassistant.md) | 智能家居 |

### 通用集成

| 方式 | 文档 |
|------|------|
| Webhooks | [webhooks](webhooks.md) | 接收外部消息 |

## 授权管理

### 用户白名单
```bash
# ~/.hermes/.env
TELEGRAM_ALLOWED_USERS=123456789,987654321
DISCORD_ALLOWED_USERS=111222333444555666
WHATSAPP_ALLOWED_USERS=15551234567

# 跨平台白名单
GATEWAY_ALLOWED_USERS=123456789

# 全开放 (谨慎使用)
GATEWAY_ALLOW_ALL_USERS=true
```

### DM 配对系统
未知用户发送配对码，Bot 所有者审批：

```bash
# 列出待批准
hermes pairing list

# 审批配对码
hermes pairing approve telegram ABC12DEF

# 撤销访问
hermes pairing revoke telegram 123456789
```

### 配置选项
```yaml
# ~/.hermes/config.yaml
unauthorized_dm_behavior: pair    # pair | ignore
```

## 网关命令

| 命令 | 说明 |
|------|------|
| `hermes gateway start` | 启动网关 |
| `hermes gateway stop` | 停止网关 |
| `hermes gateway status` | 查看状态 |
| `hermes gateway install` | 安装为系统服务 |
| `hermes gateway uninstall` | 卸载服务 |

## 通用命令

在所有消息平台都支持：

| 命令 | 说明 |
|------|------|
| `/voice` | 切换语音模式 |
| `/voice tts` | TTS 回复 |
| `/status` | 查看状态 |
| `/help` | 帮助 |

## 工作目录

```bash
# 设置网关工作目录
MESSAGING_CWD=/path/to/project
```

## 持久化服务

### systemd (Linux)
```bash
hermes gateway install
```

### launchd (macOS)
```bash
hermes gateway install
```

## 日志

```bash
tail -f ~/.hermes/logs/gateway.log
```

## 最佳实践

1. **配置白名单** - 生产环境务必设置允许用户列表
2. **使用 DM 配对** - 避免硬编码用户 ID
3. **安全检查** - 定期审查访问日志
4. **隔离部署** - 使用 Docker 后端隔离命令执行
