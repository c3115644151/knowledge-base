# NeoForge 伤害类型系统

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/resources/server/damagetypes

## 概述

伤害类型（DamageType）系统定义了游戏中各种伤害的属性，包括死亡消息、资源位置、护甲减免等。

## API 速查表

### 核心类型

| 类型 | 说明 |
|------|------|
| `DamageType` | 伤害类型 |
| `DamageSource` | 伤害来源 |
| `DamageScaling` | 伤害缩放枚举 |

### DamageScaling 值

| 值 | 说明 |
|----|------|
| `NEVER` | 不缩放（无敌） |
| `WHEN_CAUSED_BY_LIVING_NON_MOB` | 被非怪物生物攻击时 |
| `WHEN_CAUSED_BY_SAME_SURVIVOR` | 被相同幸存者攻击 |
| `ALWAYS` | 总是缩放 |

---

## 代码示例

### 创建伤害类型

```java
// 1. 注册伤害类型
public static final DeferredHolder<DamageType, DamageType> 
    CUSTOM_DAMAGE = DAMAGE_TYPES.register(
        "custom_damage",
        () -> new DamageType(
            "examplemod.customDamage",  // 翻译键
            0.1f,                       // 饥饿消耗比例
            0.5f                        // 经验消耗比例
        )
    );

// 2. 使用 DamageScaling
public static final DeferredHolder<DamageType, DamageType> 
    MAGIC_DAMAGE = DAMAGE_TYPES.register(
        "magic_damage",
        () -> new DamageType(
            "examplemod.magicDamage",
            DamageScaling.WHEN_CAUSED_BY_LIVING_NON_MOB,
            0.0f,  // 无饥饿消耗
            1.0f   // 全额经验
        )
    );
```

### 创建伤害来源

```java
// 1. 基本伤害来源
DamageSource source = new DamageSource(
    ModDamageTypes.CUSTOM_DAMAGE.get(),
    entity,          // 伤害来源实体
    directEntity,    // 直接造成伤害的实体
    x, y, z          // 伤害位置
);

// 2. 使用 DamageSources 辅助类
DamageSource magicDamage = entity.damageSources().magic(
    Entity,         // 魔法来源
    float amount     // 伤害量
);

DamageSource fallDamage = entity.damageSources().fall();

DamageSource inFire = entity.damageSources().inFire();

DamageSource onFire = entity.damageSources().onFire();

DamageSource lava = entity.damageSources().lava();

DamageSource cramming = entity.damageSources().cramming();

DamageSource drowning = entity.damageSources().drowning();

DamageSource starvation = entity.damageSources().starve();

DamageSource cactus = entity.damageSources().cactus();

DamageSource wall = entity.damageSources().thorns(
    Entity,          // 荆棘来源
    float amount     // 伤害量
);

// 3. 造成伤害
public boolean damage(LivingEntity target, float amount) {
    DamageSource source = new DamageSource(
        ModDamageTypes.MAGIC_DAMAGE.get(),
        this.entity,   // 攻击者
        this.entity,   // 直接来源
        target.getX(), target.getY(), target.getZ()
    );
    
    return target.hurt(source, amount);
}
```

### 自定义伤害消息

```java
// 1. 在 lang 文件中定义消息
// en_us.json
{
    "death.attack.examplemod.customDamage": "%1$s was vaporized by %2$s",
    "death.attack.examplemod.customDamage.player": "%1$s tried to touch %2$s's fire",
    "message.examplemod.customDamage": "You took %1$s damage!"
}

// 2. 创建自定义死亡消息
public class CustomDeathMessage implements EntityDamageSource {
    public CustomDeathMessage(DamageType type, 
            LivingEntity entity, 
            LivingEntity killer) {
        super(type, entity, killer);
    }
    
    @Override
    public Component getLocalizedDeathMessage(
            LivingEntity entity, 
            LivingEntity killer) {
        String key = "death.attack." + this.type().msgId();
        return Component.translatable(key,
            entity.getDisplayName(),
            killer.getDisplayName());
    }
}
```

### 伤害缩放与护甲

