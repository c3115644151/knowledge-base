# NeoForge LivingEntity 与生物逻辑

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/entities/livingentity

## 概述

LivingEntity 是所有具有生命值的实体的基类，包括玩家、动物、怪物等。本文档涵盖生物的伤害、治疗、自然生成等核心逻辑。

## API 速查表

### 核心类型

| 类型 | 说明 |
|------|------|
| `LivingEntity` | 生命实体基类 |
| `DamageContainer` | 伤害容器 |
| `Mob` | 生物实体基类 |
| `Player` | 玩家实体 |

### 伤害事件

| 事件 | 说明 |
|------|------|
| `LivingIncomingDamageEvent` | 接收伤害前 |
| `LivingHurtEvent` | 受到伤害时 |
| `LivingDamageEvent` | 伤害应用后 |
| `LivingDeathEvent` | 死亡时 |
| `LivingHealEvent` | 治疗时 |

---

## 代码示例

### 伤害处理

```java
// 1. 监听伤害事件
@SubscribeEvent
public static void onLivingHurt(LivingHurtEvent event) {
    LivingEntity entity = event.getEntity();
    DamageSource source = event.getSource();
    float amount = event.getAmount();
    
    // 减少火焰伤害
    if (source.is(DamageTypes.IN_FIRE)) {
        event.setAmount(amount * 0.5f);
    }
}

// 2. 拦截伤害
@SubscribeEvent
public static void onIncomingDamage(
        LivingIncomingDamageEvent event) {
    LivingEntity entity = event.getEntity();
    DamageSource source = event.getSource();
    float amount = event.getAmount();
    
    // 免疫虚空伤害
    if (source.is(DamageTypes.OUT_OF_WORLD)) {
        event.setCanceled(true);
    }
}

// 3. 监听死亡
@SubscribeEvent
public static void onLivingDeath(LivingDeathEvent event) {
    LivingEntity entity = event.getEntity();
    DamageSource source = event.getSource();
    
    if (entity instanceof Player player) {
        // 玩家死亡处理
    }
}
```

### 治疗处理

```java
// 1. 治愈实体
public static void heal(LivingEntity entity, float amount) {
    entity.heal(amount);
}

// 2. 监听治疗
@SubscribeEvent
public static void onLivingHeal(LivingHealEvent event) {
    LivingEntity entity = event.getEntity();
    float amount = event.getAmount();
    
    // 限制治疗量
    event.setAmount(Math.min(amount, 2.0f));
}
```

### 自然生成

```java
// 1. 注册生成限制
@SubscribeEvent
public static void registerSpawnPlacements(
        RegisterSpawnPlacementsEvent event) {
    event.register(
        ModEntities.CUSTOM_MOB.get(),
        SpawnPlacementTypes.ON_GROUND,
        Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
        (type, level, reason, pos, random) -> {
            // 检查生成条件
            BlockState state = level.getBlockState(pos);
            return state.isSolid() && 
                   level.getRawBrightness(pos, 0) > 8;
        },
        SpawnPlacements.Entry::configure
    );
}

// 2. 设置实体属性
@SubscribeEvent
public static void onAttributeCreation(
        EntityAttributeCreationEvent event) {
    event.put(
        ModEntities.CUSTOM_MOB.get(),
        Mob.createMobAttributes()
            .add(Attributes.MAX_HEALTH, 20.0)
            .add(Attributes.MOVEMENT_SPEED, 0.3)
            .add(Attributes.ATTACK_DAMAGE, 3.0)
            .build()
    );
}
```

---

## 注意事项

### 伤害流程
1. `LivingIncomingDamageEvent` - 可取消
2. 护甲计算
3. `LivingHurtEvent` - 可修改伤害值
4. 效果应用
5. `LivingDamageEvent`
6. `LivingDeathEvent` 或 死亡

### 常见错误
1. **死亡不触发**：未正确处理 `LivingDeathEvent`
2. **伤害无效**：`hurt` 返回 false 表示伤害被免疫
3. **生成失败**：检查 `SpawnPlacementTypes` 配置

---

## 关联引用

- 实体基础：[NeoForge-实体](./NeoForge-实体.md)
- 实体数据：[NeoForge-实体-数据](./NeoForge-实体-数据.md)
- 实体属性：[NeoForge-实体-属性](./NeoForge-实体-属性.md)
