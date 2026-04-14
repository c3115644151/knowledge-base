# Matrix 集成

连接 Matrix 开放联邦消息协议。

## 特性

- 文本、文件、图片、音频、视频
- 端到端加密（E2EE）支持
- 线程支持（MSC3440）
- 自动加入邀请的房间
- 自动线程化回复

## 架构

- 使用 `matrix-nio` Python SDK
- 通过 REST API 和 WebSocket 实时通信
- 兼容任何 Matrix homeserver（Synapse、Conduit、Dendrite、matrix.org）

## 创建 Bot 账号

### 方式一：在 homeserver 注册（推荐）
```bash
# Synapse 示例
register_new_matrix_user -c /etc/synapse/homeserver.yaml http://localhost:8008
```

### 方式二：使用 matrix.org
在 [Element Web](https://app.element.io/) 创建账号。

## 获取 Access Token

### 通过 Element
1. Settings → Help & About → Advanced → 复制 Access Token

### 通过 API
```bash
curl -X POST https://your-server/_matrix/client/v3/login \
  -H "Content-Type: application/json" \
  -d '{"type":"m.login.password","user":"@hermes:your-server.org","password":"your-password"}'
```

## 配置

### 交互式设置
```bash
hermes gateway setup
# 选择 Matrix
```

### 手动配置

**使用 Access Token**：
```bash
# ~/.hermes/.env

# 必需
MATRIX_HOMESERVER=https://matrix.example.org
MATRIX_ACCESS_TOKEN=xxx
MATRIX_ALLOWED_USERS=@alice:matrix.example.org

# 可选
MATRIX_USER_ID=@hermes:matrix.example.org  # 自动检测
MATRIX_REQUIRE_MENTION=true  # 房间内需要 @mention
MATRIX_AUTO_THREAD=true  # 自动创建线程
```

**使用密码登录**：
```bash
MATRIX_USER_ID=@hermes:matrix.example.org
MATRIX_PASSWORD=xxx
```

## E2EE 端到端加密

### 安装依赖
```bash
pip install 'matrix-nio[e2e]'

# Debian/Ubuntu
sudo apt install libolm-dev

# macOS
brew install libolm
```

### 启用加密
```bash
MATRIX_ENCRYPTION=true
```

加密密钥存储在 `~/.hermes/platforms/matrix/store/`。

## 行为特性

| 场景 | 行为 |
|------|------|
| **私信** | 无需 @mention |
| **房间** | 默认需要 @mention（设置 `MATRIX_REQUIRE_MENTION=false` 改变） |
| **线程** | 自动保持线程上下文隔离 |
| **自动线程化** | 默认每个回复创建线程（设置 `MATRIX_AUTO_THREAD=false` 禁用） |
| **多人房间** | 默认按用户隔离会话 |

## 配置示例

```yaml
# config.yaml
group_sessions_per_user: true

matrix:
  require_mention: true
  auto_thread: true
  free_response_rooms:
    - "!abc123:matrix.org"
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| Bot 不响应 | 检查 `MATRIX_ALLOWED_USERS` 包含你的 ID（完整格式 `@user:server`） |
| 认证失败 | 验证 access token 有效 |
| 加密错误 | 确认 `libolm` 已安装，`MATRIX_ENCRYPTION=true` 已设置，在 Element 中验证 Bot 设备 |
