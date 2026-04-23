# Vibe Coding 入门指南索引

> AI 引导用户按顺序完成 Vibe Coding 环境配置

---

## 学习路径

```
执行顺序：

  1. [Vibe Coding 哲学原理](./01_Vibe_Coding_哲学原理.md)
     └─ 理解核心理念和思维模式

  2. [网络环境配置](./01_网络环境配置.md)
     └─ 配置网络访问（GitHub/Google/Claude）
     └─ 前置条件：操作系统确认 + 代理订阅

  3. [开发环境搭建](./02_开发环境搭建.md)
     └─ 根据操作系统搭建开发环境
     └─ 前置条件：网络已配置
     └─ 选择：Windows(WSL2/原生)/macOS/Linux

  4. [IDE配置](./03_IDE配置.md)
     └─ 配置代码编辑器
     └─ 前置条件：开发环境已搭建
     └─ 选择：VS Code/Cursor/Windsurf

  5. [OpenCode CLI配置](./04_OpenCode-CLI配置.md)
     └─ 安装免费 AI CLI 工具（可选）
     └─ 配置免费模型（GLM-4.7/M2.1）

  6. [开始第一个项目](../playbook/快速启动指南.md)
     └─ 动手实践
```

---

## 快速配置流程（推荐顺序）

```
IF 用户需要快速开始
THEN 引导执行：

  [Step 1] 确认操作系统
    ├─ Windows → WSL2 推荐
    ├─ macOS   → Homebrew
    └─ Linux   → apt/nvm

  [Step 2] 配置网络（如需要）
    └─ 参考网络环境配置协议

  [Step 3] 安装基础工具
    ├─ Node.js (nvm)
    ├─ Git
    └─ AI CLI (opencode.ai)

  [Step 4] 配置 IDE
    └─ VS Code + 扩展

  [Step 5] 开始编程
    └─ 使用 AI 指导完成第一个项目
```

---

## 协议文件清单

```
知识库/reference/vibe-coding/guides/getting-started/
│
├── 01_网络环境配置.md    # 网络代理配置协议
├── 02_开发环境搭建.md    # 开发环境配置协议
├── 03_IDE配置.md         # IDE 配置协议
├── 04_OpenCode-CLI配置.md # 免费 CLI 工具协议
└── README.md             # 本索引文件
```

---

## AI 执行要点

```
WHEN AI 接收到用户请求配置环境
THEN 执行以下协议：

  1. 首先确认用户操作系统和当前状态
  2. 按顺序引导用户完成前置检查
  3. 根据用户选择（WSL/原生/IDE类型）执行对应分支
  4. 每步完成后验证，再进行下一步
  5. 遇到问题时查询常见问题处理表

  示例对话：
    用户: "我想配置开发环境"
    AI:   "请问你使用什么操作系统？(Windows/macOS/Linux)"
    用户: "Windows"
    AI:   "你更倾向于使用 WSL2（推荐）还是 Windows 原生环境？"
    用户: "WSL2"
    AI:   "好的，让我们开始 WSL2 开发环境配置..."
```

---

## 相关知识库路径

```
├── principles/fundamentals/  # 核心理念
│   ├── Vibe_Coding_哲学原理.md
│   └── 核心概念定义.md
│
├── playbook/                  # 方法论
│   ├── 快速启动指南.md
│   └── 工具与经验.md
│
└── case-studies/              # 实战案例
    └── 项目实践.md
```
