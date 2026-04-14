# ACP 编辑器集成

Hermes Agent 可以作为 ACP 服务器运行，让 ACP 兼容的编辑器通过 stdio 与 Hermes 通信，支持：
- 聊天消息
- 工具调用
- 文件差异
- 终端命令
- 审批提示
- 流式思考/响应

## 安装

```bash
pip install -e '.[acp]'
```

这会安装 `agent-client-protocol` 依赖并启用：
- `hermes acp`
- `hermes-acp`
- `python -m acp_adapter`

## 启动 ACP 服务器

```bash
hermes acp
# 或
hermes-acp
# 或
python -m acp_adapter
```

## 编辑器配置

### VS Code

```json
{
  "acpClient.agents": [
    {
      "name": "hermes-agent",
      "registryDir": "/path/to/hermes-agent/acp_registry"
    }
  ]
}
```

### Zed

```json
{
  "agent_servers": {
    "hermes-agent": {
      "type": "custom",
      "command": "hermes",
      "args": ["acp"]
    }
  }
}
```

### JetBrains

使用 ACP 兼容插件，指向 `acp_registry/` 目录。

## 配置和凭证

ACP 模式使用与 CLI 相同的 Hermes 配置：
- `~/.hermes/.env`
- `~/.hermes/config.yaml`
- `~/.hermes/skills/`
- `~/.hermes/state.db`

## 会话行为

ACP 会话由 ACP 适配器的内存会话管理器追踪：
- 会话 ID
- 工作目录
- 选择的模型
- 当前对话历史
- 取消事件

## 工作目录

ACP 会话将编辑器的 cwd 绑定到 Hermes 任务 ID，使文件和终端工具相对于编辑器工作区运行。

## 审批

危险终端命令可作为审批提示路由回编辑器：
- allow once（允许一次）
- allow always（总是允许）
- deny（拒绝）

## 故障排除

### ACP 代理未出现在编辑器
- 检查编辑器是否指向正确的 `acp_registry/` 路径
- 确认 Hermes 已安装并在 PATH 中
- 确认 ACP extra 已安装（`pip install -e '.[acp]'`）

### ACP 启动但立即报错
```bash
hermes doctor
hermes status
hermes acp
```

### 凭证缺失
```bash
hermes model
```
或编辑 `~/.hermes/.env`。
