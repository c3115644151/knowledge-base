# Python 库指南

将 Hermes Agent 作为 Python 库集成到自己的应用中。

## 安装

```bash
pip install git+https://github.com/NousResearch/hermes-agent.git
# 或
uv pip install git+https://github.com/NousResearch/hermes-agent.git
```

## 基本用法

```python
from run_agent import AIAgent

agent = AIAgent(
    model="anthropic/claude-sonnet-4",
    quiet_mode=True,
)

response = agent.chat("What is the capital of France?")
print(response)
```

> ⚠️ 嵌入自己的代码时始终设置 `quiet_mode=True`。

## 完整对话控制

```python
agent = AIAgent(
    model="anthropic/claude-sonnet-4",
    quiet_mode=True,
)

result = agent.run_conversation(
    user_message="Search for recent Python 3.13 features",
    task_id="my-task-1",
)

print(result["final_response"])
print(f"Messages exchanged: {len(result['messages'])}")
```

返回字典包含：
- `final_response` - 最终文本回复
- `messages` - 完整消息历史
- `task_id` - 任务标识符

## 配置工具

```python
# 仅启用 web 工具
agent = AIAgent(
    model="anthropic/claude-sonnet-4",
    enabled_toolsets=["web"],
    quiet_mode=True,
)

# 禁用终端访问
agent = AIAgent(
    model="anthropic/claude-sonnet-4",
    disabled_toolsets=["terminal"],
    quiet_mode=True,
)
```

## 多轮对话

```python
# 第一轮
result1 = agent.run_conversation("My name is Alice")
history = result1["messages"]

# 第二轮 - 代理记住上下文
result2 = agent.run_conversation(
    "What's my name?",
    conversation_history=history,
)
```

## 保存轨迹

```python
agent = AIAgent(
    model="anthropic/claude-sonnet-4",
    save_trajectories=True,
    quiet_mode=True,
)

agent.chat("Write a Python function to sort a list")
# 保存到 trajectory_samples.jsonl (ShareGPT 格式)
```

## 自定义系统提示

```python
agent = AIAgent(
    model="anthropic/claude-sonnet-4",
    ephemeral_system_prompt="You are a SQL expert. Only answer database questions.",
    quiet_mode=True,
)
```

## 批处理

```python
import concurrent.futures
from run_agent import AIAgent

prompts = ["Explain recursion", "What is a hash table?", "How does garbage collection work?"]

def process_prompt(prompt):
    agent = AIAgent(
        model="anthropic/claude-sonnet-4",
        quiet_mode=True,
        skip_memory=True,
    )
    return agent.chat(prompt)

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(process_prompt, prompts))
```

> ⚠️ 始终为每个线程/任务创建**新的 AIAgent 实例**。

## 集成示例

### FastAPI 端点
```python
from fastapi import FastAPI
from pydantic import BaseModel
from run_agent import AIAgent

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    model: str = "anthropic/claude-sonnet-4"

@app.post("/chat")
async def chat(request: ChatRequest):
    agent = AIAgent(
        model=request.model,
        quiet_mode=True,
        skip_context_files=True,
        skip_memory=True,
    )
    response = agent.chat(request.message)
    return {"response": response}
```

### CI/CD Pipeline
```python
#!/usr/bin/env python3
"""CI step: auto-review a PR diff."""
import subprocess
from run_agent import AIAgent

diff = subprocess.check_output(["git", "diff", "main...HEAD"]).decode()

agent = AIAgent(
    model="anthropic/claude-sonnet-4",
    quiet_mode=True,
    skip_context_files=True,
    skip_memory=True,
    disabled_toolsets=["terminal", "browser"],
)

review = agent.chat(f"Review this PR diff for bugs and security issues:\n\n{diff}")
print(review)
```

## 构造函数参数

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `model` | str | anthropic/claude-opus-4.6 | OpenRouter 格式的模型 |
| `quiet_mode` | bool | False | 静默模式 |
| `enabled_toolsets` | List[str] | None | 启用的工具集 |
| `disabled_toolsets` | List[str] | None | 禁用的工具集 |
| `save_trajectories` | bool | False | 保存轨迹 |
| `ephemeral_system_prompt` | str | None | 临时系统提示 |
| `max_iterations` | int | 90 | 最大迭代次数 |
| `skip_context_files` | bool | False | 跳过 AGENTS.md |
| `skip_memory` | bool | False | 禁用持久记忆 |
| `api_key` | str | None | API key |
| `base_url` | str | None | 自定义端点 |
| `platform` | str | None | 平台提示 |

## 注意事项

- `skip_context_files=True` - 不加载工作目录的 AGENTS.md
- `skip_memory=True` - 禁用持久记忆读写
- `platform` 参数注入平台格式提示
- 线程安全：每个线程/任务一个实例
- `max_iterations=10` 可防止简单 Q&A 用例的失控
