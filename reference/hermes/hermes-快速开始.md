# Quickstart

快速入门指南，安装 Hermes Agent 并开始使用。

## 安装

```bash
# Linux / macOS / WSL2 / Android (Termux)
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

安装完成后重新加载 shell：
```bash
source ~/.bashrc  # 或 source ~/.zshrc
```

## 配置 LLM Provider

```bash
hermes model       # 选择 LLM provider 和模型
hermes tools       # 配置启用的工具
hermes setup       # 一站式配置向导
```

### 支持的 Provider

| Provider | 配置方式 |
|----------|----------|
| **Nous Portal** | OAuth 登录（零配置） |
| **OpenAI Codex** | Device code 认证 |
| **Anthropic** | Claude Code 认证或 API Key |
| **OpenRouter** | 输入 API Key |
| **Hugging Face** | 设置 `HF_TOKEN` |
| **DeepSeek** | 设置 `DEEPSEEK_API_KEY` |
| **Custom Endpoint** | VLLM/SGLang/Ollama，设置 base URL + API Key |

> **最低要求**：64K tokens context window

## 开始对话

```bash
hermes
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `hermes` | 开始对话 |
| `hermes model` | 选择模型 |
| `hermes --continue` / `hermes -c` | 恢复上次会话 |
| `hermes update` | 更新版本 |
| `hermes gateway` | 启动消息网关 |

## 快捷功能

- **斜杠命令**：输入 `/` 查看所有命令
  - `/help` - 帮助
  - `/tools` - 列出工具
  - `/model` - 切换模型
  - `/save` - 保存会话

- **多行输入**：`Alt+Enter` 或 `Ctrl+J`

- **中断代理**：输入新消息或 `Ctrl+C`

## 下一步

- [CLI Guide](hermes-CLI.md) - 掌握终端界面
- [Configuration](hermes-配置.md) - 自定义配置
- [Messaging Gateway](hermes-飞书.md) - 连接消息平台
