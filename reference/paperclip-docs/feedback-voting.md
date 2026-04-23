# 反馈投票

> **核心摘要**: 当你对 Agent 的响应评分"Helpful"（点赞）或"Needs work"（点踩）时，Paperclip 将你的投票保存在本地。这包括投票和完整的上下文快照（trace bundle）。

## 投票如何工作

1. 点击任何 Agent 评论或文档修订上的 **Helpful** 或 **Needs work**
2. 如果点击 **Needs work**，会出现可选文本提示："What could have been better?" 你可以输入原因或关闭
3. 同意对话框询问是否将投票保存在本地或分享。你的选择会记住以供将来投票

### 存储的内容

每个投票创建两条本地记录：

| 记录 | 包含内容 |
|------|----------|
| **Vote** | 你的投票（up/down）、可选原因文本、分享偏好、同意版本、时间戳 |
| **Trace bundle** | 完整上下文快照：投票的评论/文档修订文本、Issue 标题、Agent 信息、你的投票和原因——理解反馈所需的一切 |

所有数据都在你的本地 Paperclip 数据库中。除非你明确选择分享，否则不会离开你的机器。

## 查看你的投票

### 快速报告（终端）

```bash
pnpm paperclipai feedback report
```

显示颜色编码的摘要：投票计数、每个 trace 的详情（带原因）和导出状态。

### API 端点

所有端点需要 board-user 访问。

**列出 Issue 的投票：**

```bash
curl http://127.0.0.1:3102/api/issues/<issueId>/feedback-votes
```

**列出 Issue 的 trace bundle（带完整 payload）：**

```bash
curl 'http://127.0.0.1:3102/api/issues/<issueId>/feedback-traces?includePayload=true'
```

**列出公司范围的所有 traces：**

```bash
curl 'http://127.0.0.1:3102/api/companies/<companyId>/feedback-traces?includePayload=true'
```

**获取单个 trace envelope 记录：**

```bash
curl http://127.0.0.1:3102/api/feedback-traces/<traceId>
```

**获取 trace 的完整导出 bundle：**

```bash
curl http://127.0.0.1:3102/api/feedback-traces/<traceId>/bundle
```

## 导出你的数据

### 导出到文件 + zip

```bash
pnpm paperclipai feedback export
```

创建带时间戳的目录：

```
feedback-export-20260331T120000Z/
  index.json                    # 带摘要统计的清单
  votes/
    PAP-123-a1b2c3d4.json      # 投票元数据（每个投票一个）
  traces/
    PAP-123-e5f6g7h8.json        # Paperclip 反馈 envelope（每个 trace 一个）
  full-traces/
    PAP-123-e5f6g7h8/
      bundle.json              # trace 的完整导出清单
      ...raw adapter files     # 可用时 codex / claude / opencode session artifacts
feedback-export-20260331T120000Z.zip
```

## 数据生命周期

| 状态 | 含义 |
|------|------|
| `local_only` | 投票保存在本地，未标记分享 |
| `pending` | 标记分享、本地保存、等待立即上传尝试 |
| `sent` | 成功传输 |
| `failed` | 尝试传输但失败；后端可用时重试 |

你的本地数据库始终保留完整投票和 trace 数据，无论分享状态如何。
