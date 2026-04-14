# Learning Path

根据你的经验和目标，找到最佳学习路径。

## 按经验级别

| 级别 | 目标 | 推荐阅读顺序 | 时间 |
|------|------|--------------|------|
| **初级** | 安装运行、基本对话、使用内置工具 | 安装 → Quickstart → CLI → 配置 | ~1小时 |
| **中级** | 设置消息 Bot、高级功能（记忆、cron、技能） | Sessions → Messaging → Tools → Skills → Memory → Cron | ~2-3小时 |
| **高级** | 自定义工具、创建技能、RL训练、贡献代码 | Architecture → Adding Tools → Creating Skills → RL Training → Contributing | ~4-6小时 |

## 按使用场景

### "我想要 CLI 编程助手"
1. Installation
2. Quickstart
3. CLI Usage
4. Code Execution
5. Context Files
6. Tips & Tricks

### "我想要 Telegram/Discord Bot"
1. Installation
2. Configuration
3. Messaging Overview
4. Telegram Setup
5. Discord Setup
6. Voice Mode
7. Use Voice Mode with Hermes
8. Security

示例项目：
- [Daily Briefing Bot](hermes-日报Bot.md)
- [Team Telegram Assistant](hermes-团队助手.md)

### "我想要自动化任务"
1. Quickstart
2. Cron Scheduling
3. Batch Processing
4. Delegation
5. Hooks

### "我想要构建自定义工具/技能"
1. Tools Overview
2. Skills Overview
3. MCP (Model Context Protocol)
4. Architecture
5. Adding Tools
6. Creating Skills

### "我想要训练模型"
1. Quickstart
2. Configuration
3. RL Training
4. Provider Routing
5. Architecture

### "我想作为 Python 库使用"
1. Installation
2. Quickstart
3. [Python Library Guide](hermes-Python库.md)
4. Architecture
5. Tools
6. Sessions

## 核心功能一览

| 功能 | 说明 | 链接 |
|------|------|------|
| **Tools** | 内置工具（文件、网络、终端等） | Tools |
| **Skills** | 可安装的插件包 | Skills |
| **Memory** | 跨会话持久记忆 | Memory |
| **Context Files** | 向对话注入文件 | Context Files |
| **MCP** | 通过 Model Context Protocol 连接外部工具 | MCP |
| **Cron** | 定时任务调度 | Cron |
| **Delegation** | 生成子代理并行工作 | Delegation |
| **Code Execution** | 沙箱环境执行代码 | Code Execution |
| **Browser** | 网页浏览和抓取 | Browser |
| **RL Training** | 强化学习微调 | RL Training |
