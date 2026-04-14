# 日报 Bot 教程

构建自动化的每日简报 Bot。

## 构建内容

每天定时：
1. 触发 cron 调度器
2. 启动 fresh agent 会话
3. 网络搜索最新资讯
4. 摘要成简报格式
5. 投递到 Telegram/Discord

## 前置条件

- Hermes Agent 已安装
- Gateway 运行中
- Firecrawl API Key（用于网络搜索）
- 消息平台已配置（推荐）

## 步骤一：手动测试工作流

```bash
hermes
```

输入：
```
Search for the latest news about AI agents and open source LLMs.
Summarize the top 3 stories in a concise briefing format with links.
```

输出示例：
```
☀️ Your AI Briefing — March 8, 2026

1. Qwen 3 Released with 235B Parameters
   → https://qwenlm.github.io/blog/qwen3/

2. LangChain Launches Agent Protocol Standard
   → https://blog.langchain.dev/agent-protocol/

3. EU AI Act Enforcement Begins
   → https://artificialintelligenceact.eu/updates/
```

## 步骤二：创建 Cron Job

### 方式一：自然语言
```
Every morning at 8am, search the web for the latest news about AI agents
and open source LLMs. Summarize the top 3 stories in a concise briefing
with links. Use a friendly, professional tone. Deliver to telegram.
```

### 方式二：CLI 斜杠命令
```
/cron add "0 8 * * *" "Search the web for the latest news about AI agents and open source LLMs. Find at least 5 recent articles from the past 24 hours. Summarize the top 3 most important stories in a concise daily briefing format. For each story include: a clear headline, a 2-sentence summary, and the source URL. Use a friendly, professional tone."
```

## 黄金法则：自包含提示

**关键**：Cron job 在**全新会话**中运行，无记忆。

### 坏提示
```
Do my usual morning briefing.
```

### 好提示
```
Search the web for the latest news about AI agents and open source LLMs.
Find at least 5 recent articles from the past 24 hours. Summarize the
top 3 most important stories in a concise daily briefing format. For each
story include: a clear headline, a 2-sentence summary, and the source URL.
Use a friendly, professional tone. Format with emoji bullet points.
```

## 步骤三：自定义简报

### 多主题简报
```
/cron add "0 8 * * *" "Create a morning briefing covering three topics. For each topic, search the web for recent news from the past 24 hours and summarize the top 2 stories with links.

Topics:
1. AI and machine learning — focus on open source models and agent frameworks
2. Cryptocurrency — focus on Bitcoin, Ethereum, and regulatory news
3. Space exploration — focus on SpaceX, NASA, and commercial space

Format as a clean briefing with section headers and emoji. End with today's date."
```

### 使用 Delegation 并行研究
```
/cron add "0 8 * * *" "Create a morning briefing by delegating research to sub-agents. Delegate three parallel tasks:
1. Delegate: Search for the top 2 AI/ML news stories from the past 24 hours with links
2. Delegate: Search for the top 2 cryptocurrency news stories from the past 24 hours with links
3. Delegate: Search for the top 2 space exploration news stories from the past 24 hours with links

Collect all results and combine them into a single clean briefing with section headers and emoji formatting."
```

### 仅工作日
```
/cron add "0 8 * * 1-5" "Search for the latest AI and tech news..."
```

### 每日两次
```
/cron add "0 8 * * *" "Morning briefing: search for AI news from the past 12 hours..."
/cron add "0 18 * * *" "Evening recap: search for AI news from the past 12 hours..."
```

## 管理 Jobs

### 列出所有任务
```bash
/cron list
# 或
hermes cron list
```

### 删除任务
```bash
/cron remove <job_id>
```

### 检查状态
```bash
hermes cron status
```

## 更多场景

简报 Bot 模式适用于：
- 竞争对手监控
- GitHub 仓库摘要
- 天气查询
- 投资组合跟踪
- 服务器健康检查
- 每日笑话
