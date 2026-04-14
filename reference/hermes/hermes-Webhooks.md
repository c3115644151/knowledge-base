# Webhooks

接收外部服务（GitHub、GitLab、JIRA、Stripe 等）的事件并触发 Agent 运行。

## 架构

```
外部服务 → Webhook POST → Hermes Gateway → Agent 处理 → 投递响应
```

## 快速开始

### 1. 启用 Webhook

```bash
hermes gateway setup
# 选择 Webhook，设置端口和 HMAC secret
```

或手动配置（`~/.hermes/.env`）：
```bash
WEBHOOK_ENABLED=true
WEBHOOK_PORT=8644
WEBHOOK_SECRET=your-global-secret
```

### 2. 验证服务器
```bash
curl http://localhost:8644/health
# 返回: {"status": "ok", "platform": "webhook"}
```

## 配置路由

在 `config.yaml` 中定义：
```yaml
platforms:
  webhook:
    enabled: true
    extra:
      port: 8644
      secret: "global-fallback-secret"
      routes:
        github-pr:
          events: ["pull_request"]
          secret: "github-webhook-secret"
          prompt: |
            Review this pull request:
            Repository: {repository.full_name}
            PR #{number}: {pull_request.title}
            Author: {pull_request.user.login}
            URL: {pull_request.html_url}
          skills: ["github-code-review"]
          deliver: "github_comment"
          deliver_extra:
            repo: "{repository.full_name}"
            pr_number: "{number}"
```

### 路由属性

| 属性 | 必需 | 说明 |
|------|------|------|
| `events` | — | 事件类型列表（如 `["pull_request"]`） |
| `secret` | ✅ | HMAC 签名验证 secret |
| `prompt` | — | 模板字符串 |
| `skills` | — | 加载的技能列表 |
| `deliver` | — | 响应投递目标 |
| `deliver_extra` | — | 投递配置 |

### 模板语法

- `{pull_request.title}` - 嵌套字段访问
- `{__raw__}` - 整个 payload（最多 4000 字符）
- 缺失的键保留字面量 `{key}`

### 投递目标

| 类型 | 说明 |
|------|------|
| `log` | 记录到 gateway 日志 |
| `github_comment` | 通过 `gh` CLI 发布 PR 评论 |
| `telegram` | 投递到 Telegram |
| `discord` | 投递到 Discord |
| `slack` | 投递到 Slack |
| 其他 | signal, sms, whatsapp, matrix, mattermost, email, dingtalk, feishu, wecom, weixin, bluebubbles |

## GitHub PR 审查配置

### 1. 创建 Webhook
1. 仓库 → Settings → Webhooks → Add webhook
2. Payload URL: `http://your-server:8644/webhooks/github-pr`
3. Content type: `application/json`
4. Secret: 匹配路由配置
5. 事件：选择 **Pull requests**

### 2. 确保 `gh` CLI 已认证
```bash
gh auth login
```

## CLI 动态订阅

### 创建订阅
```bash
hermes webhook subscribe github-issues \
  --events "issues" \
  --prompt "New issue: {issue.title}\nBy: {issue.user.login}" \
  --deliver telegram \
  --deliver-chat-id "-100123456789"
```

### 管理订阅
```bash
hermes webhook list
hermes webhook remove github-issues
hermes webhook test github-issues
```

订阅存储在 `~/.hermes/webhook_subscriptions.json`。

## 安全

### HMAC 签名验证
- **GitHub**: `X-Hub-Signature-256` header
- **GitLab**: `X-Gitlab-Token` header（纯字符串匹配）
- **通用**: `X-Webhook-Signature` header

### 速率限制
每路由每分钟 30 请求（可配置）。

### Idempotency
使用 `X-GitHub-Delivery` 或 `X-Request-ID` 缓存 1 小时，防止重复处理。

## 环境变量

| 变量 | 默认 | 说明 |
|------|------|------|
| `WEBHOOK_ENABLED` | false | 启用 webhook |
| `WEBHOOK_PORT` | 8644 | HTTP 端口 |
| `WEBHOOK_SECRET` | — | 全局 HMAC secret |
