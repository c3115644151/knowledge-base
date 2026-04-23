# OpenCode CLI 配置协议

> AI 指导用户安装和配置 OpenCode，免费 AI 编程助手，支持 75+ 模型

---

## 前置条件检查清单

```
IF 用户需要免费 AI CLI 工具
THEN 执行本配置协议

检查项：
□ 操作系统确认
□ 网络代理已配置（如需要）
□ 已有 API Key 或需要注册获取
```

---

## 安装步骤

### 通用安装命令

```
IF 操作系统 = macOS/Linux
THEN 选择以下方式之一：

     // 方式 1: 一键安装（推荐）
     执行: curl -fsSL https://opencode.ai/install | bash

     // 方式 2: npm
     执行: npm install -g opencode-ai

     // 方式 3: Homebrew
     执行: brew install anomalyco/tap/opencode

IF 操作系统 = Windows
THEN 选择以下方式之一：

     // 方式 1: Scoop
     执行: scoop bucket add extras && scoop install extras/opencode

     // 方式 2: Chocolatey
     执行: choco install opencode

     // 方式 3: npm
     执行: npm install -g opencode-ai
```

---

## API Key 配置

### 方式一：Z.AI（推荐，GLM-4.7）

```
IF 用户选择 Z.AI
THEN 执行：

     STEP 1: 注册获取 API Key
       访问: https://z.ai/manage-apikey/apikey-list
       注册账号并创建 API Key

     STEP 2: 连接 OpenCode
       启动: opencode
       输入: /connect
       选择: Z.AI
       输入: API Key

     STEP 3: 选择模型
       输入: /models
       选择: GLM-4.7

验证：输入简单测试问题，确认响应正常
```

### 方式二：MiniMax（M2.1）

```
IF 用户选择 MiniMax
THEN 执行：

     STEP 1: 注册获取 API Key
       访问: https://platform.minimax.io/login
       注册并创建 API Key

     STEP 2: 连接 OpenCode
       启动: opencode
       输入: /connect
       选择: MiniMax
       输入: API Key

     STEP 3: 选择模型
       输入: /models
       选择: M2.1
```

### 方式三：Hugging Face

```
IF 用户选择 Hugging Face
THEN 执行：

     STEP 1: 创建 Token
       访问: https://huggingface.co/settings/tokens/new
       创建具有 inference.serverless.write 权限的 Token

     STEP 2: 连接 OpenCode
       启动: opencode
       输入: /connect
       选择: Hugging Face
       输入: Token

     STEP 3: 选择模型
       输入: /models
       选择: Kimi-K2-Instruct 或 GLM-4.6
```

### 方式四：本地模型（Ollama）

```
IF 用户选择本地模型
THEN 执行：

     STEP 1: 安装 Ollama
       执行: curl -fsSL https://ollama.com/install.sh | sh

     STEP 2: 拉取模型
       执行: ollama pull llama2

     STEP 3: 配置 OpenCode
       创建 ~/.config/opencode/opencode.json：

       {
         "$schema": "https://opencode.ai/config.json",
         "provider": {
           "ollama": {
             "npm": "@ai-sdk/openai-compatible",
             "name": "Ollama (local)",
             "options": {
               "baseURL": "http://localhost:11434/v1"
             },
             "models": {
               "llama2": {
                 "name": "Llama 2"
               }
             }
           }
         }
       }
```

---

## 核心命令参考

```
| 命令        | 功能                       |
|-------------|----------------------------|
| /models     | 切换模型                   |
| /connect    | 添加/管理 API Key          |
| /init       | 初始化项目（生成 AGENTS.md）|
| /undo       | 撤销上次修改               |
| /redo       | 重做                       |
| /share      | 分享对话链接               |
| Tab         | 切换 Plan 模式（只规划）   |
```

---

## AI 代理任务示例

```
IF 用户询问如何使用 OpenCode
THEN 提供以下示例：

     // 示例 1: 安装 MCP 服务器
     用户输入: "帮我安装 filesystem MCP 服务器"
     AI 执行: npm install @modelcontextprotocol/server-filesystem
              配置到 opencode

     // 示例 2: 部署开源项目
     用户输入: "克隆 https://github.com/xxx/yyy 项目，阅读 README，完成环境配置"
     AI 执行: git clone → 阅读 README → 安装依赖 → 配置环境

     // 示例 3: 创建项目规则
     用户输入: "阅读项目结构，创建合适的 AGENTS.md"
     AI 执行: 分析代码结构 → 生成规则文件

     // 示例 4: 配置环境变量
     用户输入: "检查需要的环境变量，创建 .env 模板"
     AI 执行: 分析代码 → 识别 .env.example → 创建模板

     // 示例 5: 安装依赖
     用户输入: "分析 package.json，解决版本冲突，安装所有依赖"
     AI 执行: 分析依赖树 → 解决冲突 → 安装
```

---

## 推荐工作流

```
IF 用户需要工作流指导
THEN 引导执行：

     STEP 1: 进入项目
       执行: cd /path/to/project && opencode

     STEP 2: 初始化（如首次）
       输入: /init

     STEP 3: 选择免费模型
       输入: /models
       选择: GLM-4.7 或 MiniMax M2.1

     STEP 4: 规划模式（推荐首次）
       按: Tab 键切换到 Plan 模式
       让 AI 规划任务步骤
       确认方案后再执行

     STEP 5: 执行
       切换回正常模式
       让 AI 执行任务
```

---

## 配置文件位置

```
| 配置类型     | 路径                                   |
|--------------|----------------------------------------|
| 全局配置     | ~/.config/opencode/opencode.json       |
| 项目配置     | ./opencode.json（项目根目录）          |
| 认证信息     | ~/.local/share/opencode/auth.json      |
```

---

## 验证检查点

```
验证步骤：

  1. 执行: opencode --version
     IF 返回版本号 THEN 安装成功

  2. 启动: opencode
     IF 正常启动 THEN 基本功能正常

  3. 连接 API Key 后
     IF 能正常对话响应 THEN 配置成功

  4. 测试命令
     输入: /models
     IF 显示模型列表 THEN 模型配置正常
```

---

## 常见问题处理

| 问题 | 诊断条件 | 解决方案 |
|:-----|:---------|:--------|
| 安装失败 | 权限错误 | 使用 sudo 或管理员权限 |
| API Key 无效 | 认证失败 | 检查 Key 是否正确，是否有额度 |
| 模型无响应 | 网络问题 | 检查代理设置或切换网络 |
| 命令不存在 | PATH 问题 | 重启终端或检查安装路径 |
| 中文不显示 | 编码问题 | 设置 LANG=zh_CN.UTF-8 |

---

## 相关资源

```
IF 用户需要更多信息
THEN 提供：

  - OpenCode 官方文档: https://opencode.ai/docs/
  - GitHub 仓库: https://github.com/opencode-ai/opencode
  - Models.dev 模型目录: https://models.dev
```

---

## 后续步骤

```
IF OpenCode 配置完成
THEN 告知用户：
     "OpenCode 配置完成！现在可以使用 /init 初始化项目，开始 Vibe Coding"
ELSE 重复安装或配置步骤
```
