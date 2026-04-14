# 记忆系统 (Memory)

## 概述

Hermes Agent 的持久化记忆系统，让 Agent 跨会话记住用户偏好、项目信息和学到的知识。

## 记忆类型

### 1. 内置记忆文件

| 文件 | 位置 | 用途 |
|------|------|------|
| `MEMORY.md` | `~/.hermes/memories/` | Agent 学到的知识 |
| `USER.md` | `~/.hermes/memories/` | 用户画像和偏好 |

### 2. 上下文文件

Agent 自动发现的配置文件，影响特定项目/目录的行为：

| 文件名 | 用途 |
|--------|------|
| `.hermes.md` | Hermes 项目配置 |
| `AGENTS.md` | Agent 行为指南 |
| `CLAUDE.md` | Claude 兼容配置 |
| `.cursorrules` | Cursor IDE 规则 |
| `SOUL.md` | Agent 身份/人格 |

### 3. 上下文引用

使用 `@` 引用文件、文件夹、git diff、URL：

```
@/path/to/file.txt
@./src/
@git diff main
@https://example.com/doc
```

### 4. 检查点 (Checkpoints)

自动快照工作目录，支持回滚：

```bash
/rollback    # 回滚更改
/checkpoint  # 创建检查点
```

## 配置

```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  memory_char_limit: 2200    # ~800 tokens
  user_char_limit: 1375       # ~500 tokens
```

## Honcho 记忆

[Honcho](https://github.com/plastic-labs/honcho) 是高级记忆后端：

### 特点
- **辩证推理** - 每次对话后分析，提取用户偏好和模式的洞察
- **用户画像** - 自动维护用户模型
- **多 Agent 隔离** - 每个 Agent 有独立的 Peer 档案
- **语义搜索** - 跨记忆内容的搜索

### 工具
| 工具 | 用途 |
|------|------|
| `honcho_conclude` | 触发辩证推理 |
| `honcho_context` | 检索相关记忆 |
| `honcho_profile` | 查看/更新用户档案 |
| `honcho_search` | 语义搜索 |

### 配置
```yaml
memory:
  provider: honcho

honcho:
  observation: directional  # "unified" 或 "directional"
  peer_name: ""             # 自动检测
```

## 其他记忆提供者

| 提供者 | 说明 |
|--------|------|
| `honcho` | 辩证推理用户建模 |
| `openviking` | OpenViking 集成 |
| `mem0` | Mem0 记忆服务 |
| `hindsight` | 回顾性记忆 |
| `holographic` | 全息记忆 |
| `retaindb` | RetainDB 服务 |

## 记忆操作命令

| 命令 | 说明 |
|------|------|
| `/remember <info>` | 记住信息 |
| `/recall <query>` | 检索记忆 |
| `/forget <info>` | 删除记忆 |
| `/memory` | 查看记忆状态 |
| `hermes memory setup` | 配置记忆提供者 |

## 自动记忆

Agent 会自动：
1. 将重要信息写入 `MEMORY.md`
2. 更新 `USER.md` 中的用户偏好
3. 加载相关记忆到当前会话上下文
4. 忽略不相关或过时的记忆

## 最佳实践

1. **重要信息** - 使用 `/remember` 明确存储
2. **用户偏好** - 自然对话中学习
3. **项目上下文** - 使用 `.hermes.md`
4. **清理** - 定期使用 `/forget` 清理过时记忆
