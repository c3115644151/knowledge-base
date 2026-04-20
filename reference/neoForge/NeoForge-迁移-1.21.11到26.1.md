# NeoForge 1.21.11 → 26.1 迁移指南

> **来源**：官方 Primer 文档 https://docs.neoforged.net/primer/docs/26.1/
> **更新时间**：2026-04-20
> **适用对象**：从 1.21.11 迁移到 26.1 的 Mod 开发者

---

## 📋 迁移概览

| 变更类别 | 影响程度 | 说明 |
|----------|----------|------|
| Java 21 → 25 | 🔴 高 | 必须升级 JDK 和 IDE |
| 反混淆 | 🟡 中 | 官方映射名称，可能影响部分代码 |
| Loot Type Unrolling | 🔴 高 | 战利品系统 API 重大重构 |
| Validation Overhaul | 🟡 中 | 验证系统重构 |
| Datapack Villager Trades | 🔴 高 | 村民交易数据化 |

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

### 4.4 代码迁移

**1.21.11**：
```java
VillagerTrades.ItemListing trade = new VillagerTrades.EmeraldForItems(
    Items.WHEAT, 20, 16, 2, 1
);
```

**26.1**：使用数据包 JSON 定义交易，参见上方格式。

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

## 6. 相关文档

- [NeoForge-入门.md](./NeoForge-入门.md) - 入门配置
- [NeoForge-服务端-战利品表.md](./NeoForge-服务端-战利品表.md) - 战利品系统（需更新）
- [NeoForge-高级.md](./NeoForge-高级.md) - 高级特性

---

*文档更新：2026-04-20*
*基于官方 Primer 1.21.11 → 26.1*
