# 视觉与图像粘贴

Hermes Agent 支持**多模态视觉**——可将剪贴板中的图像直接粘贴到 CLI，让代理分析、描述或处理图像。

## 工作方式

1. 将图像复制到剪贴板（截图、浏览器图像等）
2. 使用下方方法附加
3. 输入问题并按 Enter
4. 图像显示为 `[📎 Image #1]` 徽章
5. 提交后，图像作为视觉内容块发送给模型

## 粘贴方法

### `/paste` 命令

**最可靠的方法，适用于所有环境。**

```bash
/paste
```

### Ctrl+V / Cmd+V（括号粘贴）

当剪贴板同时包含文本和图像时自动检测。

### Alt+V

大多数终端模拟器会通过 Alt 键组合。在 VSCode 集成终端中**不适用**。

### Ctrl+V（Linux 原始模式，仅 Linux）

在 Linux 桌面终端（GNOME Terminal、Konsole、Alacritty 等），`Ctrl+V` 不是粘贴快捷键，所以 Hermes 捕获它来检查剪贴板。

## 平台兼容性

| 环境 | /paste | Ctrl+V text+image | Alt+V |
|------|--------|-------------------|-------|
| macOS Terminal / iTerm2 | ✅ | ✅ | ✅ |
| Linux X11 desktop | ✅ | ✅ | ✅ |
| Linux Wayland desktop | ✅ | ✅ | ✅ |
| WSL2 (Windows Terminal) | ✅ | ✅ | ✅ |
| VSCode Terminal (local) | ✅ | ✅ | ❌ |
| SSH 终端 | ❌ | ❌ | ❌ |

## 平台设置

### macOS

无需设置。使用 `osascript` 读取剪贴板。可选安装 `pngpaste` 以提高性能。

### Linux (X11)

```bash
# Ubuntu/Debian
sudo apt install xclip
# Fedora
sudo dnf install xclip
```

### Linux (Wayland)

```bash
# Ubuntu/Debian
sudo apt install wl-clipboard
# Fedora
sudo dnf install wl-clipboard
```

### WSL2

无需额外设置。自动检测并使用 `powershell.exe` 访问 Windows 剪贴板。

## SSH 和远程会话

**SSH 环境下剪贴板粘贴不可用。** 剪贴板工具在远程服务器上运行，无法访问本地剪贴板。

### 替代方案

1. **上传图像文件** — 本地保存，通过 scp 或 VSCode 上传到远程
2. **使用 URL** — 如果图像可在线访问，直接粘贴 URL
3. **X11 转发** — `ssh -X`，但大图像传输慢
4. **使用消息平台** — 通过 Telegram、Discord 等发送图像

## 支持的模型

图像粘贴适用于任何支持视觉的模型。图像以 base64 编码的数据 URL 发送：

```json
{
  "type": "image_url",
  "image_url": {"url": "data:image/png;base64,..."}
}
```
