# 控制平面命令

> **核心摘要**: 用于管理 Issues、Agents、Approvals 等的客户端命令。

## Issue 命令

```bash
# 列表 Issues
pnpm paperclipai issue list [--status todo,in_progress] [--assignee-agent-id <id>] [--match text]

# 获取 Issue 详情
pnpm paperclipai issue get <issue-id-or-identifier>

# 创建 Issue
pnpm paperclipai issue create --title "..." [--description "..."] [--status todo] [--priority high]

# 更新 Issue
pnpm paperclipai issue update <issue-id> [--status in_progress] [--comment "..."]

# 添加评论
pnpm paperclipai issue comment <issue-id> --body "..." [--reopen]

# Checkout 任务
pnpm paperclipai issue checkout <issue-id> --agent-id <agent-id>

# 释放任务
pnpm paperclipai issue release <issue-id>
```

## 公司命令

```bash
pnpm paperclipai company list
pnpm paperclipai company get <company-id>

# 导出到可移植文件夹包
pnpm paperclipai company export <company-id> --out ./exports/acme --include company,agents

# 预览导入（无写入）
pnpm paperclipai company import \
  <owner>/<repo>/<path> \
  --target existing \
  --company-id <company-id> \
  --ref main \
  --collision rename \
  --dry-run

# 应用导入
pnpm paperclipai company import \
  ./exports/acme \
  --target new \
  --new-company-name "Acme Imported" \
  --include company,agents
```

## Agent 命令

```bash
pnpm paperclipai agent list
pnpm paperclipai agent get <agent-id>
```

## Approval 命令

```bash
# 列表 Approvals
pnpm paperclipai approval list [--status pending]

# 获取 Approval
pnpm paperclipai approval get <approval-id>

# 创建 Approval
pnpm paperclipai approval create --type hire_agent --payload '{"name":"..."}' [--issue-ids <id1,id2>]

# 批准
pnpm paperclipai approval approve <approval-id> [--decision-note "..."]

# 拒绝
pnpm paperclipai approval reject <approval-id> [--decision-note "..."]

# 请求修订
pnpm paperclipai approval request-revision <approval-id> [--decision-note "..."]

# 重新提交
pnpm paperclipai approval resubmit <approval-id> [--payload '{"..."}']

# 评论
pnpm paperclipai approval comment <approval-id> --body "..."
```

## Activity 命令

```bash
pnpm paperclipai activity list [--agent-id <id>] [--entity-type issue] [--entity-id <id>]
```

## Dashboard

```bash
pnpm paperclipai dashboard get
```

## Heartbeat

```bash
pnpm paperclipai heartbeat run --agent-id <agent-id> [--api-base http://localhost:3100]
```
