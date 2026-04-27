# NeoForge 1.21.11 → 26.1 迁移指南

> **来源**：官方 Primer 文档 https://docs.neoforged.net/primer/docs/26.1/
> **更新时间**：2026-04-20
> **适用对象**：从 1.21.11 迁移到 26.1 的 Mod 开发者

---

## 📋 迁移概览

| 变更类别 | 影响程度 | 说明 | 文档章节 |
|----------|----------|------|----------|
| Java 21 → 25 | 🔴 高 | 必须升级 JDK 和 IDE | §1 |
| 反混淆 | 🟡 中 | 官方映射名称，`ResourceLocation` → `Identifier` | §1.3 |
| Loot Type Unrolling | 🔴 高 | 所有 `*Type` 类型移除，直接使用 `MapCodec` | §2 |
| Validation Overhaul | 🟡 中 | 验证系统重构，实现 `Validatable` 接口 | §3 |
| Datapack Villager Trades | 🔴 高 | 村民交易数据化，`VillagerTrades.ItemListing` → JSON | §4 |
| 其他 API 变化 | 🟡 中 | 类重命名、方法签名变化、移除/新增类型 | §6 |

---

## 1. Java 25 和反混淆

### 1.1 JDK 升级

**26.1 要求 Java 25 JDK**

