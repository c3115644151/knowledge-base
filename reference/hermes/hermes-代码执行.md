# 代码执行 (Code Execution)

## 概述

`execute_code` 工具让 Agent 编写和执行 Python 脚本，通过沙箱 RPC 调用 Hermes 工具。

## 基本用法

```python
execute_code(
    script="print('Hello, World!')",
    tools=["terminal", "read_file"]
)
```

## 与委托的区别

| 维度 | execute_code | delegate_task |
|------|--------------|---------------|
| 推理 | 无推理，仅执行 | 完整 LLM 推理 |
| 上下文 | 仅脚本 | 新鲜隔离对话 |
| 工具访问 | 7 个工具 via RPC | 所有非阻止工具 |
| 并行性 | 单脚本 | 最多 3 个并发 |
| Token 成本 | 低 | 高 |

**规则**：需要推理时用 `delegate_task`，需要机械数据处理时用 `execute_code`。

## 可用 RPC 工具

| 工具 | 说明 |
|------|------|
| `terminal` | 执行终端命令 |
| `read_file` | 读取文件 |
| `write_file` | 写入文件 |
| `glob` | 文件搜索 |
| `grep` | 内容搜索 |
| `http_request` | HTTP 请求 |
| `env_get` | 读取环境变量 |

## 使用示例

### 多步骤数据处理
```python
execute_code(
    script="""
import json

# Read data
data = json.loads(read_file('data.json'))

# Process
results = [x for x in data if x['active']]

# Write output
write_file('filtered.json', json.dumps(results, indent=2))
print(f'Processed {len(results)} items')
""",
    tools=["read_file", "write_file"]
)
```

### 带网络请求
```python
execute_code(
    script="""
import urllib.request
import json

response = urllib.request.urlopen('https://api.example.com/data')
data = json.loads(response.read())
print(f'Fetched {len(data)} items')
""",
    tools=["http_request"]
)
```

## 安全机制

### 沙箱执行
代码在隔离环境中执行，无法访问主 Agent 的完整上下文。

### 工具限制
只有明确列出的工具可用，防止意外操作。

### 超时限制
长时间运行的脚本会被终止。

## 配置

```yaml
# ~/.hermes/config.yaml
code_execution:
  timeout: 300        # 秒
  max_output_length: 10000  # 最大输出长度
```

## Python 库

常用库预装在执行环境中：
- `json`, `csv`, `xml` - 数据格式
- `urllib`, `requests` - HTTP 请求
- `os`, `sys`, `pathlib` - 系统操作
- `datetime`, `time` - 时间处理
- `re`, `math`, `random` - 常用工具

如需其他库，考虑使用 `delegate_task` 或在脚本中动态安装。
