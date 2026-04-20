# Minecraft 世界生成：生成结构 (Generated Structures)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/生成结构](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84)  
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+  
> **本地更新时间**：2026-04-20  

---

## 模组开发核心要点 (Modding Priorities)

在 1.21+ 中，结构的生成完全由**数据包 (Datapack)** 驱动，高度依赖于 **Jigsaw (拼图) 系统** 和多种注册表的配合。

### NeoForge 对照文档

- [NeoForge 世界生成 - 结构（Structures）](../../neoForge/NeoForge-世界生成-结构.md)
- [NeoForge 战利品表](../../neoForge/NeoForge-服务端-战利品表.md)

### 1. 核心注册表与概念
结构生成分为三个主要层级（均通过数据包 JSON 定义）：
- **结构集 (Structure Set)** (`Registries.STRUCTURE_SET`)
  - 定义**在哪里**以及**多频繁**生成结构。
  - 控制生成位置的算法（如 `random_spread`）、间距 (spacing)、最小分离度 (separation) 和随机盐值 (salt)。
- **结构 (Structure)** (`Registries.STRUCTURE`)
  - 定义结构**生成的条件与起始点**。
  - 绑定到特定的生物群系标签 (`biomes`)。
  - 指定生成类型（大多数复杂结构使用 `minecraft:jigsaw`）。
  - 可定义覆盖生物生成的规则 (`spawn_overrides`)，例如在结构范围内生成特定怪物。
- **模板池 (Template Pool)** (`Registries.TEMPLATE_POOL`)
  - 存储结构的**各个部件 (Pieces)** 及其生成权重。
  - 用于 Jigsaw 系统，定义拼图块如何互相连接。

### 2. 拼图系统 (Jigsaw Blocks)
现代结构（如村庄、远古城市、试炼密室）通过游戏内的**拼图方块 (Jigsaw Block)** 拼接：
- 在结构 NBT 文件中，拼图方块包含 `name` (自身接口名)、`target` (要连接的目标接口名) 和 `pool` (下一个部件从中选取的模板池)。
- 开发者可以在游戏内使用结构方块 (Structure Block) 和拼图方块设计部件，并导出为 `.nbt` 文件放在 `data/<namespace>/structures/` 目录下。

### 3. NeoForge 结构修饰器 (Structure Modifiers)
如果要修改原版的结构（如在村庄中添加自定义怪物的生成，或让海底神殿生成在自定义生物群系中），必须使用 NeoForge 的 `StructureModifier`。
- **数据路径**：`data/<namespace>/neoforge/structure_modifier/`
- 可以动态调整结构的 `biomes` 列表或 `spawn_overrides`。
- 也可以通过数据包直接向原版村庄的 `template_pool` 中注入新的房屋变体。

### 4. 战利品与探险地图
- **战利品表 (Loot Tables)**：结构内的箱子通常不直接保存物品，而是保存 `LootTable` 的资源键。打开时动态生成战利品。
- **定位器**：自定义结构可以分配标签（如 `#minecraft:on_treasure_maps`），使制图师村民能售卖指向该结构的探险家地图。

---

## 原版 Wiki 快速索引 (Quick Reference)

### 1. 主世界结构
- [地下结构](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84#%E5%9C%B0%E4%B8%8B%E7%BB%93%E6%9E%84) *(远古城市、废弃矿井、要塞、试炼密室、古迹废墟等)*
- [地表结构](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84#%E5%9C%B0%E8%A1%A8%E7%BB%93%E6%9E%84) *(村庄、掠夺者前哨站、沙漠神殿、丛林神庙、雪屋、林地府邸、沼泽小屋等)*
- [水下结构](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84#%E6%B0%B4%E4%B8%8B%E7%BB%93%E6%9E%84) *(海底神殿、沉船、海底废墟)*

### 2. 其他维度结构
- [下界结构](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84#%E4%B8%8B%E7%95%8C) *(下界要塞、堡垒遗迹、废弃传送门)*
- [末地结构](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84#%E6%9C%AB%E5%9C%B0) *(末地城、末地船、末地折跃门)*

### 3. 机制与数据
- [可被定位的结构](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84#%E5%8F%AF%E8%A2%AB%E5%AE%9A%E4%BD%8D%E7%9A%84%E7%BB%93%E6%9E%84) *(列出了 /locate 指令中使用的标准结构 ID，如 `minecraft:ancient_city`)*
- [数据包：结构存储格式](https://zh.minecraft.wiki/w/%E7%BB%93%E6%9E%84%E5%AD%98%E5%82%A8%E6%A0%BC%E5%BC%8F) *(了解 .nbt 文件内部的数据结构)*
- [数据包：拼图结构格式](https://zh.minecraft.wiki/w/%E6%8B%BC%E5%9B%BE%E7%BB%93%E6%9E%84%E6%A0%BC%E5%BC%8F) *(深入理解 template_pool 和 jigsaw 生成逻辑)*

---

### Wiki 全目录（H2/H3/H4）

- [主世界](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84#%E4%B8%BB%E4%B8%96%E7%95%8C)
  - [地下结构](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84#%E5%9C%B0%E4%B8%8B%E7%BB%93%E6%9E%84)
  - [地表结构](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84#%E5%9C%B0%E8%A1%A8%E7%BB%93%E6%9E%84)
  - [水下结构](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84#%E6%B0%B4%E4%B8%8B%E7%BB%93%E6%9E%84)
- [下界](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84#%E4%B8%8B%E7%95%8C)
- [末地](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84#%E6%9C%AB%E5%9C%B0)
- [可被定位的结构](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84#%E5%8F%AF%E8%A2%AB%E5%AE%9A%E4%BD%8D%E7%9A%84%E7%BB%93%E6%9E%84)
- [历史](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84#%E5%8E%86%E5%8F%B2)
- [参见](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84#%E5%8F%82%E8%A7%81)
- [注释](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84#%E6%B3%A8%E9%87%8A)
- [参考](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84#%E5%8F%82%E8%80%83)
- [导航](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84#%E5%AF%BC%E8%88%AA)

## 相关资源与材质 (Assets)

- **查找结构**：`/locate structure <structure_id>`
- **放置结构测试**：`/place structure <structure_id> [pos]` 或使用结构方块 (Structure Block)。
- **拼图调试**：在放置拼图方块时，可以使用调试棒 (Debug Stick) 或在结构方块界面调整拼图深度。
