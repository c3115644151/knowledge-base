# 工具与工具集

## 概述

工具 (Tools) 是扩展 Hermes Agent 能力的函数，使其能够执行实际操作。工具按功能逻辑分组为**工具集 (Toolsets)**。

## 工具集分类

### Core Toolsets

| 工具集 | 功能 | 常用工具 |
|--------|------|----------|
| `terminal` | 文件和命令操作 | `read_file`, `write_file`, `terminal`, `glob` |
| `web` | 网络访问 | `web_search`, `web_extract`, `browser_navigate` |
| `memory` | 持久化存储 | `memory_remember`, `memory_recall`, `memory_forget` |
| `skills` | 技能管理 | `skill_view`, `skill_install`, `skill_search` |
| `delegation` | 子代理 | `delegate_task` |
| `code_execution` | Python RPC | `execute_code` |
| `send_message` | 消息发送 | `send_message` |
| `mcp` | MCP 工具 | `mcp_*` (前缀+工具名) |

### 工具集配置

```bash
# 指定工具集
hermes chat --toolsets "web,terminal,skills"

# 启用/禁用
hermes tools
```

## 内置工具参考

### 文件操作
| 工具 | 说明 | 参数 |
|------|------|------|
| `read_file` | 读取文件 | `path`, `offset`, `limit` |
| `write_file` | 写入文件 | `path`, `content` |
| `edit_file` | 编辑文件 | `path`, `old_string`, `new_string` |
| `glob` | 文件搜索 | `pattern`, `cwd` |
| `grep` | 内容搜索 | `pattern`, `path`, `options` |

### 终端命令
| 工具 | 说明 | 参数 |
|------|------|------|
| `terminal` | 执行命令 | `command`, `cwd`, `timeout` |
| `kill` | 终止进程 | `process_id` |

### Web 操作
| 工具 | 说明 | 参数 |
|------|------|------|
| `web_search` | 搜索网页 | `query`, `recency_days` |
| `web_extract` | 提取内容 | `url`, `query` |
| `browser_navigate` | 浏览器导航 | `url`, `action` |
| `browser_screenshot` | 截屏 | `url` |

### 记忆系统
| 工具 | 说明 |
|------|------|
| `memory_remember` | 存储重要信息 |
| `memory_recall` | 检索相关信息 |
| `memory_forget` | 删除记忆 |
| `honcho_conclude` | Honcho 推理 |

### 技能管理
| 工具 | 说明 |
|------|------|
| `skill_view` | 查看技能详情 |
| `skill_install` | 安装技能 |
| `skill_uninstall` | 卸载技能 |
| `skill_search` | 搜索技能 |

### 委托与执行
| 工具 | 说明 | 参数 |
|------|------|------|
| `delegate_task` | 委托子代理 | `goal`, `context`, `toolsets` |
| `execute_code` | 执行 Python | `script`, `tools` |

## MCP 工具

MCP 服务器的工具以 `mcp_<server>_<tool>` 前缀注册：

```
filesystem_server → mcp_filesystem_read_file
github_server     → mcp_github_create_issue
```

## 配置示例

### config.yaml 工具设置
```yaml
tools:
  enabled: true
  toolsets:
    - terminal
    - web
    - memory
    - skills
```

### 工具预览长度
```yaml
display:
  tool_preview_length: 80  # 截断工具预览到 80 字符
```

## 安全机制

### 危险命令审批
触发审批的命令模式：
- `rm -rf` - 递归删除
- `chmod 777` - 不安全权限
- `DROP TABLE` - SQL 删除
- `curl ... | sh` - 远程执行
- `> /etc/` - 系统文件覆盖

### 沙箱隔离
使用 `docker`/`modal`/`singularity` 后端时跳过审批（容器本身是安全边界）。

## 工具与技能的区别

| 维度 | 工具 (Tools) | 技能 (Skills) |
|------|-------------|---------------|
| 本质 | 可执行函数 | 知识文档 |
| 调用 | Agent 自动调用 | 按需加载到上下文 |
| 用途 | 执行操作 | 提供复杂任务指导 |
| 编写 | Python 代码 | Markdown 格式 |

**技能** 是告诉 Agent **如何做** 的知识，**工具** 是 Agent **实际执行** 的能力。
