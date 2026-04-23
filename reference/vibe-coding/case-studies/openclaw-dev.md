# OpenClaw 项目

## 项目背景

OpenClaw 是一个开源、自托管的 AI Agent 系统，让 AI 从"聊天工具"变成"能自主执行任务的数字员工"。支持连接 20+ 消息渠道（WhatsApp、Telegram、飞书、钉钉、Discord 等），可主动执行任务、管理日程、处理邮件、操作浏览器等。

截至 2026 年 3 月，GitHub Stars 达 278,932，成为全球第一软件项目。

## 核心技术栈

- **语言**: TypeScript/JavaScript
- **运行时**: Node.js、Bun
- **架构**: Gateway-Node-Channel 三层架构
- **通信**: WebSocket
- **记忆系统**: 四层记忆（SOUL → TOOLS → USER → Session）
- **部署**: Docker、本地安装

## 关键实现要点

### IF-THEN 规则

1. **IF** 需要远程访问 OpenClaw Gateway
   **THEN** 使用 Tailscale Serve（仅 Tailscale 网络）或 Funnel（公网 webhook 回调）

2. **IF** Gateway 需要 webhook 回调（如飞书、Slack HTTP 模式）
   **THEN** 使用 `tailscale funnel --bg` 暴露公网地址

3. **IF** 需要接入新消息渠道
   **THEN** 优先选择 long-polling 模式（如 Telegram），避免需要公网 IP 的方案

4. **IF** 在多人环境中运行 Gateway
   **THEN** 使用 VM 或专用服务器，避免 prompt injection 风险

## 渠道接入对比

| 渠道 | 难度 | 时间 | 推荐理由 |
|:---|:---|:---|:---|
| Telegram | 简单 | 5分钟 | 不需公网IP，长 polling 即可 |
| QQ | 简单 | 5分钟 | 国内首选，扫码即用 |
| Discord | 中等 | 15分钟 | 社区场景佳 |
| 飞书 | 中等 | 15分钟 | 国内企业，原生内置 |
| 钉钉 | 中等 | 20分钟 | Stream 模式免公网 |
| WhatsApp | 中等 | 10分钟 | 海外日常，需独立号码 |
| 微信个人 | 复杂 | 1小时+ | 无官方 API，封号风险 |

## 遇到的问题与解决方案

| 问题 | 解决方案 |
|:---|:---|
| 安全漏洞（CVE-2026-25253） | v2026.2 后修复，及时更新版本 |
| 恶意 Skills（ClawHub 12%） | 使用 SecureClaw 安全扫描 |
| API 账单超支 | 设置消费限额，使用本地模型 |
| 谷歌封号 | 官方已解决，关注后续稳定性 |

## 可复用经验总结

1. **Gateway 架构设计**：Loopback-First 安全设计，默认仅绑定 localhost
2. **四层记忆系统**：从不可变身份内核到实时会话，构建上下文连续性
3. **Skills 系统**：遵循"最小必要代码"原则，通过 Skills 扩展能力
4. **强依赖复用**：直接使用外部仓库源码，避免重复造轮子

---

**源文档**: `/tmp/vibe-coding-cn/assets/documents/case-studies/openclaw-dev/`
