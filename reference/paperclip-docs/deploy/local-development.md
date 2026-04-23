# 本地开发

> **核心摘要**: 零外部依赖在本地运行 Paperclip。包括开发服务器启动、数据管理和健康检查。

## 前提条件

- Node.js 20+
- pnpm 9+

## 启动开发服务器

```bash
pnpm install
pnpm dev
```

这启动：
- **API 服务器** at `http://localhost:3100`
- **UI** 由 API 服务器在开发中间件模式下提供（同源）

无需 Docker 或外部数据库。Paperclip 自动使用嵌入式 PostgreSQL。

## 一命令引导

首次安装：

```bash
pnpm paperclipai run
```

这会：
1. 如果配置缺失则自动 onboard
2. 运行启用修复的 `paperclipai doctor`
3. 检查通过时启动服务器

## Dev 中的绑定预设

默认 `pnpm dev` 保持在 `local_trusted` 且仅 loopback 绑定。

打开 Paperclip 到私有网络并启用登录：

```bash
pnpm dev --bind lan
```

对于 Tailscale-only 绑定（在检测到的 tailnet 地址上）：

```bash
pnpm dev --bind tailnet
```

允许额外的私有主机名：

```bash
pnpm paperclipai allowed-hostname dotta-macbook-pro
```

## 健康检查

```bash
curl http://localhost:3100/api/health
# -> {"status":"ok"}

curl http://localhost:3100/api/companies
# -> []
```

## 重置开发数据

擦除本地数据并重新开始：

```bash
rm -rf ~/.paperclip/instances/default/db
pnpm dev
```

## 数据位置

| 数据 | 路径 |
|------|------|
| 配置 | `~/.paperclip/instances/default/config.json` |
| 数据库 | `~/.paperclip/instances/default/db` |
| 存储 | `~/.paperclip/instances/default/data/storage` |
| Secrets 密钥 | `~/.paperclip/instances/default/secrets/master.key` |
| 日志 | `~/.paperclip/instances/default/logs` |

用环境变量覆盖：

```bash
PAPERCLIP_HOME=/custom/path PAPERCLIP_INSTANCE_ID=dev pnpm paperclipai run
```
