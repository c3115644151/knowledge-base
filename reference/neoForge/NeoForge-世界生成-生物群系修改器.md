# NeoForge 生物群系修改器

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/worldgen/biomemodifier

## 概述

生物群系修改器（Biome Modifiers）是一种数据驱动的系统，允许修改生物群系的各个方面，包括添加/删除特征、生成生物、修改气候等。

## 文件位置

```
data/<namespace>/neoforge/biome_modifier/<path>.json
```

---

## 代码示例

### 添加特征

```json
// 添加矿石到所有主世界生物群系
{
    "type": "neoforge:add_features",
    "biomes": "#c:is_overworld",
    "features": "examplemod:ore_copper_upper",
    "step": "underground_ores"
}
```

### 添加生物生成

```json
{
    "type": "neoforge:add_spawns",
    "biomes": "#c:is_overworld",
    "spawners": [
        {
            "type": "examplemod:custom_mob",
            "weight": 100,
            "minCount": 1,
            "maxCount": 4
        }
    ]
}
```

### 数据生成

```java
@Mod.EventBusSubscriber(modid = MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD)
public static class BiomeModifierGen {
    @SubscribeEvent
    public static void gatherData(GatherDataEvent event) {
        event.createProvider((output, lookupProvider) ->
            new DatapackBuiltinEntriesProvider(
                output,
                new RegistrySetBuilder()
                    .add(NeoForgeRegistries.Keys.BIOME_MODIFIERS,
                        bootstrap -> {
                            HolderGetter<Biome> biomes = 
                                bootstrap.lookup(Registries.BIOME);
                            HolderGetter<PlacedFeature> features = 
                                bootstrap.lookup(Registries.PLACED_FEATURE);
                            
                            bootstrap.register(
                                ResourceKey.create(
                                    NeoForgeRegistries.Keys.BIOME_MODIFIERS,
                                    ResourceLocation.fromNamespaceAndPath(
                                        MOD_ID, "add_ores")),
                                new AddFeaturesBiomeModifier(
                                    biomes.getOrThrow(
                                        Tags.Biomes.IS_OVERWORLD),
                                    HolderSet.direct(
                                        features.getOrThrow(
                                            ModFeatures.ORE_COPPER.get())),
                                    GenerationStep.Decoration.UNDERGROUND_ORES
                                )
                            );
                        }),
                Set.of(MOD_ID),
                Set.of()
            )
        );
    }
}
```

---

## 关联引用

- 世界生成：[NeoForge-世界生成](./NeoForge-世界生成.md)
