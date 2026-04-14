# 回退提供商

Hermes Agent 有三层弹性机制：

1. **凭证池** — 同一提供商多个 API 密钥轮换（最先尝试）
2. **主模型回退** — 主模型失败时自动切换到不同 provider:model
3. **辅助任务回退** — 视觉、压缩、网页提取等独立提供商解析

## 主模型回退

主 LLM 提供商遇到错误时（速率限制、服务器过载、认证失败、连接中断），自动切换到备用 provider:model。

### 配置

```yaml
fallback_model:
  provider: openrouter
  model: anthropic/claude-sonnet-4
```

### 支持的提供商

| 提供商 | 值 | 需求 |
|--------|-----|------|
| AI Gateway | `ai-gateway` | `AI_GATEWAY_API_KEY` |
| OpenRouter | `openrouter` | `OPENROUTER_API_KEY` |
| Nous Portal | `nous` | `hermes auth` (OAuth) |
| OpenAI Codex | `openai-codex` | `hermes model` (ChatGPT OAuth) |
| GitHub Copilot | `copilot` | `COPILOT_GITHUB_TOKEN` |
| GitHub Copilot ACP | `copilot-acp` | 外部进程（编辑器集成） |
| Anthropic | `anthropic` | `ANTHROPIC_API_KEY` |
| z.ai / GLM | `zai` | `GLM_API_KEY` |
| Kimi / Moonshot | `kimi-coding` | `KIMI_API_KEY` |
| MiniMax | `minimax` | `MINIMAX_API_KEY` |
| MiniMax (China) | `minimax-cn` | `MINIMAX_CN_API_KEY` |
| DeepSeek | `deepseek` | `DEEPSEEK_API_KEY` |
| OpenCode Zen | `opencode-zen` | `OPENCODE_ZEN_API_KEY` |
| OpenCode Go | `opencode-go` | `OPENCODE_GO_API_KEY` |
| Kilo Code | `kilocode` | `KILOCODE_API_KEY` |
| Alibaba / DashScope | `alibaba` | `DASHSCOPE_API_KEY` |
| Hugging Face | `huggingface` | `HF_TOKEN` |
| 自定义端点 | `custom` | `base_url` + `api_key_env` |

### 触发条件

- **速率限制** (HTTP 429) — 重试耗尽后
- **服务器错误** (HTTP 500, 502, 503) — 重试耗尽后
- **认证失败** (HTTP 401, 403) — 立即
- **未找到** (HTTP 404) — 立即
- **无效响应** — API 返回格式错误或空响应时

### 示例

```yaml
# Anthropic 原生为主，OpenRouter 为回退
model:
  provider: anthropic
  default: claude-sonnet-4.6
fallback_model:
  provider: openrouter
  model: anthropic/claude-sonnet-4

# Nous Portal 为回退
model:
  provider: openrouter
  default: anthropic/claude-opus-4
fallback_model:
  provider: nous
  model: nous-hermes-3
```

## 辅助任务回退

Hermes 对辅助任务使用独立的轻量级模型。每个任务有自己的提供商解析链：

| 任务 | 配置键 |
|------|--------|
| Vision | `auxiliary.vision` |
| Web Extract | `auxiliary.web_extract` |
| Compression | `auxiliary.compression` |
| Session Search | `auxiliary.session_search` |
| Skills Hub | `auxiliary.skills_hub` |
| MCP | `auxiliary.mcp` |
| Memory Flush | `auxiliary.flush_memories` |

### 自动检测链

文本任务：`OpenRouter → Nous Portal → 自定义端点 → Codex OAuth → 其他`

视觉任务：`主提供商（如果支持视觉）→ OpenRouter → Nous Portal → Codex OAuth → Anthropic`

## 摘要

| 功能 | 回退机制 | 配置位置 |
|------|----------|----------|
| 主代理模型 | `fallback_model` — 一次性故障转移 | `config.yaml` |
| Vision | 自动检测链 + 内部 OpenRouter 重试 | `auxiliary.vision` |
| Web extraction | 自动检测链 | `auxiliary.web_extract` |
| Context compression | 自动检测链 | `auxiliary.compression` |
| 委托 | 仅提供商覆盖（无自动回退） | `delegation.provider` |
| Cron jobs | 每作业提供商覆盖（无自动回退） | 每作业 `provider`/`model` |
