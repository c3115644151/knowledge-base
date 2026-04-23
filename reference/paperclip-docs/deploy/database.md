# 数据库配置

> **核心摘要**: Paperclip 通过 Drizzle ORM 使用 PostgreSQL。支持嵌入式 PGlite（默认）、Docker Postgres 和托管 PostgreSQL（Supabase）。

## 1. 嵌入式 PostgreSQL（默认）

零配置。如果不设置 `DATABASE_URL`，服务器自动启动嵌入式 PostgreSQL 实例。

```bash
pnpm dev
```

首次启动时，服务器：
1. 创建 `~/.paperclip/instances/default/db/` 用于存储
2. 确保 `paperclip` 数据库存在
3. 自动运行迁移
4. 开始服务请求

数据跨重启持久化。要重置：`rm -rf ~/.paperclip/instances/default/db`。

Docker 快速启动也默认使用嵌入式 PostgreSQL。

## 2. 本地 PostgreSQL（Docker）

完整的本地 PostgreSQL 服务器：

```bash
docker compose up -d
```

这在 `localhost:5432` 启动 PostgreSQL 17。设置连接字符串：

```bash
cp .env.example .env
# DATABASE_URL=postgres://paperclip:paperclip@localhost:5432/paperclip
```

推送 schema：

```bash
DATABASE_URL=postgres://paperclip:paperclip@localhost:5432/paperclip \
  npx drizzle-kit push
```

## 3. 托管 PostgreSQL（Supabase）

用于生产，使用托管提供商如 [Supabase](https://supabase.com/)。

1. 在 [database.new](https://database.new) 创建项目
2. 从 Project Settings > Database 复制连接字符串
3. 在 `.env` 中设置 `DATABASE_URL`

使用**直接连接**（端口 5432）用于迁移，应用使用**连接池**（端口 6543）。

如果使用连接池，禁用预处理语句：

```ts
// packages/db/src/client.ts
export function createDb(url: string) {
  const sql = postgres(url, { prepare: false });
  return drizzlePg(sql, { schema });
}
```

## 模式切换

| `DATABASE_URL` | 模式 |
|----------------|------|
| 未设置 | 嵌入式 PostgreSQL |
| `postgres://...localhost...` | 本地 Docker PostgreSQL |
| `postgres://...supabase.com...` | 托管 Supabase |

Drizzle schema（`packages/db/src/schema/`）无论模式如何都相同。
