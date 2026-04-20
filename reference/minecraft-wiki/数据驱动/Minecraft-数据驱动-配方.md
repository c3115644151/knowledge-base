# Minecraft 数据驱动：配方 (Recipes)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9)  
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+  
> **本地更新时间**：2026-04-20  

---

## 模组开发核心要点 (Modding Priorities)

在 NeoForge 开发中，所有的原版合成、烧炼、切石、锻造等机制都基于数据驱动的**配方系统 (Recipe System)**。配方定义了输入材料（`Ingredient`）和输出结果（`ItemStack` / `DataComponent`）。

### NeoForge 对照文档

- [NeoForge-服务端-配方](../../neoForge/NeoForge-服务端-配方.md)
- [NeoForge 物品数据组件](../../neoForge/NeoForge-物品-数据组件.md)

### 1. 注册表与核心类
- **注册表名称**：
  - **配方序列化器 (RecipeSerializer)**：通过 `Registries.RECIPE_SERIALIZER` 注册。负责从 JSON 解析配方数据或写入网络缓冲包。
  - **配方类型 (RecipeType)**：通过 `Registries.RECIPE_TYPE` 注册。定义配方在哪个机器或系统内生效（如 `minecraft:crafting`, `minecraft:smelting`）。
- **文件路径**：`data/<namespace>/recipe/<name>.json`
- **核心接口**：
  - `Recipe<C>`：配方逻辑的接口，处理是否匹配输入容器 (`C`)，以及生成结果。
  - `Ingredient`：配方输入的抽象，可以匹配单个物品或标签内的任何物品。在 1.21 中，支持严格匹配数据组件。

### 2. 数据驱动的配方定义 (JSON 结构)
JSON 中的主要字段（以常见的 `minecraft:crafting_shaped` 为例）：
- `type`: 配方的类型（如 `minecraft:crafting_shaped`, `minecraft:smelting`）。
- `pattern`: 字符串数组，代表 3x3 合成网格的形状。
- `key`: 字典，将 `pattern` 中的字符映射为具体的 `Ingredient`（物品或标签）。
- `result`: 结果对象，包含 `id`、`count`，在 1.21+ 中还可以包含 `components` 对象来附加数据组件（如自定义名称、附魔、自定义数据）。
- `category` & `group`: 用于在配方书 (Recipe Book) 中归类显示。

### 3. 数据生成器 (DataGen)
使用 Datagen 生成配方 JSON 是 NeoForge 的标准做法。
- **核心类**：继承 `RecipeProvider`。
- **Builder API**：
  - **有序合成**：`ShapedRecipeBuilder.shaped(RecipeCategory, ResultItem, Count)`
    - 使用 `.pattern("###")`、`.define('#', Ingredient)` 构建。
  - **无序合成**：`ShapelessRecipeBuilder.shapeless(RecipeCategory, ResultItem, Count)`
    - 使用 `.requires(Ingredient)` 添加材料。
  - **烧炼/高炉/烟熏/营火**：`SimpleCookingRecipeBuilder.smelting(...)` / `blasting()` / `smoking()` / `campfireCooking()`
  - **切石机**：`SingleItemRecipeBuilder.stonecutting(...)`
  - **锻造台**：`SmithingTransformRecipeBuilder` (升级装备) 和 `SmithingTrimRecipeBuilder` (盔甲纹饰)。
- **必须调用 `.unlockedBy(...)`**：所有的 `RecipeBuilder` 都必须提供一个解锁进度（Advancement），否则构建将抛出异常。
  - 通常使用 `has(Item)` 或 `has(Tag)` 作为解锁条件（即玩家获得材料时解锁配方）。
  - 最后调用 `.save(RecipeOutput)` 生成 JSON。

### 4. 自定义配方类型 (Custom Recipe Types)
如果你添加了新机器（如粉碎机、压块机），你需要自定义配方：
1. **实现 `Recipe<Container>`**：定义匹配逻辑 (`matches()`) 和处理结果 (`assemble()`)。
2. **实现 `RecipeSerializer<T>`**：定义 `MapCodec` 用于 JSON 解析，定义 `StreamCodec` 用于服务器到客户端的同步。
3. **实现 `RecipeType<T>`**：作为配方的分类标识。
4. **注册**：将 Serializer 和 Type 注册到对应的 DeferredRegister 中。
5. **获取配方**：在 TileEntity 或代码中，通过 `level.getRecipeManager().getRecipeFor(MyRecipeType.INSTANCE, container, level)` 获取当前输入对应的配方。

