# Minecraft 数据驱动：战利品表 (Loot Tables)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/战利品表](https://zh.minecraft.wiki/w/%E6%88%98%E5%88%A9%E5%93%81%E8%A1%A8)  
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+  
> **本地更新时间**：2026-04-20  

---

## 模组开发核心要点 (Modding Priorities)

在 NeoForge 1.21+ 中，战利品表（Loot Tables）完全由 JSON 驱动，用于控制方块掉落、实体死亡掉落、容器战利品、钓鱼、考古等所有随机物品生成。

### 1. 注册表与标识符
- **注册表名称**：无直接代码注册表，战利品表由 ResourceLocation 标识（如 `minecraft:blocks/dirt`）。但在 1.21 中可通过 `ReloadableServerResources` 获取，或者作为数据包直接加载。
- **文件路径**：`data/<namespace>/loot_table/<type>/<name>.json`
  - 常用的 `<type>` 目录：`blocks/`, `entities/`, `chests/`, `gameplay/`, `archaeology/` 等。

### 2. 数据驱动的战利品表定义 (JSON 结构)
一个战利品表包含多个**随机池 (Pools)**，每个池独立抽取物品：
- `pools`: 包含所有抽取池的数组。
  - `rolls`: 抽取次数（可以是固定值或范围）。
  - `entries`: 抽取项列表。
    - `type`: `minecraft:item`, `minecraft:loot_table`, `minecraft:empty`, `minecraft:alternatives` 等。
    - `name`: 物品 ID（当 type 为 item 时）。
    - `weight`: 抽取权重。
  - `conditions`: 必须满足的条件（如 `minecraft:survives_explosion`，`minecraft:killed_by_player`，`minecraft:random_chance` 等）。
  - `functions`: 物品修饰器，用于修改生成的物品堆（如设置数量、附魔、修改名称/组件）。
    - **1.21 组件变更**：旧版的 `minecraft:set_nbt` 已被废弃，应使用 `minecraft:set_components` 或特定的组件函数来应用数据组件。

### 3. 数据生成器 (DataGen)
NeoForge 提供了强大的 Datagen API 用于生成战利品表 JSON：
- 核心类：继承 `LootTableProvider`。
- 通常使用子类或提供 `LootTableSubProvider`：
  - **方块掉落**：继承 `BlockLootSubProvider`。
    - 使用 `dropSelf(Block)` 生成基础掉落。
    - 使用 `createOreDrop(Block, Item)` 生成矿石掉落（带时运）。
  - **实体掉落**：继承 `EntityLootSubProvider`。
- **注册 Datagen**：
  ```java
  @SubscribeEvent
  public static void gatherData(GatherDataEvent event) {
      DataGenerator generator = event.getGenerator();
      generator.addProvider(
          event.includeServer(),
          new LootTableProvider(
              generator.getPackOutput(),
              Collections.emptySet(),
              List.of(
                  new LootTableProvider.SubProviderEntry(MyBlockLoot::new, LootContextParamSets.BLOCK),
                  new LootTableProvider.SubProviderEntry(MyEntityLoot::new, LootContextParamSets.ENTITY)
              ),
              event.getLookupProvider()
          )
      );
  }
  ```

### 4. 动态修改战利品表 (Global Loot Modifiers)
如果你的模组需要修改**原版或其他模组**的战利品表（例如让僵尸掉落自定义硬币），**绝对不要直接覆盖 JSON**，而必须使用 NeoForge 的全局战利品修改器 (Global Loot Modifiers, GLM)：
- **实现类**：继承 `LootModifier`（实现 `IGlobalLootModifier`）。
- **注册序列化器**：使用 `DeferredRegister<MapCodec<? extends IGlobalLootModifier>>` 注册你的 Modifier Codec。
- **数据文件**：在 `data/<namespace>/neoforge/loot_modifiers/` 目录下创建 JSON，配置应用条件。并在 `global_loot_modifiers.json` 中按顺序声明。

### 5. 常见开发避坑指南
- **1.21 组件系统迁移**：在编写 `functions` 时，不要再使用 NBT 操作函数，需使用 `minecraft:set_components` 或其他基于数据组件的修饰器。
- **LootContext**：在代码中手动生成战利品时（如 `LootTable.getRandomItems`），必须提供正确的 `LootParams` 和 `LootContextParamSet`（如传入 `LootContextParams.THIS_ENTITY`）。缺失参数会导致条件判断失败并产生警告。

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体条件和函数的详细列表，请直接通过以下锚点跳转至 Wiki 原文查阅。

### 1. 基础结构与机制
- [用途与调用方式](https://zh.minecraft.wiki/w/%E6%88%98%E5%88%A9%E5%93%81%E8%A1%A8#%E7%94%A8%E9%80%94) *(原版和自定义容器的使用机制)*
- [定义格式与随机池](https://zh.minecraft.wiki/w/%E6%88%98%E5%88%A9%E5%93%81%E8%A1%A8#%E5%AE%9A%E4%B9%89%E6%A0%BC%E5%BC%8F) *(Loot Table JSON 的基本结构)*

### 2. 抽取项 (Entries)
- [单一抽取项](https://zh.minecraft.wiki/w/%E6%88%98%E5%88%A9%E5%93%81%E8%A1%A8#%E5%8D%95%E4%B8%80%E6%8A%BD%E5%8F%96%E9%A1%B9) *(item, loot_table, dynamic, empty 等类型)*
- [复合抽取项](https://zh.minecraft.wiki/w/%E6%88%98%E5%88%A9%E5%93%81%E8%A1%A8#%E5%A4%8D%E5%90%88%E6%8A%BD%E5%8F%96%E9%A1%B9) *(alternatives, group, sequence 逻辑)*
- [特殊抽取项 - tag](https://zh.minecraft.wiki/w/%E6%88%98%E5%88%A9%E5%93%81%E8%A1%A8#tag) *(直接从标签中随机抽取)*

### 3. 函数与谓词 (Functions & Conditions)
- [物品修饰器 (Functions)](https://zh.minecraft.wiki/w/%E6%88%98%E5%88%A9%E5%93%81%E8%A1%A8#%E7%89%A9%E5%93%81%E4%BF%AE%E9%A5%B0%E5%99%A8) *(修改数量、附魔、耐久度、数据组件等)*
- [战利品表谓词 (Conditions)](https://zh.minecraft.wiki/w/%E6%88%98%E5%88%A9%E5%93%81%E8%A1%A8#%E6%88%98%E5%88%A9%E5%93%81%E8%A1%A8%E8%B0%93%E8%AF%8D) *(随机概率、玩家击杀、工具判断、天气状态等)*

### 4. 进阶机制
- [战利品上下文 (Loot Context)](https://zh.minecraft.wiki/w/%E6%88%98%E5%88%A9%E5%93%81%E8%A1%A8#%E6%88%98%E5%88%A9%E5%93%81%E4%B8%8A%E4%B8%8B%E6%96%87) *(执行时传递的实体、位置、工具等参数)*
