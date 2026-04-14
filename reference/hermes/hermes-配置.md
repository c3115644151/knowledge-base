# 配置文件参考

## 配置管理

```bash
hermes config            # 查看当前配置
hermes config edit       # 编辑 config.yaml
hermes config set KEY VAL  # 设置值
hermes config check      # 检查缺失选项
hermes config migrate    # 交互式添加缺失选项
```

## 目录结构

```
~/.hermes/
├── config.yaml          # 主配置文件
├── .env                 # API 密钥
├── auth.json            # OAuth 凭证
├── SOUL.md              # Agent 身份
├── memories/
│   ├── MEMORY.md        # 知识记忆
│   └── USER.md          # 用户画像
├── skills/              # 技能
├── sessions/            # 会话
├── cron/                # 定时任务
├── hooks/               # 事件钩子
└── logs/                # 日志
```

## 配置优先级

1. CLI 参数 (最高)
2. `~/.hermes/config.yaml`
3. `~/.hermes/.env`
4. 内置默认值 (最低)

## 环境变量替换

```yaml
auxiliary:
  vision:
    api_key: ${GOOGLE_API_KEY}
    base_url: ${CUSTOM_VISION_URL}
```

## 终端后端

### 后端类型

```yaml
terminal:
  backend: local        # local | docker | ssh | modal | daytona | singularity
  cwd: "."
  timeout: 180         # 秒
  env_passthrough: []  # 环境变量白名单
```

### Docker 配置

```yaml
terminal:
  backend: docker
  docker_image: "nikolaik/python-nodejs:python3.11-nodejs20"
  docker_mount_cwd_to_workspace: false
  docker_forward_env:
    - "GITHUB_TOKEN"
  docker_volumes:
    - "/home/user/projects:/workspace/projects"
  container_cpu: 1
  container_memory: 5120   # MB
  container_disk: 51200    # MB
  container_persistent: true
```

### SSH 配置

```yaml
terminal:
  backend: ssh
  persistent_shell: true

# 环境变量
TERMINAL_SSH_HOST=my-server.example.com
TERMINAL_SSH_USER=ubuntu
TERMINAL_SSH_PORT=22
TERMINAL_SSH_KEY=~/.ssh/my-key
```

### Modal 配置

```yaml
terminal:
  backend: modal
  container_cpu: 1
  container_memory: 5120
  container_disk: 51200
  container_persistent: true

# 环境变量
MODAL_TOKEN_ID=xxx
MODAL_TOKEN_SECRET=xxx
```

## 记忆配置

```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  memory_char_limit: 2200
  user_char_limit: 1375
```

## 上下文压缩

```yaml
compression:
  enabled: true
  threshold: 0.50
  target_ratio: 0.20
  protect_last_n: 20
  summary_model: "google/gemini-3-flash-preview"
  summary_provider: "auto"
  summary_base_url: null
```

## 辅助模型

```yaml
auxiliary:
  vision:
    provider: "auto"
    model: ""
    base_url: ""
    api_key: ""
    timeout: 30
    download_timeout: 30
  web_extract:
    provider: "auto"
    model: ""
    base_url: ""
    api_key: ""
    timeout: 360
  compression:
    timeout: 120
```

## 委托配置

```yaml
delegation:
  max_iterations: 50
  default_toolsets: ["terminal", "file", "web"]
  model: "google/gemini-3-flash-preview"
  provider: "openrouter"
  base_url: null
  api_key: null
```

## 提供商路由 (OpenRouter)

```yaml
provider_routing:
  sort: "price"           # price | throughput | latency
  only: []
  ignore: []
  order: []
  require_parameters: false
  data_collection: null   # "allow" | "deny"
```

## 回退模型

```yaml
fallback_model:
  provider: openrouter
  model: anthropic/claude-sonnet-4
```

## 凭证池策略

```yaml
credential_pool_strategies:
  openrouter: round_robin   # fill_first | round_robin | least_used | random
  anthropic: least_used
```

## 文件读取安全

```yaml
file_read_max_chars: 100000   # 默认 ~25-35K tokens
```

## 迭代预算

```yaml
agent:
  max_turns: 90              # 默认最大迭代次数
  reasoning_effort: ""       # xhigh | high | medium | low | minimal | none
```

## 凭证池

### 凭证池配置

```yaml
# ~/.hermes/.env
# 多个相同提供商的 API 密钥
OPENROUTER_API_KEY_1=sk-or-v1-xxx1
OPENROUTER_API_KEY_2=sk-or-v2-xxx2
OPENROUTER_API_KEY_3=sk-or-v3-xxx3
ANTHROPIC_API_KEY_1=sk-ant-xxx1
ANTHROPIC_API_KEY_2=sk-ant-xxx2

# ~/.hermes/config.yaml
credential_pools:
  openrouter:
    keys:
      - "${OPENROUTER_API_KEY_1}"
      - "${OPENROUTER_API_KEY_2}"
      - "${OPENROUTER_API_KEY_3}"
    strategy: round_robin
  anthropic:
    keys:
      - "${ANTHROPIC_API_KEY_1}"
      - "${ANTHROPIC_API_KEY_2}"
    strategy: least_used
```

### 策略选项

| 策略 | 说明 |
|------|------|
| `fill_first` | 优先使用第一个密钥 (默认) |
| `round_robin` | 均匀轮换 |
| `least_used` | 选择使用最少的密钥 |
| `random` | 随机选择 |

## 安全配置

```yaml
approvals:
  mode: manual    # manual | smart | off
  timeout: 60

command_allowlist:
  - rm
  - systemctl

security:
  tirith_enabled: true
  tirith_timeout: 5
  tirith_fail_open: true
  website_blocklist:
    enabled: true
    domains:
      - "*.internal.company.com"
```

## 显示设置

```yaml
display:
  compact: false
  personality: "kawaii"
  busy_input_mode: "interrupt"   # interrupt | queue
  tool_preview_length: 80       # 0 = 无限制
  bell_on_complete: false
  verbose: false                 # off | new | all | verbose
```
