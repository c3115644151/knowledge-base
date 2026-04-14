# 插件系统

Hermes 拥有插件系统，可添加自定义工具、钩子和集成而无需修改核心代码。

## 快速概述

将目录放入 `~/.hermes/plugins/`，包含 `plugin.yaml` 和 Python 代码：

```
~/.hermes/plugins/my-plugin/
├── plugin.yaml    # 清单
├── __init__.py    # register() — 连接 schema 到处理器
├── schemas.py     # 工具 schema（LLM 看到的）
└── tools.py       # 工具处理器（运行时调用的）
```

## 最小示例

**`~/.hermes/plugins/hello-world/plugin.yaml`**
```yaml
name: hello-world
version: "1.0"
description: A minimal example plugin
```

**`~/.hermes/plugins/hello-world/__init__.py`**
```python
def register(ctx):
    # --- Tool: hello_world ---
    schema = {
        "name": "hello_world",
        "description": "Returns a friendly greeting for the given name.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name to greet"}
            },
            "required": ["name"]
        }
    }
    def handle_hello(params):
        name = params.get("name", "World")
        return f"Hello, {name}! 👋 (from the hello-world plugin)"
    ctx.register_tool("hello_world", schema, handle_hello)
    
    # --- Hook: log every tool call ---
    def on_tool_call(tool_name, params, result):
        print(f"[hello-world] tool called: {tool_name}")
    ctx.register_hook("post_tool_call", on_tool_call)
```

## 插件能力

| 能力 | 方法 |
|------|------|
| 添加工具 | `ctx.register_tool(name, schema, handler)` |
| 添加钩子 | `ctx.register_hook("post_tool_call", callback)` |
| 添加 CLI 命令 | `ctx.register_cli_command(name, help, setup_fn, handler_fn)` |
| 注入消息 | `ctx.inject_message(content, role="user")` |
| 附带数据文件 | `Path(__file__).parent / "data" / "file.yaml"` |
| 打包技能 | 加载时复制 `skill.md` 到 `~/.hermes/skills/` |
| 环境变量门控 | `requires_env: [API_KEY]` 在 plugin.yaml 中 |

## 可用钩子

| 钩子 | 触发时机 |
|------|----------|
| `pre_tool_call` | 任何工具执行前 |
| `post_tool_call` | 任何工具返回后 |
| `pre_llm_call` | 每轮一次，LLM 循环前 — 可返回 `{"context": "..."}` 注入上下文 |
| `post_llm_call` | 每轮一次，LLM 循环后（仅成功轮次） |
| `on_session_start` | 创建新会话时（仅首次） |
| `on_session_end` | 每次 `run_conversation` 结束时 |

## 插件类型

| 类型 | 作用 | 选择 | 位置 |
|------|------|------|------|
| **通用插件** | 添加工具、钩子、CLI 命令 | 多选（启用/禁用） | `~/.hermes/plugins/` |
| **内存提供者** | 替换或增强内置记忆 | 单选（一个活动） | `plugins/memory/` |
| **上下文引擎** | 替换内置上下文压缩器 | 单选（一个活动） | `plugins/context_engine/` |

## 管理命令

```bash
hermes plugins                    # 统一交互式 UI
hermes plugins list              # 表格视图 + 启用/禁用状态
hermes plugins install user/repo # 从 Git 安装
hermes plugins update my-plugin  # 拉取最新
hermes plugins remove my-plugin   # 卸载
hermes plugins enable my-plugin  # 重新启用
hermes plugins disable my-plugin  # 禁用（不移除）
```

## 消息注入

插件可使用 `ctx.inject_message()` 注入消息到活动对话：

```python
ctx.inject_message("New data arrived from the webhook", role="user")
```

- 如果代理**空闲** — 消息作为下一个输入排队
- 如果代理**运行中** — 消息中断当前操作
