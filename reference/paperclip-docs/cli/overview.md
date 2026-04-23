# CLI 概览

> **核心摘要**: Paperclip CLI 处理实例设置、诊断和控制平面操作。支持上下文配置文件以存储默认值。

## 用法

```bash
pnpm paperclipai --help
```

## 全局选项

所有命令支持：

| 选项 | 说明 |
|------|------|
| `--data-dir <path>` | 本地 Paperclip 数据根目录（与 `~/.paperclip` 隔离） |
| `--api-base <url>` | API base URL |
| `--api-key <token>` | API 认证 token |
| `--context <path>` | 上下文文件路径 |
| `--profile <name>` | 上下文配置文件名 |
| `--json` | 输出为 JSON |

公司范围的命令也接受 `--company-id <id>`。

## 上下文配置

存储默认值以避免重复选项：

```bash
# 设置默认值
pnpm paperclipai context set --api-base http://localhost:3100 --company-id <id>

# 查看当前上下文
pnpm paperclipai context show

# 列出配置文件
pnpm paperclipai context list

# 切换配置文件
pnpm paperclipai context use default
```

避免在上下文中存储 secrets，使用环境变量：

```bash
pnpm paperclipai context set --api-key-env-var-name PAPERCLIP_API_KEY
export PAPERCLIP_API_KEY=...
```

上下文存储在 `~/.paperclip/context.json`。

## 命令分类

CLI 有两类：

1. **[Setup 命令](./setup-commands.md)** — 实例引导、诊断、配置
2. **[Control-plane 命令](./control-plane-commands.md)** — Issues、Agents、Approvals、Activity
