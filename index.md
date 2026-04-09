# 知识库索引

## 话题列表

[[NeoForge开发认知]] - NeoForge 模组开发框架认知（讨论沉淀）
[[NeoForge-入门]] - 环境配置、项目结构、版本规范
[[NeoForge-概念]] - 注册表、事件系统、物理端/逻辑端
[[NeoForge-方块]] - 方块注册、BlockState、自定义方块
[[NeoForge-物品]] - 物品注册、Data Components、工具盔甲
[[NeoForge-实体]] - EntityType、实体生成、投射物
[[NeoForge-方块实体]] - BlockEntity 创建、数据存储、同步
[[NeoForge-网络]] - Payload 网络通信、数据包
[[NeoForge-资源]] - 模型、纹理、语言文件、数据生成
[[NeoForge-高级]] - 高级话题（Capability、Mixins等）

## NeoForge 详细文档

### Getting Started（入门）
- [[NeoForge-入门]] - 环境配置、项目结构、版本规范

### Concepts（概念）
- [[NeoForge-概念]] - 注册表、事件系统、物理端/逻辑端

### Blocks（方块）
- [[NeoForge-方块]] - 方块注册与基础
- [[NeoForge-方块-状态]] - Blockstates 方块状态系统

### Items（物品）
- [[NeoForge-物品]] - 物品注册与基础
- [[NeoForge-物品-交互]] - 物品交互（右键/左键）
- [[NeoForge-物品-数据组件]] - 数据组件系统
- [[NeoForge-物品-消耗品]] - 消耗品与食物
- [[NeoForge-物品-工具]] - 工具制作
- [[NeoForge-物品-护甲]] - 护甲制作
- [[NeoForge-物品-状态效果]] - 状态效果与药水

### Entities（实体）
- [[NeoForge-实体]] - 实体注册与基础
- [[NeoForge-实体-LivingEntity]] - 生物/玩家逻辑
- [[NeoForge-实体-数据]] - 实体数据与网络同步
- [[NeoForge-实体-属性]] - 属性系统
- [[NeoForge-实体-渲染器]] - 实体渲染器

### Block Entities（方块实体）
- [[NeoForge-方块实体]] - 方块实体基础
- [[NeoForge-方块实体-渲染器]] - BlockEntityRenderer 渲染器

### Resources - Client（客户端资源）
- [[NeoForge-客户端资源]] - 客户端资源总览
- [[NeoForge-客户端-国际化]] - 国际化与本地化
- [[NeoForge-资源-纹理]] - 纹理系统（PNG、动画、元数据）
- [[NeoForge-资源-模型]] - 模型定义（JSON 模型、Blockstates）
- [[NeoForge-客户端-粒子]] - 粒子系统
- [[NeoForge-资源-音效]] - 音效系统（SoundEvent、sounds.json）

### Resources - Server（服务端资源）
- [[NeoForge-服务端资源]] - 服务端资源总览
- [[NeoForge-服务端-进度]] - 进度系统（Advancements、Criteria）
- [[NeoForge-服务端-伤害类型]] - 伤害类型系统
- [[NeoForge-服务端-数据映射]] - Data Maps 数据映射
- [[NeoForge-服务端-附魔]] - 附魔系统
- [[NeoForge-服务端-战利品表]] - 战利品表系统
- [[NeoForge-服务端-配方]] - 配方系统（Recipes、RecipeSerializer）
- [[NeoForge-服务端-标签]] - 标签系统（Tags、TagKey）

### Networking（网络）
- [[NeoForge-网络]] - 网络通信基础
- [[NeoForge-网络-Payload]] - Payload 注册详解
- [[NeoForge-网络-流编解码器]] - StreamCodecs 流编解码器

### Inventories & Transfers（物品栏与传输）
- [[NeoForge-物品栏-容器]] - Container 容器系统

### Data Storage（数据存储）
- [[NeoForge-数据存储-附件]] - 数据附件系统
- [[NeoForge-数据存储-编解码器]] - Codecs 编解码器
- [[NeoForge-数据存储-值IO]] - Value I/O 值读写

