# NeoForge-服务端-标签

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/resources/server/tags

## 概述

标签（Tags）用于将多个注册对象分组。可以为任何注册类型创建标签。

## 文件结构

`data/<namespace>/tags/<type>/<path>.json`

示例：
- `data/minecraft/tags/block/stone.json` → `minecraft:stone` 标签

## JSON 结构

```json
{
    "replace": false,
    "values": [
        "minecraft:cobblestone",
        "minecraft:stone",
        {"id": "examplemod:custom_stone", "required": true}
    ]
}
```

## 创建方块标签

`data/examplemod/tags/block/example.json`:
```json
{
    "values": [
        "minecraft:stone",
        "minecraft:cobblestone",
        "examplemod:custom_stone"
    ]
}
```

## 创建物品标签

`data/examplemod/tags/item/example.json`:
```json
{
    "values": [
        "minecraft:iron_ingot",
        "examplemod:processed_iron"
    ]
}
```

## 引用标签

### 在代码中引用

```java
// 使用 TagKey
public static final TagKey<Block> EXAMPLE_BLOCKS = TagKey.create(
    Registries.BLOCK,
    Identifier.of("examplemod", "example")
);

// 检查方块是否在标签中
if (blockHolder.is(EXAMPLE_BLOCKS)) {
    // ...
}
```

### 在数据文件中引用

```json
{
    "values": [
        "#examplemod:example",  // 引用标签
        "examplemod:single_item"
    ]
}
```

## 常用标签

| 标签 | 内容 |
|------|------|
| `minecraft:blocks/mineable/*` | 可被特定工具开采的方块 |
| `minecraft:items/.axes` | 斧 |
| `minecraft:items/music_discs` | 音乐唱片 |
| `minecraft:blocks/dirt` | 泥土类方块 |
| `minecraft:entity_types/axolotls` | 美西螈可攻击的实体 |

## 数据生成

### 方块标签提供者

```java
public class MyBlockTagsProvider extends BlockTagsProvider {
    public MyBlockTagsProvider(PackOutput output, CompletableFuture<HolderLookup.Provider> lookupProvider) {
        super(output, lookupProvider, ExampleMod.MOD_ID);
    }

    @Override
    protected void addTags(HolderLookup.Provider lookupProvider) {
        // 创建标签
        tag(EXAMPLE_BLOCKS)
            .add(Blocks.STONE)
            .add(Blocks.COBBLESTONE)
            .addTag(Tags.Blocks.COBBLESTONE)
            .remove(Blocks.DIRT);

        // 替换标签
        getOrCreateBuilder(EXAMPLE_BLOCKS)
            .replace(true)
            .add(Blocks.GRASS_BLOCK);
    }
}
```

### 物品标签提供者

```java
public class MyItemTagsProvider extends ItemTagsProvider {
    public MyItemTagsProvider(PackOutput output, CompletableFuture<HolderLookup.Provider> lookupProvider,
                              CompletableFuture<TagLookup<Block>> blockTags) {
        super(output, lookupProvider, blockTags, ExampleMod.MOD_ID);
    }

    @Override
    protected void addTags(HolderLookup.Provider lookupProvider) {
        tag(EXAMPLE_ITEMS)
            .add(Items.DIAMOND)
            .addTag(ItemTags.WOOL)
            .addOptional(Identifier.of("othermod", "item"));
    }
}
```

### 复制方块标签到物品标签

```java
public class ExampleBlockTagCopyingItemTagProvider extends BlockTagCopyingItemTagProvider {
    public ExampleBlockTagCopyingItemTagProvider(PackOutput output, 
                                                   CompletableFuture<HolderLookup.Provider> lookupProvider,
                                                   CompletableFuture<TagLookup<Block>> blockTags) {
        super(output, lookupProvider, blockTags, ExampleMod.MOD_ID);
    }

    @Override
    protected void addTags(HolderLookup.Provider lookupProvider) {
        this.copy(EXAMPLE_BLOCKS, EXAMPLE_ITEMS);
    }
}
```

### 注册

```java
@SubscribeEvent
public static void gatherData(GatherDataEvent.Client event) {
    event.createProvider(MyBlockTagsProvider::new, ExampleBlockTagCopyingItemTagProvider::new);
}
```

## 标签选项

### 可选元素

```json
{
    "values": [
        {"id": "examplemod:optional_item", "required": false}
    ]
}
```

### 替换模式

```json
{
    "replace": true,
    "values": ["examplemod:new_item"]
}
```

## 常用内置 TagKey

```java
// 方块
Tags.Blocks.DIRT          // 泥土类
Tags.Blocks.STONE         // 石头类
Tags.Blocks.WOOL          // 羊毛
Tags.Blocks.COBBLESTONE   // 圆石

// 物品
Tags.Items.DIAMONDS       // 钻石
Tags.Items.GOLD_INGOTS    // 金锭
Tags.Items.IRON_INGOTS    // 铁锭
Tags.Items.WOOL           // 羊毛

// 实体类型
Tags.EntityTypes.BOSS     // Boss
Tags.EntityTypes.ARTHROPOD // 节肢生物
```

## 注意事项

1. **标签是累加的**：不同资源包添加值到同一标签
2. **使用 `replace: true`**：替换整个标签内容
3. **可选元素**：`required: false` 使元素可选
4. **同步**：某些标签会在服务端和客户端间同步
5. **命名约定**：使用 `camelCase` 或 `snake_case`

## 关联引用

- [[NeoForge-服务端资源]] - 服务端资源总览
- [[NeoForge-服务端-数据映射]] - 数据映射
- [[NeoForge-数据生成]] - 数据生成
