# VS Code Remote Tunnel 配置 - 配置协议

## 前置条件检查清单

- [ ] WSL 已开启 systemd（`/etc/wsl.conf` 配置 `[boot] systemd=true`）
- [ ] WSL 已重启（`wsl --shutdown` 后重新进入）
- [ ] 网络可直连或通过本机代理（示例：127.0.0.1:9910）
- [ ] GitHub 账号（用于 tunnel 授权）
- [ ] VS Code 客户端已安装 "Remote - Tunnels" 扩展

## 配置步骤（IF-THEN）

### 步骤 1：安装 VS Code CLI

```
IF WSL 中未安装 VS Code CLI
THEN 执行安装
```

```bash
sudo apt-get update
sudo apt-get install -y wget gpg apt-transport-https

wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | \
  sudo tee /etc/apt/keyrings/packages.microsoft.gpg >/dev/null

echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/packages.microsoft.gpg] \
  https://packages.microsoft.com/repos/code stable main" | \
  sudo tee /etc/apt/sources.list.d/vscode.list

sudo apt-get update
sudo apt-get install -y code
```

### 步骤 2：GitHub 授权

```
IF 尚未授权 GitHub 账号
THEN 执行一次性登录
```

```bash
/usr/local/bin/code tunnel user login
# 浏览器打开提示的 device code 完成 GitHub 授权
```

### 步骤 3：配置代理（如需要）

```
IF 网络需要通过代理访问
THEN 创建 systemd drop-in 配置
```

```bash
mkdir -p ~/.config/systemd/user/code-tunnel.service.d

cat > ~/.config/systemd/user/code-tunnel.service.d/proxy.conf << 'EOF'
[Service]
Environment=HTTP_PROXY=http://127.0.0.1:9910
Environment=HTTPS_PROXY=http://127.0.0.1:9910
Environment=NO_PROXY=localhost,127.0.0.1,::1
EOF

systemctl --user daemon-reload
```

### 步骤 4：安装并启用 Tunnel 服务

```
IF 需要开机自启 Tunnel
THEN 安装 systemd 服务
```

```bash
/usr/local/bin/code tunnel service install \
  --accept-server-license-terms \
  --name <tunnel-name>

systemctl --user enable code-tunnel.service
systemctl --user restart code-tunnel.service
```

## 验证检查点

- [ ] `code tunnel status` 显示 `tunnel: Connected` 和 `service_installed: true`
- [ ] `systemctl --user status code-tunnel.service` 服务运行中
- [ ] VS Code 客户端 Remote Explorer 可发现该 tunnel
- [ ] 浏览器访问 `https://vscode.dev/tunnel/<tunnel-name>` 可正常连接

## 客户端连接方式

### VS Code 桌面客户端

```
IF 使用 VS Code 桌面版
THEN 安装扩展并连接
```

1. 安装扩展：Remote - Tunnels
2. 使用同一 GitHub 账号登录
3. 打开 Remote Explorer，选择目标 tunnel

### 纯浏览器访问

```
IF 无桌面客户端
THEN 使用浏览器访问
```

访问：`https://vscode.dev/tunnel/<tunnel-name>`

## 运维命令

| 操作 | 命令 |
|------|------|
| 查看状态 | `code tunnel status` |
| 查看日志 | `code tunnel service log --log info` |
| 重命名 | `code tunnel rename <new-name>` |
| 停止隧道 | `code tunnel kill` |
| 卸载服务 | `code tunnel service uninstall` |

## 常见故障

| 问题 | 解决方案 |
|------|----------|
| 仍显示 Disconnected | 确认代理可用，`curl https://api.github.com` 能通；或 `unset HTTP_PROXY HTTPS_PROXY` |
| 路径错误 (UNC) | 不要在 `terminal.integrated.cwd` 使用 UNC 路径，删除该项或用 POSIX 路径 |
| 未启用 systemd | 检查 `/etc/wsl.conf`，修改后 `wsl --shutdown` 重新进入 |
| 授权失效 | 重新执行 `code tunnel user login` |
