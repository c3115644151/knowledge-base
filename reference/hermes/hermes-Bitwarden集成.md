# Bitwarden Secrets Manager 集成

> Hermes Agent v0.14.1+ 新功能

从 `~/.hermes/.env` 存储明文密钥改为从 Bitwarden Secrets Manager 集中管理。一个机器账户访问令牌替代 N 个提供商密钥，轮换凭证只需在 Bitwarden Web 应用中修改一次。

## 工作原理

1. 在 Bitwarden Secrets Manager 创建**机器账户**，授予项目读权限，生成**访问令牌**
2. Hermes 将令牌存储为 `~/.hermes/.env` 中的 `BWS_ACCESS_TOKEN`
3. Hermes 启动时调用 `bws secret list <project_id>`，将返回的密钥设置到 `os.environ`
4. 默认**覆盖**现有环境变量值，Bitwarden 为真相来源

`bws` 二进制文件首次使用时自动下载到 `~/.hermes/bin/`，无需手动安装。

## 设置步骤

```bash
# 1. 在 Bitwarden Web 应用中
#    - 创建/选择一个 Project (如 "Hermes keys")
#    - 添加 OPENROUTER_API_KEY、ANTHROPIC_API_KEY 等密钥
#    - Machine Accounts → New machine account → 授予项目 Read 权限
#    - Access Tokens → Create access token → 复制令牌

# 2. 运行向导
hermes secrets bitwarden setup

# 3. 验证
hermes secrets bitwarden status
```

## CLI 命令

| 命令 | 描述 |
|------|------|
| `hermes secrets bitwarden setup` | 交互式向导（安装二进制、输入令牌、选择项目、测试获取） |
| `hermes secrets bitwarden status` | 显示配置 + 二进制版本 + 令牌状态 |
| `hermes secrets bitwarden sync` | 干跑：拉取并显示将应用的密钥 |
| `hermes secrets bitwarden sync --apply` | 拉取并导出到当前 shell 环境 |
| `hermes secrets bitwarden install` | 仅下载 `bws` 二进制文件 |
| `hermes secrets bitwarden disable` | 禁用 Bitwarden，保留令牌和项目 ID |

## 配置

```yaml
secrets:
  bitwarden:
    enabled: true
    access_token_env: BWS_ACCESS_TOKEN  # bootstrap 令牌
    project_id: "uuid"                   # 项目 UUID
    cache_ttl_seconds: 300               # 缓存时间
    override_existing: true              # true=Bitwarden 覆盖 .env
    auto_install: true                  # 自动下载 bws
```

| 参数 | 默认 | 说明 |
|------|------|------|
| `enabled` | `false` | 总开关，false 时不联系 Bitwarden |
| `access_token_env` | `BWS_ACCESS_TOKEN` | Bootstrap 令牌的环境变量名 |
| `project_id` | `""` | 要同步的项目的 UUID |
| `cache_ttl_seconds` | `300` | 进程内缓存时间，设为 0 禁用缓存 |
| `override_existing` | `true` | true=Bitwarden 值覆盖 .env；false=.env 优先 |
| `auto_install` | `true` | 自动下载 bws 二进制到 `~/.hermes/bin/` |

## 故障处理

| 症状 | 原因 | 解决 |
|------|------|------|
| `BWS_ACCESS_TOKEN is not set` | 启用但令牌被清除 | 重新运行 `setup` |
| `invalid access token` | 令牌被撤销 | 生成新令牌并重新 setup |
| `bws timed out` | 网络问题 | 检查到 `api.bitwarden.com` 连通性 |
| `bws binary not available` | `auto_install: false` 且 bws 不在 PATH | 手动安装或开启 auto_install |
| `Checksum mismatch` | 下载损坏 | 重新运行，会重试 |

## 安全说明

- `BWS_ACCESS_TOKEN` 本身敏感——任何持有者都能读取机器账户有权限的所有密钥，应视为高价值 bearer token
- Hermes 拒绝让 Bitwarden 覆盖 bootstrap 令牌本身，即使 `override_existing: true`
- `bws` 下载验证 SHA-256 校验和
- Bitwarden Secrets Manager 在免费版有限额，多机器集群推荐使用

## 适用场景

**推荐使用**：多机器集群、共享开发机、Gateway VPS、集中轮换和吊销

**不推荐使用**：
- 单机个人使用（直接用 `.env` 即可）
- 气隙环境（无法访问 `api.bitwarden.com`）
- 已有 CI/CD 密钥注入机制（GitHub Actions Secrets、Vault 等）
