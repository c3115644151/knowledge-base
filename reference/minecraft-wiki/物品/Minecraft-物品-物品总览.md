# Minecraft 机制：物品 (Item)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/物品](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81)  
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+  
> **本地更新时间**：2026-04-20  

---

## 模组开发核心要点 (Modding Priorities)

在 NeoForge 1.21+ 开发中，物品 (Item) 和物品堆叠 (ItemStack) 的底层机制发生了**革命性的重构**，从传统的 NBT 标签完全迁移到了**数据组件 (Data Components)** 系统。

### NeoForge 对照文档

- [NeoForge 物品开发](../../neoForge/NeoForge-物品.md)
- [NeoForge 物品数据组件](../../neoForge/NeoForge-物品-数据组件.md)

### 1. 注册表与标识符
- **注册表名称**：`minecraft:item` (在 NeoForge 中通过 `Registries.ITEM` 或 `DeferredRegister.createItems` 访问)。
- **命名空间**：原版物品的 ResourceLocation 均为 `minecraft:<item_name>`（例如 `minecraft:diamond_sword`）。
- **ItemStack 与 Item 的区别**：`Item` 是定义在注册表中的单例（类似模板），而 `ItemStack` 是实际存在于物品栏中的实例，保存着数量和额外的数据组件。

### 2. 数据驱动与 1.21+ 组件系统 (Data Components)
1.21 彻底移除了 `ItemStack.getTag()` 和 `NBT` 的直接操作，所有物品属性（包括原版和自定义）必须通过**数据组件**驱动：
- **核心组件类型**：
  - `DataComponents.MAX_STACK_SIZE`：最大堆叠数量（原由 `Item.Properties` 定义，现转为组件）。
  - `DataComponents.MAX_DAMAGE`：最大耐久度。
  - `DataComponents.DAMAGE`：当前损伤值。
  - `DataComponents.CUSTOM_NAME` 和 `DataComponents.LORE`：自定义名称和描述。
  - `DataComponents.FOOD`：食物属性。
  - `DataComponents.ATTRIBUTE_MODIFIERS`：属性修饰符（如攻击伤害、护甲值）。
- **组件操作**：
  - 设置组件：`itemStack.set(DataComponents.XXX, value)`
  - 获取组件：`itemStack.get(DataComponents.XXX)` 或 `itemStack.getOrDefault()`
  - 检查组件：`itemStack.has(DataComponents.XXX)`
- **自定义组件注册**：通过 `Registries.DATA_COMPONENT_TYPE` 注册自定义组件类型，以存储模组的专有数据（替代以前的自定义 NBT）。

### 3. 常见开发与交互场景
- **创建基础物品**：
  - 继承 `Item` 类，构造函数传入 `Item.Properties`。在 1.21 中，`Item.Properties` 提供 `.component()` 方法用于在注册时初始化物品的默认组件。
- **物品交互方法**：
  - `use`：玩家手持物品右键点击空气或方块（未指定方块交互时）触发。返回 `InteractionResultHolder<ItemStack>`。
  - `useOn`：玩家手持物品右键点击方块触发。返回 `InteractionResult`。
  - `interactLivingEntity`：玩家手持物品右键点击实体触发。
  - `inventoryTick`：物品在玩家物品栏中每刻执行的逻辑。
- **创造模式物品栏 (Creative Tabs)**：
  - 1.20+ 后，物品需要通过监听 `BuildCreativeModeTabContentsEvent` 事件动态添加到特定的创造模式标签页中，不再在 `Item.Properties` 中硬编码。

### 4. 开发避坑指南
- **严禁使用旧版 NBT API**：1.21 中强行反射或寻找 NBT 替代品是错误做法，必须全面转向 DataComponent API。网络同步和磁盘保存现由 Codec 和 StreamCodec 自动处理。
- **ItemStack 可变性**：`ItemStack` 对象本身是可变的，但其内部的某些组件数据结构可能是不可变的（Immutable），修改时通常需要创建新的组件实例并覆盖。
- **不要将状态存在 Item 类中**：`Item` 类是单例的，所有玩家共用一个实例。特定于某个物品栈的状态**必须**存储在 `ItemStack` 的数据组件中。

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体数值或冗长表格，请直接通过以下锚点跳转至 Wiki 原文查阅。

