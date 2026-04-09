# NeoForge 护甲制作

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/items/armor

## 概述

NeoForge 1.21.x 使用 `ArmorMaterial` 和 `Equippable` 组件系统来创建和管理护甲装备，提供护甲值、韧性、附魔能力等功能。

## API 速查表

### 核心类型

| 类型 | 说明 |
|------|------|
| `ArmorMaterial` | 护甲材料 |
| `ArmorItem` | 护甲物品 |
| `ArmorItem.Type` | 护甲类型（头盔/胸甲等） |
| `Equippable` | 装备组件 |
| `EquipmentClientInfo` | 装备客户端信息 |
| `EquipmentLayer` | 装备层定义 |

### ArmorMaterial 属性

| 属性 | 说明 |
|------|------|
| `durabilityFunction` | 耐久度计算函数 |
| `damageReduction` | 伤害减免数组 |
| `enchantmentValue` | 附魔价值 |
| `equipSound` | 装备音效 |
| `repairIngredient` | 修复材料 |
| `toughness` | 韧性值 |
| `knockbackResistance` | 击退抗性 |

### 护甲类型

| 类型 | 护甲槽位 | 索引 |
|------|----------|------|
| `HELMET` | 头部 | 0 |
| `CHESTPLATE` | 胸部 | 1 |
| `LEGGINGS` | 腿部 | 2 |
| `BOOTS` | 脚部 | 3 |

---

## 代码示例

### 创建护甲材料

```java
// 1. 使用 ArmorMaterials 内置材料
public static final ArmorMaterial DIAMOND_ARMOR = ArmorMaterials.DIAMOND;
public static final ArmorMaterial NETHERITE_ARMOR = ArmorMaterials.NETHERITE;

// 2. 创建自定义材料
public static final DeferredHolder<ArmorMaterial, 
        ArmorMaterial> EMERALD_ARMOR = ARMOR_MATERIALS.register(
    "emerald",
    () -> ArmorMaterial.builder()
        .durability(Portal.DIAMOND,  // 基于钻石的耐久倍数
            15, 24, 21, 13)           // 各部位耐久值
        .protection(3, 8, 6, 3)       // 各部位护甲值
        .enchantmentValue(25)
        .equipSound(SoundEvents.ARMOR_EQUIP_DIAMOND)
        .repairIngredient(() -> 
            Ingredient.of(Items.EMERALD))
        .toughness(2.0f)
        .knockbackResistance(0.1f)
        .build()
);

// 3. 更灵活的创建方式
public static final ArmorMaterial CUSTOM_ARMOR = 
    ArmorMaterial.builder()
        .durabilityFunction(
            DurabilityFunction.or(
                Portal.bonus(1.5f),     // 1.5倍基础耐久
                Portal.constant(500)    // 固定500耐久
            ))
        .protection(
            2,   // HELMET
            6,   // CHESTPLATE
            4,   // LEGGINGS
            2    // BOOTS
        )
        .enchantmentValue(15)
        .equipSound(SoundEvents.ARMOR_EQUIP_GENERIC)
        .repairIngredient(() -> 
            Ingredient.of(Items.GOLD_INGOT))
        .toughness(1.0f)
        .knockbackResistance(0.0f)
        .build("examplemod:custom_armor");
```

### 创建护甲物品

```java
// 1. 注册护甲槽位
private static final DeferredRegister<ArmorTrimMaterial> 
    ARMOR_TRIM_MATERIALS = 
    DeferredRegister.create(NeoForgeRegistries.Keys.ArmorTrimMaterials, MOD_ID);

// 2. 创建护甲物品
public static final DeferredItem<ArmorItem> EMERALD_HELMET = 
    ITEMS.registerItem(
        "emerald_helmet",
        props -> new ArmorItem(
            EMERALD_ARMOR.get(),        // 护甲材料
            ArmorItem.Type.HELMET,      // 护甲类型
            new Item.Properties()
        ),
        Item.Properties::stacksTo
    );

public static final DeferredItem<ArmorItem> EMERALD_CHESTPLATE = 
    ITEMS.registerItem(
        "emerald_chestplate",
        props -> new ArmorItem(
            EMERALD_ARMOR.get(),
            ArmorItem.Type.CHESTPLATE,
            new Item.Properties()
        ),
        Item.Properties::stacksTo
    );

// 重复 LEGGINGS 和 BOOTS...
```

### 使用 Equippable 组件

```java
// 创建可装备物品（不仅限于护甲）
public static final DeferredItem<Item> WING_CLOAK = 
    ITEMS.registerItem(
        "wing_cloak",
        Item::new,
        props -> props
            .stacksTo(1)
            .rarity(Rarity.RARE)
            .component(DataComponents.EQUIPPABLE, 
                Equippable.builder(EquipmentSlot.CAPE)
                    .interchangeable()  // 可与其他CAPE互换
                    .build())
    );

// 自定义装备动画
public static final DeferredItem<Item> POWER_BRACELET = 
    ITEMS.registerItem(
        "power_bracelet",
        Item::new,
        props -> props
            .stacksTo(1)
            .component(DataComponents.EQUIPPABLE,
                Equippable.builder(EquipmentSlot.OFFHAND)
                    .swappable()  // 可切换主副手
                    .build())
    );
```

