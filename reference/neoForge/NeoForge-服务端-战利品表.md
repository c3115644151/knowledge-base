# NeoForge 战利品表

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/resources/server/loottables

## 概述

战利品表（Loot Tables）是定义随机战利品掉落的数据驱动系统。Minecraft 在方块破坏、实体死亡、箱子打开等场景中使用战利品表。

## 文件位置

```
data/<namespace>/loot_table/<path>.json
```

例如：`data/minecraft/loot_table/blocks/dirt.json`

---

## 基础结构

```json
{
    "type": "minecraft:entity",
    "pools": [
        {
            "rolls": 1,
            "bonus_rolls": 0,
            "entries": [
                {
                    "type": "minecraft:item",
                    "name": "minecraft:diamond",
                    "weight": 1,
                    "quality": 0,
                    "functions": []
                }
            ],
            "conditions": [],
            "functions": []
        }
    ],
    "functions": [],
    "random_sequence": "minecraft:entities/pig"
}
```

---

## 代码示例

### 基本战利品表

```json
// data/examplemod/loot_table/blocks/custom_ore.json
{
    "type": "minecraft:block",
    "pools": [
        {
            "rolls": 1,
            "entries": [
                {
                    "type": "minecraft:item",
                    "name": "examplemod:raw_ore"
                }
            ],
            "conditions": [
                {
                    "condition": "minecraft:survives_explosion"
                }
            ]
        }
    ]
}
```

### 复杂掉落

```json
{
    "type": "minecraft:entity",
    "pools": [
        {
            "rolls": {
                "type": "minecraft:uniform",
                "min": 1,
                "max": 3
            },
            "entries": [
                {
                    "type": "minecraft:item",
                    "name": "minecraft:iron_ingot",
                    "weight": 10
                },
                {
                    "type": "minecraft:item",
                    "name": "minecraft:gold_ingot",
                    "weight": 1,
                    "functions": [
                        {
                            "function": "minecraft:set_count",
                            "count": {
                                "type": "minecraft:uniform",
                                "min": 1,
                                "max": 2
                            }
                        }
                    ]
                },
                {
                    "type": "minecraft:tag",
                    "name": "minecraft:coals",
                    "expand": true
                }
            ],
            "functions": [
                {
                    "function": "minecraft:looting_enchant",
                    "count": {
                        "type": "minecraft:uniform",
                        "min": 0,
                        "max": 1
                    }
                }
            ]
        }
    ]
}
```

### 数据生成

```java
// 1. 创建 LootTableProvider
@Mod.EventBusSubscriber(modid = MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD)
public static class LootTableGen {
    @SubscribeEvent
    public static void gatherData(GatherDataEvent event) {
        event.createProvider((output, lookupProvider) ->
            new LootTableProvider(
                output,
                Set.of(),
                List.of(
                    new SubProviderEntry(
                        BlockLootSubProvider::new,
                        LootContextParamSets.BLOCK
                    ),
                    new SubProviderEntry(
                        EntityLootSubProvider::new,
                        LootContextParamSets.ENTITY
                    )
                ),
                lookupProvider
            )
        );
    }
}

// 2. 方块掉落
public class BlockLootSubProvider extends BlockLootSubProvider {
    protected BlockLootSubProvider(
            HolderLookup.Provider registries) {
        super(Set.of(), FeatureFlags.DEFAULT_FLAGS, registries);
    }
    
    @Override
    protected Iterable<Block> getKnownBlocks() {
        return ModBlocks.BLOCKS.getEntries()
            .stream()
            .map(DeferredHolder::value)
            .toList();
    }
    
    @Override
    protected void generate() {
        // 直接掉落
        dropSelf(ModBlocks.COPPER_ORE.get());
        
        // 带附魔掉落
        add(ModBlocks.SILVER_ORE.get(),
            createOreDrop(
                ModBlocks.SILVER_ORE.get(),
                ModItems.RAW_SILVER.get()));
        
        // Silk Touch 掉落
        add(ModBlocks.TREASURE_CHEST.get(),
            createSingleItemTable(
                ModItems.TREASURE.get()));
        
        // 多个掉落
        add(ModBlocks.MULTI_DROP.get(), block ->
            createMultiDropTable(
                ModItems.DROP_A.get(),
                ModItems.DROP_B.get()));
    }
}

// 3. 实体掉落
public class EntityLootSubProvider extends EntityLootSubProvider {
    protected EntityLootSubProvider(
            HolderLookup.Provider registries) {
        super(FeatureFlags.DEFAULT_FLAGS, registries);
    }
    
    @Override
    protected Stream<EntityType<?>> getKnownEntityTypes() {
        return ModEntities.ENTITIES.getEntries()
            .stream()
            .map(DeferredHolder::value);
    }
    
    @Override
    protected void generate() {
        add(ModEntities.CUSTOM_BOSS.get(),
            createSingleItemTable(ModItems.BOSS_TROPHY.get()));
        
        add(ModEntities.CUSTOM_MOB.get(),
            LootTable.lootTable()
                .withPool(LootPool.lootPool()
                    .add(LootItem.lootTableItem(Items.DIAMOND))
                    .when(LootWeather.RAINING))
                .withPool(LootPool.lootPool()
                    .add(LootItem.lootTableItem(Items.GOLD_INGOT))
                    .when(LivingEntityNotDead.NOT_RIDEABLE)));
    }
}
```

