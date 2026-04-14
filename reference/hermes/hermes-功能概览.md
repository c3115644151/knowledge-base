# 功能概览

Hermes Agent 的核心能力和功能一览。

## 核心功能

| 功能 | 说明 |
|------|------|
| **Tools & Toolsets** | 扩展代理能力的函数，按逻辑分组，可按平台启用/禁用 |
| **Skills System** | 按需加载的知识文档，最小化 token 使用的渐进式披露 |
| **Persistent Memory** | 跨会话持久记忆，通过 MEMORY.md 和 USER.md |
| **Context Files** | 自动发现 .hermes.md、AGENTS.md、CLAUDE.md 等项目上下文文件 |
| **Context References** | 输入 `@` 引用文件、文件夹、git diff 和 URL |
| **Checkpoints** | 文件修改前自动快照，支持 `/rollback` 回滚 |

## 自动化

| 功能 | 说明 |
|------|------|
| **Cron 调度** | 自然语言或 cron 表达式定时任务 |
| **Subagent Delegation** | 生成子代理并行工作，最多 3 个并发 |
| **Code Execution** | 沙箱 RPC 执行，将多步工作流压缩为单次 LLM 调用 |
| **Event Hooks** | 生命周期关键点的自定义代码 |
| **Batch Processing** | 并行处理大量提示，生成 ShareGPT 格式训练数据 |

## 媒体与 Web

| 功能 | 说明 |
|------|------|
| **Voice Mode** | CLI 和消息平台的语音交互 |
| **Browser Automation** | 多后端浏览器自动化（Browserbase、Browser Use、本地 Chrome） |
| **Vision & Image Paste** | 多模态视觉支持 |
| **Image Generation** | FAL.ai FLUX 2 Pro 图像生成 |
| **TTS** | 文本转语音，5 种提供商可选（Edge TTS、ElevenLabs、OpenAI TTS 等） |

## 集成

| 功能 | 说明 |
|------|------|
| **MCP Integration** | 通过 stdio 或 HTTP 连接 MCP 服务器 |
| **Provider Routing** | 多 LLM provider 精细路由控制 |
| **Fallback Providers** | 主 provider 失败时自动切换 |
| **Credential Pools** | 同一 provider 跨多密钥分发 API 调用 |
| **Memory Providers** | 外置记忆后端（Honcho、Mem0、Hindsight 等） |
| **API Server** | OpenAI 兼容 HTTP 端点 |
| **IDE Integration (ACP)** | VS Code、Zed、JetBrains 中的代理 |
| **RL Training** | 生成轨迹数据用于强化学习 |

## 自定义

| 功能 | 说明 |
|------|------|
| **Personality & SOUL.md** | 完全可定制的代理个性 |
| **Skins & Themes** | CLI 视觉定制（颜色、标签、品牌文字） |
| **Plugins** | 添加自定义工具、钩子和集成 |
