# NeoForge 消耗品与食物

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/items/consumables

## 概述

消耗品系统用于实现可食用的物品、可饮用的药水，以及使用后产生特定效果的物品。

## API 速查表

### 核心类型

| 类型 | 说明 |
|------|------|
| `FoodProperties` | 食物属性 |
| `Consumable` | 可消耗属性 |
| `ConsumeEffect` | 消耗效果 |
| `ItemUseAnimation` | 使用动画枚举 |
| `UseAction` | 使用动作枚举 |

### Consumable 工厂方法

| 方法 | 说明 |
|------|------|
| `Consumable.of()` | 创建基础消耗品 |
| `Consumable.builder()` | 创建构建器 |
| `.whenConsumed(ConsumeEffect)` | 消耗时触发效果 |
| `.drink()` | 设为饮品 |
| `.eat()` | 设为食物 |

### ConsumeEffect 类型

| 类型 | 说明 |
|------|------|
| `ConsumeEffect.give(ItemStack)` | 给予物品 |
| `ConsumeEffect.set(ItemStack)` | 设置物品 |
| `ConsumeEffect.apply(MobEffectInstance)` | 给予状态效果 |
| `ConsumeEffect.remove()` | 移除物品 |

---

## 代码示例

### 基础食物

```java
// 在 Item.Properties 中设置食物属性
public static final DeferredItem<Item> APPLE = ITEMS.registerItem(
    "apple",
    Item::new,
    props -> props
        .stacksTo(64)
        .food(new FoodProperties.Builder()
            .nutrition(4)                    // 饱食度
            .saturationModifier(0.3f)        // 饱和度加成
            .build())
);

// 或者使用 DataComponent（推荐方式）
public static final DeferredItem<Item> APPLE = ITEMS.registerItem(
    "apple",
    Item::new,
    props -> props
        .stacksTo(64)
        .component(DataComponents.FOOD, 
            new FoodProperties.Builder()
                .nutrition(4)
                .saturationModifier(0.3f)
                .build())
);
```

### 高级食物效果

```java
public static final DeferredItem<Item> ENCHANTED_GOLDEN_APPLE = 
    ITEMS.registerItem(
        "enchanted_golden_apple",
        Item::new,
        props -> props
            .stacksTo(64)
            .food(new FoodProperties.Builder()
                .nutrition(4)
                .saturationModifier(1.2f)
                .effect(() -> new MobEffectInstance(
                    MobEffects.REGENERATION,   // 生命恢复
                    100,                       // 持续时间
                    1                          // 等级
                ), 1.0f)                      // 概率
                .effect(() -> new MobEffectInstance(
                    MobEffects.DAMAGE_RESISTANCE,
                    100, 0), 1.0f)
                .effect(() -> new MobEffectInstance(
                    MobEffects.FIRE_RESISTANCE,
                    100, 0), 1.0f)
                .alwaysEdible()               // 即使满饱也可以吃
                .meat()                       // 可喂狼
                .fast()                       // 快速食用
                .build())
    );
```

### 自定义消耗品

```java
public class CustomConsumable extends Item {
    public CustomConsumable() {
        super(Item.Properties.of()
            .food(new FoodProperties.Builder()
                .nutrition(2)
                .saturationModifier(0.1f)
                .build())
            .useCooldown(1.0)  // 使用冷却
        );
    }
    
    @Override
    public ItemDefaultAnimation getUseAnimation(ItemStack stack) {
        return ItemDefaultAnimation.EAT;  // 或 DRINK
    }
    
    @Override
    public int getUseDuration(ItemStack stack) {
        return 32;  // 1.6秒
    }
    
    @Override
    public SoundEvent getDrinkingSound(ItemStack stack) {
        return SoundEvents.GENERIC_DRINK;
    }
    
    @Override
    public SoundEvent getEatingSound(ItemStack stack) {
        return SoundEvents.GENERIC_EAT;
    }
    
    @Override
    public ItemStack finishUsingItem(ItemStack stack, 
            Level level, LivingEntity entity) {
        if (!level.isClientSide) {
            // 服务端：添加自定义效果
            if (entity instanceof ServerPlayer player) {
                player.addEffect(new MobEffectInstance(
                    MobEffects.SPEED, 600, 1));
            }
        }
        
        // 消耗物品
        if (entity instanceof Player player 
                && !player.getAbilities().instabuild) {
            stack.shrink(1);
        }
        
        return stack;
    }
}
```

