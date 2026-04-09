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
