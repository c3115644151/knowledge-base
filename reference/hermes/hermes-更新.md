# Updating & Uninstalling

更新和卸载 Hermes Agent。

## 更新

### 自动更新
```bash
hermes update
```

更新过程：
1. Git pull 最新代码
2. 更新依赖（`uv pip install -e ".[all]"`）
3. 配置迁移（检测新选项）
4. Gateway 自动重启

### 验证更新
```bash
git status --short    # 检查工作目录
hermes doctor         # 诊断配置和依赖
hermes --version      # 确认版本号
```

### 从消息平台更新
发送 `/update` 到 Telegram/Discord/Slack/WhatsApp。

### 手动更新
```bash
cd /path/to/hermes-agent
git pull origin main
git submodule update --init --recursive
uv pip install -e ".[all]"
uv pip install -e "./tinker-atropos"
hermes config check
hermes config migrate
```

### 回滚
```bash
# 回滚到特定 commit
git checkout <commit-hash>
git submodule update --init --recursive
uv pip install -e ".[all]"

# 或回滚到特定版本
git checkout v0.6.0
uv pip install -e ".[all]"
```

### Nix 用户
```bash
nix flake update hermes-agent
# 或
nix profile upgrade hermes-agent

# 回滚
nix profile rollback
```

## 卸载

### 自动卸载
```bash
hermes uninstall
```

会询问是否保留配置文件（`~/.hermes/`）。

### 手动卸载
```bash
rm -f ~/.local/bin/hermes
rm -rf /path/to/hermes-agent
rm -rf ~/.hermes  # 可选，保留以备重装
```

### 停止 Gateway 服务
```bash
hermes gateway stop

# Linux (systemd)
systemctl --user disable hermes-gateway

# macOS (launchd)
launchctl remove ai.hermes.gateway
```
