# 手机 SSH 远程连接本地计算机

## 基于 FRP 实现方法

---

## 场景识别

### 适用场景
- 在外时需要通过手机远程访问本地 Windows 电脑
- 本地电脑处于 NAT 网络后，无公网 IP
- 需要通过固定端口访问内网机器
- 开发者需要随时通过手机 SSH 连接到开发环境

### 不适用场景
- 本地电脑可直接获得公网 IP（可直接用 SSH 端口转发）
- 对安全性要求极高的生产环境
- 网络条件较差的环境（FRP 依赖稳定连接）

### 前置要求
- AWS EC2 实例（Ubuntu，带公网 IP）作为中转服务器
- Windows 10/11 电脑，安装 OpenSSH Server
- 手机端安装 Termius 或类似 SSH 客户端
- FRP 0.58.1 (Linux + Windows 版本)

---

## 执行步骤

### 第一步：AWS 服务器端配置

#### 1.1 下载并解压 FRP
```bash
mkdir -p /home/ubuntu/.frp
cd /home/ubuntu/.frp
wget https://github.com/fatedier/frp/releases/download/v0.58.1/frp_0.58.1_linux_amd64.tar.gz
tar -zxf frp_0.58.1_linux_amd64.tar.gz
```

#### 1.2 创建服务器配置文件 frps.ini
```ini
[common]
bind_port = 1234
token = 123456
```

#### 1.3 创建启动脚本 start_frps.sh
```bash
#!/usr/bin/env bash
set -euo pipefail
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
FRP_DIR="$BASE_DIR/frp_0.58.1_linux_amd64"
FRPS_BIN="$FRP_DIR/frps"
CONFIG_FILE="$FRP_DIR/frps.ini"
LOG_FILE="$BASE_DIR/frps.log"

# 检查进程是否存在，如存在则重启
PIDS=$(pgrep -f "frps.*frps\\.ini" || true)
if [ -n "$PIDS" ]; then
  echo "frps is running; restarting (pids: $PIDS)..."
  kill $PIDS
  sleep 1
fi

# 启动 frps
echo "Starting frps with $CONFIG_FILE (log: $LOG_FILE)"
cd "$FRP_DIR"
nohup "$FRPS_BIN" -c "$CONFIG_FILE" >"$LOG_FILE" 2>&1 &
sleep 1

# 验证启动
PIDS=$(pgrep -f "frps.*frps\\.ini" || true)
if [ -n "$PIDS" ]; then
  echo "frps started (pid: $PIDS)"
else
  echo "frps failed to start; check $LOG_FILE" >&2
  exit 1
fi
```

#### 1.4 配置 AWS 安全组
在 AWS Console 中开放入站规则：
- TCP 1234 (FRP 控制端口)
- TCP 12345 (SSH 映射端口)

#### 1.5 启动 FRP 服务
```bash
cd /home/ubuntu/.frp
bash ./start_frps.sh
```

---

### 第二步：Windows 客户端配置

#### 2.1 下载 Windows 版 FRP
从 https://github.com/fatedier/frp/releases 下载 Windows 版本，解压到 `C:\frp\`

#### 2.2 创建 frpc.ini 配置文件
```ini
[common]
server_addr = <AWS公网IP>
server_port = 1234
token = 123456

[ssh]
type = tcp
local_ip = 127.0.0.1
local_port = 22
remote_port = 12345
```

#### 2.3 配置 Windows OpenSSH Server
1. 打开「设置 → 应用 → 可选功能 → 添加功能」
2. 安装 OpenSSH Server
3. 确保 SSH 服务正在运行

#### 2.4 生成 SSH 密钥对（使用 Termius）
1. 在 Termius 中生成 SSH 私钥/公钥对
2. 将公钥添加到 `C:\ProgramData\ssh\administrators_authorized_keys`
3. 私钥保存到 `C:\Users\<用户名>\.ssh\666`

#### 2.5 配置 SSH 禁用密码登录
编辑 `C:\ProgramData\ssh\sshd_config`：
```
PasswordAuthentication no
PubkeyAuthentication yes
```

#### 2.6 创建启动脚本 start_frpc.bat
```batch
cd C:\frp
Start-Process -FilePath ".\frpc.exe" -ArgumentList "-c frpc.ini" -WindowStyle Hidden
```

