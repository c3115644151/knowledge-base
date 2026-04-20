# Minecraft 物品：工具 (Tool)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/工具](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7)  
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+  
> **本地更新时间**：2026-04-20  

---

## 模组开发核心要点 (Modding Priorities)

在 NeoForge 1.21+ 中，工具的属性（如挖掘速度、可破坏方块、耐久）已经完全转向**数据组件 (Data Components)** 与**标签 (Tags)** 驱动，传统的硬编码工具类属性被大幅弱化。

### NeoForge 对照文档

- [NeoForge 物品数据组件](../../neoForge/NeoForge-物品-数据组件.md)
- [NeoForge-物品-工具](../../neoForge/NeoForge-物品-工具.md)
- [NeoForge-服务端-标签](../../neoForge/NeoForge-服务端-标签.md)

### 1. 注册表与标识符
- **注册表名称**：`minecraft:item` (在 NeoForge 中通过 `Registries.ITEM` 或 `DeferredRegister.createItems()` 管理)。
- **工具基类**：`DiggerItem`, `PickaxeItem`, `AxeItem`, `ShovelItem`, `HoeItem`, `SwordItem`。
- **核心组件**：
  - `DataComponents.TOOL`：控制工具的挖掘规则（可挖掘哪些方块、挖掘速度乘数、消耗耐久规则）。
  - `DataComponents.MAX_DAMAGE` 和 `DataComponents.DAMAGE`：取代了旧版 NBT 标签，用于控制和存储耐久度。
  - `DataComponents.WEAPON` (1.21.2+)：管理作为武器的属性。

### 2. 数据驱动的工具机制
- **挖掘等级与标签 (Mining Tiers)**：1.21 引入了新的基于标签的挖掘限制机制。
  - 方块端：使用 `#minecraft:incorrect_for_wooden_tool` 等标签标记哪些方块**不能**被低级工具挖掘，而不是指定需要的工具等级。
  - 物品端：在 `minecraft:tool` 组件的 `rules` 数组中，定义针对特定方块标签的覆盖规则（如挖掘速度提升、解除 incorrect 限制）。
- **工具动作 (ToolActions)**：NeoForge 使用 `ToolAction` 抽象了工具的交互行为（例如 `ToolActions.AXE_STRIP` 对应斧头去皮，`ToolActions.SHOVEL_FLATTEN` 对应锹铺路）。通过重写 `Item#canPerformAction` 来声明工具支持的动作。

### 3. 常见开发与交互场景
- **自定义新工具**：
  - 继承对应的原版工具类（如 `PickaxeItem`），并传入实现 `Tier` 接口的实例。
  - 在物品的 `Properties` 阶段，可以利用 `.component(DataComponents.TOOL, ...)` 来深度自定义其挖掘行为。
- **自定义右键交互**：
  - 重写 `Item#useOn(UseOnContext)`。如果是针对特定方块的通用修改（如为原版斧头添加新的去皮配方），建议监听 `BlockEvent.BlockToolModificationEvent`。
- **动态修改挖掘速度**：
  - 监听 `PlayerEvent.BreakSpeed` 事件。可用于根据玩家状态、手持工具的 NBT/组件 或周围环境动态调整挖掘速度。
- **战利品修改**：
  - 如果工具带有特殊机制改变掉落物，推荐使用**全局战利品修改器 (Global Loot Modifiers)** (监听 `LootTableLoadEvent` 注入或直接使用数据包)，而非在破坏事件中硬编码生成物品。

### 4. 开发避坑指南
- **不要直接读取/修改 NBT 获取耐久**：在 1.21+ 中，请务必使用 `ItemStack.getDamageValue()` 和 `ItemStack.setDamageValue()`，或者操作 `DataComponents.DAMAGE` 组件。操作 `Tag` 会导致数据不同步甚至游戏崩溃。
- **正确处理耐久消耗**：调用 `ItemStack#hurtAndBreak(int amount, ServerLevel level, ServerPlayer player, Consumer<Item> onBreak)`，它会自动处理耐久附魔（如耐久 III）并触发物品损坏动画。
- **旧版 Tier 逻辑迁移**：在处理是否能挖掘某方块时，应使用 `ItemStack#isCorrectToolForDrops(BlockState)`，避免手动比较硬编码的 Tier 级别。

