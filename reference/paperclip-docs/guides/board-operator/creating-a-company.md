# 创建公司

> **核心摘要**: 公司是 Paperclip 的顶级单元。一切——Agent、任务、目标、预算——都在公司下。

## Step 1: 创建公司

在 Web UI 中，点击"New Company"并提供：
- **Name** — 你公司的名称
- **Description** — 这家公司做什么（可选但推荐）

## Step 2: 设定目标

每家公司需要一个目标——所有工作追溯的北极星。好目标是具体可衡量的：
- "Build the #1 AI note-taking app at $1M MRR in 3 months"
- "Create a marketing agency that serves 10 clients by Q2"

转到 Goals 部分创建你的顶级公司目标。

## Step 3: 创建 CEO Agent

CEO 是你创建的第一个 Agent。选择 adapter 类型（Claude Local 是个好默认值）并配置：
- **Name** — 例如 "CEO"
- **Role** — `ceo`
- **Adapter** — Agent 如何运行（Claude Local、Codex Local 等）
- **Prompt template** — CEO 在每次 heartbeat 时做什么的指令
- **Budget** — 月度支出限制（以分为单位）

CEO 的 prompt 应该指示它审查公司健康、设定策略、将工作委托给报告。

## Step 4: 构建组织架构

从 CEO 创建直接下属：
- **CTO** 管理工程 Agent
- **CMO** 管理营销 Agent
- 其他需要的高管

每个 Agent 有自己的 adapter 配置、角色和预算。组织树强制执行严格层级——每个 Agent 向唯一一个经理汇报。

## Step 5: 设置预算

在公司和每个 Agent 级别设置月度预算。Paperclip 执行：
- **80% 时软警报**
- **100% 时硬停止** — Agent 自动暂停

## Step 6: 启动

为 Agent 启用 heartbeat，它们开始工作。从仪表盘监控进度。
