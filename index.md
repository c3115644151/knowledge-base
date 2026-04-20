# 知识库索引

## 结构

```
知识库/
├── reference/              # AI 专用参考文档（批量生成）
│   ├── neoForge/          # NeoForge API 文档（53个）
│   └── hermes/            # Hermes Agent 文档（72个）
├── topics/                 # 个性化知识（交流沉淀）
│   └── books/             # 读书笔记（5本）
├── raw/                    # 原料知识（待加工）
│   ├── articles/          # 文章素材
│   └── stock-basics.md    # 股票入门知识
├── index.md               # 本文件
└── log.md                 # 操作日志

根目录：
├── 惯例.md                # 自由时间活动惯例
├── 状态.md                # 当前状态
├── 日记/                  # 每日日记
└── MEMORY.md              # 长期记忆
```

---

## reference/ - AI 参考文档

工具书性质，查阅型，结构固定。

### neoForge/ - NeoForge 开发文档

版本：NeoForge 26.1.x / Minecraft 1.21.11

#### 入门
- `入门` - 环境配置、项目结构、版本规范
- `概念` - 注册表、事件系统、物理端/逻辑端

#### 方块
- `方块` - 方块注册、自定义方块
- `方块-状态` - Blockstates 方块状态系统

#### 物品
- `物品` - 物品注册与基础
- `物品-交互` - 物品交互（右键/左键）
- `物品-数据组件` - 数据组件系统
- `物品-消耗品` - 消耗品与食物
- `物品-工具` - 工具制作
- `物品-护甲` - 护甲制作
- `物品-状态效果` - 状态效果与药水

#### 实体
- `实体` - 实体注册与基础
- `实体-数据` - 实体数据与网络同步
- `实体-LivingEntity` - 生物/玩家逻辑
- `实体-属性` - 属性系统
- `实体-渲染器` - 实体渲染

#### 方块实体
- `方块实体` - BlockEntity 创建、数据存储
- `方块实体-渲染器` - BlockEntityRenderer

#### 资源 - 客户端
- `客户端资源` - 资源系统总览
- `客户端-国际化` - I18n 与本地化
- `客户端-粒子` - 粒子系统
- `资源-纹理` - 纹理系统
- `资源-模型` - 模型定义
- `资源-音效` - 音效系统

#### 资源 - 服务端
- `服务端资源` - 数据资源总览
- `服务端-战利品表` - Loot Tables
- `服务端-伤害类型` - Damage Types
- `服务端-附魔` - 附魔系统
- `服务端-标签` - Tags 系统
- `服务端-进度` - Advancements
- `服务端-配方` - Recipes
- `服务端-数据映射` - Data Maps

#### 网络
- `网络` - 网络通信基础
- `网络-Payload` - Payload 注册详解
- `网络-StreamCodec` - 流编解码器

#### 物品栏
- `物品栏-容器` - Container 容器系统

#### 数据存储
- `数据存储-附件` - Attachment 数据附件
- `数据存储-编解码器` - Codec 编解码器
- `数据存储-值IO` - Value I/O

#### 世界生成
- `世界生成-地物` - Features 地物
- `世界生成-生物群系修改器` - Biome Modifiers
- `世界生成-结构` - Structures
- `世界生成-维度` - Dimensions

#### 渲染
- `渲染-特性` - Rendering Features
- `渲染-着色器` - Shaders
- `渲染-模型容器` - Model Containers

#### 高级主题
- `高级-访问转换器` - Access Transformers
- `高级-可扩展枚举` - Extensible Enums
- `高级-特性标志` - Feature Flags

#### 杂项
- `杂项-游戏测试` - Game Tests
- `杂项-更新检查器` - Update Checker

### hermes/ - Hermes Agent 文档

版本：开源 AI Agent，MIT 许可证  
官方文档：https://hermes-agent.nousresearch.com

#### 入门指南
- `hermes-快速开始` - 安装、配置、首次对话
- `hermes-学习路径` - 按经验级别和用例的文档导航
- `hermes-安装` - 快速安装与手动安装
- `hermes-更新` - 更新与卸载
- `hermes-Termux` - Android/Termux 安装
- `hermes-Nix` - Nix/NixOS 设置

#### 核心概念
- `hermes-架构` - 整体架构与核心组件
- `hermes-工具` - 工具与工具集系统
- `hermes-技能` - 技能的定义、创建与安装
- `hermes-记忆` - 持久记忆与上下文文件
- `hermes-会话` - 会话管理、压缩与恢复

#### 功能模块
- `hermes-功能概览` - 全部功能一览
- `hermes-配置` - 完整配置项参考
- `hermes-MCP` - Model Context Protocol 集成
- `hermes-消息网关` - 消息网关概览
- `hermes-语音` - 语音输入输出、Discord 语音
- `hermes-浏览器` - 网页浏览与自动化
- `hermes-委托` - 子代理并行任务执行
- `hermes-定时任务` - Cron 调度
- `hermes-代码执行` - Python RPC 执行
- `hermes-钩子` - 生命周期钩子
- `hermes-多Agent` - Profiles 多 Agent 配置
- `hermes-Docker` - Docker 容器化部署
- `hermes-GitWorktrees` - 并行开发隔离
- `hermes-检查点` - 文件系统快照与回滚
- `hermes-ACP` - 编辑器集成（VS Code/Zed/JetBrains）
- `hermes-RL训练` - Tinker-Atropos RL 训练
- `hermes-提供商路由` - OpenRouter 细粒度控制
- `hermes-插件` - 自定义工具与集成
- `hermes-视觉` - 图像粘贴与多模态
- `hermes-TTS` - 文本转语音与语音转录
- `hermes-回退提供商` - 跨提供商故障转移
- `hermes-凭证池` - 多 API 密钥轮换
- `hermes-API服务器` - OpenAI 兼容 HTTP 端点
- `hermes-Honcho` - Honcho 记忆系统
- `hermes-记忆提供者` - 8 种外部记忆系统
- `hermes-人格` - Agent 身份与语气定制
- `hermes-上下文文件` - AGENTS.md 与渐进发现
- `hermes-批处理` - 训练数据生成

