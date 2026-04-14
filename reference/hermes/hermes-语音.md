# 语音模式 (Voice Mode)

## 概述

Hermes Agent 支持跨 CLI 和消息平台的完整语音交互。

## 功能概览

| 功能 | 平台 | 说明 |
|------|------|------|
| 交互式语音 | CLI | 按 Ctrl+B 录音，检测静音后自动响应 |
| 自动语音回复 | Telegram, Discord | Agent 回复转为语音发送 |
| 语音频道 | Discord | Bot 加入语音频道，实时对话 |

## 安装依赖

```bash
# CLI 语音模式
pip install "hermes-agent[voice]"

# 消息平台
pip install "hermes-agent[messaging]"

# 高级 TTS
pip install "hermes-agent[tts-premium]"

# 本地 TTS (可选)
python -m pip install -U neutts[all]

# 完整安装
pip install "hermes-agent[all]"
```

### 系统依赖

```bash
# macOS
brew install portaudio ffmpeg opus
brew install espeak-ng  # NeuTTS

# Ubuntu/Debian
sudo apt install portaudio19-dev ffmpeg libopus0
sudo apt install espeak-ng  # NeuTTS
```

## CLI 语音模式

### 启用
```bash
hermes
/voice on
```

### 使用
1. 按 **Ctrl+B** 开始录音 (听到提示音)
2. 说话
3. 3 秒静音后自动停止 (听到双提示音)
4. Agent 处理并回复
5. 如果 TTS 启用，自动朗读回复
6. 录音自动重新开始

### 配置
```yaml
# ~/.hermes/config.yaml
voice:
  record_key: "ctrl+b"           # 录音键
  max_recording_seconds: 120      # 最大录音时长
  auto_tts: false                # 语音模式启动时自动启用 TTS
  silence_threshold: 200          # 静音阈值 (0-32767)
  silence_duration: 3.0           # 静音检测时长
```

## TTS 配置

### STT 提供商

| 提供商 | 模型 | 速度 | 质量 | 成本 | API 密钥 |
|--------|------|------|------|------|----------|
| **本地** | base/small/large-v3 | 取决于 CPU/GPU | 好~最好 | 免费 | 无 |
| **Groq** | whisper-large-v3-turbo | 极快 (~0.5s) | 好 | 免费 | 需要 |
| **OpenAI** | whisper-1 | 快 (~1s) | 好 | 付费 | 需要 |

### TTS 提供商

| 提供商 | 质量 | 成本 | 延迟 | API 密钥 |
|--------|------|------|------|----------|
| **Edge TTS** | 好 | 免费 | ~1s | 无 |
| **ElevenLabs** | 优秀 | 付费 | ~2s | 需要 |
| **OpenAI TTS** | 好 | 付费 | ~1.5s | 需要 |
| **NeuTTS** | 好 | 免费 | 取决于 CPU | 无 |

### 配置示例

```yaml
# ~/.hermes/config.yaml
stt:
  provider: "local"    # local | groq | openai
  local:
    model: "base"

tts:
  provider: "edge"    # edge | elevenlabs | openai | neutts | minimax
  edge:
    voice: "en-US-AriaNeural"    # 322 种声音，74 种语言
  elevenlabs:
    voice_id: "pNInz6obpgDQGcFmaJgB"    # Adam
    model_id: "eleven_multilingual_v2"
```

## Discord 语音频道

### 设置

1. **添加权限** - Discord Developer Portal 添加 Connect, Speak, Use Voice Activity
2. **启用 Intent** - Presence, Server Members, Message Content
3. **安装 Opus** - `libopus0`
4. **配置环境变量**

```bash
# ~/.hermes/.env
DISCORD_BOT_TOKEN=your-bot-token
DISCORD_ALLOWED_USERS=your-user-id
```

### 命令
```
/voice join      # Bot 加入你的语音频道
/voice channel   # 同 /voice join
/voice leave     # Bot 离开
/voice status    # 查看状态
```

### 工作原理
1. Bot 监听各用户的音频流
2. 1.5 秒静音后触发处理 (至少 0.5 秒语音)
3. Whisper 转录
4. Agent 处理
5. TTS 回复并在语音频道播放
6. 播放时自动暂停监听 (防回音)

## 命令参考

| 命令 | 说明 |
|------|------|
| `/voice` | 切换语音模式 |
| `/voice on` | 启用语音模式 |
| `/voice off` | 禁用语音模式 |
| `/voice tts` | TTS 回复 |
| `/voice status` | 查看状态 |

## 环境变量

```bash
# ~/.hermes/.env

# STT
GROQ_API_KEY=...           # Groq Whisper
VOICE_TOOLS_OPENAI_KEY=... # OpenAI Whisper

# TTS
ELEVENLABS_API_KEY=***     # ElevenLabs
# VOICE_TOOLS_OPENAI_KEY above also enables OpenAI TTS
```
