# 钉钉集成

连接钉钉作为 Chatbot，支持 Stream Mode（无需公网 webhook）。

## 架构

- **Stream Mode**（推荐）- WebSocket 长连接，无需公网 URL
- Markdown 格式回复
- 无需穿透 NAT 或配置反向代理

## 前置条件

- 钉钉开发者账号
- 创建的钉钉应用
- 钉钉 User ID

## 安装依赖

```bash
pip install dingtalk-stream httpx
```

## 配置步骤

### 1. 创建钉钉应用

1. 进入 [钉钉开发者控制台](https://open-dev.dingtalk.com/)
2. 应用开发 → 创建企业内部应用
3. 启用 **机器人** 能力
4. 消息接收模式选择 **Stream 模式**

### 2. 获取凭证

在 **凭证与基础信息** 页面复制：
- Client ID（AppKey）
- Client Secret（AppSecret）

### 3. 配置 Hermes

```bash
# ~/.hermes/.env

# 必需
DINGTALK_CLIENT_ID=your-app-key
DINGTALK_CLIENT_SECRET=your-app-secret

# 安全（必需）
DINGTALK_ALLOWED_USERS=user-id-1
# 或多个用户
DINGTALK_ALLOWED_USERS=user-id-1,user-id-2
```

### 交互式设置
```bash
hermes gateway setup
# 选择 DingTalk
```

## 行为特性

| 场景 | 行为 |
|------|------|
| **私信** | 无需 @mention，每条私信独立会话 |
| **群聊** | 需要 @mention 才响应 |
| **共享群多人** | 默认按用户隔离会话 |

```yaml
# config.yaml
group_sessions_per_user: true
```

## 环境变量

| 变量 | 必需 | 默认 | 说明 |
|------|------|------|------|
| `DINGTALK_CLIENT_ID` | ✅ | — | AppKey |
| `DINGTALK_CLIENT_SECRET` | ✅ | — | AppSecret |
| `DINGTALK_ALLOWED_USERS` | — | — | 允许的 User ID |

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| Bot 不响应 | 确认机器人能力已启用，Stream 模式已选择，User ID 在白名单中 |
| Stream 断开 | 网络问题或凭证失效，自动重连（指数退避） |
| "No session_webhook" | Bot 重启后 webhook 过期，发送新消息刷新 |
