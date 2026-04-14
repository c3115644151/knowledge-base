# 添加工具

为 Hermes Agent 添加自定义工具。

## 何时使用工具 vs 技能

### 使用 Skill（技能）
- 能力可表达为指令 + shell 命令 + 现有工具
- 包装可通过 `terminal` 或 `web_extract` 调用的外部 CLI/API
- 不需要自定义 Python 集成
- 示例：arXiv 搜索、git 工作流、Docker 管理

### 使用 Tool（工具）
- 需要 API 密钥、认证流程的端到端集成
- 需要精确执行的定制处理逻辑
- 处理二进制数据、流或实时事件
- 示例：浏览器自动化、TTS、视觉分析

## 添加工具的三个文件

1. `tools/your_tool.py` - 处理器、schema、检查函数、注册
2. `toolsets.py` - 添加工具名到工具集
3. `model_tools.py` - 添加发现导入

## 步骤一：创建工具文件

```python
# tools/weather_tool.py
"""Weather Tool -- look up current weather for a location."""

import json
import os
import logging

logger = logging.getLogger(__name__)

# --- Availability check ---
def check_weather_requirements() -> bool:
    return bool(os.getenv("WEATHER_API_KEY"))

# --- Handler ---
def weather_tool(location: str, units: str = "metric") -> str:
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return json.dumps({"error": "WEATHER_API_KEY not configured"})
    try:
        # ... call weather API ...
        return json.dumps({"location": location, "temp": 22, "units": units})
    except Exception as e:
        return json.dumps({"error": str(e)})

# --- Schema ---
WEATHER_SCHEMA = {
    "name": "weather",
    "description": "Get current weather for a location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City name or coordinates"
            },
            "units": {
                "type": "string",
                "enum": ["metric", "imperial"],
                "description": "Temperature units",
                "default": "metric"
            }
        },
        "required": ["location"]
    }
}

# --- Registration ---
from tools.registry import registry

registry.register(
    name="weather",
    toolset="weather",
    schema=WEATHER_SCHEMA,
    handler=lambda args, **kw: weather_tool(
        location=args.get("location", ""),
        units=args.get("units", "metric")
    ),
    check_fn=check_weather_requirements,
    requires_env=["WEATHER_API_KEY"],
)
```

## 关键规则

> ⚠️ **关键**：
> - 处理器**必须**返回 JSON 字符串（通过 `json.dumps()`）
> - 错误**必须**返回为 `{"error": "message"}`，不能抛出异常
> - `check_fn` 返回 `False` 时工具静默排除

## 步骤二：添加到工具集

```python
# toolsets.py

# 如果应该在所有平台可用（CLI + 消息）
_HERMES_CORE_TOOLS = [
    ...
    "weather",  # 添加到这里
]

# 或创建新工具集
"weather": {
    "description": "Weather lookup tools",
    "tools": ["weather"],
    "includes": []
},
```

## 步骤三：添加发现导入

```python
# model_tools.py

def _discover_tools():
    _modules = [
        ...
        "tools.weather_tool",  # 添加到这里
    ]
```

## 异步处理器

```python
async def weather_tool_async(location: str) -> str:
    async with aiohttp.ClientSession() as session:
        ...
    return json.dumps(result)

registry.register(
    name="weather",
    toolset="weather",
    schema=WEATHER_SCHEMA,
    handler=lambda args, **kw: weather_tool_async(args.get("location", "")),
    check_fn=check_weather_requirements,
    is_async=True,  # registry 自动调用 _run_async()
)
```

## 需要 task_id 的处理器

```python
def _handle_weather(args, **kw):
    task_id = kw.get("task_id")
    return weather_tool(args.get("location", ""), task_id=task_id)

registry.register(
    name="weather",
    ...
    handler=_handle_weather,
)
```

## 设置向导集成

添加 API 密钥到配置提示：

```python
# hermes_cli/config.py

OPTIONAL_ENV_VARS = {
    ...
    "WEATHER_API_KEY": {
        "description": "Weather API key for weather lookup",
        "prompt": "Weather API key",
        "url": "https://weatherapi.com/",
        "tools": ["weather"],
        "password": True,
    },
}
```

## 检查清单

- [ ] 工具文件包含处理器、schema、检查函数、注册
- [ ] 添加到 `toolsets.py` 的适当工具集
- [ ] 发现导入添加到 `model_tools.py`
- [ ] 处理器返回 JSON 字符串，错误返回 `{"error": "..."}`
- [ ] 可选：API 密钥添加到 `OPTIONAL_ENV_VARS`
- [ ] 测试：`hermes chat -q "Use the weather tool for London"`
