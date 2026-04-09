# NeoForge 工具制作

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/items/tools

## 概述

NeoForge 1.21.x 引入了新的工具和盔甲材料系统，使用 `ToolMaterial` 和 `ArmorMaterial` 来定义工具的挖掘速度、耐久度、附魔等级等属性。

## API 速查表

### 核心类型

| 类型 | 说明 |
|------|------|
| `ToolMaterial` | 工具材料 |
| `Tier` | 工具等级接口 |
| `TierProperty` | 工具等级属性 |
| `ItemAbility` | 物品能力 |
| `Tool` | 工具组件 |
| `DamageType` | 伤害类型 |

### ToolMaterial 属性

| 属性 | 说明 |
|------|------|
| `attackDamageBonus` | 额外攻击伤害 |
| `enchantmentValue` | 附魔价值（影响附魔表） |
| `repairIngredient` | 修复材料 |
| `speed` | 挖掘速度 |
| `durability` | 耐久度 |

### 内置材料等级

| 等级 | 说明 |
|------|------|
| `Tiers.WOOD` | 木质 |
| `Tiers.STONE` | 石质 |
| `Tiers.IRON` | 铁质 |
| `Tiers.DIAMOND` | 钻石 |
| `Tiers.GOLD` | 金质 |
| `Tiers.NETHERITE` | 下界合金 |

---

## 代码示例

### 创建自定义工具材料

```java
// 1. 创建工具材料
public static final ToolMaterial EMERALD_TOOL_MATERIAL = 
    new ToolMaterial(
        2500,           // 耐久度
        12.0f,          // 挖掘速度
        4.5f,           // 额外攻击伤害
        25,             // 附魔价值
        15,             // 修复材料价值
        () -> Ingredient.of(Items.EMERALD)  // 修复材料
    );

// 2. 注册为 Tier（可选，用于 Pickaxe 等）
public static final Tier EMERALD_TIER = new Tier() {
    @Override
    public int getUses() {
        return 2500;
    }
    
    @Override
    public float getSpeed() {
        return 12.0f;
    }
    
    @Override
    public float getAttackDamageBonus() {
        return 4.5f;
    }
    
    @Override
    public int getLevel() {
        return 4;  // 对应附魔等级
    }
    
    @Override
    public int getEnchantmentValue() {
        return 25;
    }
    
    @Override
    public Ingredient getRepairIngredient() {
        return Ingredient.of(Items.EMERALD);
    }
};

// 3. 使用 DeferredRegister 注册
private static final DeferredRegister<Tier> TIERS = 
    DeferredRegister.create(NeoForgeRegistries.Keys.TOOL_TIERS, MOD_ID);

public static final DeferredHolder<Tier, Tier> EMERALD = 
    TIERS.register("emerald", () -> EMERALD_TIER);
```

### 创建自定义工具

```java
// 1. 创建剑
public static final DeferredItem<SwordItem> EMERALD_SWORD = 
    ITEMS.registerItem(
        "emerald_sword",
        props -> new SwordItem(
            EMERALD_TIER,           // 工具材料
            5,                      // 基础攻击力
            -2.0f,                  // 攻击速度修正
            new Item.Properties()
        ),
        Item.Properties::stacksTo
    );

// 2. 创建镐子
public static final DeferredItem<PickaxeItem> EMERALD_PICKAXE = 
    ITEMS.registerItem(
        "emerald_pickaxe",
        props -> new PickaxeItem(
            EMERALD_TIER,
            3,                      // 攻击力
            -2.8f,                  // 攻击速度
            new Item.Properties()
        ),
        Item.Properties::stacksTo
    );

// 3. 创建斧头
public static final DeferredItem<AxeItem> EMERALD_AXE = 
    ITEMS.registerItem(
        "emerald_axe",
        props -> new AxeItem(
            EMERALD_TIER,
            6,                      // 攻击力
            -3.2f,                  // 攻击速度
            new Item.Properties()
        ),
        Item.Properties::stacksTo
    );

// 4. 创建铲子
public static final DeferredItem<ShovelItem> EMERALD_SHOVEL = 
    ITEMS.registerItem(
        "emerald_shovel",
        props -> new ShovelItem(
            EMERALD_TIER,
            2.5f,                   // 攻击力
            -3.0f,                  // 攻击速度
            new Item.Properties()
        ),
        Item.Properties::stacksTo
    );

// 5. 创建锄头
public static final DeferredItem<HoeItem> EMERALD_HOE = 
    ITEMS.registerItem(
        "emerald_hoe",
        props -> new HoeItem(
            EMERALD_TIER,
            1,                      // 攻击力
            -3.0f,                  // 攻击速度
            new Item.Properties()
        ),
        Item.Properties::stacksTo
    );
```

### 使用 Tool 组件（NeoForge 1.21.x）