### 5. 常见开发避坑指南
- **NBT 到 Component 的迁移**：在 1.21 中，JSON 的 `result` 字段不能再直接写 NBT 数据。如果你的配方输出需要保留或添加复杂数据，请使用数据组件（Data Components）声明。
- **配方冲突**：模组应避免与原版或其他模组注册相同的合成输入配方，否则只会随机匹配其中一个（通常由加载顺序决定）。使用标签而非硬编码物品可以提高配方的兼容性。
- **配方书解锁进度**：千万不要忘记在 Datagen 中为你的配方提供 `.unlockedBy()`，否则它不会自动生成解锁配方的 JSON（在 `advancement/recipes/` 下），玩家在生存模式下将无法在配方书中看到它。

---

## 极简代码示例 (Minimal Code Examples)

### 1. 配方 Datagen (Java)
```java
public class MyRecipeProvider extends RecipeProvider {
    public MyRecipeProvider(PackOutput output, CompletableFuture<HolderLookup.Provider> lookupProvider) {
        super(output, lookupProvider);
    }

    @Override
    protected void buildRecipes(RecipeOutput output) {
        // 有序合成 (Shaped)
        ShapedRecipeBuilder.shaped(RecipeCategory.MISC, MyItems.CUSTOM_ITEM.get())
            .pattern("###")
            .pattern(" # ")
            .pattern(" # ")
            .define('#', ItemTags.PLANKS)
            .unlockedBy("has_planks", has(ItemTags.PLANKS))
            .save(output);

        // 无序合成 (Shapeless)
        ShapelessRecipeBuilder.shapeless(RecipeCategory.MISC, MyItems.CUSTOM_DUST.get(), 9)
            .requires(MyBlocks.CUSTOM_BLOCK.get())
            .unlockedBy("has_custom_block", has(MyBlocks.CUSTOM_BLOCK.get()))
            .save(output);
    }
}
```

### 2. 配方定义 (JSON)
`data/mymod/recipe/custom_item.json`
```json
{
  "type": "minecraft:crafting_shaped",
  "category": "misc",
  "key": {
    "#": {
      "tag": "minecraft:planks"
    }
  },
  "pattern": [
    "###",
    " # ",
    " # "
  ],
  "result": {
    "count": 1,
    "id": "mymod:custom_item"
  }
}
```

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版支持的各种配方类型的具体 JSON 字段、合成结构和示例，请直接通过以下锚点跳转至 Wiki 原文查阅。

### 1. 配方系统基础
- [获取配方与解锁条件](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E8%8E%B7%E5%8F%96) *(配方书的解锁机制与命令)*
- [用途与显示规则](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E7%94%A8%E9%80%94) *(配方书的界面分类)*

### 2. 基础合成 (Crafting Table)
- [有序配方 (crafting_shaped)](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E6%9C%89%E5%BA%8F%E9%85%8D%E6%96%B9) *(3x3 固定结构合成，JSON 的 pattern 与 key)*
- [无序配方 (crafting_shapeless)](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E6%97%A0%E5%BA%8F%E9%85%8D%E6%96%B9) *(无视位置的材料堆叠合成)*

### 3. 原版特殊机器 (Cooking & Processing)
- [烧炼与烹饪 (Smelting/Blasting/Smoking/Campfire)](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E7%83%A7%E7%82%BC%E9%85%8D%E6%96%B9) *(熔炉、高炉、烟熏炉、营火的配方结构与经验值)*
- [切石机配方 (stonecutting)](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E5%88%87%E7%9F%B3%E6%9C%BA%E9%85%8D%E6%96%B9) *(单物品输入，多类型输出)*
- [锻造升级与纹饰 (smithing_transform / smithing_trim)](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E9%94%BB%E9%80%A0%E9%85%8D%E6%96%B9) *(下界合金升级、盔甲修饰模板与材料的 JSON 结构)*

### 4. 原版硬编码 (定制) 配方类型
以下配方类型通常硬编码在原版逻辑中（属于特殊合成），不支持直接通过简单 JSON 修改，但在 NeoForge 中可以通过自定义 `RecipeSerializer` 扩展或覆盖其行为：
- [饰纹陶罐配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E9%A5%B0%E7%BA%B9%E9%99%B6%E7%BD%90%E9%85%8D%E6%96%B9)
- [染色配方与药染配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E6%9F%93%E8%89%B2%E9%85%8D%E6%96%B9)
- [旗帜复制与成书复制](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E6%97%97%E5%B8%9C%E5%A4%8D%E5%88%B6%E9%85%8D%E6%96%B9)
- [烟花火箭与烟火之星](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E7%83%9F%E8%8A%B1%E7%81%AB%E7%AE%AD%E9%85%8D%E6%96%B9)
- [地图缩小与物品修复](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E5%9C%B0%E5%9B%BE%E7%BC%A9%E5%B0%8F%E9%85%8D%E6%96%B9)

