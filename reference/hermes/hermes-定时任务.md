# 定时任务 (Cron)

## 概述

使用自然语言或 Cron 表达式安排任务自动运行。

## 基本用法

### 自然语言调度
```
"Every morning at 9am, check Hacker News for AI news and send me a summary on Telegram"
```

### Cron 表达式
```
"0 9 * * *"  # 每天 9:00
"*/15 * * * *"  # 每 15 分钟
"0 */2 * * *"  # 每 2 小时
```

## 安装 Cron 支持

```bash
pip install "hermes-agent[cron]"
```

## 命令

| 命令 | 说明 |
|------|------|
| `hermes cron list` | 列出所有定时任务 |
| `hermes cron show <id>` | 查看任务详情 |
| `hermes cron pause <id>` | 暂停任务 |
| `hermes cron resume <id>` | 恢复任务 |
| `hermes cron edit <id>` | 编辑任务 |
| `hermes cron delete <id>` | 删除任务 |

## 配置

```yaml
# ~/.hermes/config.yaml
cron:
  enabled: true
  max_concurrent: 3      # 最大并发任务数
  default_skill: ""      # 预加载的技能
  default_toolsets: []    # 默认工具集
```

## Cron 文件存储

```
~/.hermes/cron/
├── jobs.json           # 任务定义
└── logs/              # 执行日志
```

## 与网关集成

定时任务通过网关运行，可以：
- 发送结果到任意平台
- 访问连接的消息服务
- 使用网关的认证状态

## 最佳实践

1. **清晰的任务描述** - 帮助 Agent 理解任务目标
2. **合理的频率** - 避免过于频繁的调用
3. **错误处理** - Agent 会记录错误并继续
4. **资源限制** - 使用 `max_concurrent` 控制并发

## 高级路由

### `deliver=all` — 全平台推送

v0.13.x 新增。定时任务支持 `deliver=all` 特殊值，将任务结果推送到所有已连接的消息平台：

```
cronjob(action="create", name="daily-news",
        schedule="every day 7am",
        deliver="all",
        prompt="...")
```

可组合使用：`"origin,all"`、`"all,telegram:-100:17"`

### `context_from` — 任务链

定时任务可以消费其他任务的最新输出：

```
cronjob(action="create", name="daily-digest",
        schedule="every day 7am",
        context_from=["ai-news-fetch", "github-prs-fetch"],
        prompt="Write the daily digest using the outputs above.")
```

引用的是最近一次成功执行的输出，不是同批次运行中的输出。

### `wakeAgent` — 跳过 Agent 调用

配合 pre-check 脚本使用。通过 stdout 输出 `{"wakeAgent": false}` 可以跳过 Agent 调用，适合高频轮询场景：

```python
import json, sys
latest = fetch_latest_count()
prev = read_state("count")
if latest == prev:
    print(json.dumps({"wakeAgent": False}))
    sys.exit(0)
write_state("count", latest)
print(json.dumps({"wakeAgent": True, "context": {"new": latest - prev}}))
```

## 安全

定时任务在创建和更新时会扫描提示词注入和凭证泄露模式。包含不可见 Unicode 陷阱、SSH 后门尝试或明显凭证泄露载荷的提示词会被拦截。
