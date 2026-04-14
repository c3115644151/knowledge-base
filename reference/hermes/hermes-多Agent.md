# Profiles (多 Agent 配置)

## 概述

Profiles 允许在同一台机器上运行多个完全独立的 Hermes Agent，每个有自己独立的配置、API 密钥、记忆、会话、技能和网关。

## 快速开始

```bash
hermes profile create coder
coder setup
coder chat
```

`coder` 现在是一个完全独立的 Agent。

## 创建 Profile

### 空 Profile
```bash
hermes profile create mybot
```

### 克隆配置 (不含记忆)
```bash
hermes profile create work --clone
```

### 克隆全部 (含记忆)
```bash
hermes profile create backup --clone-all
```

### 从指定 Profile 克隆
```bash
hermes profile create work --clone --clone-from coder
```

## 使用 Profile

### 命令别名
每个 Profile 自动获得命令别名：
```bash
coder chat
coder setup
coder gateway start
coder doctor
coder skills list
coder config set model.model anthropic/claude-sonnet-4
```

### -p 标志
```bash
hermes -p coder chat
hermes chat -p coder -q "hello"
```

### 设为默认
```bash
hermes profile use coder
hermes chat  # 现在指向 coder
hermes profile use default
```

## Profile 目录结构

```
~/.hermes/
├── config.yaml           # 默认 Profile
├── .env
├── profiles/
│   └── coder/
│       ├── config.yaml   # coder 的配置
│       ├── .env          # coder 的密钥
│       ├── SOUL.md       # coder 的人格
│       ├── memories/
│       ├── sessions/
│       ├── skills/
│       └── ...
```

## 运行多个网关

每个 Profile 运行独立的网关进程：

```bash
coder gateway start
assistant gateway start
```

### 安全：Token 锁
同一 Token 只能被一个 Profile 使用，第二个会被阻止。

### 持久化服务
```bash
coder gateway install     # 创建 systemd/launchd 服务
assistant gateway install
```

## Profile 管理

```bash
hermes profile list
hermes profile show coder
hermes profile rename coder dev-bot
hermes profile export coder ./coder.tar.gz
hermes profile import ./coder.tar.gz
hermes profile delete coder
```

## 更新

`hermes update` 一次更新代码，自动同步新技能到所有 Profile：

```
→ Code updated (12 commits)
→ Skills synced: default (up to date), coder (+2 new), assistant (+2 new)
```

## 与 HERMES_HOME 的区别

Profile 是 `HERMES_HOME` 的管理包装。可以手动设置 `HERMES_HOME`，但 Profile 自动处理：
- 创建目录结构
- 生成 shell 别名
- 跟踪活动 Profile
- 同步技能更新

## Tab 补全

```bash
# Bash
eval "$(hermes completion bash)"

# Zsh
eval "$(hermes completion zsh)"
```

## Honcho 与 Profiles

启用 Honcho 时，`--clone` 自动为新 Profile 创建专用 AI peer。
