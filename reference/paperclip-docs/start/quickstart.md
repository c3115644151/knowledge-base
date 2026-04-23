# 快速开始

> **核心摘要**: 5 分钟内在本地运行 Paperclip，支持一键启动和本地开发两种模式。

## 推荐：快速启动（5 分钟）

```bash
npx paperclipai onboard --yes
```

此命令引导你完成设置、配置环境、启动 Paperclip。

如果已有 Paperclip 安装，重新运行 `onboard` 会保留现有配置和数据路径。使用 `paperclipai configure` 可以编辑设置。

之后启动 Paperclip：
```bash
npx paperclipai run
```

> **注意**: 如果使用 `npx` 进行设置，请始终使用 `npx paperclipai` 运行命令。`pnpm paperclipai` 形式仅在克隆的 Paperclip 仓库中有效。

## 本地开发

适用于为 Paperclip 本身做出贡献的开发者。

### 前提条件
- Node.js 20+
- pnpm 9+

### 启动开发服务器

```bash
git clone https://github.com/paperclipai/paperclip
cd paperclip
pnpm install
pnpm dev
```

这会启动 API 服务器和 UI，地址为 http://localhost:3100。

**无需外部数据库** — Paperclip 默认使用嵌入式 PostgreSQL 实例。

在克隆的仓库中，你也可以使用：
```bash
pnpm paperclipai run
```

这会在配置缺失时自动引导、运行带自动修复的健康检查，然后启动服务器。

## 下一步

Paperclip 运行后：

1. 在 Web UI 中创建你的第一家公司
2. 定义公司目标
3. 创建 CEO Agent 并配置其 Adapter
4. 用更多 Agent 构建组织架构
5. 设置预算并分配初始任务
6. 启动 — Agent 开始心跳，公司开始运转

---

**相关阅读**: [核心概念](./core-concepts.md) — 学习 Paperclip 背后的关键概念
