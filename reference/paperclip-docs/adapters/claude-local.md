# Claude Local Adapter

> **核心摘要**: `claude_local` adapter 在本地运行 Anthropic 的 Claude Code CLI。支持 session 持久化、skills 注入和结构化输出解析。

## 前提条件

- Claude Code CLI 已安装（`claude` 命令可用）
- `ANTHROPIC_API_KEY` 在环境或 Agent 配置中设置

## 配置字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `cwd` | string | 是 | Agent 进程的工作目录（绝对路径；权限允许时自动创建） |
| `model` | string | 否 | 要使用的 Claude 模型（例如 `claude-opus-4-6`） |
| `promptTemplate` | string | 否 | 所有运行使用的 prompt |
| `env` | object | 否 | 环境变量（支持 secret 引用） |
| `timeoutSec` | number | 否 | 进程超时（0 = 无超时） |
| `graceSec` | number | 否 | 超时/取消后强制终止前的宽限期 |
| `maxTurnsPerRun` | number | 否 | 每个 heartbeat 的最大 agentic 轮次（默认 `300`） |
| `dangerouslySkipPermissions` | boolean | 否 | 跳过权限提示（默认：`true`）；无人值守运行需要 |
| `instructionsFilePath` | string | 否 | Agent 指令文件路径（Markdown） |

## Prompt 模板

模板支持 `{{variable}}` 替换：

| 变量 | 值 |
|------|-----|
| `{{agentId}}` | Agent 的 ID |
| `{{companyId}}` | 公司 ID |
| `{{runId}}` | 当前运行 ID |
| `{{agent.name}}` | Agent 的名称 |
| `{{company.name}}` | 公司名称 |

## Session 持久化

Adapter 在 heartbeats 之间持久化 Claude Code session ID。下次唤醒时，它恢复现有对话，使 Agent 保留完整上下文。

Session 恢复是 cwd 感知的：如果自上次运行以来 Agent 的工作目录发生变化，则启动新 session 而不是恢复。

如果使用未知 session ID 恢复失败，Adapter 自动重试并使用新 session。

## Skills 注入

Adapter 创建一个临时目录，包含 Paperclip skills 的符号链接，并通过 `--add-dir` 传递。这使得 skills 可被发现，而不污染 Agent 的工作目录。

## 环境测试

使用 UI 中的"Test Environment"按钮验证 adapter 配置。它检查：

- Claude CLI 已安装且可访问
- 工作目录是绝对路径且可用（如果缺失且允许则自动创建）
- API 密钥/认证模式提示（`ANTHROPIC_API_KEY` vs 订阅登录）
- 实时 hello 探测（使用 prompt `Respond with hello.`）验证 CLI 准备就绪
