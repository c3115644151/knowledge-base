# Minecraft 实体：生物 (Mob)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/生物](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9)  
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+  
> **本地更新时间**：2026-04-20  

---

## 模组开发核心要点 (Modding Priorities)

在 NeoForge 1.21+ 中，开发自定义生物需要掌握注册表、实体属性（Attributes）、实体渲染以及数据驱动的生成机制（Biome Modifiers）。

### 1. 注册表与核心类
- **注册表名称**：`minecraft:entity_type` (通过 `Registries.ENTITY_TYPE` 或 `DeferredRegister.createEntities()` 管理)。
- **核心基类层级**：
  - `Entity` -> `LivingEntity` -> `Mob` -> `PathfinderMob` (具有寻路能力的生物) -> `Animal` / `Monster` 等子类。
- **实体类别 (MobCategory)**：
  - `MONSTER` (怪物), `CREATURE` (动物), `AMBIENT` (环境生物), `WATER_CREATURE` (水生动物) 等。这决定了刷怪上限 (Mob Cap) 与消失规则 (Despawning)。

### 2. 实体属性 (Attributes)
- **属性注册机制**：在 1.21+，生物的默认属性必须在启动时通过事件注册，不能硬编码在构造函数中。
  - 监听事件：`EntityAttributeCreationEvent`。
  - 构建属性：使用 `Mob.createMobAttributes()` 并附加所需属性，如 `.add(Attributes.MAX_HEALTH, 20.0)`，`.add(Attributes.MOVEMENT_SPEED, 0.25)`，`.add(Attributes.ATTACK_DAMAGE, 3.0)` 等。
- **属性修饰符**：可动态应用 `AttributeModifier`，用于处理药水效果、装备等带来的增益或减益。

### 3. 常见开发与交互场景
- **定义实体类并注册**：
  ```java
  // 伪代码示例
  public static final DeferredRegister<EntityType<?>> ENTITIES = DeferredRegister.create(Registries.ENTITY_TYPE, MODID);
  public static final DeferredHolder<EntityType<?>, EntityType<CustomMob>> CUSTOM_MOB = ENTITIES.register("custom_mob", 
      () -> EntityType.Builder.of(CustomMob::new, MobCategory.CREATURE)
          .sized(0.6F, 1.8F) // 碰撞箱大小
          .build("custom_mob"));
  ```
- **配置生物 AI (Goals)**：
  - 重写 `Mob#registerGoals()`，使用 `this.goalSelector.addGoal(...)` 注册行为逻辑（如游荡、攻击），使用 `this.targetSelector.addGoal(...)` 注册索敌逻辑（如仇恨系统）。
  - NeoForge 提供大量原版 AI，如 `MeleeAttackGoal` (近战)、`LookAtPlayerGoal` (注视玩家)、`WaterAvoidingRandomStrollGoal` (避水随机游荡)。
- **配置数据驱动的生成 (Spawning)**：
  - 1.21+ 完全摒弃了代码层面的 `BiomeLoadingEvent` 添加刷怪逻辑，改用 **Biome Modifiers**。
  - 在 `data/<namespace>/neoforge/biome_modifier/` 下创建 JSON 文件，将自定义生物注入到指定的生物群系标签（如 `#minecraft:is_forest`）中。
- **渲染器与模型**：
  - 模型：继承 `EntityModel` 或其子类（如 `HierarchicalModel`），并在 `EntityRenderersEvent.RegisterLayerDefinitions` 事件中注册 `ModelLayerLocation`。
  - 渲染器：继承 `MobRenderer`，在 `EntityRenderersEvent.RegisterRenderers` 中绑定 `EntityType` 与渲染器。

### 4. 开发避坑指南
- **同步实体数据 (SynchedEntityData)**：如果需要让客户端知道实体的状态（例如：毛色、是否发怒）以进行渲染，必须使用 `EntityDataAccessor`。但切忌滥用，每 tick 同步大量数据会引发严重网络卡顿。
- **内存泄漏风险**：在自定义 `Goal` 时，避免保存对 `Level`、`Chunk` 或大型数据结构的强引用。当 `Goal` 停止执行时，确保清理不必要的引用。
- **掉落物数据化**：实体的掉落物完全由战利品表控制。路径位于 `data/<namespace>/loot_table/entity/<entity_name>.json`。
- **实体碰撞箱问题**：改变实体的碰撞箱大小必须通过 `EntityType.Builder.sized`，并在必要时调用 `refreshDimensions()`，不要直接修改边界框变量。

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、AI行为详解及详尽的生物分类，请直接通过以下锚点跳转至 Wiki 原文查阅。

### 1. 机制基础
- [生成机制](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9#%E7%94%9F%E6%88%90) *(自然生成条件、刷怪笼、光照与生物群系要求)*
- [生物行为与 AI](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9#%E8%A1%8C%E4%B8%BA) *(感知范围、寻路机制、受击免疫)*

### 2. 生物分类与列表
- [**完整生物列表**](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9#%E7%94%9F%E7%89%A9%E5%88%97%E8%A1%A8)
- [玩家](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9#%E7%8E%A9%E5%AE%B6) *(可控实体的特殊机制)*
- [友好生物](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9#%E5%8F%8B%E5%A5%BD%E7%94%9F%E7%89%A9) *(无攻击行为/有伤害能力/条件敌对 等细分)*
- [敌对生物](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9#%E6%95%8C%E5%AF%B9%E7%94%9F%E7%89%A9)

### 3. 生物族群分类
- [亡灵生物](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9#%E4%BA%A1%E7%81%B5%E7%94%9F%E7%89%A9) *(僵尸、骷髅、凋灵等，受治疗药水伤害、亡灵杀手加成)*
- [节肢生物](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9#%E8%8A%82%E8%82%A2%E7%94%9F%E7%89%A9) *(蜘蛛、蠹虫、蜜蜂等，受节肢杀手加成)*
- [水生生物](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9#%E6%B0%B4%E7%94%9F%E7%94%9F%E7%89%A9) *(鱼类、海豚、鱿鱼等，免疫溺水伤害、受穿刺加成)*
- [灾厄村民](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9#%E7%81%BE%E5%8E%84%E6%9D%91%E6%B0%91) *(掠夺者、卫道士、唤魔者等，与村庄机制交互)*

### 4. 数据与历史
- [实体数据标签](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9#%E5%AE%9E%E4%BD%93%E6%95%B0%E6%8D%AE) *(NBT 结构解析)*
- [历史版本更新](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9#%E5%8E%86%E5%8F%B2)

---

## 相关资源与材质 (Assets)

如果需要为自定义生物制作材质、模型与动画，以下是原版相关资产的定位信息：

- **实体贴图**：`assets/minecraft/textures/entity/<entity_name>/` *(由于生物结构复杂，通常存放于子文件夹内)*
- **刷怪蛋材质**：原版刷怪蛋没有独立材质，而是通过代码中 `SpawnEggItem` 定义底色与斑点颜色，渲染时复用基础遮罩。
- **相关音效**：
  - 许多实体的音效存放在 `sounds/entity/<entity_name>/` 目录下。
  - 需要在 `Mob` 类中重写 `getAmbientSound()`, `getHurtSound()`, `getDeathSound()`, 和 `getStepSound()` 等方法来指定对应的 `SoundEvent`。
