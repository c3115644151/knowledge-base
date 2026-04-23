# IDE 配置协议

> AI 指导用户根据操作系统和 IDE 类型完成配置

---

## 前置条件检查清单

```
IF 用户已完成开发环境搭建
THEN 继续执行
ELSE 引导跳转至 [开发环境搭建](./开发环境搭建.md)

检查项：
□ 操作系统确认
□ IDE 类型确认（VS Code/Cursor/Windsurf）
□ 已安装或需要下载 IDE
```

---

## VS Code 配置

### Windows + WSL 用户

```
IF 操作系统 = Windows AND 使用WSL = TRUE
THEN 按顺序执行：

     STEP 1: 安装 VS Code（如未安装）
       下载: https://code.visualstudio.com/

     STEP 2: 安装 WSL 扩展
       执行: code --install-extension ms-vscode-remote.remote-wsl

     STEP 3: 打开 WSL 项目
       执行: cd /path/to/project && code .

     STEP 4: 安装开发扩展
       执行扩展安装命令：
         ms-vscode.powershell
         eamodio.gitlens
         esbenp.prettier-vscode
         dbaeumer.vscode-eslint
         mechatroner.rainbow-csv

     STEP 5: 配置终端
       设置 → 终端 → 默认配置文件 → Ubuntu (WSL)

     STEP 6: 配置自动保存
       设置 → Auto Save → afterDelay
```

### Windows 原生用户

```
IF 操作系统 = Windows AND 使用WSL = FALSE
THEN 按顺序执行：

     STEP 1: 安装 VS Code
       下载: https://code.visualstudio.com/
       或执行: winget install Microsoft.VisualStudioCode

     STEP 2: 安装开发扩展
       执行扩展安装：
         eamodio.gitlens
         esbenp.prettier-vscode
         dbaeumer.vscode-eslint
         mechatroner.rainbow-csv

     STEP 3: 配置终端
       设置 → 终端 → 选择 PowerShell 或 Git Bash

     STEP 4: 配置自动保存
       设置 → Auto Save → afterDelay

     STEP 5: 配置 Git
       确保 Git 已安装并配置 PATH
```

### macOS 用户

```
IF 操作系统 = macOS
THEN 按顺序执行：

     STEP 1: 安装 VS Code
       执行: brew install --cask visual-studio-code
       或下载: https://code.visualstudio.com/

     STEP 2: 配置命令行工具
       执行: Cmd+Shift+P → Shell Command: Install 'code' command in PATH

     STEP 3: 安装开发扩展
       执行扩展安装：
         eamodio.gitlens
         esbenp.prettier-vscode
         dbaeumer.vscode-eslint

     STEP 4: 配置自动保存
       设置 → Auto Save → afterDelay
```

### Linux 用户

```
IF 操作系统 = Linux
THEN 按顺序执行：

     STEP 1: 安装 VS Code
       执行: sudo apt install ./code_amd64.deb
       或使用 snap: sudo snap install --classic code

     STEP 2: 安装开发扩展
       执行扩展安装：
         eamodio.gitlens
         esbenp.prettier-vscode
         dbaeumer.vscode-eslint

     STEP 3: 配置自动保存
       设置 → Auto Save → afterDelay

     STEP 4: 配置终端集成
       设置 → Terminal → Integrated → Profiles → Linux
```

---

## Cursor 配置

```
IF IDE类型 = Cursor
THEN 按顺序执行：

     STEP 1: 下载安装
       访问: https://cursor.com
       下载对应系统的安装包

     STEP 2: 首次启动配置
       - 创建账号或登录
       - 选择主题
       - 选择字体大小

     STEP 3: 导入 VS Code 设置（可选）
       IF 用户之前使用 VS Code = TRUE
       THEN 执行: File → Import Settings from VS Code

     STEP 4: 配置 AI 功能
       - 登录 Cursor 账号
       - 或配置 API Key（Settings → Models）

     STEP 5: 学习核心快捷键
       | 快捷键        | 功能           |
       |---------------|----------------|
       | Ctrl/Cmd + K | AI 编辑        |
       | Ctrl/Cmd + L | AI 聊天        |
       | Ctrl/Cmd + I | Composer 模式  |

     STEP 6: 配置自动保存
       设置 → Auto Save → afterDelay
```

---

## Windsurf 配置

```
IF IDE类型 = Windsurf
THEN 按顺序执行：

     STEP 1: 下载安装
       访问: https://windsurf.com
       下载对应系统的安装包

     STEP 2: 注册并登录
       - 创建账号（新用户有免费额度）
       - 登录

     STEP 3: 首次启动配置
       - 选择主题
       - 配置基础设置

     STEP 4: 学习 AI 功能
       - Cascade 基础对话
       - 理解 Flow 的工作方式

     STEP 5: 配置基础开发环境
       - 安装对应语言扩展
       - 配置格式化工具
```

---

## 通用扩展推荐

```
IF IDE类型 = VS Code/Cursor
THEN 推荐安装以下扩展：

     // Git 相关
     eamodio.gitlens
     GitLens — Git supercharged

     // 代码格式化
     esbenp.prettier-vscode
     Prettier - Code formatter

     // 代码检查
     dbaeumer.vscode-eslint
     ESLint

     // 增强功能
     mechatroner.rainbow-csv
     Rainbow CSV

     // 主题（可选）
     ryanoasis.nerd-fonts-complete
     或 One Dark Pro / Dracula
```

---

## 验证检查点

```
验证步骤：

  1. 启动 VS Code/Cursor/Windsurf
  2. 打开一个测试项目文件夹
  3. 验证以下功能：
     □ 终端可正常打开
     □ Git 状态显示正常（VS Code）
     □ AI 功能可正常使用（Cursor/Windsurf）
     □ 扩展列表显示已安装的扩展
     □ 自动保存已启用

IF 所有验证项通过
THEN 配置成功
ELSE 报告失败的验证项
```

---

## 常见问题处理

| 问题 | 诊断条件 | 解决方案 |
|:-----|:---------|:--------|
| WSL 扩展安装失败 | Remote-WSL 错误 | 重新安装 WSL2，确保内核更新包已安装 |
| 扩展安装慢 | 网络问题 | 配置代理或使用国内镜像 |
| Cursor AI 无法使用 | 未登录/无额度 | 登录账号或检查免费额度 |
| 终端乱码 | 编码问题 | 设置 → Terminal → Encoding → UTF-8 |
| 自动保存不生效 | 快捷键冲突 | 检查是否有其他扩展覆盖设置 |

---

## 后续步骤

```
IF 验证检查点全部通过
THEN 告知用户：
     "IDE 配置完成！查看项目 README 了解 Vibe Coding 工作流"
ELSE 针对失败的检查项提供解决方案
```
