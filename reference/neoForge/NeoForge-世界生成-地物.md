# NeoForge 世界生成 - 地物（Features）

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/worldgen/features

## 概述

地物（Features）是 Minecraft 世界生成的重要组成部分，用于在地形中放置各种元素，如矿石、树木、花草、水体等。NeoForge 提供了数据驱动的系统来定义和配置地物。

## 核心概念

### ConfiguredFeature（配置的特物）

`ConfiguredFeature` 定义了地物的基本行为和配置，例如矿石要替换哪些方块、生成数量等。

### PlacedFeature（放置的特物）

`PlacedFeature` 定义了配置的特物如何在地世界中放置，包括高度范围、生物群系条件、生成方式等。

### GenerationStep.Decoration

生成步骤枚举，决定了特物在哪个阶段生成：

- `UNDERGROUND_ORES` - 地下矿石
- `UNDERGROUND_DECORATION` - 地下装饰
- `FLUID_SPRINGS` - 流体泉源
- `VEGETAL_DECORATION` - 植物装饰
- `SURFACE_STRUCTURES` - 表面结构
- `TOP_LAYER_MODIFICATION` - 顶层修饰

## 创建矿石特物

### 1. 定义 OreConfiguration

```java
public class ModOreFeatures {
    public static final ResourceKey<ConfiguredFeature<?, ?>> ORE_RUBY = createKey("ore_ruby");

    public static void bootstrap(BootstrapContext<ConfiguredFeature<?, ?>> context) {
        // 定义目标方块匹配规则
        RuleTest石头匹配 = new BlockStateMatchTest(
            Blocks.STONE.defaultBlockState()
        );
        
        // 使用标签匹配
        RuleTest石头标签 = new TagMatchTest(BlockTags.STONE_ORE_REPLACEABLES);
        
        // 创建矿石配置
        OreConfiguration configuration = new OreConfiguration(
           石头标签,  // 匹配规则
            ModBlocks.RUBY_ORE.get().defaultBlockState(),  // 放置的方块
            9  // 每个矿脉的矿石数量
        );
        
        // 注册配置的特物
        context.register(ORE_RUBY, new ConfiguredFeature<>(
            Feature.ORE,  // 特物类型
            configuration  // 特物配置
        ));
    }
    
    private static ResourceKey<ConfiguredFeature<?, ?>> createKey(String name) {
        return ResourceKey.create(Registries.CONFIGURED_FEATURE, 
            new ResourceLocation(ExampleMod.MODID, name));
    }
}
```

### 2. 定义放置特征

```java
public class ModOrePlacements {
    public static final ResourceKey<PlacedFeature> ORE_RUBY = createKey("ore_ruby");

    public static void bootstrap(BootstrapContext<PlacedFeature> context) {
        // 获取配置的特物
        HolderGetter<ConfiguredFeature<?, ?>> configuredFeatures = 
            context.lookup(Registries.CONFIGURED_FEATURE);
        
        // 创建放置修饰符列表
        List<PlacementModifier> modifiers = new ArrayList<>();
        modifiers.add(CountPlacement.of(UniformInt.of(0, 1)));  // 生成数量
        modifiers.add(SquarePlacementPlacement.of());  // 在正方形区域内
        modifiers.add(HeightRangePlacement.of(
            UniformHeight.of(VerticalAnchor.absolute(-64), VerticalAnchor.absolute(80))
        ));  // 高度范围
        modifiers.add(BiomeFilter.biome());  // 只在生物群系中
        
        // 注册放置的特物
        context.register(ORE_RUBY, new PlacedFeature(
            configuredFeatures.getOrThrow(ModOreFeatures.ORE_RUBY),
            modifiers
        ));
    }
    
    private static ResourceKey<PlacedFeature> createKey(String name) {
        return ResourceKey.create(Registries.PLACED_FEATURE, 
            new ResourceLocation(ExampleMod.MODID, name));
    }
}
```

### 3. 添加到生物群系

```java
public class ModBiomeModifiers {
    public static final ResourceKey<BiomeModifier> ADD_RUBY_ORE = registerKey("add_ruby_ore");

    public static void bootstrap(BootstrapContext<BiomeModifier> context) {
        var placedFeatures = context.lookup(Registries.PLACED_FEATURE);
        var biomes = context.lookup(Registries.BIOME);
        
        context.register(ADD_RUBY_ORE, new AddFeaturesBiomeModifier(
            biomes.getOrThrow(BiomeTags.IS_OVERWORLD),
            HolderSet.direct(placedFeatures.getOrThrow(ModOrePlacements.ORE_RUBY)),
            GenerationStep.Decoration.UNDERGROUND_ORES
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

## 常用 PlacementModifier

| 修饰符 | 说明 |
|--------|------|
| `CountPlacement.of(count)` | 生成数量 |
| `CountPlacement.of(UniformInt.of(min, max))` | 随机数量 |
| `RarityFilterPlacement.of(chance)` | 生成几率（1/chance） |
| `SquarePlacementPlacement.of()` | 正方形区域 |
| `HeightRangePlacement.of(range)` | 高度范围 |
| `SurfaceRelativeThresholdFilter.of()` | 表面相对阈值 |
| `BiomeFilter.biome()` | 生物群系过滤器 |
| `InSquarePlacementPlacement.of()` | 在正方形内随机位置 |
| `RandomOffsetPlacement.of(x, y, z)` | 随机偏移 |

## RuleTest 类型

| 类型 | 说明 |
|------|------|
| `BlockStateMatchTest` | 匹配特定方块状态 |
| `TagMatchTest` | 匹配标签中的方块 |
| `BlockMatchTest` | 匹配特定方块类型 |
| `ReplaceableMatchTest` | 匹配可替换的方块 |

## 数据生成

```java
public class ModWorldGen extends DatapackBuiltinEntriesProvider {
    public static final RegistrySetBuilder BUILDER = new RegistrySetBuilder()
        .add(Registries.CONFIGURED_FEATURE, ModOreFeatures::bootstrap)
        .add(Registries.PLACED_FEATURE, ModOrePlacements::bootstrap)
        .add(NeoForgeRegistries.Keys.BIOME_MODIFIERS, ModBiomeModifiers::bootstrap);
    
    public ModWorldGen(PackOutput output, CompletableFuture<HolderLookup.Provider> registries) {
        super(output, registries, BUILDER, Set.of(ExampleMod.MODID));
    }
}

@Mod.EventBusSubscriber(modid = ExampleMod.MODID, bus = Mod.EventBusSubscriber.Bus.MOD)
public class ModDataGeneratorHandler {
    @SubscribeEvent
    public static void gatherData(GatherDataEvent event) {
        var lp = event.getLookupProvider();
        event.getGenerator().addProvider(
            event.includeServer(),
            (DataProvider.Factory<ModWorldGen>) pOutput -> new ModWorldGen(pOutput, lp)
        );
    }
}
```

## 关联引用

- [结构](./NeoForge-世界生成-结构.md)
- [维度](./NeoForge-世界生成-维度.md)
- [生物群系修改器](./NeoForge-世界生成-生物群系修改器.md)
