# Android/Termux 安装

在 Android 手机上通过 Termux 运行 Hermes Agent。

## 支持的功能

✅ Hermes CLI
✅ Cron 支持
✅ PTY/后台终端支持
✅ MCP 支持
✅ Honcho 记忆支持
✅ ACP 支持

❌ `.[all]` 完整安装
❌ Voice（`faster-whisper` 不支持 Android）
❌ 自动浏览器引导
❌ Docker 隔离

## 安装方式

### 方式一：一键安装（推荐）
```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

安装器会自动：
- 使用 `pkg` 安装系统包
- 用 `python -m venv` 创建虚拟环境
- 安装 `.[termux]`
- 链接 `hermes` 到 `$PREFIX/bin`

### 方式二：手动安装

**1. 更新 Termux 并安装系统包**
```bash
pkg update
pkg install -y git python clang rust make pkg-config libffi openssl nodejs ripgrep ffmpeg
```

**2. 克隆 Hermes**
```bash
git clone --recurse-submodules https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
```

**3. 创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate
export ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"
python -m pip install --upgrade pip setuptools wheel
```

**4. 安装 Termux 捆绑包**
```bash
python -m pip install -e '.[termux]' -c constraints-termux.txt
```

**5. 链接到 PATH**
```bash
ln -sf "$PWD/venv/bin/hermes" "$PREFIX/bin/hermes"
```

**6. 验证**
```bash
hermes version
hermes doctor
```

## 故障排除

### `uv pip install` 失败
使用 stdlib venv + pip：
```bash
python -m venv venv
source venv/bin/activate
export ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"
python -m pip install -e '.[termux]' -c constraints-termux.txt
```

### `jiter`/`maturin` 报错
设置 API 级别：
```bash
export ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"
python -m pip install -e '.[termux]' -c constraints-termux.txt
```

### 缺少 ripgrep 或 Node
```bash
pkg install ripgrep nodejs
```

### 构建失败
安装构建工具链：
```bash
pkg install clang rust make pkg-config libffi openssl
```
