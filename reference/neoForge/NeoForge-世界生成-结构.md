# NeoForge 世界生成 - 结构（Structures）

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/worldgen/structures

## 概述

结构（Structures）是 Minecraft 世界生成中用于放置预定义建筑和地标（如村庄、要塞、沙漠神殿等）的系统。NeoForge 提供了完整的数据驱动结构系统。

## 结构组件

### StructureTemplate

存储结构的方块和实体数据，作为 `.nbt` 文件保存。

### ConfiguredStructureFeature

定义结构的类型和配置，包括：
- 边界框计算
- 地形适应
- 生成条件

### PlacedStructure

定义结构的放置参数：
- 生成间距
- 盐值（salt）
- 位置约束

## 创建自定义结构

### 1. 定义结构模板

将结构保存为 NBT 文件：`data/examplemod/structures/my_structure.nbt`

可以使用 Minecraft 的结构方块（Structure Block）创建和导出结构。

### 2. 创建 ConfiguredStructureFeature

```java
public class ModStructureFeatures {
    public static final ResourceKey<ConfiguredStructureFeature<?, ?>> MY_STRUCTURE = 
        createKey("my_structure");

    public static void bootstrap(BootstrapContext<ConfiguredStructureFeature<?, ?>> context) {
        context.register(MY_STRUCTURE, new ConfiguredStructureFeature<>(
            StructureTemplatePool.START,  // 结构池
            new Structure.StructureSettings(
                BiomeTags.HAS_OVERWORLD_RUINED_PORTAL,  // 生成条件
                ImmutableMap.of(),  // 额外配置
                GenerationStep.Decoration.SURFACE_STRUCTURES,  // 生成阶段
                true,  // 地形适应
                8,  // 地面偏移
                2,  // 集间距
                3,  // 射束半径
                512,  // 集大小
                true  // 包含射束
            )
        ));
    }
    
    private static ResourceKey<ConfiguredStructureFeature<?, ?>> createKey(String name) {
        return ResourceKey.create(
            Registries.CONFIGURED_STRUCTURE_FEATURE,
            new ResourceLocation(ExampleMod.MODID, name)
        );
    }
}
```

### 3. 创建 PlacedStructure

```java
public class ModStructurePlacements {
    public static final ResourceKey<PlacedFeature> MY_STRUCTURE = createKey("my_structure");

    public static void bootstrap(BootstrapContext<PlacedFeature> context) {
        var configuredStructures = context.lookup(Registries.CONFIGURED_STRUCTURE_FEATURE);
        
        context.register(MY_STRUCTURE, new PlacedFeature(
            configuredStructures.getOrThrow(ModStructureFeatures.MY_STRUCTURE),
            Arrays.asList(
                RarityFilter.onAverageOnceEvery(30),  // 1/30 生成几率
                InSquarePlacementPlacement.spread(),  // 方形分布
                HeightRangePlacement.of(
                    RectangleRange.of(-20, 40)  // 高度范围
                ),
                BiomeFilter.biome()  // 生物群系过滤
            )
        ));
    }
    
    private static ResourceKey<PlacedFeature> createKey(String name) {
        return ResourceKey.create(
            Registries.PLACED_FEATURE,
            new ResourceLocation(ExampleMod.MODID, name)
        );
    }
}
```

### 4. 添加到生物群系

```java
public class ModBiomeModifiers {
    public static final ResourceKey<BiomeModifier> ADD_MY_STRUCTURE = 
        registerKey("add_my_structure");

    public static void bootstrap(BootstrapContext<BiomeModifier> context) {
        var placedFeatures = context.lookup(Registries.PLACED_FEATURE);
        var biomes = context.lookup(Registries.BIOME);
        
        context.register(ADD_MY_STRUCTURE, new AddFeaturesBiomeModifier(
            biomes.getOrThrow(BiomeTags.IS_OVERWORLD),
            HolderSet.direct(placedFeatures.getOrThrow(ModStructurePlacements.MY_STRUCTURE)),
            GenerationStep.Decoration.SURFACE_STRUCTURES
        ));
    }
    
    private static ResourceKey<BiomeModifier> registerKey(String name) {
        return ResourceKey.create(
            NeoForgeRegistries.Keys.BIOME_MODIFIERS,
            new ResourceLocation(ExampleMod.MODID, name)
        );
    }
}
```

## 结构池（Jigsaw）

使用结构池创建程序化结构：

```java
// 在 BootstrapContext 中
context.register(
    StructurePools.ROOT, 
    () -> new StructureTemplatePool(
        new ResourceLocation("minecraft:village/plains/town_centers"),
        List.of(
            StructurePoolElement.legacy("examplemod:my_pool/start"),
            StructurePoolElement.empty()
        ),
        StructureTemplatePool.Projection.RIGID
    )
);
```

## StructureSettings 参数

| 参数 | 说明 |
|------|------|
| `biomePredicate` | 生物群系谓词 |
| `surfaceThreshold` | 表面阈值 |
| `bonusRoll` | 额外尝试次数 |
| `generationStep` | 生成阶段 |
| `terrainAdaptive` | 是否进行地形适应 |
| `groundLevelDelta` | 地面高度偏移 |
| `setSpacing` | 设置间距 |
| `setSeparation` | 设置间距 |
| `setSeedModifier` | 设置种子修改器 |
| `projectStartToHeightmap` | 是否投影到高度图 |
| `broadcast` | 是否广播 |
| `beams` | 光束数量 |

## 验证结构生成

使用 `/locate` 命令测试结构是否正确生成：
```
/locate examplemod:my_structure
```

## 关联引用

- [地物](./NeoForge-世界生成-地物.md)
- [维度](./NeoForge-世界生成-维度.md)
- [生物群系修改器](./NeoForge-世界生成-生物群系修改器.md)
