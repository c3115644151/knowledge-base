# 上下文文件

Hermes Agent 自动发现并加载塑造其行为的上下文文件。

## 支持的上下文文件

| 文件 | 用途 | 发现方式 |
|------|------|----------|
| **.hermes.md** / **HERMES.md** | 项目指令（最高优先级） | 步行到 git 根目录 |
| **AGENTS.md** | 项目指令、约定、架构 | 启动时从 CWD + 子目录渐进 |
| **CLAUDE.md** | Claude Code 上下文文件（也检测） | 同上 |
| **SOUL.md** | 全局人格和语气定制 | 仅 `HERMES_HOME/SOUL.md` |
| **.cursorrules** | Cursor IDE 编码约定 | 仅 CWD |
| **.cursor/rules/\*.mdc** | Cursor IDE 规则模块 | 仅 CWD |

**优先级**：`.hermes.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules`。**SOUL.md** 始终独立加载为代理身份（槽位 #1）。

## AGENTS.md

`AGENTS.md` 是主要项目上下文文件。告诉代理项目结构、遵循的约定和特殊指令。

### 渐进子目录发现

启动时，Hermes 从工作目录加载 `AGENTS.md` 到系统提示。当代理在会话期间导航到子目录时，**渐进发现**这些目录中的上下文文件并注入。

```
my-project/
├── AGENTS.md ← 启动时加载
├── frontend/
│ └── AGENTS.md ← 发现当代理读取 frontend/ 文件
├── backend/
│ └── AGENTS.md ← 发现当代理读取 backend/ 文件
└── shared/
 └── AGENTS.md ← 发现当代理读取 shared/ 文件
```

## SOUL.md

`SOUL.md` 控制代理的人格、语气和沟通风格。

**位置**：
- `~/.hermes/SOUL.md`
- 或 `$HERMES_HOME/SOUL.md`（使用自定义 home 目录时）

## .cursorrules

Hermes 与 Cursor IDE 的 `.cursorrules` 文件和 `.cursor/rules/*.mdc` 规则模块兼容。

## 安全：提示注入保护

所有上下文文件在被包含前扫描潜在提示注入：
- 指令覆盖尝试："ignore previous instructions"
- 欺骗模式："do not tell the user"
- 隐藏 HTML 注释：`<!-- ignore instructions -->`
- 隐藏 div 元素：`<div style="display:none">`
- 凭证泄露：`curl ... $API_KEY`
- 秘密文件访问：`cat .env`、`cat credentials`

## 大小限制

| 限制 | 值 |
|------|-----|
| 每文件最大字符数 | 20,000 (~7,000 tokens) |
| 头部截断比例 | 70% |
| 尾部截断比例 | 20% |

## AGENTS.md 最佳实践

1. **保持简洁** — 保持在 20K 字符以下
2. **用标题结构化** — 使用 `##` 标题分节
3. **包含具体示例** — 显示首选代码模式、API 形状
4. **说明不要做什么** — "never modify migration files directly"
5. **列出关键路径和端口** — 代理用这些执行终端命令
6. **随项目更新** — 过时的上下文比没有更糟
