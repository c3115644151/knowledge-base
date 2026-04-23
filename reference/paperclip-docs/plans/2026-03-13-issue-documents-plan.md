# Issue 文档计划

> **状态**: 草案 | **日期**: 2026-03-13

## 摘要

为 Paperclip 添加一等**文档**作为可编辑的、有版本控制的、公司范围的文本工件，可链接到 Issue。

第一个必需的约定是 key 为 `plan` 的文档。

## 目标

1. 给予 Issue 一等带键文档，从 `plan` 开始
2. 让文档可由董事会用户和同公司 Issue 访问权限的 Agent 编辑
3. 用仅追加修订保留变更历史
4. 使 `plan` 文档在 Agent/heartbeat 使用的正常 Issue fetch 中自动可用
5. 替换 skills/docs 中当前的 `<plan>`-在-描述 约定
6. 保持设计与未来 artifact/deliverables 层兼容

## 非目标

- 完全协作文档编辑
- 二进制文件版本历史
- 浏览器 IDE 或工作区编辑器
- 同一变更中的完整 artifact-system 实现
- 第一天每个实体类型的广义多态关系

## 推荐数据模型

### 表

#### `documents`

规范文本文档记录。

| 字段 | 类型 |
|------|------|
| `id` | string |
| `company_id` | string |
| `title` | string |
| `format` | string |
| `latest_body` | string |
| `latest_revision_id` | string |
| `latest_revision_number` | number |

#### `document_revisions`

仅追加历史。

| 字段 | 类型 |
|------|------|
| `id` | string |
| `document_id` | string |
| `revision_number` | number |
| `body` | string |

#### `issue_documents`

Issue 关系 + 工作流键。

| 字段 | 类型 |
|------|------|
| `id` | string |
| `issue_id` | string |
| `document_id` | string |
| `key` | string |

## API 端点

| 方法 | 端点 | 说明 |
|------|------|------|
| `GET` | `/api/issues/:issueId/documents` | 列表文档 |
| `GET` | `/api/issues/:issueId/documents/:key` | 按键获取 |
| `PUT` | `/api/issues/:issueId/documents/:key` | 创建或更新 |
| `GET` | `/api/issues/:issueId/documents/:key/revisions` | 修订历史 |

## 实现阶段

1. **共享合约和 schema** — 数据库表、迁移、共享类型
2. **服务器服务和路由** — CRUD 端点、验证
3. **UI Issue 文档界面** — 创建、编辑、历史抽屉
4. **Skills/docs 迁移** — 更新指令远离描述中嵌入的 `<plan>`
5. **遗留兼容** — `<plan>` 块回退读取
