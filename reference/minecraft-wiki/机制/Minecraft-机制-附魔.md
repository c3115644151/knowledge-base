# Minecraft 机制：附魔 (Enchantment)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/附魔](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94)  
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+  
> **本地更新时间**：2026-04-20  

---

## 模组开发核心要点 (Modding Priorities)

在 NeoForge 开发中，附魔（魔咒）已高度**数据驱动化 (Data-Driven)**。魔咒不再是硬编码的类，而是由数据包 (Datapack) 中的 JSON 文件定义，并由注册表管理。

### NeoForge 对照文档

- [NeoForge-服务端-附魔.md](../../neoForge/NeoForge-服务端-附魔.md)
- [NeoForge-物品-数据组件.md](../../neoForge/NeoForge-物品-数据组件.md)
- [NeoForge LivingEntity 与生物逻辑](../../neoForge/NeoForge-实体-LivingEntity.md)

### 1. 注册表与标识符
- **注册表名称**：`minecraft:enchantment` (在 NeoForge 中通常通过 `Registries.ENCHANTMENT` 访问)
- **命名空间**：原版魔咒的 ResourceLocation 均为 `minecraft:<enchantment_name>`（例如 `minecraft:sharpness`）。
- **组件存储 (1.21+)**：物品上的魔咒现在存储在**数据组件 (Data Components)** 中，而不是传统的 NBT `Enchantments` 标签。
  - 关键组件类型：`DataComponents.ENCHANTMENTS` 和 `DataComponents.STORED_ENCHANTMENTS`（仅附魔书）。

### 2. 数据驱动的魔咒定义 (JSON 结构)
魔咒的属性完全由 JSON 文件定义，存放在数据包的 `data/<namespace>/enchantment/` 目录下。一个典型的魔咒 JSON 包含以下关键字段：
- `description`: 魔咒名称的翻译键（如 `enchantment.minecraft.sharpness`）。
- `supported_items`: 一个**物品标签 (Item Tag)**（如 `#minecraft:enchantable/weapon`），定义哪些物品可以接受此魔咒。
- `primary_items`: 一个物品标签，定义附魔台主要为哪些物品提供此魔咒。
- `weight`: 附魔台选中该魔咒的权重（整数）。
- `max_level`: 最大等级。
- `min_cost` & `max_cost`: 基于附魔等级的最小/最大消耗计算公式。
- `anvil_cost`: 铁砧合并成本乘数。
- `slots`: 装备槽位（如 `mainhand`, `head`, `chest` 等），定义魔咒在哪些槽位生效。
- `effects`: **核心扩展点**。通过组件系统 (Component System) 定义魔咒的实际效果（如增加伤害、属性修饰、战利品修改等）。

### 3. 常见开发与交互场景
- **为物品添加魔咒**：
  - 代码层面：使用 `ItemStack.enchant(Enchantment, level)`（注意：在 1.21+ 中，需要获取魔咒的 `Holder<Enchantment>` 或 `ResourceKey<Enchantment>`，通常通过 `RegistryAccess` 或动态注册表获取）。
  - 数据层面：在战利品表 (Loot Tables) 中使用 `minecraft:enchant_randomly` 或 `minecraft:enchant_with_levels` 函数。
- **自定义魔咒效果**：
  - 简单效果：利用原版提供的 `effects` 组件（如 `minecraft:damage` 增加伤害，`minecraft:attributes` 修改实体属性）。
  - 复杂/自定义逻辑：NeoForge 提供了多种事件拦截。例如：
    - `LivingDamageEvent` / `LivingHurtEvent`：拦截伤害计算。
    - `BlockEvent.BreakEvent` / `LootTableLoadEvent`：修改挖掘掉落。
    - 在事件处理中，通过遍历 `ItemStack` 的 `DataComponents.ENCHANTMENTS` 来检测自定义魔咒并应用逻辑。
- **控制附魔台行为**：
  - 修改 `supported_items` 和 `primary_items` 标签即可控制自定义物品是否能在附魔台附魔。
  - 对于特殊逻辑，可监听 `EnchantmentLevelSetEvent`（控制附魔台等级计算）。

### 4. 开发避坑指南
- **1.21 组件系统迁移**：不要再尝试通过直接操作 NBT（如 `itemStack.getOrCreateTag().getList("Enchantments")`）来修改魔咒。必须使用新的 `DataComponent` API，否则会导致数据不同步或崩溃。
- **宝藏魔咒 (Treasure Enchantments)**：现在通过给魔咒分配特定的标签（如 `#minecraft:treasure`）来控制，而不是代码中的布尔标志。
- **不共存魔咒 (Exclusive Enchantments)**：也是通过标签（如 `#minecraft:exclusive_set/damage`）来管理排斥关系。

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体数值或冗长表格，请直接通过以下锚点跳转至 Wiki 原文查阅。

