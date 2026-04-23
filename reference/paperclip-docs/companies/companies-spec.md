# Agent 公司规范

> **版本**: `agentcompanies/v1-draft`

## 1. 目的

Agent 公司包是用于描述使用带有 YAML frontmatter 的 markdown 文件的公司、团队、Agent、项目、任务和相关 skills 的文件系统和 GitHub 原生格式。

此规范是 Agent Skills 规范的扩展，不是替代。

它定义了公司、团队和 Agent 级包结构如何围绕现有 `SKILL.md` 模型组合。

此规范是供应商中立的。旨在可供任何 Agent 公司运行时使用，不仅限于 Paperclip。

## 2. 核心原则

1. Markdown 是规范的
2. Git 仓库是有效的包容器
3. 注册表是可选的发现层，不是权威
4. `SKILL.md` 仍由 Agent Skills 规范拥有
5. 外部引用必须可固定到不可变 Git commits
6. 属性和许可证元数据必须存活于导入/导出
7. slug 和相对路径是可移植的身份层，不是数据库 id
8. 约定文件夹结构应无需冗长连接即可工作
9. 供应商特定保真度属于可选扩展，不是基本包

## 3. 包种类

包根由一个主要 markdown 文件标识：

- `COMPANY.md` 公司包
- `TEAM.md` 团队包
- `AGENTS.md` Agent 包
- `PROJECT.md` 项目包
- `TASK.md` 任务包
- `SKILL.md` Agent Skills 规范定义的 skill 包

## 4. 保留文件和目录

约定结构：

```text
COMPANY.md
TEAM.md
AGENTS.md
PROJECT.md
TASK.md
SKILL.md
agents/<slug>/AGENTS.md
teams/<slug>/TEAM.md
projects/<slug>/PROJECT.md
projects/<slug>/tasks/<slug>/TASK.md
tasks/<slug>/TASK.md
skills/<slug>/SKILL.md
.paperclip.yaml
HEARTBEAT.md
SOUL.md
TOOLS.md
README.md
assets/
scripts/
references/
```

## 5. Paperclip 映射

Paperclip 可以将本规范映射到其运行时模型：

| 基本包 | Paperclip |
|--------|-----------|
| `COMPANY.md` | 公司元数据 |
| `TEAM.md` | 可导入的组织子树 |
| `AGENTS.md` | Agent 身份和指令 |
| `PROJECT.md` | 起始项目定义 |
| `TASK.md` | 起始 Issue/任务定义，`recurring: true` 时为重复任务模板 |
| `SKILL.md` | 导入的 skill 包 |
| `sources[]` | 来源和固定上游引用 |
| `.paperclip.yaml` | Adapter 配置、运行时配置、env 输入声明、权限、预算、routine triggers 等 Paperclip 特定保真度 |