### 自定义装备渲染信息

```java
// 1. 在 assets/modid/models/item/custom_equipment.json
{
    "parent": "minecraft:item/generated",
    "textures": {
        "layer0": "examplemod:item/custom_equipment"
    },
    // 装备时的纹理
    "overrides": [
        {
            "predicate": {
                "custom_model_data": 1
            },
            "model": "examplemod:item/equipment_offhand"
        }
    ]
}

// 2. 装备时的骨骼和渲染（需要自定义渲染器）
public class CustomEquipmentRenderer {
    public static void register() {
        // 注册自定义装备渲染
        ClientRegistry.registerEquipmentRenderer(
            MOD_ID + ":custom_equipment",
            ctx -> new CustomEquipmentRenderer(ctx)
        );
    }
}
```

### 护甲属性计算

```java
// 护甲值计算公式
// 总护甲值 = Σ(部位护甲值)
// 伤害减免 = 0.02 * 总护甲值 / (0.02 * 总护甲值 + 总韧性 + 2)

// 韧性效果
// 有效护甲 = 总护甲 + 总韧性 / 4

// 伤害减免上限约80%（20护甲+10韧性）

// 击退抗性
// 击退减少量 = knockbackResistance * 0.1
// 最大击退抗性 = 1.0 (完全免疫击退)

// 代码中访问护甲属性
public static float getDamageReduction(ArmorItem item, 
        DamageSource source) {
    // 通过 ArmorMaterial 获取
    return item.getMaterial().getDefenseForType(
        item.getType(), source);
}
```

### 修复护甲

```java
// 1. 通过 ArmorMaterial 自动支持
// .repairIngredient() 中指定的材料

// 2. 自定义修复逻辑
public class RepairableArmorItem extends ArmorItem {
    public RepairableArmorItem(ArmorMaterial material, 
            Type type, Properties properties) {
        super(material, type, properties);
    }
    
    @Override
    public boolean isValidRepairItem(ItemStack toRepair, 
            ItemStack repair) {
        if (!toRepair.isDamaged()) return false;
        
        // 自定义修复逻辑
        return repair.is(Items.EMERALD) 
            && toRepair.getDamageValue() >= 
                toRepair.getMaxDamage() - 10;
    }
}
```

---

## 护甲材料参考

| 材料 | 耐久倍数 | 护甲值(H/C/L/B) | 韧性 | 附魔价值 |
|------|----------|-----------------|------|----------|
| Leather | 1.0x | 1/2/1/1 | 0.0 | 15 |
| Chain | 1.0x | 1/4/2/1 | 0.0 | 12 |
| Iron | 1.0x | 2/6/4/2 | 0.0 | 9 |
| Diamond | 1.0x | 3/8/6/3 | 2.0 | 10 |
| Gold | 1.0x | 1/5/3/1 | 0.0 | 25 |
| Netherite | 1.0x | 3/8/6/3 | 3.0 | 15 |
| Turtle | 1.0x | 2/6/5/2 | 0.0 | 9 |

---

## 注意事项

### 版本差异
- NeoForge 1.21.x 使用 `ArmorMaterial` 而非旧版 `ArmorMaterial`
- 护甲值存储在 `ArmorMaterial` 中，而非 `ArmorItem`
- 使用 `Equippable` 组件替代旧版 `EquipmentSlot` 逻辑

### 常见错误
1. **护甲值异常**：检查耐久倍数和护甲值数组索引
2. **装备无效**：确保 `Equippable` 组件配置正确
3. **渲染问题**：装备纹理需要正确配置 JSON

### 最佳实践

```java
// 推荐：集中管理护甲材料
public static class ModArmorMaterials {
    public static final DeferredHolder<ArmorMaterial, 
            ArmorMaterial> CRYSTAL = 
        ARMOR_MATERIALS.register("crystal", () -> 
            ArmorMaterial.builder()
                .durability(Portal.constant(500))
                .protection(3, 8, 5, 3)
                .enchantmentValue(20)
                .equipSound(SoundEvents.ARMOR_EQUIP_GENERIC)
                .repairIngredient(() -> 
                    Ingredient.of(Items.AMETHYST_SHARD))
                .toughness(2.5f)
                .knockbackResistance(0.0f)
                .build());
}

// 创建全套护甲的辅助方法
public static DeferredItem<ArmorItem> createArmor(
        String name, 
        ArmorMaterial material, 
        ArmorItem.Type type) {
    return ITEMS.registerItem(
        name,
        props -> new ArmorItem(material, type, props),
        Item.Properties::stacksTo
    );
}
```

---

## 关联引用

- 物品基础：[NeoForge-物品](./NeoForge-物品.md)
- 数据组件：[NeoForge-物品-数据组件](./NeoForge-物品-数据组件.md)
- 工具制作：[NeoForge-物品-工具](./NeoForge-物品-工具.md)
- 实体属性：[NeoForge-实体-属性](./NeoForge-实体-属性.md)