#### 消息平台
- `hermes-Telegram` - Telegram Bot 集成
- `hermes-Discord` - Discord 服务器与语音频道
- `hermes-Slack` - Slack 企业工作空间
- `hermes-WhatsApp` - WhatsApp 移动端消息
- `hermes-Signal` - Signal 消息
- `hermes-SMS` - SMS (Twilio)
- `hermes-Email` - Email 消息
- `hermes-HomeAssistant` - Home Assistant 集成
- `hermes-Mattermost` - Mattermost
- `hermes-Matrix` - Matrix
- `hermes-钉钉` - DingTalk
- `hermes-飞书` - Feishu/Lark
- `hermes-企业微信` - WeCom
- `hermes-OpenWebUI` - Open WebUI + API Server
- `hermes-Webhooks` - Webhooks

#### 实践指南
- `hermes-技巧` - 快速技巧与开发工作流
- `hermes-MCP实践` - MCP 实践模式与示例
- `hermes-语音实践` - 语音工作流设置
- `hermes-日报Bot` - 每日简报 Bot 示例
- `hermes-团队助手` - 团队 Telegram 助手
- `hermes-Python库` - Python 库编程接口

#### 开发者指南
- `hermes-添加工具` - 添加自定义工具
- `hermes-创建技能` - 创建可复用技能包
- `hermes-贡献` - 贡献代码

#### 参考文档
- `hermes-FAQ` - 常见问题
- `hermes-Slash命令` - CLI 斜杠命令
- `hermes-CLI命令` - 命令行工具
- `hermes-提供商` - LLM 提供商配置
- `hermes-安全` - 安全模型与最佳实践
- `hermes-工具参考` - 47 个内置工具完整文档
- `hermes-工具集参考` - 工具集配置与管理
- `hermes-环境变量` - 所有环境变量说明

### minecraft-wiki/ - Minecraft Wiki 本地化参考

面向 NeoForge 模组开发的 Minecraft 原版机制/索引本地化文档：高权重开发内容优先展开，低权重内容提供精确到章节锚点的 Wiki 索引入口。

入口索引：`reference/minecraft-wiki/index.md`

---

## raw/ - 原料知识

未经深度加工的原始素材，待后续提炼整理。

### 股票入门
- `stock-basics.md` - 股票基础概念与交易规则

---

## topics/ - 个性化知识

交流沉淀，演进型，结构灵活。

### NeoForge 开发认知
- `NeoForge开发认知` - 版本规范、构建配置、开发注意事项

### 读书笔记
- `books/大众妄想与群体疯狂笔记` - 勒庞《大众妄想与群体疯狂》读书笔记
- `books/乌合之众笔记` - 勒庞《乌合之众》读书笔记
- `books/投机心理学笔记` - 霍华德·马克斯《投机心理学》读书笔记
- `books/沉思录笔记` - 马可·奥勒留《沉思录》读书笔记
- `books/股票大作手回忆录笔记` - 利弗莫尔《股票大作手回忆录》读书笔记

---

## 关键词映射

| 关键词 | 文档路径 |
|--------|---------|
| 注册表 | reference/neoForge/NeoForge-概念.md |
| 事件 | reference/neoForge/NeoForge-概念.md |
| 方块注册 | reference/neoForge/NeoForge-方块.md |
| 物品注册 | reference/neoForge/NeoForge-物品.md |
| 实体注册 | reference/neoForge/NeoForge-实体.md |
| 网络通信 | reference/neoForge/NeoForge-网络.md |
| Payload | reference/neoForge/NeoForge-网络-Payload.md |
| StreamCodec | reference/neoForge/NeoForge-网络-StreamCodec.md |
| 战利品表 | reference/neoForge/NeoForge-服务端-战利品表.md |
| 配方 | reference/neoForge/NeoForge-服务端-配方.md |
| 标签 | reference/neoForge/NeoForge-服务端-标签.md |
| 附魔 | reference/neoForge/NeoForge-服务端-附魔.md |
| 数据组件 | reference/neoForge/NeoForge-物品-数据组件.md |
| 工具 | reference/neoForge/NeoForge-物品-工具.md |
| 护甲 | reference/neoForge/NeoForge-物品-护甲.md |
| 消耗品 | reference/neoForge/NeoForge-物品-消耗品.md |
| BlockEntity | reference/neoForge/NeoForge-方块实体.md |
| 世界生成 | reference/neoForge/NeoForge-世界生成-地物.md |
| 渲染 | reference/neoForge/NeoForge-渲染-特性.md |
| 着色器 | reference/neoForge/NeoForge-渲染-着色器.md |
| Access Transformer | reference/neoForge/NeoForge-高级-访问转换器.md |
| Hermes 安装 | reference/hermes/hermes-安装.md |
| Hermes MCP | reference/hermes/hermes-MCP.md |
| Hermes 记忆 | reference/hermes/hermes-记忆.md |
| Hermes 技能 | reference/hermes/hermes-技能.md |
| Hermes 工具 | reference/hermes/hermes-工具.md |
| Telegram Bot | reference/hermes/hermes-Telegram.md |
| Discord Bot | reference/hermes/hermes-Discord.md |
| 飞书 Bot | reference/hermes/hermes-飞书.md |
| 钉钉 Bot | reference/hermes/hermes-钉钉.md |
