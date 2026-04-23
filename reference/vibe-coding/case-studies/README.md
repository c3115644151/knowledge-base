# Case Studies 实战案例索引

> 真实项目的开发经验与复盘

## 案例列表

| 项目 | 类型 | 核心技术 | 适用场景 |
|:---|:---|:---|:---|
| [polymarket-dev.md](./polymarket-dev.md) | 套利系统 | Python / Polymarket API / ASCII 可视化 | 预测市场分析、程序化交易 |
| [telegram-dev.md](./telegram-dev.md) | Bot 开发 | Python / python-telegram-bot | 消息平台集成、格式化处理 |
| [fate-engine-dev.md](./fate-engine-dev.md) | 业务引擎 | Python / 强依赖复用模式 | 命理分析、复杂算法集成 |
| [openclaw-dev.md](./openclaw-dev.md) | AI Agent | TypeScript / WebSocket / Gateway 架构 | 多渠道接入、自托管 AI 助手 |

---

## 技术栈对照表

| 技术栈 | 案例 |
|:---|:---|
| **Python** | polymarket-dev、telegram-dev、fate-engine-dev |
| **TypeScript** | openclaw-dev |
| **API 集成** | polymarket-dev（Polymarket/Kalshi）、openclaw-dev（20+渠道） |
| **WebSocket** | openclaw-dev |
| **ASCII 可视化** | polymarket-dev、fate-engine-dev |
| **强依赖复用** | fate-engine-dev |
| **Docker** | openclaw-dev |

---

## 适用场景指引

### 预测市场与程序化交易
→ 参考 [polymarket-dev.md](./polymarket-dev.md)
- 套利逻辑设计
- API 数据采集
- ASCII 可视化

### 消息平台 Bot 开发
→ 参考 [telegram-dev.md](./telegram-dev.md)
- Markdown 格式处理
- Bot 框架使用
- 错误排查方法

### 复杂业务系统构建
→ 参考 [fate-engine-dev.md](./fate-engine-dev.md)
- 强依赖复用模式
- 问题描述模板化
- 完整性检查流程

### AI Agent 平台部署
→ 参考 [openclaw-dev.md](./openclaw-dev.md)
- Gateway 架构设计
- 多渠道接入
- 记忆系统设计
- 安全与成本控制

---

## 跨案例通用经验

1. **强依赖复用模式**：优先使用成熟仓库源码，避免重复造轮子
2. **问题描述模板化**：结构化输出确保无歧义，便于 AI 分析
3. **完整性检查**：代码生成后系统性验证
4. **终端友好可视化**：ASCII 字符画适合各类终端环境

---

**源目录**: `/tmp/vibe-coding-cn/assets/documents/case-studies/`
