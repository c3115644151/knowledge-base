# NeoForge-服务端-进度

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/resources/server/advancements

## 概述

进度（Advancements）是类似任务的系统，玩家可以完成它们。进度基于进度条件，并在完成时执行行为。

通过在命名空间的 `advancement` 子文件夹中创建 JSON 文件添加新进度。

## JSON 结构

```json
{
    "parent": "examplemod:parent_advancement",  // 父进度 ID
    "display": {
        "icon": {
            "item": "minecraft:diamond"
        },
        "title": {"translate": "advancements.example.title"},
        "description": {"translate": "advancements.example.description"},
        "frame": "task",  // "task", "goal", "challenge"
        "background": "examplemod:textures/advancement.png",
        "show_toast": true,
        "announce_to_chat": true,
        "hidden": false
    },
    "criteria": {
        "example_criterion": {
            "trigger": "minecraft:inventory_changed",
            "conditions": {
                "items": [{"items": ["minecraft:diamond"]}]
            }
        }
    },
    "requirements": [["example_criterion"]],
    "rewards": {
        "experience": 100,
        "loot": ["examplemod:loot/example_loot"],
        "recipes": ["examplemod:recipe/example_recipe"]
    }
}
```

## 自定义触发器

### 创建触发器实例

```java
public record ExampleTriggerInstance(Optional<ContextAwarePredicate> player, ItemPredicate predicate)
        implements SimpleCriterionTrigger.SimpleInstance {
    
    public boolean matches(ItemStack stack) {
        return this.predicate.test(stack);
    }
}
```

### 创建触发器

```java
public class ExampleCriterionTrigger extends SimpleCriterionTrigger<ExampleTriggerInstance> {
    public void trigger(ServerPlayer player, ItemStack stack) {
        this.trigger(player, triggerInstance -> triggerInstance.matches(stack));
    }
}
```

### 注册触发器

```java
public static final DeferredRegister<CriterionTrigger<?>> TRIGGER_TYPES =
    DeferredRegister.create(Registries.TRIGGER_TYPE, ExampleMod.MOD_ID);

public static final Supplier<ExampleCriterionTrigger> EXAMPLE_TRIGGER =
    TRIGGER_TYPES.register("example", ExampleCriterionTrigger::new);
```

### 定义 Codec

```java
public record ExampleTriggerInstance(Optional<ContextAwarePredicate> player, ItemPredicate predicate)
        implements SimpleCriterionTrigger.SimpleInstance {
    
    public static final Codec<ExampleTriggerInstance> CODEC = RecordCodecBuilder.create(instance ->
        instance.group(
            EntityPredicate.ADVANCEMENT_CODEC.optionalFieldOf("player").forGetter(ExampleTriggerInstance::player),
            ItemPredicate.CODEC.fieldOf("item").forGetter(ExampleTriggerInstance::predicate)
        ).apply(instance, ExampleTriggerInstance::new)
    );
}

public class ExampleCriterionTrigger extends SimpleCriterionTrigger<ExampleTriggerInstance> {
    @Override
    public Codec<ExampleTriggerInstance> codec() {
        return ExampleTriggerInstance.CODEC;
    }
}
```

### 触发进度

```java
EXAMPLE_TRIGGER.get().trigger(player, itemStack);
```

## 数据生成

```java
@SubscribeEvent
public static void gatherData(GatherDataEvent.Client event) {
    event.createProvider((output, lookupProvider) ->
        new AdvancementProvider(output, lookupProvider, List.of(
            ExampleClass::generateExampleAdvancements
        ))
    );
}
```

```java
public static void generateExampleAdvancements(HolderLookup.Provider registries, 
                                              Consumer<AdvancementHolder> saver) {
    Advancement.Builder.advancement()
        .parent(AdvancementSubProvider.createPlaceholder("minecraft:story/root"))
        .display(
            new ItemStack(Items.GRASS_BLOCK),
            Component.translatable("advancements.examplemod.example.title"),
            Component.translatable("advancements.examplemod.example.description"),
            null,
            AdvancementType.GOAL,
            true, true, false
        )
        .rewards(AdvancementRewards.Builder.experience(100))
        .addCriterion("pickup_dirt", InventoryChangeTrigger.TriggerInstance.hasItems(Items.DIRT))
        .requirements(AdvancementRequirements.allOf(List.of("pickup_dirt")))
        .save(saver, Identifier.fromNamespaceAndPath("examplemod", "example_advancement"));
}
```

## 进度框架类型

| 类型 | 说明 |
|------|------|
| `task` | 普通任务（默认） |
| `goal` | 目标，显示金色边框 |
| `challenge` | 挑战，显示深紫色边框 |

## 注意事项

1. **进度树**：根进度显示在进度界面
2. **条件**：一个进度可以有多个条件，需要全部满足
3. **父进度**：定义进度树结构
4. **奖励**：可给予经验、配方、战利品表或执行函数

## 关联引用

- [[NeoForge-服务端资源]] - 服务端资源总览
- [[NeoForge-服务端-战利品表]] - 战利品表
- [[NeoForge-服务端-配方]] - 配方系统
