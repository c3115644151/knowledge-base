# 凭证池

凭证池允许为同一提供商注册多个 API 密钥或 OAuth 令牌。当一个密钥达到速率限制或配额时，Hermes 自动轮换到下一个健康密钥。

这与[回退提供商](hermes-回退提供商.md)不同——凭证池是同一提供商轮换；回退是跨提供商故障转移。

## 工作原理

```
请求 → 从池中选择密钥 (round_robin / least_used / fill_first / random)
      → 发送到提供商
      → 429 速率限制?
        → 重试同一密钥一次（瞬时抖动）
        → 第二次 429 → 轮换到下一个池密钥
      → 所有密钥耗尽 → fallback_model (不同提供商)
      → 402 计费错误?
        → 立即轮换到下一个密钥 (24h 冷却)
      → 401 认证过期?
        → 尝试刷新 OAuth 令牌
        → 刷新失败 → 轮换到下一个密钥
      → 成功 → 正常继续
```

## 快速开始

已有 `.env` 中的 API 密钥？自动发现为 1 密钥池。要受益于池化，添加更多密钥：

```bash
# 添加第二个 OpenRouter 密钥
hermes auth add openrouter --api-key sk-or-v1-your-second-key

# 添加第二个 Anthropic 密钥
hermes auth add anthropic --type api-key --api-key sk-ant-api03-your-second-key

# 添加 Anthropic OAuth 凭证
hermes auth add anthropic --type oauth
```

检查池：
```bash
hermes auth list
```

## CLI 命令

| 命令 | 描述 |
|------|------|
| `hermes auth` | 交互式池管理向导 |
| `hermes auth list` | 显示所有池和凭证 |
| `hermes auth add <provider>` | 添加凭证 |
| `hermes auth remove <provider> <index>` | 按索引移除凭证 |
| `hermes auth reset <provider>` | 清除所有冷却/耗尽状态 |

## 轮换策略

```yaml
credential_pool_strategies:
  openrouter: round_robin
  anthropic: least_used
```

| 策略 | 行为 |
|------|------|
| `fill_first`（默认） | 使用第一个健康密钥直到耗尽，然后移动到下一个 |
| `round_robin` | 均匀轮换密钥 |
| `least_used` | 始终选择请求计数最低的密钥 |
| `random` | 在健康密钥中随机选择 |

## 错误恢复

| 错误 | 行为 | 冷却 |
|------|------|------|
| **429 速率限制** | 重试同一密钥一次。第二次连续 429 轮换到下一个密钥 | 1 小时 |
| **402 计费/配额** | 立即轮换到下一个密钥 | 24 小时 |
| **401 认证过期** | 尝试刷新 OAuth 令牌。刷新失败则轮换 | — |

## 自动发现

| 来源 | 自动种子? |
|------|----------|
| 环境变量 | 是 |
| OAuth 令牌 (auth.json) | 是 |
| Claude Code 凭证 | 是 (Anthropic) |
| Hermes PKCE OAuth | 是 (Anthropic) |
| 自定义端点配置 | 是 |

## 委托与子代理

通过 `delegate_task` 生成子代理时，父代理的凭证池自动共享给子代理：
- **同一提供商** — 子代理收到父代理的完整池
- **不同提供商** — 子代理加载该提供商自己的池
- **无池配置** — 子代理回退到继承的单一 API 密钥
