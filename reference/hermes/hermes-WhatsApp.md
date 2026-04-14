# WhatsApp 集成

## 概述

WhatsApp 通过 Baileys 库实现，支持个人号（无需官方 API）。

## 设置

### 1. 安装依赖

```bash
npm install
```

### 2. 配置

```bash
# ~/.hermes/.env
WHATSAPP_ALLOWED_USERS=15551234567
```

```yaml
# ~/.hermes/config.yaml
whatsapp:
  enabled: true
  allowed_users: []
```

### 3. 扫码登录

首次运行会生成二维码：

```bash
hermes gateway start
```

终端会显示 QR 码，用 WhatsApp 扫描。

### 4. 会话持久化

会话保存在 `~/.hermes/whatsapp/session/`

## 配置选项

| 选项 | 说明 |
|------|------|
| `session_dir` | 会话目录 |
| `allowed_users` | 允许的用户 |
| `auto_read` | 自动已读 |
| `send_delivery` | 发送送达状态 |

## 使用

- 给 Bot 发消息
- 使用 `/voice` 命令（如果启用）
- 发送图片、语音

## 限制

- 同一时间只能一个设备在线
- 不支持频道/群组（仅 DM）
- 需要保持终端运行

## 安全

- 始终使用白名单
- 会话文件包含敏感数据
- 定期备份会话
