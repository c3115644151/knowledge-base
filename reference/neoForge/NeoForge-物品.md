# NeoForge 物品开发

## 注册物品

### 基本注册流程

```java
// 1. 创建 DeferredRegister
public static final DeferredRegister.Items ITEMS = 
    DeferredRegister.createItems(MOD_ID);

// 2. 注册物品
public static final DeferredItem<Item> EXAMPLE_ITEM = ITEMS.registerItem(
    "example_item",
    Item::new,                  // 工厂方法
    props -> props              // 属性配置
);

// 3. 注册简单物品（更简洁）
public static final DeferredItem<Item> SIMPLE_ITEM = 
    ITEMS.registerSimpleItem("simple_item");

// 4. 注册方块物品（自动创建BlockItem）
public static final DeferredItem<BlockItem> BLOCK_ITEM =
    ITEMS.registerSimpleBlockItem(
        "example_block",
        ModBlocks.EXAMPLE_BLOCK
    );
```

⚠️ **Item.Properties 必须设置 ID（26.1 新增）**：

```java
// 正确：工厂函数接收 id 参数
public static final DeferredItem<Item> MY_ITEM = ITEMS.register(
    "my_item",
    id -> new Item(new Item.Properties().setId(ResourceKey.create(Registries.ITEM, id)))
);
```

错误：`new Item.Properties())` 不设置 ID → 运行时报 "Item id not set" NPE。

### Item.Properties 常用方法

| 方法 | 说明 |
|------|------|
| `setId()` | 设置资源键（**必须**） |
| `overrideDescription()` | 设置物品翻译键，存储在 `DataComponents#ITEM_NAME` |
| `useBlockDescriptionPrefix()` | 便捷方法，调用 `overrideDescription` 设置方块翻译键 |
| `requiredFeatures()` | 设置所需特性标志（用于版本特性锁定） |
| `stacksTo(int)` | 最大堆叠数（默认64） |
| `durability(int)` | 耐久度（设置后堆叠数自动变为1） |
| `fireResistant()` | 防火属性（通过 `DataComponents#FIRE_RESISTANT`） |
| `rarity(Rarity)` | 稀有度（COMMON/UNCOMMON/RARE/EPIC） |
| `setNoCombineRepair()` | 禁用砂轮和合成台修复 |
| `jukeboxPlayable()` | 设置唱片机播放的数据包 `JukeboxSong` 资源键 |
| `food(FoodProperties)` | 食物属性 |
| `craftRemainder(Item)` | 合成后残留物 |
| `useCooldown(double)` | 使用冷却时间（秒，通过 `DataComponents#USE_COOLDOWN`） |
| `usingConvertsTo(Item)` | 使用后转换物品（存储在 `DataComponents#USE_REMAINDER`） |
| `enchantable(int)` | 设置最大附魔值（通过 `DataComponents#ENCHANTABLE`） |
| `repairable()` | 设置修复物品或标签（通过 `DataComponents#REPAIRABLE`） |
| `equippable()` | 设置可装备槽位（通过 `DataComponents#EQUIPPABLE`） |
| `equippableUnswappable()` | 同上，但禁用快捷交换 |

### 工具和护甲额外属性

- `enchantable` - 设置最大附魔值，允许物品被附魔
- `repairable` - 设置可用于修复耐久度的物品或标签
- `equippable` - 设置物品可装备到的槽位
- `equippableUnswappable` - 同上，但禁用使用物品按钮的快速交换

### 食物属性

```java
FoodProperties food = FoodProperties.Builder()
    .nutrition(4)                    // 饱食度
    .saturationModifier(0.3f)        // 饱和度
    .meat()                         // 可喂食狼
    .effect(() -> new MobEffectInstance(
        MobEffects.MOVEMENT_SPEED,   // 效果
        200,                        // 持续时间(ticks)
        0                           // 等级
    ), 1.0f)                        // 概率
    .alwaysEdible()                 // 总是可食用（即使饱腹）
    .fast()                         // 快速食用
    .build();
```

