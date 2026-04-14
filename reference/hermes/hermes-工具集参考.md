# 工具集参考

工具集是控制代理能做什么的命名工具包。它们是按平台、会话或任务配置工具可用性的主要机制。

## 工具集工作方式

每个工具精确属于一个工具集。启用工具集时，该包中所有工具对代理可用。工具集有三种：

- **Core（核心）** — 单个逻辑相关工具组（如 `file` 包含 `read_file`, `write_file`, `patch`, `search_files`）
- **Composite（组合）** — 组合多个核心工具集（如 `debugging` 包含 file、terminal、web 工具）
- **Platform（平台）** — 特定部署上下文的完整工具配置（如 `hermes-cli` 是交互式 CLI 会话的默认配置）

## 配置工具集

### 按会话（CLI）

```bash
hermes chat --toolsets web,file,terminal
hermes chat --toolsets debugging  # composite — 展开为 file + terminal + web
hermes chat --toolsets all        # 所有工具
```

### 按平台（config.yaml）

```yaml
toolsets:
  - hermes-cli           # CLI 默认
  # - hermes-telegram    # Telegram 网关覆盖
```

### 交互式管理

```bash
/tools list
/tools disable browser
/tools enable rl
```

## 核心工具集

| 工具集 | 工具 | 用途 |
|--------|------|------|
| `browser` | browser_*, web_search | 完整浏览器自动化 |
| `clarify` | clarify | 需要澄清时向用户提问 |
| `code_execution` | execute_code | 运行调用 Hermes 工具的 Python 脚本 |
| `cronjob` | cronjob | 安排和管理定期任务 |
| `delegation` | delegate_task | 生成隔离子代理实例 |
| `file` | patch, read_file, search_files, write_file | 文件读取、写入、搜索、编辑 |
| `homeassistant` | ha_* | 通过 Home Assistant 控制智能家居 |
| `image_gen` | image_generate | 通过 FAL.ai 文本生成图像 |
| `memory` | memory | 持久跨会话记忆管理 |
| `messaging` | send_message | 发送到其他平台 |
| `moa` | mixture_of_agents | 通过多模型共识 |
| `rl` | rl_* | RL 训练环境管理 |
| `search` | web_search | 仅网页搜索 |
| `session_search` | session_search | 搜索过去对话会话 |
| `skills` | skill_manage, skill_view, skills_list | 技能浏览 |
| `terminal` | process, terminal | Shell 命令执行 |
| `todo` | todo | 会话内任务列表管理 |
| `tts` | text_to_speech | 文本转语音生成 |
| `vision` | vision_analyze | 通过视觉模型图像分析 |
| `web` | web_extract, web_search | 网页搜索和页面内容提取 |

## 组合工具集

| 工具集 | 展开为 | 用途 |
|--------|--------|------|
| `debugging` | file + terminal + web | 调试会话 |
| `safe` | image_gen + vision + web | 只读研究和媒体生成。无文件写入、终端访问、代码执行 |

## 平台工具集

| 工具集 | 与 `hermes-cli` 的差异 |
|--------|------------------------|
| `hermes-cli` | 完整工具集 — 默认 |
| `hermes-acp` | 丢弃 clarify、cronjob、image_generate、send_message、tts、homeassistant |
| `hermes-api-server` | 丢弃 clarify、send_message、tts |
| `hermes-telegram` | 同 hermes-cli |
| `hermes-discord` | 同 hermes-cli |
| `hermes-slack` | 同 hermes-cli |
| `hermes-whatsapp` | 同 hermes-cli |
| `hermes-signal` | 同 hermes-cli |
| `hermes-matrix` | 同 hermes-cli |
| `hermes-mattermost` | 同 hermes-cli |
| `hermes-email` | 同 hermes-cli |
| `hermes-sms` | 同 hermes-cli |
| `hermes-dingtalk` | 同 hermes-cli |
| `hermes-feishu` | 同 hermes-cli |
| `hermes-wecom` | 同 hermes-cli |
| `hermes-weixin` | 同 hermes-cli |
| `hermes-homeassistant` | 同 hermes-cli |
| `hermes-webhook` | 同 hermes-cli |
| `hermes-gateway` | 所有消息平台工具集的并集 |

## 动态工具集

### MCP 服务器工具集

每个配置的 MCP 服务器在运行时生成 `mcp-<server>` 工具集。

```yaml
mcp:
  servers:
    github:
      command: npx
      args: ["-y", "@modelcontextprotocol/server-github"]
```

### 插件工具集

插件可通过 `ctx.register_tool()` 在初始化期间注册自己的工具集。

### 自定义工具集

```yaml
toolsets:
  - hermes-cli
custom_toolsets:
  data-science:
    - file
    - terminal
    - code_execution
    - web
    - vision
```

### 通配符

- `all` 或 `*` — 展开为每个已注册工具集（内置 + 动态 + 插件）
