# Slash 命令参考

## 概述

在 Hermes CLI 中输入 `/` 查看自动补全菜单。

## 内置命令

### 会话管理

| 命令 | 说明 |
|------|------|
| `/help` | 显示帮助 |
| `/title <name>` | 命名当前会话 |
| `/compress` | 压缩对话历史 |
| `/usage` | 显示 token 使用情况 |
| `/verbose` | 切换详细输出 |

### 模型控制

| 命令 | 说明 |
|------|------|
| `/model` | 显示/切换模型 |
| `/reasoning` | 推理努力级别 |

### 语音

| 命令 | 说明 |
|------|------|
| `/voice` | 切换语音模式 |
| `/voice on` | 启用语音 |
| `/voice off` | 禁用语音 |
| `/voice tts` | 启用 TTS |
| `/status` | 查看状态 |

### 工具与技能

| 命令 | 说明 |
|------|------|
| `/tools` | 列出可用工具 |
| `/skill <name>` | 加载技能 |
| `/skills browse` | 浏览技能目录 |

### 文件与目录

| 命令 | 说明 |
|------|------|
| `/cd <path>` | 更改工作目录 |
| `/pwd` | 显示当前目录 |

### 人格

| 命令 | 说明 |
|------|------|
| `/personality pirate` | 切换人格预设 |
| `/skin` | 显示/切换皮肤 |

### 其他

| 命令 | 说明 |
|------|------|
| `/yolo` | 切换 YOLO 模式 |
| `/background <prompt>` | 后台任务 |
| `/reload-mcp` | 重新加载 MCP |

## 预置人格

- `helpful` - helpful
- `concise` - 简洁
- `technical` - 技术
- `creative` - 创意
- `teacher` - 教师
- `kawaii` - 可爱
- `catgirl` - 猫娘
- `pirate` - 海盗
- `shakespeare` - 莎士比亚
- `surfer` - 冲浪者
- `noir` - 黑色电影
- `uwu` - UwU
- `philosopher` - 哲学家
- `hype` - 嗨

## 技能命令

每个已安装的技能自动成为 slash 命令：
```
/gif-search funny cats
/github-pr-workflow create a PR
```

## 快速命令

在 `config.yaml` 中定义：
```yaml
quick_commands:
  status:
    type: exec
    command: systemctl status hermes-agent
```

使用 `/status` 执行。

## MCP 命令

| 命令 | 说明 |
|------|------|
| `/reload-mcp` | 重新加载 MCP 服务器 |
| `/mcp <server> <tool>` | 直接调用 MCP 工具 |

## 自定义命令

### 外部命令
```yaml
quick_commands:
  deploy:
    type: exec
    command: ./scripts/deploy.sh
```

### 消息发送
```yaml
quick_commands:
  notify-team:
    type: message
    platform: telegram
    message: "Deployment complete!"
```
