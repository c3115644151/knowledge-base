# Vibe Coding CN - AI 知识索引

> **用途说明**：本目录为 AI Agent 可直接检索和执行的知识协议库。内容从人类可读教程转化为 IF-THEN 规则、决策树和问题-解决方案映射。

---

## 📋 知识库结构

```
vibe-coding/
├── README.md                    # 本文件（总索引）
├── core-protocols.md            # 核心行为协议（IF-THEN 规则）
├── concept-index.md             # 概念索引（定义|触发|指引）
├── decision-trees.md            # 决策树汇总
├── problem-solution-map.md      # 问题-解决方案映射
├── philosophy/                  # 哲学方法论
├── fundamentals/                # 基础原则（17 个文件）
├── guides/                      # 操作指南
│   ├── getting-started/        # 入门配置（5 个文件）
│   └── playbook/               # 实践手册（11 个文件）
├── case-studies/               # 实战案例（5 个文件）
├── skills/                     # 技能库索引（20 个技能分类）
├── prompts/                    # 提示词索引
└── workflow/                   # 工作流（3 个工作流协议）
```

---

## 🎯 AI 执行入口

### 新任务启动
```
1. 读取 core-protocols.md → 获取 IF-THEN 规则
2. 读取 decision-trees.md → 确定执行路径
3. 检索 problem-solution-map.md → 预判可能问题
```

### 环境配置
```
→ guides/getting-started/ 按顺序执行
```

### 遇到问题
```
→ problem-solution-map.md → 定位问题类型
→ fundamentals/common-pitfalls.md → 获取解决方案
→ fundamentals/strong-constraints.md → 确认约束边界
```

### 架构设计
```
→ philosophy/metaphysics-framework.md → 建立概念框架
→ fundamentals/glue-coding.md → 确定模块策略
→ fundamentals/project-architecture-template.md → 参考模板
```

---

## 📚 文档索引

### 核心协议（必读）
| 文件 | 内容 | 执行入口 |
|:---|:---|:---|
| `core-protocols.md` | 核心行为协议 | IF-THEN 规则 |
| `concept-index.md` | 概念索引 | 定义\|触发\|指引 |
| `decision-trees.md` | 决策树汇总 | 条件→分支→动作 |
| `problem-solution-map.md` | 问题-解决方案映射 | 问题→规则 |

### 哲学方法论
| 文件 | 内容 |
|:---|:---|
| `philosophy/README.md` | 方法论索引 |
| `philosophy/metaphysics-framework.md` | 世界观框架 |
| `philosophy/phenomenology.md` | 现象学还原协议 |
| `philosophy/控制论与科学方法论.md` | 负反馈收敛、黑箱测试 |
| `philosophy/辩证法.md` | 正反合循环 |
| `philosophy/AI蜂群协作.md` | 多 Agent 协作协议 |

### 基础原则（17 个文件）
| 文件 | 内容 |
|:---|:---|
| `fundamentals/README.md` | 基础原则索引 |
| `fundamentals/glue-coding.md` | 胶水编程原理 |
| `fundamentals/dev-experience.md` | 开发经验总结 |
| `fundamentals/code-review.md` | 代码审查协议 |
| `fundamentals/code-organization.md` | 代码组织原则 |
| `fundamentals/language-layers.md` | 语言层要素（L1-L12） |
| `fundamentals/common-pitfalls.md` | 常见坑汇总 |
| `fundamentals/strong-constraints.md` | 强前置条件约束 |
| `fundamentals/problem-solving.md` | 问题求解框架 |
| `fundamentals/programming-philosophy.md` | 编程之道 |
| `fundamentals/hard-won-lessons.md` | 血的教训 |
| `fundamentals/project-architecture-template.md` | 项目架构模板 |
| `fundamentals/system-prompt-principles.md` | 系统提示词构建 |
| `fundamentals/dataset-oriented-data-service.md` | 数据服务模板 |
| `fundamentals/harness-engineering.md` | Harness Engineering |
| `fundamentals/recursive-self-optimizing-systems.md` | 元方法论形式化 |

### 操作指南
| 目录 | 文件数 | 内容 |
|:---|:---:|:---|
| `guides/getting-started/` | 5 | 网络配置、开发环境、IDE、CLI |
| `guides/playbook/` | 11 | tmux、LazyVim 快捷键、各种配置文档 |

### 实战案例
| 文件 | 项目 | 技术栈 |
|:---|:---|:---|
| `case-studies/polymarket-dev.md` | Polymarket 套利 | Python, Web3 |
| `case-studies/telegram-dev.md` | Telegram Bot | Python, Telegram API |
| `case-studies/fate-engine-dev.md` | 命理引擎 | Python, 数据可视化 |
| `case-studies/openclaw-dev.md` | AI Agent | 多 Agent 协作 |

### 技能库
| 分类 | 数量 | 代表技能 |
|:---|:---:|:---|
| AI 工具与开发 | 5 | canvas-dev, claude-code-guide |
| 加密货币与交易 | 5 | ccxt, polymarket, hummingbot |
| 数据库 | 2 | postgresql, timescaledb |
| 开发工具 | 3 | proxychains, tmux-autopilot |
| 文档生成 | 3 | markdown-to-epub, sop-generator |
| 社交通讯 | 2 | telegram-dev |

### 工作流
| 工作流 | 触发场景 |
|:---|:---|
| `workflow/canvas-dev/` | 需要白板驱动架构设计 |
| `workflow/auto-dev-loop/` | 需要全自动开发闭环 |
| `workflow/markdown-to-epub/` | 需要文档格式转换 |

---

## 📊 统计信息

| 类别 | 文件数 |
|:---|:---:|
| 核心协议 | 4 |
| 哲学方法论 | 6 |
| 基础原则 | 16 |
| 入门指南 | 5 |
| 实践手册 | 11 |
| 实战案例 | 5 |
| 技能索引 | 2 |
| 工作流 | 4 |
| **总计** | **53+** |

---

## 🔄 更新说明

- **来源**：tukuaiai/vibe-coding-cn GitHub 仓库
- **转化原则**：经验描述 → 可执行规则（IF-THEN）
- **更新时间**：2026-04-23
- **维护策略**：随源仓库更新同步转化

---

## 🚀 快速导航

- 想了解核心理念？→ `philosophy/metaphysics-framework.md`
- 想配置开发环境？→ `guides/getting-started/`
- 遇到问题？→ `problem-solution-map.md`
- 想参考实战案例？→ `case-studies/`
- 需要特定技能？→ `skills/README.md`
