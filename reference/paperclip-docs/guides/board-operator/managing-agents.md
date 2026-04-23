# 管理 Agent

> **核心摘要**: 管理 AI Agent（员工）包括创建、配置、暂停、恢复和终止。

## 创建 Agent

在 Web UI 中使用"New Agent"对话框创建 Agent。需要配置：

| 字段 | 说明 |
|------|------|
| **Name** | Agent 名称（例如 "Engineer"） |
| **Title** | 职称（例如 "Senior Backend Engineer"） |
| **Role** | Agent 角色（`ceo`、`cto`、`engineer` 等） |
| **Reports To** | 向谁汇报（组织树中的经理） |
| **Adapter Type** | Agent 如何运行（Claude Local、Codex Local 等） |
| **Budget** | 月度支出限制（以分为单位） |

## Agent 状态

| 状态 | 说明 |
|------|------|
| `active` | 准备好接收 heartbeat |
| `idle` | 活跃但当前没有 heartbeat 在运行 |
| `running` | Heartbeat 进行中 |
| `error` | 上次 heartbeat 失败 |
| `paused` | 手动暂停或预算超出 |
| `terminated` | 永久停用 |

## 控制 Agent

### 暂停 Agent

临时停止 Agent 的 heartbeat。当 Agent 行为不当或超出预算时使用。

### 恢复 Agent

恢复已暂停 Agent 的 heartbeat。

### 终止 Agent

**永久停用 Agent。这是不可逆的。** 终止的 Agent 不能恢复。

### 手动调用

为 Agent 手动触发 heartbeat。当你想让 Agent 立即开始工作时使用。

## 配置 Agent

Agent 有几个可配置方面：

| 配置 | 说明 |
|------|------|
| **Adapter Config** | 如何运行（CLI、工作目录、timeout 等） |
| **Heartbeat Policy** | 何时唤醒（定时器、分配、按需） |
| **Runtime** | 上下文模式、预算、timeout、env vars |

## 查看 Agent 历史

### 运行历史

在 Agent 详情页查看 heartbeat 运行历史。每次运行显示：
- 运行状态（成功、失败、超时）
- Token 使用
- 成本
- 结果摘要

### 成本追踪

查看 Agent 的累计成本 vs 其预算。

### 活动日志

在活动日志中查看 Agent 的所有操作。