| 项目 | 1.21.11 | 26.1 |
|------|---------|------|
| Java 版本 | 21 | **25** |
| 推荐 JDK | Microsoft OpenJDK 21 | [Microsoft OpenJDK 25](https://learn.microsoft.com/en-us/java/openjdk/download#openjdk-25) |

**IDE 支持要求**：

| IDE | 最低版本 |
|-----|----------|
| Eclipse | 2025-12，或 2025-09 + Java 25 Support 插件 |
| IntelliJ IDEA | 2025.2 |

### 1.2 Java 25 新特性

Vanilla 使用了 [JEP 447](https://openjdk.org/jeps/447)：允许在构造函数中 `super` 调用之前执行语句。

```java
// Java 25 新特性示例
public class Example {
    private final int value;
    
    public Example(int input) {
        // JEP 447: super 之前可以有语句
        if (input < 0) {
            throw new IllegalArgumentException("Input must be positive");
        }
        this.value = input;
        super(); // 现在可以在语句之后调用
    }
}
```

### 1.3 反混淆

**26.1 恢复了官方映射名称**：
- 所有值类型现在使用 Mojang 官方名称
- 部分内容因 Java 编译过程未被捕获（如内联原始类型和字符串常量）
- 仅影响使用非官方映射的用户或 Mod 加载器

---

## 2. Loot Type Unrolling（战利品类型展开）

### 2.1 核心变化

**重大 API 变化**：战利品相关类型不再使用包装对象，注册表直接持有 `MapCodec`。

| 原类型 | 新类型 |
|--------|--------|
| `LootPoolEntryType` | `MapCodec<LootPoolEntryContainer>` |
| `LootItemFunctionType` | `MapCodec<LootItemFunction>` |
| `LootItemConditionType` | `MapCodec<LootItemCondition>` |
| `LootNumberProviderType` | `MapCodec<NumberProvider>` |
| `LootNbtProviderType` | `MapCodec<NbtProvider>` |
| `LootScoreProviderType` | `MapCodec<ScoreboardNameProvider>` |
| `FloatProviderType` | `MapCodec<FloatProvider>` |
| `IntProviderType` | `MapCodec<IntProvider>` |

### 2.2 代码迁移示例

**1.21.11 写法**：
```java
public class NoopItemFunction implements LootItemFunction {
    public static final LootItemFunctionType TYPE = 
        new LootItemFunctionType(NoopItemFunction.CODEC);
    
    @Override
    public LootItemFunctionType getType() {
        return TYPE;
    }
}

// 注册
Registry.register(BuiltInRegistries.LOOT_FUNCTION_TYPE, 
    ResourceLocation.parse("examplemod:noop"), NoopItemFunction.TYPE);
```

**26.1 写法**：
```java
public record NoopItemFunction() implements LootItemFunction {
    public static final NoopItemFunction INSTANCE = new NoopItemFunction();
    
    // MapCodec 直接作为注册对象
    public static final MapCodec<NoopItemFunction> MAP_CODEC = 
        MapCodec.unit(INSTANCE);
    
    // getType 改为 codec
    @Override
    public MapCodec<NoopItemFunction> codec() {
        return MAP_CODEC;
    }
}

// 注册 MapCodec
Registry.register(BuiltInRegistries.LOOT_FUNCTION_TYPE,
    Identifier.fromNamespaceAndPath("examplemod", "noop"), 
    NoopItemFunction.MAP_CODEC);
```

### 2.3 FloatProvider 和 IntProvider 变化

**FloatProvider**：
- 从 `class` 改为 `interface`
- `CODEC` → `FloatProviders#CODEC`
- `codec()` → `FloatProviders#codec()`
- `getType()` → `codec()`（非一一对应）
- `getMinValue()` → `min()`
- `getMaxValue()` → `max()`
- `FloatProviderType` 接口已移除
- 所有子类型现在是 record

**IntProvider**：
- 从 `class` 改为 `interface`
- `CODEC` → `IntProviders#CODEC`
- `getMinValue()` → `minInclusive()`
- `getMaxValue()` → `maxInclusive()`
- `IntProviderType` 接口已移除
- 除 `WeightedListInt` 外，所有子类型现在是 record

### 2.4 受影响的注册表

| 注册表键 | 变化 |
|----------|------|
| `LOOT_POOL_ENTRY_TYPE` | 持有 `LootPoolEntryContainer` MapCodec |
| `LOOT_FUNCTION_TYPE` | 持有 `LootItemFunction` MapCodec |
| `LOOT_CONDITION_TYPE` | 持有 `LootItemCondition` MapCodec |
| `LOOT_NUMBER_PROVIDER_TYPE` | 持有 `NumberProvider` MapCodec |
| `LOOT_NBT_PROVIDER_TYPE` | 持有 `NbtProvider` MapCodec |
| `LOOT_SCORE_PROVIDER_TYPE` | 持有 `ScoreboardNameProvider` MapCodec |
| `FLOAT_PROVIDER_TYPE` | 持有 `FloatProvider` MapCodec |
| `INT_PROVIDER_TYPE` | 持有 `IntProvider` MapCodec |

---

## 3. Validation Overhaul（验证系统重构）

### 3.1 核心变化

验证处理器已重构，所有验证对象实现 `Validatable` 接口。

**Validatable 接口**：
```java
public interface Validatable {
    void validate(ValidationContext ctx);
}
```

### 3.2 验证示例

```java
@Override
public void validate(ValidationContext ctx) {
    if (this.foo() != this.bar()) {
        ctx.reportProblem(() -> "'Foo' does not equal 'bar'.");
    }
}

// 验证子字段
@Override
public void validate(ValidationContext ctx) {
    for (int i = 0; i < this.children.size(); i++) {
        var childCtx = ctx.forIndexedField("children", i);
        if (condition) {
            childCtx.reportProblem(() -> "Issue description");
        }
    }
}

// 验证 Validatable 子对象
@Override
public void validate(ValidationContext ctx) {
    Validatable.validate(ctx, "child", this.child);
}
```

### 3.3 Codec 集成

```java
public record ExampleObject() implements Validatable {
    public static final Codec<ExampleObject> CODEC = MapCodec.unitCodec(
        ExampleObject::new
    ).validate(
        Validatable.validatorForContext(LootContextParamSets.ALL_PARAMS)
    );
}
```

### 3.4 受影响的类

| 类 | 变化 |
|----|------|
| `CriterionTriggerInstance` | `validate()` 接受 `ValidationContextSource` |
| `ContextAwarePredicate` | 实现 `Validatable` |
| `ConditionalEffect` | 实现 `Validatable` |
| `TargetedConditionalEffect` | 实现 `Validatable` |
| `IntRange` | 实现 `LootContextUser` |
| `LootContextUser` | 实现 `Validatable` |
| `LootDataType` | 泛型必须扩展 `Validatable` |
| `LootPool` | 实现 `Validatable` |
| `LootTable` | 实现 `Validatable` |
| `LootPoolEntryContainer` | 实现 `Validatable` |

---

## 4. Datapack Villager Trades（数据包村民交易）

### 4.1 核心变化

村民交易从代码定义变为数据包注册表。

| 概念 | 说明 |
|------|------|
| `VillagerTrade` | 单个交易定义 |
| `TradeSet` | 交易集合，定义可选交易池 |
| 文件位置 | `data/<namespace>/villager_trade/<path>.json` |

### 4.2 交易格式示例

```json
{
    "wants": {
        "id": "minecraft:apple",
        "count": {
            "type": "minecraft:uniform",
            "min": 1,
            "max": 5
        },
        "components": {
            "minecraft:custom_name": "Apple...?"
        }
    },
    "additional_wants": {
        "id": "minecraft:emerald"
    },
    "gives": {
        "id": "minecraft:golden_apple",
        "count": 1,
        "components": {
            "minecraft:custom_name": "Not an Apple"
        }
    },
    "max_uses": {
        "type": "minecraft:uniform",
        "min": 1,
        "max": 20
    },
    "reputation_discount": {
        "type": "minecraft:uniform",
        "min": 0,
        "max": 0.05
    },
    "xp": {
        "type": "minecraft:uniform",
        "min": 10,
        "max": 20
    },
    "merchant_predicate": {
        "condition": "minecraft:entity_properties",
        "entity": "this",
        "predicate": {
            "predicates": {
                "minecraft:villager/variant": ["minecraft:desert", "minecraft:snow"]
            }
        }
    },
    "given_item_modifiers": [
        {
            "function": "minecraft:enchant_randomly",
            "include_additional_cost_component": true,
            "options": "#minecraft:trades/desert_common"
        }
    ],
    "double_trade_price_enchantments": "#minecraft:trades/desert_common"
}
```

### 4.3 TradeSet 格式

**文件位置**：`data/<namespace>/trade_set/<path>.json`

```json
{
    "trades": "#examplemod:example_profession/level_1",
    "amount": {
        "type": "minecraft:uniform",
        "min": 1,
        "max": 5
    },
    "allow_duplicates": true,
    "random_sequence": "examplemod:example_profession/level_1"
}
```

### 4.4 Item Listing 转换示例

#### EmeraldForItems → JSON

**1.21.11 代码**：
```java
VillagerTrades.ItemListing trade = new VillagerTrades.EmeraldForItems(
    Items.WHEAT,  // 想要的物品
    20,           // 物品数量
    16,           // 最大使用次数
    2,            // 经验值
    1             // 返回的绿宝石数量
);
```

**26.1 JSON**：
```json
{
    "gives": {
        "count": 1,
        "id": "minecraft:emerald"
    },
    "max_uses": 16,
    "reputation_discount": 0.05,
    "wants": {
        "count": 20,
        "id": "minecraft:wheat"
    },
    "xp": 2
}
```

#### ItemsForEmeralds → JSON

**1.21.11 代码**：
```java
VillagerTrades.ItemListing trade = new VillagerTrades.ItemsForEmeralds(
    Items.BREAD,  // 给予的物品
    1,            // 绿宝石数量
    6,            // 物品数量
    16,           // 最大使用次数
    1,            // 经验值
    0.05f         // 价格乘数
);
```

**26.1 JSON**：
```json
{
    "gives": {
        "count": 6,
        "id": "minecraft:bread"
    },
    "max_uses": 16,
    "reputation_discount": 0.05,
    "wants": {
        "count": 1,
        "id": "minecraft:emerald"
    },
    "xp": 1
}
```

#### EnchantBookForEmeralds → JSON

**1.21.11 代码**：
```java
VillagerTrades.ItemListing trade = new VillagerTrades.EnchantBookForEmeralds(
    30,                                    // 经验值
    3,                                     // 最小附魔等级
    3,                                     // 最大附魔等级
    EnchantmentTags.TRADES_DESERT_SPECIAL  // 附魔标签
);
```

**26.1 JSON**：
```json
{
    "additional_wants": {
        "id": "minecraft:book"
    },
    "double_trade_price_enchantments": "#minecraft:double_trade_price",
    "given_item_modifiers": [
        {
            "function": "minecraft:enchant_with_levels",
            "include_additional_cost_component": true,
            "levels": {
                "type": "minecraft:uniform",
                "min": 3,
                "max": 3
            },
            "options": ["minecraft:efficiency"]
        }
    ],
    "gives": {
        "count": 1,
        "id": "minecraft:enchanted_book"
    },
    "max_uses": 12,
    "reputation_discount": 0.2,
    "wants": {
        "count": {
            "type": "minecraft:sum",
            "summands": [11.0, {"type": "minecraft:uniform", "max": 35.0, "min": 0.0}]
        },
        "id": "minecraft:emerald"
    },
    "xp": 30
}
```

#### Villager Variants（村民变体）

某些交易根据村民类型提供不同选项，现在使用 `merchant_predicate` 检查：

```json
{
    "merchant_predicate": {
        "condition": "minecraft:entity_properties",
        "entity": "this",
        "predicate": {
            "predicates": {
                "minecraft:villager/variant": "minecraft:desert"
            }
        }
    }
}
```

### 4.5 新注册表

| 注册表键 | 说明 |
|----------|------|
| `TRADE_SET` | 交易集合 |
| `VILLAGER_TRADE` | 单个交易 |

### 4.6 VillagerProfession 变化

```java
public static final VillagerProfession EXAMPLE = Registry.register(
    BuiltInRegistries.VILLAGER_PROFESSION,
    Identifier.fromNamespaceAndPath("examplemod", "example_profession"),
    new VillagerProfession(
        Component.literal(""),
        p -> true,
        p -> true,
        ImmutableSet.of(),
        ImmutableSet.of(),
        null,
        // 新增：职业等级到交易集的映射
        Int2ObjectMap.ofEntries(
            Int2ObjectMap.entry(
                1,
                ResourceKey.create(Registries.TRADE_SET, 
                    Identifier.fromNamespaceAndPath("examplemod", "example_profession/level_1"))
            )
        )
    )
);
```

---

## 5. 迁移检查清单

### 环境配置
- [ ] 安装 Java 25 JDK
- [ ] 更新 `JAVA_HOME` 环境变量
- [ ] 更新 IDE 到支持 Java 25 的版本
- [ ] 更新 Gradle 项目配置

### Loot 系统
- [ ] 检查所有自定义 `LootItemFunction`，迁移到 MapCodec
- [ ] 检查所有自定义 `LootItemCondition`，迁移到 MapCodec
- [ ] 检查所有自定义 `LootPoolEntryContainer`，迁移到 MapCodec
- [ ] 检查 `IntProvider` 和 `FloatProvider` 的使用
- [ ] 将 `getType()` 改为 `codec()`
- [ ] 将 `CODEC` 字段改为 `MAP_CODEC`

### 验证系统
- [ ] 为自定义 Loot 对象实现 `Validatable` 接口
- [ ] 更新 `validate` 方法签名
- [ ] 检查 `CriterionTriggerInstance` 的 `validate` 方法

### 村民交易
- [ ] 将代码定义的交易迁移到数据包 JSON
- [ ] 创建 `villager_trade/` 和 `trade_set/` 数据包目录
- [ ] 更新 `VillagerProfession` 定义

---

## 6. 其他重要 API 变化

以下为官方文档中记录的其他重要变化摘要，完整列表请参考 [官方 Primer](https://docs.neoforged.net/primer/docs/26.1/)。

### 6.1 包级别变化

| 包 | 变化概述 |
|----|----------|
| `net.minecraft.util.valueproviders` | `CODEC` → `MAP_CODEC`，`FloatProvider`/`IntProvider` 从 class 改为 interface |
| `net.minecraft.world.level.storage.loot.*` | 所有 `*Type` 类型移除，直接使用 `MapCodec` |
| `net.minecraft.advancements.criterion` | `CriterionValidator` → `ValidationContextSource` + `Validatable` |
| `net.minecraft.world.item.enchantment` | `ConditionalEffect` 实现 `Validatable`，`codec` 不再需要 `ContextKeySet` |
| `net.minecraft.world.entity.npc.villager` | `VillagerTrades` 拆分为多个类，交易移至数据包 |

### 6.2 重要类变化

| 类 | 变化 |
|----|------|
| `Identifier` | 替代 `ResourceLocation`（官方映射）|
| `CompilableString` | 替代 `SelectorPattern` |
| `ResolutionContext` | 替代 `CommandSourceStack` + `Entity` 在组件解析中 |
| `BlockState` | 构造函数签名变化，不再接受 `MapCodec` |
| `DataGenerator` | 现为抽象类，原有实现在 `DataGenerator$Cached` |
| `LevelAccessor` | 不再实现 `LevelReader` |
| `SnowyDirtBlock` | → `SnowyBlock` |
| `SpreadingSnowyDirtBlock` | → `SpreadingSnowyBlock` |
| `IceSpikeFeature` | → `SpikeFeature`（非一一对应）|
| `FollowBoatGoal` | → `FollowPlayerRiddenEntityGoal` |

### 6.3 方法签名变化

| 方法/字段 | 变化 |
|-----------|------|
| `LootItemFunction#getType()` | → `codec()` |
| `LootItemCondition#getType()` | → `codec()` |
| `FloatProvider#getMinValue()` | → `min()` |
| `FloatProvider#getMaxValue()` | → `max()` |
| `IntProvider#getMinValue()` | → `minInclusive()` |
| `IntProvider#getMaxValue()` | → `maxInclusive()` |
| `Player#currentImpulseImpactPos` | → `LivingEntity#currentImpulseImpactPos` |
| `Brightness#pack()` | → `LightCoordsUtil#pack()` |
| `Entity#getTags()` | → `entityTags()` |
| `LivingEntity#canAttackType()` | → `canAttack()`，参数变化 |
| `LivingEntity#lungeForwardMaybe()` | → `postPiercingAttack()` |
| `LivingEntity#entityAttackRange()` | → `getAttackRangeWith()` |
| `BlockBehaviour$BlockStateBase#hasPostProcess()` | → `getPostProcessPos()` |
| `TreeConfiguration#dirtProvider` | → `belowTrunkProvider` |
| `TreeConfiguration#forceDirt` | → `belowTrunkProvider`（语义变化）|

### 6.4 移除的类型

| 移除的类型 | 替代方案 |
|------------|----------|
| `LootPoolEntryType` | `MapCodec<LootPoolEntryContainer>` |
| `LootItemFunctionType` | `MapCodec<LootItemFunction>` |
| `LootItemConditionType` | `MapCodec<LootItemCondition>` |
| `LootNumberProviderType` | `MapCodec<NumberProvider>` |
| `LootNbtProviderType` | `MapCodec<NbtProvider>` |
| `LootScoreProviderType` | `MapCodec<ScoreboardNameProvider>` |
| `FloatProviderType` | `MapCodec<FloatProvider>` |
| `IntProviderType` | `MapCodec<IntProvider>` |
| `CriterionValidator` | `ValidationContextSource` + `Validatable` |
| `SelectorPattern` | `CompilableString` |
| `Blocks`（references）| `BlockIds` |
| `Items`（references）| `ItemIds` |
| `FOREST_ROCK`（Feature）| `BLOCK_BLOB` |
| `ICE_SPIKE`（Feature）| `SPIKE` |

### 6.5 新增类型

| 新增类型 | 说明 |
|----------|------|
| `Validatable` | 验证接口 |
| `ValidationContext` | 验证上下文 |
| `ValidationContextSource` | 验证上下文源 |
| `FloatProviders` | 所有 vanilla float providers 注册处 |
| `IntProviders` | 所有 vanilla int providers 注册处 |
| `VillagerTrade` | 单个村民交易（数据包）|
| `TradeSet` | 交易集合（数据包）|
| `CompilableString` | 可编译字符串，替代 `SelectorPattern` |
| `ResolutionContext` | 组件解析上下文 |
| `BlockBlobConfiguration` | BlockBlobFeature 配置 |

---

## 7. Pack Changes

### 7.1 数据包目录单数化

26.1 将大部分数据包目录从复数形式改为单数形式。**这是 DLC（Data Loading Change）层面的破坏性变更**，不改变 Java API，但改变资源路径。

| 目录 | 1.21.11（旧） | 26.1（新） |
|------|--------------|-----------|
| 战利品表 | `loot_tables/` | **`loot_table/`** |
| 进度 | `advancements/` | **`advancement/`** |
| 配方 | `recipes/` | **`recipe/`** |

**影响**：所有 `data/<namespace>/loot_tables/` 下的 JSON 文件必须移动到 `data/<namespace>/loot_table/`。在旧路径下的文件不会被加载，导致战利品表不生效且无日志错误。

**正确的资源路径示例**：
```
# ✅ 26.1 正确路径
src/main/resources/data/relictales/loot_table/blocks/suspicious_mossy_cobblestone.json

# ❌ 1.21.11 旧路径（26.1 不会加载）
src/main/resources/data/relictales/loot_tables/blocks/suspicious_mossy_cobblestone.json
```

### 7.2 完整变更列表

可在 [Misode's version changelog](https://misode.github.io/versions/?id=26.1&tab=changelog) 查看完整列表。

---

## 8. 相关文档

- [NeoForge-入门.md](./NeoForge-入门.md) - 入门配置
- [NeoForge-服务端-战利品表.md](./NeoForge-服务端-战利品表.md) - 战利品系统（需更新）
- [NeoForge-高级.md](./NeoForge-高级.md) - 高级特性

---

*文档更新：2026-04-20*
*基于官方 Primer 1.21.11 → 26.1*