### 战利品表条件

```json
// 条件示例
{
    "condition": "minecraft:entity_properties",
    "predicate": {
        "entity": "this",
        "properties": {
            "on_fire": true
        }
    }
}

{
    "condition": "minecraft:damage_source_properties",
    "predicate": {
        "source_entity": {
            "type": "minecraft:player"
        }
    }
}

{
    "condition": "minecraft:killed_by_player"
}

{
    "condition": "minecraft:random_chance_with_looting",
    "chance": 0.1,
    "looting_multiplier": 0.05
}
```

### 战利品表函数

```json
// 函数示例
{
    "function": "minecraft:set_count",
    "count": 3
}

{
    "function": "minecraft:set_count",
    "count": {
        "type": "minecraft:uniform",
        "min": 1,
        "max": 5
    }
}

{
    "function": "minecraft:add_player_count",
    "count": {
        "type": "minecraft:uniform",
        "min": 1,
        "max": 3
    }
}

{
    "function": "minecraft:furnace_smelt"
}

{
    "function": "minecraft:enchant_with_levels",
    "levels": {
        "type": "minecraft:uniform",
        "min": 10,
        "max": 30
    }
}
```

---

## 触发战利品表

```java
// 1. 获取战利品表
LootTable lootTable = level.getServer().reloadableRegistries()
    .getLootTable(key);

// 2. 构建参数
LootParams.Builder paramsBuilder = 
    new LootParams.Builder((ServerLevel) level);
paramsBuilder.withParameter(
    LootContextParams.ORIGIN, position);
paramsBuilder.withParameter(
    LootContextParams.THIS_ENTITY, entity);
paramsBuilder.withLuck(player.getLuck());

// 3. 生成掉落
LootParams params = paramsBuilder.create(
    LootContextParamSets.EMPTY);
List<ItemStack> drops = lootTable.getRandomItems(params);

// 4. 生成到世界
for (ItemStack drop : drops) {
    ItemEntity itemEntity = new ItemEntity(
        level,
        position.getX(), position.getY(), position.getZ(),
        drop);
    level.addFreshEntity(itemEntity);
}
```

---

## 考古战利品表（Archaeology）

> **重要**：考古战利品表与方块/实体战利品表**完全独立**。BrushableBlockEntity 在刷取完成时使用 `LootContextParamSets.ARCHAEOLOGY` 参数集加载战利品表。

### 考古战利品表 vs 普通战利品表

| 属性 | 方块战利品表 | 考古战利品表 |
|------|-------------|-------------|
| `type` | `minecraft:block` | **`minecraft:archaeology`** |
| 上下文参数集 | `LootContextParamSets.BLOCK` | `LootContextParamSets.ARCHAEOLOGY` |
| `rolls` 类型 | int 或 `NumberProvider` | **float**（如 `1.0`） |
| pool conditions | 支持 | **不支持**（ARCHAEOLOGY 参数集为空） |
| `random_sequence` | 可选 | **建议显式设置** |

### 正确格式

```json
{
  "type": "minecraft:archaeology",
  "pools": [
    {
      "rolls": 1.0,
      "bonus_rolls": 0.0,
      "entries": [
        { "type": "minecraft:item", "name": "minecraft:emerald", "weight": 1 },
        { "type": "minecraft:item", "name": "minecraft:bone", "weight": 2 }
      ]
    }
  ],
  "random_sequence": "relictales:blocks/suspicious_mossy_cobblestone"
}
```

### 注意事项

1. `rolls` 使用 **float** 值（`1.0`），不是 int（`1`）
2. **不能**包含 pool level conditions（如 `survives_explosion`）
3. 文件路径：`data/<namespace>/loot_table/blocks/<name>.json`
4. 由 `BrushableBlockEntity.unpackLootTable()` 在内部加载，不需要手动调用

---

## 注意事项

### 性能考虑
- 避免在战利品表中使用复杂函数
- 合理使用 `bonus_rolls` 而非多 `rolls`

### 常见错误
1. **掉落不生效**：检查 JSON 路径和文件名
2. **条件不满足**：确认条件是否正确配置
3. **数据生成失败**：确保 Provider 正确注册

---

## 关联引用