---

## 自定义物品类

```java
public class CustomItem extends Item {
    public CustomItem() {
        super(Item.Properties.of()
            .setId(ResourceKey.create(Registries.ITEM, 
                Identifier.fromNamespaceAndPath(MOD_ID, "custom_item")))
            .stacksTo(64)
            .durability(100)
        );
    }
    
    @Override
    public InteractionResult useOn(
            UseOnContext context) {
        // 在方块上使用（右击方块）
        Level level = context.getLevel();
        BlockPos pos = context.getClickedPos();
        // ...
        return InteractionResult.SUCCESS;
    }
}
```

### 常用方法重写

| 方法 | 触发时机 |
|------|----------|
| `useOn()` | 右键点击方块 |
| `use()` | 右键使用物品 |
| `finishUsingItem()` | 使用完毕时（如吃食物） |
| `releaseUsing()` | 释放使用（如弓） |
| `hurtEnemy()` | 左键攻击实体 |
| `mineBlock()` | 挖掘方块 |
| `inventoryTick()` | 物品在背包中每tick |

### 右键使用示例

```java
@Override
public InteractionResult useOn(UseOnContext context) {
    Level level = context.getLevel();
    Player player = context.getPlayer();
    BlockPos pos = context.getClickedPos();
    
    if (!level.isClientSide()) {
        // 服务端逻辑
        player.sendSystemMessage(
            Component.literal("Clicked at: " + pos)
        );
        return InteractionResult.SUCCESS;
    }
    return InteractionResult.PASS;
}
```

---

## 物品交互

### 玩家交互事件

```java
@SubscribeEvent
public static void onPlayerInteract(
        PlayerInteractEvent.RightClickBlock event) {
    Level level = event.getLevel();
    Player player = event.getEntity();
    ItemStack stack = event.getItemStack();
    BlockPos pos = event.getPos();
    Direction face = event.getFace();
    
    if (stack.is(MyItems.MY_ITEM.get())) {
        // 处理物品使用
        if (!level.isClientSide()) {
            // 服务端逻辑
            player.swing(InteractionHand.MAIN_HAND);
        }
        event.setCancellationResult(InteractionResult.SUCCESS);
    }
}
```

### 交互类型

| 事件 | 说明 |
|------|------|
| `PlayerInteractEvent.RightClickBlock` | 右键方块 |
| `PlayerInteractEvent.RightClickItem` | 右键手持物品 |
| `PlayerInteractEvent.LeftClickBlock` | 左键方块 |
| `PlayerInteractEvent.LeftClickEmpty` | 左键空气 |
| `PlayerInteractEvent.EntityInteract` | 右键实体 |
| `PlayerInteractEvent.EntityInteractSpecific` | 右键特定实体 |

---

## 数据组件 (Data Components)

### 概述
数据组件是可附加到物品栈的自定义数据，支持序列化。

### 创建自定义数据组件

```java
// 1. 定义 Record
public record EnergyData(int energy, int capacity) 
    implements Component, ComponentPatch<ItemStack> {
    
    public static final StreamCodec<ByteBuf, EnergyData> STREAM_CODEC = 
        StreamCodec.composite(
            VarInt.MAX_CODEC,
            EnergyData::energy,
            VarInt.MAX_CODEC,
            EnergyData::capacity,
            EnergyData::new
        );
}

// 2. 注册组件
public static final DeferredRegister.DataComponents DATA_COMPONENTS =
    DeferredRegister.createDataComponents(MOD_ID);

public static final DeferredHolder<DataComponentType<EnergyData>, 
    DataComponentType<EnergyData>> ENERGY = DATA_COMPONENTS.register(
    "energy",
    () -> DataComponentType.<EnergyData>builder()
        .persistent(EnergyData.CODEC)        // 持久化编解码器
        .networkSynchronized(EnergyData.STREAM_CODEC)  // 网络同步
        .build()
);
```