### 1. 机制基础
- [魔咒属性与规则](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E9%AD%94%E5%92%92%E5%B1%9E%E6%80%A7) *(适用性、等级限制、出现条件等)*
- [附魔书机制](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E9%99%84%E9%AD%94%E4%B9%A6) *(铁砧合并、基岩版与Java版的差异)*

### 2. 获取与移除方式
- [自然生成途径清单](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E8%87%AA%E7%84%B6%E7%94%9F%E6%88%90) *(战利品箱、村民交易、生物掉落的详细概率与等级)*
- [附魔台运作机制](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E9%99%84%E9%AD%94)
- [铁砧机制与累积惩罚](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E9%93%81%E7%A0%A7)
- [如何移除魔咒](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E7%A7%BB%E9%99%A4%E7%89%A9%E5%93%81%E9%AD%94%E5%92%92) *(砂轮与合成修复)*

### 3. 魔咒数据字典 (超长表格)
> **[点击查看所有原版魔咒完整列表](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E6%89%80%E6%9C%89%E9%AD%94%E5%92%92)**

*速查提示：原版魔咒的命名空间 ID 形式为 `minecraft:<英文名>`。*
*例如：*
- *锋利 (Sharpness): `minecraft:sharpness`*
- *时运 (Fortune): `minecraft:fortune`*
- *精准采集 (Silk Touch): `minecraft:silk_touch`*
- *经验修补 (Mending): `minecraft:mending`*

### 4. 相关命令与数据修改
- [作弊与命令修改魔咒](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E4%BD%9C%E5%BC%8A%E4%B8%8E%E5%91%BD%E4%BB%A4) *(`/enchant`, `/give`, `/item` 等命令的用法)*

---

### Wiki 全目录（H2/H3/H4）

- [机制](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E6%9C%BA%E5%88%B6)
  - [魔咒属性](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E9%AD%94%E5%92%92%E5%B1%9E%E6%80%A7)
  - [附魔书](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E9%99%84%E9%AD%94%E4%B9%A6)
- [获取附魔物品](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E8%8E%B7%E5%8F%96%E9%99%84%E9%AD%94%E7%89%A9%E5%93%81)
  - [自然生成](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E8%87%AA%E7%84%B6%E7%94%9F%E6%88%90)
  - [附魔](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E9%99%84%E9%AD%94)
  - [铁砧](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E9%93%81%E7%A0%A7)
  - [物品修复](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E7%89%A9%E5%93%81%E4%BF%AE%E5%A4%8D)
  - [作弊与命令](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E4%BD%9C%E5%BC%8A%E4%B8%8E%E5%91%BD%E4%BB%A4)
- [移除物品魔咒](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E7%A7%BB%E9%99%A4%E7%89%A9%E5%93%81%E9%AD%94%E5%92%92)
- [所有魔咒](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E6%89%80%E6%9C%89%E9%AD%94%E5%92%92)
  - [宝藏型魔咒](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E5%AE%9D%E8%97%8F%E5%9E%8B%E9%AD%94%E5%92%92)
  - [魔咒的适用性](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E9%AD%94%E5%92%92%E7%9A%84%E9%80%82%E7%94%A8%E6%80%A7)
    - [手持物品魔咒](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E6%89%8B%E6%8C%81%E7%89%A9%E5%93%81%E9%AD%94%E5%92%92)
    - [盔甲位物品魔咒](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E7%9B%94%E7%94%B2%E4%BD%8D%E7%89%A9%E5%93%81%E9%AD%94%E5%92%92)
- [数据驱动](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E6%95%B0%E6%8D%AE%E9%A9%B1%E5%8A%A8)
- [历史](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E5%8E%86%E5%8F%B2)
- [参考](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E5%8F%82%E8%80%83)
- [导航](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94#%E5%AF%BC%E8%88%AA)

## 相关资源与材质 (Assets)

如果需要为自定义魔咒或相关 UI 提供材质参考，以下是原版相关资产的定位信息：

- **附魔书材质**：`assets/minecraft/textures/item/enchanted_book.png`
- **附魔台材质**：
  - 顶部：`assets/minecraft/textures/block/enchanting_table_top.png`
  - 侧面：`assets/minecraft/textures/block/enchanting_table_side.png`
  - 底部：`assets/minecraft/textures/block/enchanting_table_bottom.png`
- **附魔闪烁光效 (Glint)**：`assets/minecraft/textures/misc/enchanted_glint_entity.png` / `enchanted_glint_item.png`
- *(本地资产占位路径：`/workspace/reference/minecraft-wiki/assets/enchanting/`)*