## 极简代码示例 (Minimal Code Examples)

### 注册自定义工具 (Java)
```java
public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems("modid");

public static final DeferredItem<PickaxeItem> CUSTOM_PICKAXE = ITEMS.register("custom_pickaxe",
    () -> new PickaxeItem(
        Tiers.DIAMOND,
        new Item.Properties()
            .attributes(PickaxeItem.createAttributes(Tiers.DIAMOND, 1.0F, -2.8F))
    )
);
```

### 物品模型 (JSON)
路径：`assets/modid/models/item/custom_pickaxe.json`
```json
{
  "parent": "minecraft:item/handheld",
  "textures": {
    "layer0": "modid:item/custom_pickaxe"
  }
}
```

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、合成配方、工具列表，请直接通过以下锚点跳转至 Wiki 原文查阅。

### 1. 物品与分类
- [物品列表](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E7%89%A9%E5%93%81%E5%88%97%E8%A1%A8) *(镐、斧、剑、锹、锄以及各种功能性工具如时钟、指南针)*
- [最佳工具判定](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E6%9C%80%E4%BD%B3%E5%B7%A5%E5%85%B7) *(破坏方块最快的工具对应表)*

### 2. 获取与合成
- [生物掉落](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E7%94%9F%E7%89%A9)
- [合成配方汇总](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E5%90%88%E6%88%90) *(木、石、铁、金、钻石等各材质的合成表)*
- [锻造与下界合金升级](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E9%94%BB%E9%80%A0)

### 3. 用途与机制
- [物品耐久](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E7%89%A9%E5%93%81%E8%80%90%E4%B9%85) *(不同材质的耐久度上限及消耗规则)*
- [烧炼材料与燃料](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E7%83%A7%E7%82%BC%E6%9D%90%E6%96%99) *(将工具烧炼回收粒，或将木制工具作为燃料)*

### 4. 历史沿革
- [工具历史版本更新](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E5%8E%86%E5%8F%B2)

---

### Wiki 全目录（H2/H3/H4）

- [物品列表](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E7%89%A9%E5%93%81%E5%88%97%E8%A1%A8)
- [获取](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E8%8E%B7%E5%8F%96)
  - [生物](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E7%94%9F%E7%89%A9)
  - [合成](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E5%90%88%E6%88%90)
  - [锻造](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E9%94%BB%E9%80%A0)
- [用途](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E7%94%A8%E9%80%94)
  - [最佳工具](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E6%9C%80%E4%BD%B3%E5%B7%A5%E5%85%B7)
  - [物品耐久](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E7%89%A9%E5%93%81%E8%80%90%E4%B9%85)
  - [烧炼材料](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E7%83%A7%E7%82%BC%E6%9D%90%E6%96%99)
  - [燃料](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E7%87%83%E6%96%99)
- [历史](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E5%8E%86%E5%8F%B2)
- [参见](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E5%8F%82%E8%A7%81)
- [导航](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7#%E5%AF%BC%E8%88%AA)

## 相关资源与材质 (Assets)

如果需要为自定义工具提供材质和模型参考，以下是原版相关资产的定位信息：

- **物品材质**：`assets/minecraft/textures/item/<material>_<tool>.png` *(如 `diamond_pickaxe.png`, `iron_axe.png`)*
- **手持模型**：`assets/minecraft/models/item/<material>_<tool>.json` 
  - *注：绝大多数工具使用 `"parent": "minecraft:item/handheld"` 来确保在玩家手中的握持角度正确。*
- **攻击与挖掘音效**：
  - 破坏方块音效绑定在方块的 `SoundType` 上，无需在工具处定义。
  - 武器挥舞音效：`entity.player.attack.sweep` 等。
