# NeoForge 附魔系统

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/resources/server/enchantments

## 概述

附魔系统用于创建自定义附魔和配置附魔效果。

## API 速查表

### 核心类型

| 类型 | 说明 |
|------|------|
| `Enchantment` | 附魔基类 |
| `EnchantmentType` | 附魔类型 |
| `EnchantmentInstance` | 附魔实例 |

---

## 代码示例

### 创建附魔

```java
// 1. 创建附魔
public static final DeferredHolder<Enchantment, Enchantment> 
    CUSTOM_ENCHANTMENT = ENCHANTMENTS.register(
        "custom_enchantment",
        () -> new Enchantment(
            Enchantment.Rarity.RARE,      // 稀有度
            EnchantmentType.TRIDENT,      // 适用的物品类型
            EquipmentSlotGroup.HANDS)    // 装备槽位
        {
            @Override
            public void doPostAttack(
                    LivingEntity user, 
                    LivingEntity target, 
                    int level) {
                // 攻击后触发
                target.setSecondsOnFire(2 * level);
            }
            
            @Override
            public int getMaxLevel() {
                return 5;  // 最大等级
            }
            
            @Override
            public float getDamageBonus(int level, 
                    DamageSource source) {
                return level * 0.5f;
            }
        }
    );
```

### 附魔配置

```java
// 1. 在附魔构建器中配置
public static final DeferredHolder<Enchantment, Enchantment> 
    MY_ENCHANTMENT = ENCHANTMENTS.register(
        "my_enchantment",
        () -> Enchantment.builder(
                Enchantment.Rarity.UNCOMMON,
                EnchantmentType.DIGGER,
                EquipmentSlotGroup.MAINHAND
            )
            .damage(level -> 1.0f + level * 0.5f)
            .onAttack((user, target, level) -> {
                // 攻击回调
            })
            .build()
    );
```

---

## 关联引用

- 物品系统：[NeoForge-物品](./NeoForge-物品.md)
- 标签系统：[NeoForge-服务端-标签](./NeoForge-服务端-标签.md)
