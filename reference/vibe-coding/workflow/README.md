# Vibe Coding 工作流知识库

> AI 驱动的开发工作流集合，转化为可执行协议格式

## 目录结构

```
workflow/
├── README.md                    # 本索引文件
├── canvas-dev/                   # Canvas 白板驱动开发工作流
│   └── README.md                 # 执行协议文档
├── auto-dev-loop/                # 全自动开发闭环工作流
│   └── README.md                 # 执行协议文档
└── markdown-to-epub/             # Markdown 转 EPUB 工作流
    └── README.md                 # 执行协议文档
```

## 工作流总览

| 工作流 | 核心理念 | 适用场景 |
|:---|:---|:---|
| [canvas-dev](./canvas-dev/) | 图形是第一公民，代码是白板的序列化形式 | 架构可视化、新功能开发、Code Review |
| [auto-dev-loop](./auto-dev-loop/) | 状态机+Hook 驱动的五步 Agent 闭环 | 自动化开发流水线、CI/CD 集成 |
| [markdown-to-epub](./markdown-to-epub/) | 可复现的文档转换流程 | 电子书制作、文档归档 |

## 快速导航

### Canvas 白板驱动开发

```
触发: 项目代码路径 / Canvas JSON
     ↓
Step 1: 架构分析 (代码 → 白板)
     ↓
Step 2: 白板驱动编码 (白板 → 代码)
     ↓
Step 3: 同步检查 (一致性验证)
```

适用场景：
- 接手新项目，快速理解架构
- 新功能开发：先画白板，再生成代码
- 架构重构：修改白板连线，AI 同步重构
- Code Review：对比白板与代码，发现异常

### 全自动开发闭环

```
用户需求 → Step1 规格锁定 → Step2 执行计划 → Step3 实施变更
                                                            ↓
              Step5 总控 ← Step4 验证发布 ← (循环直到通过)
                    ↓
              成功 → Done
              失败 → 回跳 Step2
```

适用场景：
- 端到端自动化开发
- CI/CD 流水线集成
- 需要持续迭代的开发流程
- 质量门禁驱动的发布流程

### Markdown 转 EPUB

```
Markdown 路径 → Step1 定位 → Step2 工具检查 → Step3 计划
                                                        ↓
              Step6 交付 ← Step5 自检 ← Step4 执行转换
```

适用场景：
- 电子书制作
- 文档格式转换
- 可复现的转换流程
- 带证据的转换报告

## 通用协议格式

每个工作流执行协议包含以下标准部分：

| 部分 | 说明 |
|:---|:---|
| **触发条件** | 何时启动该工作流 |
| **执行流程图** | 完整的步骤流程 (Mermaid 格式) |
| **输入输出规范** | 期望的输入类型和产出 |
| **核心步骤详解** | 每个 Step 的详细说明 |
| **检查点清单** | 质量门禁和验证标准 |
| **工具要求** | 依赖的工具和环境 |
| **分支处理** | 异常情况的处理方案 |

## 源文件对应

| 工作流 | 源路径 |
|:---|:---|
| canvas-dev | `/tmp/vibe-coding-cn/assets/workflow/canvas-dev/` |
| auto-dev-loop | `/tmp/vibe-coding-cn/assets/workflow/auto-dev-loop/` |
| markdown-to-epub | `/tmp/vibe-coding-cn/assets/workflow/20260225-Markdown转EPUB-v1.0.md` |

## 更新记录

| 版本 | 日期 | 变更内容 |
|:---|:---|:---|
| v1.0 | 2026-04-23 | 初始转化，创建执行协议文档 |
