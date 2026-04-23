# Codex Local Adapter

> **核心摘要**: `codex_local` adapter 在本地运行 OpenAI 的 Codex CLI。支持通过 `previous_response_id` 链路的 session 持久化和通过全局 Codex skills 目录的 skills 注入。

## 前提条件

- Codex CLI 已安装（`codex` 命令可用）
- `OPENAI_API_KEY` 在环境或 Agent 配置中设置

## 配置字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `cwd` | string | 是 | Agent 进程的工作目录（绝对路径；权限允许时自动创建） |
| `model` | string | 否 | 要使用的模型 |
| `promptTemplate` | string | 否 | 所有运行使用的 prompt |
| `env` | object | 否 | 环境变量（支持 secret 引用） |
| `timeoutSec` | number | 否 | 进程超时（0 = 无超时） |
| `graceSec` | number | 否 | 超时/取消后强制终止前的宽限期 |
| `fastMode` | boolean | 否 | 启用 Codex Fast 模式。当前仅支持 `gpt-5.4`，消耗更快 |
| `dangerouslyBypassApprovalsAndSandbox` | boolean | 否 | 跳过安全检查（仅开发用） |
| `instructionsFilePath` | string | 否 | Agent 指令文件路径 |

## Session 持久化

Codex 使用 `previous_response_id` 实现会话连续性。Adapter 跨 heartbeats 序列化和恢复此 ID，使 Agent 能够保持对话上下文。

## Skills 注入

Adapter 将 Paperclip skills 符号链接到 Codex 全局 skills 目录（`~/.codex/skills`）。现有用户 skills 不会被覆盖。

## Fast 模式

启用 `fastMode` 时，Paperclip 添加等效于以下内容的 Codex 配置覆盖：

```bash
-c 'service_tier="fast"' -c 'features.fast_mode=true'
```

Paperclip 当前仅在选定模型为 `gpt-5.4` 时应用此设置。在其他模型上，此开关保留在配置中但在执行时被忽略。

## 托管 `CODEX_HOME`

当 Paperclip 在托管 worktree 实例内运行时（`PAPERCLIP_IN_WORKTREE=true`），Adapter 使用 Paperclip 实例下的 worktree 隔离 `CODEX_HOME`，以便 Codex skills、sessions、logs 和其他运行时状态不会跨 checkouts 泄漏。它从用户主 Codex home 播种隔离的 home 以保持共享认证/配置连续性。

## 环境测试

环境测试检查：

- Codex CLI 已安装且可访问
- 工作目录是绝对路径且可用（如果缺失且允许则自动创建）
- 认证信号（`OPENAI_API_KEY` 存在）
- 实时 hello 探测（使用 prompt `Respond with hello.`）验证 CLI 实际可以运行