- 方块：[NeoForge-方块](./NeoForge-方块.md)
- 实体：[NeoForge-实体](./NeoForge-实体.md)
- 数据生成：[NeoForge-服务端-数据生成](./NeoForge-服务端-数据生成.md)


---

## 🔄 26.1 版本重大变化

> **重要**：26.1 对战利品系统进行了重大重构，详见 [NeoForge-迁移-1.21.11到26.1.md](./NeoForge-迁移-1.21.11到26.1.md)

### Loot Type Unrolling

**核心变化**：战利品相关类型不再使用包装对象，注册表直接持有 `MapCodec`。

#### 注册表变化

| 注册表键 | 1.21.11 | 26.1 |
|----------|---------|------|
| `LOOT_POOL_ENTRY_TYPE` | `LootPoolEntryType` | `MapCodec<LootPoolEntryContainer>` |
| `LOOT_FUNCTION_TYPE` | `LootItemFunctionType` | `MapCodec<LootItemFunction>` |
| `LOOT_CONDITION_TYPE` | `LootItemConditionType` | `MapCodec<LootItemCondition>` |
| `LOOT_NUMBER_PROVIDER_TYPE` | `LootNumberProviderType` | `MapCodec<NumberProvider>` |
| `LOOT_NBT_PROVIDER_TYPE` | `LootNbtProviderType` | `MapCodec<NbtProvider>` |
| `LOOT_SCORE_PROVIDER_TYPE` | `LootScoreProviderType` | `MapCodec<ScoreboardNameProvider>` |

#### 自定义 LootItemFunction 迁移

**1.21.11 写法**：
```java
public class CustomFunction implements LootItemFunction {
    public static final LootItemFunctionType TYPE = 
        new LootItemFunctionType(CustomFunction.CODEC);
    
    @Override
    public LootItemFunctionType getType() {
        return TYPE;
    }
}

// 注册
Registry.register(BuiltInRegistries.LOOT_FUNCTION_TYPE, 
    ResourceLocation.parse("examplemod:custom"), CustomFunction.TYPE);
```

**26.1 写法**：
```java
public record CustomFunction(/* 参数 */) implements LootItemFunction {
    public static final MapCodec<CustomFunction> MAP_CODEC = 
        RecordCodecBuilder.mapCodec(instance ->
            instance.group(
                // 参数 codec
            ).apply(instance, CustomFunction::new)
        );
    
    @Override
    public MapCodec<CustomFunction> codec() {
        return MAP_CODEC;
    }
}

// 注册
Registry.register(BuiltInRegistries.LOOT_FUNCTION_TYPE,
    Identifier.fromNamespaceAndPath("examplemod", "custom"), 
    CustomFunction.MAP_CODEC);
```

#### 自定义 LootItemCondition 迁移

**1.21.11 写法**：
```java
public class CustomCondition implements LootItemCondition {
    public static final LootItemConditionType TYPE = 
        new LootItemConditionType(CustomCondition.CODEC);
    
    @Override
    public LootItemConditionType getType() {
        return TYPE;
    }
}
```

**26.1 写法**：
```java
public record CustomCondition(/* 参数 */) implements LootItemCondition {
    public static final MapCodec<CustomCondition> MAP_CODEC = 
        RecordCodecBuilder.mapCodec(instance ->
            instance.group(
                // 参数 codec
            ).apply(instance, CustomCondition::new)
        );
    
    @Override
    public MapCodec<CustomCondition> codec() {
        return MAP_CODEC;
    }
}
```

#### 字段重命名

- `CODEC` → `MAP_CODEC`
- `getType()` → `codec()`

### Validation Overhaul

战利品对象现在需要实现 `Validatable` 接口：

```java
public class CustomLootObject implements Validatable {
    @Override
    public void validate(ValidationContext ctx) {
        // 验证逻辑
        if (someCondition) {
            ctx.reportProblem(() -> "问题描述");
        }
    }
}
```

### 受影响的类

| 类 | 变化 |
|----|------|
| `LootTable` | 实现 `Validatable` |
| `LootPool` | 实现 `Validatable` |
| `LootPoolEntryContainer` | 实现 `Validatable` |
| `LootContextUser` | 实现 `Validatable` |
| `NumberProvider` | `getType()` → `codec()` |
| `NbtProvider` | 实现 `LootContextUser`，`getType()` → `codec()` |

---

## 迁移检查清单

- [ ] 所有自定义 `LootItemFunction` 迁移到 MapCodec
- [ ] 所有自定义 `LootItemCondition` 迁移到 MapCodec
- [ ] 所有自定义 `LootPoolEntryContainer` 迁移到 MapCodec
- [ ] 将 `getType()` 改为 `codec()`
- [ ] 将 `CODEC` 字段改为 `MAP_CODEC`
- [ ] 为自定义 Loot 对象实现 `Validatable`（如需要）
