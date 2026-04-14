# CLI 命令参考

## 主命令

### hermes
```bash
hermes                  # 启动交互式会话
hermes chat             # 同 hermes
hermes chat -q "..."    # 单次查询模式
hermes --continue       # 恢复上次会话
hermes -c               # 简写
hermes --resume <id>    # 恢复指定会话
hermes -r <id>          # 简写
hermes --yolo           # YOLO 模式
hermes -w               # Git worktree 模式
```

### 选项

```bash
--model <model>        # 指定模型
--provider <provider>   # 指定提供商
--toolsets <list>      # 工具集列表
-s <skill1,skill2>     # 预加载技能
--verbose              # 详细输出
```

## 模型与工具

### hermes model
```bash
hermes model            # 交互式选择提供商
hermes model list       # 列出可用模型
```

### hermes tools
```bash
hermes tools            # 配置工具
hermes tools list       # 列出可用工具
```

## 配置

### hermes config
```bash
hermes config           # 查看配置
hermes config show      # 显示当前配置
hermes config edit      # 编辑 config.yaml
hermes config set <key> <value>  # 设置值
hermes config get <key>          # 获取值
hermes config check     # 检查缺失选项
hermes config migrate   # 交互式迁移
```

## 网关

### hermes gateway
```bash
hermes gateway start     # 启动网关
hermes gateway stop      # 停止网关
hermes gateway restart   # 重启网关
hermes gateway status    # 查看状态
hermes gateway setup     # 交互式设置
hermes gateway install   # 安装系统服务
hermes gateway uninstall # 卸载系统服务
```

## Profiles

### hermes profile
```bash
hermes profile list                # 列出所有 profiles
hermes profile show <name>         # 显示详情
hermes profile use <name>          # 设为默认
hermes profile create <name>        # 创建
hermes profile create <name> --clone     # 克隆配置
hermes profile create <name> --clone-all  # 克隆全部
hermes profile rename <old> <new>  # 重命名
hermes profile export <name> <file>  # 导出
hermes profile import <file> <name>    # 导入
hermes profile delete <name>      # 删除
```

## 会话

### hermes sessions
```bash
hermes sessions list             # 列出会话
hermes sessions show <id>        # 显示会话
hermes sessions search <query>   # 搜索会话
hermes sessions rename <id> <title>  # 重命名
hermes sessions delete <id>      # 删除
```

## 技能

### hermes skills
```bash
hermes skills list                    # 列出已安装
hermes skills browse                  # 浏览目录
hermes skills search <query>          # 搜索
hermes skills install <url>           # 安装
hermes skills install <url> --force    # 强制覆盖
hermes skills uninstall <name>        # 卸载
hermes skills create <name>           # 创建新技能
```

## 记忆

### hermes memory
```bash
hermes memory setup       # 配置记忆提供者
hermes memory status      # 查看状态
```

### hermes honcho
```bash
hermes honcho status      # 查看连接状态
hermes honcho peer        # 管理 peer
```

## 定时任务

### hermes cron
```bash
hermes cron list          # 列出任务
hermes cron show <id>     # 显示详情
hermes cron pause <id>   # 暂停
hermes cron resume <id>  # 恢复
hermes cron edit <id>    # 编辑
hermes cron delete <id>  # 删除
```

## 配对

### hermes pairing
```bash
hermes pairing list              # 列出
hermes pairing approve <platform> <code>  # 审批
hermes pairing revoke <platform> <user_id>  # 撤销
hermes pairing clear-pending     # 清除待处理
```

## MCP

### hermes mcp
```bash
hermes mcp serve           # 作为 MCP 服务器运行
hermes mcp add <name>      # 添加 MCP 服务器
hermes mcp remove <name>   # 移除
hermes mcp reload          # 重新加载
```

## ACP

### hermes acp
```bash
hermes acp                # 启动 ACP 服务器
```

## 更新与诊断

### hermes update
```bash
hermes update             # 更新到最新版本
hermes version            # 显示版本
hermes doctor             # 运行诊断
hermes status             # 查看状态
```

## Tab 补全

```bash
hermes completion bash    # Bash 补全脚本
hermes completion zsh     # Zsh 补全脚本
```

## 卸载

### hermes uninstall
```bash
hermes uninstall          # 卸载 Hermes
```
