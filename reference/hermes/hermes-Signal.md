# Signal 消息

通过 signal-cli 连接 Signal，实现端到端加密消息。

## 架构

- 使用 [signal-cli](https://github.com/AsamK/signal-cli) 的 HTTP 模式
- SSE (Server-Sent Events) 实时流式消息
- JSON-RPC 发送响应
- 无额外 Python 依赖（仅需 `httpx`）

## 前置条件

- **signal-cli** - Java 版 Signal 客户端
- **Java 17+** 运行时
- **Signal 手机号**（作为链接设备）

## 安装 signal-cli

```bash
# macOS
brew install signal-cli

# Linux (下载最新版本)
VERSION=$(curl -Ls -o /dev/null -w %{url_effective} \
  https://github.com/AsamK/signal-cli/releases/latest | sed 's/^.*\/v//')
curl -L -O "https://github.com/AsamK/signal-cli/releases/download/v${VERSION}/signal-cli-${VERSION}.tar.gz"
sudo tar xf "signal-cli-${VERSION}.tar.gz" -C /opt
sudo ln -sf "/opt/signal-cli-${VERSION}/bin/signal-cli" /usr/local/bin/
```

## 配置步骤

### 1. 链接 Signal 账号
```bash
signal-cli link -n "HermesAgent"
```
会显示 QR 码或链接：
1. 打开 Signal → 设置 → 链接设备 → 链接新设备
2. 扫描 QR 码或输入 URI

### 2. 启动 signal-cli 守护进程
```bash
# 替换为你的 Signal 号码（E.164 格式）
signal-cli --account +1234567890 daemon --http 127.0.0.1:8080
```

验证运行：
```bash
curl http://127.0.0.1:8080/api/v1/check
# 返回: {"versions":{"signal-cli":...}}
```

### 3. 配置 Hermes
```bash
hermes gateway setup
# 选择 Signal 平台
```

手动配置（`~/.hermes/.env`）：
```bash
# 必需
SIGNAL_HTTP_URL=http://127.0.0.1:8080
SIGNAL_ACCOUNT=+1234567890

# 安全
SIGNAL_ALLOWED_USERS=+1234567890,+0987654321

# 可选
SIGNAL_GROUP_ALLOWED_USERS=groupId1,groupId2  # 群组访问
SIGNAL_HOME_CHANNEL=+1234567890  # cron 任务默认投递目标
```

## 访问控制

| 配置 | 行为 |
|------|------|
| `SIGNAL_ALLOWED_USERS` 已设置 | 仅白名单用户可交互 |
| 未设置白名单 | 未知用户收到配对码 |
| `SIGNAL_ALLOW_ALL_USERS=true` | 任何人可交互（谨慎使用） |

| 配置 | 行为 |
|------|------|
| 未设置 | 所有群消息被忽略 |
| 设置群 ID | 仅列出的群被监控 |
| 设置为 `*` | Bot 所在的所有群都响应 |

## 功能

- **附件**：接收/发送图片、音频、文档（100MB 限制）
- **打字指示器**：处理时显示
- **电话号码脱敏**：日志中自动脱敏 `+15551234567` → `+155****4567`
- **Note to Self**：如果用自己号码运行，可用"给自己发消息"功能
- **健康监控**：自动重连（SSE 断开、空闲 120 秒）

## 环境变量

| 变量 | 必需 | 默认 | 说明 |
|------|------|------|------|
| `SIGNAL_HTTP_URL` | ✅ | — | signal-cli HTTP 端点 |
| `SIGNAL_ACCOUNT` | ✅ | — | Bot 手机号（E.164） |
| `SIGNAL_ALLOWED_USERS` | — | — | 逗号分隔的电话号/UUID |
| `SIGNAL_GROUP_ALLOWED_USERS` | — | — | 群组 ID 列表或 `*` |
| `SIGNAL_HOME_CHANNEL` | — | — | cron 默认投递目标 |

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| "Cannot reach signal-cli" | 确保 daemon 正在运行 |
| 消息未收到 | 检查 `SIGNAL_ALLOWED_USERS` 包含发送者号码（含 `+` 前缀） |
| 群消息被忽略 | 配置 `SIGNAL_GROUP_ALLOWED_USERS` |
