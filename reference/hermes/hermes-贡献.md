# Contributing

为 Hermes Agent 做贡献的指南。

## 贡献优先级

1. **Bug 修复** - 崩溃、错误行为、数据丢失
2. **跨平台兼容性** - macOS、不同 Linux 发行版、WSL2
3. **安全加固** - shell 注入、提示注入、路径遍历
4. **性能和健壮性** - 重试逻辑、错误处理、优雅降级
5. **新技能** - 广泛有用的（见 Creating Skills）
6. **新工具** - 很少需要
7. **文档** - 修复、澄清、新示例

## 开发设置

### 前置条件

| 要求 | 说明 |
|------|------|
| **Git** | 支持 `--recurse-submodules` |
| **Python 3.11+** | uv 会安装缺失的 |
| **uv** | 快速 Python 包管理器 |
| **Node.js 18+** | 可选（浏览器工具和 WhatsApp 需要） |

### 克隆和安装

```bash
git clone --recurse-submodules https://github.com/NousResearch/hermes-agent.git
cd hermes-agent

# 创建 venv
uv venv venv --python 3.11
export VIRTUAL_ENV="$(pwd)/venv"

# 安装所有 extras
uv pip install -e ".[all,dev]"
uv pip install -e "./tinker-atropos"

# 可选：浏览器工具
npm install
```

### 配置开发环境

```bash
mkdir -p ~/.hermes/{cron,sessions,logs,memories,skills}
cp cli-config.yaml.example ~/.hermes/config.yaml
touch ~/.hermes/.env
echo 'OPENROUTER_API_KEY=sk-or-v1-your-key' >> ~/.hermes/.env
```

### 运行

```bash
# 符号链接
mkdir -p ~/.local/bin
ln -sf "$(pwd)/venv/bin/hermes" ~/.local/bin/hermes

# 验证
hermes doctor
hermes chat -q "Hello"
```

### 运行测试

```bash
pytest tests/ -v
```

## 代码风格

- **PEP 8**（实践例外，不严格限制行长度）
- **注释**：仅解释非显而易见的意图
- **错误处理**：捕获特定异常，使用 `logger.warning()`/`logger.error()`
- **跨平台**：从不假设 Unix
- **Profile 安全路径**：从不硬编码 `~/.hermes`

## 跨平台兼容性

Hermes 官方支持 Linux、macOS、WSL2。原生 Windows **不支持**。

### 1. `termios` 和 `fcntl` 仅 Unix

```python
try:
    from simple_term_menu import TerminalMenu
    menu = TerminalMenu(options)
    idx = menu.show()
except (ImportError, NotImplementedError):
    # 回退：编号菜单
    for i, opt in enumerate(options):
        print(f" {i+1}. {opt}")
    idx = int(input("Choice: ")) - 1
```

### 2. 文件编码

```python
try:
    load_dotenv(env_path)
except UnicodeDecodeError:
    load_dotenv(env_path, encoding="latin-1")
```

### 3. 路径分隔符

使用 `pathlib.Path` 而非字符串拼接。

## Pull Request 流程

### 分支命名
```
fix/description     # Bug 修复
feat/description    # 新功能
docs/description    # 文档
test/description    # 测试
refactor/description  # 重构
```

### 提交前检查

1. `pytest tests/ -v`
2. 手动测试
3. 检查跨平台影响
4. PR 保持专注

### 提交信息

使用 [Conventional Commits](https://www.conventionalcommits.org/)：

```
<type>(<scope>): <description>
```

| Type | 用于 |
|------|------|
| `fix` | Bug 修复 |
| `feat` | 新功能 |
| `docs` | 文档 |
| `test` | 测试 |
| `refactor` | 重构 |
| `chore` | 构建、CI、依赖更新 |

示例：
```
fix(cli): prevent crash in save_config_value when model is a string
feat(gateway): add WhatsApp multi-user session isolation
```

## 社区

- **Discord**: [discord.gg/NousResearch](https://discord.gg/NousResearch)
- **GitHub Discussions**: 设计提案和架构讨论
- **Skills Hub**: 上传和分享技能

## 许可证

MIT License
