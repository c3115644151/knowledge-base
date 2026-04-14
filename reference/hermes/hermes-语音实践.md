# 语音模式实践

语音模式使用指南。

## 三种语音体验

| 模式 | 适用场景 | 平台 |
|------|----------|------|
| **交互式麦克风** | 个人免手操作 | CLI |
| **语音回复** | 消息聊天中语音回复 | Telegram、Discord |
| **语音频道 Bot** | 实时语音对话 | Discord 语音频道 |

## 最佳路径

1. 先让文字模式工作
2. 启用语音回复
3. 最后（可选）Discord 语音频道

## 安装依赖

### CLI 麦克风 + 播放
```bash
pip install "hermes-agent[voice]"
```

### 消息平台
```bash
pip install "hermes-agent[messaging]"
```

### 本地 NeuTTS（可选）
```bash
pip install -U neutts[all]
```

### 系统依赖

**macOS**：
```bash
brew install portaudio ffmpeg opus espeak-ng
```

**Ubuntu/Debian**：
```bash
sudo apt install portaudio19-dev ffmpeg libopus0 espeak-ng
```

## 选择 STT 和 TTS 提供商

### 最简/最便宜配置

| 组件 | 提供商 | 说明 |
|------|--------|------|
| **STT** | `local` | 本地（需 faster-whisper） |
| **TTS** | `edge` | 免费 Edge TTS |

### 安装本地 STT
```bash
pip install faster-whisper
```

## 配置

### CLI 语音

```bash
# ~/.hermes/.env
VOICE_STT_PROVIDER=local
VOICE_TTS_PROVIDER=edge
```

启动 Hermes 后启用：
```bash
/voice on
```

按 `Ctrl+B` 录音，`/voice tts` 让 Hermes 说话。

### 消息平台语音

```bash
pip install "hermes-agent[messaging]"
```

在消息平台中：
- 发送语音消息 → 自动转录并处理
- TTS 回复 → 自动生成语音消息

## Discord 语音频道

### 1. 安装依赖
```bash
pip install "hermes-agent[discord-voice]"
sudo apt install ffmpeg libopus0
```

### 2. 配置

```bash
# ~/.hermes/.env
DISCORD_BOT_TOKEN=xxx
DISCORD_VOICE_ENABLED=true
VOICE_TTS_PROVIDER=edge
```

### 3. 使用

加入 Discord 语音频道，发送消息 `@Bot join` 让 Bot 加入语音频道。

## TTS 提供商

| 提供商 | 费用 | 质量 |
|--------|------|------|
| `edge` | 免费 | 良好 |
| `elevenlabs` | 付费 | 最佳 |
| `openai` | 付费 | 优秀 |
| `minimax` | 付费 | 良好 |
| `neutts` | 免费 | 基础 |

## 配置 TTS
```bash
# ~/.hermes/.env
VOICE_TTS_PROVIDER=edge

# ElevenLabs
ELEVENLABS_API_KEY=xxx
VOICE_TTS_VOICE=xxx

# OpenAI
OPENAI_API_KEY=xxx

# MiniMax
MINIMAX_API_KEY=xxx
```

## 快捷命令

| 命令 | 说明 |
|------|------|
| `/voice on` | 启用语音输入 |
| `/voice off` | 禁用语音输入 |
| `/voice tts` | 切换 TTS 回复 |
| `/voice status` | 显示语音状态 |
