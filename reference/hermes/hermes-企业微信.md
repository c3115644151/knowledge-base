# 企业微信集成

通过企业微信 AI Bot WebSocket 网关连接。

## 架构

- 使用企业微信 AI Bot WebSocket 网关
- 实时双向通信
- 无需公网 endpoint

## 前置条件

- 企业微信组织账号
- 企业微信管理后台创建的 AI Bot
- Bot ID 和 Secret

## 配置

### 1. 创建 AI Bot

1. 登录[企业微信管理后台](https://work.weixin.qq.com/wework_admin/)
2. 应用 → 创建应用 → AI Bot
3. 配置名称和描述
4. 复制 **Bot ID** 和 **Secret**

### 2. 配置 Hermes

```bash
# ~/.hermes/.env

# 必需
WECOM_BOT_ID=your-bot-id
WECOM_SECRET=your-secret

# 可选
WECOM_ALLOWED_USERS=user_id_1,user_id_2
WECOM_HOME_CHANNEL=chat_id
```

### 3. 启动

```bash
hermes gateway
```

## 访问控制

### DM 策略
```bash
WECOM_DM_POLICY=allowlist
```

| 值 | 行为 |
|------|------|
| `open` | 任何人都可 DM（默认） |
| `allowlist` | 仅白名单用户可 DM |
| `disabled` | 忽略所有 DM |

### 群策略
```bash
WECOM_GROUP_POLICY=allowlist
```

| 值 | 行为 |
|------|------|
| `open` | 所有群响应（默认） |
| `allowlist` | 仅白名单群响应 |
| `disabled` | 忽略所有群消息 |

### 细粒度群控制
```yaml
platforms:
  wecom:
    enabled: true
    extra:
      bot_id: "your-bot-id"
      secret: "your-secret"
      group_policy: "allowlist"
      group_allow_from:
        - "group_id_1"
        - "group_id_2"
      groups:
        group_id_1:
          allow_from:
            - "user_alice"
            - "user_bob"
        "*":
          allow_from:
            - "user_admin"
```

## 媒体支持

| 类型 | 大小限制 |
|------|----------|
| 图片 | 10 MB |
| 文档 | 20 MB |
| 视频 | 10 MB |
| 语音 | 2 MB（仅 AMR 原生） |

- 图片超过 10MB → 自动降级为文件
- 视频超过 10MB → 自动降级为文件
- 非 AMR 音频 → 自动降级为文件

## 环境变量

| 变量 | 必需 | 说明 |
|------|------|------|
| `WECOM_BOT_ID` | ✅ | AI Bot ID |
| `WECOM_SECRET` | ✅ | AI Bot Secret |
| `WECOM_ALLOWED_USERS` | — | 用户 ID 列表 |
| `WECOM_HOME_CHANNEL` | — | cron 投递目标 |
| `WECOM_DM_POLICY` | — | DM 策略 |
| `WECOM_GROUP_POLICY` | — | 群策略 |

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 媒体解密失败 | `pip install cryptography` |
| 语音发送为文件 | 企业微信仅支持 AMR 格式原生语音 |
| 文件过大 | 企业微信限制 20MB |
