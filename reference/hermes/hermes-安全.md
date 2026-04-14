# 安全指南

## 安全模型概述

Hermes Agent 采用纵深防御安全模型，七层保护：

1. **用户授权** - 白名单、DM 配对
2. **危险命令审批** - 人类-in-the-loop
3. **容器隔离** - Docker/Singularity/Modal
4. **MCP 凭证过滤** - 环境变量隔离
5. **上下文文件扫描** - 提示注入检测
6. **跨会话隔离** - 会话数据隔离
7. **输入清理** - Shell 注入防护

## 危险命令审批

### 审批模式

```yaml
approvals:
  mode: manual   # manual | smart | off
  timeout: 60
```

| 模式 | 行为 |
|------|------|
| `manual` | 始终提示审批 |
| `smart` | LLM 评估风险后决定 |
| `off` | 禁用所有审批 |

### 危险命令模式

触发审批的命令：
- `rm -rf` - 递归删除
- `chmod 777` - 不安全权限
- `DROP TABLE` - SQL 删除
- `curl ... | sh` - 远程执行
- `> /etc/` - 系统文件覆盖

### YOLO 模式

绕过所有审批：
```bash
hermes --yolo
/yolo  # 切换开关
```

## 用户授权

### 白名单
```bash
TELEGRAM_ALLOWED_USERS=123456789
DISCORD_ALLOWED_USERS=111222333
GATEWAY_ALLOWED_USERS=123456789
```

### DM 配对系统
```bash
hermes pairing list
hermes pairing approve telegram ABC12DEF
hermes pairing revoke telegram 123456789
```

## 容器隔离

### Docker 安全标志
```yaml
terminal:
  backend: docker
  container_cpu: 1
  container_memory: 5120
  container_disk: 51200
```

### 后端安全对比

| 后端 | 隔离 | 危险命令检查 |
|------|------|-------------|
| `local` | 无 | ✅ 是 |
| `ssh` | 远程 | ✅ 是 |
| `docker` | 容器 | ❌ 跳过 |
| `singularity` | 容器 | ❌ 跳过 |
| `modal` | 云沙箱 | ❌ 跳过 |

## MCP 安全

### 环境变量过滤
只传递显式配置的 `env`：
```yaml
mcp_servers:
  github:
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "***"
```

### 凭证编辑
错误消息中的凭证自动编辑为 `[REDACTED]`。

## SSRF 防护

阻止访问：
- 私有网络 (10.x, 172.16.x, 192.168.x)
- 环回地址 (127.x, ::1)
- 链接本地 (169.254.x)
- 云元数据 (169.254.169.254)

## 网站黑名单

```yaml
security:
  website_blocklist:
    enabled: true
    domains:
      - "*.internal.company.com"
      - "admin.example.com"
```

## 提示注入防护

上下文文件扫描检测：
- 忽略指令
- 隐藏 HTML 评论
- 凭证窃取尝试
- 不可见 Unicode 字符

## Tirith 扫描

内容级命令扫描：
```yaml
security:
  tirith_enabled: true
  tirith_timeout: 5
  tirith_fail_open: true
```

## 生产部署检查清单

1. ✅ 设置显式白名单
2. ✅ 使用 Docker 后端
3. ✅ 限制资源 (CPU, 内存, 磁盘)
4. ✅ 密钥存储在 `~/.hermes/.env`
5. ✅ 启用 DM 配对
6. ✅ 定期审查命令白名单
7. ✅ 设置 `MESSAGING_CWD`
8. ✅ 不以 root 运行
9. ✅ 监控日志
10. ✅ 定期更新

## 文件权限

```bash
chmod 600 ~/.hermes/.env
```