### Wiki 全目录（H2/H3/H4）

- [获取](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E8%8E%B7%E5%8F%96)
- [用途](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E7%94%A8%E9%80%94)
- [Java版](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#Java%E7%89%88)
  - [合成配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E5%90%88%E6%88%90%E9%85%8D%E6%96%B9)
    - [有序配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E6%9C%89%E5%BA%8F%E9%85%8D%E6%96%B9)
    - [无序配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E6%97%A0%E5%BA%8F%E9%85%8D%E6%96%B9)
    - [类型转化配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E7%B1%BB%E5%9E%8B%E8%BD%AC%E5%8C%96%E9%85%8D%E6%96%B9)
    - [染色配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E6%9F%93%E8%89%B2%E9%85%8D%E6%96%B9)
    - [药染配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E8%8D%AF%E6%9F%93%E9%85%8D%E6%96%B9)
  - [定制配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E5%AE%9A%E5%88%B6%E9%85%8D%E6%96%B9)
    - [饰纹陶罐配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E9%A5%B0%E7%BA%B9%E9%99%B6%E7%BD%90%E9%85%8D%E6%96%B9)
    - [旗帜复制配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E6%97%97%E5%B8%9C%E5%A4%8D%E5%88%B6%E9%85%8D%E6%96%B9)
    - [成书复制配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E6%88%90%E4%B9%A6%E5%A4%8D%E5%88%B6%E9%85%8D%E6%96%B9)
    - [烟花火箭配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E7%83%9F%E8%8A%B1%E7%81%AB%E7%AE%AD%E9%85%8D%E6%96%B9)
    - [烟火之星合成配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E7%83%9F%E7%81%AB%E4%B9%8B%E6%98%9F%E5%90%88%E6%88%90%E9%85%8D%E6%96%B9)
    - [烟火之星色彩淡化配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E7%83%9F%E7%81%AB%E4%B9%8B%E6%98%9F%E8%89%B2%E5%BD%A9%E6%B7%A1%E5%8C%96%E9%85%8D%E6%96%B9)
    - [地图缩小配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E5%9C%B0%E5%9B%BE%E7%BC%A9%E5%B0%8F%E9%85%8D%E6%96%B9)
    - [物品修复配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E7%89%A9%E5%93%81%E4%BF%AE%E5%A4%8D%E9%85%8D%E6%96%B9)
    - [盾牌装饰配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E7%9B%BE%E7%89%8C%E8%A3%85%E9%A5%B0%E9%85%8D%E6%96%B9)
  - [烧炼配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E7%83%A7%E7%82%BC%E9%85%8D%E6%96%B9)
    - [高炉配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E9%AB%98%E7%82%89%E9%85%8D%E6%96%B9)
    - [营火配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E8%90%A5%E7%81%AB%E9%85%8D%E6%96%B9)
    - [熔炉配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E7%86%94%E7%82%89%E9%85%8D%E6%96%B9)
    - [烟熏炉配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E7%83%9F%E7%86%8F%E7%82%89%E9%85%8D%E6%96%B9)
  - [切石机配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E5%88%87%E7%9F%B3%E6%9C%BA%E9%85%8D%E6%96%B9)
  - [锻造配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E9%94%BB%E9%80%A0%E9%85%8D%E6%96%B9)
- [基岩版](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E5%9F%BA%E5%B2%A9%E7%89%88)
  - [recipe_shaped](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#recipe_shaped)
  - [recipe_shapeless](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#recipe_shapeless)
  - [recipe_furnace](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#recipe_furnace)
  - [recipe_brewing_container](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#recipe_brewing_container)
  - [recipe_brewing_mix](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#recipe_brewing_mix)
  - [recipe_smithing_transform](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#recipe_smithing_transform)
  - [recipe_smithing_trim](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#recipe_smithing_trim)
  - [recipe_material_reduction](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#recipe_material_reduction)
- [历史](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E5%8E%86%E5%8F%B2)
- [参考](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E5%8F%82%E8%80%83)
- [导航](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9#%E5%AF%BC%E8%88%AA)

---

## 相关资源与材质 (Assets)

配方系统主要关联的是数据文件与 GUI/交互，而非固定贴图资源：
- **数据文件路径**：`data/<namespace>/recipe/<name>.json`（实际目录以数据包结构为准，常见为 `recipes/`）
- **与组件系统联动**：1.21+ 可通过配方输出携带 Data Components（例如自定义耐久/自定义属性的物品）