### 使用数据组件

```java
// 设置
itemStack.set(DataComponents.CUSTOM_DATA, new CustomData(value));

// 获取
CustomData data = itemStack.get(DataComponents.CUSTOM_DATA);
if (data != null) {
    int value = data.value();
}

// 检查
boolean has = itemStack.has(DataComponents.CUSTOM_DATA);

// 更新
itemStack.update(DataComponents.CUSTOM_DATA, 
    oldData -> new CustomData(oldData.value() + 1));

// 移除
itemStack.remove(DataComponents.CUSTOM_DATA);
```

---

## 工具与盔甲

### 工具属性

```java
Item.Properties.of()
    .attributes(
        SwordItem.createAttributes(
            Tier.DIAMOND,    // 材质
            3.0f,           // 伤害
            -2.4f           // 攻击速度
        )
    )
    .enchantable(10)      // 可附魔等级
    .repairable(Provider.tag(ItemTags.DIAMOND_TOOL_MATERIALS));  // 修复材料
```

### 盔甲属性

```java
Item.Properties.of()
    .attributes(
        ArmorItem.createAttributes(
            ArmorMaterials.DIAMOND,  // 材质
            ArmorItem.Type.HELMET,   // 类型
            EquipmentSlot.HEAD      // 装备槽
        )
    )
    .enchantable(15)
    .equippable(EquipmentSlot.HEAD);  // 可装备
```

### 装备事件

```java
@SubscribeEvent
public static void onEquip(
        EquipmentChangeEvent event) {
    ItemStack oldItem = event.getOldItem();
    ItemStack newItem = event.getNewItem();
    EquipmentSlot slot = event.getSlot();
    
    if (newItem.is(MyItems.CUSTOM_ARMOR.get())) {
        // 装备新物品
    }
}
```

---

## 创造模式标签

### 添加到现有标签

```java
@SubscribeEvent
public static void buildContents(
        BuildCreativeModeTabContentsEvent event) {
    // 添加到 BUILDABLE 或其他标签
    if (event.getTabKey() == CreativeModeTabs.BUILDING_BLOCKS) {
        event.accept(MyItems.MY_ITEM.get());
    }
}
```

### 创建自定义标签

```java
public static final DeferredRegister<CreativeModeTab> CREATIVE_TABS =
    DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MOD_ID);

public static final Supplier<CreativeModeTab> MY_TAB = 
    CREATIVE_TABS.register("my_tab", () ->
        CreativeModeTab.builder()
            .title(Component.translatable("itemGroup." + MOD_ID + ".my_tab"))
            .icon(() -> new ItemStack(MyItems.MY_ITEM.get()))
            .displayItems((params, output) -> {
                output.accept(MyItems.MY_ITEM.get());
            })
            .build()
    );
```

---

## ItemStack 操作

### 基本操作

```java
ItemStack stack = new ItemStack(Items.DIAMOND, 5);

// 检查
stack.isEmpty();
stack.is(Items.DIAMOND);
stack.has(DataComponents.ENCHANTMENTS);

// 数量
stack.getCount();
stack.setCount(3);
stack.shrink(1);  // 减少

// 复制
ItemStack copy = stack.copy();
```

### JSON 表示

```json
{
    "id": "minecraft:diamond",
    "count": 5,
    "components": {
        "minecraft:enchantment_glint_override": true
    }
}
```

---

## 注意事项

- ⚠️ `Item` 代表物品类型，`ItemStack` 代表具体堆叠实例
- ⚠️ 服务端逻辑使用 `!level.isClientSide()` 检查
- ⚠️ 修改 ItemStack 需要注意可变性，必要时使用 `copy()`
- ⚠️ 物品模型和纹理需要资源文件

## 关联文档
- [NeoForge-资源.md](./NeoForge-资源.md) - 资源文件（模型、纹理）
- [NeoForge-方块实体.md](./NeoForge-方块实体.md) - 方块实体数据同步
