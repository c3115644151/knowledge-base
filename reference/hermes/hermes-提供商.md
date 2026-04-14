# AI 提供商参考

## 支持的提供商

| 提供商 | 环境变量 | 配置方式 |
|--------|----------|----------|
| **Nous Portal** | OAuth | `hermes model` |
| **OpenAI Codex** | OAuth | `hermes model` |
| **Anthropic** | `ANTHROPIC_API_KEY` | `hermes model` |
| **OpenRouter** | `OPENROUTER_API_KEY` | 直接设置 |
| **AI Gateway** | `AI_GATEWAY_API_KEY` | 直接设置 |
| **GitHub Copilot** | `COPILOT_GITHUB_TOKEN` | `hermes model` |
| **GitHub Copilot ACP** | 外部进程 | 编辑器集成 |
| **z.ai / GLM** | `GLM_API_KEY` | 直接设置 |
| **Kimi / Moonshot** | `KIMI_API_KEY` | 直接设置 |
| **MiniMax** | `MINIMAX_API_KEY` | 直接设置 |
| **MiniMax (China)** | `MINIMAX_CN_API_KEY` | 直接设置 |
| **DeepSeek** | `DEEPSEEK_API_KEY` | 直接设置 |
| **Hugging Face** | `HF_TOKEN` | 直接设置 |
| **Google/Gemini** | `GOOGLE_API_KEY` | 直接设置 |
| **Alibaba / DashScope** | `DASHSCOPE_API_KEY` | 直接设置 |
| **Kilo Code** | `KILOCODE_API_KEY` | 直接设置 |
| **OpenCode Zen** | `OPENCODE_ZEN_API_KEY` | 直接设置 |
| **OpenCode Go** | `OPENCODE_GO_API_KEY` | 直接设置 |
| **自定义端点** | — | `hermes model` |

## Anthropic (Claude 原生)

```bash
# API 密钥
export ANTHROPIC_API_KEY=sk-ant-xxx

# OAuth (推荐)
hermes model  # 选择 Anthropic
```

## OpenRouter

```bash
# ~/.hermes/.env
OPENROUTER_API_KEY=sk-or-v1-xxx
```

```yaml
# ~/.hermes/config.yaml
model:
  provider: openrouter
  default: anthropic/claude-sonnet-4
```

## AI Gateway (Vercel)

```bash
# ~/.hermes/.env
AI_GATEWAY_API_KEY=xxx
```

```yaml
model:
  provider: ai-gateway
  default: anthropic/claude-sonnet-4.6
```

## Nous Portal

```bash
hermes model  # 选择 Nous Portal → OAuth 登录
```

## OpenAI Codex

```bash
hermes model  # 选择 Codex → OAuth 登录
```

## GitHub Copilot

```bash
# OAuth (推荐)
hermes model  # 选择 Copilot → OAuth 登录

# 或使用 token
hermes model  # 选择 Copilot
```

Token 优先级：`COPILOT_GITHUB_TOKEN` > `GH_TOKEN` > `GITHUB_TOKEN`

## GitHub Copilot ACP

编辑器集成模式，通过外部进程通信：

```bash
# 安装
pip install -e '.[acp]'

# 启动
hermes acp
```

## z.ai / GLM

```bash
# ~/.hermes/.env
GLM_API_KEY=xxx
ZAI_API_KEY=xxx       # 别名
Z_AI_API_KEY=xxx      # 别名
```

```yaml
model:
  provider: zai
  default: glm-4-plus
```

## Kimi / Moonshot

```bash
# ~/.hermes/.env
KIMI_API_KEY=xxx
```

```yaml
model:
  provider: kimi-coding
  default: moonshot-v1-8k
```

## MiniMax

```bash
# ~/.hermes/.env (全球)
MINIMAX_API_KEY=xxx

# 中国端点
MINIMAX_CN_API_KEY=xxx
```

