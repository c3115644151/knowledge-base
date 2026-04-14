# 会话管理 (Sessions)

## 概述

Hermes Agent 将对话历史存储在 SQLite 数据库中，支持会话恢复、搜索和压缩。

## 会话存储

```
~/.hermes/
└── state.db          # SQLite 数据库
    ├── sessions      # 会话元数据
    ├── messages      # 消息历史
    └── indexes       # 全文搜索索引
```

### 数据库内容
- 会话元数据 (ID、标题、时间戳、token 计数)
- 消息历史
- 跨压缩/恢复的会话谱系
- `session_search` 使用的全文搜索索引

## 会话命令

| 命令 | 说明 |
|------|------|
| `hermes sessions list` | 列出所有会话 |
| `hermes sessions show <id>` | 显示会话详情 |
| `hermes sessions rename <id> <title>` | 重命名会话 |
| `hermes sessions delete <id>` | 删除会话 |
| `hermes sessions search <query>` | 搜索会话 |

## 会话恢复

### CLI 恢复
```bash
hermes --continue          # 恢复最近的 CLI 会话
hermes -c                  # 简写
hermes -c "my project"     # 按标题恢复
hermes --resume <session_id>  # 按 ID 恢复
hermes -r <session_id>     # 简写
```

### 恢复时显示
恢复会话时显示"上一次对话"面板：
- 紧凑的对话历史摘要
- 工具调用概览

## 上下文压缩

当对话接近上下文限制时自动压缩：

```yaml
compression:
  enabled: true
  threshold: 0.50          # 50% 时触发
  target_ratio: 0.20       # 保留 20%
  protect_last_n: 20       # 最少保留 20 条消息
  summary_model: "google/gemini-3-flash-preview"
  summary_provider: "auto"
```

### 压缩规则
- **保留**: 最初 3 条 + 最近 4 条消息
- **压缩**: 中间消息被摘要替换

### 手动压缩
```bash
/compress    # 手动压缩当前会话
```

## 后台会话

在不中断当前对话的情况下运行后台任务：

```bash
/background 分析 /var/log 中的错误
```

### 特性
- 完全隔离的对话历史
- 继承当前会话的配置
- 最多 3 个并发后台任务
- 结果以面板形式显示

## 上下文压力警告

| 进度 | 级别 | 行为 |
|------|------|------|
| ≥60% | 信息 | CLI 显示进度条 |
| ≥85% | 警告 | 压缩即将触发 |

## 迭代预算压力

当接近最大迭代次数时警告：

| 阈值 | 级别 | 信息 |
|------|------|------|
| 70% | 注意 | `[BUDGET: 63/90. 27 iterations left]` |
| 90% | 警告 | `[BUDGET WARNING: 81/90. Only 9 left]` |

```yaml
agent:
  max_turns: 90    # 默认最大迭代次数
```

## 会话管理技巧

1. **命名会话** - `/title My Session` 便于后续恢复
2. **定期压缩** - 长对话使用 `/compress`
3. **后台任务** - 使用 `/background` 处理长时间任务
4. **会话搜索** - 快速找到历史信息
