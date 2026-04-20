# Minecraft 机制：方块 (Block)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/方块](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97)  
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+  
> **本地更新时间**：2026-04-20  

---

## 模组开发核心要点 (Modding Priorities)

在 NeoForge 开发中，方块 (Block) 构成了世界的基础，且在 1.21+ 进一步规范了其数据驱动 (Data-Driven) 机制和组件系统。

### 1. 注册表与标识符
- **注册表名称**：`minecraft:block` (在 NeoForge 中通过 `Registries.BLOCK` 或 `DeferredRegister.createBlocks` 进行注册和访问)。
- **命名空间**：原版方块的 ResourceLocation 均为 `minecraft:<block_name>`（例如 `minecraft:stone`）。
- **方块物品 (BlockItem)**：方块注册后本身并不会在物品栏中出现，必须同时在 `minecraft:item` 注册表中注册对应的 `BlockItem`，玩家才能在物品栏持有和放置该方块。

### 2. 数据驱动的方块定义 (JSON 结构)
方块的视觉与掉落物表现高度依赖数据包 (Datapack) 和资源包 (Resourcepack) 中的 JSON 文件：
- **方块状态 (Blockstates)** (`assets/<namespace>/blockstates/`)：决定方块在不同状态（如朝向、是否充能）下使用哪个三维模型。
- **方块模型 (Models)** (`assets/<namespace>/models/block/`)：定义方块的几何形状与引用的纹理贴图。
- **战利品表 (Loot Tables)** (`data/<namespace>/loot_table/blocks/`)：决定方块被破坏后的掉落物。如果未定义，方块被破坏后将**不掉落任何物品**。
- **方块标签 (Block Tags)** (`data/minecraft/tags/block/`)：用于逻辑判断。1.21+ 中，决定方块采掘等级（如 `#minecraft:needs_iron_tool`）和适配工具（如 `#minecraft:mineable/pickaxe`）完全依赖标签。

### 3. 常见开发与交互场景
- **创建基础方块**：
  - 继承 `Block` 类，在构造函数中传入 `BlockBehaviour.Properties`（通常通过 `BlockBehaviour.Properties.of()` 创建，可设置硬度 `destroyTime`、抗爆性 `explosionResistance`、声音 `sound`、是否发光 `lightLevel` 等）。
- **方块交互 (右键点击)**：
  - 重写 `useWithoutItem` (处理空手或非特定物品交互) 和 `useItemOn` (处理持物品交互)。返回 `ItemActionResult.SUCCESS` 或 `InteractionResult.SUCCESS` 代表交互成功。
- **自定义碰撞与形状**：
  - 默认方块为 1x1x1 完整正方体。若需自定义（如台阶、楼梯），需重写 `getShape`（光线追踪/轮廓形状）和 `getCollisionShape`（实体碰撞形状），返回 `VoxelShape`。
- **方块实体 (Block Entity)**：
  - 如果方块需要存储额外数据（如箱子物品、熔炉烧炼进度）或每刻执行逻辑（Tick），需要实现 `EntityBlock` 接口并关联一个 `BlockEntity`，同时注册对应的 `BlockEntityType`。

### 4. 开发避坑指南
- **方块状态属性必须注册**：如果你在自定义方块中使用了 `BooleanProperty`、`DirectionProperty` 等状态属性，必须重写 `createBlockStateDefinition` 并通过 `builder.add()` 注册这些属性，否则游戏启动时会崩溃。
- **默认状态设置**：在方块类的构造函数中，记得调用 `this.registerDefaultState(...)` 设置初始方块状态。
- **工具挖掘掉落判定**：不要在代码中硬编码挖掘工具逻辑。必须通过在 `data/<namespace>/tags/block/mineable/` 下的 JSON 中添加标签，方块才会正确被工具挖掘和掉落。

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体数值或冗长表格，请直接通过以下锚点跳转至 Wiki 原文查阅。

### 1. 机制基础
- [方块行为](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97#%E8%A1%8C%E4%B8%BA) *(受重力影响、发光、空气方块机制、声音与粒子)*
- [方块高度与判定箱](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97#%E6%96%B9%E5%9D%97%E9%AB%98%E5%BA%A6) *(完整方块与不完整方块的碰撞差)*
- [方块纹理与模型](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97#%E7%BA%B9%E7%90%86) *(静态纹理与动态纹理)*

### 2. 相关方块机制
- [方块物品 (Block Item)](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E7%89%A9%E5%93%81) *(方块在物品栏中的形态)*
- [下落的方块 (Falling Block)](https://zh.minecraft.wiki/w/%E4%B8%8B%E8%90%BD%E7%9A%84%E6%96%B9%E5%9D%97) *(沙子、沙砾等受重力影响的机制)*

### 3. 方块数据字典 (超长表格)
> **[点击查看所有原版方块完整列表](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97#%E6%96%B9%E5%9D%97%E5%88%97%E8%A1%A8)**

*速查提示：原版方块的命名空间 ID 形式为 `minecraft:<英文名>`。*
*例如：*
- *石头 (Stone): `minecraft:stone`*
- *橡木原木 (Oak Log): `minecraft:oak_log`*
- *命令方块 (Command Block): `minecraft:command_block`*

---

## 相关资源与材质 (Assets)

如果需要为自定义方块提供材质或模型参考，以下是原版相关资产的定位信息：

- **方块纹理 (Textures)**：`assets/minecraft/textures/block/`
- **方块模型 (Models)**：`assets/minecraft/models/block/`
- **方块状态 (Blockstates)**：`assets/minecraft/blockstates/`
- **默认方块战利品表 (Loot Tables)**：`data/minecraft/loot_table/blocks/`