### 1. 机制基础
- [物品行为与属性](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81#%E8%A1%8C%E4%B8%BA) *(堆叠限制、稀有度、冷却时间、展示与发光)*
- [耐久度 (Durability)](https://zh.minecraft.wiki/w/%E8%80%90%E4%B9%85%E5%BA%A6) *(工具、武器、盔甲的消耗规则)*
- [合成返还物品 (Recipe Remainder)](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81#%E8%A1%8C%E4%B8%BA) *(如水桶返还空桶、蜂蜜瓶返还玻璃瓶)*

### 2. 交互与分类
- [产生方块、液体或实体的物品](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81#%E4%BA%A7%E7%94%9F%E6%96%B9%E5%9D%97%E3%80%81%E6%B6%B2%E4%BD%93%E6%88%96%E5%AE%9E%E4%BD%93%E7%9A%84%E7%89%A9%E5%93%81) *(如刷怪蛋、船、桶)*
- [在世界中可以交互的物品](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81#%E5%9C%A8%E4%B8%96%E7%95%8C%E4%B8%AD%E5%8F%AF%E4%BB%A5%E4%BA%A4%E4%BA%92%E7%9A%84%E7%89%A9%E5%93%81) *(如打火石、骨粉、命名牌)*
- [刷怪蛋 (Spawn Egg)](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81#%E5%88%B7%E6%80%AA%E8%9B%8B)

### 3. 物品数据字典 (超长表格)
> **[点击查看所有原版物品完整列表](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81#%E7%89%A9%E5%93%81%E5%88%97%E8%A1%A8)**

*速查提示：原版物品的命名空间 ID 形式为 `minecraft:<英文名>`。*
*例如：*
- *钻石剑 (Diamond Sword): `minecraft:diamond_sword`*
- *末影珍珠 (Ender Pearl): `minecraft:ender_pearl`*
- *不死图腾 (Totem of Undying): `minecraft:totem_of_undying`*

---

### Wiki 全目录（H2/H3/H4）

- [行为](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81#%E8%A1%8C%E4%B8%BA)
- [物品列表](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81#%E7%89%A9%E5%93%81%E5%88%97%E8%A1%A8)
  - [产生方块、液体或实体的物品](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81#%E4%BA%A7%E7%94%9F%E6%96%B9%E5%9D%97%E3%80%81%E6%B6%B2%E4%BD%93%E6%88%96%E5%AE%9E%E4%BD%93%E7%9A%84%E7%89%A9%E5%93%81)
  - [在世界中可以交互的物品](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81#%E5%9C%A8%E4%B8%96%E7%95%8C%E4%B8%AD%E5%8F%AF%E4%BB%A5%E4%BA%A4%E4%BA%92%E7%9A%84%E7%89%A9%E5%93%81)
  - [在世界中间接使用的物品](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81#%E5%9C%A8%E4%B8%96%E7%95%8C%E4%B8%AD%E9%97%B4%E6%8E%A5%E4%BD%BF%E7%94%A8%E7%9A%84%E7%89%A9%E5%93%81)
  - [刷怪蛋](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81#%E5%88%B7%E6%80%AA%E8%9B%8B)
  - [教育版独有的物品](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81#%E6%95%99%E8%82%B2%E7%89%88%E7%8B%AC%E6%9C%89%E7%9A%84%E7%89%A9%E5%93%81)
  - [已移除的物品](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81#%E5%B7%B2%E7%A7%BB%E9%99%A4%E7%9A%84%E7%89%A9%E5%93%81)
- [数据值](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81#%E6%95%B0%E6%8D%AE%E5%80%BC)
- [历史](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81#%E5%8E%86%E5%8F%B2)
- [参见](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81#%E5%8F%82%E8%A7%81)
- [注释](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81#%E6%B3%A8%E9%87%8A)
- [导航](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81#%E5%AF%BC%E8%88%AA)

## 相关资源与材质 (Assets)

如果需要为自定义物品提供材质或模型参考，以下是原版相关资产的定位信息：

- **物品纹理 (Textures)**：`assets/minecraft/textures/item/`
- **物品模型 (Models)**：`assets/minecraft/models/item/` *(大部分基于 `item/generated` 自动生成 3D 模型，工具为 `item/handheld`)*
- **修饰符与组件 (Tags)**：`data/minecraft/tags/item/` *(定义物品属于哪个分类，如 `#minecraft:swords`)*
