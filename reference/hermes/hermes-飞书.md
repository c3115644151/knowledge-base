# 飞书/Lark 集成

连接飞书和 Lark 作为全功能 Bot，支持 WebSocket 和 Webhook 两种模式。

## 两种连接模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **WebSocket**（推荐） | Hermes 发起连接，无需公网 | 本地/私有服务器 |
| **Webhook** | 飞书推送事件到 Hermes | 已有 HTTP 端点 |

## 配置步骤

### 1. 创建飞书/Lark 应用

1. 打开开发者控制台：
   - 飞书：https://open.feishu.cn/
   - Lark：https://open.larksuite.com/
2. 创建应用
3. 复制 **App ID** 和 **App Secret**
4. 启用 **机器人** 能力

### 2. 选择连接模式

**WebSocket 模式（推荐）**：
```bash
FEISHU_CONNECTION_MODE=websocket
pip install websockets
```

**Webhook 模式**：
```bash
FEISHU_CONNECTION_MODE=webhook
pip install aiohttp
```

### 3. 配置 Hermes

```bash
# ~/.hermes/.env

# 必需
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=secret_xxx
FEISHU_DOMAIN=feishu  # 或 lark

# 强烈推荐
FEISHU_ALLOWED_USERS=ou_xxx,ou_yyy
FEISHU_HOME_CHANNEL=oc_xxx  # cron 投递目标
```

## 行为特性

| 场景 | 行为 |
|------|------|
| **私信** | Hermes 响应每条消息 |
| **群聊** | 需要 @mention 才响应 |
| **共享群** | 默认按用户隔离会话 |

```yaml
group_sessions_per_user: true
```

## 安全配置

### 用户白名单
```bash
FEISHU_ALLOWED_USERS=ou_xxx,ou_yyy
```

### Webhook 加密密钥
```bash
FEISHU_ENCRYPT_KEY=your-encrypt-key
FEISHU_VERIFICATION_TOKEN=your-verification-token
```

### 群消息策略
```bash
FEISHU_GROUP_POLICY=allowlist  # 默认
```

| 值 | 行为 |
|------|------|
| `open` | 任何人都可用 |
| `allowlist` | 仅白名单用户可用 |
| `disabled` | 完全忽略群消息 |

### 细粒度群控制
```yaml
platforms:
  feishu:
    extra:
      default_group_policy: "open"
      admins:
        - "ou_admin_open_id"
      group_rules:
        "oc_group_chat_id_1":
          policy: "allowlist"
          allowlist:
            - "ou_user_open_id_1"
```

## 交互卡片

当用户点击按钮时，路由为：
```
/card button {"key": "value", ...}
```

在飞书应用中启用事件：`card.action.trigger`

## 媒体支持

### 接收
| 类型 | 处理 |
|------|------|
| 图片 | 下载并缓存 |
| 音频 | 下载并缓存 |
| 视频 | 下载并缓存为文档 |
| 文件 | 下载并缓存 |

### 发送
| 方法 | 内容 |
|------|------|
| `send` | 文本或富文本消息 |
| `send_image` | 原生图片气泡 |
| `send_document` | 文件附件 |
| `send_voice` | 音频文件 |
| `send_video` | 视频消息 |

## 环境变量

| 变量 | 必需 | 默认 | 说明 |
|------|------|------|------|
| `FEISHU_APP_ID` | ✅ | — | App ID |
| `FEISHU_APP_SECRET` | ✅ | — | App Secret |
| `FEISHU_DOMAIN` | — | feishu | feishu 或 lark |
| `FEISHU_CONNECTION_MODE` | — | websocket | websocket 或 webhook |
| `FEISHU_ALLOWED_USERS` | — | — | Open ID 列表 |
| `FEISHU_HOME_CHANNEL` | — | — | 投递目标 chat ID |
| `FEISHU_ENCRYPT_KEY` | — | — | Webhook 签名验证 |
| `FEISHU_VERIFICATION_TOKEN` | — | — | 验证 token |

## 速率限制

Webhook 模式下：
- 60 秒滑动窗口
- 每 (app_id, path, IP) 三元组 120 请求/窗口
