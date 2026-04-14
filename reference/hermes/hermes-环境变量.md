# 环境变量参考

所有变量放在 `~/.hermes/.env`，或使用 `hermes config set VAR value` 设置。

## LLM 提供商

| 变量 | 描述 |
|------|------|
| `OPENROUTER_API_KEY` | OpenRouter API 密钥（推荐） |
| `OPENROUTER_BASE_URL` | 覆盖 OpenRouter 兼容基础 URL |
| `AI_GATEWAY_API_KEY` | Vercel AI Gateway API 密钥 |
| `AI_GATEWAY_BASE_URL` | 覆盖 AI Gateway 基础 URL |
| `OPENAI_API_KEY` | 自定义 OpenAI 兼容端点的 API 密钥 |
| `OPENAI_BASE_URL` | 自定义端点基础 URL |
| `COPILOT_GITHUB_TOKEN` | GitHub token — 第一优先级 |
| `GH_TOKEN` | GitHub token — 第二优先级 |
| `GITHUB_TOKEN` | GitHub token — 第三优先级 |
| `GLM_API_KEY` | z.ai / ZhipuAI GLM API 密钥 |
| `KIMI_API_KEY` | Kimi / Moonshot AI API 密钥 |
| `MINIMAX_API_KEY` | MiniMax API 密钥 — 全球端点 |
| `MINIMAX_CN_API_KEY` | MiniMax API 密钥 — 中国端点 |
| `KILOCODE_API_KEY` | Kilo Code API 密钥 |
| `HF_TOKEN` | Hugging Face token |
| `GOOGLE_API_KEY` | Google AI Studio API 密钥 |
| `ANTHROPIC_API_KEY` | Anthropic Console API 密钥 |
| `DASHSCOPE_API_KEY` | Alibaba Cloud DashScope API 密钥 |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 |
| `OPENCODE_ZEN_API_KEY` | OpenCode Zen API 密钥 |
| `OPENCODE_GO_API_KEY` | OpenCode Go API 密钥 |
| `CLAUDE_CODE_OAUTH_TOKEN` | 显式 Claude Code token 覆盖 |
| `HERMES_MODEL` | 首选模型名（gateway 使用） |
| `LLM_MODEL` | 默认模型名 |

## 提供商 Auth (OAuth)

| 变量 | 描述 |
|------|------|
| `HERMES_INFERENCE_PROVIDER` | 覆盖提供商选择：`auto`, `openrouter`, `nous`, `openai-codex`, `copilot`, `copilot-acp`, `anthropic`, `huggingface`, `zai`, `kimi-coding`, `minimax`, `minimax-cn`, `kilocode`, `alibaba`, `deepseek`, `opencode-zen`, `opencode-go`, `ai-gateway` |
| `HERMES_PORTAL_BASE_URL` | 覆盖 Nous Portal URL |
| `HERMES_TIMEZONE` | IANA 时区覆盖 |

## 工具 API

| 变量 | 描述 |
|------|------|
| `PARALLEL_API_KEY` | AI 原生网页搜索 |
| `FIRECRAWL_API_KEY` | 网页抓取和云浏览器 |
| `TAVILY_API_KEY` | Tavily API 密钥 |
| `EXA_API_KEY` | Exa API 密钥 |
| `BROWSERBASE_API_KEY` | Browser automation |
| `BROWSERBASE_PROJECT_ID` | Browserbase 项目 ID |
| `BROWSER_USE_API_KEY` | Browser Use 云浏览器 API 密钥 |
| `BROWSER_CDP_URL` | Chrome DevTools Protocol URL（通过 `/browser connect` 设置） |
| `FAL_KEY` | 图像生成 |
| `GROQ_API_KEY` | Groq Whisper STT API 密钥 |
| `ELEVENLABS_API_KEY` | ElevenLabs 高级 TTS 语音 |
| `HONCHO_API_KEY` | 跨会话用户建模 |
| `SUPERMEMORY_API_KEY` | 语义长期记忆 |
| `TINKER_API_KEY` | RL 训练 |
| `WANDB_API_KEY` | RL 训练指标 |
| `DAYTONA_API_KEY` | Daytona 云沙箱 |

## 终端后端

