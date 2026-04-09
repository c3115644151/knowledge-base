# NeoForge 配方系统

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/resources/server/recipes

## 概述

配方系统定义了物品的合成、加工、冶炼等方式。

## 文件位置

```
data/<namespace>/recipes/<name>.json
```

---

## 代码示例

### 形状配方

```json
{
    "type": "minecraft:crafting_shaped",
    "pattern": [
        "###",
        " # "
    ],
    "key": {
        "#": {
            "item": "minecraft:diamond"
        }
    },
    "result": {
        "item": "examplemod:diamond_sword"
    }
}
```

### 无形状配方

```json
{
    "type": "minecraft:crafting_shapeless",
    "ingredients": [
        {
            "item": "minecraft:diamond"
        },
        {
            "item": "minecraft:stick"
        }
    ],
    "result": {
        "item": "examplemod:diamond_tool"
    }
}
```

### 熔炉配方

```json
{
    "type": "minecraft:smelting",
    "ingredient": {
        "item": "examplemod:raw_ore"
    },
    "result": "examplemod:ingot",
    "experience": 0.7,
    "cookingtime": 200
}
```

### 数据生成

```java
// Recipe Provider
public class ModRecipeProvider extends RecipeProvider {
    public ModRecipeProvider(PackOutput output,
            CompletableFuture<HolderLookup.Provider> lookupProvider) {
        super(output, lookupProvider);
    }
    
    @Override
    protected void buildRecipes(RecipeOutput output) {
        // 形状配方
        ShapedRecipeBuilder.shaped(Consumer, Items.DIAMOND)
            .pattern("###")
            .pattern("###")
            .pattern("###")
            .define('#', Items.DIRT)
            .unlockedBy("has_diamond", has(Items.DIAMOND))
            .save(output, "my_recipe");
        
        // 无形状配方
        ShapelessRecipeBuilder.shapeless(Items.DIAMOND)
            .requires(Items.DIRT, 3)
            .unlockedBy("has_dirt", has(Items.DIRT))
            .save(output, "my_shapeless_recipe");
    }
}
```

---

## 注意事项

### 配方类型
- `crafting_shaped` - 形状合成
- `crafting_shapeless` - 无形状合成
- `smelting` - 熔炉冶炼
- `blasting` - 高炉冶炼
- `smoking` - 烟熏炉
- `campfire_cooking` - 营火烹饪
- `stonecutting` - 切石
- `smithing_transform` - 锻造

---

## 关联引用

- 数据生成：[NeoForge-数据生成](./NeoForge-数据生成.md)
