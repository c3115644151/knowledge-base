# 提供商路由

当使用 [OpenRouter](https://openrouter.ai/) 作为 LLM 提供商时，Hermes Agent 支持**提供商路由**——细粒度控制请求由哪个底层 AI 提供商处理及其优先级。

## 配置

在 `~/.hermes/config.yaml` 添加 `provider_routing` 部分：

```yaml
provider_routing:
  sort: "price"           # 如何排名提供商
  only: []                # 白名单：仅使用这些提供商
  ignore: []              # 黑名单：永不使用这些提供商
  order: []               # 显式提供商优先级顺序
  require_parameters: false  # 仅使用支持所有参数的提供商
  data_collection: null   # 控制数据收集 ("allow" 或 "deny")
```

## 选项

### `sort`

| 值 | 描述 |
|----|------|
| `"price"` | 最便宜的提供商优先 |
| `"throughput"` | 每秒 token 最快的优先 |
| `"latency"` | 首 token 时间最低的优先 |

### `only`

白名单。设置后**仅**使用这些提供商。

### `ignore`

黑名单。这些提供商**永不**使用。

### `order`

显式优先级顺序。列出的提供商优先，未列出的作为后备。

### `require_parameters`

`true` 时，OpenRouter 仅路由到支持**所有**请求参数的提供商。

### `data_collection`

控制提供商是否可将提示用于训练。`"allow"` 或 `"deny"`。

## 实用示例

### 优化成本

```yaml
provider_routing:
  sort: "price"
```

### 优化速度

```yaml
provider_routing:
  sort: "latency"
```

### 锁定特定提供商

```yaml
provider_routing:
  only:
    - "Anthropic"
```

### 排除提供商

```yaml
provider_routing:
  ignore:
    - "Together"
    - "DeepInfra"
  data_collection: "deny"
```

### 组合使用

```yaml
provider_routing:
  sort: "price"
  ignore: ["Together"]
  require_parameters: true
  data_collection: "deny"
```

## 工作原理

提供商路由偏好通过 `extra_body.provider` 字段传递给 OpenRouter API。适用于：
- **CLI 模式** — 配置在 `~/.hermes/config.yaml`
- **网关模式** — 相同配置文件

## 与回退提供商的比较

提供商路由控制 OpenRouter **内部**的子提供商选择。如需在主提供商完全失败时自动切换到**不同的提供商**，请参见 [回退提供商](hermes-回退提供商.md)。
