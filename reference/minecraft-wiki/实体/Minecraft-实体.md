# Minecraft 机制：实体 (Entity)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/实体](https://zh.minecraft.wiki/w/%E5%AE%9E%E4%BD%93)  
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+  
> **本地更新时间**：2026-04-20  

---

## 模组开发核心要点 (Modding Priorities)

实体 (Entity) 代表 Minecraft 世界中所有动态的、移动中的对象，从玩家、生物到掉落物和弹射物。在 NeoForge 1.21+ 中，实体系统的开发趋于规范化，特别是属性 (Attributes) 和数据同步 (Data Sync) 方面。

### 1. 注册表与标识符
- **注册表名称**：`minecraft:entity_type` (在 NeoForge 中通过 `Registries.ENTITY_TYPE` 或 `DeferredRegister.createEntityTypes` 访问)。
- **实体类型 (EntityType)**：使用 `EntityType.Builder.of(EntityClass::new, MobCategory)` 构建。定义了实体的碰撞箱尺寸 (`sized()`)、更新频率 (`clientTrackingRange()`, `updateInterval()`) 以及分类 (`MobCategory` 如 `MONSTER`, `CREATURE`, `MISC`)。

### 2. 实体分类与核心类层次
- **`Entity`**：所有实体的基类（如矿车、船、弹射物、掉落物）。
- **`LivingEntity`**：具有生命值、状态效果、护甲和装备槽的实体。
- **`Mob`**：由 AI 驱动的生物。
- **`PathfinderMob`**：能够使用导航 (Pathfinding) 寻路的生物。
- **`Animal` / `Monster`**：具体的动物（可繁殖）或怪物（具攻击性）基类。

### 3. 常见开发与交互场景
- **生物属性 (Attributes) 注册**：
  - 1.21+ 中，所有 `LivingEntity` 必须在启动时注册其默认属性（如最大生命值、移动速度、攻击伤害）。
  - 监听 `EntityAttributeCreationEvent` 事件，使用 `event.put(CustomEntityType.get(), CustomEntity.createAttributes().build())` 注册。
- **实体 AI 与目标 (Goals)**：
  - 在 `registerGoals()` 中添加 AI 行为。
  - `goalSelector.addGoal(priority, new ...)`：如 `MeleeAttackGoal` (近战攻击), `WaterAvoidingRandomStrollGoal` (随机游走)。
  - `targetSelector.addGoal(...)`：如 `NearestAttackableTargetGoal` (寻找目标)。
- **附加数据 (Attachment 系统)**：
  - 1.20.4+ 引入，取代了旧版的 Capabilities 系统用于存储实体的自定义持久化数据。
  - 注册 `AttachmentType`，通过 `entity.getData(ATTACHMENT_TYPE)` 和 `entity.setData(ATTACHMENT_TYPE, value)` 操作。
- **渲染与模型**：
  - 客户端特有。监听 `EntityRenderersEvent.RegisterRenderers` 绑定 `EntityRenderer`。
  - 监听 `EntityRenderersEvent.RegisterLayerDefinitions` 注册实体的几何模型层次 (Model Layer)。

### 4. 开发避坑指南
- **服务端与客户端分离**：实体同时存在于服务端 (`level.isClientSide == false`) 和客户端。逻辑运算（如伤害、生命值扣除、AI）**只能**在服务端进行。
- **数据同步 (EntityDataAccessor)**：如果需要客户端知道实体的某些状态（用于渲染动画等），必须使用 `SynchedEntityData`。在 `defineSynchedData()` 中注册 `EntityDataAccessor`，并在状态改变时 `entityData.set(...)`。
- **NBT 保存与读取**：重写 `addAdditionalSaveData(CompoundTag)` 和 `readAdditionalSaveData(CompoundTag)`，确保重启游戏后实体的状态（如变种颜色、冷却时间）不会丢失。

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体数值或冗长表格，请直接通过以下锚点跳转至 Wiki 原文查阅。

### 1. 机制基础
- [实体一般行为](https://zh.minecraft.wiki/w/%E5%AE%9E%E4%BD%93#%E4%B8%80%E8%88%AC%E8%A1%8C%E4%B8%BA) *(亮度、状态效果、命名牌机制)*
- [实体运动与碰撞箱](https://zh.minecraft.wiki/w/%E5%AE%9E%E4%BD%93#%E8%BF%90%E5%8A%A8) *(速度、位置计算公式)*
- [骑乘机制 (Riding)](https://zh.minecraft.wiki/w/%E5%AE%9E%E4%BD%93#%E9%AA%91%E8%A1%8C) *(蜘蛛骑士、矿车组合体规则)*

### 2. 特殊实体类型
- [掉落物实体 (Item Entity)](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81%EF%BC%88%E5%AE%9E%E4%BD%93%EF%BC%89) *(5分钟消失机制、无敌判定)*
- [下落的方块 (Falling Block)](https://zh.minecraft.wiki/w/%E5%AE%9E%E4%BD%93#%E4%B8%8B%E8%90%BD%E7%9A%84%E6%96%B9%E5%9D%97) *(沙子坍塌、悬空更新机制)*
- [船和矿车 (Vehicles)](https://zh.minecraft.wiki/w/%E5%AE%9E%E4%BD%93#%E8%88%B9%E5%92%8C%E7%9F%BF%E8%BD%A6)

### 3. 实体数据字典 (超长表格)
> **[点击查看所有原版实体完整列表](https://zh.minecraft.wiki/w/%E5%AE%9E%E4%BD%93#%E6%89%80%E6%9C%89%E5%AE%9E%E4%BD%93)**

*速查提示：原版实体的命名空间 ID 形式为 `minecraft:<英文名>`。*
*例如：*
- *僵尸 (Zombie): `minecraft:zombie`*
- *箭 (Arrow): `minecraft:arrow`*
- *掉落物 (Item): `minecraft:item`*
- *盔甲架 (Armor Stand): `minecraft:armor_stand`*

---

## 相关资源与材质 (Assets)

如果需要为自定义实体提供材质、模型或动画参考，以下是原版相关资产的定位信息：

- **实体纹理 (Textures)**：`assets/minecraft/textures/entity/`
- **战利品表 (Loot Tables)**：`data/minecraft/loot_table/entities/` *(控制生物掉落物)*
- **实体标签 (Tags)**：`data/minecraft/tags/entity_type/` *(如 `#minecraft:raiders`, `#minecraft:arrows`)*
- *注：Java 版的实体模型大多在代码中定义（`EntityModel` 子类），资源包仅提供贴图。但在较新的版本中，部分模型定义正在向数据驱动的方向努力。*
