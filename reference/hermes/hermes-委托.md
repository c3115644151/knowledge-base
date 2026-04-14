# 子代理委托 (Delegation)

## 概述

`delegate_task` 工具生成子 AIAgent 实例，具有隔离的上下文、限制的工具集和自己的终端会话。

## 基本用法

### 单任务委托
```python
delegate_task(
    goal="Debug why tests fail",
    context="Error: assertion in test_foo.py line 42",
    toolsets=["terminal", "file"]
)
```

### 并行批量委托
最多 3 个并发子代理：
```python
delegate_task(tasks=[
    {"goal": "Research topic A", "toolsets": ["web"]},
    {"goal": "Research topic B", "toolsets": ["web"]},
    {"goal": "Fix the build", "toolsets": ["terminal", "file"]}
])
```

## 关键特性

### 隔离上下文
子代理从**完全新鲜的对话**开始，没有父代理的任何对话历史。

```python
# ❌ 错误 - 子代理不知道 "error" 是什么
delegate_task(goal="Fix the error")

# ✅ 正确 - 提供完整上下文
delegate_task(
    goal="Fix the TypeError in api/handlers.py",
    context="""The file api/handlers.py has a TypeError on line 47:
'NoneType' object has no attribute 'get'.
The function process_request() receives a dict from parse_body(),
but parse_body() returns None when Content-Type is missing."""
)
```

### 配置子代理模型
使用更便宜/更快的模型处理简单任务：
```yaml
# ~/.hermes/config.yaml
delegation:
  model: "google/gemini-flash-2.0"
  provider: "openrouter"
```

## 工具集选择

| 工具集模式 | 用途 |
|-----------|------|
| `["terminal", "file"]` | 代码工作、调试、文件编辑 |
| `["web"]` | 研究、事实核查 |
| `["terminal", "file", "web"]` | 全栈任务 |
| `["file"]` | 只读分析、代码审查 |
| `["terminal"]` | 系统管理 |

### 始终阻止的工具
- `delegation` - 防止递归委托
- `clarify` - 子代理不能与用户交互
- `memory` - 不写入共享持久记忆
- `code_execution` - 子代理应逐步推理
- `send_message` - 防止跨平台副作用

## 配置

```yaml
# ~/.hermes/config.yaml
delegation:
  max_iterations: 50                    # 子代理最大迭代次数
  default_toolsets: ["terminal", "file", "web"]
  model: "google/gemini-3-flash-preview"
  provider: "openrouter"

# 或使用自定义端点
delegation:
  model: "qwen2.5-coder"
  base_url: "http://localhost:1234/v1"
  api_key: "local-key"
```

## 委托 vs execute_code

| 维度 | delegate_task | execute_code |
|------|---------------|--------------|
| 推理 | 完整 LLM 推理循环 | 仅 Python 代码执行 |
| 上下文 | 新鲜隔离对话 | 仅脚本，无对话 |
| 工具访问 | 所有非阻止工具 + 推理 | 7 个工具 via RPC，无推理 |
| 并行性 | 最多 3 个并发子代理 | 单脚本 |
| 适用场景 | 需要判断的复杂任务 | 机械数据处理 |
| Token 成本 | 较高 | 较低 |

**经验法则**：需要推理、判断或多步骤问题解决时使用 `delegate_task`。需要机械数据处理或脚本工作流时使用 `execute_code`。

## 实际示例

### 并行研究
```python
delegate_task(tasks=[
    {"goal": "Research WebAssembly in 2025",
     "context": "Focus: browser support, runtimes, language support",
     "toolsets": ["web"]},
    {"goal": "Research RISC-V adoption in 2025",
     "context": "Focus: server chips, embedded, ecosystem",
     "toolsets": ["web"]},
    {"goal": "Research quantum computing progress",
     "context": "Focus: error correction, applications, key players",
     "toolsets": ["web"]}
])
```

### 代码审查 + 修复
```python
delegate_task(
    goal="Review auth module for security issues and fix any found",
    context="""Project at /home/user/webapp.
Auth files: src/auth/login.py, src/auth/jwt.py, src/auth/middleware.py.
Uses Flask, PyJWT, bcrypt.
Focus on: SQL injection, JWT validation, password handling.""",
    toolsets=["terminal", "file"]
)
```

## 限制

- 最大并发：3 个子代理
- 最大深度：2 (父 = 0, 子 = 1; 子不能再委托)
- 每次最多迭代：50 (可配置)
