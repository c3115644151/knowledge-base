# NeoForge 世界生成 - 维度（Dimensions）

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/worldgen/dimensions

## 概述

维度（Dimensions）是 Minecraft 中的独立世界，每个维度有其自己的地形生成规则、环境设置和物理特性。NeoForge 允许 mod 开发者创建完全自定义的维度。

## 核心组件

### DimensionType

定义维度的基本属性：
- 是否有无尽深渊
- 是否有明暗周期
- 是否缩放聊天
- 燃烧时间
- 望远镜缩放
- 下界缩放
- 预测性生成
- 最小 Y 高度和高度

### ChunkGenerator

定义如何生成该维度的地形：
- `NoiseBasedChunkGenerator` - 基于噪声的地形生成
- `FlatLevelSource` - 平坦地形（用于超平坦）

### WorldPreset

预设维度组合，如主世界、下界、末地。

## 创建自定义维度

### 1. 创建 DimensionType

```java
public class ModDimensionTypes {
    public static final ResourceKey<DimensionType> MY_DIMENSION = 
        ResourceKey.create(Registries.DIMENSION_TYPE, 
            new ResourceLocation(ExampleMod.MODID, "my_dimension"));

    public static void bootstrap(RegisterCapabilitiesEvent event) {
        // DimensionType 通过 JSON 注册
    }
}
```

### 2. JSON 配置

`data/examplemod/dimension_type/my_dimension.json`:

```json
{
    "height": 384,
    "logical_height": 384,
    "bed_works": false,
    "has_raid": false,
    "has_skylight": true,
    "has_ceiling": false,
    "coordinate_scale": 1.0,
    "ambient_light": 0.0,
    "ultrawarm": false,
    "natural": true,
    "respawn_anchor_works": false,
    "min_y": -64,
    "monster_spawn_block_light_limit": 0,
    "monster_spawn_light_level": {
        "type": "minecraft:constant",
        "value": 7
    }
}
```

### 3. 创建维度

`data/examplemod/dimension/my_dimension.json`:

```json
{
    "type": "examplemod:my_dimension",
    "generator": {
        "type": "minecraft:noise",
        "settings": "minecraft:overworld",
        "biome_source": {
            "type": "minecraft:fixed",
            "biome": "examplemod:my_biome"
        }
    }
}
```

### 4. 使用 NoiseBasedChunkGenerator

```json
{
    "type": "minecraft:overworld",
    "settings": "minecraft:overworld",
    "biome_source": {
        "type": "minecraft:multi_noise",
        "preset": "minecraft:overworld"
    }
}
```

#### 自定义 NoiseSettings

```java
// 注册自定义噪声设置
public static final ResourceKey<NoiseGeneratorSettings> MY_SETTINGS = 
    ResourceKey.create(
        Registries.NOISE_GENERATOR_SETTINGS,
        new ResourceLocation(ExampleMod.MODID, "my_settings")
    );

// JSON: data/examplemod/worldgen/noise_settings/my_settings.json
{
    "sea_level": 63,
    "disable_mob_generation": false,
    "aquifers_enabled": true,
    "ore_veins_enabled": true,
    "legacy_random_source": false,
    "default_block": {
        "Name": "minecraft:stone"
    },
    "default_fluid": {
        "Name": "minecraft:water",
        "Properties": {
            "level": "0"
        }
    },
    "noise": {
        "min_y": -64,
        "height": 384,
        "size_horizontal": 1,
        "size_vertical": 2
    },
    "surface_rules": {
        "surface_type": "minecraft:stone",
        "foundation_type": "minecraft:stone",
        "decorator_types": {
            "top": "minecraft:grass",
            "sea_floor": "minecraft:gravel",
            "floor_multiplier": "minecraft:stone",
            "wall": "minecraft:cobblestone"
        },
        "underground": {
            "accessibility": "minecraft:stone"
        }
    }
}
```

## WorldPreset

创建预设维度组合：

```java
// 注册自定义预设
public static final ResourceKey<WorldPreset> MY_PRESET = 
    ResourceKey.create(
        Registries.WORLD_PRESET,
        new ResourceLocation(ExampleMod.MODID, "my_preset")
    );

// JSON: data/examplemod/world_preset/my_preset.json
{
    "dimensions": {
        "minecraft:overworld": {
            "type": "minecraft:overworld",
            "generator": {
                "type": "minecraft:noise",
                "settings": "minecraft:overworld",
                "biome_source": {
                    "type": "minecraft:fixed",
                    "biome": "minecraft:plains"
                }
            }
        },
        "examplemod:my_dimension": {
            "type": "examplemod:my_dimension",
            "generator": "examplemod:my_generator"
        }
    }
}
```

## 创建维度入口（传送门）

```java
public class MyPortalBlock extends Block {
    @Override
    public void playerWillDestroy(Player player, BlockPos pos, BlockState state, 
            BlockEntity blockEntity) {
        // 传送逻辑
    }
}

// 注册维度
public class ModDimensions {
    public static final ResourceKey<Level> MY_DIMENSION_KEY = 
        ResourceKey.create(Registries.DIMENSION, 
            new ResourceLocation(ExampleMod.MODID, "my_dimension"));
    
    public static final HolderGetter<DimensionType> getDimensionType() {
        return BuiltInRegistries.DIMENSION_TYPE.asLookup()
            .getOrThrow(ModDimensionTypes.MY_DIMENSION);
    }
}
```

## 维度规则

| 规则 | 说明 |
|------|------|
| `bed_works` | 床是否可用 |
| `has_raid` | 是否有袭击事件 |
| `has_skylight` | 是否有天空光 |
| `has_ceiling` | 是否有天花板 |
| `ultrawarm` | 是否为超温（影响水蒸发） |
| `natural` | 是否为自然维度 |
| `respawn_anchor_works` | 重生锚是否可用 |
| `logical_height` | 逻辑高度（影响传送门高度限制） |

## 关联引用

- [地物](./NeoForge-世界生成-地物.md)
- [结构](./NeoForge-世界生成-结构.md)
- [生物群系修改器](./NeoForge-世界生成-生物群系修改器.md)
