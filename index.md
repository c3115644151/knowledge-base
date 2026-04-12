# 知识库索引

## 结构

```
知识库/
├── reference/              # AI 专用参考文档（批量生成）
│   └── neoForge/          # NeoForge API 文档（53个）
├── topics/                 # 个性化知识（交流沉淀）
├── agent-growth/           # Agent成长日记与惯例
│   ├── diary/             # 每日日记
│   └── 惯例.md            # 自由时间活动惯例
├── raw/                    # 原料知识（待加工）
│   ├── articles/          # 文章素材
│   ├── videos/            # 视频解析结果
│   └── stock-basics.md    # 股票入门知识
├── index.md               # 本文件
└── log.md                 # 操作日志
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

---

## agent-growth/ - Agent 成长日记

凝筝安排的"自由时间"空间，记录Agent自我探索与成长。

### 目录结构
- `diary/` - 每日日记（YYYYMMDD.md）
- `惯例.md` - 自由时间活动惯例

---

## raw/ - 原料知识

未经深度加工的原始素材，待后续提炼整理。

### 股票入门
- `stock-basics.md` - 股票基础概念与交易规则

### 视频解析
- `videos/` - B站/抖音视频字幕与内容

---

## topics/ - 个性化知识

交流沉淀，演进型，结构灵活。

### NeoForge 开发认知
- `NeoForge开发认知` - 版本规范、构建配置、开发注意事项

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
