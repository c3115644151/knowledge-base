# Minecraft Wiki 本地化知识库

> 基于中文 Minecraft Wiki (https://zh.minecraft.wiki/) 的本地化参考文档，面向 NeoForge 模组开发：高权重内容优先展开，低权重内容提供精确到章节锚点的索引入口。

## 文档统计

| 分类 | 数量 |
|------|------|
| 机制 | 6 |
| 数据驱动 | 3 |
| 世界生成 | 3 |
| 方块 | 1 |
| 物品 | 3 |
| 实体 | 2 |
| **总计** | **18** |

## 机制

| 文档 | 说明 |
|------|------|
| [Minecraft-机制-附魔.md](机制/Minecraft-机制-附魔.md) | 附魔与魔咒：数据驱动、数据组件迁移、事件干预入口 |
| [Minecraft-机制-状态效果.md](机制/Minecraft-机制-状态效果.md) | 状态效果：注册、实例、叠加规则、tick 与事件入口 |
| [Minecraft-机制-伤害.md](机制/Minecraft-机制-伤害.md) | 伤害：damage_type 数据驱动、标签、伤害来源与拦截点 |
| [Minecraft-机制-交易.md](机制/Minecraft-机制-交易.md) | 交易：村民/流浪商人交易池、声望/需求、注入与平衡 |
| [Minecraft-机制-酿造.md](机制/Minecraft-机制-酿造.md) | 酿造：药水链路、配方注入、与状态效果联动 |
| [Minecraft-机制-红石电路.md](机制/Minecraft-机制-红石电路.md) | 红石电路：信号接口、更新传播、比较器/脉冲相关 |

## 数据驱动

| 文档 | 说明 |
|------|------|
| [Minecraft-数据驱动-战利品表.md](数据驱动/Minecraft-数据驱动-战利品表.md) | Loot Tables：JSON 结构、DataGen、全局战利品修改器 |
| [Minecraft-数据驱动-标签.md](数据驱动/Minecraft-数据驱动-标签.md) | Tags：TagKey、JSON 合并/替换、DataGen、跨模组兼容 |
| [Minecraft-数据驱动-配方.md](数据驱动/Minecraft-数据驱动-配方.md) | Recipes：配方类型/序列化器、Builder、组件化输出 |

## 世界生成

| 文档 | 说明 |
|------|------|
| [Minecraft-世界生成-生物群系.md](世界生成/Minecraft-世界生成-生物群系.md) | Biomes：worldgen/biome、BiomeModifier、气候与着色 |
| [Minecraft-世界生成-生成结构.md](世界生成/Minecraft-世界生成-生成结构.md) | Structures：structure_set/structure/template_pool、拼图系统、StructureModifier |
| [Minecraft-世界生成-维度.md](世界生成/Minecraft-世界生成-维度.md) | Dimensions：dimension_type + dimension、噪声生成、传送入口 |

## 方块

| 文档 | 说明 |
|------|------|
| [Minecraft-方块-方块总览.md](方块/Minecraft-方块-方块总览.md) | Blocks：注册、BlockState、模型/掉落/标签数据驱动 |

## 物品

| 文档 | 说明 |
|------|------|
| [Minecraft-物品-物品总览.md](物品/Minecraft-物品-物品总览.md) | Items：1.21 数据组件体系、交互入口、创造标签页 |
| [Minecraft-物品-工具.md](物品/Minecraft-物品-工具.md) | Tools：Tool 组件、挖掘标签、Tier 与工具行为 |
| [Minecraft-物品-食物.md](物品/Minecraft-物品-食物.md) | Food：Food/Consumable 组件、食用行为与事件入口 |

## 实体

| 文档 | 说明 |
|------|------|
| [Minecraft-实体-实体总览.md](实体/Minecraft-实体-实体总览.md) | Entities：注册、同步数据、属性与渲染绑定 |
| [Minecraft-实体-生物总览.md](实体/Minecraft-实体-生物总览.md) | Mobs：AI Goals、生成、属性初始化与 BiomeModifier |

## 关键词映射

| 关键词 | 文档路径 |
|--------|---------|
| enchantment / 附魔 | 机制/Minecraft-机制-附魔.md |
| mob effect / 状态效果 | 机制/Minecraft-机制-状态效果.md |
| damage_type / 伤害类型 | 机制/Minecraft-机制-伤害.md |
| trading / 交易 | 机制/Minecraft-机制-交易.md |
| brewing / 酿造 | 机制/Minecraft-机制-酿造.md |
| redstone / 红石 | 机制/Minecraft-机制-红石电路.md |
| loot table / 战利品表 | 数据驱动/Minecraft-数据驱动-战利品表.md |
| tags / 标签 | 数据驱动/Minecraft-数据驱动-标签.md |
| recipes / 配方 | 数据驱动/Minecraft-数据驱动-配方.md |
| biome / 生物群系 | 世界生成/Minecraft-世界生成-生物群系.md |
| structures / 生成结构 | 世界生成/Minecraft-世界生成-生成结构.md |
| dimension / 维度 | 世界生成/Minecraft-世界生成-维度.md |
| block / 方块 | 方块/Minecraft-方块-方块总览.md |
| item / 物品 | 物品/Minecraft-物品-物品总览.md |
| tool / 工具 | 物品/Minecraft-物品-工具.md |
| food / 食物 | 物品/Minecraft-物品-食物.md |
| entity / 实体 | 实体/Minecraft-实体-实体总览.md |
| mob / 生物 | 实体/Minecraft-实体-生物总览.md |
