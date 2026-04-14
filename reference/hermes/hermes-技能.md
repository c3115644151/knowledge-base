# 技能系统 (Skills)

## 概念

**技能 (Skills)** 是按需加载的知识文档，存储在 `~/.hermes/skills/` 目录。Agent 遇到复杂任务时自动加载相关技能到上下文。

### 技能 vs 工具 vs 记忆

| 类型 | 本质 | 触发方式 | 用途 |
|------|------|----------|------|
| **技能** | 知识文档 | 按需加载 | 告诉 Agent 如何做 |
| **工具** | 可执行函数 | Agent 自动调用 | 执行实际操作 |
| **记忆** | 事实存储 | 自动检索 | 记住学到的知识 |

## 技能结构

每个技能是一个目录，包含 `SKILL.md`：

```
~/.hermes/skills/my-skill/
└── SKILL.md          # 技能定义文件
```

### SKILL.md 格式

```markdown
---
name: my-skill
description: 技能的简短描述
---

# My Skill

详细的使用说明...

## 使用场景

当用户需要...

## 示例

```bash
example command
```
```

### YAML Frontmatter 可选字段

```yaml
---
name: skill-name
description: 简短描述
allowed_tools:        # 允许使用的工具
  - terminal
  - read_file
required_environment_variables:  # 必需的环境变量
  - name: API_KEY
    prompt: API Key for service
    help: Get from https://...
credential_files:      # 需要的凭证文件
  - path: token.json
    description: OAuth token
---
```

## 技能安装

### 从 skills.sh 安装
```bash
hermes skills install skills-sh/vercel-labs/json-render

# 强制覆盖
hermes skills install openai/skills/k8s --force
```

### 从官方目录安装
```bash
hermes skills install official/security/1password
```

### 从 URL 安装
```bash
hermes skills install https://example.com/skill --source well-known
```

### 搜索技能
```bash
hermes skills search kubernetes
hermes skills search react --source skills-sh
```

## 技能命令

| 命令 | 说明 |
|------|------|
| `/skill <name>` | 加载技能到当前会话 |
| `/skills browse` | 浏览可用技能 |
| `hermes skills list` | 列出已安装技能 |
| `hermes skills install <url>` | 安装技能 |
| `hermes skills uninstall <name>` | 卸载技能 |
| `hermes skills search <query>` | 搜索技能 |

## 自动加载

Agent 会根据任务自动识别和加载相关技能。技能内容按渐进式披露模式加载，节省 token。

## 技能与 Slash 命令

每个已安装的技能自动注册为 slash 命令：

```bash
/gif-search funny cats
/axolotl help me fine-tune Llama 3
/github-pr-workflow create a PR
```

## 创建自定义技能

```bash
hermes skills create my-awesome-skill
```

这会在 `~/.hermes/skills/my-awesome-skill/` 创建目录和模板 `SKILL.md`。

## 技能与 skills.sh 兼容性

Hermes 技能系统兼容 [agentskills.io](https://agentskills.io/specification) 开放标准。

## 实践技巧

1. **保持简洁** - 技能内容会被加载到上下文
2. **渐进披露** - 使用折叠或分节组织长内容
3. **示例代码** - 包含可运行的示例
4. **明确触发条件** - 在 description 中描述使用场景
