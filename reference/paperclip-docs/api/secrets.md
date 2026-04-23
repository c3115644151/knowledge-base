# Secrets API

> **核心摘要**: 管理 Agent 在环境配置中引用的加密密钥。密钥加密存储，支持版本控制。

## 列表 Secrets

```bash
GET /api/companies/{companyId}/secrets
```

返回密钥元数据（不解密值）。

## 创建 Secret

```bash
POST /api/companies/{companyId}/secrets
{
  "name": "anthropic-api-key",
  "value": "sk-ant-..."
}
```

值在存储时加密。只返回 secret ID 和元数据。

## 更新 Secret

```bash
PATCH /api/secrets/{secretId}
{
  "value": "sk-ant-new-value..."
}
```

创建新版本的 secret。引用 `"version": "latest"` 的 Agent 在下次 heartbeat 时自动获取新值。

## 在 Agent 配置中使用 Secrets

在 Agent adapter config 中引用 secret 而不是内联值：

```json
{
  "env": {
    "ANTHROPIC_API_KEY": {
      "type": "secret_ref",
      "secretId": "{secretId}",
      "version": "latest"
    }
  }
}
```

服务器在运行时解析和解密 secret 引用，将真实值注入 Agent 进程环境。
