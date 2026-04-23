# 部署概览

> **核心摘要**: Paperclip 支持三种部署配置，从零摩擦本地到面向互联网的生产环境。

## 部署模式

| 模式 | 认证 | 最佳场景 |
|------|------|----------|
| `local_trusted` | 无需登录 | 单操作员本地机器 |
| `authenticated` + `private` | 需要登录 | 私有网络（Tailscale、VPN、LAN） |
| `authenticated` + `public` | 需要登录 | 面向互联网的云部署 |

## 快速对比

### 本地信任（默认）

- 仅 loopback 主机绑定（localhost）
- 无需人类登录流程
- 最快的本地启动
- 适用于：solo 开发和小实验

### 认证 + 私有

- 需要通过 Better Auth 登录
- 绑定到所有接口以进行网络访问
- 自动 base URL 模式（更低摩擦）
- 适用于：通过 Tailscale 或本地网络的团队访问

### 认证 + 公开

- 需要登录
- 需要明确的公共 URL
- 更严格的安全检查
- 适用于：云托管、面向互联网的部署

## 选择模式

| 场景 | 推荐模式 |
|------|----------|
| 只是试用 Paperclip？ | `local_trusted`（默认） |
| 与私有网络上的团队共享？ | `authenticated` + `private` |
| 部署到云？ | `authenticated` + `public` |

在 onboard 时设置模式：

```bash
pnpm paperclipai onboard
```

或稍后更新：

```bash
pnpm paperclipai configure --section server
```