```java
// 创建带 Tool 组件的物品（替代旧版 Digger）
public static final DeferredItem<Item> CUSTOM_PICKAXE = 
    ITEMS.registerItem(
        "custom_pickaxe",
        Item::new,
        props -> props
            .attributes(createToolAttributes(
                TierProperties.create()
                    .durability(1500)
                    .speed(10.0f)
                    .attackDamageBonus(3.0f)
                    .enchantmentValue(20)
                    .repairIngredient(() -> 
                        Ingredient.of(Items.DIAMOND))))
            .component(DataComponents.TOOL, 
                new Tool(
                    Collections.emptyList(),  // 破坏效果
                    8.0f                      // 挖掘速度
                ))
    );

// ToolTier 注册
private static final DeferredRegister<ToolTier> TOOL_TIERS = 
    DeferredRegister.create(NeoForgeRegistries.Keys.TOOL_TIERS, MOD_ID);

public static final DeferredHolder<ToolTier, ToolTier> MY_TIER = 
    TOOL_TIERS.register("my_tier", () -> 
        ToolTier.create(
            1500,       // 耐久度
            10.0f,      // 速度
            3.0f,       // 攻击加成
            20,         // 附魔价值
            15,         // 修复价值
            () -> Ingredient.of(Items.DIAMOND)
        ));
```

### 自定义破坏效果

```java
// 定义破坏效果
public static final ToolRule MY_RULE = ToolRule.event(
    // 规则条件
    BlockIngestSet.of(BlockTags.MINEABLE_PICKAXE),
    // 破坏时给予物品
    ToolAction.DEFAULT_PICKAXE_DIGGING,
    // 效果
    (level, pos, state, player, stack) -> {
        // 在服务端执行
        if (!level.isClientSide) {
            // 生成额外物品
            ItemEntity item = new ItemEntity(
                level, 
                pos.getX() + 0.5, 
                pos.getY() + 0.5, 
                pos.getZ() + 0.5,
                new ItemStack(Items.DIAMOND));
            level.addFreshEntity(item);
        }
        return ToolActionResult.SUCCESS;
    }
);

// 注册到工具
public static final DeferredItem<Item> LUCKY_PICKAXE = 
    ITEMS.registerItem(
        "lucky_pickaxe",
        Item::new,
        props -> props
            .attributes(createToolAttributes(
                TierProperties.of(Tiers.DIAMOND)))
            .component(DataComponents.TOOL, 
                new Tool(
                    List.of(MY_RULE),
                    8.0f)));
```

### 物品能力 (ItemAbility)

```java
// 定义自定义能力
public static final ItemAbility BIND_CURSE = 
    ItemAbility.register("examplemod:bind_curse");

// 使用能力
public static final DeferredItem<Item> CURSED_PICKAXE = 
    ITEMS.registerItem(
        "cursed_pickaxe",
        Item::new,
        props -> props
            .attributes(createToolAttributes(
                TierProperties.of(Tiers.DIAMOND)))
            .component(ItemAbility.ITEM_ACTION, 
                ItemAbilityEntry.of(
                    List.of(BIND_CURSE)))
    );

// 检查物品能力
if (stack.has(ItemAbility.BIND_CURSE)) {
    // 处理绑定诅咒逻辑
}
```

---

## 工具等级速查

| 等级 | 耐久 | 速度 | 攻击加成 | 附魔价值 |
|------|------|------|----------|----------|
| Wood | 59 | 2.0 | 0.0 | 15 |
| Stone | 131 | 4.0 | 1.0 | 5 |
| Iron | 250 | 6.0 | 2.0 | 14 |
| Diamond | 1561 | 8.0 | 3.0 | 10 |
| Gold | 32 | 12.0 | 0.0 | 22 |
| Netherite | 2031 | 9.0 | 4.0 | 15 |

---

## 注意事项

### 版本差异
- NeoForge 1.21.x 使用 `ToolMaterial` / `Tier` 替代旧版 `Tier`
- 工具属性通过 `Item#attributes()` 或 `ToolComponent` 设置
- `Digger` 类已被废弃

### 常见错误
1. **工具无法挖掘**：未正确设置 `Tier` 或未添加 `mineable/*` 标签
2. **附魔异常**：检查 `enchantmentValue` 是否合理
3. **耐久度问题**：基础耐久不包含修复加成

### 最佳实践

```java
// 推荐：使用 ToolTier DeferredRegister
private static final DeferredRegister<ToolTier> TOOL_TIERS = 
    DeferredRegister.create(NeoForgeRegistries.Keys.TOOL_TIERS, MOD_ID);

public static final DeferredHolder<ToolTier, ToolTier> MY_TIER = 
    TOOL_TIERS.register("my_tier", () -> 
        ToolTier.create(
            1500,       // 耐久
            10.0f,      // 速度
            3.0f,       // 攻击
            20,         // 附魔
            15,         // 修复
            () -> Ingredient.of(Items.DIAMOND)
        ));

// 在事件中注册方块标签
@SubscribeEvent
public static void addMineable(AddToolModifiersEvent event) {
    event.addBlock(
        BlockTags.MINEABLE_PICKAXE, 
        MY_TIER.get());
}
```

---

## 关联引用

- 物品基础：[NeoForge-物品](./NeoForge-物品.md)
- 数据组件：[NeoForge-物品-数据组件](./NeoForge-物品-数据组件.md)
- 护甲制作：[NeoForge-物品-护甲](./NeoForge-物品-护甲.md)
- 方块标签：[NeoForge-服务端-标签](./NeoForge-服务端-标签.md)
