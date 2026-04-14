# Nix/NixOS 设置

Hermes Agent 提供 Nix flake，支持三种集成级别。

## 三种集成级别

| 级别 | 适用场景 | 特点 |
|------|----------|------|
| **`nix run`/`nix profile`** | 任意 Nix 用户 | 预构建二进制，即装即用 |
| **NixOS Module (原生)** | NixOS 服务器 | 声明式配置，systemd 服务 |
| **NixOS Module (容器)** | 需自安装包的 Agent | 上述 + 持久 Ubuntu 容器 |

## 快速开始

```bash
# 直接运行
nix run github:NousResearch/hermes-agent -- setup
nix run github:NousResearch/hermes-agent -- chat

# 或持久安装
nix profile install github:NousResearch/hermes-agent
hermes setup
hermes chat
```

## NixOS Module

### 添加 Flake Input
```n# flake.nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    hermes-agent.url = "github:NousResearch/hermes-agent";
  };
  outputs = { nixpkgs, hermes-agent, ... }: {
    nixosConfigurations.your-host = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [
        hermes-agent.nixosModules.default
        ./configuration.nix
      ];
    };
  };
}
```

### 最小配置
```n# configuration.nix
{ config, ... }: {
  services.hermes-agent = {
    enable = true;
    settings.model.default = "anthropic/claude-sonnet-4";
    environmentFiles = [ config.sops.secrets."hermes-env".path ];
    addToSystemPackages = true;
  };
}
```

### 选择部署模式

| 模式 | 运行方式 | Agent 可自安装包 |
|------|----------|------------------|
| **Native** (默认) | 硬化的 systemd 服务 | ❌ |
| **Container** | 持久 Ubuntu 容器 | ✅ |

```nservices.hermes-agent = {
  enable = true;
  container.enable = true;  # 启用容器模式
};
```

## 配置选项

| 选项 | 说明 | 示例 |
|------|------|------|
| `settings.model.default` | LLM 模型 | `"anthropic/claude-sonnet-4"` |
| `settings.model.base_url` | Provider 端点 | `"https://openrouter.ai/api/v1"` |
| `environmentFiles` | API keys | `[ config.sops.secrets."hermes-env".path ]` |
| `documents."SOUL.md"` | Agent 个性 | `builtins.readFile ./my-soul.md` |
| `mcpServers.<name>` | MCP 服务器 | 见 MCP 配置 |
| `container.extraVolumes` | 挂载目录 | `[ "/data:/data:rw" ]` |
| `container.backend` | 容器后端 | `"podman"` |

## Secrets 管理

### sops-nix
```n{
  sops = {
    defaultSopsFile = ./secrets/hermes.yaml;
    age.keyFile = "/home/user/.config/sops/age/keys.txt";
    secrets."hermes-env" = { format = "yaml"; };
  };
  services.hermes-agent.environmentFiles = [
    config.sops.secrets."hermes-env".path
  ];
}
```

### agenix
```n{
  age.secrets.hermes-env.file = ./secrets/hermes-env.age;
  services.hermes-agent.environmentFiles = [
    config.age.secrets.hermes-env.path
  ];
}
```

## MCP 服务器配置

### Stdio (本地)
```n
services.hermes-agent.mcpServers = {
  filesystem = {
    command = "npx";
    args = [ "-y" "@modelcontextprotocol/server-filesystem" "/data/workspace" ];
  };
  github = {
    command = "npx";
    args = [ "-y" "@modelcontextprotocol/server-github" ];
    env.GITHUB_PERSONAL_ACCESS_TOKEN = "\${GITHUB_TOKEN}";  # 从 .env 解析
  };
};
```

### HTTP (远程)
```n
services.hermes-agent.mcpServers.remote-api = {
  url = "https://mcp.example.com/v1/mcp";
  headers.Authorization = "Bearer \${MCP_REMOTE_API_KEY}";
  timeout = 180;
};
```

## 托管模式限制

NixOS 模块下以下 CLI 命令被阻止：
- `hermes setup` - 配置是声明式的
- `hermes config edit/set` - 配置由 Nix 生成
- `hermes gateway install/uninstall` - 由 NixOS 管理

## 开发

```bash
cd hermes-agent
nix develop
# Shell 提供 Python 3.11 + uv + Node.js + ripgrep + git

# direnv (推荐)
direnv allow
```

## 检查
```bash
nix flake check

# 单独检查
nix build .#checks.x86_64-linux.package-contents
nix build .#checks.x86_64-linux.cli-commands
nix build .#checks.x86_64-linux.managed-guard
```
