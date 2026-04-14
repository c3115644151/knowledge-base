# 人格与 SOUL.md

Hermes Agent 的人格完全可定制。`SOUL.md` 是**主要身份**——它在系统提示中排第一，定义代理是谁。

## SOUL.md 工作方式

Hermes 在 `~/.hermes/SOUL.md` 自动生成默认 `SOUL.md`。

### 重要行为

- **SOUL.md 是代理的主要身份**。占据系统提示槽位 #1
- 如果不存在，Hermes 自动创建起始 `SOUL.md`
- 现有用户 `SOUL.md` 文件永不被覆盖
- Hermes 仅从 `HERMES_HOME` 加载 `SOUL.md`
- Hermes 不在工作目录中查找 `SOUL.md`

## SOUL.md vs AGENTS.md

### SOUL.md

用于：
- 身份
- 语气
- 风格
- 沟通默认值
- 人格级行为

### AGENTS.md

用于：
- 项目架构
- 编码约定
- 工具偏好
- 特定项目的仓库工作流
- 命令、端口、路径、部署说明

**规则**：
- 应该随身携带的 → `SOUL.md`
- 属于项目的 → `AGENTS.md`

## 内置人格

| 名称 | 描述 |
|------|------|
| **helpful** | 友好、通用助手 |
| **concise** | 简洁、点到为止 |
| **technical** | 详细、准确技术专家 |
| **creative** | 创新、跳出框框思考 |
| **teacher** | 耐心教育者，清晰示例 |
| **kawaii** | 可爱表达，星星眼和热情 ★ |
| **catgirl** | 猫娘表达，喵~\~ |
| **pirate** | 赫尔墨斯船长，科技海盗 |
| **shakespeare** | 莎士比亚戏剧风格 |
| **surfer** | 完全放松的兄弟氛围 |
| **noir** | 硬汉侦探叙述 |
| **uwu** | 极致可爱 uwu 语言 |
| **philosopher** | 深度思考每个问题 |
| **hype** | 最大能量和热情！！！ |

## 切换人格

### CLI
```bash
/personality
/personality concise
/personality technical
```

### 消息平台
```bash
/personality teacher
```

## 自定义人格（config）

在 `~/.hermes/config.yaml` 定义命名自定义人格：

```yaml
agent:
  personalities:
    codereviewer: >
      You are a meticulous code reviewer. Identify bugs, security issues,
      performance concerns, and unclear design choices. Be precise and constructive.
```

然后切换：
```bash
/personality codereviewer
```

## 好的 SOUL.md 内容

```markdown
# Personality

You are a pragmatic senior engineer with strong taste.
You optimize for truth, clarity, and usefulness over politeness theater.

## Style

- Be direct without being cold
- Prefer substance over filler
- Push back when something is a bad idea
- Admit uncertainty plainly
- Keep explanations compact unless depth is useful

## What to avoid

- Sycophancy
- Hype language
- Repeating the user's framing if it's wrong
- Overexplaining obvious things

## Technical posture

- Prefer simple systems over clever systems
- Care about operational reality, not idealized architecture
- Treat edge cases as part of the design, not cleanup
```
