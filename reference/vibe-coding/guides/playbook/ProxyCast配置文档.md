# ProxyCast 完整配置 - 配置协议

## 前置条件检查清单

- [ ] ProxyCast 可执行文件已部署
- [ ] AI 凭证已配置（Kiro/Gemini/Qwen/OpenRouter）
- [ ] 端口 8999 未被占用
- [ ] Claude Code / 其他 AI 工具已安装
- [ ] （可选）SQLite3 用于数据库操作
- [ ] （可选）Systemd 用于服务管理

## 配置步骤（IF-THEN）

### 步骤 1：启动 ProxyCast 服务

```
IF ProxyCast 未运行
THEN 启动服务
```

```bash
cd /path/to/proxycast-main && ./src-tauri/target/release/proxycast &
# 服务监听: http://127.0.0.1:8999
```

### 步骤 2：配置 Claude Code（禁用遥测）

```
IF 需要使用 Claude Code 通过 ProxyCast
THEN 设置环境变量并启动
```

```bash
# Claude Opus 4.6
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 \
ANTHROPIC_BASE_URL=http://127.0.0.1:8999 \
ANTHROPIC_API_KEY=proxy_cast \
claude --dangerously-skip-permissions --model claude-opus-4-5

# Claude Sonnet 4.5
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 \
ANTHROPIC_BASE_URL=http://127.0.0.1:8999 \
ANTHROPIC_API_KEY=proxy_cast \
claude --dangerously-skip-permissions --model claude-sonnet-4-5
```

### 步骤 3：配置其他 AI 工具

```
IF 需要配置 Cherry Studio / Cursor / Cline / Python
THEN 使用以下通用配置
```

| 配置项 | 值 |
|--------|-----|
| API Base URL | `http://127.0.0.1:8999/v1` |
| API Key | `proxy_cast` |
| 默认模型 | `claude-opus-4-5` |

```python
# Python 示例
from openai import OpenAI
client = OpenAI(
    base_url="http://127.0.0.1:8999/v1",
    api_key="proxy_cast"
)
```

### 步骤 4：刷新 Kiro Token（如过期）

```
IF Kiro Token 过期导致 API 调用失败
THEN 执行刷新脚本
```

```bash
REFRESH_TOKEN=$(cat ~/.aws/sso/cache/kiro-auth-token.json | jq -r '.refreshToken')
curl -s -X POST "https://prod.us-east-1.auth.desktop.kiro.dev/refreshToken" \
  -H "Content-Type: application/json" \
  -d "{\"refreshToken\": \"$REFRESH_TOKEN\"}" > /tmp/new_token.json

# 更新 token 文件
cat ~/.aws/sso/cache/kiro-auth-token.json | jq --slurpfile new /tmp/new_token.json \
  '.accessToken = $new[0].accessToken | .expiresAt = (now + 3600 | todate)' \
  > ~/.aws/sso/cache/kiro-auth-token.json.tmp
mv ~/.aws/sso/cache/kiro-auth-token.json.tmp ~/.aws/sso/cache/kiro-auth-token.json
```

### 步骤 5：配置 Systemd 服务（可选）

```
IF 需要开机自启 ProxyCast
THEN 创建 systemd 服务
```

```bash
cat > /etc/systemd/system/proxycast.service << 'EOF'
[Unit]
Description=ProxyCast API Proxy Service
After=network.target

[Service]
Type=simple
User=<username>
WorkingDirectory=/path/to/proxycast-main
ExecStart=/path/to/proxycast-main/src-tauri/target/release/proxycast
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable proxycast
sudo systemctl start proxycast
```

## 验证检查点

- [ ] `curl http://127.0.0.1:8999/v1/models -H "Authorization: Bearer proxy_cast"` 返回模型列表
- [ ] Claude Code 启动后能正常对话
- [ ] `ps aux | grep proxycast` 显示进程运行中
- [ ] `ss -tlnp | grep 8999` 显示端口监听
- [ ] API 调用返回正确响应（包含 `choices` 字段）

## 可用模型速查

| Provider | 模型 | 用途 |
|----------|------|------|
| Kiro | `claude-opus-4-5` | 最强性能 |
| Kiro | `claude-sonnet-4-5` | 平衡性能 |
| Gemini | `gemini-2.5-flash` | 快速响应 |
| OpenRouter | `deepseek/deepseek-r1-0528:free` | 推理任务 |
| OpenRouter | `mistralai/devstral-2512:free` | 代码任务 |

## 常见故障

| 问题 | 解决方案 |
|------|----------|
| ProxyCast 未运行 | 执行 `ps aux \| grep proxycast`，未找到则启动 |
| Token 过期 | 在 ProxyCast 界面点击"刷新 Token" |
| 遥测断线 | 确保设置 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` |
| 端口冲突 | 检查 `ss -tlnp \| grep 8999`，杀死占用进程 |
