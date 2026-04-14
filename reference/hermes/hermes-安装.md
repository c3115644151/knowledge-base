# 安装指南

## 快速安装

### Linux / macOS / WSL2 / Android (Termux)
```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

### 安装后
```bash
source ~/.bashrc  # 或 source ~/.zshrc
hermes            # 开始聊天!
```

## 前置要求

唯一需要的是 **Git**。安装脚本自动处理：
- `uv` (快速 Python 包管理器)
- **Python 3.11**
- **Node.js v22** (浏览器自动化和 WhatsApp)
- **ripgrep** (快速文件搜索)
- **ffmpeg** (TTS 音频转换)

## 手动安装

### 1. 克隆仓库
```bash
git clone --recurse-submodules https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
```

### 2. 安装 uv 和创建虚拟环境
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv venv --python 3.11
```

### 3. 安装依赖
```bash
export VIRTUAL_ENV="$(pwd)/venv"
uv pip install -e ".[all]"
```

### 可选依赖表

| Extra | 内容 | 安装命令 |
|-------|------|----------|
| `all` | 全部 | `uv pip install -e ".[all]"` |
| `messaging` | Telegram & Discord | `uv pip install -e ".[messaging]"` |
| `cron` | Cron 调度 | `uv pip install -e ".[cron]"` |
| `cli` | 终端菜单 UI | `uv pip install -e ".[cli]"` |
| `modal` | Modal 云后端 | `uv pip install -e ".[modal]"` |
| `voice` | CLI 麦克风 | `uv pip install -e ".[voice]"` |
| `mcp` | MCP 支持 | `uv pip install -e ".[mcp]"` |
| `honcho` | Honcho 记忆 | `uv pip install -e ".[honcho]"` |
| `slack` | Slack 消息 | `uv pip install -e ".[slack]"` |
| `homeassistant` | HA 集成 | `uv pip install -e ".[homeassistant]"` |
| `termux` | Android/Termux | `python -m pip install -e ".[termux]" -c constraints-termux.txt` |

### 4. 配置目录
```bash
mkdir -p ~/.hermes/{cron,sessions,logs,memories,skills,pairing,hooks,image_cache,audio_cache,whatsapp/session}
cp cli-config.yaml.example ~/.hermes/config.yaml
touch ~/.hermes/.env
```

### 5. 添加 API 密钥
```bash
# ~/.hermes/.env
OPENROUTER_API_KEY=sk-or-v1-your-key-here
FIRECRAWL_API_KEY=fc-your-key  # 可选
FAL_KEY=your-fal-key          # 可选
```

### 6. 添加到 PATH
```bash
mkdir -p ~/.local/bin
ln -sf "$(pwd)/venv/bin/hermes" ~/.local/bin/hermes
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 7. 验证安装
```bash
hermes version
hermes doctor
```

## Android / Termux

参见 [Termux 指南](termux.md)

## Nix / NixOS

参见 [Nix 设置指南](nix-setup.md)

## 配置 LLM 提供商

```bash
hermes model
```

支持的提供商：
- **Nous Portal** - OAuth 订阅
- **OpenAI Codex** - ChatGPT OAuth
- **Anthropic** - Claude 原生
- **OpenRouter** - 多提供商路由
- **GitHub Copilot**
- **自定义端点** - Ollama, vLLM 等

### 最小上下文
需要 **64K tokens** 以上上下文窗口的模型。

## 快速命令参考

```bash
hermes                 # 开始聊天
hermes model           # 选择 LLM 提供商
hermes tools           # 配置工具
hermes setup           # 完整设置向导
hermes doctor          # 诊断问题
hermes update          # 更新版本
hermes gateway         # 启动消息网关
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| `hermes: command not found` | 重新加载 shell (`source ~/.bashrc`) |
| API 密钥未设置 | 运行 `hermes model` 或 `hermes config set OPENROUTER_API_KEY xxx` |
| 更新后配置缺失 | 运行 `hermes config check` 然后 `hermes config migrate` |
