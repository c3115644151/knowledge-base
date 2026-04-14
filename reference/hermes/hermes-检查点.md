# Checkpoints & Rollback

Hermes Agent 在破坏性操作前自动快照工作目录，支持一键回滚。

## 工作原理

- 检测到文件修改工具即将执行时
- 每个目录每轮对话最多创建一次快照
- 快照存储在 `~/.hermes/checkpoints/` 的影子 git 仓库中

## 触发条件

**自动创建快照**：
- 文件工具：`write_file`、`patch`
- 破坏性终端命令：`rm`、`mv`、`sed -i`、`truncate`、`shred`、输出重定向、`git reset/clean/checkout`

## 命令参考

| 命令 | 说明 |
|------|------|
| `/rollback` | 列出所有快照及变更统计 |
| `/rollback <N>` | 回滚到快照 N（同时撤销上次对话） |
| `/rollback diff <N>` | 预览快照 N 与当前状态的差异 |
| `/rollback <N> <file>` | 仅恢复快照 N 中的单个文件 |

## 使用示例

### 列出快照
```
/rollback
```
输出：
```
📸 Checkpoints for /path/to/project:
 1. 4270a8c 2026-03-16 04:36 before patch (1 file, +1/-0)
 2. eaf4c1f 2026-03-16 04:35 before write_file
 3. b3f9d2e 2026-03-16 04:34 before terminal: sed -i (1 file, +1/-1)
 /rollback <N> restore to checkpoint N
```

### 预览差异
```
/rollback diff 1
```

### 恢复快照
```
/rollback 1
```

回滚后：
- 自动保存预回滚快照（可撤销回滚）
- 恢复工作目录中的文件
- 撤销对话历史以匹配恢复的文件状态

### 恢复单个文件
```
/rollback 1 src/broken_file.py
```

## 配置

```yaml
checkpoints:
  enabled: true          # 主开关（默认: true）
  max_snapshots: 50     # 每个目录最大快照数
```

禁用：
```yaml
checkpoints:
  enabled: false
```

## 快照存储位置

```
~/.hermes/checkpoints/
 ├── <hash1>/  # 影子 git 仓库
 ├── <hash2>/
 └── ...
```

每个 hash 派生自工作目录的绝对路径。

## 安全与性能保障

- **Git 不可用**：静默禁用快照
- **目录范围**：跳过根目录和 home 目录
- **仓库大小**：超过 50,000 文件的目录跳过
- **无变化快照**：跳过无变更的快照
- **非致命错误**：所有错误仅记录日志

## 最佳实践

1. 保持快照启用（无修改时零开销）
2. 回滚前使用 `/rollback diff` 预览
3. 结合 Git worktree 使用，获得最大安全性
