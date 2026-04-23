# Secrets 管理

> **核心摘要**: Paperclip 使用本地主密钥加密存储 secrets。Agent 环境变量中的敏感值（API 密钥、token）存储为加密 secret 引用。

## 默认提供者：`local_encrypted`

Secrets 使用存储在以下位置的本地主密钥加密：

```
~/.paperclip/instances/default/secrets/master.key
```

此密钥在 onboard 期间自动创建。密钥永远不会离开你的机器。

## 配置

### CLI 设置

Onboarding 写入默认 secrets 配置：

```bash
pnpm paperclipai onboard
```

更新 secrets 设置：

```bash
pnpm paperclipai configure --section secrets
```

验证 secrets 配置：

```bash
pnpm paperclipai doctor
```

### 环境变量覆盖

| 变量 | 说明 |
|------|------|
| `PAPERCLIP_SECRETS_MASTER_KEY` | 32 字节密钥（base64、hex 或原始字符串） |
| `PAPERCLIP_SECRETS_MASTER_KEY_FILE` | 自定义密钥文件路径 |
| `PAPERCLIP_SECRETS_STRICT_MODE` | 设置为 `true` 强制 secret 引用 |

## 严格模式

启用严格模式时，敏感 env 密钥（匹配 `*_API_KEY`、`*_TOKEN`、`*_SECRET`）必须使用 secret 引用而不是内联纯值。

```bash
PAPERCLIP_SECRETS_STRICT_MODE=true
```

推荐用于本地信任之外的任何部署。

## 迁移内联 Secrets

如果有使用内联 API 密钥的现有 Agent，迁移到加密 secret 引用：

```bash
pnpm secrets:migrate-inline-env         # 试运行
pnpm secrets:migrate-inline-env --apply # 应用迁移
```

## Agent 配置中的 Secret 引用

Agent 环境变量使用 secret 引用：

```json
{
  "env": {
    "ANTHROPIC_API_KEY": {
      "type": "secret_ref",
      "secretId": "8f884973-c29b-44e4-8ea3-6413437f8081",
      "version": "latest"
    }
  }
}
```

服务器在运行时解析和解密这些引用，将真实值注入 Agent 进程环境。