```yaml
model:
  provider: minimax          # 全球
  # provider: minimax-cn     # 中国
  default: moonshot-v1-8k
```

## DeepSeek

```bash
# ~/.hermes/.env
DEEPSEEK_API_KEY=xxx
```

```yaml
model:
  provider: deepseek
  default: deepseek-chat
```

## Hugging Face

```bash
# ~/.hermes/.env
HF_TOKEN=hf_xxx
```

```yaml
model:
  provider: huggingface
  default: meta-llama/Llama-3-70b-instruct
```

## Google / Gemini

```bash
# ~/.hermes/.env
GOOGLE_API_KEY=xxx
GEMINI_API_KEY=xxx    # 别名
```

```yaml
model:
  provider: google
  default: gemini-pro
```

## Alibaba / DashScope

```bash
# ~/.hermes/.env
DASHSCOPE_API_KEY=xxx
```

```yaml
model:
  provider: alibaba
  default: qwen-turbo
```

## Kilo Code

```bash
# ~/.hermes/.env
KILOCODE_API_KEY=xxx
```

```yaml
model:
  provider: kilocode
  default: kilocode-model
```

## OpenCode Zen

```bash
# ~/.hermes/.env
OPENCODE_ZEN_API_KEY=xxx
```

按量付费访问策划模型。

## OpenCode Go

```bash
# ~/.hermes/.env
OPENCODE_GO_API_KEY=xxx
```

$10/月订阅访问开源模型。

## 自定义端点

```bash
hermes model  # 选择 "Custom endpoint"
```

```yaml
model:
  provider: custom
  base_url: http://localhost:11434/v1
  default: llama-3.1-70b
  context_length: 32768
```

## 凭证池

多个相同提供商的 API 密钥自动轮换：

```bash
# ~/.hermes/.env
OPENROUTER_API_KEY_1=sk-or-v1-xxx1
OPENROUTER_API_KEY_2=sk-or-v1-xxx2
```

### 策略

| 策略 | 说明 |
|------|------|
| `fill_first` | 优先第一个 (默认) |
| `round_robin` | 均匀轮换 |
| `least_used` | 选择最少使用的 |
| `random` | 随机 |

```yaml
credential_pool_strategies:
  openrouter: round_robin
  anthropic: least_used
```

## 回退模型

当主模型失败时自动切换：

```yaml
fallback_model:
  provider: openrouter
  model: anthropic/claude-sonnet-4
```

### 支持的备用提供商

| 提供商 | 值 | 需求 |
|--------|-----|------|
| AI Gateway | `ai-gateway` | `AI_GATEWAY_API_KEY` |
| OpenRouter | `openrouter` | `OPENROUTER_API_KEY` |
| Nous Portal | `nous` | OAuth |
| OpenAI Codex | `openai-codex` | OAuth |
| GitHub Copilot | `copilot` | Token |
| GitHub Copilot ACP | `copilot-acp` | 外部进程 |
| Anthropic | `anthropic` | API Key |
| z.ai / GLM | `zai` | `GLM_API_KEY` |
| Kimi | `kimi-coding` | `KIMI_API_KEY` |
| MiniMax | `minimax` | `MINIMAX_API_KEY` |
| MiniMax (China) | `minimax-cn` | `MINIMAX_CN_API_KEY` |
| DeepSeek | `deepseek` | `DEEPSEEK_API_KEY` |
| OpenCode Zen | `opencode-zen` | `OPENCODE_ZEN_API_KEY` |
| OpenCode Go | `opencode-go` | `OPENCODE_GO_API_KEY` |
| Kilo Code | `kilocode` | `KILOCODE_API_KEY` |
| Alibaba / DashScope | `alibaba` | `DASHSCOPE_API_KEY` |
| Hugging Face | `huggingface` | `HF_TOKEN` |
| 自定义端点 | `custom` | `base_url` + `api_key_env` |
