# NeoForge 高级 - 特性标志

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/advanced/featureflags

## 概述

特性标志是一种允许开发者将一组特性 gating 在某些必需标志后面的系统。这些特性可以是注册的元素、游戏机制、数据包条目或 mod 的其他独特系统。

常见用例是将实验性特性/元素 gating 在实验性标志后面，允许用户轻松切换并在他们最终确定之前试用。

## 创建特性标志

要创建新的特性标志，需要创建一个 JSON 文件，并在 `neoforge.mods.toml` 的 `[[mods]]` 块中通过 `featureFlags` 条目引用：

```
# In neoforge.mods.toml:
[[mods]]
    featureFlags="META-INF/feature_flags.json"
```

JSON 文件结构：

```json
{
    "flags": [
        "examplemod:experimental"
    ]
}
```

## 获取特性标志

注册后可以通过 `FeatureFlagRegistry.getFlag(Identifier)` 获取特性标志：

```java
public static final FeatureFlag EXPERIMENTAL = FeatureFlags.REGISTRY.getFlag(
    Identifier.fromNamespaceAndPath("examplemod", "experimental")
);
```

## 特性元素

`FeatureElement` 是可以被赋予一组必需标志的注册表值。这些值只有在相应的必需标志与级别中启用的标志匹配时才对玩家可用。

当特性元素被禁用时，它会完全从玩家视野中隐藏，所有交互都会被跳过。

### 支持的注册表

- Item
- Block
- EntityType
- MenuType
- Potion
- MobEffect
- GameRule

### 标记元素

```java
// Item
DeferredRegister.Items ITEMS = DeferredRegister.createItems("examplemod");
DeferredItem<Item> EXPERIMENTAL_ITEM = ITEMS.registerSimpleItem("experimental", 
    props -> props.requiredFeatures(EXPERIMENTAL)
);

// Block
DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks("examplemod");
DeferredBlock<Block> EXPERIMENTAL_BLOCK = BLOCKS.registerSimpleBlock("experimental", 
    BlockBehaviour.Properties.of().requiredFeatures(EXPERIMENTAL)
);

// BlockItem 继承自 Block 的必需特性
DeferredItem<BlockItem> EXPERIMENTAL_BLOCK_ITEM = ITEMS.registerSimpleBlockItem(EXPERIMENTAL_BLOCK);

// EntityType
DeferredRegister<EntityType<?>> ENTITY_TYPES = DeferredRegister.create(Registries.ENTITY_TYPE, "examplemod");
DeferredHolder<EntityType<?>, EntityType<ExperimentalEntity>> EXPERIMENTAL_ENTITY = ENTITY_TYPES.register(
    "experimental",
    registryName -> EntityType.Builder.of(ExperimentalEntity::new, MobCategory.AMBIENT)
        .requiredFeatures(EXPERIMENTAL)
        .build(ResourceKey.create(Registries.ENTITY_TYPE, registryName))
);

// MenuType
DeferredRegister<MenuType<?>> MENU_TYPES = DeferredRegister.create(Registries.MENU, "examplemod");
DeferredHolder<MenuType<?>, MenuType<ExperimentalMenu>> EXPERIMENTAL_MENU = MENU_TYPES.register(
    "experimental",
    () -> new MenuType<>((IContainerFactory<ExperimentalMenu>) (windowId, inventory, buffer) -> new ExperimentalMenu(windowId, inventory, buffer),
        FeatureFlagSet.of(EXPERIMENTAL))
);

// MobEffect
DeferredRegister<MobEffect> MOB_EFFECTS = DeferredRegister.create(Registries.MOB_EFFECT, "examplemod");
DeferredHolder<MobEffect, ExperimentalMobEffect> EXPERIMENTAL_MOB_EFFECT = MOB_EFFECTS.register(
    "experimental",
    registryName -> new ExperimentalMobEffect(MobEffectCategory.NEUTRAL, CommonColors.WHITE)
        .requiredFeatures(EXPERIMENTAL)
);

// Potion
DeferredRegister<Potion> POTIONS = DeferredRegister.create(Registries.POTION, "examplemod");
DeferredHolder<Potion, ExperimentalPotion> EXPERIMENTAL_POTION = POTIONS.register(
    "experimental",
    registryName -> new ExperimentalPotion(registryName.toString(), new MobEffectInstance(EXPERIMENTAL_MOB_EFFECT))
        .requiredFeatures(EXPERIMENTAL)
);

// GameRule
DeferredRegister<GameRule> GAME_RULES = DeferredRegister.create(Registries.GAME_RULE, "examplemod");
DeferredHolder<GameRule, GameRule> EXPERIMENTAL_GAME_RULE = GAME_RULES.register(
    "experimental",
    registryName -> new GameRule(
        GameRuleCategory.MISC, GameRuleType.BOOL, BoolArgumentType.bool(),
        GameRuleTypeVisitor::visitBoolean, Codec.BOOL, bool -> bool ? 1 : 0, false,
        FeatureFlagSet.of(EXPERIMENTAL)
    )
);
```

## 验证启用状态

```java
// 获取启用的特性集
level.enabledFeatures();
entity.level().enabledFeatures();

// 客户端
minecraft.getConnection().enabledFeatures();

// 服务端
server.getWorldData().enabledFeatures();

// 验证
requiredFeatures.isSubsetOf(enabledFeatures);
featureElement.isEnabled(enabledFeatures);
itemStack.isItemEnabled(enabledFeatures);
```

> `ItemStack` 有特殊的 `isItemEnabled(FeatureFlagSet)` 方法，以便空堆栈即使其对应 Item 的必需特性不匹配也被视为已启用。

## 特性包

特性包是一种特殊的数据包，不仅加载资源和/或数据，还能切换给定的一组特性标志。

### pack.mcmeta 结构

```json
{
    "features": {
        "enabled": ["examplemod:experimental"]
    },
    "pack": { /* ... */ }
}
```

### 内置特性包

通过 `AddPackFindersEvent` 事件注册：

```java
@SubscribeEvent
public static void addFeaturePacks(final AddPackFindersEvent event) {
    event.addPackFinders(
        Identifier.fromNamespaceAndPath("examplemod", "data/examplemod/datapacks/experimental"),
        PackType.SERVER_DATA,
        Component.literal("ExampleMod: Experiments"),
        PackSource.FEATURE,
        false,
        Pack.Position.TOP
    );
}
```

### 单人游戏启用

1. 创建新世界
2. 进入 Experiments 屏幕
3. 切换所需的包
4. 点击 `Done` 确认

### 多人游戏启用

1. 打开服务器的 `server.properties` 文件
2. 将特性包 ID 添加到 `initial-enabled-packs`

## 数据生成

```java
@SubscribeEvent
public static void gatherData(final GatherDataEvent.Client event) {
    DataGenerator generator = event.getGenerator();
    
    PackGenerator featurePack = generator.getBuiltinDatapack(true, "examplemod", "experimental");
    
    featurePack.addProvider(output -> PackMetadataGenerator.forFeaturePack(
        output,
        Component.literal("Enabled experimental features for ExampleMod"),
        FeatureFlagSet.of(EXPERIMENTAL)
    ));
}
```

## 关联引用

- [访问转换器](./NeoForge-高级-访问转换器.md)
- [可扩展枚举](./NeoForge-高级-可扩展枚举.md)