```java
// 1. 造成可护甲减免的伤害
DamageSource genericDamage = entity.damageSources().generic()
    .type(ModDamageTypes.MAGIC_DAMAGE.get());

entity.hurt(genericDamage, 10.0f);  // 可被护甲减免

// 2. 造成无视护甲的伤害
DamageSource bypassArmor = entity.damageSources().magic()
    .bypassArmor();

entity.hurt(bypassArmor, 5.0f);  // 无视护甲

// 3. 造成无敌帧无效的伤害
DamageSource noInvul = entity.damageSources().outOfWorld()
    .type(ModDamageTypes.VOID.get())
    .bypassInvulnerableTimes()
    .bypassArmor()
    .bypassEnchantments();
```

### 事件监听

```post="java"]
// 1. 监听伤害事件
@SubscribeEvent
public static void onLivingHurt(LivingHurtEvent event) {
    DamageSource source = event.getSource();
    LivingEntity entity = event.getEntity();
    
    // 检查伤害类型
    if (source.is(DamageTypes.MAGIC)) {
        event.setAmount(event.getAmount() * 0.8f);
    }
    
    // 检查是否是玩家
    if (entity instanceof Player player) {
        // 特殊处理
    }
}

// 2. 监听伤害防御
@SubscribeEvent
public static void onLivingDamageShield(
        LivingShieldBlockEvent event) {
    // 当盾牌格挡时
    DamageSource source = event.getDamageSource();
    LivingEntity entity = event.getEntity();
    float damage = event.getDamage();
    
    // 自定义盾牌格挡逻辑
}
```

---

## 内置伤害类型

| 类型 | 说明 |
|------|------|
| `IN_FIRE` | 在火中 |
| `LIGHTNING_BOLT` | 闪电 |
| `ON_FIRE` | 着火 |
| `LAVA` | 熔岩 |
| `HOT_FLOOR` | 热地板 |
| `IN_WALL` | 墙内 |
| `CRAMMING` | 挤压 |
| `DROWN` | 溺水 |
| `DRY_OUT` | 干渴 |
| `STARVE` | 饥饿 |
| `CACTUS` | 仙人掌 |
| `FALL` | 摔落 |
| `FLY_INTO_WALL` | 撞墙 |
| `OUT_OF_WORLD` | 虚空 |
| `GENERIC` | 通用 |
| `MAGIC` | 魔法 |
| `WITHER` | 凋零 |
| `DRAGON_BREATH` | 龙息 |
| `SWEET_BERRY_BUSH` | 甜浆果丛 |
| `FREEZE` | 冰冻 |
| `FALLING_BLOCK` | 掉落方块 |
| `STALAGMITE` | 钟乳石 |
| `THORNS` | 荆棘 |
| `FIRE_TICK` | 燃烧伤害 |
| `SONIC_BOOM` | 声波冲击 |
| `ARROW` | 箭矢 |
| `TRIDENT` | 三叉戟 |
| `MOB_ATTACK` | 生物攻击 |
| `MOB_ATTACK_NO_AGGRO` | 生物无仇恨攻击 |
| `PLAYER_ATTACK` | 玩家攻击 |
| `PROJECTILE` | 投射物 |
| `FIREWORKS` | 烟花 |
| `SONIC` | 声波 |
| `UNATTRIBUTED_FIREBALL` | 无归属火球 |
| `WITHER_SKULL` | 凋零骷髅头 |
| `INDIRECT_MAGIC` | 间接魔法 |

---

## 注意事项

### 版本差异
- NeoForge 1.21.x 使用 `DamageType` 注册表
- 伤害消息使用组件系统
- `DamageScaling` 替代旧版枚举

### 常见错误
1. **伤害不生效**：`hurt` 返回 false 表示伤害被免疫
2. **死亡消息缺失**：检查翻译键是否正确定义
3. **护甲无效**：检查是否使用了 `bypassArmor`

### 最佳实践

```java
// 推荐：使用辅助方法创建 DamageSource
public static DamageSource causeCustomDamage(
        DamageSources sources,
        LivingEntity entity,
        float amount) {
    return sources.magic()
        .type(ModDamageTypes.MAGIC_DAMAGE.get())
        .amount(amount);
}
```

---

## 关联引用

- 实体：[NeoForge-实体](./NeoForge-实体.md)
- LivingEntity：[NeoForge-实体-LivingEntity](./NeoForge-实体-LivingEntity.md)
- 事件系统：[NeoForge-概念-事件](./NeoForge-概念-事件.md)
