# Honcho 记忆

[Honcho](https://github.com/plastic-labs/honcho) 是 AI 原生记忆后端，在 Hermes 内置记忆系统之上添加辩证推理和深度用户建模。

## Honcho 添加的功能

| 能力 | 内置记忆 | Honcho |
|------|----------|--------|
| 跨会话持久化 | ✔ 文件式 MEMORY.md/USER.md | ✔ 服务器端 API |
| 用户画像 | ✔ 手动代理策划 | ✔ 自动辩证推理 |
| 多代理隔离 | — | ✔ 每个对等体独立画像 |
| 观察模式 | — | ✔ 统一或定向观察 |
| 结论（派生洞察） | — | ✔ 服务器端推理模式 |
| 历史搜索 | ✔ FTS5 会话搜索 | ✔ 语义搜索结论 |

**辩证推理**：每次对话后，Honcho 分析交换并派生"结论"——关于用户偏好、习惯和目标的洞察。

**多代理画像**：多个 Hermes 实例与同一用户对话时，Honcho 维护独立的"对等体"画像。

## 设置

```bash
hermes memory setup  # 选择 "honcho" 从提供商列表
```

或手动配置：

```yaml
# ~/.hermes/config.yaml
memory:
  provider: honcho
```

```bash
echo "HONCHO_API_KEY=your-key" >> ~/.hermes/.env
```

从 [honcho.dev](https://honcho.dev/) 获取 API 密钥。

## 配置选项

```yaml
# ~/.hermes/config.yaml
honcho:
  observation: directional  # "unified"（新安装默认）或 "directional"
  peer_name: ""             # 自动检测，或手动设置
```

**观察模式**：
- `unified` — 所有观察进入单一池。更简单，适合单代理设置。
- `directional` — 观察标记方向（user→agent, agent→user）。支持更丰富的对话动态分析。

## 工具

Honcho 作为记忆提供者活动时，四个额外工具可用：

| 工具 | 用途 |
|------|------|
| `honcho_conclude` | 触发服务器端辩证推理 |
| `honcho_context` | 检索当前对话的相关上下文 |
| `honcho_profile` | 查看或更新用户 Honcho 画像 |
| `honcho_search` | 语义搜索所有存储的结论和观察 |

## CLI 命令

```bash
hermes honcho status  # 显示连接状态和配置
hermes honcho peer    # 更新多代理设置的对等体名称
```

## 从 `hermes honcho` 迁移

如果之前使用了独立 `hermes honcho setup`：

1. 现有配置（`honcho.json` 或 `~/.honcho/config.json`）保留
2. 服务器端数据（记忆、结论、用户画像）完整
3. 在 config.yaml 设置 `memory.provider: honcho` 以重新激活

无需重新登录或重新设置。
