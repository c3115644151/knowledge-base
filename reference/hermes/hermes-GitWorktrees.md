# Git Worktrees

## 概述

Git Worktrees 允许在同一仓库上运行多个并行的 Hermes Agent，每个有自己独立的分支和工作目录，互不干扰。

## 配置

```yaml
# ~/.hermes/config.yaml
worktree:
  enabled: true    # 或设置 hermes -w 标志
  auto_include:
    - ".env"
    - "node_modules/"
```

### .worktreeinclude 文件

在仓库根目录创建 `.worktreeinclude`：
```
# .worktreeinclude
.env
.venv/
node_modules/
```

## 使用

```bash
# 交互模式
hermes -w

# 单次查询
hermes -w -q "Fix issue #123"
```

## 工作原理

1. 启动时在 `.worktrees/` 创建新 worktree
2. 为会话分配唯一分支
3. Agent 在隔离环境中工作
4. 退出时：
   - 干净的 worktree → 自动删除
   - 有更改的 worktree → 保留供手动恢复

## 使用场景

- 并行处理多个 Issue
- 同时开发多个功能
- 在不影响主分支的情况下实验
