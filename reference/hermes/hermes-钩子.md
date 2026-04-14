# 事件钩子 (Hooks)

## 概述

钩子允许在关键生命周期点运行自定义代码，用于日志记录、告警、Webhook 集成等。

## 钩子类型

### 网关钩子 (Gateway Hooks)
- `on_message_received` - 收到消息时
- `on_message_sent` - 发送消息时
- `on_error` - 发生错误时
- `on_startup` - 启动时
- `on_shutdown` - 关闭时

### 插件钩子 (Plugin Hooks)
- `pre_tool_call` - 工具调用前
- `post_tool_call` - 工具调用后
- `on_metrics` - 指标收集时
- `guardrails` - 安全检查

## 钩子目录

```
~/.hermes/hooks/
├── gateway/
│   ├── on_message.py
│   └── on_error.py
└── plugins/
    └── my_guardrail.py
```

## 钩子脚本格式

### Python 脚本
```python
# ~/.hermes/hooks/gateway/on_message.py

def on_message_received(context):
    """
    Called when a message is received.
    
    context contains:
    - platform: str (telegram, discord, etc.)
    - user_id: str
    - message: str
    - session_id: str
    """
    platform = context.get("platform")
    user_id = context.get("user_id")
    message = context.get("message")
    
    print(f"[{platform}] {user_id}: {message}")
    
    return context  # Return modified context
```

### 返回值
- 返回 `context` - 继续处理
- 返回 `None` - 跳过后续处理
- 抛出异常 - 错误处理

## 常用示例

### 日志记录
```python
# ~/.hermes/hooks/gateway/on_message.py
import json
from datetime import datetime

def on_message_received(context):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "platform": context.get("platform"),
        "user_id": context.get("user_id"),
        "message": context.get("message")
    }
    
    with open("/tmp/hermes_messages.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    return context
```

### Slack Webhook 告警
```python
# ~/.hermes/hooks/gateway/on_error.py
import urllib.request

WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

def on_error(context):
    error = context.get("error")
    session_id = context.get("session_id")
    
    payload = {
        "text": f":warning: Hermes Error\nSession: {session_id}\nError: {error}"
    }
    
    data = json.dumps(payload).encode()
    req = urllib.request.Request(WEBHOOK_URL, data=data)
    urllib.request.urlopen(req)
    
    return context
```

### 响应过滤
```python
# ~/.hermes/hooks/gateway/on_message_sent.py

SENSITIVE_PATTERNS = ["password", "api_key", "secret"]

def on_message_sent(context):
    message = context.get("message", "")
    
    for pattern in SENSITIVE_PATTERNS:
        if pattern.lower() in message.lower():
            print(f"[SECURITY] Sensitive pattern detected: {pattern}")
            # 可以选择修改或阻止消息
    
    return context
```

## 插件钩子

### 工具拦截
```python
# ~/.hermes/hooks/plugins/tool_guardrail.py

def pre_tool_call(tool_name, arguments):
    """
    Called before a tool is executed.
    Return modified arguments or raise to block.
    """
    if tool_name == "terminal":
        cmd = arguments.get("command", "")
        if "rm -rf /" in cmd:
            raise ValueError("Blocked dangerous command")
    
    return arguments

def post_tool_call(tool_name, result):
    """
    Called after a tool executes.
    Can modify or log results.
    """
    if tool_name == "terminal":
        print(f"[AUDIT] Terminal command executed: {result}")
    
    return result
```

### 安全护栏
```python
# Guardrails 可以在 Agent 响应前进行检查

def guardrails(response):
    """
    Validate or modify agent response.
    """
    if "internal error" in response.lower():
        return "An error occurred. Please try again."
    return response
```

## 配置

```yaml
# ~/.hermes/config.yaml
hooks:
  enabled: true
  gateway_path: "~/.hermes/hooks/gateway"
  plugin_path: "~/.hermes/hooks/plugins"
```

## 调试

钩子中的错误会记录到日志：
```bash
tail -f ~/.hermes/logs/errors.log
```

使用 `print()` 调试也会显示在输出中。
