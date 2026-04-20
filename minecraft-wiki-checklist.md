# Minecraft Wiki 本地化清单 (NeoForge 开发优先)

> **目标**：将中文 Minecraft Wiki 的核心开发相关内容本地化，提取对 Mod 开发最具价值的数据结构、注册表与机制交互点，并将低优先级原版内容降维为精确的锚点索引，最终存放在 `reference/minecraft-wiki/` 目录下。

## 目录结构规划
```text
知识库/
└── reference/
    └── minecraft-wiki/
        ├── 机制/            # 附魔、交易、酿造等
        ├── 方块/            # 自然方块、功能方块、红石等
        ├── 物品/            # 武器、工具、消耗品等
        ├── 实体/            # 敌对、中立、友好生物
        ├── 世界生成/        # 群系、结构、维度
        └── assets/          # 存放相关原版材质与图标
```

## 核心条目清单 (Checklist)

### 1. 基础机制 (Mechanics)
- [x] [附魔](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94) (Enchanting)
  - **优先级**：高
  - **开发重点**：1.21数据驱动JSON格式、数据组件(`DataComponents.ENCHANTMENTS`)迁移、事件拦截(`LivingDamageEvent`)。
- [x] [状态效果](https://zh.minecraft.wiki/w/%E7%8A%B6%E6%80%81%E6%95%88%E6%9E%9C) (Status Effects)
  - **优先级**：高
  - **开发重点**：注册(`MobEffect`)、实例创建(`MobEffectInstance`)、每Tick更新逻辑(`applyEffectTick`)。
- [x] [交易](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93) (Trading)
  - **优先级**：中
  - **开发重点**：村民职业注册、自定义交易项注入(`VillagerTradesEvent`)、经验与等级关系。
- [x] [酿造](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0) (Brewing)
  - **优先级**：中
  - **开发重点**：药水注册(`Potion`)、酿造配方添加(`BrewingRecipeRegistry`)。
- [x] [伤害类型](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3) (Damage)
  - **优先级**：极高
  - **开发重点**：数据驱动伤害类型JSON配置、伤害源(`DamageSource`)获取与判定、伤害标签(`damage_type` tags)。
- [x] [红石电路](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF) (Redstone)
  - **优先级**：中
  - **开发重点**：方块红石充能判定(`isSignalSource`, `getSignal`)、方块更新机制。

### 2. 世界生成 (World Generation)
- [x] [生物群系](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB) (Biomes)
  - **优先级**：高
  - **开发重点**：数据包定义、生物群系修改器(`BiomeModifiers`)。
- [x] [生成结构](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84) (Structures)
  - **优先级**：中
  - **开发重点**：Jigsaw/拼图方块机制、池(`template_pool`)配置。
- [x] [维度](https://zh.minecraft.wiki/w/%E7%BB%B4%E5%BA%A6) (Dimensions)
  - **优先级**：低
  - **开发重点**：维度类型(`dimension_type`)配置、传送门生成拦截。

### 3. 方块与物品总览 (Blocks & Items)
- [x] [方块总览](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97) (Blocks)
  - **优先级**：极高
  - **开发重点**：方块状态(`BlockState`)、属性(`BlockBehaviour.Properties`)、VoxelShape碰撞箱。
- [x] [物品总览](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81) (Items)
  - **优先级**：极高
  - **开发重点**：数据组件(`DataComponent`)、物品属性(`Item.Properties`)、交互方法(`use`, `useOn`)。
- [x] [工具](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7) (Tools)
  - **优先级**：高
  - **开发重点**：Tier 层级系统(挖掘等级、耐久、效率)、标签判定。
- [x] [食物](https://zh.minecraft.wiki/w/%E9%A3%9F%E7%89%A9) (Food)
  - **优先级**：高
  - **开发重点**：食物组件(`FoodProperties`)、营养值、饱和度与药水效果附加。

### 4. 实体与生物 (Entities)
- [x] [生物总览](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9) (Mobs)
  - **优先级**：高
  - **开发重点**：属性系统(`AttributeSupplier`)、AI目标与任务(`GoalSelector`)。
- [x] [实体总览](https://zh.minecraft.wiki/w/%E5%AE%9E%E4%BD%93) (Entities)
  - **优先级**：极高
  - **开发重点**：注册、同步数据(`EntityDataAccessor`)、渲染器绑定。

### 5. 模组开发数据向 (Data-Driven)
- [x] [战利品表](https://zh.minecraft.wiki/w/%E6%88%98%E5%88%A9%E5%93%81%E8%A1%A8) (Loot Tables)
  - **优先级**：极高
  - **开发重点**：JSON格式、全局战利品修改器(`GlobalLootModifiers`)。
- [x] [标签](https://zh.minecraft.wiki/w/%E6%A0%87%E7%AD%BE) (Tags)
  - **优先级**：极高
  - **开发重点**：JSON格式、标签的合并与替换、代码中如何查询(`is(TagKey)`)。
- [x] [配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9) (Recipes)
  - **优先级**：高
  - **开发重点**：各类工作台配方JSON、自定义配方类型(`RecipeType`)。
