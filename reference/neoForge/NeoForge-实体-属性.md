# NeoForge 实体属性系统

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/entities/attributes

## 概述

属性系统用于定义实体的各种数值属性，如生命值、攻击伤害、移动速度等。每个属性可以拥有多个修饰符来改变其基础值。

## API 速查表

### 核心类型

| 类型 | 说明 |
|------|------|
| `Attribute` | 属性定义 |
| `AttributeModifier` | 属性修饰符 |
| `RangedAttribute` | 带范围的属性 |
| `AttributeMap` | 属性映射 |

### AttributeModifier 操作

| 操作 | 说明 |
|------|------|
| `ADD_VALUE` | 加法（直接加到基础值） |
| `ADD_MULTIPLIED_BASE` | 乘法（乘以基础值的倍率） |
| `ADD_MULTIPLIED_TOTAL` | 乘法（乘以总和的倍率） |

---

## 代码示例

### 创建自定义属性

```java
// 1. 注册属性
public static final DeferredHolder<Attribute, Attribute> 
    MY_ATTRIBUTE = ATTRIBUTES.register(
        "my_attribute",
        () -> new RangedAttribute(
            "examplemod.my_attribute",  // 翻译键
            10.0,                       // 默认值
            0.0,                        // 最小值
            1024.0                      // 最大值
        )
    );

// 2. 使用简单的 Attribute（无范围限制）
public static final DeferredHolder<Attribute, Attribute> 
    NO_RANGE_ATTRIBUTE = ATTRIBUTES.register(
        "no_range_attribute",
        () -> new Attribute("examplemod.no_range", 5.0)
    );
);

// 3. 注册百分比属性
public static final DeferredHolder<Attribute, Attribute> 
    PERCENTAGE_ATTRIBUTE = ATTRIBUTES.register(
        "percentage_attribute",
        () -> Attribute.create("examplemod.percentage", 0.0)
    );
```

### 添加属性修饰符

```java
// 1. 在物品上定义属性
public static final DeferredItem<Item> MAGICAL_SWORD = 
    ITEMS.registerItem(
        "magical_sword",
        () -> new SwordItem(Tiers.DIAMOND, 5, -2.5f, 
            new Item.Properties()
                .attributes(
                    SwordItem.createAttributes(Tiers.DIAMOND, 5, -2.5f))
                .attributes(
                    ItemAttributes.create(
                        Attributes.ATTACK_DAMAGE,
                        2.0,
                        AttributeModifier.Operation.ADD_VALUE
                    ))
        ),
        Item.Properties::stacksTo
    );

// 2. 在护甲上定义属性
public static final DeferredItem<ArmorItem> COPPER_HELMET = 
    ITEMS.registerItem(
        "copper_helmet",
        () -> new ArmorItem(
            ArmorMaterials.COPPER,
            ArmorItem.Type.HELMET,
            new Item.Properties()
                .attributes(
                    ArmorItem.createAttributes(
                        ArmorMaterials.COPPER, 
                        ArmorItem.Type.HELMET)))
        ),
        Item.Properties::stacksTo
    );

// 3. 动态添加修饰符
public static void addModifier(LivingEntity entity, 
        UUID uuid, String name, double amount, 
        AttributeModifier.Operation operation) {
    
    AttributeInstance instance = entity.getAttribute(
        Attributes.ATTACK_DAMAGE);
    
    if (instance != null) {
        // 先移除旧修饰符
        instance.removeModifier(uuid);
        
        // 添加新修饰符
        instance.addTransientModifier(
            new AttributeModifier(
                uuid,
                name,
                amount,
                operation
            )
        );
    }
}

// 4. 使用装备监听
public static void onEquipmentChange(
        LivingEntity entity, EquipmentSlot slot, 
        ItemStack from, ItemStack to) {
    
    if (slot == EquipmentSlot.MAINHAND) {
        // 处理主手装备变化
    }
}
```

### 使用 AttributeMap

```java
public class AttributeHelper {
    // 获取属性值
    public static double getValue(LivingEntity entity, 
            Attribute attribute) {
        AttributeInstance instance = entity.getAttribute(attribute);
        return instance != null ? instance.getValue() : 0.0;
    }
    
    // 获取基础值
    public static double getBaseValue(LivingEntity entity, 
            Attribute attribute) {
        AttributeInstance instance = entity.getAttribute(attribute);
        return instance != null ? instance.getBaseValue() : 0.0;
    }
    
    // 设置基础值
    public static void setBaseValue(LivingEntity entity, 
            Attribute attribute, double value) {
        AttributeInstance instance = entity.getAttribute(attribute);
        if (instance != null) {
            instance.setBaseValue(value);
        }
    }
    
    // 检查是否有特定修饰符
    public static boolean hasModifier(LivingEntity entity, 
            Attribute attribute, UUID uuid) {
        AttributeInstance instance = entity.getAttribute(attribute);
        if (instance != null) {
            return instance.getModifier(uuid) != null;
        }
        return false;
    }
    
    // 移除修饰符
    public static void removeModifier(LivingEntity entity, 
            Attribute attribute, UUID uuid) {
        AttributeInstance instance = entity.getAttribute(attribute);
        if (instance != null) {
            instance.removeModifier(uuid);
        }
    }
}
```

