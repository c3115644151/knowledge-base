# 设置命令

> **核心摘要**: 实例引导和诊断命令。包括 `run`、`onboard`、`doctor`、`configure` 等。

## `paperclipai run`

一命令引导和启动：

```bash
pnpm paperclipai run
```

执行：
1. 如果配置缺失则自动 onboard
2. 运行启用修复的 `paperclipai doctor`
3. 检查通过时启动服务器

选择特定实例：

```bash
pnpm paperclipai run --instance dev
```

## `paperclipai onboard`

交互式首次设置：

```bash
pnpm paperclipai onboard
```

如果 Paperclip 已配置，重新运行 `onboard` 保留现有配置。使用 `paperclipai configure` 更改现有安装的设置。

首次提示：
1. `Quickstart`（推荐）：本地默认值（嵌入式数据库、无 LLM 提供商、本地磁盘存储、默认 secrets）
2. `Advanced setup`：完整交互式配置

引导后立即启动：

```bash
pnpm paperclipai onboard --run
```

非交互式默认值 + 立即启动：

```bash
pnpm paperclipai onboard --yes
```

## `paperclipai doctor`

健康检查（带可选自动修复）：

```bash
pnpm paperclipai doctor
pnpm paperclipai doctor --repair
```

验证：
- 服务器配置
- 数据库连接
- Secrets adapter 配置
- 存储配置
- 缺失的关键文件

## `paperclipai configure`

更新配置部分：

```bash
pnpm paperclipai configure --section server
pnpm paperclipai configure --section secrets
pnpm paperclipai configure --section storage
```

## `paperclipai env`

显示解析后的环境配置：

```bash
pnpm paperclipai env
```

## `paperclipai allowed-hostname`

允许用于认证/私有模式的私有主机名：

```bash
pnpm paperclipai allowed-hostname my-tailscale-host
```

## 本地存储路径

| 数据 | 默认路径 |
|------|----------|
| 配置 | `~/.paperclip/instances/default/config.json` |
| 数据库 | `~/.paperclip/instances/default/db` |
| 日志 | `~/.paperclip/instances/default/logs` |
| 存储 | `~/.paperclip/instances/default/data/storage` |
| Secrets 密钥 | `~/.paperclip/instances/default/secrets/master.key` |

用以下方式覆盖：

```bash
PAPERCLIP_HOME=/custom/home PAPERCLIP_INSTANCE_ID=dev pnpm paperclipai run
```

或直接在任何命令上传递 `--data-dir`：

```bash
pnpm paperclipai run --data-dir ./tmp/paperclip-dev
pnpm paperclipai doctor --data-dir ./tmp/paperclip-dev
```