| 变量 | 默认 | 描述 |
|------|------|------|
| `TERMINAL_ENV` | `local` | 后端：`local`, `docker`, `ssh`, `singularity`, `modal`, `daytona` |
| `TERMINAL_DOCKER_IMAGE` | `nikolaik/python-nodejs:...` | Docker 镜像 |
| `TERMINAL_TIMEOUT` | — | 命令超时（秒） |
| `TERMINAL_LIFETIME_SECONDS` | — | 终端会话最大生命周期 |
| `TERMINAL_CWD` | — | 所有终端会话的工作目录 |
| `SUDO_PASSWORD` | — | 启用 sudo |

## 容器资源

| 变量 | 默认 | 描述 |
|------|------|------|
| `TERMINAL_CONTAINER_CPU` | `1` | CPU 核心数 |
| `TERMINAL_CONTAINER_MEMORY` | `5120` | 内存（MB） |
| `TERMINAL_CONTAINER_DISK` | `51200` | 磁盘（MB） |

## 持久 Shell

| 变量 | 默认 | 描述 |
|------|------|------|
| `TERMINAL_PERSISTENT_SHELL` | `true` | 非本地后端启用持久 shell |
| `TERMINAL_LOCAL_PERSISTENT` | `false` | 本地后端启用持久 shell |

## 消息平台

| 变量 | 描述 |
|------|------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token |
| `DISCORD_BOT_TOKEN` | Discord bot token |
| `SLACK_BOT_TOKEN` | Slack bot token |
| `WHATSAPP_ENABLED` | 启用 WhatsApp (`true`/`false`) |
| `SIGNAL_HTTP_URL` | signal-cli daemon HTTP 端点 |
| `FEISHU_APP_ID` | Feishu/Lark bot App ID |
| `FEISHU_APP_SECRET` | Feishu/Lark bot App Secret |
| `WECOM_BOT_ID` | WeCom AI Bot ID |
| `MATRIX_HOMESERVER` | Matrix homeserver URL |
| `MATRIX_ACCESS_TOKEN` | Matrix 访问令牌 |
| `HASS_TOKEN` | Home Assistant 长期访问令牌 |

## API 服务器

| 变量 | 默认 | 描述 |
|------|------|------|
| `API_SERVER_ENABLED` | `false` | 启用 API 服务器 |
| `API_SERVER_KEY` | — | Bearer token 认证 |
| `API_SERVER_PORT` | `8642` | HTTP 服务器端口 |
| `API_SERVER_HOST` | `127.0.0.1` | 绑定地址 |
| `API_SERVER_CORS_ORIGINS` | — | 逗号分隔允许的浏览器来源 |

## 代理行为

| 变量 | 默认 | 描述 |
|------|------|------|
| `HERMES_MAX_ITERATIONS` | `90` | 每对话最大工具调用迭代 |
| `HERMES_QUIET` | `false` | 抑制非必要输出 |
| `HERMES_API_TIMEOUT` | `1800` | LLM API 调用超时（秒） |
| `HERMES_ENABLE_PROJECT_PLUGINS` | `false` | 启用 repo 本地插件发现 |

## 会话设置

| 变量 | 默认 | 描述 |
|------|------|------|
| `SESSION_IDLE_MINUTES` | `1440` | 不活动后重置会话 |
| `SESSION_RESET_HOUR` | `4` | 每日重置小时（24h 格式） |

## 辅助任务覆盖

| 变量 | 描述 |
|------|------|
| `AUXILIARY_VISION_PROVIDER` | 视觉任务提供商覆盖 |
| `AUXILIARY_VISION_MODEL` | 视觉任务模型覆盖 |
| `AUXILIARY_WEB_EXTRACT_PROVIDER` | 网页提取提供商覆盖 |
| `AUXILIARY_WEB_EXTRACT_MODEL` | 网页提取模型覆盖 |

## 提供商路由（config.yaml）

通过 `~/.hermes/config.yaml` 的 `provider_routing` 部分配置：

| 键 | 描述 |
|-----|------|
| `sort` | 排序：`"price"`（默认）、`"throughput"`、`"latency"` |
| `only` | 允许的提供商 slug 列表 |
| `ignore` | 跳过的提供商 slug 列表 |
| `order` | 尝试的提供商顺序 |
| `require_parameters` | 仅使用支持所有参数的提供商 |
| `data_collection` | `"allow"`（默认）或 `"deny"` |