### Worldgen（世界生成）
- [[NeoForge-世界生成-地物]] - Features 地物系统
- [[NeoForge-世界生成-生物群系修改器]] - Biome Modifiers 生物群系修改器
- [[NeoForge-世界生成-结构]] - Structures 结构系统
- [[NeoForge-世界生成-维度]] - Dimensions 维度系统

### Rendering（渲染）
- [[NeoForge-渲染-特性]] - Rendering Features 渲染特性
- [[NeoForge-渲染-着色器]] - Shaders 着色器

### Advanced Topics（高级主题）
- [[NeoForge-高级]] - 高级话题总览
- [[NeoForge-高级-访问转换器]] - Access Transformers 访问转换器
- [[NeoForge-高级-可扩展枚举]] - Extensible Enums 可扩展枚举
- [[NeoForge-高级-特性标志]] - Feature Flags 特性标志

### Miscellaneous（杂项）
- [[NeoForge-杂项-游戏测试]] - 游戏测试框架
- [[NeoForge-杂项-更新检查器]] - 更新检查器

## 关键词映射

### 基础概念
- 注册 → NeoForge-概念
- 事件 → NeoForge-概念
- DeferredRegister → NeoForge-概念
- 端/Side → NeoForge-概念

### 方块与物品
- 方块 → NeoForge-方块
- Blockstate → NeoForge-方块-状态
- 物品 → NeoForge-物品
- 交互 → NeoForge-物品-交互
- DataComponent → NeoForge-物品-数据组件
- 消耗品/食物 → NeoForge-物品-消耗品
- 工具 → NeoForge-物品-工具
- 护甲 → NeoForge-物品-护甲
- 状态效果/药水 → NeoForge-物品-状态效果

### 实体
- 实体 → NeoForge-实体
- LivingEntity → NeoForge-实体-LivingEntity
- 属性 → NeoForge-实体-属性
- 渲染器 → NeoForge-实体-渲染器

### 方块实体
- BlockEntity → NeoForge-方块实体
- BER → NeoForge-方块实体-渲染器

### 资源
- 模型/纹理 → NeoForge-资源-纹理 / NeoForge-资源-模型
- 数据生成 → NeoForge-资源
- 音效 → NeoForge-资源-音效
- 国际化 → NeoForge-客户端-国际化
- 粒子 → NeoForge-客户端-粒子

### 服务端资源
- 进度/Advancement → NeoForge-服务端-进度
- 战利品表 → NeoForge-服务端-战利品表
- 伤害类型 → NeoForge-服务端-伤害类型
- Data Map → NeoForge-服务端-数据映射
- 附魔 → NeoForge-服务端-附魔
- 配方 → NeoForge-服务端-配方
- 标签/Tag → NeoForge-服务端-标签

### 网络
- 网络 → NeoForge-网络
- Payload → NeoForge-网络-Payload
- StreamCodec → NeoForge-网络-流编解码器

### 物品栏
- Container → NeoForge-物品栏-容器

### 数据存储
- Codec → NeoForge-数据存储-编解码器
- Value I/O → NeoForge-数据存储-值IO
- Attachment → NeoForge-数据存储-附件

### 世界生成
- 地物/Feature → NeoForge-世界生成-地物
- 生物群系 → NeoForge-世界生成-生物群系修改器
- 结构/Structure → NeoForge-世界生成-结构
- 维度/Dimension → NeoForge-世界生成-维度

### 渲染
- 渲染特性 → NeoForge-渲染-特性
- 着色器/Shader → NeoForge-渲染-着色器

### 高级主题
- Access Transformer → NeoForge-高级-访问转换器
- Extensible Enum → NeoForge-高级-可扩展枚举
- Feature Flag → NeoForge-高级-特性标志

### 杂项
- 游戏测试 → NeoForge-杂项-游戏测试
- 更新检查 → NeoForge-杂项-更新检查器
