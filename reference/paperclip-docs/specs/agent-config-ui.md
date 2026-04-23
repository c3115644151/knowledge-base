# Agent Config UI 规格

> **上下文**: 本规格涵盖三个界面：Agent 创建对话框、Agent 详情页和 Agents 列表页。

## 1. Agent 创建对话框

### 字段

**Identity（始终可见）**

| 字段 | 控制 | 必需 | 默认 |
|------|------|------|------|
| Name | 文本输入 | 是 | - |
| Title | 文本输入 | 否 | - |
| Role | Chip Popover | 否 | `general` |
| Reports To | Chip Popover (Agent 选择) | 否 | - |
| Capabilities | 文本输入 | 否 | - |

**Adapter（可折叠部分，默认展开）**

| 字段 | 控制 | 默认 |
|------|------|------|
| Adapter Type | Chip Popover | `claude_local` |
| Test Environment | Button | - |
| CWD | 文本输入 | - |
| Prompt Template | Textarea | - |
| Model | 文本输入 | - |

**Heartbeat Policy（可折叠部分，默认折叠）**

| 字段 | 控制 | 默认 |
|------|------|------|
| Enabled | Toggle | true |
| Interval (sec) | Number | 300 |
| Wake on Assignment | Toggle | true |
| Wake on On-Demand | Toggle | true |

## 2. Agent 详情页

### Tabs

| Tab | 说明 |
|------|------|
| Overview | 摘要卡和组织位置 |
| Configuration | 可编辑的 adapter/heartbeat/runtime 配置 |
| Runs | 分页的 heartbeat 运行列表 |
| Issues | 分配给此 Agent 的 Issues |
| Costs | 累计成本和预算进度条 |

## 3. Agents 列表页

### 改进

- 添加"New Agent"按钮
- 添加视图切换：列表视图和组织架构视图

### 组织架构视图

- 显示报告层级的树形布局
- 每个节点显示：Agent 名称、角色、状态徽章
- CEO 在顶部，direct reports 在下
