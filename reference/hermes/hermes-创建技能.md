# 创建技能

创建和分享 Hermes Agent 技能。

## Skill vs Tool

### 创建 Skill（技能）
- 能力可表达为指令 + shell 命令 + 现有工具
- 包装可通过 `terminal` 或 `web_extract` 调用的外部 CLI/API
- 不需要自定义 Python 集成
- 示例：arXiv 搜索、git 工作流、Docker 管理、PDF 处理

### 创建 Tool（工具）
- 需要端到端集成（API 密钥、认证流）
- 需要精确执行的定制处理逻辑
- 处理二进制数据、流或实时事件
- 示例：浏览器自动化、TTS、视觉分析

## 目录结构

```
skills/
├── research/
│ └── arxiv/
│ ├── SKILL.md           # 必需：主要指令
│ └── scripts/           # 可选：辅助脚本
│ └── search_arxiv.py
├── productivity/
│ └── ocr-and-documents/
│ ├── SKILL.md
│ └── scripts/
└── references/
```

## SKILL.md 格式

```markdown
---
name: my-skill
description: Brief description (shown in skill search results)
version: 1.0.0
author: Your Name
license: MIT
platforms: [macos, linux]    # 可选 - 限制到特定 OS
metadata:
  hermes:
    tags: [Category, Subcategory, Keywords]
    related_skills: [other-skill-name]
    requires_toolsets: [web]           # 可选 - 仅这些工具集激活时显示
    requires_tools: [web_search]        # 可选 - 仅这些工具可用时显示
    fallback_for_toolsets: [browser]    # 可选 - 这些工具集激活时隐藏
    fallback_for_tools: [browser_navigate]
    config:                            # 可选 - config.yaml 设置
      - key: my.setting
        description: "What this setting controls"
        default: "sensible-default"
        prompt: "Display prompt for setup"
required_environment_variables:          # 可选 - 需要的 env vars
  - name: MY_API_KEY
    prompt: "Enter your API key"
    help: "Get one at https://example.com"
    required_for: "API access"
---

# Skill Title

Brief intro.

## When to Use

Trigger conditions.

## Quick Reference

Table of common commands.

## Procedure

Step-by-step instructions.

## Pitfalls

Known failure modes.

## Verification

How to confirm it worked.
```

## 条件激活

### 平台限制
```yaml
platforms: [macos]            # 仅 macOS
platforms: [macos, linux]    # macOS 和 Linux
```

### 工具依赖
```yaml
metadata:
  hermes:
    requires_toolsets: [web]           # web 工具集必须激活
    requires_tools: [web_search]       # web_search 工具必须存在
    fallback_for_toolsets: [browser]    # browser 工具集激活时隐藏
```

| 字段 | 行为 |
|------|------|
| `requires_toolsets` | 任何列出的工具集**不**可用时隐藏 |
| `requires_tools` | 任何列出的工具**不**存在时隐藏 |
| `fallback_for_toolsets` | 任何列出的工具集**已**可用时隐藏 |
| `fallback_for_tools` | 任何列出的工具**已**存在时隐藏 |

## 环境变量需求

```yaml
required_environment_variables:
  - name: TENOR_API_KEY
    prompt: "Tenor API key"
    help: Get a key from https://developers.google.com/tenor
    required_for: "GIF search functionality"
```

缺失值**不会隐藏**技能。加载时 Hermes 会提示配置。

### 沙箱传递
声明的 `required_environment_variables` 自动传递到沙箱执行环境：
```yaml
terminal:
  env_passthrough:
    - MY_CUSTOM_VAR
```

## config.yaml 设置

```yaml
metadata:
  hermes:
    config:
      - key: wiki.path
        description: Path to the LLM Wiki knowledge base directory
        default: "~/wiki"
        prompt: Wiki directory path
```

存储在 `skills.config.<key>`。

## 发布技能

将技能上传到 Skills Hub 与社区分享。

## 相关链接

- [Adding Tools](hermes-添加工具.md)
- [Contributing](hermes-贡献.md)
