# NeoForge 状态效果与药水

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/items/mobeffects

## 概述

状态效果（MobEffect）用于给生物添加各种状态改变，如加速、隐身、中毒等。药水（Potion）则是将效果瓶装化的方式。

## API 速查表

### 核心类型

| 类型 | 说明 |
|------|------|
| `MobEffect` | 状态效果基类 |
| `MobEffectInstance` | 效果实例 |
| `MobEffectCategory` | 效果类别（BENEFICIAL/HARMFUL/NEUTRAL） |
| `InstantenousMobEffect` | 即时效果 |
| `Potion` | 药水类型 |
| `PotionBrewing` | 药水酿造系统 |

### MobEffectCategory

| 值 | 说明 | 药水颜色 |
|----|------|----------|
| `BENEFICIAL` | 正面效果 | 蓝色 |
| `HARMFUL` | 负面效果 | 红色 |
| `NEUTRAL` | 中性效果 | 灰色 |

---

## 代码示例

### 创建状态效果

```java
// 1. 创建基础状态效果
public static final DeferredHolder<MobEffect, MobEffect> CUSTOM_EFFECT = 
    MOB_EFFECTS.register(
        "custom_effect",
        () -> new MobEffect(
            MobEffectCategory.BENEFICIAL,  // 效果类别
            0x00FF00)                       // 粒子颜色
        {
            @Override
            public void applyEffectTick(
                    LivingEntity entity, 
                    int amplifier) {
                // 每tick执行的逻辑
                entity.heal(0.5f);  // 每tick恢复0.5生命
            }
            
            @Override
            public boolean shouldApplyEffectTickThisTick(
                    int duration, int amplifier) {
                // 返回true表示此tick应用效果
                return true;
            }
        }
    );

// 2. 创建即时效果
public static final DeferredHolder<MobEffect, 
        InstantEffect> INSTANT_HEAL = MOB_EFFECTS.register(
    "instant_heal",
    () -> new InstantEffect(
        (pAgent, pLevel, pEntity) -> {
            // 即时给予治疗
            if (pEntity != null) {
                pEntity.heal(4.0f);
                // 播放粒子效果
                if (pEntity.level().isClientSide) {
                    pAgent.makeParticles(
                        ParticleTypes.HEART, 
                        pEntity.getX(), 
                        pEntity.getY() + 0.5, 
                        pEntity.getZ());
                }
            }
        })
);

// 3. 创建有条件的效果
public static final DeferredHolder<MobEffect, MobEffect> NUTRITION = 
    MOB_EFFECTS.register(
        "nutrition",
        () -> new MobEffect(
            MobEffectCategory.BENEFICIAL, 0x8B4513)
        {
            @Override
            public boolean shouldApplyEffectTickThisTick(
                    int duration, int amplifier) {
                // 仅在有饥饿值时应用
                return duration % 20 == 0;  // 每秒检查一次
            }
            
            @Override
            public void applyEffectTick(
                    LivingEntity entity, 
                    int amplifier) {
                if (entity instanceof Player player) {
                    FoodData foodData = player.getFoodData();
                    // 增加饱食度
                    foodData.eat(1, 0.1f);
                }
            }
        }
    );
```

### 创建药水

```java
// 1. 创建基础药水
public static final DeferredHolder<Potion, Potion> CUSTOM_POTION = 
    POTIONS.register(
        "custom_potion",
        () -> new Potion(
            new MobEffectInstance(
                ModMobEffects.CUSTOM_EFFECT.get(),  // 效果
                3600,                                // 持续时间(ticks)
                0                                    // 等级
            )
        )
    );

// 2. 创建延长版药水
public static final DeferredHolder<Potion, Potion> LONG_CUSTOM_POTION = 
    POTIONS.register(
        "long_custom_potion",
        () -> new Potion(
            new MobEffectInstance(
                ModMobEffects.CUSTOM_EFFECT.get(),
                9600,  // 8分钟
                0
            )
        )
    );

// 3. 创建增强版药水
public static final DeferredHolder<Potion, Potion> STRONG_CUSTOM_POTION = 
    POTIONS.register(
        "strong_custom_potion",
        () -> new Potion(
            new MobEffectInstance(
                ModMobEffects.CUSTOM_EFFECT.get(),
                1800,  // 3分钟
                1      // II级
            )
        )
    );
```

### 药水酿造配方

```java
// 1. 添加药水酿造配方
@Mod.EventBusSubscriber(modid = MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD)
public static class BrewingRecipes {
    @SubscribeEvent
    public static void registerBrewingRecipes(
            RegisterPotionBrewingRecipesEvent event) {
        // 基础药水 -> 目标药水
        event.addMix(
            Potions.AWKWARD,          // 基础药水
            Items.BLAZE_POWDER,       // 添加物
            ModPotions.CUSTOM_POTION   // 结果药水
        );
        
        // 药水 -> 延长版药水
        event.addMix(
            ModPotions.CUSTOM_POTION,
            Items.REDSTONE,
            ModPotions.LONG_CUSTOM_POTION
        );
        
        // 药水 -> 增强版药水
        event.addMix(
            ModPotions.CUSTOM_POTION,
            Items.GLOWSTONE_DUST,
            ModPotions.STRONG_CUSTOM_POTION
        );
    }
}

// 2. 使用 PotionBrewing 直接添加
@SubscribeEvent
public static void onBrewingRecipes(
        RegisterPotionBrewingRecipesEvent event) {
    // 修改酿造配方
    event.addMix(
        Potions.POISON,
        Items.SUGAR,
        Potions.SWIFTNESS
    );
}
```

