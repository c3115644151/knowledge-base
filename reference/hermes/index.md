# Hermes Agent 知识库

> 开源 AI Agent，MIT 许可证，支持多平台消息网关、持久记忆、技能系统、MCP 集成

**官方文档**: https://hermes-agent.nousresearch.com  
**GitHub**: https://github.com/NousResearch/hermes-agent

## 文档统计

| 分类 | 数量 |
|------|------|
| 核心概念 | 5 |
| 功能模块 | 34 |
| 消息平台 | 16 |
| 实践指南 | 6 |
| 参考文档 | 11 |
| **总计** | **72** |

## 核心概念

| 文档 | 说明 |
|------|------|
| [hermes-架构.md](hermes-架构.md) | Hermes Agent 整体架构与核心组件 |
| [hermes-工具.md](hermes-工具.md) | 工具系统设计、工具集分类 |
| [hermes-技能.md](hermes-技能.md) | 技能的定义、创建与安装 |
| [hermes-记忆.md](hermes-记忆.md) | 持久记忆、上下文文件、内存提供者 |
| [hermes-会话.md](hermes-会话.md) | 会话存储、恢复、上下文压缩 |

## 功能模块

| 文档 | 说明 |
|------|------|
| [hermes-安装.md](hermes-安装.md) | 快速安装与手动安装 |
| [hermes-配置.md](hermes-配置.md) | 完整配置项参考 |
| [hermes-MCP.md](hermes-MCP.md) | Model Context Protocol 支持 |
| [hermes-消息网关.md](hermes-消息网关.md) | 消息网关概览 |
| [hermes-语音.md](hermes-语音.md) | 语音输入输出、Discord 语音 |
| [hermes-浏览器.md](hermes-浏览器.md) | 网页浏览与自动化 |
| [hermes-委托.md](hermes-委托.md) | 子代理并行任务执行 |
| [hermes-定时任务.md](hermes-定时任务.md) | 自然语言 Cron 调度 |
| [hermes-代码执行.md](hermes-代码执行.md) | Python RPC 执行 |
| [hermes-钩子.md](hermes-钩子.md) | 生命周期钩子 |
| [hermes-多Agent.md](hermes-多Agent.md) | 运行多个独立 Agent |
| [hermes-Docker.md](hermes-Docker.md) | 容器化部署 |
| [hermes-GitWorktrees.md](hermes-GitWorktrees.md) | 并行开发隔离 |
| [hermes-ACP.md](hermes-ACP.md) | ACP 服务器、VS Code/Zed/JetBrains 集成 |
| [hermes-RL训练.md](hermes-RL训练.md) | Tinker-Atropos RL 训练管道 |
| [hermes-提供商路由.md](hermes-提供商路由.md) | OpenRouter 细粒度提供商控制 |
| [hermes-插件.md](hermes-插件.md) | 自定义工具、钩子、集成 |
| [hermes-视觉.md](hermes-视觉.md) | 图像粘贴、多模态支持 |
| [hermes-TTS.md](hermes-TTS.md) | 文本转语音、语音消息转录 |
| [hermes-回退提供商.md](hermes-回退提供商.md) | 跨提供商故障转移 |
| [hermes-凭证池.md](hermes-凭证池.md) | 多 API 密钥轮换 |
| [hermes-API服务器.md](hermes-API服务器.md) | OpenAI 兼容 HTTP 端点 |
| [hermes-Honcho.md](hermes-Honcho.md) | AI 原生跨会话用户建模 |
| [hermes-记忆提供者.md](hermes-记忆提供者.md) | 8 种外部记忆系统 |
| [hermes-人格.md](hermes-人格.md) | 代理身份与语气定制 |
| [hermes-上下文文件.md](hermes-上下文文件.md) | AGENTS.md、渐进发现 |
| [hermes-批处理.md](hermes-批处理.md) | 训练数据生成 |
| [hermes-技能.md](hermes-技能.md) | 渐进披露技能框架 |

## 消息平台

| 文档 | 说明 |
|------|------|
| [hermes-消息网关.md](hermes-消息网关.md) | 消息平台目录 |
| [hermes-Telegram.md](hermes-Telegram.md) | 即时消息 Bot |
| [hermes-Discord.md](hermes-Discord.md) | 服务器 + 语音频道 |
| [hermes-Slack.md](hermes-Slack.md) | 企业工作空间 |
| [hermes-WhatsApp.md](hermes-WhatsApp.md) | 移动端消息 |

## 实践指南

| 文档 | 说明 |
|------|------|
| [hermes-技巧.md](hermes-技巧.md) | 快速技巧、开发工作流 |

## 参考文档

| 文档 | 说明 |
|------|------|
| [hermes-FAQ.md](hermes-FAQ.md) | 常见问题 |
| [hermes-Slash命令.md](hermes-Slash命令.md) | CLI 斜杠命令 |
| [hermes-CLI命令.md](hermes-CLI命令.md) | 命令行工具 |
| [hermes-提供商.md](hermes-提供商.md) | LLM 提供商配置 |
| [hermes-安全.md](hermes-安全.md) | 安全模型与最佳实践 |
| [hermes-工具参考.md](hermes-工具参考.md) | 47 个内置工具完整文档 |
| [hermes-工具集参考.md](hermes-工具集参考.md) | 工具集配置与管理 |
| [hermes-环境变量.md](hermes-环境变量.md) | 所有环境变量说明 |

## 快速导航

### 安装
```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

### 启动
```bash
hermes                 # 交互式会话
hermes -q "问题"       # 单次查询
hermes gateway run     # 消息网关模式
```

### 配置模型
```bash
hermes model           # 交互式选择 LLM 提供商
```

### 文档链接
- [安装指南](hermes-安装.md)
- [配置参考](hermes-配置.md)
- [技能系统](hermes-技能.md)
- [记忆系统](hermes-记忆.md)
- [消息网关](hermes-消息网关.md)
