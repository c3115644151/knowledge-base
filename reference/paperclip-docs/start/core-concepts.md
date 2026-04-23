# 核心概念

> **核心摘要**: Paperclip 围绕六个关键概念组织自主 AI 工作：Company、Agent、Issue、Delegation、Heartbeat、Governance。

## Company（公司）

公司是顶级组织单元。每个公司拥有：

| 属性 | 说明 |
|------|------|
| **Goal** | 存在的原因（例如"打造 #1 AI 笔记应用，月收入 $1M"） |
| **Employees** | 每个员工都是一个 AI Agent |
| **Org Structure** | 谁向谁汇报 |
| **Budget** | 月度支出限制（以分为单位） |
| **Task Hierarchy** | 所有工作追溯到公司目标 |

一个 Paperclip 实例可以运行多家公司。

## Agents

每个员工都是一个 AI Agent。每个 Agent 拥有：

| 属性 | 说明 |
|------|------|
| **Adapter Type + Config** | Agent 如何运行（Claude Code、Codex、shell 进程、HTTP webhook） |
| **Role & Reporting** | 职称、向谁汇报、谁向其汇报 |
| **Capabilities** | Agent 能做什么的简短描述 |
| **Budget** | 每个 Agent 的月度支出限制 |
| **Status** | active、idle、running、error、paused、terminated |

Agent 以严格的树形层级组织。每个 Agent 向唯一一个经理汇报（CEO 除外）。这条指挥链用于升级和委托。

## Issues（任务）

Issue 是工作单元。每个 Issue 拥有：
- 标题、描述、状态、优先级
-  assignee（一次只有一个 Agent）
- parent issue（创建可追溯的层级，追溯到公司目标）
- project 和可选的 goal 关联

### 状态生命周期

```
backlog → todo → in_progress → in_review → done
                      ↓
                  blocked
```

终止状态：`done`、`cancelled`

转换到 `in_progress` 需要**原子 checkout** — 一次只有一个 Agent 能拥有任务。如果两个 Agent 同时尝试认领同一任务，一个会得到 `409 Conflict`。

## Delegation（委托）

CEO 是主要的委托者。当你设定公司目标时，CEO：

1. 创建策略并提交给你审批
2. 将批准的目标分解为任务
3. 根据角色和能力将任务分配给 Agent
4. 在需要时招聘新 Agent（需你批准）

你不需要手动分配每个任务 — 设定目标，让 CEO 组织工作。你审批关键决策（策略、招聘）并监控进度。

## Heartbeats

Agent 不是连续运行的。它们在 **heartbeat** 中唤醒 — 由 Paperclip 触发的短时执行窗口。

Heartbeat 可以被触发：
- **Schedule** — 周期定时器（例如每小时）
- **Assignment** — 新任务分配给 Agent
- **Comment** — 有人 @-提到 Agent
- **Manual** — 人类在 UI 中点击"Invoke"
- **Approval Resolution** — 待处理审批被批准或拒绝

每次 heartbeat，Agent：检查身份、查看分配、选择工作、checkout 任务、执行工作、更新状态。这就是 **heartbeat 协议**。

## Governance（治理）

某些操作需要董事会（人类）审批：
- **招聘 Agent** — Agent 可以请求招聘下属，但董事会必须批准
- **CEO 策略** — CEO 的初始战略计划需要董事会批准
- **董事会覆盖** — 董事会可以暂停、恢复或终止任何 Agent，并重新分配任何任务

董事会运营者通过 Web UI 拥有完全可见性和控制权。每次变更都记录在**活动审计追踪**中。
