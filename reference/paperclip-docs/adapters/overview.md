# Adapters 概览

> **核心摘要**: Adapter 是 Paperclip 编排层与 Agent 运行时之间的桥接器。每个 Adapter 知道如何调用特定类型的 AI Agent 并捕获其结果。

## Adapter 工作原理

当 heartbeat 触发时，Paperclip：

1. 查找 Agent 的 `adapterType` 和 `adapterConfig`
2. 用执行上下文调用 Adapter 的 `execute()` 函数
3. Adapter 生成或调用 Agent 运行时
4. Adapter 捕获 stdout、解析 usage/cost 数据、返回结构化结果

## 内置 Adapter

| Adapter | 类型键 | 说明 |
|---------|--------|------|
| [Claude Local](./claude-local.md) | `claude_local` | 本地运行 Claude Code CLI |
| [Codex Local](./codex-local.md) | `codex_local` | 本地运行 OpenAI Codex CLI |
| [Gemini Local](./gemini-local.md) | `gemini_local` | 本地运行 Gemini CLI（实验性） |
| OpenCode Local | `opencode_local` | 本地运行 OpenCode CLI（多提供商 `provider/model`） |
| Cursor | `cursor` | 在后台模式运行 Cursor |
| Pi Local | `pi_local` | 本地运行嵌入式 Pi Agent |
| Hermes Local | `hermes_local` | 本地运行 Hermes CLI |
| OpenClaw Gateway | `openclaw_gateway` | 连接到 OpenClaw gateway 端点 |
| [Process](./process.md) | `process` | 执行任意 shell 命令 |
| [HTTP](./http.md) | `http` | 发送 webhook 到外部 Agent |

### 外部（插件）Adapter

| Adapter | 包 | 类型键 | 说明 |
|---------|-----|--------|------|
| Droid Local | `@henkey/droid-paperclip-adapter` | `droid_local` | 本地运行 Factory Droid |

## 外部 Adapter

你可以将 Adapter 作为独立包构建和分发 — 无需更改 Paperclip 源代码。外部 Adapter 通过插件系统在启动时加载。

```bash
# 通过 API 从 npm 安装
curl -X POST http://localhost:3102/api/adapters \
  -d '{"packageName": "my-paperclip-adapter"}'
# 或从本地目录链接
curl -X POST http://localhost:3102/api/adapters \
  -d '{"localPath": "/home/user/my-adapter"}'
```

## Adapter 架构

每个 Adapter 是被三个注册表使用的包：

```
my-adapter/
  src/
    index.ts            # 共享元数据（type、label、models）
    server/
      execute.ts        # 核心执行逻辑
      parse.ts          # 输出解析
      test.ts           # 环境诊断
    ui-parser.ts        # 自包含 UI 转录解析器（外部 Adapter）
    cli/
      format-event.ts   # `paperclipai run --watch` 的终端输出
```

| 注册表 | 功能 | 来源 |
|--------|------|------|
| **Server** | 执行 Agent、捕获结果 | 从包根的 `createServerAdapter()` |
| **UI** | 渲染运行转录、提供配置表单 | `ui-parser.js`（动态）或静态导入（内置） |
| **CLI** | 为实时观看格式化终端输出 | 静态导入 |

## 选择 Adapter

| 需求 | 推荐 |
|------|------|
| 需要编码 Agent？ | 使用 `claude_local`、`codex_local`、`opencode_local`、`hermes_local`，或安装 `droid_local` 作为外部插件 |
| 需要运行脚本或命令？ | 使用 `process` |
| 需要调用外部服务？ | 使用 `http` |
| 需要自定义？ | [创建你自己的 Adapter](./creating-an-adapter.md) 或 [构建外部 Adapter 插件](./external-adapters.md) |

## UI Parser 合约

外部 Adapter 可以提供一个自包含的 UI 解析器，告诉 Paperclip Web UI 如何渲染其 stdout。没有它，UI 使用通用 shell 解析器。详见 [UI Parser 合约](./adapter-ui-parser.md)。