### 使用 Consumable 组件

```java
// 创建可消耗物品（使用 DataComponent）
public static final DeferredItem<Item> MAGIC_POTION = 
    ITEMS.registerItem(
        "magic_potion",
        Item::new,
        props -> props
            .stacksTo(1)
            .component(DataComponents.CONSUMABLE, 
                Consumable.builder()
                    .drink()  // 饮品动画
                    .whenConsumed(
                        ConsumeEffect.apply(
                            new MobEffectInstance(
                                MobEffects.NIGHT_VISION, 
                                3600)))
                    .whenConsumed(
                        ConsumeEffect.give(
                            new ItemStack(Items.GLASS_BOTTLE)))
                    .build())
    );

// 干草球式消耗
public static final DeferredItem<Item> HAY_BALE_ITEM = 
    ITEMS.registerItem(
        "hay_bale",
        Item::new,
        props -> props
            .stacksTo(64)
            .component(DataComponents.CONSUMABLE,
                Consumable.builder()
                    .eat()  // 食物动画
                    .whenConsumed(
                        ConsumeEffect.apply(
                            new MobEffectInstance(
                                ModEffects.SATISFACTION.get(), 
                                1200)))
                    .build())
    );
```

### 药水酿造

```java
// 注册自定义药水
public static final DeferredHolder<MobEffect, 
        InstantEffect> CUSTOM_EFFECT = MOB_EFFECTS.register(
    "custom_effect",
    () -> new InstantEffect(
        (pAgent, pLevel, pEntity) -> {
            // 即时效果逻辑
            pAgent.teleportTo(pEntity.getX(), 
                pEntity.getY() + 10, pEntity.getZ());
        })
);

public static final DeferredHolder<MobEffect, 
        MobEffect> LONG_CUSTOM_EFFECT = MOB_EFFECTS.register(
    "long_custom_effect",
    () -> new MobEffect(MobEffectCategory.BENEFICIAL, 0x00FF00) {
        @Override
        public void applyEffectTick(LivingEntity entity, 
                int amplifier) {
            // 持续效果逻辑
        }
        @Override
        public boolean shouldApplyEffectTickThisTick(
                int duration, int amplifier) {
            return true;
        }
    }
);

// 酿造配方
public static final DeferredHolder<Potion, Potion> CUSTOM_POTION = 
    POTIONS.register(
        "custom_potion",
        () -> new Potion(
            new MobEffectInstance(CUSTOM_EFFECT.get(), 3600)));
```

---

## 注意事项

### 食物属性值

| 属性 | 说明 | 范围 |
|------|------|------|
| `nutrition` | 饱食度恢复量 | 0-20 |
| `saturationModifier` | 饱和度加成系数 | 0-∞ |
| `canAlwaysEat` | 总是可以吃 | boolean |
| `fastFood` | 快速食用 | boolean |

### 常见问题
1. **食物不消失**：`finishUsingItem` 中忘记 `stack.shrink(1)`
2. **无消耗**：使用 `consumable` 组件时自动处理消耗
3. **效果不生效**：检查 `MobEffectInstance` 参数是否正确

### 最佳实践

```java
@Override
public ItemStack finishUsingItem(ItemStack stack, 
        Level level, LivingEntity entity) {
    // 播放音效（在客户端）
    if (entity instanceof Player player) {
        player.playSound(SoundEvents.GENERIC_EAT, 0.5f, 
            0.8f / (level.random.nextFloat() * 0.4f + 1.2f));
    }
    
    // 服务端逻辑
    if (!level.isClientSide) {
        // 添加效果等
    }
    
    // 消耗物品（保留创造模式）
    if (entity instanceof Player player 
            && !player.getAbilities().instabuild) {
        stack.shrink(1);
    }
    
    return stack;
}
```

---

## 关联引用

- 物品基础：[NeoForge-物品](./NeoForge-物品.md)
- 数据组件：[NeoForge-物品-数据组件](./NeoForge-物品-数据组件.md)
- 状态效果：[NeoForge-物品-状态效果](./NeoForge-物品-状态效果.md)