#### 2.7 配置开机自启
将 `start_frpc.bat` 复制到启动文件夹：
```
C:\Users\<用户名>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

---

### 第三步：手机端连接配置

#### 3.1 在 Termius 中创建主机
- Host: `<AWS公网IP>`
- Port: `12345`
- Username: `<Windows用户名>`
- Authentication: Key (选择私钥)

#### 3.2 连接测试
点击连接，接受指纹提示即可。

---

## 常用命令

### 服务器端
```bash
# 启动/重启
cd /home/ubuntu/.frp && bash ./start_frps.sh

# 查看进程
ps -ef | grep frps

# 查看监听端口
ss -lnpt | grep 1234

# 查看日志
tail -n 50 /home/ubuntu/.frps.log

# 停止服务
pkill -f "frps.*frps.ini"
```

### Windows 客户端
```powershell
# 前台启动（调试用）
cd C:\frp; .\frpc.exe -c frpc.ini

# 放行防火墙并启动
Add-MpPreference -ExclusionPath "C:\frp"
Unblock-File C:\frp\frpc.exe
Start-Process -FilePath ".\frpc.exe" -ArgumentList "-c frpc.ini" -WindowStyle Hidden

# 开机自启（管理员 PowerShell）
schtasks /Create /TN "FRPClient" /TR "C:\frp\frpc.exe -c C:\frp\frpc.ini" /SC ONLOGON /RL HIGHEST /F /RU <用户名>
```

---

## 故障排查

| 问题 | 可能原因 | 解决方案 |
|-----|---------|---------|
| Permission denied (publickey) | 公钥未正确配置 | 确认公钥在 `C:\ProgramData\ssh\administrators_authorized_keys` |
| Connection refused | frps 未运行或端口未放行 | 检查 AWS 安全组规则，确认 frps 进程运行 |
| frpc 连接失败 | server_addr/token 不匹配 | 检查 frpc.ini 配置与 frps.ini 一致 |
| 连接超时 | 网络问题或防火墙 | 检查 ufw/aws 安全组/本地防火墙 |

---

## 注意事项

### 安全相关
1. **Token 保密**：frps.ini 中的 token 必须保密，不要泄露
2. **私钥保护**：SSH 私钥不要上传到公共平台
3. **密钥登录**：务必禁用密码登录，只保留密钥认证
4. **定期检查**：定期检查 frps.log 是否有异常连接

### 维护相关
1. **FRP 版本更新**：INI 格式未来会被弃用，后续建议改用 TOML/YAML
2. **systemd 服务**：生产环境建议将 frps 注册为 systemd 服务
3. **进程监控**：建议配置进程监控，确保 frpc 断开后自动重连
4. **版本锁定**：记录当前使用的 FRP 版本号，便于问题复现

### 网络相关
1. **端口选择**：避免使用常用端口（如 22），减少被扫描风险
2. **备用方案**：建议记录 AWS Console 登录信息，以防 FRP 配置失效
3. **延迟考虑**：FRP 会增加网络延迟，不适合对实时性要求高的场景

---

## 文件清单

| 文件 | 位置 | 说明 |
|-----|------|-----|
| frps | AWS: /home/ubuntu/.frp/frp_0.58.1_linux_amd64/frps | FRP 服务端可执行文件 |
| frps.ini | AWS: /home/ubuntu/.frp/frp_0.58.1_linux_amd64/frps.ini | FRP 服务端配置 |
| start_frps.sh | AWS: /home/ubuntu/.frp/start_frps.sh | FRP 服务端启动脚本 |
| frps.log | AWS: /home/ubuntu/.frp/frps.log | FRP 服务端日志 |
| frpc.exe | Windows: C:\frp\frpc.exe | FRP 客户端可执行文件 |
| frpc.ini | Windows: C:\frp\frpc.ini | FRP 客户端配置 |
| start_frpc.bat | Windows: C:\frp\start_frpc.bat | FRP 客户端启动脚本 |
| SSH 私钥 | Windows: C:\Users\<用户>\.ssh\666 | SSH 私钥文件 |
| SSH 公钥 | Windows: C:\ProgramData\ssh\666_keys | SSH 管理员授权公钥 |
