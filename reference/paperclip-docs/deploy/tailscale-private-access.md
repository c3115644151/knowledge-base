# Tailscale 私有访问

> **核心摘要**: 通过 Tailscale 在私有网络上运行 Paperclip 并从其他设备连接。包括绑定预设和主机名允许列表。

## 1. 在私有认证模式下启动 Paperclip

```bash
pnpm dev --bind tailnet
```

推荐行为：
- `PAPERCLIP_DEPLOYMENT_MODE=authenticated`
- `PAPERCLIP_DEPLOYMENT_EXPOSURE=private`
- `PAPERCLIP_BIND=tailnet`

如果需要旧的宽泛私有网络行为，使用：

```bash
pnpm dev --bind lan
```

## 2. 找到可访问的 Tailscale 地址

从运行 Paperclip 的机器：

```bash
tailscale ip -4
```

你也可以使用 Tailscale MagicDNS 主机名（例如 `my-macbook.tailnet.ts.net`）。

## 3. 从其他设备打开 Paperclip

使用 Tailscale IP 或 MagicDNS 主机名加上 Paperclip 端口：

```
http://<tailscale-host-or-ip>:3100
```

示例：

```
http://my-macbook.tailnet.ts.net:3100
```

## 4. 允许自定义私有主机名（必要时）

如果你使用自定义私有主机名访问 Paperclip，将其添加到允许列表：

```bash
pnpm paperclipai allowed-hostname my-macbook.tailnet.ts.net
```

## 5. 验证服务器可访问

从远程 Tailscale 连接设备：

```bash
curl http://<tailscale-host-or-ip>:3100/api/health
```

预期结果：

```json
{"status":"ok"}
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 私有主机名上的登录或重定向错误 | 用 `paperclipai allowed-hostname` 添加 |
| 应用只在 `localhost` 上工作 | 确保使用 `--bind lan` 或 `--bind tailnet` 而不是 plain `pnpm dev` |
| 本地可连接但远程不行 | 验证两台设备在同一 Tailscale 网络上且端口 `3100` 可达 |
