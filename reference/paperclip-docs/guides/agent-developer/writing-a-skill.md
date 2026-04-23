# Skill 编写指南

> **核心摘要**: Skill 是 Agent 可以在 heartbeat 期间调用的可重用指令。它们是教 Agent 如何执行特定任务的 markdown 文件。

## Skill 结构

Skill 是包含 `SKILL.md` 文件的目录，可选支持文件在 `references/` 中：

```
skills/
└── my-skill/
    ├── SKILL.md          # 主 skill 文档
    └── references/       # 可选支持文件
        └── examples.md
```

## SKILL.md 格式

```markdown
---
name: my-skill
description: >
  简短描述这个 skill 做什么以及何时使用。
  这作为路由逻辑——Agent 阅读这个来决定
  是否加载完整 skill 内容。
---
# My Skill
Agent 的详细指令...
```

### Frontmatter 字段

| 字段 | 说明 |
|------|------|
| **name** | Skill 的唯一标识符（kebab-case） |
| **description** | 路由描述，告诉 Agent 何时使用这个 skill。写成决策逻辑，不是营销文案。 |

## Skill 在运行时如何工作

1. Agent 在其上下文中看到 skill 元数据（name + description）
2. Agent 决定 skill 是否与其当前任务相关
3. 如果相关，Agent 加载完整 SKILL.md 内容
4. Agent 遵循 skill 中的指令

这保持 base prompt 小——只在需要时加载完整 skill 内容。

## 最佳实践

| 实践 | 说明 |
|------|------|
| **将描述写成路由逻辑** | 包括"use when"和"don't use when"指导 |
| **具体且可操作** | Agent 应该能够无歧义地遵循 skill |
| **包含代码示例** | 具体的 API 调用和命令示例比散文更可靠 |
| **保持 skill 专注** | 每个 concern 一个 skill；不要混合无关的程序 |
| **谨慎使用引用文件** | 将支持细节放在 `references/` 而不是膨胀主 SKILL.md |

## Skill 注入

Adapter 负责使 skill 对其 Agent 运行时可发现。`claude_local` adapter 使用带有符号链接的临时目录和 `--add-dir`。`codex_local` adapter 使用全局 skills 目录。详见 [创建 Adapter](../adapters/creating-an-adapter.md) 指南。
