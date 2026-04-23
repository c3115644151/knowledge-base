# ClipHub 计划

> **状态**: 已废弃注意 | 此 marketplace 计划早于 markdown-first 公司包方向。

## 概述

**ClipHub** 是整个公司 AI 团队配置的"应用商店"——预构建的 Paperclip 配置、Agent 蓝图、skills 和治理模板，从第一天起就可以运输真实工作。

| 维度 | ClipHub |
|------|---------|
| 销售单位 | 团队蓝图（多 Agent 组织） |
| 买家 | 想启动 AI 公司的创始人/团队负责人 |
| 安装目标 | Paperclip 公司（Agent、项目、治理） |
| 价值主张 | "跳过组织设计——几分钟内获得一个可发货团队" |
| 价格范围 | $0–$499 per 蓝图 |

## 产品分类

### 团队蓝图（主要产品）

完整的 Paperclip 公司配置：
- **组织架构**: 带有角色、报告链、能力的 Agent
- **Agent 配置**: Adapter 类型、模型、prompt 模板、指令路径
- **治理规则**: 审批流程、预算限制、升级链
- **项目模板**: 预配置的项目和工作区设置
- **Skills & 指令**: 每个 Agent 打包的 AGENTS.md / skill 文件

### Agent 蓝图（个人 Agent）

设计插入 Paperclip 组织的单个 Agent 配置：
- 角色定义、prompt 模板、adapter 配置
- 报告链期望
- 包含的 skill bundles
- 治理默认值

### Skills（模块化能力）

任何 Paperclip Agent 都可以使用的可移植 skill 文件：
- Markdown skill 文件带指令
- 工具配置和 shell 脚本
- 兼容 Paperclip 的 skill 加载系统

### 治理模板

预构建审批流程和策略：
- 预算阈值和审批链
- 跨团队委托规则
- 升级程序
- 计费代码结构

## MVP 范围

### Phase 1: 基础
- [ ] Listing schema 和 CRUD API
- [ ] 带过滤的浏览页面（类型、类别、价格）
- [ ] 带组织架构可视化的 Listing 详情页
- [ ] 创建者注册和 listing 创建向导
- [ ] 仅免费安装（尚无支付）
- [ ] 安装流程：蓝图 → Paperclip 公司

### Phase 2: 支付 & 社交
- [ ] Stripe Connect 集成
- [ ] 购买流程
- [ ] 审核系统
- [ ] 创建者分析仪表盘
- [ ] "从 Paperclip 导出"CLI 命令

### Phase 3: 增长
- [ ] 相关性排序搜索
- [ ] 精选/趋势 listings
- [ ] 创建者验证程序
- [ ] 蓝图版本控制和更新通知
- [ ] 实时演示沙箱
- [ ] 程序化发布的 API

> **注意**: 此计划已被 markdown-first 公司包方向取代。
