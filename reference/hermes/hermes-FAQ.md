# 常见问题 (FAQ)

## 概述

### Hermes Agent 是什么？

Hermes Agent 是一个开源 AI Agent，支持 CLI 和消息网关模式，具备持久记忆、技能系统、MCP 集成、语音交互等能力。MIT 许可证。

### 支持哪些平台？

- **消息**: Telegram, Discord, Slack, WhatsApp, Signal, Email, Home Assistant, 钉钉, 飞书, 企业微信
- **开发**: VS Code, Zed, JetBrains (via ACP)
- **协议**: MCP (Model Context Protocol)

### 它能做什么？

- 终端/命令行自动化
- 网页搜索和浏览
- 文件操作和代码编辑
- 多平台消息发送
- 定时任务调度
- 子代理并行任务
- 语音对话 (CLI 和 Discord)
- 浏览器自动化

## 安装与设置

### 如何安装？

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

参见 [安装指南](hermes-安装.md)。

### 需要什么模型？

需要 **64K+ 上下文窗口** 的模型。推荐：
- Claude 3.5+ (200K)
- GPT-4 Turbo (128K)
- Gemini 1.5 Pro (1M)
- DeepSeek V3 (128K)

### 支持本地模型吗？

是。使用自定义端点配置：
```bash
hermes model  # 选择 "Custom endpoint"
```

支持 Ollama、vLLM、SGLang 等。

## 配置

### API 密钥放哪里？

- **密钥**: `~/.hermes/.env`
- **其他配置**: `~/.hermes/config.yaml`

### 多个 LLM 提供商？

支持。使用 `provider_routing` 配置 OpenRouter 内部路由。

## 记忆与技能

### 记忆和技能的区别？

- **记忆**: 存储事实，跨会话自动检索
- **技能**: 存储步骤指导，按需加载

参见 [记忆系统](hermes-记忆.md) 和 [技能系统](hermes-技能.md)。

### 如何让 Agent 记住信息？

```
/remember My API key is xxx for service Y
```

或直接告诉 Agent，它会自动存储重要信息。

## 会话

### 如何恢复之前的会话？

```bash
hermes --continue  # 最近会话
hermes -r <session_id>  # 指定会话
```

### 对话太长怎么办？

使用 `/compress` 压缩对话历史，保留关键上下文。

## 安全

### Agent 能执行危险命令吗？

有安全检查。危险命令需要审批：
- `rm -rf`
- `DROP TABLE`
- `curl ... | sh`

使用 Docker 后端时跳过审批（容器是安全边界）。

### 如何保护 API 密钥？

- 设置 `chmod 600 ~/.hermes/.env`
- 不要提交到版本控制
- 使用白名单限制访问

参见 [安全指南](hermes-安全.md)。

## 故障排除

### "hermes: command not found"

```bash
source ~/.bashrc
```

或检查 `~/.local/bin` 是否在 PATH 中。

### 模型不工作

```bash
hermes doctor
hermes model  # 重新配置
```

### 速率限制

- 等待后重试
- 配置凭证池轮换密钥
- 考虑升级计划

### 上下文溢出

```bash
/compress
```

或使用更长上下文的模型。
