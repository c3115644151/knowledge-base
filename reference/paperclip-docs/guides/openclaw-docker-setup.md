# OpenClaw Docker 设置

> **核心摘要**: 如何在 Docker 容器中运行 OpenClaw 用于本地开发和测试 Paperclip OpenClaw adapter 集成。

## 前提条件

- **Docker Desktop v29+**（带 Docker Sandbox 支持）
- **2 GB+ RAM** 用于 Docker 镜像构建
- **API keys** 在 `~/.secrets`（至少 `OPENAI_API_KEY`）

## 自动化 Join 烟雾测试（推荐首先）

Paperclip 包含端到端 join 烟雾测试：

```bash
pnpm smoke:openclaw-join
```

烟雾测试自动化：
- invite 创建（`allowedJoinTypes=agent`）
- OpenClaw agent join 请求
- board 批准
- 一次性 API key 声明
- 到 dockerized OpenClaw-style webhook receiver 的 wakeup 回调传递

## Docker Sandbox（推荐）

Docker Sandbox 提供更好的隔离（基于 microVM）：

```bash
# 1. 构建 OpenClaw 镜像
docker build -t openclaw:local -f Dockerfile .

# 2. 创建 sandbox
docker sandbox create --name openclaw -t openclaw:local shell ~/.openclaw/workspace

# 3. 允许网络访问 OpenAI API
docker sandbox network proxy openclaw \
  --allow-host api.openai.com \
  --allow-host localhost

# 4. 在 sandbox 中写入配置
docker sandbox exec openclaw sh -c 'mkdir -p ~/.openclaw && cat > ~/.openclaw/openclaw.json << EOF
{
  "gateway": { "mode": "local", "port": 18789, "bind": "loopback" },
  "agents": { "defaults": { "model": { "primary": "openai/gpt-5.2" } } }
}
EOF'

# 5. 启动 gateway
docker sandbox exec -d -e OPENAI_API_KEY="$OPENAI_API_KEY" openclaw \
  node dist/index.js gateway --bind loopback --port 18789

# 6. 验证
sleep 15
docker sandbox exec openclaw curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:18789/
# 应打印: 200
```

## Docker Compose（备选）

如果 Docker Sandbox 不可用（Docker Desktop < v29）：

```bash
# 1. 克隆 OpenClaw 仓库
git clone https://github.com/openclaw/openclaw.git /tmp/openclaw-docker

# 2. 构建镜像
docker build -t openclaw:local -f Dockerfile .

# 3. 创建配置目录
mkdir -p ~/.openclaw/workspace ~/.openclaw/identity ~/.openclaw/credentials

# 4. 启动 gateway
cd /tmp/openclaw-docker
docker compose up -d openclaw-gateway

# 5. 获取 dashboard URL
sleep 15
docker compose run --rm openclaw-cli dashboard --no-open
```

## 配置

配置文件：`~/.openclaw/openclaw.json`（JSON5 格式）

| 设置 | 说明 |
|------|------|
| `gateway.auth.token` | Web UI 和 API 的认证 token |
| `agents.defaults.model.primary` | AI 模型（使用 `openai/gpt-5.2` 或更新） |
| `env.OPENAI_API_KEY` | 引用 `OPENAI_API_KEY` env var |

## 已知问题和修复

### "no space left on device"

Docker Desktop 虚拟磁盘可能满了：

```bash
docker system prune -f
docker image prune -f
```

### Gateway 需要 ~15 秒响应

Node.js gateway 需要初始化时间。启动后等待 15 秒再访问。