### 使用效果实例

```java
// 1. 添加效果
public static void addEffect(LivingEntity entity) {
    // 基础用法
    entity.addEffect(new MobEffectInstance(
        ModMobEffects.CUSTOM_EFFECT.get(),
        3600,  // 3分钟
        0      // 等级
    ));
    
    // 带概率
    if (entity.level().random.nextFloat() < 0.3f) {
        entity.addEffect(new MobEffectInstance(
            ModMobEffects.CUSTOM_EFFECT.get(),
            3600, 0
        ));
    }
}

// 2. 检查是否有效果
public static boolean hasEffect(LivingEntity entity) {
    return entity.hasEffect(ModMobEffects.CUSTOM_EFFECT.get());
}

// 3. 获取效果
public static int getAmplifier(LivingEntity entity) {
    MobEffectInstance effect = 
        entity.getEffect(ModMobEffects.CUSTOM_EFFECT.get());
    if (effect != null) {
        return effect.getAmplifier();  // 返回等级 (0 = I级)
    }
    return -1;
}

// 4. 移除效果
public static void removeEffect(LivingEntity entity) {
    entity.removeEffect(ModMobEffects.CUSTOM_EFFECT.get());
}

// 5. 清除所有效果
public static void clearEffects(LivingEntity entity) {
    entity.removeAllEffects();
}
```

### 药水瓶物品

```java
// 1. 创建药水瓶物品
public static final DeferredItem<Item> CUSTOM_POTION_ITEM = 
    ITEMS.registerItem(
        "custom_potion",
        () -> new PotionItem(
            new Item.Properties()
                .stacksTo(1)
                .craftRemainder(Items.GLASS_BOTTLE)
        ),
        Item.Properties::stacksTo
    );

// 2. 创建可饮用药水
public static final DeferredItem<Item> CUSTOM_SPLASH_POTION = 
    ITEMS.registerItem(
        "custom_splash_potion",
        () -> new SplashPotionItem(
            new Item.Properties()
                .stacksTo(1)
                .craftRemainder(Items.GLASS_BOTTLE)
        ),
        Item.Properties::stacksTo
    );

// 3. 创建投射药水
public static final DeferredItem<Item> CUSTOM_LINGERING_POTION = 
    ITEMS.registerItem(
        "custom_lingering_potion",
        () -> new LingeringPotionItem(
            new Item.Properties()
                .stacksTo(1)
                .craftRemainder(Items.GLASS_BOTTLE)
        ),
        Item.Properties::stacksTo
    );

// 4. 创建药水箭矢
public static final DeferredItem<ArrowItem> CUSTOM_POTION_ARROW = 
    ITEMS.registerItem(
        "custom_potion_arrow",
        () -> new ArrowItem(
            new Item.Properties().stacksTo(64)
        ) {
            @Override
            public ItemStack getDefaultStack() {
                ItemStack stack = new ItemStack(this);
                stack.set(DataComponents.POTION, 
                    new PotionContentsData(
                        new MobEffectInstance(
                            ModMobEffects.CUSTOM_EFFECT.get(),
                            3600)));
                return stack;
            }
        },
        Item.Properties::stacksTo
    );
```

---

## 注意事项

### 版本差异
- NeoForge 1.21.x 使用 `MobEffect` 而非旧版 `MobEffect`
- 药水使用 `PotionContentsData` 而非直接设置 NBT
- `MobEffectInstance` 构造方法有变化

### 常见问题
1. **效果不生效**：检查 `shouldApplyEffectTickThisTick` 返回值
2. **药水酿造失败**：确认添加物是有效的酿造材料
3. **药水颜色错误**：检查 `MobEffect` 构造函数中的颜色参数

### 最佳实践

```java
// 推荐：在服务端注册药水
@Mod.EventBusSubscriber(modid = MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD)
public static class Registries {
    @SubscribeEvent
    public static void registerPotions(RegisterPotionsEvent event) {
        event.register(
            ModPotions.CUSTOM_POTION.getId(),
            ModPotions.CUSTOM_POTION
        );
    }
}
```

---

## 关联引用

- 物品基础：[NeoForge-物品](./NeoForge-物品.md)
- 消耗品：[NeoForge-物品-消耗品](./NeoForge-物品-消耗品.md)
- 实体逻辑：[NeoForge-实体-LivingEntity](./NeoForge-实体-LivingEntity.md)
