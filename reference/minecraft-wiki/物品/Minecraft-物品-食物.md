# Minecraft 物品：食物 (Food)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/食物](https://zh.minecraft.wiki/w/%E9%A3%9F%E7%89%A9)  
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+  
> **本地更新时间**：2026-04-20  

---

## 模组开发核心要点 (Modding Priorities)

在 NeoForge 1.21+ 体系中，食物机制迎来了重大重构。食物不再仅仅依赖于 `Item` 类中硬编码的属性，而是被拆分和细化为完全由**数据组件 (Data Components)** 驱动的体系，特别是 1.21.2 引入了 `Consumable` 组件。

### 1. 注册表与核心组件
食物作为普通物品注册在 `Registries.ITEM` 中。控制食物行为的核心数据组件包括：
- `DataComponents.FOOD`：定义食物的基础营养属性。
  - 包含字段：`nutrition` (饥饿值恢复量, int)、`saturation` (饱和度修饰符, float)、`can_always_eat` (满饥饿值时是否可食用, boolean)。
- `DataComponents.CONSUMABLE` (1.21.2+)：接管了所有与“消耗”相关的逻辑。
  - 包含字段：`consume_seconds` (食用耗时)、`animation` (动画类型：`eat`, `drink` 等)、`sound` (食用音效)、`has_consume_particles` (是否产生食用粒子)、`on_consume_effects` (食用后触发的各种效果，如药水效果、传送等)。

### 2. 数据驱动的食物与效果定义
- **添加状态效果**：在 `DataComponents.CONSUMABLE` 的 `on_consume_effects` 列表中，可以添加 `ApplyStatusEffectsConsumeEffect` 等实例，支持设置概率。这完全替代了旧版 `FoodProperties.Builder#effect(...)`。
- **返还物品 (Remainder)**：吃完（如炖菜留下的空碗）的逻辑被定义在消耗后返还物品的组件属性中，也可通过 `Item#getCraftingRemainingItem()` 或相应的组件管理合成返还。

### 3. 常见开发与交互场景
- **创建自定义食物**：
  ```java
  // 示例伪代码 (1.21+)
  public static final DeferredItem<Item> MAGIC_APPLE = ITEMS.register("magic_apple", 
      () -> new Item(new Item.Properties()
          .component(DataComponents.FOOD, new FoodProperties.Builder()
              .nutrition(4).saturationModifier(1.2F).alwaysEat().build())
          .component(DataComponents.CONSUMABLE, Consumables.DEFAULT_FOOD) // 可按需自定义
      ));
  ```
- **监听与拦截食用过程**：
  - `LivingEntityUseItemEvent.Start`：玩家开始吃食物时触发，可用于修改总耗时。
  - `LivingEntityUseItemEvent.Tick`：食用过程中每 tick 触发，可用于中断食用或添加持续特效。
  - `LivingEntityUseItemEvent.Finish`：食用完成瞬间触发，可修改食用后返还的物品或强制触发特定逻辑。

### 4. 开发避坑指南
- **食物与消耗品的解耦**：切记在 1.21.2+ 后，`FOOD` 组件仅负责饱食度和营养！如果你想修改吃东西的声音、时间和产生的粒子，必须修改 `CONSUMABLE` 组件。
- **蛋糕 (Cake) 不是食物物品**：在代码层面，蛋糕是一个方块 (Block)，通过 `BlockBehaviour#useItemOn` 触发玩家右键食用逻辑，它**不具备**上述的 `FOOD` 或 `CONSUMABLE` 组件。开发类似机制时需注意区分“物品型食物”与“方块型食物”。
- **狐狸的进食AI**：狐狸会自动拾取并食用带有 `FOOD` 组件的物品。如果你设计的食物具有负面或破坏性效果，请确保处理好非玩家实体（如狐狸）食用的边界情况。

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体食物数据、营养价值表，请直接通过以下锚点跳转至 Wiki 原文查阅。

### 1. 机制与特性
- [食用机制](https://zh.minecraft.wiki/w/%E9%A3%9F%E7%89%A9#%E6%9C%BA%E5%88%B6) *(食用时长、饱和度计算、特殊情况下的可食用性)*
- [狐狸的交互](https://zh.minecraft.wiki/w/%E9%A3%9F%E7%89%A9#%E7%8B%90%E7%8B%B8) *(狐狸拾取和吃掉食物的行为)*

### 2. 食物数据字典
- [营养价值表](https://zh.minecraft.wiki/w/%E9%A3%9F%E7%89%A9#%E8%90%A5%E5%85%BB%E4%BB%B7%E5%80%BC) *(超自然、好、普通、低、差 等级的划分及对应食物)*
- [**完整食物列表**](https://zh.minecraft.wiki/w/%E9%A3%9F%E7%89%A9#%E9%A3%9F%E7%89%A9%E5%88%97%E8%A1%A8) *(包含所有食物的饥饿值、饱和度、获取方式和特殊效果的超长表格)*

### 3. 相关成就与历史
- [相关成就](https://zh.minecraft.wiki/w/%E9%A3%9F%E7%89%A9#%E6%88%90%E5%B0%B1) & [进度](https://zh.minecraft.wiki/w/%E9%A3%9F%E7%89%A9#%E8%BF%9B%E5%BA%A6)
- [食物历史版本更新](https://zh.minecraft.wiki/w/%E9%A3%9F%E7%89%A9#%E5%8E%86%E5%8F%B2)

---

## 相关资源与材质 (Assets)

如果需要为自定义食物提供材质和模型参考，以下是原版相关资产的定位信息：

- **物品材质**：`assets/minecraft/textures/item/<food_name>.png` *(如 `apple.png`, `cooked_beef.png`, `mushroom_stew.png`)*
- **基础模型**：绝大多数食物使用 `"parent": "minecraft:item/generated"`，由游戏自动生成 2D 贴图的厚度。
- **相关音效**：
  - 吃食物：`entity.generic.eat`
  - 喝（汤、蜂蜜等）：`entity.generic.drink`
  - 打嗝：`entity.player.burp`
