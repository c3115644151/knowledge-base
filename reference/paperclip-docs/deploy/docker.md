# Docker 部署

> **核心摘要**: 在 Docker 中运行 Paperclip，无需在本地安装 Node 或 pnpm。包括 Docker Compose 快速启动。

## Compose 快速启动（推荐）

```bash
docker compose -f docker/docker-compose.quickstart.yml up --build
```

打开 http://localhost:3100。

默认值：
- 主机端口：`3100`
- 数据目录：`./data/docker-paperclip`

用环境变量覆盖：

```bash
PAPERCLIP_PORT=3200 PAPERCLIP_DATA_DIR=../data/pc \
  docker compose -f docker/docker-compose.quickstart.yml up --build
```

> **注意**：`PAPERCLIP_DATA_DIR` 相对于 compose 文件（`docker/`）解析，所以 `../data/pc` 映射到项目根的 `data/pc`。

## 手动 Docker 构建

```bash
docker build -t paperclip-local .
docker run --name paperclip \
  -p 3100:3100 \
  -e HOST=0.0.0.0 \
  -e PAPERCLIP_HOME=/paperclip \
  -v "$(pwd)/data/docker-paperclip:/paperclip" \
  paperclip-local
```

## 数据持久化

所有数据持久化在绑定挂载下（`./data/docker-paperclip`）：
- 嵌入式 PostgreSQL 数据
- 上传的资源
- 本地 secrets 密钥
- Agent 工作区数据

## Docker 中的 Claude 和 Codex Adapter

Docker 镜像预装了：
- `claude`（Anthropic Claude Code CLI）
- `codex`（OpenAI Codex CLI）

传递 API 密钥以启用容器内的本地 adapter 运行：

```bash
docker run --name paperclip \
  -p 3100:3100 \
  -e HOST=0.0.0.0 \
  -e PAPERCLIP_HOME=/paperclip \
  -e OPENAI_API_KEY=sk-... \
  -e ANTHROPIC_API_KEY=sk-... \
  -v "$(pwd)/data/docker-paperclip:/paperclip" \
  paperclip-local
```

没有 API 密钥，应用正常运行 — adapter 环境检查会显示缺失的先决条件。
