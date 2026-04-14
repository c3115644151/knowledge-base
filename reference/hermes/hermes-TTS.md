# 语音与 TTS

Hermes Agent 在所有消息平台上支持文本转语音输出和语音消息转录。

## 文本转语音

六种提供商：

| 提供商 | 质量 | 成本 | API 密钥 |
|--------|------|------|----------|
| **Edge TTS**（默认） | 良好 | 免费 | 无需 |
| **ElevenLabs** | 优秀 | 付费 | `ELEVENLABS_API_KEY` |
| **OpenAI TTS** | 良好 | 付费 | `VOICE_TOOLS_OPENAI_KEY` |
| **MiniMax TTS** | 优秀 | 付费 | `MINIMAX_API_KEY` |
| **Mistral (Voxtral TTS)** | 优秀 | 付费 | `MISTRAL_API_KEY` |
| **NeuTTS** | 良好 | 免费 | 无需 |

### 平台交付

| 平台 | 交付方式 | 格式 |
|------|----------|------|
| Telegram | 语音气泡（内联播放） | Opus `.ogg` |
| Discord | 语音气泡，回退到文件附件 | Opus/MP3 |
| WhatsApp | 音频文件附件 | MP3 |
| CLI | 保存到 `~/.hermes/audio_cache/` | MP3 |

### 配置

```yaml
# ~/.hermes/config.yaml
tts:
  provider: "edge"              # "edge" | "elevenlabs" | "openai" | "minimax" | "mistral" | "neutts"
  edge:
    voice: "en-US-AriaNeural"   # 322 voices, 74 languages
  elevenlabs:
    voice_id: "pNInz6obpgDQGcFmaJgB"
    model_id: "eleven_multilingual_v2"
  openai:
    model: "gpt-4o-mini-tts"
    voice: "alloy"
  minimax:
    model: "speech-2.8-hd"
    voice_id: "English_Graceful_Lady"
    speed: 1
  mistral:
    model: "voxtral-mini-tts-2603"
    voice_id: "c69964a6-ab8b-4f8a-9465-ec0925096ec8"
```

### Telegram 语音气泡与 ffmpeg

Telegram 语音气泡需要 Opus/OGG 音频格式：
- **OpenAI、ElevenLabs、Mistral** 原生输出 Opus — 无需额外设置
- **Edge TTS**（默认）输出 MP3，需要 **ffmpeg** 转换
- **MiniMax TTS** 输出 MP3，需要 **ffmpeg** 转换
- **NeuTTS** 输出 WAV，也需要 **ffmpeg** 转换

```bash
# Ubuntu/Debian
sudo apt install ffmpeg
# macOS
brew install ffmpeg
```

## 语音消息转录（STT）

Telegram、Discord、WhatsApp、Slack 或 Signal 上的语音消息自动转录并注入为文本。

| 提供商 | 质量 | 成本 | API 密钥 |
|--------|------|------|----------|
| **本地 Whisper**（默认） | 良好 | 免费 | 无需 |
| **Groq Whisper API** | 良好-最佳 | 免费额度 | `GROQ_API_KEY` |
| **OpenAI Whisper API** | 良好-最佳 | 付费 | `VOICE_TOOLS_OPENAI_KEY` 或 `OPENAI_API_KEY` |

### 配置

```yaml
stt:
  provider: "local"           # "local" | "groq" | "openai" | "mistral"
  local:
    model: "base"           # tiny, base, small, medium, large-v3
  openai:
    model: "whisper-1"
  mistral:
    model: "voxtral-mini-latest"
```

### 本地 Whisper 模型

| 模型 | 大小 | 速度 | 质量 |
|------|------|------|------|
| `tiny` | ~75 MB | 最快 | 基础 |
| `base` | ~150 MB | 快 | 良好（默认） |
| `small` | ~500 MB | 中等 | 更好 |
| `medium` | ~1.5 GB | 较慢 | 优秀 |
| `large-v3` | ~3 GB | 最慢 | 最佳 |

### 回退行为

如果配置的提供商不可用，自动回退：
- 本地 faster-whisper 不可用 → 尝试本地 whisper CLI → 云提供商
- 无可用 → 语音消息传递并附准确说明
