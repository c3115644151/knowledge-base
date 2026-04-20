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

## 结构处理器（StructureProcessor）

> ⚠️ **1.21 版本 API 规范**（以下均为官方 Mojang 映射名称）

### 适用场景

`StructureProcessor` 用于在结构生成时动态替换方块。只有 **Jigsaw 结构**（村庄、废弃矿井、要塞等）才能通过 `processor_list` JSON 覆盖注入自定义方块。

**不能使用 StructureProcessor 的 legacy 结构**（见下节）。

### 完整实现流程

#### 1. 创建 Processor 类

```java
package com.examplemod.content.structure;

import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import com.examplemod.init.ModBlocks;
import net.minecraft.core.BlockPos;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureProcessor;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureProcessorType;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate;
import net.minecraft.world.level.block.Blocks;
import org.jetbrains.annotations.Nullable;

public class JungleTempleProcessor extends StructureProcessor {

    public static final MapCodec<JungleTempleProcessor> CODEC = RecordCodecBuilder.mapCodec(instance ->
            instance.point(new JungleTempleProcessor())
    );

    private static final float REPLACEMENT_CHANCE = 0.20f;

    @Override
    @Nullable
    public StructureTemplate.StructureBlockInfo processBlock(
            LevelReader level,                      // ✅ 不是 ServerLevelAccessor
            BlockPos offset,
            BlockPos pos,
            StructureTemplate.StructureBlockInfo originalBlockInfo,  // 原始方块（NBT 模板中定义）
            StructureTemplate.StructureBlockInfo currentBlockInfo,  // 当前方块（经前面处理器处理后）
            StructurePlaceSettings settings
    ) {
        if (currentBlockInfo.state().is(Blocks.MOSSY_STONE_BRICKS)) {
            RandomSource random = level.getRandom();
            if (random.nextFloat() < REPLACEMENT_CHANCE) {
                return new StructureTemplate.StructureBlockInfo(
                        currentBlockInfo.pos(),
                        ModBlocks.SUSPICIOUS_MOSSY_STONE_BRICKS.get().defaultBlockState(),
                        currentBlockInfo.nbt()
                );
            }
        }
        return currentBlockInfo;
    }

    @Override
    protected StructureProcessorType<?> getType() {
        return ModStructureProcessors.JUNGLE_TEMPLE_PROCESSOR.get();
    }
}
```

#### 2. 注册 StructureProcessorType

⚠️ **常见错误**：
- ❌ `Registries.STRUCTURE_PROCESSOR_SERIALIZER`（不存在）
- ✅ `Registries.STRUCTURE_PROCESSOR`

```java
package com.examplemod.init;

import com.mojang.serialization.MapCodec;
import com.examplemod.RelicTales;
import com.examplemod.content.structure.JungleTempleProcessor;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureProcessorType;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModStructureProcessors {
    // ✅ 注册到 STRUCTURE_PROCESSOR（不是 SERIALIZER）
    public static final DeferredRegister<StructureProcessorType<?>> PROCESSORS =
            DeferredRegister.create(Registries.STRUCTURE_PROCESSOR, RelicTales.MOD_ID);

    // ✅ DeferredHolder 泛型：DeferredHolder<类型自身, 包装类型>
    public static final DeferredHolder<StructureProcessorType<?>, StructureProcessorType<JungleTempleProcessor>> JUNGLE_TEMPLE_PROCESSOR =
            PROCESSORS.register("jungle_temple_processor", () -> () -> JungleTempleProcessor.CODEC);

    public static void init() {}
}
```

在 `RelicRegisters.init(bus)` 中注册：
```java
ModStructureProcessors.PROCESSORS.register(bus);
```

#### 3. 创建 processor_list JSON（仅适用于 Jigsaw 结构）

路径：`src/main/resources/data/minecraft/worldgen/processor_list/<structure_name>.json`

**覆盖丛林神殿示例**（见下节：⚠️ 不适用）：
```json
{
  "processors": [
    {
      "processor_type": "examplemod:jungle_temple_processor"
    }
  ]
}
```

---

## Legacy 结构与注入方案

### 哪些是 Legacy 结构

以下结构使用硬编码 Java 逻辑生成（无 NBT 模板池），**无法通过 `processor_list` JSON 覆盖注入方块**：

| 结构 | 类型 | 能否使用 processor_list |
|------|------|----------------------|
| 丛林神殿 `jungle_temple` | Legacy Feature | ❌ 不能 |
| 沙漠神殿 `desert_pyramid` | Legacy Feature | ❌ 不能 |
| 要塞 `stronghold` | Jigsaw ✅ | ✅ 可以 |
| 下界堡垒 `nether_fortress` | Jigsaw ✅ | ✅ 可以 |
| 末地城 `end_city` | Jigsaw ✅ | ✅ 可以 |
| 村庄（所有变种） | Jigsaw ✅ | ✅ 可以 |
| 废弃矿井 `mineshaft` | Jigsaw ✅ | ✅ 可以 |

> **验证方法**：查看 `data/minecraft/worldgen/` 目录是否有对应的 `.nbt` 模板文件。
> 有 `.nbt` 模板 = Jigsaw 结构，可注入；无 = Legacy 结构，不可注入。

### 注入 Legacy 结构（丛林/沙漠神殿）的两种方案

#### 方案 A：BiomeModifier 完全替换（推荐）

1. 通过 BiomeModifier JSON 移除原版结构：
```json
// data/<modid>/neoforge/biome_modifier/remove_jungle_temple.json
{
  "type": "neoforge:remove_features",
  "biomes": "#minecraft:has_structure/jungle_temple",
  "features": "minecraft:jungle_temple"
}
```

2. 自定义 Jigsaw 格式的"复制版"丛林神殿结构，并附加自定义 processor_list。

#### 方案 B：Mixin 拦截生成逻辑

在 26.1 反混淆环境下，直接 Mixin `JungleTemplePiece` 类，在 `placeBlock` 调用处注入替换逻辑：

```java
@Mixin(JungleTemplePiece.class)
public abstract class MixinJungleTemplePiece {
    @Inject(method = "placeBlock", at = @At("HEAD"), cancellable = true)
    private void onPlaceBlock(WorldGenLevel level, BlockState state, int x, int y, int z,
                               BoundingBox box, CallbackInfoReturnable<Boolean> ci) {
        if (state.is(Blocks.MOSSY_STONE_BRICKS) && level.getRandom().nextFloat() < 0.2f) {
            // 替换逻辑
            level.setBlock(new BlockPos(x, y, z),
                ModBlocks.SUSPICIOUS_MOSSY_STONE_BRICKS.get().defaultBlockState(), 3);
            ci.setReturnValue(true);
        }
    }
}
```

---

## 验证结构生成

使用 `/locate` 命令测试结构是否正确生成：
```
/locate examplemod:my_structure
```

## 关联引用

- [地物](./NeoForge-世界生成-地物.md)
- [维度](./NeoForge-世界生成-维度.md)
- [生物群系修改器](./NeoForge-世界生成-生物群系修改器.md)