### 注册默认属性

```java
// 在实体类型上注册默认属性
public static final DeferredHolder<EntityType<?>, 
        EntityType<MyEntity>> MY_ENTITY = ENTITY_TYPES.register(
    "my_entity",
    () -> EntityType.Builder.of(
            MyEntity::new,
            MobCategory.CREATURE
        )
        .sized(0.6f, 1.8f)
        .clientTrackingRange(8)
        .updateInterval(10)
        .build("examplemod:my_entity")
);

// 在事件中设置默认属性
@SubscribeEvent
public static void onAttributeCreation(
        EntityAttributeCreationEvent event) {
    event.put(
        MY_ENTITY.get(),
        Mob.createMobAttributes()
            .add(Attributes.MAX_HEALTH, 20.0)
            .add(Attributes.MOVEMENT_SPEED, 0.3)
            .add(Attributes.ATTACK_DAMAGE, 3.0)
            .add(Attributes.ARMOR, 2.0)
            .add(Attributes.ARMOR_TOUGHNESS, 1.0)
            // 添加自定义属性
            .add(ModAttributes.MY_ATTRIBUTE.get(), 10.0)
            .build()
    );
}
```

### 使用事件监听属性变化

```post="java"]
@SubscribeEvent
public static void onAttributeModifierAdd(
        EntityAttributeModificationEvent event) {
    // 为特定实体类型添加额外属性
    event.add(
        EntityTypes.PLAYER,
        Attributes.SWIFT_Sneak.SWIFT_SNEAK_SPEED
    );
}

@SubscribeEvent
public static void onLivingAttributeUpdate(
        LivingAttributeInstanceEvent event) {
    AttributeInstance instance = event.getInstance();
    // 监听属性值变化
}
```

---

## 内置属性参考

| 属性 | 类 | 默认值 | 说明 |
|------|-----|--------|------|
| `MAX_HEALTH` | RangedAttribute | 20.0 | 最大生命值 |
| `FOLLOW_RANGE` | RangedAttribute | 32.0 | 追踪范围 |
| `MOVEMENT_SPEED` | Attribute | 0.7 | 移动速度 |
| `ATTACK_DAMAGE` | Attribute | 2.0 | 攻击伤害 |
| `ATTACK_KNOCKBACK` | Attribute | 0.0 | 攻击击退 |
| `ARMOR` | Attribute | 0.0 | 护甲值 |
| `ARMOR_TOUGHNESS` | Attribute | 0.0 | 护甲韧性 |
| `KNOCKBACK_RESISTANCE` | Attribute | 0.0 | 击退抗性 |
| `LUCK` | RangedAttribute | 0.0 | 幸运值 |
| `SAFETY` | Attribute | 0.0 | 安全值 |
| `SWIFT_SNEAK_SPEED` | Attribute | 0.0 | 潜行速度 |
| `BURNING_TIME` | Attribute | 0.0 | 燃烧时间 |
| `SCALE` | Attribute | 1.0 | 缩放 |
| `STEP_HEIGHT` | Attribute | 0.6 | 跨步高度 |
| `BLOCK_INTERACTION_RANGE` | Attribute | 0.0 | 方块交互范围 |
| `ENTITY_INTERACTION_RANGE` | Attribute | 0.0 | 实体交互范围 |
| `FLYING_SPEED` | Attribute | 0.4 | 飞行速度 |
| `JUMP_STRENGTH` | Attribute | 0.42 | 跳跃强度 |

---

## 注意事项

### 属性计算顺序
1. 获取基础值
2. 应用 `ADD_MULTIPLIED_BASE` 修饰符
3. 应用 `ADD_VALUE` 修饰符
4. 应用 `ADD_MULTIPLIED_TOTAL` 修饰符

### 常见错误
1. **属性未注册**：`Attribute` 必须先注册才能使用
2. **修饰符冲突**：多个同 UUID 的修饰符会互相覆盖
3. **范围问题**：使用 `RangedAttribute` 限制值范围

### 最佳实践

```java
// 推荐：使用稳定的 UUID
public static final UUID MAGICAL_SWORD_BONUS_ID = 
    UUID.fromString("12345678-1234-1234-1234-123456789abc");

// 创建永久修饰符
public static AttributeModifier createModifier(
        double amount, 
        AttributeModifier.Operation operation) {
    return new AttributeModifier(
        MAGICAL_SWORD_BONUS_ID,
        "Magical Sword Bonus",
        amount,
        operation
    );
}
```

---

## 关联引用

- 实体基础：[NeoForge-实体](./NeoForge-实体.md)
- LivingEntity：[NeoForge-实体-LivingEntity](./NeoForge-实体-LivingEntity.md)
- 物品属性：[NeoForge-物品-工具](./NeoForge-物品-工具.md)
