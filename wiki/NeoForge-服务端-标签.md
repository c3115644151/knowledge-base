# NeoForge 标签系统

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/resources/server/tags

## 概述

标签（Tags）系统用于按类别组织游戏对象，便于数据驱动和模组间交互。

## 文件位置

```
data/<namespace>/tags/<category>/<name>.json
```

### 标签类别

| 类别 | 路径 | 示例 |
|------|------|------|
| Block tags | `tags/blocks/` | `#minecraft:mineable/pickaxe` |
| Item tags | `tags/items/` | `#minecraft:planks` |
| Fluid tags | `tags/fluids/` | `#minecraft:water` |
| Entity tags | `tags/entity_types/` | `#minecraft:skeletons` |
| Biome tags | `tags/biomes/` | `#minecraft:is_overworld` |

---

## 代码示例

### JSON 格式

```json
{
    "replace": false,
    "values": [
        "minecraft:diamond",
        "minecraft:emerald",
        "examplemod:custom_gem"
    ]
}
```

### 带条件的标签

```json
{
    "replace": false,
    "values": [
        {
            "id": "examplemod:optional_block",
            "required": false
        }
    ]
}
```

### 数据生成

```java
// Block Tags Provider
public class ModBlockTagsProvider extends BlockTagsProvider {
    public ModBlockTagsProvider(PackOutput output,
            CompletableFuture<HolderLookup.Provider> lookupProvider) {
        super(output, lookupProvider, MOD_ID);
    }
    
    @Override
    protected void addTags(HolderLookup.Provider provider) {
        // 添加标签
        tag(MY_CUSTOM_TAG)
            .add(ModBlocks.MY_BLOCK.get())
            .addOptional(OtherModBlocks.OTHER_BLOCK.get());
        
        // 继承标签
        tag(Tags.Blocks.MINEABLE_PICKAXE)
            .addTag(MY_CUSTOM_TAG);
    }
}
```

---

## 注意事项

### 标签命名
- 使用命名空间前缀：`modid:tag_name`
- 引用其他标签：`#namespace:tag_name`
- 避免与原版标签冲突

---

## 关联引用

- 数据生成：[NeoForge-数据生成](./NeoForge-数据生成.md)
- 方块系统：[NeoForge-方块](./NeoForge-方块.md)
