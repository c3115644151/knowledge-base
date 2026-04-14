# Docker 部署

## 两种 Docker 使用方式

1. **在 Docker 中运行 Hermes** - Agent 本身在容器内运行
2. **Docker 作为终端后端** - Agent 在主机运行，命令在 Docker 沙箱中执行

## 在 Docker 中运行 Hermes

### 快速开始

```bash
# 首次设置向导
docker run -it --rm \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent setup
```

### 运行网关模式

```bash
docker run -d \
  --name hermes \
  --restart unless-stopped \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent gateway run
```

### 交互式聊天

```bash
docker run -it --rm \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent
```

## 持久化卷

`/opt/data` 是所有 Hermes 状态的单一真相来源：

| 路径 | 内容 |
|------|------|
| `.env` | API 密钥 |
| `config.yaml` | 配置 |
| `SOUL.md` | 人格 |
| `sessions/` | 会话历史 |
| `memories/` | 记忆 |
| `skills/` | 技能 |
| `cron/` | 定时任务 |
| `logs/` | 日志 |

## Docker Compose

```yaml
version: "3.8"
services:
  hermes:
    image: nousresearch/hermes-agent:latest
    container_name: hermes
    restart: unless-stopped
    command: gateway run
    volumes:
      - ~/.hermes:/opt/data
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2.0"
```

```bash
docker compose up -d
docker compose logs -f hermes
```

## 环境变量传递

```bash
docker run -d \
  --name hermes \
  -v ~/.hermes:/opt/data \
  -e ANTHROPIC_API_KEY="sk-ant-..." \
  -e OPENAI_API_KEY="sk-..." \
  nousresearch/hermes-agent gateway run
```

## 资源限制

| 资源 | 最小 | 推荐 |
|------|------|------|
| 内存 | 1 GB | 2-4 GB |
| CPU | 1 核 | 2 核 |
| 磁盘 | 500 MB | 2+ GB |

浏览器自动化最耗内存，不需要时 1GB 足够。

```bash
docker run -d \
  --name hermes \
  --memory=4g --cpus=2 \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent gateway run
```

## Playwright 浏览器支持

浏览器工具需要共享内存：

```bash
docker run -d \
  --name hermes \
  --shm-size=1g \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent gateway run
```

## 升级

```bash
docker pull nousresearch/hermes-agent:latest
docker rm -f hermes
docker run -d \
  --name hermes \
  --restart unless-stopped \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent gateway run
```

## Docker 终端后端

Agent 在主机运行，命令在 Docker 容器中执行：

```yaml
# ~/.hermes/config.yaml
terminal:
  backend: docker
  docker_image: "nikolaik/python-nodejs:python3.11-nodejs20"
  docker_volumes:
    - "/home/user/projects:/workspace/projects"
  container_cpu: 1
  container_memory: 5120
```

参见 [配置 - 终端后端](hermes-配置.md) 获取完整参考。

## 故障排除

### 容器立即退出
检查日志：`docker logs hermes`
- 缺少或无效的 `.env`
- 端口冲突

### 权限错误
```bash
chmod -R 755 ~/.hermes
```

### 浏览器工具不工作
添加 `--shm-size=1g`

### 健康检查
```bash
docker logs --tail 50 hermes
docker exec hermes hermes version
docker stats hermes
```
